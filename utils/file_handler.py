import os
import pandas as pd

def read_sales_data(filename):
    """Task 1.1: Reads sales data from file handling encoding issues."""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return []
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                next(f) # Skip header
                return [line.strip() for line in f if line.strip()]
        except: continue
    return []

def save_to_output(df, filename):
    """Saves a dataframe to the output folder."""
    if not os.path.exists('output'): os.makedirs('output')
    df.to_csv(os.path.join('output', filename), index=False)

def save_text_report(content, filename):
    """Saves a text report to the output folder."""
    if not os.path.exists('output'): os.makedirs('output')
    with open(os.path.join('output', filename), 'w') as f:
        f.write(content)
    print(f"✓ Report saved to: output/{filename}")

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Task 3.2 Helper: Saves enriched transactions back to file with pipe delimiter.
    """
    if not enriched_transactions:
        print("No enriched data to save.")
        return

    # Ensure data folder exists
    if not os.path.exists('data'):
        os.makedirs('data')
        
    filepath = filename # filename already includes 'data/' path based on prompt
    
    # Define headers based on the keys of the first transaction
    headers = list(enriched_transactions[0].keys())
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write Header
            f.write('|'.join(headers) + '\n')
            
            # Write Rows
            for t in enriched_transactions:
                # Convert all values to string and handle None
                row = [str(t.get(h, '')) if t.get(h) is not None else '' for h in headers]
                f.write('|'.join(row) + '\n')
                
        print(f"✓ Enriched data saved to: {filepath}")
    except IOError as e:
        print(f"✗ Error saving enriched data: {e}")
