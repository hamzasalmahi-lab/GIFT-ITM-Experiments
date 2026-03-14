# GIFT-ITM-Experiments
GIFT Math Experimentations 

## Threshold Audit Script

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the symbolic derivation:

```bash
python3 audit_threshold.py
```

Expected result:

```text
The mathematically [PROVED] threshold is: Phi_th = L_bio*kappa/(2*lambda) + Phi_0
```

Run the basic test:

```bash
python3 -m unittest discover -s tests
```

## DPDR Simulation Script

Run the ODE simulation:

```bash
python3 simulate_dpdr.py
```

If you are running in a headless environment, use a non-interactive Matplotlib backend:

```bash
MPLBACKEND=Agg python3 simulate_dpdr.py
```

## Ricci Scalar Script

Run the symbolic Ricci scalar calculation:

```bash
python3 calc_ricci.py
```

## Warped Ricci Analysis

Run the full 5D warped-metric analysis:

```bash
python3 analyze_warped_ricci.py
```

## Unified Parameter Optimization

Run the global optimization for a unified GIFT-ITM parameter set:

```bash
python3 optimize_unified_parameters.py
```

If no coherent solution is found, the script saves:

```text
incoherence_gap.png
```

## Variational MRA-I Derivation

Run the symbolic variational derivation linking IFEs to a dynamical \\dot{Phi} closure:

```bash
python3 derive_mrai_variation.py
```

## Changelog (2026-03-14)

- Added `audit_threshold.py` for symbolic threshold derivation from the equilibrium condition.
- Added `simulate_dpdr.py` for ODE simulation of DPDR threshold dynamics.
- Added `calc_ricci.py` for symbolic 5D Ricci scalar computation with EinsteinPy.
- Added `analyze_warped_ricci.py` for non-diagonal warped 5D metric analysis, first-order reduction constraints, and warp-error term output.
- Added tests: `test_audit_threshold.py`, `test_calc_ricci.py`, and `test_analyze_warped_ricci.py`.
- Expanded `requirements.txt` with scientific/symbolic dependencies needed by all scripts.
