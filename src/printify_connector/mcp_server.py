"""Antigravity MCP JSON-RPC 2.0 Server for Printify Connector.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List
from .artwork_auditor import audit_artwork
from .catalog import PRINT_PROVIDERS, get_blueprint_by_id, search_blueprints
from .client import PrintifyClient
from .margin_engine import calculate_margins


TOOLS: List[Dict[str, Any]] = [
    {
        "name": "printify_search_blueprints",
        "description": "Search Printify catalog blueprints (T-shirts, hoodies, mugs, canvases, journals) by title, category, or keyword.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword or brand (e.g. 'Bella Canvas', 'Mug', 'Hoodie')"},
                "category": {"type": "string", "description": "Category filter (e.g. 'Clothing', 'Home & Living')"}
            }
        }
    },
    {
        "name": "printify_get_print_providers",
        "description": "List verified print providers with turnaround times, ratings, and shipping rates for a given blueprint.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "blueprint_id": {"type": "integer", "description": "Integer ID of the Printify blueprint (e.g. 12 for Bella+Canvas 3001)"}
            },
            "required": ["blueprint_id"]
        }
    },
    {
        "name": "printify_calculate_margins",
        "description": "Calculate exact production costs, Printify Premium 20% discount, Etsy/Shopify fees, break-even price, and profit margins.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "blueprint_id": {"type": "integer", "description": "Printify blueprint ID"},
                "retail_price": {"type": "number", "description": "Intended selling price in USD"},
                "channel": {"type": "string", "description": "Sales channel ('etsy' or 'shopify')", "default": "etsy"},
                "is_premium": {"type": "boolean", "description": "Apply Printify Premium 20% discount", "default": True},
                "shipping_destination": {"type": "string", "description": "Destination country code ('US' or 'INTL')", "default": "US"},
                "quantity": {"type": "integer", "description": "Quantity to order", "default": 1}
            },
            "required": ["blueprint_id", "retail_price"]
        }
    },
    {
        "name": "printify_audit_artwork",
        "description": "Audit artwork dimensions, aspect ratio, and effective DPI against blueprint print areas to guarantee 300 DPI high-res print output.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "blueprint_id": {"type": "integer", "description": "Printify blueprint ID"},
                "image_width_px": {"type": "integer", "description": "Artwork width in pixels"},
                "image_height_px": {"type": "integer", "description": "Artwork height in pixels"},
                "print_position": {"type": "string", "description": "Print position ('front', 'back', 'wrap')", "default": "front"}
            },
            "required": ["blueprint_id", "image_width_px", "image_height_px"]
        }
    },
    {
        "name": "printify_create_product_payload",
        "description": "Generate schema-valid Printify product creation payload ready for publishing or API dispatch.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "blueprint_id": {"type": "integer", "description": "Printify blueprint ID"},
                "title": {"type": "string", "description": "Product title"},
                "description": {"type": "string", "description": "Product description"},
                "image_url": {"type": "string", "description": "Public HTTPS URL of artwork image"},
                "retail_price": {"type": "number", "description": "Retail price in USD", "default": 28.00},
                "provider_id": {"type": "integer", "description": "Optional print provider ID"}
            },
            "required": ["blueprint_id", "title", "description", "image_url"]
        }
    },
    {
        "name": "printify_get_shop_info",
        "description": "Retrieve Printify shop information, sales channels, and API connection status.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute tool call and return response."""
    client = PrintifyClient()

    if name == "printify_search_blueprints":
        query = arguments.get("query")
        category = arguments.get("category")
        return {"blueprints": search_blueprints(query, category)}

    elif name == "printify_get_print_providers":
        b_id = arguments["blueprint_id"]
        return {"blueprint_id": b_id, "providers": client.get_print_providers(b_id)}

    elif name == "printify_calculate_margins":
        return calculate_margins(
            blueprint_id=arguments["blueprint_id"],
            retail_price=float(arguments["retail_price"]),
            channel=arguments.get("channel", "etsy"),
            is_premium=arguments.get("is_premium", True),
            shipping_destination=arguments.get("shipping_destination", "US"),
            quantity=int(arguments.get("quantity", 1))
        )

    elif name == "printify_audit_artwork":
        return audit_artwork(
            blueprint_id=arguments["blueprint_id"],
            image_width_px=int(arguments["image_width_px"]),
            image_height_px=int(arguments["image_height_px"]),
            print_position=arguments.get("print_position", "front")
        )

    elif name == "printify_create_product_payload":
        return client.create_product_payload(
            blueprint_id=arguments["blueprint_id"],
            title=arguments["title"],
            description=arguments["description"],
            image_url=arguments["image_url"],
            retail_price=float(arguments.get("retail_price", 28.00)),
            provider_id=arguments.get("provider_id")
        )

    elif name == "printify_get_shop_info":
        return client.get_shop_info()

    raise ValueError(f"Unknown tool: {name}")


def run_mcp_server() -> None:
    """Run MCP JSON-RPC 2.0 stdio server loop."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            if method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                arguments = params.get("arguments", {})
                result = handle_tool_call(name, arguments)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                    }
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method {method} not found"}
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32000, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()
