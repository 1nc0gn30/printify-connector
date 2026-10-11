"""
HTTP & REST API Server for Printify Connector
Port 8115 — Zero external runtime dependencies (100% Python Standard Library)
Provides REST endpoints and serves dark-glassmorphic frontend.
"""

import json
import os
import sys
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from .artwork_auditor import audit_artwork_dimensions
from .catalog import (
    BLUEPRINTS,
    PRINT_PROVIDERS,
    get_blueprint,
    get_provider,
    list_blueprints,
    list_providers,
)
from .margin_engine import calculate_multi_channel_margins, calculate_shipping_rates


class PrintifyRequestHandler(SimpleHTTPRequestHandler):
    """Handles static files from public/ and JSON API endpoints."""

    def __init__(self, *args, **kwargs):
        # Set directory to the package public folder
        public_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "public"
        )
        super().__init__(*args, directory=public_dir, **kwargs)

    def _send_json(self, data, status=HTTPStatus.OK):
        """Serialize and send JSON response with standard CORS headers."""
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests for static assets and API queries."""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query = parse_qs(parsed.query)

        # Health & Status
        if path in ("/health", "/api/health"):
            return self._send_json({
                "status": "healthy",
                "service": "printify-connector",
                "version": "1.0.0",
                "port": 8115,
                "engine": "Python Standard Library (Zero External Dependencies)",
                "creator": "Neal Frazier Tech (@1nc0gn30)"
            })

        if path == "/api/stats":
            return self._send_json({
                "service": "printify-connector",
                "status": "online",
                "port": 8115,
                "blueprintsCount": len(BLUEPRINTS),
                "providersCount": len(PRINT_PROVIDERS),
                "premiumDiscountPct": 20.0,
                "supportedChannels": ["Etsy", "Shopify", "Direct Web3"],
                "creator": "Neal Frazier Tech (@1nc0gn30)"
            })

        # Blueprints Catalog
        if path == "/api/blueprints":
            category = query.get("category", [None])[0]
            items = list_blueprints(category)
            return self._send_json({
                "success": True,
                "count": len(items),
                "blueprints": items
            })

        # Single Blueprint Detail
        if path.startswith("/api/blueprints/"):
            bp_id = path.split("/")[-1]
            bp = get_blueprint(bp_id)
            if bp:
                return self._send_json({"success": True, "blueprint": bp})
            return self._send_json({"error": f"Blueprint '{bp_id}' not found"}, status=HTTPStatus.NOT_FOUND)

        # Print Providers Catalog
        if path == "/api/providers":
            country = query.get("country", [None])[0]
            providers = list_providers(country)
            return self._send_json({
                "success": True,
                "count": len(providers),
                "providers": providers
            })

        # Single Provider Detail
        if path.startswith("/api/providers/"):
            provider_id = path.split("/")[-1]
            prov = get_provider(provider_id)
            if prov:
                return self._send_json({"success": True, "provider": prov})
            return self._send_json({"error": f"Provider '{provider_id}' not found"}, status=HTTPStatus.NOT_FOUND)

        # Fallback to serving static files from public/
        return super().do_GET()

    def do_POST(self):
        """Handle POST calculation and auditing requests."""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        # Read JSON body safely
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 1024 * 1024:  # 1 MB limit
                return self._send_json({"error": "Payload exceeds 1MB limit"}, status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
            body_bytes = self.rfile.read(content_length)
            body = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except Exception as e:
            return self._send_json({"error": f"Invalid JSON body: {str(e)}"}, status=HTTPStatus.BAD_REQUEST)

        # Margin Calculation
        if path == "/api/margins":
            bp_id = body.get("blueprintId", "bella_canvas_3001")
            retail_price = float(body.get("retailPrice", 28.00))
            shipping_charged = float(body.get("shippingCharged", 4.99))
            is_premium = bool(body.get("hasPrintifyPremium", False))
            target_margin = float(body.get("targetMarginPct", 40.0))

            res = calculate_multi_channel_margins(
                blueprint_id=bp_id,
                retail_price=retail_price,
                shipping_charged=shipping_charged,
                has_printify_premium=is_premium,
                target_margin_pct=target_margin
            )
            return self._send_json({"success": True, "calculation": res})

        # Artwork DPI & Dimension Auditor
        if path == "/api/audit":
            bp_id = body.get("blueprintId", "bella_canvas_3001")
            width_px = int(body.get("widthPx", 4500))
            height_px = int(body.get("heightPx", 5100))
            file_name = body.get("fileName", "design.png")
            file_size_bytes = int(body.get("fileSizeBytes", 4 * 1024 * 1024))

            audit = audit_artwork_dimensions(
                blueprint_id=bp_id,
                width_px=width_px,
                height_px=height_px,
                file_name=file_name,
                file_size_bytes=file_size_bytes
            )
            return self._send_json({"success": True, "audit": audit})

        # Shipping Rates
        if path == "/api/shipping":
            bp_id = body.get("blueprintId", "bella_canvas_3001")
            destination = body.get("destination", "US")
            is_express = bool(body.get("isExpress", False))

            rates = calculate_shipping_rates(bp_id, destination, is_express)
            return self._send_json({"success": True, "shipping": rates})

        # Generate Printify Order / Product Creation Payload
        if path == "/api/create-payload":
            bp_id = body.get("blueprintId", "bella_canvas_3001")
            provider_id = body.get("printProviderId", "monster_digital")
            title = body.get("title", "Sovereign Archetype Graphic Tee")
            description = body.get("description", "Premium print-on-demand garment manufactured with eco-friendly water-based inks.")
            tags = body.get("tags", ["graphic tee", "minimalist", "vintage"])
            image_url = body.get("imageUrl", "https://example.com/artwork.png")

            bp = get_blueprint(bp_id)
            if not bp:
                return self._send_json({"error": f"Unknown blueprint: {bp_id}"}, status=HTTPStatus.NOT_FOUND)

            payload = {
                "title": title,
                "description": description,
                "blueprint_id": bp.get("id"),
                "print_provider_id": provider_id,
                "variants": [
                    {
                        "id": f"{bp.get('id')}_s_black",
                        "price": 2800,  # in cents
                        "is_enabled": True
                    },
                    {
                        "id": f"{bp.get('id')}_m_black",
                        "price": 2800,
                        "is_enabled": True
                    },
                    {
                        "id": f"{bp.get('id')}_l_black",
                        "price": 2800,
                        "is_enabled": True
                    },
                    {
                        "id": f"{bp.get('id')}_xl_black",
                        "price": 2800,
                        "is_enabled": True
                    }
                ],
                "print_areas": [
                    {
                        "variant_ids": [f"{bp.get('id')}_s_black", f"{bp.get('id')}_m_black", f"{bp.get('id')}_l_black", f"{bp.get('id')}_xl_black"],
                        "placeholders": [
                            {
                                "position": "front",
                                "images": [
                                    {
                                        "id": "upload_placeholder_id",
                                        "x": 0.5,
                                        "y": 0.5,
                                        "scale": 1.0,
                                        "angle": 0,
                                        "src": image_url
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "tags": tags
            }
            return self._send_json({"success": True, "printify_payload": payload})

        return self._send_json({"error": f"Path not found: {path}"}, status=HTTPStatus.NOT_FOUND)


def run_server(port=8115, host="127.0.0.1"):
    """Start the Printify Connector HTTP daemon."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, PrintifyRequestHandler)
    print(f"📦 Printify Connector HTTP Server active at http://{host}:{port}")
    print(f"   • Endpoints: /api/stats, /api/blueprints, /api/providers, /api/margins, /api/audit")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down Printify Connector server gracefully...")
        httpd.server_close()
