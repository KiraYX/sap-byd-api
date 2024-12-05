import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Parameters
mu = 50  # Process mean
sigma = 2  # Standard deviation
USL = 55  # Upper Specification Limit
LSL = 45  # Lower Specification Limit

# Generate data for the normal distribution
x = np.linspace(30, 70, 1000)
y = norm.pdf(x, mu, sigma)

# Plot the distribution curve
plt.plot(x, y, label='Process Distribution', color='blue')
plt.fill_between(x, y, where=(x >= LSL) & (x <= USL), color='green', alpha=0.3, label='Acceptable Range')

# Add specification limits
plt.axvline(USL, color='red', linestyle='--', label=f'USL = {USL}')
plt.axvline(LSL, color='red', linestyle='--', label=f'LSL = {LSL}')
plt.axvline(mu, color='black', linestyle='-', label=f'Mean = {mu}')

# Show labels
plt.title('CP and CPK Graph')
plt.xlabel('Measurement')
plt.ylabel('Probability Density')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()
