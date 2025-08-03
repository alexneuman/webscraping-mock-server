
from decimal import Decimal

from models.category import Category

pseudo_brand_names = [
    "Zenvana", "Frostiq", "Lumeno", "Driftory", "Nexora", "Snappi", "Veltrix",
    "Blunova", "Pixego", "Grovia", "Klypto", "Avanafy", "Qubitro", "Breezio",
    "Thryvo", "Orbexa", "Vintari", "Cravely", "Moxora", "Chromaic", "Zipnix",
    "Lunexa", "Yondify", "Tribleo", "Aerly", "Glowser", "Flixera", "Nebulyn",
    "Quantasy", "Trevoxa", "Vasture", "Juvox", "Bravayo", "Zentomi", "Twixly",
    "Savora", "Mindaro", "Xendria", "Nomixy", "Kleptoza", "Uptono", "Glimver",
    "Orbion", "Dexora", "Plentza", "Fynera", "Axenor", "Olixta", "Nuvista",
    "Fuzora", "Wavento", "Drivaro", "Lyphiq", "Craxel", "Xylentis", "Snorix",
    "Virelia", "Nimello", "Zyptra", "Optivio", "Grainza", "Trovexa", "Epikta",
    "Hushory", "Jomira", "Vintiq", "Slyntra", "Opthera", "Clyvera", "Zentrik",
    "Blytro", "Mingleo", "Velzio", "Bravexa", "Xanoji", "Quantori", "Tyxo",
    "Raventa", "Nyxora", "Zaluxo", "Drimza", "Plynza", "Solnix", "Klumira",
    "Trenzia", "Zorvia", "Skyntra", "Fravix", "Vibrosa", "Myntraq", "Zylenta",
    "Bluntry", "Clevara", "Jentro", "Obzoro", "Knivix", "Fyloxa", "Zetari",
    "Wondora", "Vortiq", "Thryzo", "Omnika"
]


psuedo_categories = [
    "Technology",
    "Health & Wellness",
    "Finance",
    "Education",
    "Entertainment",
    "Fashion",
    "Food & Beverage",
    "Travel",
    "Home & Garden",
    "Sports & Fitness",
    "Automotive",
    "Real Estate",
    "Beauty & Personal Care",
    "Gaming",
    "Pets",
    "Art & Design",
    "News & Media",
    "Business Services",
    "E-commerce",
    "Non-Profit & Charity"
]

def assign_n_uneven_categories_by_index(i, categories, n) -> list[Category]:
    """
        A function that arbitrarily, deterministically adds categories to products
        
    """
    num_categories = len(categories)
    base = i % num_categories

    # Generate `n` pseudo-random but deterministic category indices
    cat_indices = [
        (base + (i * j + j**2 + 3)) % num_categories
        for j in range(n)
    ]

    # Remove duplicates, keep order, map to category names
    seen = set()
    cat_names = [categories[j] for j in cat_indices if j not in seen and not seen.add(j)]

    return cat_names


def get_fake_categories() -> list[Category]:
    return [ Category(name=c) for c in psuedo_categories]

import hashlib

def generate_fake_price(index: int, total_items: int, min_price: float = 500.0, max_price: float = 20000.0) -> Decimal:
    """
    Generate a deterministic, irregular fake price based on index using hashing.
    Not linear, not curved, but stable and within bounds.
    """
    # Clamp index
    index = max(0, min(index, total_items - 1))

    # Hash the index (convert to bytes)
    hash_bytes = hashlib.sha256(str(index).encode()).digest()

    # Take first 4 bytes to get a pseudo-random int
    raw_int = int.from_bytes(hash_bytes[:4], 'big')

    # Normalize to a 0–1 float
    normalized = raw_int / 0xFFFFFFFF

    # Scale to price range
    price = min_price + normalized * (max_price - min_price)
    return Decimal(round(price, 2))
