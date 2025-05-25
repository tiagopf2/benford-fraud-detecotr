# Written by Tiago Perez

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import chisquare

# Fake invoice data
np.random.seed(42)

honest_amounts = np.random.lognormal(mean=7, sigma=0.5, size=950).astype(int)

suspicious_amounts = np.random.choice([999, 888, 777, 666], size=50)

invoice_amounts = np.concatenate([honest_amounts, suspicious_amounts])
vendors = np.random.choice(['Vendor A', 'Vendor B', 'Vendor C', 'Vendor D'], size=1000)

df = pd.DataFrame({
    'InvoiceID': range(1, 1001),
    'Vendor': vendors,
    'Amount': invoice_amounts
})

# Leading digits from amounts
def get_leading_digit(x):
    while x >= 10:
        x //= 10
    return x

df['LeadingDigit'] = df['Amount'].apply(get_leading_digit)

# Benford’s Law
benford_dist = {d: np.log10(1 + 1/d) for d in range(1, 10)}
observed_counts = Counter(df['LeadingDigit'])
total = sum(observed_counts.values())
observed_freq = {d: observed_counts[d] / total for d in range(1, 10)}
expected_freq = [benford_dist[d] for d in range(1, 10)]
observed_freq_list = [observed_freq.get(d, 0) for d in range(1, 10)]

# Chi-square test
chi2_stat, p_value = chisquare(f_obs=observed_freq_list, f_exp=expected_freq)
print(f"Chi-square statistic: {chi2_stat:.4f}")
print(f"P-value: {p_value:.4f}")

# Visualization
plt.figure(figsize=(10, 5))
plt.bar(range(1, 10), observed_freq_list, alpha=0.7, label='Observed')
plt.plot(range(1, 10), expected_freq, color='red', marker='o', label='Benford\'s Law')
plt.xticks(range(1, 10))
plt.xlabel('Leading Digit')
plt.ylabel('Frequency')
plt.title('Leading Digit Distribution vs. Benford\'s Law')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Flag suspicious vendors
suspicious_values = [999, 888, 777, 666]
df['Suspicious'] = df['Amount'].isin(suspicious_values)
suspicious_vendors = df[df['Suspicious']].groupby('Vendor').size().sort_values(ascending=False)

print("\nVendors with suspicious invoice counts:")
print(suspicious_vendors)
