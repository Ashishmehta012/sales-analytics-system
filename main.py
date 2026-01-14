from utils.file_handler import read_sales_data, save_enriched_data
import utils.data_processor as dp
import utils.api_handler as api
import sys

def main():
    print("="*40)
    print("SALES ANALYTICS SYSTEM")
    print("="*40 + "\n")

    try:
        # [1/10] Reading Data
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        if not raw_lines:
            print("✗ No data found. Exiting.")
            return
        print(f"✓ Successfully read {len(raw_lines)} transactions\n")

        # [2/10] Parsing Data
        print("[2/10] Parsing and cleaning data...")
        parsed_transactions = dp.parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records\n")

        # [3/10] Filter Options (User Interaction)
        print("[3/10] Filter Options Available:")
        
        # Calculate available options for display
        regions = sorted(list(set(t['Region'] for t in parsed_transactions if t['Region'])))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in parsed_transactions]
        
        print(f"Regions: {', '.join(regions)}")
        if amounts:
            print(f"Amount Range: {min(amounts):.0f} - {max(amounts):.0f}")
        else:
            print("Amount Range: N/A")

        # Interaction Logic
        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()
        
        filter_region = None
        filter_min = None
        filter_max = None

        if choice == 'y':
            print("\n--- Enter Filter Criteria (Press Enter to skip) ---")
            r_input = input(f"Enter Region ({', '.join(regions)}): ").strip()
            if r_input in regions:
                filter_region = r_input
            
            min_input = input("Enter Minimum Amount: ").strip()
            if min_input.isdigit():
                filter_min = float(min_input)
                
            max_input = input("Enter Maximum Amount: ").strip()
            if max_input.isdigit():
                filter_max = float(max_input)
            print("✓ Filters applied\n")
        else:
            print("✓ Proceeding without filters\n")

        # [4/10] Validating Transactions
        print("[4/10] Validating transactions...")
        valid_data, inv_count, summary = dp.validate_and_filter(
            parsed_transactions, 
            region=filter_region, 
            min_amount=filter_min, 
            max_amount=filter_max
        )
        print(f"✓ Valid: {len(valid_data)} | Invalid: {inv_count}")
        print(f"✓ Filtered Result: {len(valid_data)} records remaining\n")

        if not valid_data:
            print("✗ No valid data left to analyze. Exiting.")
            return

        # [5/10] Analyzing Data
        print("[5/10] Analyzing sales data...")
        # (We call these just to ensure they run without error, results are used in report)
        _ = dp.calculate_total_revenue(valid_data)
        _ = dp.region_wise_sales(valid_data)
        print("✓ Analysis complete\n")

        # [6/10] API Fetching
        print("[6/10] Fetching product data from API...")
        api_products = api.fetch_all_products()
        if api_products:
            print(f"✓ Fetched {len(api_products)} products\n")
        else:
            print("! Warning: API fetch failed. Proceeding without enrichment.\n")

        # [7/10] Enrichment
        print("[7/10] Enriching sales data...")
        enriched_data = []
        if api_products:
            product_map = api.create_product_mapping(api_products)
            enriched_data = api.enrich_sales_data(valid_data, product_map)
            
            matches = sum(1 for t in enriched_data if t.get('API_Match'))
            percentage = (matches / len(valid_data)) * 100
            print(f"✓ Enriched {matches}/{len(valid_data)} transactions ({percentage:.1f}%)\n")
        else:
            enriched_data = valid_data # Fallback
            print("✓ Skipped enrichment (API data missing)\n")

        # [8/10] Saving Enriched Data
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_data, 'data/enriched_sales_data.txt')
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # [9/10] Generating Report
        print("[9/10] Generating report...")
        dp.generate_sales_report(valid_data, enriched_data, 'output/sales_report.txt')
        print("✓ Report saved to: output/sales_report.txt\n")

        # [10/10] Completion
        print("[10/10] Process Complete!")
        print("="*40)

    except Exception as e:
        print(f"\nCRITICAL ERROR: {str(e)}")
        print("The program has been stopped safely.")
        sys.exit(1)

if __name__ == "__main__":
    main()
