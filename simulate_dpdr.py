import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ODE parameters from the paper (MRA-I sub-model)
alpha = 0.5   # Restoring force
Phi_target = 0.8
Phi_th = 0.4  # The threshold where the system "breaks"


def gift_ode(t, Phi):
    # A simplified version of the ODE near the bifurcation
    return -alpha * (Phi - Phi_target) * (Phi - Phi_th)


# Run simulation
t_span = (0, 50)
y0 = [0.7]  # Start in conscious state
sol = solve_ivp(gift_ode, t_span, y0, t_eval=np.linspace(0, 50, 100))

# Plotting the result
plt.plot(sol.t, sol.y[0])
plt.axhline(y=Phi_th, color='r', linestyle='--', label='DPDR Threshold')
plt.title("Transition into DPDR (Saddle-Node Bifurcation)")
plt.xlabel("Time")
plt.ylabel("Phi_voi (Coupling Precision)")
plt.legend()
plt.show()