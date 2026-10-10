"""Printify Blueprint and Print Provider Catalog Database.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# Verified Printify Blueprints with real industry specifications
PRINTIFY_BLUEPRINTS: List[Dict[str, Any]] = [
    {
        "id": 12,
        "title": "Unisex Jersey Short Sleeve Tee",
        "brand": "Bella+Canvas 3001",
        "category": "Men's Clothing / T-Shirts",
        "description": "The classic Bella+Canvas 3001 unisex jersey short sleeve tee fits like a well-loved favorite with soft 100% cotton.",
        "base_cost_standard": 9.15,
        "base_cost_premium": 7.32,
        "print_areas": [
            {"position": "front", "width": 4000, "height": 4800, "recommended_dpi": 300},
            {"position": "back", "width": 4000, "height": 4800, "recommended_dpi": 300},
            {"position": "neck", "width": 1200, "height": 1200, "recommended_dpi": 300}
        ],
        "default_provider_id": 10,
        "popular": True,
        "tags": ["apparel", "t-shirt", "bella-canvas", "bestseller", "cotton"]
    },
    {
        "id": 49,
        "title": "Unisex Heavy Blend™ Crewneck Sweatshirt",
        "brand": "Gildan 18000",
        "category": "Men's Clothing / Sweatshirts",
        "description": "A sturdy and warm sweatshirt bound to keep you warm in the colder months. 50% cotton, 50% polyester pre-shrunk fleece knit.",
        "base_cost_standard": 13.84,
        "base_cost_premium": 11.07,
        "print_areas": [
            {"position": "front", "width": 4200, "height": 4800, "recommended_dpi": 300},
            {"position": "back", "width": 4200, "height": 4800, "recommended_dpi": 300}
        ],
        "default_provider_id": 29,
        "popular": True,
        "tags": ["apparel", "sweatshirt", "crewneck", "gildan", "warm", "bestseller"]
    },
    {
        "id": 77,
        "title": "Unisex Heavy Blend™ Hooded Sweatshirt",
        "brand": "Gildan 18500",
        "category": "Men's Clothing / Hoodies",
        "description": "Crafted with 50% cotton and 50% polyester, this classic hoodie offers a spacious kangaroo pocket and matching drawstrings.",
        "base_cost_standard": 17.50,
        "base_cost_premium": 14.00,
        "print_areas": [
            {"position": "front", "width": 4200, "height": 3800, "recommended_dpi": 300},
            {"position": "back", "width": 4200, "height": 4800, "recommended_dpi": 300}
        ],
        "default_provider_id": 29,
        "popular": True,
        "tags": ["apparel", "hoodie", "gildan", "outerwear", "bestseller"]
    },
    {
        "id": 68,
        "title": "Ceramic Mug 11oz",
        "brand": "Generic",
        "category": "Home & Living / Mugs",
        "description": "Glossy high-grade ceramic mug suitable for both hot and cold beverages. Microwave and dishwasher safe.",
        "base_cost_standard": 4.60,
        "base_cost_premium": 3.68,
        "print_areas": [
            {"position": "full_wrap", "width": 2475, "height": 1155, "recommended_dpi": 300}
        ],
        "default_provider_id": 3,
        "popular": True,
        "tags": ["home-and-living", "mugs", "ceramic", "coffee", "bestseller"]
    },
    {
        "id": 84,
        "title": "Matte Vertical Canvas Wrap (16x24 in)",
        "brand": "Generic",
        "category": "Home & Living / Canvas",
        "description": "Premium artist-grade cotton canvas with 1.25 inch solid front construction and archival inks.",
        "base_cost_standard": 22.40,
        "base_cost_premium": 17.92,
        "print_areas": [
            {"position": "front", "width": 5400, "height": 7800, "recommended_dpi": 300}
        ],
        "default_provider_id": 8,
        "popular": True,
        "tags": ["home-and-living", "canvas", "wall-art", "decor", "high-ticket"]
    },
    {
        "id": 92,
        "title": "Stainless Steel Polar Camel Tumbler 20oz",
        "brand": "Polar Camel",
        "category": "Home & Living / Drinkware",
        "description": "Double-wall vacuum insulated tumbler with clear lid. Keeps drinks cold for 24 hours or hot for 8 hours.",
        "base_cost_standard": 12.20,
        "base_cost_premium": 9.76,
        "print_areas": [
            {"position": "wrap", "width": 2800, "height": 2200, "recommended_dpi": 300}
        ],
        "default_provider_id": 24,
        "popular": False,
        "tags": ["drinkware", "tumbler", "stainless-steel", "travel"]
    },
    {
        "id": 142,
        "title": "Spiral Notebook (Ruled Line)",
        "brand": "Generic",
        "category": "Stationery / Notebooks",
        "description": "118 page spiral notebook with ruled line paper. Excellent companion for daily journaling and sketches.",
        "base_cost_standard": 6.80,
        "base_cost_premium": 5.44,
        "print_areas": [
            {"position": "front", "width": 1950, "height": 2400, "recommended_dpi": 300}
        ],
        "default_provider_id": 16,
        "popular": False,
        "tags": ["stationery", "journal", "notebook", "gift"]
    }
]

# Verified Print Providers
PRINT_PROVIDERS: List[Dict[str, Any]] = [
    {
        "id": 10,
        "name": "Monster Digital",
        "location": "United States (Miami, FL)",
        "rating": 9.4,
        "avg_production_days": 2.1,
        "shipping_standard_us": 4.75,
        "shipping_additional_us": 2.20,
        "shipping_international": 10.50,
        "status": "Optimal"
    },
    {
        "id": 29,
        "name": "SwiftPOD",
        "location": "United States (San Jose, CA)",
        "rating": 9.6,
        "avg_production_days": 1.9,
        "shipping_standard_us": 4.95,
        "shipping_additional_us": 2.40,
        "shipping_international": 11.20,
        "status": "Optimal"
    },
    {
        "id": 3,
        "name": "District Photo",
        "location": "United States (Beltsville, MD)",
        "rating": 9.1,
        "avg_production_days": 2.8,
        "shipping_standard_us": 5.80,
        "shipping_additional_us": 3.10,
        "shipping_international": 12.00,
        "status": "Optimal"
    },
    {
        "id": 8,
        "name": "Drive Fulfillment",
        "location": "United States (Salt Lake City, UT)",
        "rating": 9.3,
        "avg_production_days": 2.4,
        "shipping_standard_us": 9.50,
        "shipping_additional_us": 4.50,
        "shipping_international": 18.00,
        "status": "Optimal"
    },
    {
        "id": 24,
        "name": "MyLocker",
        "location": "United States (Detroit, MI)",
        "rating": 8.9,
        "avg_production_days": 3.2,
        "shipping_standard_us": 5.50,
        "shipping_additional_us": 2.75,
        "shipping_international": 13.50,
        "status": "Good"
    },
    {
        "id": 16,
        "name": "Spoke Custom Products",
        "location": "United States (Atlanta, GA)",
        "rating": 9.2,
        "avg_production_days": 2.3,
        "shipping_standard_us": 4.90,
        "shipping_additional_us": 2.10,
        "shipping_international": 9.80,
        "status": "Optimal"
    }
]


BLUEPRINTS = PRINTIFY_BLUEPRINTS

SLUG_TO_BLUEPRINT_ID: Dict[str, int] = {
    "bella_canvas_3001": 12,
    "bella-canvas-3001": 12,
    "unisex_jersey_tee": 12,
    "gildan_18000": 49,
    "gildan-18000": 49,
    "crewneck_sweatshirt": 49,
    "gildan_18500": 77,
    "gildan-18500": 77,
    "hooded_sweatshirt": 77,
    "hoodie": 77,
    "ceramic_mug_11oz": 68,
    "ceramic_mug": 68,
    "mug": 68,
    "canvas_wrap": 84,
    "matte_canvas": 84,
    "canvas": 84,
    "polar_camel_tumbler": 92,
    "tumbler": 92,
    "spiral_notebook": 142,
    "notebook": 142,
    "journal": 142
}

SLUG_TO_PROVIDER_ID: Dict[str, int] = {
    "monster_digital": 10,
    "monster-digital": 10,
    "swiftpod": 29,
    "swift_pod": 29,
    "district_photo": 3,
    "district-photo": 3,
    "drive_fulfillment": 8,
    "drive-fulfillment": 8,
    "mylocker": 24,
    "my_locker": 24,
    "spoke_custom": 16,
    "spoke-custom": 16,
    "spoke_custom_products": 16
}


def search_blueprints(query: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Filter blueprints by search query or category."""
    results = PRINTIFY_BLUEPRINTS
    if query:
        q = query.lower()
        results = [
            b for b in results
            if q in b["title"].lower()
            or q in b["brand"].lower()
            or any(q in t for t in b["tags"])
        ]
    if category:
        cat = category.lower()
        results = [b for b in results if cat in b["category"].lower()]
    return results


def list_blueprints(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all blueprints, optionally filtered by category."""
    return search_blueprints(category=category)


def get_blueprint_by_id(blueprint_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve blueprint by integer ID."""
    for b in PRINTIFY_BLUEPRINTS:
        if b["id"] == blueprint_id:
            return b
    return None


def get_blueprint(identifier: Any) -> Optional[Dict[str, Any]]:
    """Retrieve blueprint by int ID, slug, or title match."""
    if identifier is None:
        return None
    if isinstance(identifier, int):
        return get_blueprint_by_id(identifier)
    
    val_str = str(identifier).strip()
    if val_str.isdigit():
        return get_blueprint_by_id(int(val_str))
    
    lower_slug = val_str.lower().replace(" ", "_")
    if lower_slug in SLUG_TO_BLUEPRINT_ID:
        return get_blueprint_by_id(SLUG_TO_BLUEPRINT_ID[lower_slug])
    
    # Fuzzy match by brand or title
    for b in PRINTIFY_BLUEPRINTS:
        if lower_slug in b["title"].lower().replace(" ", "_") or lower_slug in b["brand"].lower().replace(" ", "_"):
            return b
    return None


def list_providers(country: Optional[str] = None) -> List[Dict[str, Any]]:
    """List print providers, optionally filtered by country code."""
    if not country:
        return PRINT_PROVIDERS
    c = country.upper()
    return [p for p in PRINT_PROVIDERS if c in p.get("location", "").upper()]


def get_provider_by_id(provider_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve print provider by integer ID."""
    for p in PRINT_PROVIDERS:
        if p["id"] == provider_id:
            return p
    return None


def get_provider(identifier: Any) -> Optional[Dict[str, Any]]:
    """Retrieve print provider by int ID, slug, or name match."""
    if identifier is None:
        return None
    if isinstance(identifier, int):
        return get_provider_by_id(identifier)
    
    val_str = str(identifier).strip()
    if val_str.isdigit():
        return get_provider_by_id(int(val_str))
    
    lower_slug = val_str.lower().replace(" ", "_")
    if lower_slug in SLUG_TO_PROVIDER_ID:
        return get_provider_by_id(SLUG_TO_PROVIDER_ID[lower_slug])
    
    for p in PRINT_PROVIDERS:
        if lower_slug in p["name"].lower().replace(" ", "_"):
            return p
    return None
