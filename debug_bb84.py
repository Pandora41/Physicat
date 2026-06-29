# debug_bb84.py
from app.simulations.qkd.bb84 import BB84

# Run simulation sederhana
bb84 = BB84(n_photons=100, noise=0.02)
result = bb84.run()

# Print semua attribute
print("=== Attributes of BB84Result ===")
for attr in dir(result):
    if not attr.startswith('_'):
        try:
            value = getattr(result, attr)
            print(f"{attr}: {type(value).__name__} = {value}")
        except Exception as e:
            print(f"{attr}: ERROR - {e}")

print("\n=== vars(result) ===")
print(vars(result))