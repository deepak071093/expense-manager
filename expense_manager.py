#print("Hello, Linux Mint!")
#print("hey shona")


import re
from collections import defaultdict

# Initialize totals
category_totals = defaultdict(float)
total_amount = 0.0
month_name = ""

# Function to convert single amount string to float
def parse_single_amount(amount_str):
    amount_str = amount_str.replace(',', '').strip().lower()
    multiplier = 1
    if amount_str.endswith('k'):
        multiplier = 1000
        amount_str = amount_str[:-1]  # remove 'k'
    try:
        return float(amount_str) * multiplier
    except ValueError:
        return 0.0

# Function to parse a sum of amounts separated by '+'
def parse_amount(amount_str):
    parts = amount_str.split('+')
    total = 0.0
    for p in parts:
        total += parse_single_amount(p)
    return total

# Open and read the text file
with open("/media/deepak/New Volume1/Programming_Data/Python/expenses.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    
    # Get month name from first line (assumes format "{month_name} expenses")
    if not month_name and line.lower().endswith("expenses"):
        month_name = line.split()[0]
        continue
    
    # Skip empty lines
    if not line:
        continue
    
    # Match lines like "amount - "description"" (amount can have '+', 'k', decimals)
    match = re.match(r'([\d.,kK\+]+)\s*-\s*(?:"|“)?(.+?)(?:"|”)?$', line)

    if match:
        amount_str, description = match.groups()
        amount = parse_amount(amount_str)
        total_amount += amount
        
        # Normalize description as category: lowercase
        category = description.strip().lower()
        category_totals[category] += amount

# Print result
print(f"{month_name} expenditure")
print(f"total - {total_amount}")

for cat, amt in category_totals.items():
    print(f"{cat} - {amt}")
