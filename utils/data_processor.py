import datetime
import os

def parse_transactions(raw_lines):
    """Task 1.2: Parses raw lines into clean dictionaries."""
    transactions = []
    for line in raw_lines:
        fields = line.split('|')
        if len(fields) != 8: continue
        try:
            qty_val = fields[4].replace(',', '').strip()
            price_val = fields[5].replace(',', '').strip()
            transactions.append({
                'TransactionID': fields[0].strip(),
                'Date': fields[1].strip(),
                'ProductID': fields[2].strip(),
                'ProductName': fields[3].replace(',', ' ').strip(),
                'Quantity': int(qty_val),
                'UnitPrice': float(price_val),
                'CustomerID': fields[6].strip(),
                'Region': fields[7].strip()
            })
        except ValueError: continue
    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """Task 1.3: Validates and applies optional filters."""
    valid_list, inv_count = [], 0
    reg_filtered, amt_filtered = 0, 0
    
    # Validation Rules
    for t in transactions:
        is_valid = (t['Quantity'] > 0 and t['UnitPrice'] > 0 and
                    t['TransactionID'].startswith('T') and
                    t['ProductID'].startswith('P') and
                    t['CustomerID'].startswith('C'))
        if not is_valid:
            inv_count += 1
            continue
        if region and t['Region'] != region:
            reg_filtered += 1
            continue
        total = t['Quantity'] * t['UnitPrice']
        if (min_amount and total < min_amount) or (max_amount and total > max_amount):
            amt_filtered += 1
            continue
        valid_list.append(t)

    return valid_list, inv_count, {
        'total_input': len(transactions), 'invalid': inv_count,
        'final_count': len(valid_list)
    }

# --- Analytics Functions ---

def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    rev = calculate_total_revenue(transactions)
    stats = {}
    for t in transactions:
        r = t['Region']
        if r not in stats: stats[r] = {'total_sales': 0.0, 'transaction_count': 0}
        stats[r]['total_sales'] += t['Quantity'] * t['UnitPrice']
        stats[r]['transaction_count'] += 1
    for r in stats: 
        stats[r]['percentage'] = round((stats[r]['total_sales']/rev)*100, 2)
    return dict(sorted(stats.items(), key=lambda x: x[1]['total_sales'], reverse=True))

def top_selling_products(transactions, n=5):
    prods = {}
    for t in transactions:
        n_ = t['ProductName']
        if n_ not in prods: prods[n_] = {'qty': 0, 'rev': 0.0}
        prods[n_]['qty'] += t['Quantity']
        prods[n_]['rev'] += t['Quantity'] * t['UnitPrice']
    return [(k, v['qty'], v['rev']) for k, v in sorted(prods.items(), key=lambda x: x[1]['qty'], reverse=True)[:n]]

def customer_analysis(transactions):
    custs = {}
    for t in transactions:
        cid = t['CustomerID']
        amt = t['Quantity'] * t['UnitPrice']
        if cid not in custs: custs[cid] = {'spent': 0.0, 'count': 0, 'prods': set()}
        custs[cid]['spent'] += amt
        custs[cid]['count'] += 1
        custs[cid]['prods'].add(t['ProductName'])
    return {c: {'total_spent': round(d['spent'], 2), 'purchase_count': d['count'], 
            'avg_order_value': round(d['spent']/d['count'], 2), 
            'products_bought': sorted(list(d['prods']))} for c, d in sorted(custs.items(), key=lambda x: x[1]['spent'], reverse=True)}

def daily_sales_trend(transactions):
    trend = {}
    for t in transactions:
        d = t['Date']
        if d not in trend: trend[d] = {'revenue': 0.0, 'count': 0, 'custs': set()}
        trend[d]['revenue'] += t['Quantity'] * t['UnitPrice']
        trend[d]['count'] += 1
        trend[d]['custs'].add(t['CustomerID'])
    return {k: {'revenue': round(v['revenue'], 2), 'transaction_count': v['count'], 'unique_customers': len(v['custs'])} for k, v in sorted(trend.items())}

def find_peak_sales_day(transactions):
    trend = daily_sales_trend(transactions)
    if not trend: return None
    peak = max(trend, key=lambda d: trend[d]['revenue'])
    return (peak, trend[peak]['revenue'], trend[peak]['transaction_count'])

def low_performing_products(transactions, threshold=10):
    prods = {}
    for t in transactions:
        n_ = t['ProductName']
        if n_ not in prods: prods[n_] = {'qty': 0, 'rev': 0.0}
        prods[n_]['qty'] += t['Quantity']
        prods[n_]['rev'] += t['Quantity'] * t['UnitPrice']
    return sorted([(k, v['qty'], v['rev']) for k, v in prods.items() if v['qty'] < threshold], key=lambda x: x[1])

# --- Task 4.1: Report Generation ---

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """Generates a comprehensive formatted text report (Task 4.1)."""
    
    # 1. Gather Data
    total_rev = calculate_total_revenue(transactions)
    count = len(transactions)
    avg_order = total_rev / count if count else 0
    dates = sorted([t['Date'] for t in transactions])
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"
    
    region_stats = region_wise_sales(transactions)
    top_prods = top_selling_products(transactions, n=5)
    top_custs = list(customer_analysis(transactions).items())[:5]
    daily_stats = daily_sales_trend(transactions)
    
    peak_day = find_peak_sales_day(transactions)
    low_prods = low_performing_products(transactions)
    
    # 2. Build Report Strings
    lines = []
    lines.append("="*50)
    lines.append(f"{'SALES ANALYTICS REPORT':^50}")
    lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^50}")
    lines.append(f"Records Processed: {count:^50}")
    lines.append("="*50 + "\n")
    
    lines.append("OVERALL SUMMARY")
    lines.append("-" * 45)
    lines.append(f"Total Revenue:      ${total_rev:,.2f}")
    lines.append(f"Total Transactions: {count}")
    lines.append(f"Average Order Value: ${avg_order:,.2f}")
    lines.append(f"Date Range:         {date_range}\n")
    
    lines.append("REGION-WISE PERFORMANCE")
    lines.append("-" * 65)
    lines.append(f"{'Region':<15} {'Sales':<15} {'% of Total':<15} {'Tx Count':<10}")
    for reg, stats in region_stats.items():
        lines.append(f"{reg:<15} ${stats['total_sales']:<14,.2f} {stats['percentage']:<14}% {stats['transaction_count']:<10}")
    lines.append("")
    
    lines.append("TOP 5 PRODUCTS")
    lines.append("-" * 65)
    lines.append(f"{'Rank':<5} {'Product Name':<25} {'Qty Sold':<10} {'Revenue':<15}")
    for i, (name, qty, rev) in enumerate(top_prods, 1):
        lines.append(f"{i:<5} {name:<25} {qty:<10} ${rev:,.2f}")
    lines.append("")
    
    lines.append("TOP 5 CUSTOMERS")
    lines.append("-" * 65)
    lines.append(f"{'Rank':<5} {'Cust ID':<10} {'Total Spent':<15} {'Orders':<10}")
    for i, (cid, stats) in enumerate(top_custs, 1):
        lines.append(f"{i:<5} {cid:<10} ${stats['total_spent']:<14,.2f} {stats['purchase_count']:<10}")
    lines.append("")
    
    lines.append("DAILY SALES TREND (Last 5 Days)")
    lines.append("-" * 65)
    lines.append(f"{'Date':<15} {'Revenue':<15} {'Tx Count':<10} {'Unique Cust':<10}")
    # Showing last 5 for brevity, or remove slice to show all
    for date, stats in list(daily_stats.items())[-5:]: 
        lines.append(f"{date:<15} ${stats['revenue']:<14,.2f} {stats['transaction_count']:<9} {stats['unique_customers']:<10}")
    lines.append("")
    
    lines.append("PRODUCT PERFORMANCE ANALYSIS")
    lines.append("-" * 45)
    if peak_day:
        lines.append(f"Best Selling Day: {peak_day[0]} (${peak_day[1]:,.2f})")
    
    lines.append(f"Low Performing Products (<10 units): {len(low_prods)}")
    if low_prods:
        lines.append(f"  Example: {low_prods[0][0]} ({low_prods[0][1]} sold)")
    
    # Avg Tx Value per Region
    lines.append("\nAverage Transaction Value by Region:")
    for reg, stats in region_stats.items():
        avg_reg = stats['total_sales'] / stats['transaction_count']
        lines.append(f"  {reg}: ${avg_reg:,.2f}")
    lines.append("")

    lines.append("API ENRICHMENT SUMMARY")
    lines.append("-" * 45)
    # Calculate enrichment stats
    unique_products = set(t['ProductID'] for t in enriched_transactions)
    enriched_prods = set(t['ProductID'] for t in enriched_transactions if t.get('API_Match'))
    failed_prods = unique_products - enriched_prods
    
    success_rate = (len(enriched_prods) / len(unique_products) * 100) if unique_products else 0
    
    lines.append(f"Total Unique Products: {len(unique_products)}")
    lines.append(f"Successfully Enriched: {len(enriched_prods)}")
    lines.append(f"Success Rate:          {success_rate:.1f}%")
    if failed_prods:
        lines.append(f"Failed to enrich:      {', '.join(list(failed_prods)[:5])}...")
    lines.append("="*50)

    # 3. Write to File
    if not os.path.exists('output'):
        os.makedirs('output')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        
    print(f"✓ Sales Report generated at: {output_file}")
