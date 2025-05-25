# Invoice Fraud Analyzer

This is a fraud detection tool that analyzes invoice data and flags suspicious vendors based on **Benford’s Law**, **pattern anomalies**, and a custom **Suspicion Score**. It combines mathematical theory with practical heuristics to help detect potential financial manipulation.


## What It Does

- Applies **Benford’s Law** to detect unnatural number distributions in invoice amounts.
- Flags vendors who:
  - Overuse suspicious amounts like 999, 888, or 777.
  - Reuse the same invoice amount frequently.
  - Show unusually low variation in their billing.
- Assigns each vendor a **Suspicion Score (0–100)** based on multiple factors.
- Displays a final decision: **Likely Cheater or Not**.


## Key Features

- Benford-based anomaly detection (statistical red flags)
- Pattern detection: repeated values & low variance
- Custom suspicion scoring system
- Data visualizations (bar charts + heatmaps)
- Fully scriptable and extendable


## How It Works

For each vendor in your dataset, we calculate:
-  How closely their data follows **Benford’s Law**
-  Whether they **reuse suspicious values**
-  Whether their invoice amounts are **too consistent**
-  A combined **Suspicion Score** with customizable weights

The results include flags like:
- `Flagged by Benford`
- `Flagged by Repetition`
- `Flagged by Low STD`
- `Likely Cheater` decision


## Example Input

Just a CSV file with this format:

```csv
InvoiceID,Vendor,Amount
1,CheaterVendor_1,999
2,HonestVendor_1,1420
3,CheaterVendor_2,888
...
