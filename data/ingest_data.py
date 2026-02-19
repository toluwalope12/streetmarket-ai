import random
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers
from faker import Faker

# ========== CONFIGURATION ==========
# Use your exact API key and host
es = Elasticsearch(
    hosts=["https://my-elasticsearch-project-a2dd1e.es.europe-west2.gcp.elastic.cloud:443"],
    api_key="UENjdVdwd0JieGRqaC1tUUVFc0Y6Z1Q4SkJJbWEzNXBfM2hZUFJvRmhodw==",
    verify_certs=False,       # Remove if you have proper certificates
    ssl_show_warn=False
)

# Localised Faker for authentic African names
fake_ng = Faker('en_NG')   # Nigeria
fake_ke = Faker('en_KE')   # Kenya
fake_gh = Faker('en_NG')   # Ghana (fallback to Nigerian names)

# ========== HELPER FUNCTIONS ==========
def random_location(city):
    """Return a slightly randomised (lat, lon) for a given city."""
    cities = {
        'Lagos': (6.5244, 3.3792),
        'Nairobi': (-1.2864, 36.8172),
        'Accra': (5.6037, -0.1870),
        'Mombasa': (-4.0435, 39.6682),
        'Kumasi': (6.6885, -1.6244)
    }
    base_lat, base_lon = cities.get(city, (6.5244, 3.3792))
    # Add random offset (~1km)
    lat = base_lat + random.uniform(-0.01, 0.01)
    lon = base_lon + random.uniform(-0.01, 0.01)
    return lat, lon

def generate_product_name():
    """Return a product name, sometimes with typos (messy data)."""
    products = ['tomatoes', 'onions', 'peppers', 'cassava', 'maize', 'rice', 'beans',
                'plantains', 'oranges', 'mangoes', 'charcoal', 'eggs', 'chicken',
                'fish', 'palm oil', 'groundnuts', 'yams']
    product = random.choice(products)
    # 20% chance of a typo
    if random.random() < 0.2:
        typos = {
            'tomatoes': 'tomatos', 'onions': 'oninons', 'peppers': 'pepas',
            'cassava': 'casava', 'maize': 'mayze', 'rice': 'rise',
            'beans': 'beens', 'plantains': 'plantin', 'oranges': 'ornges'
        }
        product = typos.get(product, product)
    return product

# ========== DATA GENERATION FUNCTIONS ==========
def generate_vendors(n=1000):
    vendors = []
    cities = ['Lagos', 'Nairobi', 'Accra', 'Mombasa', 'Kumasi']
    for i in range(n):
        city = random.choice(cities)
        lat, lon = random_location(city)
        # Pick locale-appropriate name
        if city in ['Lagos', 'Accra', 'Kumasi']:
            name = fake_ng.name() if 'Lagos' in city else fake_gh.name()
        else:
            name = fake_ke.name()
        vendor = {
            '_index': 'vendors',
            '_id': f'VENDOR_{i:04d}',
            '_source': {
                'vendor_id': f'VENDOR_{i:04d}',
                'name': name,
                'location': {'lat': lat, 'lon': lon},
                'phone': fake_ng.phone_number()[:15],
                'product_category': random.choice(['food', 'clothing', 'household', 'electronics']),
                'credit_score': round(random.uniform(0.2, 0.9), 2),
                'joined_date': (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat()
            }
        }
        vendors.append(vendor)
    return vendors

def generate_transactions(vendors, days=30):
    transactions = []
    for vendor in vendors:
        vendor_id = vendor['_source']['vendor_id']
        base_daily = random.uniform(2.0, 8.0)   # USD equivalent
        for day in range(days):
            date = datetime.now() - timedelta(days=days-day-1)
            # Weekend multiplier
            if date.weekday() >= 5:
                multiplier = random.uniform(1.2, 1.5)
            else:
                multiplier = random.uniform(0.8, 1.2)
            amount = base_daily * multiplier
            tx = {
                '_index': 'transactions',
                '_source': {
                    'transaction_id': f'TX_{vendor_id}_{day:02d}',
                    'vendor_id': vendor_id,
                    'amount': round(amount, 2),
                    'timestamp': date.isoformat(),
                    'payment_method': random.choice(['cash', 'mobile_money'])
                }
            }
            transactions.append(tx)
    return transactions

def generate_street_prices(vendors, n=5000):
    prices = []
    for _ in range(n):
        vendor = random.choice(vendors)
        product = generate_product_name()
        price = random.uniform(0.5, 20.0)
        prices.append({
            '_index': 'street_prices',
            '_source': {
                'product_name': product,
                'price': round(price, 2),
                'location': vendor['_source']['location'],
                'source': random.choice(['whatsapp', 'sms']),
                'timestamp': (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
            }
        })
    return prices

def generate_official_prices():
    products = {
        'tomatoes': {'wholesale': 1.2, 'retail': 2.0},
        'onions': {'wholesale': 0.8, 'retail': 1.5},
        'peppers': {'wholesale': 1.5, 'retail': 2.5},
        'cassava': {'wholesale': 1.0, 'retail': 1.8},
        'maize': {'wholesale': 0.6, 'retail': 1.2},
        'rice': {'wholesale': 1.1, 'retail': 1.9},
        'beans': {'wholesale': 1.3, 'retail': 2.2},
        'plantains': {'wholesale': 1.4, 'retail': 2.4},
        'oranges': {'wholesale': 0.9, 'retail': 1.6},
        'mangoes': {'wholesale': 1.0, 'retail': 1.7}
    }
    official = []
    for product, prices in products.items():
        official.append({
            '_index': 'official_prices',
            '_source': {
                'product_name': product,
                'wholesale_price': prices['wholesale'],
                'retail_price': prices['retail'],
                'source': 'ministry_of_trade',
                'timestamp': datetime.now().isoformat()
            }
        })
    return official

def generate_traffic_events(n=50):
    events = []
    cities = ['Lagos', 'Nairobi', 'Accra', 'Mombasa', 'Kumasi']
    for _ in range(n):
        city = random.choice(cities)
        lat, lon = random_location(city)
        events.append({
            '_index': 'traffic_events',
            '_source': {
                'event_type': random.choice(['protest', 'road_closure', 'accident', 'flooding']),
                'location': {'lat': lat, 'lon': lon},
                'severity': random.randint(1, 5),
                'timestamp': (datetime.now() - timedelta(days=random.randint(0, 14))).isoformat()
            }
        })
    return events

def generate_foot_traffic(n=2000):
    traffic = []
    for _ in range(n):
        # Focus on Lagos area
        lat = random.uniform(6.4, 6.6)
        lon = random.uniform(3.3, 3.5)
        hour = random.randint(6, 20)
        day = random.randint(0, 6)
        count = int(random.gauss(100, 30))  # normal distribution around 100
        if count < 0:
            count = 10
        traffic.append({
            '_index': 'foot_traffic',
            '_source': {
                'location': {'lat': lat, 'lon': lon},
                'hour': hour,
                'day_of_week': day,
                'traffic_count': count,
                'timestamp': (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
            }
        })
    return traffic

def create_mama_amina():
    """Special case: vendor with a 35‑day journey from low to high credit."""
    docs = []
    vendor_id = 'VENDOR_MAMA_AMINA'
    # Vendor profile
    docs.append({
        '_index': 'vendors',
        '_id': vendor_id,
        '_source': {
            'vendor_id': vendor_id,
            'name': 'Amina Okonkwo',
            'location': {'lat': 6.5244, 'lon': 3.3792},
            'phone': '+2348012345678',
            'product_category': 'food',
            'credit_score': 0.3,
            'joined_date': (datetime.now() - timedelta(days=40)).isoformat()
        }
    })
    # 35 days of transactions with growth
    for day in range(35):
        date = datetime.now() - timedelta(days=34-day)
        if day < 14:
            amount = random.uniform(3, 5)
        elif day < 21:
            amount = random.uniform(5, 7)
        else:
            amount = random.uniform(6.5, 7.5)
        amount *= random.uniform(0.9, 1.1)
        docs.append({
            '_index': 'transactions',
            '_source': {
                'transaction_id': f'TX_AMINA_{day:02d}',
                'vendor_id': vendor_id,
                'amount': round(amount, 2),
                'timestamp': date.isoformat(),
                'payment_method': 'mobile_money' if day > 20 else 'cash'
            }
        })
    # Some street price observations from her
    for _ in range(5):
        docs.append({
            '_index': 'street_prices',
            '_source': {
                'product_name': 'tomatoes',
                'price': round(random.uniform(1.8, 2.2), 2),
                'location': {'lat': 6.5244, 'lon': 3.3792},
                'source': 'whatsapp',
                'timestamp': (datetime.now() - timedelta(days=random.randint(0, 14))).isoformat()
            }
        })
    return docs

# ========== MAIN EXECUTION ==========
def main():
    print("🚀 STREETMARKET AI – Data Ingestion Started\n")

    print("📦 Generating vendors...")
    vendors = generate_vendors(1000)
    print(f"   {len(vendors)} vendors created.")

    print("💰 Generating transactions...")
    transactions = generate_transactions(vendors, 30)
    print(f"   {len(transactions)} transactions created.")

    print("🏷️ Generating street prices...")
    street_prices = generate_street_prices(vendors, 5000)
    print(f"   {len(street_prices)} street prices created.")

    print("📊 Generating official prices...")
    official_prices = generate_official_prices()
    print(f"   {len(official_prices)} official price records.")

    print("🚧 Generating traffic events...")
    traffic_events = generate_traffic_events(50)
    print(f"   {len(traffic_events)} traffic events.")

    print("👣 Generating foot traffic...")
    foot_traffic = generate_foot_traffic(2000)
    print(f"   {len(foot_traffic)} foot traffic records.")

    print("👩🏿‍🌾 Creating Mama Amina special data...")
    mama_amina = create_mama_amina()
    print(f"   {len(mama_amina)} documents for Mama Amina.")

    # Combine all documents
    all_docs = vendors + transactions + street_prices + official_prices + traffic_events + foot_traffic + mama_amina
    print(f"\n📎 Total documents to index: {len(all_docs)}")

    # Bulk upload to Elasticsearch
    print("\n⏳ Indexing...")
    success, failed = helpers.bulk(es, all_docs, stats_only=True, raise_on_error=False)
    print(f"\n✅ Indexing completed. Success: {success}, Failed: {failed}")

if __name__ == "__main__":
    main()