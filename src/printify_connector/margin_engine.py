"""Printify Profit Margin & Pricing Calculator Engine.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from .catalog import get_blueprint, get_provider


def calculate_margins(
    blueprint_id: Any,
    retail_price: float,
    provider_id: Optional[Any] = None,
    is_premium: bool = True,
    channel: str = "etsy",
    shipping_destination: str = "US",
    quantity: int = 1
) -> Dict[str, Any]:
    """Calculate production costs, fees, profit, and margins."""
    blueprint = get_blueprint(blueprint_id)
    if not blueprint:
        raise ValueError(f"Unknown blueprint ID or slug '{blueprint_id}'")

    p_id = provider_id or blueprint.get("default_provider_id", 10)
    provider = get_provider(p_id)

    # 1. Base Production Cost (Apply 20% discount if Printify Premium)
    base_unit_cost = blueprint["base_cost_premium"] if is_premium else blueprint["base_cost_standard"]
    total_production_cost = round(base_unit_cost * quantity, 2)
    standard_unit_cost = blueprint["base_cost_standard"]
    premium_savings = round((standard_unit_cost - base_unit_cost) * quantity, 2) if is_premium else 0.0

    # 2. Shipping Cost
    is_us = shipping_destination.upper() in ["US", "USA", "UNITED STATES"]
    if provider:
        if is_us:
            first_item = provider.get("shipping_standard_us", 4.75)
            additional_item = provider.get("shipping_additional_us", 2.20)
        else:
            first_item = provider.get("shipping_international", 10.50)
            additional_item = provider.get("shipping_international", 10.50) * 0.6
        shipping_cost = round(first_item + (additional_item * max(0, quantity - 1)), 2)
    else:
        shipping_cost = 4.75 if is_us else 10.50

    # 3. Total COGS (Cost of Goods Sold)
    total_cogs = round(total_production_cost + shipping_cost, 2)

    # 4. Sales Channel Platform Fees
    total_revenue = round(retail_price * quantity, 2)
    channel_norm = channel.lower()

    if channel_norm == "etsy":
        # Etsy: 6.5% transaction fee + 3% + $0.25 payment processing + $0.20 listing fee
        transaction_fee = total_revenue * 0.065
        processing_fee = (total_revenue * 0.03) + 0.25
        listing_fee = 0.20
        total_platform_fees = round(transaction_fee + processing_fee + listing_fee, 2)
    elif channel_norm == "shopify":
        # Shopify Basic: 2.9% + $0.30 payment gateway fee
        total_platform_fees = round((total_revenue * 0.029) + 0.30, 2)
    else:
        # Default direct checkout / web3 (e.g. Stripe 2.9% + $0.30 or DePay 0% fee)
        total_platform_fees = round((total_revenue * 0.029) + 0.30, 2)

    # 5. Net Profit & Margin
    total_expenses = round(total_cogs + total_platform_fees, 2)
    net_profit = round(total_revenue - total_expenses, 2)
    profit_margin_pct = round((net_profit / total_revenue) * 100, 1) if total_revenue > 0 else 0.0

    # 6. Break-Even Price Calculation
    # Revenue = COGS + Fees
    # For Etsy: Rev = COGS + 0.095*Rev + 0.45 => Rev*(1 - 0.095) = COGS + 0.45 => Rev = (COGS + 0.45) / 0.905
    if channel_norm == "etsy":
        break_even_total = (total_cogs + 0.45) / 0.905
    else:
        break_even_total = (total_cogs + 0.30) / 0.971
    break_even_unit = round(break_even_total / quantity, 2)

    # 7. Recommended Pricing Tiers (for single item)
    rec_aggressive = round(break_even_unit / 0.70, 2)  # 30% margin
    rec_balanced = round(break_even_unit / 0.50, 2)    # 50% margin
    rec_premium = round(break_even_unit / 0.35, 2)     # 65% margin

    return {
        "blueprint_id": blueprint_id,
        "blueprint_title": blueprint["title"],
        "brand": blueprint["brand"],
        "quantity": quantity,
        "is_premium": is_premium,
        "channel": channel.upper(),
        "shipping_destination": "US" if is_us else "International",
        "retail_price_unit": retail_price,
        "total_revenue": total_revenue,
        "base_production_cost": total_production_cost,
        "premium_savings": premium_savings,
        "shipping_cost": shipping_cost,
        "total_cogs": total_cogs,
        "platform_fees": total_platform_fees,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "profit_margin_pct": profit_margin_pct,
        "break_even_price": break_even_unit,
        "recommended_pricing": {
            "tier_30_pct": rec_aggressive,
            "tier_50_pct": rec_balanced,
            "tier_65_pct": rec_premium
        }
    }


def calculate_multi_channel_margins(
    blueprint_id: Any,
    retail_price: float,
    shipping_charged: float = 4.99,
    has_printify_premium: bool = False,
    target_margin_pct: float = 40.0
) -> Dict[str, Any]:
    """Calculate and compare profit margins across Etsy, Shopify, and Direct Web3."""
    blueprint = get_blueprint(blueprint_id)
    if not blueprint:
        raise ValueError(f"Unknown blueprint ID or slug '{blueprint_id}'")

    channels = ["etsy", "shopify", "direct"]
    channel_comparisons = {}

    for ch in channels:
        calc_std = calculate_margins(
            blueprint_id=blueprint_id,
            retail_price=retail_price,
            is_premium=False,
            channel=ch,
            shipping_destination="US"
        )
        calc_prem = calculate_margins(
            blueprint_id=blueprint_id,
            retail_price=retail_price,
            is_premium=True,
            channel=ch,
            shipping_destination="US"
        )
        channel_comparisons[ch] = {
            "channel": ch.upper(),
            "standard": {
                "base_cost": calc_std["base_production_cost"],
                "shipping": calc_std["shipping_cost"],
                "platform_fees": calc_std["platform_fees"],
                "total_expenses": calc_std["total_expenses"],
                "net_profit": calc_std["net_profit"],
                "margin_pct": calc_std["profit_margin_pct"],
                "break_even": calc_std["break_even_price"]
            },
            "premium": {
                "base_cost": calc_prem["base_production_cost"],
                "savings": calc_prem["premium_savings"],
                "shipping": calc_prem["shipping_cost"],
                "platform_fees": calc_prem["platform_fees"],
                "total_expenses": calc_prem["total_expenses"],
                "net_profit": calc_prem["net_profit"],
                "margin_pct": calc_prem["profit_margin_pct"],
                "break_even": calc_prem["break_even_price"]
            },
            "annual_savings_100_sales": round(calc_prem["premium_savings"] * 100, 2),
            "annual_savings_500_sales": round(calc_prem["premium_savings"] * 500, 2)
        }

    # Active selection
    active_calc = calculate_margins(
        blueprint_id=blueprint_id,
        retail_price=retail_price,
        is_premium=has_printify_premium,
        channel="etsy",
        shipping_destination="US"
    )

    return {
        "blueprint": {
            "id": blueprint["id"],
            "title": blueprint["title"],
            "brand": blueprint["brand"],
            "category": blueprint["category"],
            "base_cost_standard": blueprint["base_cost_standard"],
            "base_cost_premium": blueprint["base_cost_premium"]
        },
        "inputs": {
            "retail_price": retail_price,
            "shipping_charged": shipping_charged,
            "has_printify_premium": has_printify_premium,
            "target_margin_pct": target_margin_pct
        },
        "active_summary": active_calc,
        "channels": channel_comparisons,
        "premium_20_pct_discount_active": has_printify_premium,
        "premium_subscription_annual_roi": {
            "cost_per_year": 300.00,  # $24.99/mo or $299/yr
            "break_even_orders": round(300.00 / (blueprint["base_cost_standard"] - blueprint["base_cost_premium"]), 1) if (blueprint["base_cost_standard"] - blueprint["base_cost_premium"]) > 0 else 0
        }
    }


def calculate_shipping_rates(
    blueprint_id: Any,
    destination: str = "US",
    is_express: bool = False
) -> Dict[str, Any]:
    """Calculate standard and express shipping rates for a blueprint and provider."""
    blueprint = get_blueprint(blueprint_id)
    if not blueprint:
        raise ValueError(f"Unknown blueprint ID or slug '{blueprint_id}'")

    provider_id = blueprint.get("default_provider_id", 10)
    provider = get_provider(provider_id)

    is_us = destination.upper() in ["US", "USA", "UNITED STATES"]

    if provider:
        std_first = provider.get("shipping_standard_us", 4.75) if is_us else provider.get("shipping_international", 10.50)
        std_add = provider.get("shipping_additional_us", 2.20) if is_us else provider.get("shipping_international", 10.50) * 0.6
        provider_name = provider.get("name", "Default Provider")
        lead_days = provider.get("avg_production_days", 2.0)
    else:
        std_first = 4.75 if is_us else 10.50
        std_add = 2.20 if is_us else 6.30
        provider_name = "Default Print Provider"
        lead_days = 2.5

    exp_multiplier = 2.2 if is_us else 2.8
    express_first = round(std_first * exp_multiplier, 2)
    express_add = round(std_add * 1.5, 2)

    return {
        "blueprint_id": blueprint["id"],
        "blueprint_title": blueprint["title"],
        "provider_name": provider_name,
        "destination": "US" if is_us else destination.upper(),
        "is_express": is_express,
        "estimated_production_days": lead_days,
        "standard_delivery": {
            "carrier": "USPS First Class / DHL eCommerce" if is_us else "Asendia / PostNL",
            "transit_days": "3-5 business days" if is_us else "7-15 business days",
            "first_item_cost": std_first,
            "additional_item_cost": std_add
        },
        "express_delivery": {
            "carrier": "FedEx 2Day / UPS Ground" if is_us else "FedEx International",
            "transit_days": "2-3 business days" if is_us else "3-5 business days",
            "first_item_cost": express_first,
            "additional_item_cost": express_add
        }
    }
