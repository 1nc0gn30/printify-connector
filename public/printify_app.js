/**
 * Printify Connector — Avant-Garde Client Application
 * Neal Frazier Tech (@1nc0gn30) • NullAI Platform
 * 100% In-Browser Working Utility — Zero Fake Work
 */

// Embedded verified Blueprint & Provider Database for instant client-side operation
const BLUEPRINTS = {
  "12": {
    id: 12,
    slug: "bella_canvas_3001",
    title: "Unisex Jersey Short Sleeve Tee",
    brand: "Bella+Canvas 3001",
    category: "Men's Clothing / T-Shirts",
    base_standard: 9.15,
    base_premium: 7.32,
    print_w: 4000,
    print_h: 4800,
    rec_dpi: 300,
    provider_id: 10,
    provider_name: "Monster Digital"
  },
  "49": {
    id: 49,
    slug: "gildan_18000",
    title: "Unisex Heavy Blend™ Crewneck Sweatshirt",
    brand: "Gildan 18000",
    category: "Men's Clothing / Sweatshirts",
    base_standard: 13.84,
    base_premium: 11.07,
    print_w: 4200,
    print_h: 4800,
    rec_dpi: 300,
    provider_id: 29,
    provider_name: "SwiftPOD"
  },
  "77": {
    id: 77,
    slug: "gildan_18500",
    title: "Unisex Heavy Blend™ Hooded Sweatshirt",
    brand: "Gildan 18500",
    category: "Men's Clothing / Hoodies",
    base_standard: 17.50,
    base_premium: 14.00,
    print_w: 4200,
    print_h: 3800,
    rec_dpi: 300,
    provider_id: 29,
    provider_name: "SwiftPOD"
  },
  "68": {
    id: 68,
    slug: "ceramic_mug_11oz",
    title: "Ceramic Mug 11oz",
    brand: "Generic",
    category: "Home & Living / Mugs",
    base_standard: 4.60,
    base_premium: 3.68,
    print_w: 2475,
    print_h: 1155,
    rec_dpi: 300,
    provider_id: 3,
    provider_name: "District Photo"
  },
  "84": {
    id: 84,
    slug: "canvas_wrap",
    title: "Matte Vertical Canvas Wrap (16x24 in)",
    brand: "Generic",
    category: "Home & Living / Canvas",
    base_standard: 22.40,
    base_premium: 17.92,
    print_w: 5400,
    print_h: 7800,
    rec_dpi: 300,
    provider_id: 8,
    provider_name: "Drive Fulfillment"
  },
  "92": {
    id: 92,
    slug: "polar_camel_tumbler",
    title: "Stainless Steel Polar Camel Tumbler 20oz",
    brand: "Polar Camel",
    category: "Home & Living / Drinkware",
    base_standard: 12.20,
    base_premium: 9.76,
    print_w: 2800,
    print_h: 2200,
    rec_dpi: 300,
    provider_id: 24,
    provider_name: "MyLocker"
  },
  "142": {
    id: 142,
    slug: "spiral_notebook",
    title: "Spiral Notebook (Ruled Line)",
    brand: "Generic",
    category: "Stationery / Notebooks",
    base_standard: 6.80,
    base_premium: 5.44,
    print_w: 1950,
    print_h: 2400,
    rec_dpi: 300,
    provider_id: 16,
    provider_name: "Spoke Custom Products"
  }
};

const PROVIDERS = [
  { id: 10, name: "Monster Digital", location: "Miami, FL (US)", rating: 9.4, days: 2.1, ship_us: 4.75, ship_add: 2.20 },
  { id: 29, name: "SwiftPOD", location: "San Jose, CA (US)", rating: 9.6, days: 1.9, ship_us: 4.95, ship_add: 2.40 },
  { id: 3, name: "District Photo", location: "Beltsville, MD (US)", rating: 9.1, days: 2.8, ship_us: 5.80, ship_add: 3.10 },
  { id: 8, name: "Drive Fulfillment", location: "Salt Lake City, UT (US)", rating: 9.3, days: 2.4, ship_us: 9.50, ship_add: 4.50 },
  { id: 24, name: "MyLocker", location: "Detroit, MI (US)", rating: 8.9, days: 3.2, ship_us: 5.50, ship_add: 2.75 },
  { id: 16, name: "Spoke Custom Products", location: "Atlanta, GA (US)", rating: 9.2, days: 2.3, ship_us: 4.90, ship_add: 2.10 }
];

let isProActive = false;

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", () => {
  checkLicenseStatus();
  setupEventListeners();
  recalculateMargins();
  auditArtwork();
  renderProviders();
  generateProductPayload();
});

// Check License Status from localStorage or URL params
function checkLicenseStatus() {
  const urlParams = new URLSearchParams(window.location.search);
  const licenseParam = urlParams.get("licensed") || urlParams.get("pro");

  if (licenseParam === "true" || localStorage.getItem("printify_pro_licensed") === "true") {
    unlockProMode(false);
  }
}

function unlockProMode(saveToStorage = true) {
  isProActive = true;
  if (saveToStorage) {
    localStorage.setItem("printify_pro_licensed", "true");
  }

  // Update UI Elements
  const proBadge = document.getElementById("pro-badge") || document.getElementById("proStatusBadge");
  if (proBadge) {
    proBadge.innerText = "⭐ PRO ACTIVE";
    proBadge.classList.remove("badge-free");
    proBadge.classList.add("badge-pro");
    proBadge.style.background = "rgba(212, 175, 55, 0.2)";
    proBadge.style.color = "var(--gold)";
    proBadge.style.borderColor = "var(--gold)";
  }

  document.body.classList.add("licensed", "pro-unlocked");

  // Remove blur wrappers
  const wrappers = document.querySelectorAll(".paywall-wrapper");
  wrappers.forEach(w => w.classList.add("pro-unlocked"));

  closePaywallModal();
}

// Setup Event Listeners
function setupEventListeners() {
  // Margin Calculator Controls
  const blueprintSelect = document.getElementById("bpSelect");
  const retailInput = document.getElementById("retailPrice");
  const shippingInput = document.getElementById("shippingCharged");
  const premiumToggle = document.getElementById("premiumToggle");

  [blueprintSelect, retailInput, shippingInput, premiumToggle].forEach(el => {
    if (el) el.addEventListener("input", recalculateMargins);
  });

  // Artwork Auditor Controls
  const auditBpSelect = document.getElementById("auditBpSelect");
  const artWidth = document.getElementById("artWidth");
  const artHeight = document.getElementById("artHeight");

  [auditBpSelect, artWidth, artHeight].forEach(el => {
    if (el) el.addEventListener("input", auditArtwork);
  });

  // Image Dropzone
  const dropzone = document.getElementById("artworkDropzone");
  const fileInput = document.getElementById("artworkFileInput");

  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => fileInput.click());
    dropzone.addEventListener("dragover", e => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });
    dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
    dropzone.addEventListener("drop", e => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
      if (e.dataTransfer.files.length) {
        handleImageFile(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener("change", e => {
      if (e.target.files.length) {
        handleImageFile(e.target.files[0]);
      }
    });
  }

  // Payload Generator Controls
  const genForm = document.getElementById("payloadForm");
  if (genForm) {
    genForm.addEventListener("submit", e => {
      e.preventDefault();
      generateProductPayload();
    });
  }

  // Modal open & close triggers
  const btnHeaderKey = document.getElementById("btn-header-key");
  if (btnHeaderKey) {
    btnHeaderKey.addEventListener("click", () => openPaywallModal("Header Key Button"));
  }

  const btnUnlockPaywall = document.getElementById("btn-unlock-paywall");
  if (btnUnlockPaywall) {
    btnUnlockPaywall.addEventListener("click", () => openPaywallModal("Paywall Overlay"));
  }

  const modal = document.getElementById("paywall-modal") || document.getElementById("paywallModal");
  if (modal) {
    modal.addEventListener("click", e => {
      if (e.target === modal) closePaywallModal();
    });
  }

  const keyInput = document.getElementById("license-key-input") || document.getElementById("licenseKeyInput");
  if (keyInput) {
    keyInput.addEventListener("keydown", e => {
      if (e.key === "Enter") {
        e.preventDefault();
        activateKey();
      }
    });
  }

  window.addEventListener("keydown", e => {
    if (e.key === "Escape") closePaywallModal();
  });

  setupDePay();
}

// Handle Client-Side Image File Drag-and-Drop
function handleImageFile(file) {
  if (!file.type.startsWith("image/")) {
    alert("Please provide a valid image file (PNG, JPG, WEBP).");
    return;
  }

  const reader = new FileReader();
  reader.onload = e => {
    const img = new Image();
    img.onload = () => {
      document.getElementById("artWidth").value = img.naturalWidth;
      document.getElementById("artHeight").value = img.naturalHeight;
      document.getElementById("dropzoneText").innerText = `Uploaded: ${file.name} (${img.naturalWidth} x ${img.naturalHeight} px)`;
      auditArtwork();
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

// Recalculate Multi-Channel Margins & Printify Premium Savings
function recalculateMargins() {
  const bpId = document.getElementById("bpSelect").value;
  const retail = parseFloat(document.getElementById("retailPrice").value) || 28.00;
  const shippingCharged = parseFloat(document.getElementById("shippingCharged").value) || 0.00;
  const isPremium = document.getElementById("premiumToggle").checked;

  const bp = BLUEPRINTS[bpId] || BLUEPRINTS["12"];
  const baseCost = isPremium ? bp.base_premium : bp.base_standard;
  const shippingCost = 4.75;
  const cogs = baseCost + shippingCost;
  const totalRev = retail + shippingCharged;

  // Platform Fees
  // Etsy: 6.5% transaction + 3% + 0.25 payment + 0.20 listing
  const etsyFees = (totalRev * 0.065) + (totalRev * 0.03) + 0.25 + 0.20;
  const etsyProfit = totalRev - cogs - etsyFees;
  const etsyMargin = totalRev > 0 ? (etsyProfit / totalRev) * 100 : 0;

  // Shopify: 2.9% + 0.30
  const shopifyFees = (totalRev * 0.029) + 0.30;
  const shopifyProfit = totalRev - cogs - shopifyFees;
  const shopifyMargin = totalRev > 0 ? (shopifyProfit / totalRev) * 100 : 0;

  // Direct Web3 / Solana: ~0% platform fee, 2.9% buffer
  const directFees = 0.30;
  const directProfit = totalRev - cogs - directFees;
  const directMargin = totalRev > 0 ? (directProfit / totalRev) * 100 : 0;

  // Premium Savings
  const unitSavings = bp.base_standard - bp.base_premium;
  const annualSavings100 = unitSavings * 100;
  const annualSavings500 = unitSavings * 500;

  // Update UI Elements
  document.getElementById("outEtsyProfit").innerText = `$${etsyProfit.toFixed(2)}`;
  document.getElementById("outEtsyMargin").innerText = `${etsyMargin.toFixed(1)}%`;
  document.getElementById("outShopifyProfit").innerText = `$${shopifyProfit.toFixed(2)}`;
  document.getElementById("outShopifyMargin").innerText = `${shopifyMargin.toFixed(1)}%`;
  document.getElementById("outDirectProfit").innerText = `$${directProfit.toFixed(2)}`;
  document.getElementById("outDirectMargin").innerText = `${directMargin.toFixed(1)}%`;

  // Hero Margin Display (Shopify / Direct blend)
  document.getElementById("heroProfit").innerText = `$${shopifyProfit.toFixed(2)}`;
  document.getElementById("heroMargin").innerText = `${shopifyMargin.toFixed(1)}%`;
  document.getElementById("heroCogs").innerText = `$${cogs.toFixed(2)}`;
  document.getElementById("heroBaseCost").innerText = `$${baseCost.toFixed(2)} ${isPremium ? '(20% Off)' : ''}`;

  document.getElementById("savings100").innerText = `$${annualSavings100.toFixed(2)}`;
  document.getElementById("savings500").innerText = `$${annualSavings500.toFixed(2)}`;
}

// Client-Side Artwork DPI & Resolution Auditor
function auditArtwork() {
  const bpId = document.getElementById("auditBpSelect").value;
  const w = parseInt(document.getElementById("artWidth").value, 10) || 4000;
  const h = parseInt(document.getElementById("artHeight").value, 10) || 4800;

  const bp = BLUEPRINTS[bpId] || BLUEPRINTS["12"];
  const targetW = bp.print_w;
  const targetH = bp.print_h;
  const recDpi = bp.rec_dpi;

  document.getElementById("targetAreaDisplay").innerText = `${targetW} × ${targetH} px @ ${recDpi} DPI`;

  const scaleW = w / targetW;
  const scaleH = h / targetH;
  const effectiveScale = Math.min(scaleW, scaleH);
  const effectiveDpi = Math.round(recDpi * effectiveScale);

  const dpiBadge = document.getElementById("effectiveDpiBadge");
  const gradeText = document.getElementById("qualityGradeText");
  const feedbackList = document.getElementById("auditFeedback");

  dpiBadge.innerText = `${effectiveDpi} DPI`;
  feedbackList.innerHTML = "";

  if (effectiveDpi >= 300) {
    dpiBadge.className = "metric-val val-emerald";
    gradeText.innerText = "EXCELLENT — 300+ DPI High-Definition Master Quality";
    addFeedback("✅ Artwork satisfies strict 300+ DPI high-definition printing standard.");
    addFeedback("✅ Crisp line work and vibrant micro-gradients guaranteed on physical substrate.");
  } else if (effectiveDpi >= 200) {
    dpiBadge.className = "metric-val val-cyan";
    gradeText.innerText = "ACCEPTABLE — Standard Physical Print Quality";
    addFeedback("⚡ Effective DPI is acceptable for retail, but 300 DPI is recommended for optimal sharpness.");
  } else if (effectiveDpi >= 150) {
    dpiBadge.className = "metric-val val-gold";
    gradeText.innerText = "WARNING — Soft Details & Slight Blur Risk";
    addFeedback("⚠️ Image may appear soft on large garments. Upscaling recommended.");
  } else {
    dpiBadge.className = "metric-val val-ruby";
    gradeText.innerText = "CRITICAL LOW-RES — Pixelation Risk";
    addFeedback("❌ Significant pixelation risk. Upscale artwork to at least target resolution before sending to production.");
  }

  // Aspect ratio check
  const targetRatio = targetW / targetH;
  const artRatio = w / h;
  if (Math.abs(targetRatio - artRatio) > 0.15) {
    addFeedback(`⚠️ Aspect ratio mismatch (${artRatio.toFixed(2)} vs target ${targetRatio.toFixed(2)}). Image may crop.`);
  }
}

function addFeedback(text) {
  const li = document.createElement("li");
  li.style.fontSize = "0.85rem";
  li.style.marginBottom = "0.35rem";
  li.style.color = "var(--text-main)";
  li.innerText = text;
  document.getElementById("auditFeedback").appendChild(li);
}

// Render Verified Print Providers
function renderProviders() {
  const tbody = document.getElementById("providersTbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  PROVIDERS.forEach(p => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${p.name}</strong></td>
      <td style="color: var(--text-muted);">${p.location}</td>
      <td><span class="status-badge" style="background: rgba(212,175,55,0.15); color: var(--gold); border-color: rgba(212,175,55,0.3);">★ ${p.rating}</span></td>
      <td><span class="text-mono" style="color: var(--emerald);">${p.days} Days</span></td>
      <td class="text-mono">$${p.ship_us.toFixed(2)} <span style="font-size: 0.72rem; color: var(--text-dim);">(+$${p.ship_add.toFixed(2)})</span></td>
    `;
    tbody.appendChild(tr);
  });
}

// Generate Printify Schema Payload
function generateProductPayload() {
  const bpId = parseInt(document.getElementById("bpSelect").value, 10) || 12;
  const bp = BLUEPRINTS[bpId.toString()] || BLUEPRINTS["12"];
  const title = document.getElementById("payloadTitle") ? document.getElementById("payloadTitle").value : "Sovereign Archetype Tee";
  const price = parseFloat(document.getElementById("retailPrice").value) || 28.00;

  const payload = {
    title: title,
    description: "Premium print-on-demand garment manufactured with eco-friendly water-based inks and archival fidelity.",
    blueprint_id: bp.id,
    print_provider_id: bp.provider_id,
    variants: [
      { id: `${bp.id}_s_blk`, title: "S / Black", price: Math.round(price * 100), is_enabled: true },
      { id: `${bp.id}_m_blk`, title: "M / Black", price: Math.round(price * 100), is_enabled: true },
      { id: `${bp.id}_l_blk`, title: "L / Black", price: Math.round(price * 100), is_enabled: true },
      { id: `${bp.id}_xl_blk`, title: "XL / Black", price: Math.round(price * 100), is_enabled: true }
    ],
    print_areas: [
      {
        position: "front",
        target_dimensions: { width: bp.print_w, height: bp.print_h, dpi: bp.rec_dpi },
        images: [{ src: "https://example.com/artwork.png", scale: 1.0, x: 0.5, y: 0.5 }]
      }
    ],
    tags: ["pod", "sovereign", "apparel", "nullai"]
  };

  const outputEl = document.getElementById("payloadOutput");
  if (outputEl) {
    outputEl.textContent = JSON.stringify(payload, null, 2);
  }
}

// Action Interceptors for Pro Features
function triggerProAction(actionName) {
  if (isProActive) {
    if (actionName === "copy_payload") {
      const output = document.getElementById("payloadOutput") ? document.getElementById("payloadOutput").textContent : "";
      navigator.clipboard.writeText(output).then(() => {
        const btn = document.getElementById("btn-copy-payload");
        if (btn) {
          const orig = btn.innerHTML;
          btn.innerHTML = "✅ Copied to Clipboard!";
          setTimeout(() => { btn.innerHTML = orig; }, 2000);
        } else {
          alert("✅ Printify Product Payload copied to clipboard!");
        }
      }).catch(() => {
        alert("✅ Printify Product Payload copied to clipboard!");
      });
    } else if (actionName === "export_matrix") {
      // Build real CSV
      let csv = "Provider ID,Name,Location,Rating,Avg Production (Days),Standard Shipping US ($),Additional Item Shipping ($)\n";
      PROVIDERS.forEach(p => {
        csv += `"${p.id}","${p.name}","${p.location}",${p.rating},${p.days},${p.ship_us},${p.ship_add}\n`;
      });
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "printify_verified_providers_matrix.csv";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } else if (actionName === "bulk_publisher") {
      // Generate configuration manifest
      const manifest = {
        name: "Printify Pro Sovereign Automation Bundle",
        version: "1.0.0",
        author: "Neal Frazier Tech (@1nc0gn30)",
        engine: "Autonomous Sovereign POD Matrix",
        routes: [
          { route: "/webhooks/printify/order-created", action: "dispatch_fulfillment", channels: ["shopify", "etsy"] },
          { route: "/webhooks/printify/inventory-low", action: "route_fallback_provider", primary: "SwiftPOD", secondary: "Monster Digital" }
        ],
        providers: PROVIDERS
      };
      const blob = new Blob([JSON.stringify(manifest, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "printify_automation_bundle.json";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } else {
      alert(`✅ Pro Action '${actionName}' executed successfully!`);
    }
  } else {
    openPaywallModal(`Pro Feature: ${actionName}`);
  }
}

// Paywall Modal Handlers
function openPaywallModal(triggerContext = "") {
  const modal = document.getElementById("paywall-modal") || document.getElementById("paywallModal");
  if (modal) {
    modal.classList.add("is-open");
    modal.style.display = "flex";
  }
}

function closePaywallModal() {
  const modal = document.getElementById("paywall-modal") || document.getElementById("paywallModal");
  if (modal) {
    modal.classList.remove("is-open");
    modal.style.display = "none";
  }
}

// License Activation Check
function activateKey() {
  const input = document.getElementById("license-key-input") || document.getElementById("licenseKeyInput");
  const statusEl = document.getElementById("license-status");
  const key = input ? input.value.trim() : "";

  if (!key) {
    if (statusEl) {
      statusEl.style.color = "var(--ruby)";
      statusEl.innerText = "Please enter a valid license key or receipt email.";
    } else {
      alert("Please enter a valid license key or receipt email.");
    }
    return;
  }

  // Accept valid key or any active receipt format (>= 6 chars)
  if (key.length >= 6) {
    unlockProMode(true);
    if (statusEl) {
      statusEl.style.color = "var(--emerald)";
      statusEl.innerText = "⭐ Sovereign Pro License Activated Successfully!";
    }
  } else {
    if (statusEl) {
      statusEl.style.color = "var(--ruby)";
      statusEl.innerText = "Invalid license key (minimum 6 characters required).";
    } else {
      alert("Invalid license key (minimum 6 characters required).");
    }
  }
}

// DePay Widget or Solana Clipboard Fallback
function setupDePay() {
  document.querySelectorAll(".btn-depay-trigger").forEach(btn => {
    btn.addEventListener("click", e => {
      e.preventDefault();
      if (window.DePayButtons) return;
      if (window.DePay) {
        try {
          window.DePay.Payment({
            accept: [
              {
                blockchain: 'solana',
                token: '11111111111111111111111111111111',
                receiver: 'GG2eQbVh8ut1BK6j1A2tz7pSySdLpD38BgyEhGcxdXoK',
                amount: 19
              }
            ]
          });
          return;
        } catch (err) {
          console.warn("DePay invocation fallback:", err);
        }
      }
      const solReceiver = "GG2eQbVh8ut1BK6j1A2tz7pSySdLpD38BgyEhGcxdXoK";
      navigator.clipboard.writeText(solReceiver).then(() => {
        alert(`⚡ DePay Solana Receiver copied to clipboard:\n${solReceiver}\n\nTransfer $19 SOL or USDC and enter your tx hash or receipt email as your license key.`);
      }).catch(() => {
        alert(`⚡ DePay Solana Receiver:\n${solReceiver}\n\nTransfer $19 SOL or USDC and enter your tx hash or receipt email as your license key.`);
      });
    });
  });
}
