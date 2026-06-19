import streamlit as st
from urllib.parse import quote_plus
import requests
import re
import os
from pathlib import Path

# Local Assets Mapping
ASSETS = {
    "hero": "assets/hero.jpg",
    "app_banner": "assets/app_banner.jpg",
    "sale": "assets/sale_banner.jpg",
    "premium": "assets/premium_banner.jpg",
    "beauty": "assets/beauty.jpg",
    "casual": "assets/casual.jpg",
    "dress": "assets/dress.jpg",
    "ethnic": "assets/ethnic.jpg",
    "festival": "assets/festival.jpg",
    "festival_banner": "assets/festival_banner.jpg",
    "kids": "assets/kids.jpg",
    "kurti": "assets/kurti.jpg",
    "men": "assets/men.jpg",
    "office": "assets/office.jpg",
    "party": "assets/party.jpg",
    "women": "assets/women.jpg",
    "footwear": "assets/footwear.jpg",
}

ASSETS_ABS = {
    k: str((Path(__file__).resolve().parent / v).resolve())
    for k, v in ASSETS.items()
}



# Try to import recommendation, with fallback
try:
    from src.recommendation import recommend
except ImportError:
    def recommend(occasion, budget):
        # Fallback recommendation function
        import pandas as pd
        return pd.DataFrame({
            'Category': ['Kurti', 'Jeans', 'Tshirt', 'Shirt'],
            'Price': ['999', '1299', '599', '799']
        })

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

body {
background-color: #fafafa;
}

</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="Bharat Fashion AI",
    page_icon="🛍️",
    layout="wide"
)

# --- Styles: stronger contrast, bold header, card styles
st.markdown(
    """
    <style>
    .stApp {
        background: #fff;
    }
    /* Myntra-themed controls */
    select, .stSelectbox select {
        background: linear-gradient(90deg,#ff6f00 0%, #ff3d00 100%);
        color: white !important;
        font-weight:700;
        border-radius:8px;
        padding:8px 10px;
        border: none;
    }
    select option {
        color: #222;
    }
    input[type=range] {
        accent-color: #ff3d00;
    }
    .stSlider > div {
        color: #ff3d00;
        font-weight:700;
    }
    .header-bar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #ff6b9d 75%, #ff9a56 100%);
        color: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        margin-bottom: 18px;
    }
    .header-title { font-size:36px; font-weight:800; margin:0; }
    .header-sub { color: rgba(255,255,255,0.92); margin-top:6px; }
    .cta-button button {
        background: #ffffff;
        color: #ff3d00;
        font-weight:700;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        box-shadow: 0 6px 18px rgba(255,61,0,0.18);
        cursor: pointer;
    }
    .card-row { display:flex; gap:16px; margin-top:18px; }
    .card { flex:1; border-radius:12px; overflow:hidden; position:relative; height:220px; background-size:cover; background-position:center; box-shadow: 0 8px 24px rgba(0,0,0,0.08); cursor:pointer; transition: transform 0.3s ease; }
    .card:hover { transform: translateY(-4px); box-shadow: 0 12px 28px rgba(0,0,0,0.12); }
    .card .overlay { position:absolute; left:0; right:0; bottom:0; padding:14px; background:linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.45) 60%); color:white; }
    .card-title { font-weight:700; font-size:18px; }
    .muted { color:#666; }
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');
    * { font-family: 'Montserrat', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }
    .rec-row { display:flex; gap:16px; flex-wrap:wrap; margin-top:18px; }
    .rec-card { width:220px; border-radius:12px; overflow:hidden; background:#fff; box-shadow:0 8px 20px rgba(0,0,0,0.08); }
    .rec-card img { width:100%; height:220px; object-fit:cover; display:block; }
    .rec-card-body { padding:10px; }
    .price { color:#ff3d00; font-weight:800; margin-top:6px; }
    .myntra-logo {
        font-size: 32px;
        font-weight: 900;
        background: linear-gradient(90deg, #ff6f00 0%, #ff3d00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 2px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .bag-icon {
        font-size: 32px;
        background: linear-gradient(135deg, #ff6f00 0%, #ff3d00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: pink with white;
        background-clip: text;
    }
    .header-content {
        display: flex;
        align-items: center;
        gap: 24px;
        flex: 1;
    }
    .header-text h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 800;
    }
    .header-text p {
        margin: 4px 0 0 0;
        font-size: 14px;
        opacity: 0.95;
    }
    .feature-card img { cursor:pointer; transition: transform 0.3s ease; }
    .feature-card img:hover { transform: scale(1.05); }
    .spotlight-card img { cursor:pointer; transition: transform 0.3s ease; }
    .spotlight-card img:hover { transform: scale(1.05); }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Helper function to resolve local asset paths for Streamlit

def asset_path(rel_path: str) -> str:
    """Return a path usable by Streamlit <img src=...>.

    We convert to an absolute filesystem path to avoid issues when
    Streamlit's working directory differs.
    """
    return str((Path(__file__).resolve().parent / rel_path).resolve())






# --- Header / Banner
st.markdown("## 🛒 Top Fashion Picks")

products = [
    ("Kurti", "₹899", "assets/kurti.jpg"),
    ("Dress", "₹1199", "assets/dress.jpg"),
    ("Jeans", "₹999", "assets/jeans.jpg"),
    ("Shirt", "₹799", "assets/shirt.jpg"),
    ("Jacket", "₹1299", "assets/jacket.jpg"),
    ("Footwear", "₹999", "assets/footwear.jpg")
]

cols = st.columns(3)

for i, (name, price, img_path) in enumerate(products):
    
    with cols[i % 3]:
        st.markdown(f"""
        <div style="
        background:white;
        border-radius:15px;
        padding:10px;
        margin:10px;
        box-shadow:0 5px 20px rgba(0,0,0,0.1);
        text-align:center;
        ">

        <img src="{asset_path(img_path)}" style="width:100%;border-radius:10px;">

        <h4>{name}</h4>

        <p style="color:#ff3f6c;font-weight:800;">{price}</p>

        </div>
        """, unsafe_allow_html=True)

st.markdown(
        """
        <div class='header-bar'>
            <div class='header-content'>
                <div style='display:flex;align-items:center;gap:12px'>
                    <span class='bag-icon'>🛍️</span>
                    <div class='myntra-logo'>MYNTRA</div>
                </div>
                <div class='header-text' style='flex:1'>
                    <h1 style='color:white;margin:0'>Bharat Fashion AI</h1>
                    <p>Discover your style • Smart recommendations • Best prices</p>
                </div>
                <div style='text-align:right'>
                    <a href='https://www.myntra.com/' target='_blank' style='text-decoration:none'><div class='cta-button'><button style='cursor:pointer'>✨ Explore</button></div></a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

# --- Main Cover Image
st.markdown("""
<div style='border-radius:16px;overflow:hidden;box-shadow: 0 20px 50px rgba(0,0,0,0.15);margin-bottom:24px;height:300px'>
    <a href='https://www.myntra.com/' target='_blank' style='text-decoration:none;display:block;height:100%'>
        <img src='""" + ASSETS_ABS["hero"] + """' style='width:100%;height:100%;object-fit:cover;cursor:pointer;transition: transform 0.3s ease' onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'"/>
    </a>
</div>
""", unsafe_allow_html=True)

# --- Selection Section with Cover Image
st.markdown("""
<div style='border-radius:12px;overflow:hidden;box-shadow: 0 15px 40px rgba(0,0,0,0.12);margin-bottom:24px;height:250px;position:relative'>
    <img src='""" + ASSETS_ABS["app_banner"] + """' style='width:100%;height:100%;object-fit:cover'/>
    <div style='position:absolute;top:0;left:0;right:0;bottom:0;background:linear-gradient(135deg, rgba(102,126,234,0.7) 0%, rgba(118,75,162,0.7) 100%);display:flex;align-items:center;justify-content:center'>
        <div style='text-align:center;color:white'>
            <h2 style='margin:0;font-size:32px;font-weight:800'>Find Your Perfect Style</h2>
            <p style='margin:8px 0 0 0;font-size:16px;opacity:0.95'>Select occasion & budget to get personalized recommendations</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Controls
col1, col2 = st.columns([2, 1])

with col1:
    occasion = st.selectbox(
        "👕 Select Occasion",
        [
            "Casual",
            "Festival",
            "Office",
            "Party"
        ]
    )

with col2:
    budget = st.slider(
        "💰 Select Budget (₹)",
        500,
        3000,
        1000
    )

# --- Occasion Images Preview
st.markdown("""
<div style='display:flex;gap:12px;margin-top:16px;flex-wrap:wrap'>
    <div style='flex:1;min-width:120px;border-radius:10px;overflow:hidden;box-shadow:0 8px 20px rgba(0,0,0,0.1);background:#f0f0f0'>
        <a href='https://www.myntra.com/jeans' target='_blank' style='text-decoration:none;display:block'>
            <img src='""" + ASSETS_ABS["casual"] + """' alt='Casual' style='width:100%;height:120px;object-fit:cover;cursor:pointer;display:block'/>
            <div style='padding:8px;text-align:center;background:#f9f9f9'>
                <small style='font-weight:700;color:#333'>Casual</small>
            </div>
        </a>
    </div>
    <div style='flex:1;min-width:120px;border-radius:10px;overflow:hidden;box-shadow:0 8px 20px rgba(0,0,0,0.1);background:#f0f0f0'>
        <a href='https://www.myntra.com/kurti' target='_blank' style='text-decoration:none;display:block'>
            <img src='""" + ASSETS_ABS["festival"] + """' alt='Festival' style='width:100%;height:120px;object-fit:cover;cursor:pointer;display:block'/>
            <div style='padding:8px;text-align:center;background:#f9f9f9'>
                <small style='font-weight:700;color:#333'>Festival</small>
            </div>
        </a>
    </div>
    <div style='flex:1;min-width:120px;border-radius:10px;overflow:hidden;box-shadow:0 8px 20px rgba(0,0,0,0.1);background:#f0f0f0'>
        <a href='https://www.myntra.com/trousers' target='_blank' style='text-decoration:none;display:block'>
            <img src='""" + ASSETS_ABS["office"] + """' alt='Office' style='width:100%;height:120px;object-fit:cover;cursor:pointer;display:block'/>
            <div style='padding:8px;text-align:center;background:#f9f9f9'>
                <small style='font-weight:700;color:#333'>Office</small>
            </div>
        </a>
    </div>
    <div style='flex:1;min-width:120px;border-radius:10px;overflow:hidden;box-shadow:0 8px 20px rgba(0,0,0,0.1);background:#f0f0f0'>
        <a href='https://www.myntra.com/dresses' target='_blank' style='text-decoration:none;display:block'>
            <img src='""" + ASSETS_ABS["party"] + """' alt='Party' style='width:100%;height:120px;object-fit:cover;cursor:pointer;display:block'/>
            <div style='padding:8px;text-align:center;background:#f9f9f9'>
                <small style='font-weight:700;color:#333'>Party</small>
            </div>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sample fashion image gallery (attractive, royalty-free images)
st.markdown("### Trending now")
st.markdown("""
<div style='border-radius:12px;overflow:hidden;box-shadow: 0 15px 40px rgba(0,0,0,0.12);margin-bottom:18px;height:200px'>
    <a href='https://www.myntra.com/trending' target='_blank' style='text-decoration:none;display:block;height:100%'>
        <img src='""" + ASSETS["sale"] + """' style='width:100%;height:100%;object-fit:cover;cursor:pointer;transition: transform 0.3s ease' onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'"/>
    </a>
</div>
""", unsafe_allow_html=True)

gallery = [
    ("Trending", ASSETS["sale"], "https://www.myntra.com/trending"),
    ("Ethnic Picks", ASSETS["ethnic"], "https://www.myntra.com/kurti"),
    ("Western Edit", ASSETS["dress"], "https://www.myntra.com/dresses"),
]

cards_html = "<div class='card-row'>"
for title, url, link in gallery:
    cards_html += f"<a href='{link}' target='_blank' style='text-decoration:none;color:inherit'><div class='card' style=\"background-image:url('{url}')\">"
    cards_html += f"<div class='overlay'><div class='card-title'>{title}</div><p style='color:#fff;font-size:12px;margin:6px 0 0 0'>Click to explore →</p></div></div></a>"
cards_html += "</div>"

st.markdown(cards_html, unsafe_allow_html=True)

# --- Features Section with Images
st.markdown("### Why Choose Bharat Fashion AI?")
st.markdown("""
<div style='border-radius:12px;overflow:hidden;box-shadow: 0 15px 40px rgba(0,0,0,0.12);margin-bottom:18px;height:200px'>
    <a href='https://www.myntra.com/women' target='_blank' style='text-decoration:none;display:block;height:100%'>
        <img src='""" + ASSETS["women"] + """' style='width:100%;height:100%;object-fit:cover;cursor:pointer;transition: transform 0.3s ease' onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'"/>
    </a>
</div>
""", unsafe_allow_html=True)

features_col1, features_col2, features_col3 = st.columns(3)

with features_col1:
    st.markdown("""
    <div class='feature-card' style='text-align:center;padding:20px;background:#f5f5f5;border-radius:12px'>
        <a href='https://www.myntra.com/women' target='_blank' style='text-decoration:none'>
            <img src='""" + ASSETS["beauty"] + """' style='width:100%;height:150px;object-fit:cover;border-radius:8px;margin-bottom:10px'/>
        </a>
        <h3 style='margin:10px 0;color:#667eea'>Smart AI</h3>
        <p style='font-size:12px;color:#666'>Personalized recommendations based on your style</p>
    </div>
    """, unsafe_allow_html=True)

with features_col2:
    st.markdown("""
    <div class='feature-card' style='text-align:center;padding:20px;background:#f5f5f5;border-radius:12px'>
        <a href='https://www.myntra.com/offers' target='_blank' style='text-decoration:none'>
            <img src='""" + ASSETS["men"] + """' style='width:100%;height:150px;object-fit:cover;border-radius:8px;margin-bottom:10px'/>
        </a>
        <h3 style='margin:10px 0;color:#764ba2'>Best Prices</h3>
        <p style='font-size:12px;color:#666'>Find products within your budget instantly</p>
    </div>
    """, unsafe_allow_html=True)

with features_col3:
    st.markdown("""
    <div class='feature-card' style='text-align:center;padding:20px;background:#f5f5f5;border-radius:12px'>
        <a href='https://www.myntra.com/' target='_blank' style='text-decoration:none'>
            <img src='""" + ASSETS["kids"] + """' style='width:100%;height:150px;object-fit:cover;border-radius:8px;margin-bottom:10px'/>
        </a>
        <h3 style='margin:10px 0;color:#f093fb'>Diverse Style</h3>
        <p style='font-size:12px;color:#666'>Casual, ethnic, party wear & more</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Fashion Spotlight")
st.markdown("""
<div style='border-radius:12px;overflow:hidden;box-shadow: 0 15px 40px rgba(0,0,0,0.12);margin-bottom:18px;height:200px'>
    <a href='https://www.myntra.com/' target='_blank' style='text-decoration:none;display:block;height:100%'>
        <img src='""" + ASSETS["premium"] + """' style='width:100%;height:100%;object-fit:cover;cursor:pointer;transition: transform 0.3s ease' onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'"/>
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='display:flex;gap:16px;flex-wrap:wrap;margin-bottom:18px'>
  <div class='spotlight-card' style='flex:1;min-width:280px;border-radius:16px;overflow:hidden;box-shadow:0 20px 40px rgba(0,0,0,0.1)'>
    <a href='https://www.myntra.com/trending' target='_blank' style='text-decoration:none;color:inherit'>
        <img src='""" + ASSETS["sale"] + """' style='width:100%;height:240px;object-fit:cover;cursor:pointer'/>
    </a>
    <div style='padding:16px;background:#fff'>
      <h3 style='margin:0 0 8px 0;color:#333'>Trending Now</h3>
      <p style='margin:0;color:#666;font-size:14px'>Stylish picks for every occasion.</p>
    </div>
  </div>
  <div class='spotlight-card' style='flex:1;min-width:280px;border-radius:16px;overflow:hidden;box-shadow:0 20px 40px rgba(0,0,0,0.1)'>
    <a href='https://www.myntra.com/ethnic' target='_blank' style='text-decoration:none;color:inherit'>
        <img src='""" + ASSETS["festival_banner"] + """' style='width:100%;height:240px;object-fit:cover;cursor:pointer'/>
    </a>
    <div style='padding:16px;background:#fff'>
      <h3 style='margin:0 0 8px 0;color:#333'>Festival Ready</h3>
      <p style='margin:0;color:#666;font-size:14px'>Ethnic looks with modern appeal.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if st.button("✨ Get Recommendations"):

    result = recommend(
        occasion,
        budget
    )

    st.success("Recommendations Generated")
    
    st.markdown("""
    <div style='border-radius:12px;overflow:hidden;box-shadow: 0 15px 40px rgba(0,0,0,0.12);margin-bottom:18px;height:200px'>
        <a href='https://www.myntra.com/' target='_blank' style='text-decoration:none;display:block;height:100%'>
            <img src='""" + ASSETS["premium"] + """' style='width:100%;height:100%;object-fit:cover;cursor:pointer;transition: transform 0.3s ease' onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'"/>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare default images for occasions - Using ASSETS
    
    default_images = {
        'Casual': ASSETS['casual'],
        'Festival': ASSETS['festival'],
        'Office': ASSETS['office'],
        'Party': ASSETS['party']
    }
    
    category_links = {
        'Kurti': 'https://www.myntra.com/kurti',
        'Jeans': 'https://www.myntra.com/jeans',
        'Tshirt': 'https://www.myntra.com/tshirts',
        'Shirt': 'https://www.myntra.com/shirts',
        'Saree': 'https://www.myntra.com/saree',
        'Jacket': 'https://www.myntra.com/jackets',
        'Dress': 'https://www.myntra.com/dresses'
    }
    occasion_links = {
        'Casual': 'https://www.myntra.com/casual-wear',
        'Festival': 'https://www.myntra.com/ethnic',
        'Office': 'https://www.myntra.com/formal-wear',
        'Party': 'https://www.myntra.com/dresses'
    }

    st.markdown("### Recommendations")

    # Category to image mapping - Using ASSETS dictionary
    category_images = {
        'Kurti': ASSETS['kurti'],
        'Jeans': ASSETS['casual'],
        'Tshirt': ASSETS['casual'],
        'Shirt': ASSETS['men'],
        'Saree': ASSETS['ethnic'],
        'Jacket': ASSETS['premium'],
        'Dress': ASSETS['dress'],
        'Gown': ASSETS['party'],
        'Lehenga': ASSETS['festival'],
        'Sherwani': ASSETS['men'],
        'Blazer': ASSETS['office'],
        'Heels': ASSETS['women'],
        'Winter': ASSETS['casual']
    }

    # If result is a DataFrame-like with columns, render colorful cards with images
    try:
        df = result
        if hasattr(df, 'head') and hasattr(df, 'columns'):
            rows = df.head(6)
            rec_html = "<div class='rec-row'>"
            for idx, (_, row) in enumerate(rows.iterrows()):
                category = row.get('Category', 'Product')
                price = row.get('Price', '')
                img_url = category_images.get(category, default_images.get(occasion, list(default_images.values())[0]))
                # Fallback to occasion image if category image doesn't load
                if not img_url:
                    img_url = default_images.get(occasion, ASSETS['dress'])
                product_url = occasion_links.get(occasion, category_links.get(category, f"https://www.myntra.com/search?q={quote_plus(str(category))}"))
                rec_html += f"<a href='{product_url}' target='_blank' style='text-decoration:none;color:inherit'><div class='rec-card'><img src='{img_url}' alt='{category}' style='cursor:pointer' onerror=\"this.src='{ASSETS['dress']}'\"/><div class='rec-card-body'><div style='font-weight:700'>{category}</div><div class='price'>₹{price}</div></div></div></a>"
            rec_html += "</div>"
            st.markdown(rec_html, unsafe_allow_html=True)
        else:
            # Fallback: show raw result
            st.dataframe(result, use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying recommendations: {e}")
        st.dataframe(result, use_container_width=True)

# --- Category Gallery Section (Always visible)
st.markdown("---")
st.markdown("### Fashion Categories")
st.markdown("""
<div style='border-radius:12px;overflow:hidden;box-shadow: 0 15px 40px rgba(0,0,0,0.12);margin-bottom:18px;height:200px'>
    <a href='https://www.myntra.com/' target='_blank' style='text-decoration:none;display:block;height:100%'>
        <img src='""" + ASSETS["ethnic"] + """' style='width:100%;height:100%;object-fit:cover;cursor:pointer;transition: transform 0.3s ease' onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'"/>
    </a>
</div>
""", unsafe_allow_html=True)

category_showcase = [
    ('Women\'s Ethnic', ASSETS["ethnic"], 'https://www.myntra.com/kurti'),
    ('Men\'s Wear', ASSETS["men"], 'https://www.myntra.com/shirts'),
    ('Footwear', ASSETS["dress"], 'https://www.myntra.com/footwear'),
    ('Outerwear', ASSETS["premium"], 'https://www.myntra.com/jackets'),
    ('Winter Wear', ASSETS["casual"], 'https://www.myntra.com/jackets'),
]

cols = st.columns(len(category_showcase))

for idx, (cat_name, cat_img, cat_link) in enumerate(category_showcase):
    with cols[idx]:
        st.markdown(f"""
        <a href='{cat_link}' target='_blank' style='text-decoration:none'>
        <div style='text-align:center;background:#f9f9f9;padding:12px;border-radius:10px;border:2px solid #eee;cursor:pointer;transition: transform 0.3s ease' onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
            <img src='{cat_img}' style='width:100%;height:100px;object-fit:cover;border-radius:6px;margin-bottom:8px;cursor:pointer'/>
            <h4 style='margin:8px 0;color:#333;font-size:13px'>{cat_name}</h4>
        </div>
        </a>
        """, unsafe_allow_html=True)

st.markdown("---")

st.caption(
    "Built for Myntra WeForShe 2026"
)