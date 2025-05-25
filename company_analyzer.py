import pandas as pd
import numpy as np
from scipy.stats import chisquare
from collections import Counter

df = pd.read_csv("improved_invoice_data_benford_test.csv")

# Benford's distribution
benford_dist = {d: np.log10(1 + 1/d) for d in range(1, 10)}
expected_freq = [benford_dist[d] for d in range(1, 10)]

# Extract leading digit
def get_leading_digit(x):
    x = abs(int(x))
    while x >= 10:
        x //= 10
    return x

df['LeadingDigit'] = df['Amount'].apply(get_leading_digit)

# Suspicious values
suspicious_values = [999, 888, 777, 666]

# Strongly skewed fake invoices
high_digits = [900, 950, 980, 999, 890, 970]
fake_amounts = np.random.choice(high_digits, size=700)

# Analysis functions
def suspicious_value_ratio(group):
    suspicious = group['Amount'].isin(suspicious_values).sum()
    return suspicious / len(group)

def repetition_score(group):
    top_count = group['Amount'].value_counts().iloc[0]
    return top_count / len(group)

def variance_score(group):
    return group['Amount'].std()

# Analysis for each vendor
results = []

for vendor, group in df.groupby('Vendor'):
    counts = Counter(group['LeadingDigit'])
    total = sum(counts.values())
    if total < 30:
        continue 

    observed_freq = [counts.get(d, 0) / total for d in range(1, 10)]
    chi2_stat, p_value = chisquare(f_obs=observed_freq, f_exp=expected_freq)

    suspicious_ratio = suspicious_value_ratio(group)
    repeat = repetition_score(group)
    std_dev = variance_score(group)

    results.append({
        'Vendor': vendor,
        'Chi2': round(chi2_stat, 4),
        'P-Value': round(p_value, 4),
        'Flagged by Benford': p_value < 0.05,
        'Suspicious %': round(suspicious_ratio, 3),
        'Flagged by Value': suspicious_ratio > 0.2,
        'Repetition Score': round(repeat, 3),
        'Flagged by Repetition': repeat > 0.2,
        'Amount STD': round(std_dev, 2),
        'Flagged by Low STD': std_dev < 200
    })

# Results
df_results = pd.DataFrame(results)

# All flagging methods
df_results['Likely Cheater'] = (
    df_results['Flagged by Benford'] |
    df_results['Flagged by Value'] |
    df_results['Flagged by Repetition'] |
    df_results['Flagged by Low STD']
)

# Reliability rate
num_total = len(df_results)
num_flagged = df_results['Likely Cheater'].sum()
reliability_rate = (num_total - num_flagged) / num_total * 100

# Results
print(df_results.sort_values(by='Likely Cheater', ascending=False))
print(f"\nCheaters detected: {num_flagged} / {num_total}")
print(f"Estimated reliability rate: {reliability_rate:.2f}%")
