"""Modular UI/UX renderers for the Soil-Sense Bento-grid dashboard."""

import streamlit as st
from typing import Dict, List, Any
from src.config import OPTIMAL_AGRONOMIC_RANGES, FEATURE_BOUNDS


def render_header():
    """Render top brand header with status badge and SHA-256 verification pill."""
    st.markdown(
        """
        <div class="brand-header">
            <div>
                <div class="brand-title">
                    <span>🌱</span> Soil-Sense
                    <span class="brand-badge">ML CLASSIFIER v1.0</span>
                </div>
                <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 0.3rem;">
                    Precision Agronomic Soil Fertility Diagnostics & Actionable Soil Health Intelligence
                </div>
            </div>
            <div class="status-pill">
                <div class="pulse-dot"></div>
                <span>ML Pipeline Verified (SHA-256)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_fertility_badge(fertility_class: str, confidence: float):
    """Render high-impact fertility status card."""
    cls_lower = fertility_class.lower()
    class_icons = {
        "high": "🟢 OPTIMAL / HIGH FERTILITY",
        "medium": "🟡 MODERATE / BALANCED FERTILITY",
        "low": "🔴 LOW / DEGRADED FERTILITY",
    }
    banner_class = f"result-banner result-banner-{cls_lower}"
    title_text = class_icons.get(cls_lower, fertility_class.upper())

    st.markdown(
        f"""
        <div class="{banner_class}">
            <div class="result-label">Diagnostic Status</div>
            <div class="result-value">{fertility_class.upper()}</div>
            <div>
                <span class="confidence-pill">Confidence: {confidence * 100:.1f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_probability_bars(probabilities: Dict[str, float]):
    """Render modern stacked probability bars."""
    st.markdown('<div class="card-title"><span>📊</span> Class Probability Distribution</div>', unsafe_allow_html=True)
    for cls in ["High", "Medium", "Low"]:
        prob = probabilities.get(cls, 0.0)
        pct = round(prob * 100, 1)
        cls_lower = cls.lower()
        st.markdown(
            f"""
            <div class="prob-row">
                <div class="prob-header">
                    <span>{cls} Fertility</span>
                    <span style="font-family: 'JetBrains Mono', monospace;">{pct}%</span>
                </div>
                <div class="prob-track">
                    <div class="prob-fill fill-{cls_lower}" style="width: {pct}%;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_parameter_matrix(input_values: Dict[str, float]):
    """Render parameter health matrix showing each parameter vs its optimal ICAR/FAO band."""
    st.markdown('<div class="card-title"><span>🎯</span> Agronomic Parameter Health Matrix</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    features_order = ["N", "P", "K", "pH", "EC", "Moisture", "Temperature", "Humidity"]

    for idx, feat in enumerate(features_order):
        col = cols[idx % 4]
        val = input_values[feat]
        unit = FEATURE_BOUNDS[feat]["unit"]
        opt_min, opt_max = OPTIMAL_AGRONOMIC_RANGES[feat]

        if val < opt_min:
            status = "Low"
            status_color = "#ef4444"
            bg_color = "rgba(239, 68, 68, 0.15)"
        elif val > opt_max:
            status = "High"
            status_color = "#f59e0b"
            bg_color = "rgba(245, 158, 11, 0.15)"
        else:
            status = "Optimal"
            status_color = "#10b981"
            bg_color = "rgba(16, 185, 129, 0.15)"

        with col:
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 10px; padding: 0.75rem; margin-bottom: 0.6rem;">
                    <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">{feat} ({unit})</div>
                    <div style="font-size: 1.25rem; font-weight: 700; color: #ffffff; margin: 0.2rem 0;">{val:.1f}</div>
                    <div style="display: inline-block; font-size: 0.7rem; font-weight: 600; padding: 0.1rem 0.45rem; border-radius: 4px; color: {status_color}; background: {bg_color};">
                        {status} • Ref: {opt_min}-{opt_max}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_agronomic_advisory(diagnostics: List[Dict[str, str]]):
    """Render actionable agronomic treatment recommendations."""
    st.markdown('<div class="card-title"><span>🌾</span> Actionable Agronomic Guidance</div>', unsafe_allow_html=True)

    for item in diagnostics:
        sev = item.get("severity", "medium")
        card_class = f"advice-card advice-{sev}"
        tag_class = f"advice-status status-tag-{sev}"

        st.markdown(
            f"""
            <div class="{card_class}">
                <div class="advice-param">
                    <span>{item['parameter']}</span>
                    <span class="{tag_class}">{item['status']}</span>
                </div>
                <div style="color: #cbd5e1; margin-bottom: 0.3rem;">{item['observation']}</div>
                <div style="color: #94a3b8; font-size: 0.82rem;">
                    <strong style="color: #38bdf8;">Prescription:</strong> {item['recommendation']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_disclaimer():
    """Render academic and ethical disclaimer."""
    st.markdown(
        """
        <div class="disclaimer-box">
            <strong>⚠️ Academic & Decision Support Notice:</strong>
            Soil-Sense is an academic machine learning research system developed for rapid decision support and pattern screening.
            Predictions are generated via statistical inference and should not replace certified wet-laboratory soil testing,
            local extension services, or agronomist-validated chemical prescriptions before commercial field application.
        </div>
        """,
        unsafe_allow_html=True,
    )
