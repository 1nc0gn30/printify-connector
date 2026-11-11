"""HTTP API (ephemeral port) and offline-mode honesty tests. No external network calls."""
import json
import os
import sys
import threading
import unittest
import urllib.request
from http.server import HTTPServer
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from printify_connector import __version__
from printify_connector.cli import main as cli_main
from printify_connector.client import PrintifyClient
from printify_connector.server import PrintifyRequestHandler


class TestOfflineClient(unittest.TestCase):
    def test_request_without_token_raises_clear_error(self):
        with mock.patch.dict(os.environ, {"PRINTIFY_API_TOKEN": ""}):
            client = PrintifyClient()
            self.assertFalse(client.is_live)
            with self.assertRaises(RuntimeError) as ctx:
                client._request("/shops.json")
            self.assertIn("PRINTIFY_API_TOKEN is not set", str(ctx.exception))

    def test_shop_info_never_fakes_a_shop(self):
        with mock.patch.dict(os.environ, {"PRINTIFY_API_TOKEN": "", "PRINTIFY_SHOP_ID": ""}):
            info = PrintifyClient().get_shop_info()
        self.assertFalse(info["api_connected"])
        self.assertNotIn("title", info)
        self.assertIsNone(info["shop_id"])

    def test_payload_variants_priced_in_cents(self):
        payload = PrintifyClient(token="").create_product_payload(
            blueprint_id=12, title="T", description="D", image_url="https://example.com/a.png", retail_price=31.5
        )
        self.assertTrue(all(v["price"] == 3150 for v in payload["variants"]))
        self.assertEqual(payload["blueprint_id"], 12)


class TestHttpApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", 0), PrintifyRequestHandler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def _get(self, path):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=5) as r:
            return r.status, json.loads(r.read())

    def _post(self, path, body, origin=None):
        headers = {"Content-Type": "application/json"}
        if origin:
            headers["Origin"] = origin
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}{path}", data=json.dumps(body).encode(), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_health_reports_real_port_and_version(self):
        status, data = self._get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["port"], self.port)
        self.assertEqual(data["version"], __version__)
        self.assertIn("apiConfigured", data)

    def test_blueprints_endpoint(self):
        status, data = self._get("/api/blueprints")
        self.assertEqual(status, 200)
        self.assertEqual(data["count"], len(data["blueprints"]))
        self.assertGreater(data["count"], 0)

    def test_margins_endpoint_math(self):
        status, data = self._post("/api/margins", {"blueprintId": "bella_canvas_3001", "retailPrice": 30, "shippingCharged": 5})
        self.assertEqual(status, 200)
        self.assertTrue(data["success"])
        self.assertIn("calculation", data)

    def test_cross_origin_post_blocked(self):
        status, data = self._post("/api/margins", {}, origin="https://evil.example")
        self.assertEqual(status, 403)

    def test_unknown_blueprint_404(self):
        try:
            self._get("/api/blueprints/does_not_exist")
            self.fail("expected 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)


class TestCli(unittest.TestCase):
    def test_status_json_offline(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with mock.patch.dict(os.environ, {"PRINTIFY_API_TOKEN": ""}), redirect_stdout(buf):
            rc = cli_main(["--port", "1", "--json"])
        self.assertEqual(rc, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(data["status"], "standby")
        self.assertFalse(data["api_token_configured"])
        self.assertEqual(data["version"], __version__)



class TestMcpProtocol(unittest.TestCase):
    def test_initialize_and_notifications(self):
        from printify_connector.mcp_server import handle_request
        init = handle_request({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        self.assertEqual(init["result"]["serverInfo"]["name"], "printify-connector")
        self.assertIsNone(handle_request({"jsonrpc": "2.0", "method": "notifications/initialized"}))

    def test_unknown_tool_is_error_result(self):
        from printify_connector.mcp_server import handle_request
        resp = handle_request({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "nope"}})
        self.assertTrue(resp["result"]["isError"])



class TestCatalogFilters(unittest.TestCase):
    def test_category_aliases_match_help_text(self):
        from printify_connector.catalog import list_blueprints
        apparel = list_blueprints("Apparel")
        self.assertTrue(apparel)
        self.assertTrue(all("clothing" in b["category"].lower() for b in apparel))
        self.assertTrue(list_blueprints("Drinkware"))
        self.assertTrue(list_blueprints("Home"))

    def test_country_code_filter(self):
        from printify_connector.catalog import PRINT_PROVIDERS, list_providers
        self.assertEqual(len(list_providers("US")), len([p for p in PRINT_PROVIDERS if "United States" in p["location"]]))
        self.assertEqual(list_providers("DE"), [])


if __name__ == "__main__":
    unittest.main()
