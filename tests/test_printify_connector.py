"""Unit tests for Printify Connector.

100% Python Standard Library — Zero External Dependencies.
Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from printify_connector.catalog import (
    BLUEPRINTS,
    PRINT_PROVIDERS,
    get_blueprint,
    get_blueprint_by_id,
    get_provider,
    get_provider_by_id,
    list_blueprints,
    list_providers,
    search_blueprints,
)
from printify_connector.margin_engine import (
    calculate_margins,
    calculate_multi_channel_margins,
    calculate_shipping_rates,
)
from printify_connector.artwork_auditor import (
    audit_artwork,
    audit_artwork_dimensions,
)
from printify_connector.client import PrintifyClient
from printify_connector.mcp_server import handle_tool_call, TOOLS


class TestPrintifyCatalog(unittest.TestCase):
    def test_blueprints_exist(self):
        self.assertGreaterEqual(len(BLUEPRINTS), 7)

    def test_get_blueprint_by_id_and_slug(self):
        bp_by_id = get_blueprint_by_id(12)
        self.assertIsNotNone(bp_by_id)
        self.assertEqual(bp_by_id["brand"], "Bella+Canvas 3001")

        bp_by_slug = get_blueprint("bella_canvas_3001")
        self.assertIsNotNone(bp_by_slug)
        self.assertEqual(bp_by_slug["id"], 12)

        bp_by_string_id = get_blueprint("49")
        self.assertIsNotNone(bp_by_string_id)
        self.assertEqual(bp_by_string_id["brand"], "Gildan 18000")

    def test_search_blueprints(self):
        mugs = search_blueprints(query="mug")
        self.assertTrue(any(b["id"] == 68 for b in mugs))

        hoodies = search_blueprints(category="Hoodies")
        self.assertTrue(any(b["id"] == 77 for b in hoodies))

    def test_providers(self):
        self.assertGreaterEqual(len(PRINT_PROVIDERS), 5)
        prov = get_provider("monster_digital")
        self.assertIsNotNone(prov)
        self.assertEqual(prov["id"], 10)


class TestMarginEngine(unittest.TestCase):
    def test_calculate_margins_standard(self):
        res = calculate_margins(
            blueprint_id="bella_canvas_3001",
            retail_price=28.00,
            is_premium=False,
            channel="etsy"
        )
        self.assertEqual(res["base_production_cost"], 9.15)
        self.assertEqual(res["shipping_cost"], 4.75)
        self.assertGreater(res["net_profit"], 10.0)
        self.assertGreater(res["profit_margin_pct"], 35.0)

    def test_calculate_margins_premium(self):
        res_std = calculate_margins(blueprint_id=12, retail_price=28.00, is_premium=False)
        res_prem = calculate_margins(blueprint_id=12, retail_price=28.00, is_premium=True)
        self.assertLess(res_prem["base_production_cost"], res_std["base_production_cost"])
        self.assertGreater(res_prem["net_profit"], res_std["net_profit"])
        self.assertAlmostEqual(res_prem["premium_savings"], 1.83, places=2)

    def test_multi_channel_margins(self):
        res = calculate_multi_channel_margins(
            blueprint_id="bella_canvas_3001",
            retail_price=28.00,
            has_printify_premium=False
        )
        self.assertIn("etsy", res["channels"])
        self.assertIn("shopify", res["channels"])
        self.assertIn("direct", res["channels"])
        self.assertGreater(res["channels"]["shopify"]["premium"]["margin_pct"], 50.0)

    def test_shipping_rates(self):
        rates = calculate_shipping_rates(blueprint_id=12, destination="US")
        self.assertIn("standard_delivery", rates)
        self.assertIn("express_delivery", rates)
        self.assertGreater(rates["express_delivery"]["first_item_cost"], rates["standard_delivery"]["first_item_cost"])


class TestArtworkAuditor(unittest.TestCase):
    def test_audit_high_res_artwork(self):
        res = audit_artwork_dimensions(
            blueprint_id="bella_canvas_3001",
            width_px=4500,
            height_px=5100
        )
        self.assertEqual(res["print_quality_grade"], "EXCELLENT")
        self.assertTrue(res["is_print_ready"])
        self.assertGreaterEqual(res["effective_dpi"], 300)

    def test_audit_low_res_artwork(self):
        res = audit_artwork_dimensions(
            blueprint_id="bella_canvas_3001",
            width_px=800,
            height_px=800
        )
        self.assertEqual(res["print_quality_grade"], "CRITICAL_LOW_RES")
        self.assertFalse(res["is_print_ready"])
        self.assertLess(res["effective_dpi"], 150)


class TestClientAndMCP(unittest.TestCase):
    def test_client_offline_mock(self):
        client = PrintifyClient()
        shop_info = client.get_shop_info()
        self.assertEqual(shop_info["mode"], "OFFLINE_DETERMINISTIC")
        payload = client.create_product_payload(
            blueprint_id=12,
            title="Test Tee",
            description="A test shirt",
            image_url="https://example.com/art.png"
        )
        self.assertEqual(payload["blueprint_id"], 12)
        self.assertGreaterEqual(len(payload["variants"]), 5)

    def test_mcp_tools(self):
        self.assertGreaterEqual(len(TOOLS), 6)
        res = handle_tool_call("printify_search_blueprints", {"query": "canvas"})
        self.assertIn("blueprints", res)


if __name__ == "__main__":
    unittest.main()
