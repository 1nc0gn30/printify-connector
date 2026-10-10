"""Printify Artwork Resolution & DPI Auditor.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from .catalog import get_blueprint


def audit_artwork(
    blueprint_id: Any,
    image_width_px: int,
    image_height_px: int,
    print_position: str = "front",
    declared_dpi: Optional[int] = None
) -> Dict[str, Any]:
    """Audit artwork resolution against blueprint print area requirements."""
    blueprint = get_blueprint(blueprint_id)
    if not blueprint:
        raise ValueError(f"Unknown blueprint ID or slug '{blueprint_id}'")

    areas = blueprint.get("print_areas", [])
    selected_area = next((a for a in areas if a["position"] == print_position), areas[0] if areas else None)

    if not selected_area:
        raise ValueError(f"No print area defined for blueprint {blueprint_id}")

    target_w = selected_area["width"]
    target_h = selected_area["height"]
    rec_dpi = selected_area.get("recommended_dpi", 300)

    # Compute effective DPI ratio
    width_ratio = image_width_px / target_w
    height_ratio = image_height_px / target_h
    effective_scale = min(width_ratio, height_ratio)
    effective_dpi = round(rec_dpi * effective_scale)

    status = "EXCELLENT"
    feedback = []

    if effective_dpi >= 300:
        status = "EXCELLENT"
        feedback.append("Artwork satisfies strict 300+ DPI high-definition printing standard.")
    elif effective_dpi >= 200:
        status = "ACCEPTABLE"
        feedback.append(f"Effective DPI is {effective_dpi}. Acceptable print quality, but 300 DPI is recommended for optimal sharpness.")
    elif effective_dpi >= 150:
        status = "WARNING"
        feedback.append(f"Effective DPI is {effective_dpi}. Image may appear soft or slightly pixelated on large physical garments.")
    else:
        status = "CRITICAL_LOW_RES"
        feedback.append(f"Effective DPI is only {effective_dpi}. Significant pixelation risk. Upscaling or re-export required.")

    # Aspect ratio check
    target_aspect = target_w / target_h
    art_aspect = image_width_px / image_height_px
    aspect_diff = abs(target_aspect - art_aspect)

    if aspect_diff > 0.15:
        feedback.append(f"Aspect ratio mismatch (Artwork: {art_aspect:.2f} vs Print Area: {target_aspect:.2f}). Cropping or letterboxing may occur.")

    return {
        "blueprint_id": blueprint["id"],
        "blueprint_title": blueprint["title"],
        "print_position": print_position,
        "target_dimensions": {"width_px": target_w, "height_px": target_h, "recommended_dpi": rec_dpi},
        "artwork_dimensions": {"width_px": image_width_px, "height_px": image_height_px, "declared_dpi": declared_dpi},
        "effective_dpi": effective_dpi,
        "print_quality_grade": status,
        "is_print_ready": effective_dpi >= 200,
        "scaling_factor": round(effective_scale, 3),
        "feedback": feedback
    }


def audit_artwork_dimensions(
    blueprint_id: Any,
    width_px: int,
    height_px: int,
    file_name: str = "design.png",
    file_size_bytes: Optional[int] = None,
    print_position: str = "front"
) -> Dict[str, Any]:
    """Convenience auditor for CLI and REST endpoints."""
    res = audit_artwork(
        blueprint_id=blueprint_id,
        image_width_px=width_px,
        image_height_px=height_px,
        print_position=print_position
    )
    res["file_name"] = file_name
    if file_size_bytes:
        res["file_size_mb"] = round(file_size_bytes / (1024 * 1024), 2)
    return res
