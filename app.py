import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go

# 1. Load your saved assets
# Ensure these files are in the same folder as app.py
model = joblib.load('sustainability_model.pkl')
features = joblib.load('feature_columns.pkl')

# 2. Page Configuration
st.set_page_config(page_title="ESG Judge Pro", page_icon="🌱", layout="wide")

# 3. Professional UI Styling (The "Background" and Look)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        background-image: linear-gradient(315deg, #f8f9fa 0%, #e8f5e9 74%);
    }
    .stApp {
        background: transparent;
    }
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True) # FIXED: Changed unsafe_all_with_html to unsafe_allow_html

# 4. App Header
st.title("🌱 Corporate Sustainability Intelligence")
st.write("Simulate corporate metrics to predict ESG Tiers and analyze the balance between pillars.")

# 5. Layout Columns
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("🛠️ Simulation Controls")
    # Grouping inputs into an expander for a cleaner UI
    with st.expander("Adjust ESG Pillars", expanded=True):
        gov = st.slider("Governance Score", 0, 100, 75)
        soc = st.slider("Social Score", 0, 100, 60)
        env = st.slider("Environmental Score", 0, 100, 65)
    
    with st.expander("Impact Metrics"):
        carbon = st.number_input("Carbon Footprint (Tons)", value=250)
        energy = st.number_input("Energy Consumption (MWh)", value=1200)

with col2:
    st.subheader("📊 Live Sustainability Profile")
    
    # 6. Radar Chart: Visualizing the Balance of the "Big Three"
    categories = ['Governance', 'Social', 'Environmental']
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[gov, soc, env],
        theta=categories,
        fill='toself',
        name='Company Profile',
        line_color='#2e7d32',
        fillcolor='rgba(46, 125, 50, 0.4)'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 7. Prediction Logic
if st.button("🚀 Analyze Company Tier", use_container_width=True):
    # Prepare the input matching the 14 training features
    full_input = {col: 0.0 for col in features}
    full_input.update({
        'ESG_Governance': gov, 'ESG_Social': soc, 'ESG_Environmental': env,
        'CarbonEmissions': carbon, 'EnergyConsumption': energy
    })
    
    # Ensure correct column order
    input_df = pd.DataFrame([full_input])[features]
    prediction = model.predict(input_df)[0]
    
    # Visual Results Section
    st.divider()
    c1, c2, c3 = st.columns(3)
    
    with c2:
        if prediction == 'Leader':
            st.success(f"### Result: **{prediction}**")
            st.balloons()
        elif prediction == 'Laggard':
            st.error(f"### Result: **{prediction}**")
        else:
            st.warning(f"### Result: **{prediction}**")