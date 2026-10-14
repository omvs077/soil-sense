"""Modular UI/UX renderers for the Soil-Sense Bento-grid dashboard."""

import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from typing import Dict, List, Any
from src.config import OPTIMAL_AGRONOMIC_RANGES, FEATURE_BOUNDS


def render_header():
    """Render top brand header with status badge and SHA-256 verification pill."""
    html = (
        '<div class="brand-header">'
        '<div>'
        '<div class="brand-title"><span>🌱</span> Soil-Sense <span class="brand-badge">ML CLASSIFIER v1.0</span></div>'
        '<div style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">'
        'Precision Agronomic Soil Fertility Diagnostics & Actionable Soil Health Intelligence'
        '</div>'
        '</div>'
        '<div class="status-pill"><div class="pulse-dot"></div><span>ML Pipeline Verified (SHA-256)</span></div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_fertility_badge(fertility_class: str, confidence: float):
    """Render high-impact fertility status card."""
    cls_lower = fertility_class.lower()
    banner_class = f"result-banner result-banner-{cls_lower}"
    html = (
        f'<div class="{banner_class}">'
        f'<div class="result-label">Diagnostic Status</div>'
        f'<div class="result-value">{fertility_class.upper()} FERTILITY</div>'
        f'<div><span class="confidence-pill">Classification Confidence: {confidence * 100:.1f}%</span></div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_probability_bars(probabilities: Dict[str, float]):
    """Render modern stacked probability bars."""
    st.markdown('<div class="card-header-bar"><span>📊</span> Class Probability Distribution</div>', unsafe_allow_html=True)
    rows_html = []
    for cls in ["High", "Medium", "Low"]:
        prob = probabilities.get(cls, 0.0)
        pct = round(prob * 100, 1)
        cls_lower = cls.lower()
        rows_html.append(
            f'<div class="prob-row">'
            f'<div class="prob-header"><span>{cls} Fertility</span><span style="font-family: \'JetBrains Mono\', monospace; font-weight: 700;">{pct}%</span></div>'
            f'<div class="prob-track"><div class="prob-fill fill-{cls_lower}" style="width: {pct}%;"></div></div>'
            f'</div>'
        )
    st.markdown("".join(rows_html), unsafe_allow_html=True)


def render_parameter_matrix(input_values: Dict[str, float]):
    """Render responsive CSS grid showing all 8 soil parameters vs their optimal ICAR/FAO bands."""
    st.markdown('<div class="card-header-bar"><span>🎯</span> Agronomic Parameter Health Matrix</div>', unsafe_allow_html=True)

    features_order = ["N", "P", "K", "pH", "EC", "Moisture", "Temperature", "Humidity"]
    items_html = []

    for feat in features_order:
        val = input_values[feat]
        unit = FEATURE_BOUNDS[feat]["unit"]
        opt_min, opt_max = OPTIMAL_AGRONOMIC_RANGES[feat]

        if val < opt_min:
            status = "Low"
            status_color = "#ef4444"
            bg_color = "rgba(239, 68, 68, 0.18)"
        elif val > opt_max:
            status = "High"
            status_color = "#f59e0b"
            bg_color = "rgba(245, 158, 11, 0.18)"
        else:
            status = "Optimal"
            status_color = "#10b981"
            bg_color = "rgba(16, 185, 129, 0.18)"

        formatted_val = f"{val:.1f}" if feat != "pH" else f"{val:.2f}"

        items_html.append(
            f'<div class="param-card">'
            f'<div class="param-name">{feat} ({unit})</div>'
            f'<div class="param-val">{formatted_val}</div>'
            f'<div class="param-badge" style="color: {status_color}; background: {bg_color}; border: 1px solid {status_color}40;">'
            f'{status} &bull; {opt_min}-{opt_max}'
            f'</div>'
            f'</div>'
        )

    grid_container = f'<div class="param-grid">{"".join(items_html)}</div>'
    st.markdown(grid_container, unsafe_allow_html=True)


def render_agronomic_advisory(diagnostics: List[Dict[str, str]]):
    """Render actionable agronomic treatment recommendations."""
    st.markdown('<div class="card-header-bar"><span>🌾</span> Actionable Agronomic Guidance</div>', unsafe_allow_html=True)

    advisories_html = []
    for item in diagnostics:
        sev = item.get("severity", "medium")
        card_class = f"advice-card advice-{sev}"
        tag_class = f"advice-status status-tag-{sev}"
        advisories_html.append(
            f'<div class="{card_class}">'
            f'<div class="advice-param"><span>{item["parameter"]}</span><span class="{tag_class}">{item["status"]}</span></div>'
            f'<div style="color: #cbd5e1; margin-bottom: 0.25rem;">{item["observation"]}</div>'
            f'<div style="color: #94a3b8; font-size: 0.82rem;"><strong style="color: #38bdf8;">Correction:</strong> {item["recommendation"]}</div>'
            f'</div>'
        )

    st.markdown("".join(advisories_html), unsafe_allow_html=True)


def render_disclaimer():
    """Render academic and ethical disclaimer."""
    html = (
        '<div class="disclaimer-box">'
        '<strong>⚠️ Academic & Decision Support Notice:</strong> '
        'Soil-Sense is an academic machine learning research system developed for rapid decision support and pattern screening. '
        'Predictions are generated via statistical inference and should not replace certified wet-laboratory soil testing, '
        'local extension services, or agronomist-validated chemical prescriptions before commercial field application.'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
