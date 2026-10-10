"""Printify API v1 Client.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional
from .catalog import PRINTIFY_BLUEPRINTS, PRINT_PROVIDERS, get_blueprint_by_id, get_provider_by_id


class PrintifyClient:
    """Printify REST API v1 Client with Live & Offline Deterministic Modes."""

    BASE_URL = "https://api.printify.com/v1"

    def __init__(self, token: Optional[str] = None, shop_id: Optional[str] = None) -> None:
        self.token = token or os.environ.get("PRINTIFY_API_TOKEN", "")
        self.shop_id = shop_id or os.environ.get("PRINTIFY_SHOP_ID", "mock_shop_1nc0gn30")
        self.is_live = bool(self.token)

    def _request(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make an authenticated HTTP request or fallback to mock mode."""
        if not self.is_live:
            return self._mock_response(endpoint, method, data)

        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "PrintifyConnector-Antigravity/1.0.0"
        }

        body = json.dumps(data).encode("utf-8") if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Printify API Error {e.code}: {err_body}")
        except Exception as e:
            raise RuntimeError(f"Printify Connection Error: {e}")

    def get_shop_info(self) -> Dict[str, Any]:
        """Retrieve shop metadata and connected sales channels."""
        if not self.is_live:
            return {
                "id": self.shop_id,
                "title": "Neal Frazier Tech Sovereign POD Hub",
                "sales_channel": "shopify,etsy",
                "mode": "OFFLINE_DETERMINISTIC",
                "api_connected": False,
                "plan": "Printify Premium (Autonomous 20% Discount)",
                "currency": "USD"
            }
        return self._request("/shops.json")

    def get_blueprints(self) -> List[Dict[str, Any]]:
        """List catalog blueprints."""
        if not self.is_live:
            return PRINTIFY_BLUEPRINTS
        return self._request("/catalog/blueprints.json")

    def get_print_providers(self, blueprint_id: int) -> List[Dict[str, Any]]:
        """List verified print providers for a blueprint."""
        if not self.is_live:
            return PRINT_PROVIDERS
        return self._request(f"/catalog/blueprints/{blueprint_id}/print_providers.json")

    def create_product_payload(
        self,
        blueprint_id: int,
        title: str,
        description: str,
        image_url: str,
        provider_id: Optional[int] = None,
        retail_price: float = 28.00,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Build schema-valid Printify product creation payload."""
        bp = get_blueprint_by_id(blueprint_id)
        if not bp:
            raise ValueError(f"Unknown blueprint ID {blueprint_id}")

        p_id = provider_id or bp.get("default_provider_id", 10)
        provider = get_provider_by_id(p_id)

        # Standard size variants (S, M, L, XL, 2XL)
        variant_ids = [45012, 45013, 45014, 45015, 45016]
        price_cents = int(retail_price * 100)

        variants = []
        for vid in variant_ids:
            variants.append({
                "id": vid,
                "price": price_cents,
                "is_enabled": True
            })

        print_areas = bp.get("print_areas", [])
        placeholders = []
        for area in print_areas:
            placeholders.append({
                "position": area["position"],
                "images": [
                    {
                        "id": "img_autogen_1nc0gn30",
                        "name": "artwork.png",
                        "type": "image/png",
                        "src": image_url,
                        "x": 0.5,
                        "y": 0.5,
                        "scale": 1.0,
                        "angle": 0
                    }
                ]
            })

        product_payload = {
            "title": title,
            "description": description,
            "blueprint_id": blueprint_id,
            "print_provider_id": p_id,
            "variants": variants,
            "print_areas": placeholders,
            "tags": tags or bp.get("tags", ["sovereign", "pod"])
        }

        return product_payload

    def _mock_response(self, endpoint: str, method: str, data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Internal mock handler for testing without API keys."""
        if "blueprints" in endpoint:
            return {"data": PRINTIFY_BLUEPRINTS}
        if "shops" in endpoint:
            return {
                "id": "mock_shop_1nc0gn30",
                "title": "Neal Frazier Tech Sovereign Store",
                "sales_channel": "shopify"
            }
        return {"status": "ok", "mode": "MOCK_MODE", "endpoint": endpoint}
