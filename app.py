import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import base64

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="ESG Sustainability Score",
    page_icon="🌱",
    layout="wide"
)

# --------------------------------------------------
# BACKGROUND FUNCTION
# --------------------------------------------------
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>

        /* Background */
        .stApp {{
            background: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.22);
            z-index: -1;
        }}

        /* Headings */
        h1, h2, h3 {{
            color: white !important;
            font-weight: 700;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        }}

        p {{
            color: white !important;
            text-shadow: 1px 1px 6px rgba(0,0,0,0.8);
        }}

        /* Universal Glass Card */
        .glass-card {{
            background: rgba(22, 27, 34, 0.55);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        }}

        /* Expander */
        div[data-testid="stExpander"] {{
            background: rgba(22, 27, 34, 0.55) !important;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        }}

        /* Inputs */
        div[data-baseweb="input"] {{
            background-color: rgba(0,0,0,0.5) !important;
            border-radius: 10px;
            color: white !important;
        }}

        /* Buttons */
        .stButton > button {{
            border-radius: 14px;
            background: linear-gradient(90deg, #2e7d32, #43a047);
            color: white;
            font-weight: 600;
            padding: 0.8rem;
            border: none;
            font-size: 16px;
        }}

        .stButton > button:hover {{
            background: linear-gradient(90deg, #1b5e20, #2e7d32);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background
set_background("env2.jpg")

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
model = joblib.load("sustainability_model.pkl")
features = joblib.load("feature_columns.pkl")

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("Corporate Sustainability Intelligence")
st.write("Simulate corporate metrics to predict ESG Tiers and analyze the balance between pillars.")

st.divider()

# --------------------------------------------------
# LAYOUT
# --------------------------------------------------
col1, col2 = st.columns([1, 1.5])

# ---------------- LEFT ----------------
with col1:
    st.subheader("Simulation Controls")

    with st.expander("Adjust ESG Pillars", expanded=True):
        gov = st.slider("Governance Score", 0, 100, 75)
        soc = st.slider("Social Score", 0, 100, 60)
        env = st.slider("Environmental Score", 0, 100, 65)

    with st.expander("Impact Metrics"):
        carbon = st.number_input("Carbon Footprint (Tons)", value=250)
        energy = st.number_input("Energy Consumption (MWh)", value=1200)

# ---------------- RIGHT ----------------
with col2:
    st.subheader("Live Sustainability Profile")

    categories = ['Governance', 'Social', 'Environmental']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[gov, soc, env],
        theta=categories,
        fill='toself',
        line_color='#4CAF50',
        fillcolor='rgba(76, 175, 80, 0.4)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(255,255,255,0.3)"
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )

    # Glass background for chart
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
if st.button("Analyze Company Tier", use_container_width=True):

    full_input = {col: 0.0 for col in features}
    full_input.update({
        'ESG_Governance': gov,
        'ESG_Social': soc,
        'ESG_Environmental': env,
        'CarbonEmissions': carbon,
        'EnergyConsumption': energy
    })

    input_df = pd.DataFrame([full_input])[features]
    prediction = model.predict(input_df)[0]

    st.divider()

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    if prediction == "Leader":
        st.markdown("<h2 style='color:#4CAF50;'>🏆 Leader Tier</h2>", unsafe_allow_html=True)
        st.balloons()   # 🎈 BALLOONS ENABLED
    elif prediction == "Laggard":
        st.markdown("<h2 style='color:#ff5252;'>⚠️ Laggard Tier</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color:#FFC107;'>⚖️ Average Tier</h2>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

