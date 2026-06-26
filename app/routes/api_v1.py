# API v1 Routes - main API endpoints for version 1 of the RESTful API
from typing import Dict, Any, List

import structlog
from flask import Blueprint, jsonify, request, render_template
from flasgger import swag_from

from app.simulations.qkd.bb84 import BB84
from app.simulations.attacks.intercept_resend import InterceptResend, PartialIntercept
from app.simulations.attacks.pns import PNS

logger = structlog.get_logger(__name__)

bp = Blueprint("api_v1", __name__)




# Get all items - returns a list of all items in the system with pagination
@bp.route("/items", methods=["GET"])
def get_items() -> Dict[str, Any]:
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    logger.info("Items requested", page=page, per_page=per_page)

    # Placeholder response - replace with actual database query
    return jsonify(
        {
            "items": [],
            "total": 0,
            "page": page,
            "per_page": per_page,
        }
    )


# Get a specific item by ID
@bp.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id: int) -> Dict[str, Any]:
    logger.info("Item requested", item_id=item_id)

    # Placeholder response - replace with actual database query
    return jsonify({"id": item_id, "name": "Sample Item"}), 200


# Create a new item
@bp.route("/items", methods=["POST"])
def create_item() -> Dict[str, Any]:
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    logger.info("Item creation requested", name=data.get("name"))

    # Placeholder response - replace with actual database insert
    return jsonify(
        {
            "id": 1,
            "name": data["name"],
            "message": "Item created successfully",
        }
    ), 201

@bp.route("/", methods=["GET"])
def page() -> str:
    logger.info("Page requested")
    return render_template("index.html", message="Hello from Flask!")


@bp.route("/bb84/simulate", methods=["POST"])
def simulate_bb84():
    try:
        data = request.get_json()
        
        n_photons = data.get("n_photons", 10000)
        noise = data.get("noise", 0.02)
        attack_type = data.get("attack_type", "none")
        attack_params = data.get("attack_params", {})
        
        # Create Eve attack
        eve = None
        if attack_type == "intercept_resend":
            eve = InterceptResend()
        elif attack_type == "partial_intercept":
            rate = attack_params.get("rate", 0.2)
            eve = PartialIntercept(rate=rate)
        elif attack_type == "pns":
            mu = attack_params.get("mu", 0.1)
            eve = PNS(mu=mu)
        
        logger.info(
            "bb84_simulation_started",
            n_photons=n_photons,
            noise=noise,
            attack_type=attack_type
        )
        
        bb84 = BB84(n_photons=n_photons, noise=noise)
        result = bb84.run(eve=eve)
        
        # ✅ FIXED: Pakai attribute yang bener
        response = {
            "success": True,
            "n_photons": result.n_photons,
            "noise": noise,
            "attack_type": attack_type,
            "qber": result.qber,
            "sifted_key_length": result.n_sifted,  # ✅ GANTI: len(result.sifted_key) → result.n_sifted
            "eve_information": result.eve_information,
            "n_errors": result.n_errors,
            "n_intercepted": result.n_intercepted,
            "eve_correct": result.eve_correct,
            "summary": {
                "total_photons": result.n_photons,
                "sifted_bits": result.n_sifted,
                "errors": result.n_errors,
                "eve_intercepted": result.n_intercepted,
                "eve_correct_guesses": result.eve_correct,
                "qber_percent": round(result.qber * 100, 2),
                "eve_info_bits": round(result.eve_information, 4)
            }
        }
        
        logger.info(
            "bb84_simulation_completed",
            qber=response["qber"],
            sifted_key_length=response["sifted_key_length"]
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error("bb84_simulation_failed", error=str(e))
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route("/bb84/sweep", methods=["POST"])
def sweep_bb84():
    try:
        data = request.get_json()
        attack_type = data.get("attack_type", "partial_intercept")
        param_values = data.get("param_values", [0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
        noise_values = data.get("noise_values")  # ✅ BARU: buat sweep noise
        
        results = []
        
        for i, param_val in enumerate(param_values):
            eve = None
            
            # Buat Eve attack
            if attack_type == "intercept_resend":
                eve = InterceptResend()
            elif attack_type == "partial_intercept":
                eve = PartialIntercept(rate=param_val)
            elif attack_type == "pns":
                eve = PNS(mu=param_val)
            
            # ✅ Tentukan noise level
            if noise_values and i < len(noise_values):
                noise = noise_values[i]
            else:
                noise = 0.02  # Default
            
            bb84 = BB84(n_photons=10000, noise=noise)
            result = bb84.run(eve=eve)
            
            results.append({
                "param": param_val,
                "qber": result.qber,
                "eve_info": result.eve_information,
                "n_sifted": result.n_sifted,
                "n_errors": result.n_errors
            })
        
        return jsonify({
            "success": True,
            "attack_type": attack_type,
            "results": results
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
