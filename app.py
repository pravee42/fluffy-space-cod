from flask import Flask, jsonify, request
import requests
import sqlite3
import json

app = Flask(__name__)

# SQLite3 connection details
DATABASE_NAME = "bigbasket.db"
TABLE_NAME = "products"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

# Create table if it doesn't exist
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        desc TEXT,
        sku_max_quantity INTEGER,
        pack_desc TEXT,
        sort_index_pos INTEGER,
        cart_count INTEGER,
        is_best_value BOOLEAN,
        weight TEXT,
        absolute_url TEXT,
        usp TEXT,
        avail_status TEXT,
        display_mrp BOOLEAN,
        display_sp BOOLEAN,
        not_for_sale BOOLEAN,
        button TEXT,
        show_express BOOLEAN,
        mrp REAL,
        sp REAL,
        discount_text TEXT,
        discount_avail BOOLEAN,
        subscription_price REAL,
        offer_entry_text TEXT,
        image_urls TEXT,
        brand_name TEXT,
        brand_slug TEXT,
        brand_url TEXT,
        tlc_name TEXT,
        tlc_slug TEXT,
        mlc_name TEXT,
        mlc_slug TEXT,
        mlc_id INTEGER,
        llc_name TEXT,
        llc_slug TEXT,
        llc_id INTEGER,
        avg_rating REAL,
        rating_count INTEGER,
        review_count INTEGER,
        parent_id INTEGER,
        child_id TEXT,
        is_tobacco BOOLEAN
    );
    """)
    conn.commit()
    conn.row_factory = sqlite3.Row
    
    return conn

# API request details for BigBasket
BIGBASKET_URL = 'https://www.bigbasket.com/listing-svc/v2/products?type=pc&slug=atta-flours-sooji&page=2'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Cookie': (
        'x-entry-context-id=100; x-entry-context=bb-b2c; _bb_locSrc=default; '
        'x-channel=web; _bb_loid=j:null; _bb_bhid=; _bb_nhid=1723; '
        '_bb_vid=MTI1NzgwNjQ0MjE=; _bb_dsevid=; _bb_dsid=; _bb_cid=1; '
        '_bb_aid=MzA4NTgxODk5Nw==; csrftoken=vuRv3s7aOjhGxjxjve9l1mE5f7P3dlexx7FxUcLkMenReod2NRRNPL9XML6wEhbJ; '
        '_bb_home_cache=e45768e6.1.visitor; _bb_bb2.0=1; is_global=1; _bb_addressinfo=; '
        '_bb_pin_code=; _bb_sa_ids=10654; _is_tobacco_enabled=0; _is_bb1.0_supported=0; '
        'is_integrated_sa=0; bb2_enabled=true; bigbasket.com=13d7d3d8-37e6-4082-91e2-57890ffe3a6b; '
        'jarvis-id=69a0514e-b474-40d8-8de4-e03104bb08ea; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xMDY1NA==; '
        'csurftoken=M3DvPw.MTI1NzgwNjQ0MjE=.1723344572200.r5+zEzMZcsrCzfYA+hdU+VM/ut0LXU/gjNbwdYCl0n4=; '
        'ts=2024-08-11%2008:19:51.270; csurftoken=M3DvPw.MTI1NzgwNjQ0MjE=.1723344572200.r5+zEzMZcsrCzfYA+hdU+VM/ut0LXU/gjNbwdYCl0n4='
    )
}

@app.route('/products', methods=['GET'])
def get_products():
    """Endpoint to get all products from the database."""
    conn = get_db_connection()
    products = conn.execute(f"SELECT * FROM {TABLE_NAME}").fetchall()
    conn.close()

    products_list = [dict(row) for row in products]
    return jsonify(products_list)

@app.route('/products/fetch', methods=['GET'])
def fetch_and_store_products():
    response = requests.get(BIGBASKET_URL, headers=HEADERS)

    if response.status_code == 200:
        try:
            data = response.json()
            products = data['tabs'][0]['product_info']['products']

            conn = get_db_connection()

            if products:
                for product in products:
                    desc = product.get('desc')
                    sku_max_quantity = product.get('sku_max_quantity', 0)
                    pack_desc = product.get('pack_desc', '')
                    sort_index_pos = product.get('sort_index_pos', 0)
                    cart_count = product.get('cart_count', 0)
                    is_best_value = product.get('is_best_value', False)
                    weight = product.get('w', '')
                    absolute_url = product.get('absolute_url', '')
                    usp = product.get('usp', '')
                    
                    availability = product.get('availability', {})
                    avail_status = availability.get('avail_status', '')
                    display_mrp = availability.get('display_mrp', False)
                    display_sp = availability.get('display_sp', False)
                    not_for_sale = availability.get('not_for_sale', False)
                    button = availability.get('button', '')
                    show_express = availability.get('show_express', False)
                    
                    pricing = product.get('pricing', {}).get('discount', {})
                    discount_text = pricing.get('d_text', '')
                    discount_avail = pricing.get('d_avail', 'false') == 'true'
                    offer_entry_text = pricing.get('offer_entry_text', '')

                    images = product.get('images', [])
                    image_urls = json.dumps([img['l'] for img in images])

                    brand = product.get('brand', {})
                    brand_name = brand.get('name', '')
                    brand_slug = brand.get('slug', '')
                    brand_url = brand.get('url', '')

                    category = product.get('category', {})
                    tlc_name = category.get('tlc_name', '')
                    tlc_slug = category.get('tlc_slug', '')
                    mlc_name = category.get('mlc_name', '')
                    mlc_slug = category.get('mlc_slug', '')
                    mlc_id = category.get('mlc_id', 0)
                    llc_name = category.get('llc_name', '')
                    llc_slug = category.get('llc_slug', '')
                    llc_id = category.get('llc_id', 0)

                    rating_info = product.get('rating_info', {})
                    rating_count = rating_info.get('rating_count', 0)
                    review_count = rating_info.get('review_count', 0)

                    parent_info = product.get('parent_info', {})
                    parent_id = parent_info.get('parent_id', 0)
                    child_id = product.get('id', '')
                    mrp = float(pricing.get('mrp', 0) or 0)
                    sp = float(pricing.get('prim_price', {}).get('sp', 0) or 0)
                    subscription_price = float(pricing.get('subscription_price', 0) or 0)
                    avg_rating = float(rating_info.get('avg_rating', 0) or 0)


                    is_tobacco = product.get('is_tobacco', False)

                    conn.execute(f"""
                    INSERT INTO {TABLE_NAME} (
                        desc, sku_max_quantity, pack_desc, sort_index_pos, cart_count, is_best_value, weight, absolute_url, usp, 
                        avail_status, display_mrp, display_sp, not_for_sale, button, show_express, mrp, sp, discount_text, discount_avail, 
                        subscription_price, offer_entry_text, image_urls, brand_name, brand_slug, brand_url, tlc_name, tlc_slug, 
                        mlc_name, mlc_slug, mlc_id, llc_name, llc_slug, llc_id, avg_rating, rating_count, review_count, parent_id, 
                        child_id, is_tobacco
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        desc, sku_max_quantity, pack_desc, sort_index_pos, cart_count, is_best_value, weight, absolute_url, usp,
                        avail_status, display_mrp, display_sp, not_for_sale, button, show_express, mrp, sp, discount_text, discount_avail,
                        subscription_price, offer_entry_text, image_urls, brand_name, brand_slug, brand_url, tlc_name, tlc_slug,
                        mlc_name, mlc_slug, mlc_id, llc_name, llc_slug, llc_id, avg_rating, rating_count, review_count, parent_id,
                        child_id, is_tobacco
                    ))

                conn.commit()

            conn.close()
            return jsonify({"status": "success", "message": "Products fetched and stored successfully"}), 200

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Failed to fetch products from BigBasket API"}), 500

if __name__ == '__main__':
    app.run(debug=True)
