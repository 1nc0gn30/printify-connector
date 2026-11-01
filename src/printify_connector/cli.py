"""Command Line Interface for Printify Connector.

Engineered by 1nc0gn30 (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from typing import List, Optional

from .artwork_auditor import audit_artwork_dimensions
from .catalog import list_blueprints, list_providers
from .margin_engine import calculate_multi_channel_margins
from .mcp_server import run_mcp_server
from .server import run_server


def _default_bind_host() -> str:
    """Bind address: localhost unless explicitly opted in via $ZOTH_BIND_HOST or
    $HOST (IP literal only; zsh sets HOST to the hostname) or --host."""
    import ipaddress
    for var in ("ZOTH_BIND_HOST", "HOST"):
        val = os.environ.get(var, "").strip()
        if val == "localhost":
            return "127.0.0.1"
        if val:
            try:
                ipaddress.ip_address(val)
                return val
            except ValueError:
                pass
    return "127.0.0.1"


# ANSI Formatting
C_GOLD = "\033[38;5;214m"
C_CYAN = "\033[38;5;51m"
C_GREEN = "\033[38;5;48m"
C_RED = "\033[38;5;196m"
C_AMBER = "\033[38;5;208m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"


def print_banner() -> None:
    print(f"{C_GOLD}{C_BOLD}📦 PRINTIFY CONNECTOR v2.5.0{C_RESET}")
    print(f"{C_DIM}Printify Open API v1 Connector & 20% Premium Margin Engine{C_RESET}")
    print(f"{C_DIM}Engineered by 1nc0gn30 (@1nc0gn30) • NullAI Platform{C_RESET}\n")


def cmd_status(host: str = "127.0.0.1", port: int = 8115, as_json: bool = False) -> int:
    url = f"http://{host}:{port}/health"
    live_info = None
    try:
        with urllib.request.urlopen(url, timeout=2.0) as resp:
            live_info = json.loads(resp.read().decode("utf-8"))
    except Exception:
        pass

    blueprints = list_blueprints()
    providers = list_providers()

    data = {
        "status": "online" if live_info else "standby",
        "service": "printify-connector",
        "version": "2.5.0",
        "port": port,
        "blueprints_count": len(blueprints),
        "providers_count": len(providers),
        "license": "100% Free & Open Access (Zero Paywalls)",
        "daemon": live_info,
    }

    if as_json:
        print(json.dumps(data, indent=2))
        return 0

    print_banner()
    state_color = C_GREEN if live_info else C_AMBER
    print(f"Daemon Status:      {state_color}{data['status'].upper()}{C_RESET} ({url})")
    print(f"Catalog Blueprints: {C_CYAN}{data['blueprints_count']} items cataloged{C_RESET}")
    print(f"Print Providers:    {C_GOLD}{data['providers_count']} verified partners{C_RESET}")
    print(f"Access Guarantee:   100% Free & Open Access (Zero Paywalls)")
    print()
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="printify-connector",
        description="Printify Open API v1 Connector, Blueprint Catalog, & 20% Premium Margin Engine"
    )
    parser.add_argument("-v", "--version", action="version", version="printify-connector 2.5.0")
    parser.add_argument("--status", action="store_true", help="Print local service status and configuration")
    parser.add_argument("--json", action="store_true", help="Output status/telemetry as JSON")
    parser.add_argument("--host", default=_default_bind_host(), help="Host interface (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8115, help="Port to bind/check (default: 8115)")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: status
    status_p = subparsers.add_parser("status", help="Check local service and API configuration status")
    status_p.add_argument("--host", default="127.0.0.1", help="Host interface")
    status_p.add_argument("--port", type=int, default=8115, help="Port (default: 8115)")
    status_p.add_argument("--json", action="store_true", help="Output status report as JSON")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Run the HTTP & REST API daemon")
    serve_parser.add_argument("--port", type=int, default=8115, help="HTTP listening port (default: 8115)")
    serve_parser.add_argument("--host", type=str, default=_default_bind_host(), help="Host interface")

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

    args = parser.parse_args(argv)

    if getattr(args, "status", False) or (getattr(args, "json", False) and not args.command):
        return cmd_status(host=args.host, port=args.port, as_json=True if getattr(args, "json", False) else False)

    cmd = args.command or "serve"

    if cmd == "status":
        return cmd_status(host=args.host, port=args.port, as_json=args.json)
    elif cmd == "serve":
        run_server(port=args.port, host=args.host)
        return 0
    elif cmd == "mcp":
        run_mcp_server()
        return 0
    elif cmd == "blueprints":
        items = list_blueprints(args.category)
        print(json.dumps(items, indent=2))
        return 0
    elif cmd == "providers":
        providers = list_providers(args.country)
        print(json.dumps(providers, indent=2))
        return 0
    elif cmd == "margins":
        res = calculate_multi_channel_margins(
            blueprint_id=args.blueprint,
            retail_price=args.price,
            shipping_charged=args.shipping,
            has_printify_premium=args.premium
        )
        print(json.dumps(res, indent=2))
        return 0
    elif cmd == "audit":
        audit = audit_artwork_dimensions(
            blueprint_id=args.blueprint,
            width_px=args.width,
            height_px=args.height,
            file_name=args.name
        )
        print(json.dumps(audit, indent=2))
        return 0
    elif cmd == "info":
        return cmd_status(host=args.host, port=args.port, as_json=False)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
