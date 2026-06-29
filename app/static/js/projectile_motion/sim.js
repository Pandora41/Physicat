
    // ===================== P5.JS SIMULATION =====================
    let v0 = 20, angle = 45, g = 9.8, h0 = 0;
    let vx, vy, x, y, t, launched = false, paused = false;
    let trace = [], trace2 = [], mode = 'normal';
    let canvasW = 820, canvasH = 400;
    let scale = 8; // pixels per meter
    let groundY, launchX;
    let projectile = { r: 8, color: [255, 107, 157] };
    let trailParticles = [];

    function setup() {
        let container = document.getElementById('canvas-container');
        let canvas = createCanvas(canvasW, canvasH);
        canvas.parent(container);
        textFont('Segoe UI', 'Noto Sans JP');
        textAlign(LEFT, CENTER);
        
        groundY = canvasH - 40;
        launchX = 60;
        resetProjectile();
        updateCalculations();
    }

    function draw() {
        // Background gradient
        for (let y = 0; y < canvasH; y++) {
            let inter = map(y, 0, canvasH, 0, 1);
            let c1 = color(26, 26, 58);
            let c2 = color(35, 35, 75);
            let c = lerpColor(c1, c2, inter);
            stroke(c);
            line(0, y, canvasW, y);
        }

        // Grid
        drawGrid();
        
        // Ground
        drawGround();
        
        // Launch point marker
        drawLaunchPoint();
        
        // Update & draw projectile
        if (launched && !paused) {
            updatePhysics();
            // Check if projectile hit the ground
            if (y >= groundY) {
                y = groundY;
                launched = false;
                createImpactEffect(x, y);
            }
            if (mode === 'trace' || mode === 'compare') {
                trace.push({x: x, y: y});
                if (trace.length > 500) trace.shift();
            }
            if (mode === 'compare' && frameCount % 3 === 0) {
                trace2.push({x: x, y: y});
            }
        }
        
        // Draw trace
        if (mode === 'trace' || mode === 'compare') drawTrace(trace, color(168, 85, 247, 180));
        if (mode === 'compare') drawTrace(trace2, color(59, 130, 246, 120), true);
        
        // Draw projectile
        drawProjectile();
        
        // Draw vectors if in vector mode
        if (mode === 'vectors' && launched) drawVectors();
        
        // Draw info overlay
        drawInfoOverlay();
        
        // Update trail particles
        updateTrailParticles();
    }

    function drawGrid() {
        stroke(70, 70, 110, 60);
        strokeWeight(0.5);
        // Vertical lines (every 5m)
        for (let mx = 0; mx <= 100; mx += 5) {
            let px = launchX + mx * scale;
            if (px <= canvasW) line(px, 0, px, groundY);
        }
        // Horizontal lines (every 5m)
        for (let my = 0; my <= 50; my += 5) {
            let py = groundY - my * scale;
            if (py >= 0) line(0, py, canvasW, py);
        }
        // Axis labels
        fill(140, 140, 190);
        noStroke();
        textSize(10);
        for (let mx = 0; mx <= 100; mx += 10) {
            let px = launchX + mx * scale;
            if (px <= canvasW - 15) text(mx + 'm', px, groundY + 15);
        }
        for (let my = 0; my <= 40; my += 10) {
            let py = groundY - my * scale;
            if (py >= 20) text(my + 'm', 10, py);
        }
    }

    function drawGround() {
        // Ground
        fill(45, 55, 85);
        noStroke();
        rect(0, groundY, canvasW, canvasH - groundY);
        // Grass pattern
        stroke(80, 120, 80, 100);
        strokeWeight(1);
        for (let i = 0; i < canvasW; i += 15) {
            line(i, groundY, i + 5, groundY - 8);
            line(i + 7, groundY, i + 12, groundY - 6);
        }
        // Ground line
        stroke(100, 140, 100, 180);
        strokeWeight(2);
        line(0, groundY, canvasW, groundY);
    }

    function drawLaunchPoint() {
        // Launch platform
        fill(90, 70, 110);
        noStroke();
        rect(launchX - 20, groundY - h0*scale - 15, 40, 15, 3);
        // Launch marker
        fill(255, 180, 80);
        ellipse(launchX, groundY - h0*scale, 12, 12);
        fill(255, 220, 120);
        ellipse(launchX, groundY - h0*scale, 6, 6);
        // Angle arc
        if (!launched) {
            noFill();
            stroke(255, 150, 100, 150);
            strokeWeight(2);
            arc(launchX, groundY - h0*scale, 35, 35, PI, PI + radians(angle));
            fill(255, 180, 120);
            noStroke();
            textSize(11);
            text(nf(angle, 1, 0) + '°', launchX + 20, groundY - h0*scale - 10);
        }
    }

    function drawProjectile() {
        // Glow effect
        noStroke();
        for (let r = projectile.r + 8; r > projectile.r; r -= 2) {
            fill(projectile.color[0], projectile.color[1], projectile.color[2], map(r, projectile.r, projectile.r+8, 40, 0));
            ellipse(x, y, r*2, r*2);
        }
        // Main projectile (cute cat style)
        fill(projectile.color[0], projectile.color[1], projectile.color[2]);
        ellipse(x, y, projectile.r*2, projectile.r*2);
        // Face
        fill(255);
        ellipse(x - 3, y - 2, 4, 4);
        ellipse(x + 3, y - 2, 4, 4);
        fill(50, 50, 80);
        ellipse(x - 3, y - 2, 2, 2);
        ellipse(x + 3, y - 2, 2, 2);
        // Mouth
        noFill();
        stroke(50, 50, 80);
        strokeWeight(1.5);
        arc(x, y + 2, 6, 4, 0, PI);
        noStroke();
        // Ears
        fill(projectile.color[0], projectile.color[1], projectile.color[2]);
        triangle(x - 6, y - 8, x - 9, y - 14, x - 3, y - 11);
        triangle(x + 6, y - 8, x + 9, y - 14, x + 3, y - 11);
    }

    function drawVectors() {
        let vMag = sqrt(vx*vx + vy*vy);
        let scaleV = 3;
        
        // Velocity vector (cyan)
        stroke(59, 200, 240, 220);
        strokeWeight(2.5);
        line(x, y, x + vx*scaleV, y - vy*scaleV);
        // Arrowhead
        let angleV = atan2(-vy, vx);
        drawArrowhead(x + vx*scaleV, y - vy*scaleV, angleV, color(59, 200, 240));
        
        // Velocity components
        stroke(100, 200, 100, 180);
        strokeWeight(1.5);
        strokeDash(5);
        line(x, y, x + vx*scaleV, y); // vx
        line(x + vx*scaleV, y, x + vx*scaleV, y - vy*scaleV); // vy
        noDash();
        
        // Labels
        fill(100, 220, 255);
        noStroke();
        textSize(10);
        text('vₓ', x + vx*scaleV/2, y - 8);
        fill(120, 230, 120);
        text('vᵧ', x + vx*scaleV + 5, y - vy*scaleV/2);
        
        // Gravity vector (red, at projectile)
        stroke(255, 100, 100, 200);
        strokeWeight(2);
        let gLen = 25;
        line(x, y, x, y + gLen);
        drawArrowhead(x, y + gLen, HALF_PI, color(255, 100, 100));
        fill(255, 130, 130);
        text('g', x + 8, y + gLen/2);
    }

    function drawArrowhead(x, y, angle, col) {
        push();
        translate(x, y);
        rotate(angle);
        noStroke();
        fill(col);
        triangle(0, 0, -8, -4, -8, 4);
        pop();
    }

    function drawTrace(points, col, dashed = false) {
        if (points.length < 2) return;
        noFill();
        if (dashed) {
            strokeDash(6);
            strokeWeight(1.5);
        } else {
            strokeWeight(2);
        }
        stroke(col);
        beginShape();
        for (let p of points) {
            vertex(p.x, p.y);
        }
        endShape();
        if (dashed) noDash();
    }

    function drawInfoOverlay() {
        // Current position & velocity
        if (launched) {
            fill(30, 30, 60, 200);
            noStroke();
            rect(10, 10, 180, 75, 8);
            fill(200, 200, 240);
            textSize(11);
            text(`t = ${(t).toFixed(2)} s`, 20, 28);
            text(`x = ${((x - launchX) / scale).toFixed(2)} m`, 20, 45);
            text(`y = ${((groundY - y) / scale).toFixed(2)} m`, 20, 62);
            // Current velocity components
            let vxCurrent = vx;
            let vyCurrent = vy - g * t;
            text(`v = ${sqrt(vxCurrent*vxCurrent + vyCurrent*vyCurrent).toFixed(1)} m/s`, 120, 45);
        }
        
        // Mode indicator
        fill(60, 60, 100, 180);
        rect(canvasW - 110, 10, 100, 28, 6);
        fill(180, 200, 255);
        textSize(11);
        textAlign(CENTER, CENTER);
        let modeLabel = {normal:'🎯 ノーマル', vectors:'📐 ベクトル', trace:'👣 軌跡', compare:'🔁 比較'};
        text(modeLabel[mode], canvasW - 60, 24);
        textAlign(LEFT, CENTER);
    }

    function updatePhysics() {
        t += 1/60;
        // x = x0 + vx * t (horizontal motion is uniform)
        x = launchX + vx * t * scale;
        // y = y0 - (v0y * t - 0.5 * g * t^2) (subtract because in p5.js, y increases downward)
        y = groundY - h0 * scale - (vy * t - 0.5 * g * t * t) * scale;
        
        // Create trail particles
        if (frameCount % 2 === 0 && launched) {
            trailParticles.push({
                x: x, y: y,
                life: 30,
                size: random(2, 5),
                vx: random(-0.3, 0.3),
                vy: random(-0.5, 0.2)
            });
        }
    }

    function updateTrailParticles() {
        for (let i = trailParticles.length - 1; i >= 0; i--) {
            let p = trailParticles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life--;
            p.size *= 0.97;
            
            noStroke();
            fill(255, 150, 200, p.life * 8);
            ellipse(p.x, p.y, p.size * 2, p.size * 2);
            
            if (p.life <= 0 || p.size < 0.5) trailParticles.splice(i, 1);
        }
    }

    function createImpactEffect(impactX, impactY) {
        for (let i = 0; i < 15; i++) {
            trailParticles.push({
                x: impactX, y: impactY,
                life: 40,
                size: random(3, 7),
                vx: random(-2, 2),
                vy: random(-3, -0.5)
            });
        }
    }

    function strokeDash(d) {
        drawingContext.setLineDash([d, d]);
    }
    function noDash() {
        drawingContext.setLineDash([]);
    }

    // ===================== CONTROLS & CALCULATIONS =====================
    function resetProjectile() {
        vx = v0 * cos(radians(angle));
        vy = v0 * sin(radians(angle));
        x = launchX;
        y = groundY - h0 * scale;
        t = 0;
        trace = [];
        trace2 = [];
        trailParticles = [];
    }

    function launchProjectile() {
        if (launched) return;
        resetProjectile();
        launched = true;
        paused = false;
    }

    function togglePause() {
        if (!launched) return;
        paused = !paused;
    }

    function clearTrace() {
        trace = [];
        trace2 = [];
    }

    function resetAll() {
        launched = false;
        paused = false;
        v0 = 20; angle = 45; g = 9.8; h0 = 0;
        document.getElementById('v0').value = v0;
        document.getElementById('angle').value = angle;
        document.getElementById('gravity').value = g;
        document.getElementById('height0').value = h0;
        updateParams();
        resetProjectile();
        updateCalculations();
    }

    function toggleMode(newMode) {
        mode = newMode;
        document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
        if (newMode !== 'compare') trace2 = [];
    }

    function updateParams() {
        v0 = parseFloat(document.getElementById('v0').value);
        angle = parseFloat(document.getElementById('angle').value);
        g = parseFloat(document.getElementById('gravity').value);
        h0 = parseFloat(document.getElementById('height0').value);
        
        document.getElementById('v0Val').textContent = v0;
        document.getElementById('angleVal').textContent = angle;
        document.getElementById('gVal').textContent = g.toFixed(1);
        document.getElementById('h0Val').textContent = h0;
        
        let vx0 = v0 * cos(radians(angle));
        let vy0 = v0 * sin(radians(angle));
        document.getElementById('calcDisplay').innerHTML = 
            `v₀ₓ = ${vx0.toFixed(2)} m/s &nbsp;|&nbsp; v₀ᵧ = ${vy0.toFixed(2)} m/s`;
        
        if (!launched) {
            resetProjectile();
            updateCalculations();
        }
    }

    function updateCalculations() {
        let vx0 = v0 * cos(radians(angle));
        let vy0 = v0 * sin(radians(angle));
        
        // Time to max height
        let tMax = vy0 / g;
        // Max height
        let H = h0 + (vy0 * vy0) / (2 * g);
        // Total time (solve quadratic: h0 + vy0*t - 0.5*g*t^2 = 0)
        let discriminant = vy0*vy0 + 2*g*h0;
        let tTotal = (vy0 + sqrt(discriminant)) / g;
        // Range
        let R = vx0 * tTotal;
        // Final velocity (energy conservation: vf = sqrt(v0² + 2gh0))
        let vf = sqrt(v0*v0 + 2*g*h0);
        
        document.getElementById('statTime').textContent = tTotal.toFixed(2) + ' s';
        document.getElementById('statRange').textContent = R.toFixed(1) + ' m';
        document.getElementById('statHeight').textContent = H.toFixed(1) + ' m';
        document.getElementById('statVFinal').textContent = vf.toFixed(1) + ' m/s';
    }

    function switchTab(tabName) {
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('tab-' + tabName).classList.add('active');
        event.target.classList.add('active');
    }

   
    