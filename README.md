<div align="center">
  <img src="assets/hero-banner.svg" alt="Printify Connector — Sovereign Architecture Banner" width="100%" />
</div>

<br />

# 📦 Printify Connector for Antigravity & Sovereign AI Agents

> ⚡ **Live Web Application**: [https://printify.nullai.tech](https://printify.nullai.tech)  
> 🏛️ **Zoth Studio Workspace**: [https://zoth.nullai.tech/tools/printify-connector](https://zoth.nullai.tech/tools/printify-connector)  
> 🛡️ **Sovereign Status**: 100% Free & Open-Access · Zero Paywalls · 100% Zero-Egress Compatible

[![Audit](https://img.shields.io/badge/guardrail-100%25%20passed-emerald)](https://printify.nullai.tech)
[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/python-3.10%2B-gold)](https://python.org)
[![Zero Pip](https://img.shields.io/badge/dependencies-0%20external-purple)](https://nullai.tech)

Autonomous **Printify Open API v1 Connector**, 20% Premium Margin Engine, Artwork DPI Auditor, and Antigravity MCP Suite for **Google Antigravity** AI agents and **Zoth Studio v2 / ZothOS Linux 3.3**. Exposes 6 Model Context Protocol (MCP) tools for catalog search, print provider routing, real-time fee & profit modeling across sales channels, artwork validation, and product payload generation.

---

## 📖 What It Does

- **Printify Open API v1 Integration**: Search blueprints (Bella+Canvas 3001, Gildan 18000, Ceramic Mugs, Posters) and compare verified print providers (Monster Digital, SwiftPOD, District Photo, MyLocker).
- **20% Printify Premium Margin Simulator**: Real-time margin calculator comparing Etsy, Shopify, and Direct Web3 sales channels, factoring in Printify Premium discounts and computing annual break-even order volume.
- **Artwork DPI & Resolution Auditor**: Validates image dimensions and pixel density against exact physical print areas (e.g. 4000x4800 px @ 300 DPI) with zero-upload in-browser verification.
- **Automated JSON Product Payloads**: Formats complete multi-variant product creation payloads for automated submission to Printify's API.
- **100% Free & Open-Access**: Zero paywalls, zero license locks, zero telemetry leaks.

---

## ⚙️ How It Works

1. **Standalone Enclave (`127.0.0.1:8115`)**: Powered by `server.py` serving a dark-glassmorphic cockpit with live `/health`, `/api/stats`, `/api/blueprints`, `/api/providers`, and `/api/margins` endpoints.
2. **Zoth Studio v2 God-Mode Route**: Deeply integrated into the 71-Tool Sovereign Matrix at `/tools/printify-connector`.
3. **ZothOS CLI (`printify-connector`)**: Native binary installed in `/usr/local/bin` and `~/.local/bin` for automated command-line audits and CI/CD pipelines.
4. **Antigravity MCP Bridge**: Standard JSON-RPC 2.0 stdio server providing 6 autonomous tools for AI agents.

---

## ⚡ 6 Model Context Protocol (MCP) Tools

When registered in `~/.gemini/config/mcp_config.json`, Antigravity gains immediate access to:

1. `printify_search_blueprints`: Search catalog blueprints by query or category.
2. `printify_get_print_providers`: List verified print providers for a blueprint.
3. `printify_calculate_margins`: Compute exact COGS, fees, net margins, and break-even pricing.
4. `printify_audit_artwork`: Validate artwork pixel dimensions and DPI against print areas.
5. `printify_create_product_payload`: Generate validated Printify product creation JSON payloads.
6. `printify_get_shop_info`: Retrieve store connection status and channel metadata.

---

## 💻 ZothOS CLI & Server Commands

```bash
# Check status and health
printify-connector --status
printify-connector status

# Output telemetry in JSON format
printify-connector --json

# List available catalog blueprints
printify-connector blueprints --category Apparel

# Calculate profit margins with 20% Premium discount
printify-connector margins --blueprint bella_canvas_3001 --price 28.00 --premium

# Audit artwork resolution and DPI
printify-connector audit --blueprint bella_canvas_3001 --width 4500 --height 5100

# Launch standalone workstation server on port 8115
python3 server.py --port 8115
```

---

## ☕ Support Neal Frazier Tech & NullAI

Printify Connector is 100% free, open-source, and sovereign software. If this tool brings you value, consider supporting our ongoing development:

- **☕ Buy Us a Coffee (Stripe)**: [buy.stripe.com/3cIfZg27PdKo2D64Ocfw40X](https://buy.stripe.com/3cIfZg27PdKo2D64Ocfw40X)
- **◎ Solana Tip Address**: `GG2eQbVh8ut1BK6j1A2tz7pSySdLpD38BgyEhGcxdXoK`

---

<div align="center">
  <sub>Engineered by <b>Neal Frazier Tech</b> (<a href="https://github.com/1nc0gn30">@1nc0gn30</a>) &bull; <a href="https://nullai.tech">NullAI Platform</a> &bull; <a href="https://zoth.nullai.tech">Zoth Studio v2</a></sub>
</div>
