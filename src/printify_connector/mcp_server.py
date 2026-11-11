"""Antigravity MCP JSON-RPC 2.0 Server for Printify Connector.

Engineered by 1nc0gn30 (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

from . import __version__
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
        return {"blueprint_id": b_id, "source": "printify_api" if client.is_live else "offline_reference_catalog", "providers": client.get_print_providers(b_id)}

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


def handle_request(req: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Dispatch one JSON-RPC 2.0 message. Returns None for notifications."""
    req_id = req.get("id")
    method = req.get("method")
    if req_id is None and isinstance(method, str) and method.startswith("notifications/"):
        return None
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": (req.get("params") or {}).get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "printify-connector", "version": __version__},
        }}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = req.get("params") or {}
        try:
            result = handle_tool_call(params.get("name"), params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": req_id, "result": {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}]}}
        except Exception as exc:  # tool-level failure is reported to the model, not as a protocol error
            return {"jsonrpc": "2.0", "id": req_id, "result": {
                "isError": True, "content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {method} not found"}}


def run_mcp_server() -> None:
    """Run MCP JSON-RPC 2.0 stdio server loop."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            resp = handle_request(json.loads(line))
        except json.JSONDecodeError as e:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {e}"}}
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
