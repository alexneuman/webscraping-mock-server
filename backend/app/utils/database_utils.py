
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

def assign_categories(items, categories):
    assignments = []
    for i, item in enumerate(items):
        # Use a skewed formula to create uneven distribution
        mod = i % 10
        if mod in (0, 1):
            cat_index = 0
        elif mod in (2, 3):
            cat_index = len(categories) // 3
        elif mod == 4:
            cat_index = len(categories) // 2
        elif mod in (5, 6, 7):
            cat_index = (2 * len(categories)) // 3
        else:
            cat_index = len(categories) - 1
        assignments.append((item, categories[cat_index]))
    return assignments

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