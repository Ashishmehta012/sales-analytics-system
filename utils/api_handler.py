import requests

def fetch_all_products():
    """
    Task 3.1a: Fetches all products from DummyJSON API.
    Requirements: limit=100, try-except for connection errors.
    """
    url = "https://dummyjson.com/products?limit=100"
    try:
        print(f"Connecting to API: {url}...")
        response = requests.get(url, timeout=10)
        
        # Check if request was successful (Status Code 200)
        response.raise_for_status()
        
        data = response.json()
        products = data.get('products', [])
        
        print(f"✓ Success: Fetched {len(products)} products from API.")
        return products
        
    except requests.exceptions.RequestException as e:
        print(f"✗ API Error: {e}")
        return []

def create_product_mapping(api_products):
    """
    Task 3.1b: Creates a dictionary mapping Product IDs to info.
    Format: {1: {'title': '...', 'category': '...', ...}, ...}
    """
    mapping = {}
    for p in api_products:
        pid = p.get('id')
        mapping[pid] = {
            'title': p.get('title'),
            'category': p.get('category'),
            'brand': p.get('brand'),
            'rating': p.get('rating')
        }
    return mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Task 3.2: Enriches transaction data with API product information.
    Logic: Extracts numeric ID from 'P101' -> 101 and looks up API data.
    """
    enriched_data = []
    
    for t in transactions:
        # Create a copy so we don't mutate the original dictionary reference
        new_t = t.copy()
        
        # Default values (if no match found)
        new_t['API_Category'] = None
        new_t['API_Brand'] = None
        new_t['API_Rating'] = None
        new_t['API_Match'] = False
        
        try:
            # Logic: Extract numeric ID from 'P101' -> 101
            raw_pid = new_t['ProductID']
            # Remove 'P' and convert to int
            numeric_id = int(raw_pid.upper().replace('P', ''))
            
            # Lookup in the mapping
            if numeric_id in product_mapping:
                api_info = product_mapping[numeric_id]
                new_t['API_Category'] = api_info['category']
                new_t['API_Brand'] = api_info['brand']
                new_t['API_Rating'] = api_info['rating']
                new_t['API_Match'] = True
                
        except (ValueError, AttributeError):
            # Handles cases where ProductID format is unexpected (e.g., 'X2')
            pass
            
        enriched_data.append(new_t)
        
    return enriched_data
