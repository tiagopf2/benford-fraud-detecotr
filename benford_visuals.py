# Written by Tiago Perez

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("improved_invoice_data_benford_test.csv") 

# Leading digit
def get_leading_digit(x):
    x = abs(int(x))
    while x >= 10:
        x //= 10
    return x

df['LeadingDigit'] = df['Amount'].apply(get_leading_digit)

# Bar Chart: Benford vs Actual

benford_dist = {d: np.log10(1 + 1/d) for d in range(1, 10)}
benford_df = pd.DataFrame({
    'Digit': list(range(1, 10)),
    'Benford %': [v * 100 for v in benford_dist.values()]
})

# Leading digit frequencies
actual_counts = df['LeadingDigit'].value_counts(normalize=True).sort_index() * 100
actual_df = pd.DataFrame({'Digit': actual_counts.index, 'Actual %': actual_counts.values})

# Comparison
compare_df = pd.merge(benford_df, actual_df, on='Digit')

# Side-by-side bar chart
plt.figure(figsize=(10, 6))
bar_width = 0.35
r1 = np.arange(len(compare_df['Digit']))
r2 = [x + bar_width for x in r1]

plt.bar(r1, compare_df['Benford %'], width=bar_width, label='Benford', alpha=0.7)
plt.bar(r2, compare_df['Actual %'], width=bar_width, label='Actual', alpha=0.7)

plt.xticks([r + bar_width / 2 for r in r1], compare_df['Digit'])
plt.xlabel('Leading Digit')
plt.ylabel('Percentage (%)')
plt.title('Leading Digit Distribution: Actual vs. Benford\'s Law')
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()

# Heatmap: Vendor Suspicion Stats

# Metrics by vendor
vendor_stats = df.groupby('Vendor').agg({
    'Amount': ['count', 'mean', 'std'],
    'LeadingDigit': lambda x: (x == 9).mean()
})

vendor_stats.columns = ['Invoice Count', 'Avg Amount', 'STD Amount', '% Leading 9s']
vendor_stats = vendor_stats.reset_index()

# Heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(vendor_stats.set_index('Vendor'), annot=True, fmt=".2f", cmap="YlOrRd")
plt.title('Vendor Heatmap: Invoice Metrics & % of Leading 9s')
plt.tight_layout()
plt.show()
