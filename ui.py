"""
ui.py - Euron Recruitment Agent UI Components
From transcript: 'UI wali file mein saari display cheezein hain.
CSS aur JavaScript bhi yahan use kiya hai. Color change karna bhi yahan se hota hai.'

Functions:
- setup_page()
- inject_css(accent_color)
- display_header()
- setup_sidebar()  → returns api_key, accent_color
- create_score_pie_chart(score, label)
- display_analysis(result)
- display_weakness_detail(text)
"""

import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64
import io


# ─────────────────────────────────────────────────────────────
# 1. SETUP PAGE
# ─────────────────────────────────────────────────────────────
def setup_page():
    """
    From transcript: 'Setup page function mein page title, icon, layout set karte hain.
    Emoji icon aur JavaScript bhi yahan use kiya.'
    """
    st.set_page_config(
        page_title="Euron Recruitment Agent",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )


# ─────────────────────────────────────────────────────────────
# 2. INJECT CSS  (custom CSS + JS color support)
# ─────────────────────────────────────────────────────────────
def inject_css(accent_color: str = "#e53935"):
    """
    From transcript: 'CSS aur JavaScript ka use karke color change kar sakte ho.
    Ye custom CSS function hai. Color picker se jo bhi color select karo
    woh yahan apply hota hai.'
    """
    st.markdown(
        f"""
        <style>
        /* ── Global ── */
        [data-testid="stAppViewContainer"] {{
            background-color: #0e0e1a;
            color: #e0e0e0;
        }}
        [data-testid="stSidebar"] {{
            background-color: #12121f;
            border-right: 1px solid #2a2a3e;
        }}

        /* ── Header Banner ── */
        .euron-header {{
            background: linear-gradient(135deg, {accent_color} 0%, #7b1fa2 100%);
            padding: 2rem 2.5rem;
            border-radius: 14px;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 6px 30px rgba(0,0,0,0.4);
        }}
        .euron-header h1 {{
            color: white;
            font-size: 2.6rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
        }}
        .euron-header p {{
            color: rgba(255,255,255,0.85);
            font-size: 1.05rem;
            margin: 0.4rem 0 0;
        }}

        /* ── Score Card ── */
        .score-card {{
            background: #1a1a2e;
            border: 2px solid {accent_color};
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .score-card .score-number {{
            font-size: 3rem;
            font-weight: 900;
            color: {accent_color};
            margin: 0;
        }}
        .score-card .score-label {{
            color: #aaa;
            font-size: 0.9rem;
            margin-top: 0.3rem;
        }}

        /* ── Status Banners ── */
        .status-selected {{
            background: #1b5e20;
            color: #a5d6a7;
            border-left: 5px solid #4caf50;
            border-radius: 8px;
            padding: 1rem 1.5rem;
            font-size: 1.05rem;
            font-weight: 600;
            margin: 1rem 0;
        }}
        .status-rejected {{
            background: #b71c1c;
            color: #ffcdd2;
            border-left: 5px solid #ef5350;
            border-radius: 8px;
            padding: 1rem 1.5rem;
            font-size: 1.05rem;
            font-weight: 600;
            margin: 1rem 0;
        }}

        /* ── Skill Tags ── */
        .skill-tag-strength {{
            display: inline-block;
            background: #1b5e20;
            color: #a5d6a7;
            border-radius: 20px;
            padding: 4px 12px;
            margin: 3px;
            font-size: 0.82rem;
        }}
        .skill-tag-weakness {{
            display: inline-block;
            background: #4a0000;
            color: #ff8a80;
            border-radius: 20px;
            padding: 4px 12px;
            margin: 3px;
            font-size: 0.82rem;
        }}

        /* ── Result Box ── */
        .result-box {{
            background: #12121e;
            border-left: 4px solid {accent_color};
            border-radius: 8px;
            padding: 1.2rem 1.5rem;
            margin-top: 1rem;
            line-height: 1.8;
            color: #ddd;
        }}

        /* ── File Uploader ── */
        [data-testid="stFileUploadDropzone"] {{
            border: 2px dashed {accent_color} !important;
            border-radius: 10px !important;
            background: #1a1a2e !important;
        }}

        /* ── Buttons ── */
        .stButton > button {{
            background: linear-gradient(135deg, {accent_color}, #c62828);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }}

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab"] {{
            color: #aaa;
            font-weight: 600;
            padding: 10px 20px;
        }}
        .stTabs [aria-selected="true"] {{
            color: {accent_color} !important;
            border-bottom: 2px solid {accent_color} !important;
        }}

        /* ── Sidebar version ── */
        .sidebar-version {{
            text-align: center;
            color: #555;
            font-size: 0.78rem;
            margin-top: 2rem;
        }}
        </style>

        <!-- JavaScript for color picker integration (from video) -->
        <script>
        function updateAccentColor(color) {{
            document.documentElement.style.setProperty('--accent-color', color);
        }}
        </script>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# 3. DISPLAY HEADER
# ─────────────────────────────────────────────────────────────
def display_header():
    """
    From transcript: 'Header mein image/logo aur title display hota hai.
    JavaScript use kiya hai is section mein.'
    """
    st.markdown(
        """
        <div class="euron-header">
            <h1>🚀 Euron Recruitment Agent</h1>
            <p>Smart Resume Analysis &amp; Interview Preparation System</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# 4. SETUP SIDEBAR
# ─────────────────────────────────────────────────────────────
def setup_sidebar() -> tuple:
    """
    From transcript: 'Sidebar mein API key password field mein rakha hai
    taki dikhe nahi. Accent color bhi yahan se change karte hain.'
    Returns (api_key, accent_color)
    """
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("### 🔑 API Keys")

        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Enter your OpenAI API key. Get it at platform.openai.com",
            key="api_key_input"
        )

        st.markdown("---")
        st.markdown("### 🎨 Theme")

        accent_color = st.color_picker(
            "Accent Color",
            value="#e53935",
            help="Change the accent color of the UI"
        )

        st.markdown("---")
        st.markdown(
            """
            <div class="sidebar-version">
                🚀 Euron Recruitment Agent<br>v1.0.0
            </div>
            """,
            unsafe_allow_html=True,
        )

    return api_key, accent_color


# ─────────────────────────────────────────────────────────────
# 5. CREATE SCORE PIE CHART
# ─────────────────────────────────────────────────────────────
def create_score_pie_chart(score: float, cut_off: int = 75) -> None:
    """
    From transcript: 'Pie chart ke form mein data dikhata hai.
    Matplotlib use kiya hai. Strength aur weakness ka comparison.'
    """
    fig, ax = plt.subplots(figsize=(4, 4), facecolor="#0e0e1a")
    ax.set_facecolor("#0e0e1a")

    achieved = min(score, 100)
    remaining = max(0, 100 - achieved)

    colors = ["#4caf50" if score >= cut_off else "#ef5350", "#2a2a3e"]
    wedge_props = {"width": 0.5, "edgecolor": "#0e0e1a", "linewidth": 3}

    ax.pie(
        [achieved, remaining],
        colors=colors,
        startangle=90,
        wedgeprops=wedge_props,
    )

    # Center text
    center_text = f"{score:.0f}%"
    ax.text(0, 0, center_text, ha="center", va="center",
            fontsize=22, fontweight="bold",
            color="#4caf50" if score >= cut_off else "#ef5350")

    ax.text(0, -0.15, "ATS Score", ha="center", va="center",
            fontsize=9, color="#aaa")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────
# 6. DISPLAY ANALYSIS RESULTS
# ─────────────────────────────────────────────────────────────
def display_analysis(result: dict) -> None:
    """
    From transcript: 'Score dikhao, strengths dikhao, weaknesses dikhao,
    selected/not selected bata do. Pie chart bhi yahan show hota hai.'
    """
    if "error" in result:
        st.error(result["error"])
        return

    score = result.get("total_score", 0)
    selected = result.get("selected", False)
    strengths = result.get("strengths", [])
    missing = result.get("missing_skills", [])
    reasoning = result.get("reasoning", "")

    # ── Score row ──
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown(
            f"""<div class="score-card">
                <p class="score-number">{score:.0f}</p>
                <p class="score-label">ATS Score / 100</p>
            </div>""",
            unsafe_allow_html=True,
        )

    with col2:
        create_score_pie_chart(score, result.get("min_score", 75))

    with col3:
        st.markdown(
            f"""<div class="score-card">
                <p class="score-number" style="font-size:1.5rem">
                    {'✅ SELECTED' if selected else '❌ NOT SELECTED'}
                </p>
                <p class="score-label">Cut-off: {result.get('min_score', 75)}/100</p>
            </div>""",
            unsafe_allow_html=True,
        )

    # ── Selection status banner ──
    if selected:
        st.markdown(
            '<div class="status-selected">✅ Congratulations! Your resume passes ATS screening.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-rejected">❌ Unfortunately, your resume did not pass ATS screening.</div>',
            unsafe_allow_html=True,
        )

    # ── Reasoning ──
    st.markdown("#### 📋 Analysis Summary")
    st.markdown(
        f'<div class="result-box">{reasoning}</div>',
        unsafe_allow_html=True,
    )

    # ── Strengths ──
    if strengths:
        st.markdown("#### ✅ Strengths (Skills Matched)")
        strengths_html = "".join(
            f'<span class="skill-tag-strength">✓ {s}</span>' for s in strengths
        )
        st.markdown(strengths_html, unsafe_allow_html=True)

    # ── Missing Skills ──
    if missing:
        st.markdown("#### ❌ Missing Skills (Not Found in Resume)")
        missing_html = "".join(
            f'<span class="skill-tag-weakness">✗ {s}</span>' for s in missing
        )
        st.markdown(missing_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 7. DISPLAY WEAKNESS DETAIL
# ─────────────────────────────────────────────────────────────
def display_weakness_detail(text: str) -> None:
    """
    From transcript: 'Detail weakness analysis expand karke dikhata hai.'
    """
    if text:
        with st.expander("🔍 Detailed Weakness Analysis", expanded=False):
            st.markdown(
                f'<div class="result-box">{text}</div>',
                unsafe_allow_html=True,
            )
