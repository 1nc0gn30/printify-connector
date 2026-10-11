"""
CLI Entrypoint for Printify Connector
Supports server daemon, Model Context Protocol (MCP), and local utility commands.
"""

import argparse
import json
import sys

from .artwork_auditor import audit_artwork_dimensions
from .catalog import list_blueprints, list_providers
from .margin_engine import calculate_multi_channel_margins
from .mcp_server import run_mcp_server
from .server import run_server


def main():
    parser = argparse.ArgumentParser(
        prog="printify-connector",
        description="Printify Open API v1 Connector, Blueprint Catalog, & 20% Premium Margin Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Run the HTTP & REST API daemon")
    serve_parser.add_argument("--port", type=int, default=8115, help="HTTP listening port (default: 8115)")
    serve_parser.add_argument("--host", type=str, default="0.0.0.0", help="Binding host address (default: 0.0.0.0)")

    # Command: mcp
    subparsers.add_parser("mcp", help="Run the Antigravity Model Context Protocol (MCP) stdio server")

    # Command: blueprints
    bp_parser = subparsers.add_parser("blueprints", help="List available print blueprints")
    bp_parser.add_argument("--category", type=str, default=None, help="Filter by category (Apparel, Drinkware, Home)")

    # Command: providers
    prov_parser = subparsers.add_parser("providers", help="List verified print providers")
    prov_parser.add_argument("--country", type=str, default=None, help="Filter by country code (US, UK, DE)")

    # Command: margins
    margin_parser = subparsers.add_parser("margins", help="Calculate profit margins across Etsy, Shopify, & Direct Web3")
    margin_parser.add_argument("--blueprint", type=str, default="bella_canvas_3001", help="Blueprint ID")
    margin_parser.add_argument("--price", type=float, default=28.00, help="Retail sale price")
    margin_parser.add_argument("--shipping", type=float, default=4.99, help="Shipping charged to customer")
    margin_parser.add_argument("--premium", action="store_true", help="Apply Printify Premium 20%% cost reduction")

    # Command: audit
    audit_parser = subparsers.add_parser("audit", help="Audit artwork dimensions and DPI against blueprint print area")
    audit_parser.add_argument("--blueprint", type=str, default="bella_canvas_3001", help="Blueprint ID")
    audit_parser.add_argument("--width", type=int, required=True, help="Image width in pixels")
    audit_parser.add_argument("--height", type=int, required=True, help="Image height in pixels")
    audit_parser.add_argument("--name", type=str, default="design.png", help="Filename of artwork")

    # Command: info
    subparsers.add_parser("info", help="Show system status and API configuration")

    args = parser.parse_args()

    if args.command == "serve":
        run_server(port=args.port, host=args.host)
    elif args.command == "mcp":
        run_mcp_server()
    elif args.command == "blueprints":
        items = list_blueprints(args.category)
        print(json.dumps(items, indent=2))
    elif args.command == "providers":
        providers = list_providers(args.country)
        print(json.dumps(providers, indent=2))
    elif args.command == "margins":
        res = calculate_multi_channel_margins(
            blueprint_id=args.blueprint,
            retail_price=args.price,
            shipping_charged=args.shipping,
            has_printify_premium=args.premium
        )
        print(json.dumps(res, indent=2))
    elif args.command == "audit":
        audit = audit_artwork_dimensions(
            blueprint_id=args.blueprint,
            width_px=args.width,
            height_px=args.height,
            file_name=args.name
        )
        print(json.dumps(audit, indent=2))
    elif args.command == "info":
        print(json.dumps({
            "service": "printify-connector",
            "version": "1.0.0",
            "status": "ready",
            "assigned_port": 8115,
            "creator": "Neal Frazier Tech (@1nc0gn30)",
            "monetization": "Stripe ($19 lifetime) + DePay Solana Widget"
        }, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
