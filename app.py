import streamlit as st
import pandas as pd
import plotly.express as px
from ui_components import (
    init_ui,
    render_status_badge,
    render_kpi_card,
    render_risk_meter,
)

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="LEAKLOCK | Enterprise DLP & AI Guardrail",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Initialize Theme & CSS
init_ui()

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & THEME TOGGLE
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:10px; padding: 8px 0 20px 0; border-bottom: 1px solid #1e293b;">
            <span style="font-size: 1.8rem;">🛡️</span>
            <div>
                <div style="font-weight:800; font-size:1.15rem; letter-spacing:0.04em;">LEAKLOCK</div>
                <div style="font-size:0.72rem; color:#94a3b8;">Enterprise DLP Engine v2.4</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    page = st.radio(
        "NAVIGATION",
        ["🔍 Content Scanner", "⚙️ Policy Manager", "📊 Audit Dashboard", "ℹ️ About LEAKLOCK"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Light / Dark Theme Toggle
    current_theme = st.session_state.theme
    toggle_label = "🌙 Dark Mode (SOC)" if current_theme == "dark" else "☀️ Light Mode (Exec)"
    if st.toggle(toggle_label, value=(current_theme == "dark")):
        if st.session_state.theme != "dark":
            st.session_state.theme = "dark"
            st.rerun()
    else:
        if st.session_state.theme != "light":
            st.session_state.theme = "light"
            st.rerun()

    st.markdown(
        """
        <div style="margin-top:24px; padding:12px; background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.3); border-radius:8px; font-size:0.78rem;">
            🟢 <b>Engine Status:</b> Operational<br>
            <span style="color:#94a3b8;">All guardrails active</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# PAGE 1: CONTENT SCANNER
# ---------------------------------------------------------
if page == "🔍 Content Scanner":
    st.markdown("## 🔍 Real-Time DLP & Prompt Scanner")
    st.caption("Inspect outbound prompts, payloads, and documents for secrets, PII, and policy violations.")

    col_in, col_out = st.columns([1.05, 1], gap="large")

    with col_in:
        st.markdown('<div class="ll-kpi-title">INPUT PAYLOAD</div>', unsafe_allow_html=True)
        payload = st.text_area(
            "Input Payload",
            height=240,
            placeholder="Paste text, code snippet, or LLM prompt here (e.g., AWS key AKIAIOSFODNN7EXAMPLE or email john@corp.com)...",
            label_visibility="collapsed",
        )
        scan_btn = st.button("🛡️ Run Security Scan", type="primary", use_container_width=True)

    with col_out:
        st.markdown('<div class="ll-kpi-title">ENFORCEMENT VERDICT & SANITIZED OUTPUT</div>', unsafe_allow_html=True)

        if scan_btn and payload.strip():
            # =========================================================
            # TODO: Replace mock dict below with your existing backend:
            # result = your_scanner_engine.scan(payload)
            # =========================================================
            if "AKIA" in payload or "private_key" in payload.lower():
                result = {"action": "BLOCK", "risk_score": 92, "sanitized": "[PAYLOAD BLOCKED BY ENTERPRISE POLICY]", "findings": ["AWS_ACCESS_KEY", "HIGH_ENTROPY_SECRET"]}
            elif "@" in payload:
                result = {"action": "REDACT", "risk_score": 55, "sanitized": payload.replace("john@corp.com", "[REDACTED_EMAIL]"), "findings": ["EMAIL_ADDRESS"]}
            else:
                result = {"action": "ALLOW", "risk_score": 8, "sanitized": payload, "findings": []}

            # Render Verdict Header
            st.markdown(
                f"""
                <div class="ll-card" style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="ll-kpi-title">POLICY DECISION</div>
                        <div style="font-size:0.9rem;">{len(result["findings"])} sensitive entities detected</div>
                    </div>
                    {render_status_badge(result["action"])}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Render Risk Score Bar
            render_risk_meter(result["risk_score"])

            # Sanitized Output Box
            st.code(result["sanitized"], language="text")
        else:
            st.markdown(
                """
                <div class="ll-card" style="height:240px; display:flex; align-items:center; justify-content:center; text-align:center; color:var(--text-secondary);">
                    <div>
                        <div style="font-size:2rem; margin-bottom:8px;">🛡️</div>
                        Submit a payload on the left to view real-time enforcement decision, risk score, and redacted output.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------
# PAGE 2: POLICY MANAGER
# ---------------------------------------------------------
elif page == "⚙️ Policy Manager":
    st.markdown("## ⚙️ Security Policy Manager")
    st.caption("Configure active detection rules and enforcement actions without modifying core engine code.")

    policies = [
        {"id": "POL-01", "name": "Credentials & API Keys", "desc": "Detects AWS, GitHub, Slack, and private SSH keys.", "default": "BLOCK"},
        {"id": "POL-02", "name": "Personally Identifiable Information (PII)", "desc": "Detects emails, phone numbers, Aadhaar/SSN, and credit cards.", "default": "REDACT"},
        {"id": "POL-03", "name": "Internal Source Code & IP", "desc": "Detects proprietary headers and internal repository URLs.", "default": "BLOCK"},
        {"id": "POL-04", "name": "Public Metadata & General Queries", "desc": "Standard non-sensitive traffic.", "default": "ALLOW"},
    ]

    for pol in policies:
        c1, c2, c3 = st.columns([3, 1.5, 1])
        with c1:
            st.markdown(
                f"""
                <div style="padding: 6px 0;">
                    <span style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:var(--accent);">{pol['id']}</span>
                    <div style="font-weight:600; font-size:1rem;">{pol['name']}</div>
                    <div style="font-size:0.82rem; color:var(--text-secondary);">{pol['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            action = st.selectbox(
                f"Action for {pol['id']}",
                ["ALLOW", "REDACT", "BLOCK"],
                index=["ALLOW", "REDACT", "BLOCK"].index(pol["default"]),
                key=f"sel_{pol['id']}",
                label_visibility="collapsed",
            )
        with c3:
            st.markdown(f"<div style='padding-top:6px; text-align:right;'>{render_status_badge(action)}</div>", unsafe_allow_html=True)
        st.divider()

# ---------------------------------------------------------
# PAGE 3: AUDIT DASHBOARD
# ---------------------------------------------------------
elif page == "📊 Audit Dashboard":
    st.markdown("## 📊 Security Telemetry & Audit Logs")
    st.caption("Real-time visibility into scanned payloads, redactions, and blocked data exfiltration attempts.")

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Total Scans (24h)", "1,482", "↑ 12% vs yesterday", "#3b82f6")
    with k2:
        render_kpi_card("Allowed Clean", "1,120", "75.5% of traffic", "#22c55e")
    with k3:
        render_kpi_card("Auto-Redacted", "298", "20.1% sanitized", "#f59e0b")
    with k4:
        render_kpi_card("Critical Blocked", "64", "4.3% hard stops", "#ef4444")

    # Charts Row
    ch1, ch2 = st.columns(2)
    plotly_template = "plotly_dark" if st.session_state.theme == "dark" else "plotly_white"

    with ch1:
        df_actions = pd.DataFrame({
            "Action": ["ALLOW", "REDACT", "BLOCK"],
            "Count": [1120, 298, 64]
        })
        fig_donut = px.pie(
            df_actions, names="Action", values="Count", hole=0.62,
            color="Action",
            color_discrete_map={"ALLOW": "#22c55e", "REDACT": "#f59e0b", "BLOCK": "#ef4444"},
            title="Enforcement Action Breakdown",
            template=plotly_template
        )
        fig_donut.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_donut, use_container_width=True)

    with ch2:
        df_threats = pd.DataFrame({
            "Category": ["API Keys", "Email / PII", "Financial / Card", "Internal IP", "JWT Tokens"],
            "Detections": [142, 118, 54, 31, 17]
        })
        fig_bar = px.bar(
            df_threats, x="Detections", y="Category", orientation="h",
            title="Top Detected Entity Categories",
            template=plotly_template,
            color_discrete_sequence=["#3b82f6"]
        )
        fig_bar.update_layout(margin=dict(t=40, b=20, l=20, r=20), height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Styled Audit Log Table
    st.markdown("### Recent Audit Events")
    audit_df = pd.DataFrame([
        {"Timestamp": "2026-10-17 18:10:04", "Rule": "POL-01 (AWS Key)", "Risk": 95, "Decision": "🛑 BLOCK", "User": "dev-api-04"},
        {"Timestamp": "2026-10-17 18:08:49", "Rule": "POL-02 (Email PII)", "Risk": 52, "Decision": "⚡ REDACT", "User": "support-agent"},
        {"Timestamp": "2026-10-17 18:05:12", "Rule": "None", "Risk": 4, "Decision": "✔ ALLOW", "User": "analyst-01"},
    ])
    st.dataframe(
        audit_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Risk": st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100, format="%d/100"),
        },
    )

# ---------------------------------------------------------
# PAGE 4: ABOUT LEAKLOCK
# ---------------------------------------------------------
elif page == "ℹ️ About LEAKLOCK":
    st.markdown("## ℹ️ About LEAKLOCK")
    st.markdown(
        """
        <div class="ll-card">
            <h4>Enterprise Data Loss Prevention (DLP) & LLM Guardrail</h4>
            <p style="color:var(--text-secondary); line-height:1.6;">
                LEAKLOCK inspects outbound prompts, API payloads, and documents in real time to prevent accidental leakage 
                of secrets, cryptographic keys, and regulated PII before data leaves your trust boundary.
            </p>
            <hr style="border-color:var(--border-color); margin: 16px 0;">
            <div style="display:flex; gap:12px; flex-wrap:wrap;">
                <span class="ll-badge ll-badge-allow">✔ ZERO-TRUST INSPECTION</span>
                <span class="ll-badge ll-badge-redact">⚡ DETERMINISTIC REDACTION</span>
                <span class="ll-badge ll-badge-block">🛑 SUB-10MS LATENCY</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )