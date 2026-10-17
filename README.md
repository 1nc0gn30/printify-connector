# Printify Connector 📦

> ⚡ **Live Web Application**: [https://printify-connector.netlify.app](https://printify-connector.netlify.app)  
> 💳 **Unlock Pro Lifetime License ($19 One-Time, $0/mo)**: **[Instant Pro Unlock via Stripe](https://buy.stripe.com/4gMfZg9AheOsdhKbcAfw40L)** *(Use promo code `FOUNDER25` for 25% off)*  
> 🏆 **All-Access Sovereign Pro Bundle (All 44 Tools — $49 Lifetime)**: **[Get All 44 Studios via Stripe](https://buy.stripe.com/eVq14m5k16hW4Le0xWfw40M)**

> Autonomous Printify Open API v1 Connector, 20% Premium Margin Engine, Artwork DPI Auditor, and Antigravity MCP Suite.  
> **100% Python Standard Library — Zero External Runtime Dependencies.**  
> Engineered by **Neal Frazier Tech** ([@1nc0gn30](https://github.com/1nc0gn30)) • [NullAI Platform](https://nullai.tech)

---

## 🌟 Sovereign Capabilities

- **Zero-Dependency Architecture**: Built 100% on Python 3.10+ standard library (`http.server`, `urllib.request`, `json`, `argparse`). Zero pip dependencies, zero telemetry leaks.
- **20% Printify Premium Margin Engine**: Real-time margin calculator comparing Etsy, Shopify, and Direct Web3 sales channels, factoring in Printify Premium discounts and computing annual break-even order volume.
- **Artwork DPI & Resolution Auditor**: Validates image dimensions and pixel density against exact physical print areas (e.g. 4000x4800 px @ 300 DPI for Bella+Canvas 3001) with instant browser-based file analysis.
- **Print Provider Matrix**: Lead times, ratings, and standard/additional item shipping costs for verified providers (Monster Digital, SwiftPOD, District Photo, Drive Fulfillment, MyLocker, Spoke).
- **Antigravity MCP Suite**: 6 native JSON-RPC 2.0 tools for Claude, Antigravity, and autonomous AI agents.
- **Dual Checkout Cash Registers**: Direct Stripe payment link ($19 lifetime founding member pricing) + DePay Solana Widget.

---

## 🚀 Quickstart

### 1. Run the HTTP & REST Daemon
```bash
./bin/printify-connector serve --port 8115
```
Visit `http://localhost:8115` in your browser.

### 2. Antigravity MCP Server (Stdio)
```bash
./bin/printify-connector mcp
```

### 3. CLI Commands
```bash
# System status
./bin/printify-connector info

# List blueprints
./bin/printify-connector blueprints

# Calculate profit margins
./bin/printify-connector margins --blueprint bella_canvas_3001 --price 28.00 --premium

# Audit artwork resolution
./bin/printify-connector audit --blueprint bella_canvas_3001 --width 4500 --height 5100
```

---

## 🛠️ MCP Tools

1. `printify_search_blueprints`: Search catalog blueprints by query or category.
2. `printify_get_print_providers`: List verified print providers for a blueprint.
3. `printify_calculate_margins`: Compute exact COGS, fees, net margins, and break-even pricing.
4. `printify_audit_artwork`: Validate artwork pixel dimensions and DPI against print areas.
5. `printify_create_product_payload`: Generate validated Printify product creation JSON payloads.
6. `printify_get_shop_info`: Retrieve store connection status and channel metadata.

---

## 📜 License & Sovereign Directives
Engineered by **Neal Frazier Tech** ([@1nc0gn30](https://github.com/1nc0gn30)) • NullAI Platform.
All rights reserved.

## Network exposure

The server binds to `127.0.0.1` by default. To reach it from other devices,
opt in explicitly with `--host 0.0.0.0` (or set `ZOTH_BIND_HOST=0.0.0.0`; an IP
in `HOST` is also honoured, a plain hostname is ignored) and only on a trusted
network.

## Safety

- The browser API only accepts cross-origin requests from `localhost` / `127.0.0.1` pages. POSTs from any other website get `403`, and CORS echoes only local origins (never `*`), so a site you visit can't drive or read this local server. CLI and agent clients (no `Origin` header) are unaffected.
- `PRINTIFY_API_TOKEN` is only used in the `Authorization` header. The connector makes read-only catalog/shop calls and builds product payloads locally; it never creates products or orders.
