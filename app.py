import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Gatundu North Sweet Potato Risk Dashboard",
    page_icon="",
    layout="wide"
)

# ==================== LOAD YOUR RF MODEL ====================
@st.cache_resource
def load_model():
    try:
        model = joblib.load(r"D:\MKULIMA_SHAPEUP\sweet_popatoes_stress_model (1).pkl")
        return model
    except:
        st.warning("Model not found. Using simulated predictions.")
        return None

model = load_model()

# ==================== GATUNDU NORTH WARDS DATA ====================
GATUNDU_NORTH_WARDS = {
    "Chania Ward": {
        "population": "45,200",
        "area_km2": "45.2",
        "altitude": "1750-1850m",
        "soil_type": "Red volcanic, well-drained",
        "sweet_potato_area_ha": 320,
        "avg_yield_ton_ha": 8.5,
        "main_varieties": ["Orange Fleshed", "Purple", "White"],
        "risk_factors": ["Soil erosion", "Limited irrigation", "Pest pressure"],
        "market_access": "Good",
        "market_details": "near Gatundu town",
        "irrigation_coverage": "25%",
        "color": "#FF9800"
    },
    "Githobokoni Ward": {
        "population": "38,500",
        "area_km2": "38.7",
        "altitude": "1700-1800m",
        "soil_type": "Clay loam, volcanic",
        "sweet_potato_area_ha": 280,
        "avg_yield_ton_ha": 7.8,
        "main_varieties": ["Orange Fleshed", "Local white"],
        "risk_factors": ["Waterlogging in valleys", "Frost risk", "Rodents"],
        "market_access": "Moderate",
        "market_details": "",
        "irrigation_coverage": "18%",
        "color": "#4CAF50"
    },
    "Gituamba Ward": {
        "population": "52,800",
        "area_km2": "52.1",
        "altitude": "1800-1900m",
        "soil_type": "Mixed volcanic soils",
        "sweet_potato_area_ha": 420,
        "avg_yield_ton_ha": 9.2,
        "main_varieties": ["Commercial varieties", "Orange Fleshed", "Purple"],
        "risk_factors": ["Land pressure", "Pollution risk", "High input costs"],
        "market_access": "Excellent",
        "market_details": "urban market",
        "irrigation_coverage": "40%",
        "color": "#2196F3"
    },
    "Mang'u Ward": {
        "population": "42,300",
        "area_km2": "42.5",
        "altitude": "1650-1750m",
        "soil_type": "Sandy loam, less fertile",
        "sweet_potato_area_ha": 380,
        "avg_yield_ton_ha": 6.5,
        "main_varieties": ["Traditional varieties", "Drought tolerant"],
        "risk_factors": ["Drought prone", "Poor soils", "Limited extension services"],
        "market_access": "Poor",
        "market_details": "remote areas",
        "irrigation_coverage": "12%",
        "color": "#9C27B0"
    }
}

# Sweet potato specific parameters
SWEET_POTATO_PROFILE = {
    "optimal_temp": "20-30°C",
    "optimal_soil_temp": "18-25°C",
    "rainfall_need": "750-1000mm",
    "growing_period": "3-6 months",
    "drought_tolerance": "Medium-High",
    "waterlogging_sensitivity": "High",
    "critical_stages": ["Vine establishment", "Tuber initiation", "Tuber bulking"],
    "major_pests": ["Sweet potato weevil", "Virus complexes", "Rodents"],
    "major_diseases": ["Alternaria leaf spot", "Fusarium wilt", "Root rot"]
}

# ==================== DASHBOARD HEADER ====================
st.title(" Gatundu North Sweet Potato Risk Comparison Dashboard")
st.markdown("**Ward-level risk assessment for sweet potato farming** | Using Random Forest predictions")

# ==================== SIDEBAR ====================
st.sidebar.title("Sweet Potato Focus")
st.sidebar.markdown(f"""
**Gatundu North Sub-County**
*Kiambu County*

**Sweet Potato Profile:**
- Optimal Temp: {SWEET_POTATO_PROFILE['optimal_temp']}
- Rainfall Need: {SWEET_POTATO_PROFILE['rainfall_need']}
- Growing Period: {SWEET_POTATO_PROFILE['growing_period']}
- Drought Tolerance: {SWEET_POTATO_PROFILE['drought_tolerance']}
""")

# ==================== MAIN DASHBOARD ====================
tab1, tab2, tab3 = st.tabs(["📊 Ward Comparison", "🎯 Risk Assessment", "📈 Historical Analysis"])

with tab1:
    st.header("Ward-to-Ward Comparison")
    
    # FIXED: Clean market access values and handle them properly
    market_access_levels = ["Poor", "Moderate", "Good", "Excellent"]
    
    comparison_data = []
    for ward, data in GATUNDU_NORTH_WARDS.items():
        # Clean market access - extract just the level
        market_access = data['market_access']
        
        # Get index for market access
        try:
            market_index = market_access_levels.index(market_access)
        except ValueError:
            # If not found, default to "Moderate"
            market_index = 1
        
        # Convert population string to integer
        try:
            population_int = int(data['population'].replace(',', ''))
        except:
            population_int = 40000  # Default value
        
        comparison_data.append({
            'Ward': ward,
            'Population': population_int,
            'Area (km²)': float(data['area_km2']),
            'Sweet Potato Area (ha)': data['sweet_potato_area_ha'],
            'Avg Yield (ton/ha)': data['avg_yield_ton_ha'],
            'Irrigation %': float(data['irrigation_coverage'].replace('%', '')),
            'Market Access': market_access,
            'Market Access Index': market_index,  # Use the cleaned index
            'Risk Score': np.random.uniform(0.2, 0.8)  # Simulated for now
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # Visual comparison
    col1, col2 = st.columns(2)
    
    with col1:
        # Yield comparison
        fig_yield = px.bar(df_comparison, 
                          x='Ward', 
                          y='Avg Yield (ton/ha)',
                          color='Ward',
                          color_discrete_map={
                              ward: data['color'] 
                              for ward, data in GATUNDU_NORTH_WARDS.items()
                          },
                          title="Sweet Potato Yield by Ward",
                          text='Avg Yield (ton/ha)')
        fig_yield.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        st.plotly_chart(fig_yield, use_container_width=True)
        
        # Irrigation coverage
        fig_irrigation = px.pie(df_comparison,
                               values='Irrigation %',
                               names='Ward',
                               title="Irrigation Coverage by Ward",
                               color='Ward',
                               color_discrete_map={
                                   ward: data['color'] 
                                   for ward, data in GATUNDU_NORTH_WARDS.items()
                               })
        st.plotly_chart(fig_irrigation, use_container_width=True)
    
    with col2:
        # Area under cultivation
        fig_area = px.bar(df_comparison,
                         x='Ward',
                         y='Sweet Potato Area (ha)',
                         color='Ward',
                         color_discrete_map={
                             ward: data['color'] 
                             for ward, data in GATUNDU_NORTH_WARDS.items()
                         },
                         title="Sweet Potato Cultivation Area",
                         text='Sweet Potato Area (ha)')
        fig_area.update_traces(texttemplate='%{text:.0f} ha', textposition='outside')
        st.plotly_chart(fig_area, use_container_width=True)
        
        # Risk radar chart - FIXED: Use Market Access Index instead of trying to find string
        fig_radar = go.Figure()
        
        for ward in GATUNDU_NORTH_WARDS.keys():
            ward_df = df_comparison[df_comparison['Ward'] == ward]
            fig_radar.add_trace(go.Scatterpolar(
                r=[
                    ward_df['Avg Yield (ton/ha)'].values[0]/10,  # Scale down
                    ward_df['Irrigation %'].values[0]/20,        # Scale down
                    ward_df['Market Access Index'].values[0]/3,  # Scale to 0-1
                    1 - ward_df['Risk Score'].values[0]          # Inverted risk
                ],
                theta=['Yield', 'Irrigation', 'Market', 'Safety'],
                name=ward,
                fill='toself'
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Ward Performance Radar Chart"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # Detailed ward information
    st.subheader(" Detailed Ward Profiles")
    selected_ward = st.selectbox("Select ward for details:", list(GATUNDU_NORTH_WARDS.keys()))
    
    if selected_ward:
        ward_data = GATUNDU_NORTH_WARDS[selected_ward]
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Population", ward_data['population'])
            st.metric("Area", f"{ward_data['area_km2']} km²")
            st.metric("Altitude", ward_data['altitude'])
        
        with col_b:
            st.metric("Sweet Potato Area", f"{ward_data['sweet_potato_area_ha']} ha")
            st.metric("Average Yield", f"{ward_data['avg_yield_ton_ha']} ton/ha")
            st.metric("Irrigation Coverage", ward_data['irrigation_coverage'])
        
        with col_c:
            st.write("**Main Varieties:**")
            for variety in ward_data['main_varieties']:
                st.write(f"- {variety}")
            
            st.write("**Market Access:**")
            # Combine the access level with details if they exist
            market_text = ward_data['market_access']
            if ward_data.get('market_details'):
                market_text += f" ({ward_data['market_details']})"
            st.write(market_text)
        
        # Risk factors
        st.write("**Major Risk Factors:**")
        for risk in ward_data['risk_factors']:
            st.write(f"⚠️ {risk}")

# Rest of your code remains the same...
with tab2:
    st.header(" Sweet Potato Risk Assessment")
    st.markdown("**Using your Random Forest model for stress prediction**")
    
    # Multi-ward input for comparison
    st.subheader("Compare Multiple Wards")
    
    selected_wards = st.multiselect(
        "Select wards to compare:",
        list(GATUNDU_NORTH_WARDS.keys()),
        default=list(GATUNDU_NORTH_WARDS.keys())[:2]
    )
    
    if selected_wards:
        # Create input columns for each selected ward
        ward_inputs = {}
        
        cols = st.columns(len(selected_wards))
        for idx, ward in enumerate(selected_wards):
            with cols[idx]:
                st.markdown(f"### {ward}")
                
                # Ward-specific default values based on characteristics
                ward_data = GATUNDU_NORTH_WARDS[ward]
                
                # Adjust defaults based on ward characteristics
                if ward == "Gituamba":  # Drier area
                    default_lst = 32.0
                    default_sm = 45.0
                elif ward == "Gatundu North (Town)":  # Urban, warmer
                    default_lst = 30.0
                    default_sm = 50.0
                else:  # Other wards
                    default_lst = 28.0
                    default_sm = 60.0
                
                lst = st.slider(
                    f"Temperature (°C)",
                    min_value=20.0,
                    max_value=40.0,
                    value=default_lst,
                    key=f"lst_{ward}"
                )
                
                soil_moisture = st.slider(
                    f"Soil Moisture (%)",
                    min_value=20.0,
                    max_value=100.0,
                    value=default_sm,
                    key=f"sm_{ward}"
                )
                
                ndvi = st.slider(
                    f"NDVI Value",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.65,
                    step=0.01,
                    key=f"ndvi_{ward}"
                )
                
                ward_inputs[ward] = [lst, soil_moisture, ndvi]
        
        # Run RF predictions
        if st.button("Run Random Forest Predictions", type="primary"):
            st.subheader(" Prediction Results")
            
            results = []
            
            for ward, features in ward_inputs.items():
                features_array = np.array([features])
                
                if model is not None:
                    # Use actual RF model
                    try:
                        if hasattr(model, 'predict_proba'):
                            stress_prob = model.predict_proba(features_array)[0][1]
                        else:
                            stress_prob = float(model.predict(features_array)[0])
                    except:
                        # Fallback calculation
                        stress_prob = (features[0]/40 * 0.4) + ((100-features[1])/100 * 0.4) + ((1-features[2])/2 * 0.2)
                else:
                    # Simulated prediction
                    stress_prob = (features[0]/40 * 0.4) + ((100-features[1])/100 * 0.4) + ((1-features[2])/2 * 0.2)
                
                # Adjust based on ward characteristics
                if ward == "Gituamba":
                    stress_prob *= 1.2  # Higher risk area
                elif ward == "Kamwangi":
                    stress_prob *= 0.9  # Better conditions
                
                results.append({
                    'Ward': ward,
                    'LST': features[0],
                    'Soil Moisture': features[1],
                    'NDVI': features[2],
                    'Stress Probability': stress_prob,
                    'Risk Level': 'HIGH' if stress_prob > 0.6 else ('MODERATE' if stress_prob > 0.3 else 'LOW')
                })
            
            # Display results
            results_df = pd.DataFrame(results)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Results table
                st.dataframe(results_df.style.format({
                    'LST': '{:.1f}°C',
                    'Soil Moisture': '{:.1f}%',
                    'NDVI': '{:.3f}',
                    'Stress Probability': '{:.3f}'
                }), use_container_width=True)
            
            with col2:
                # Comparative bar chart
                fig = px.bar(results_df,
                            x='Ward',
                            y='Stress Probability',
                            color='Risk Level',
                            color_discrete_map={
                                'LOW': '#4CAF50',
                                'MODERATE': '#FFC107',
                                'HIGH': '#F44336'
                            },
                            title="Stress Probability by Ward",
                            text='Stress Probability')
                fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            # Insurance recommendations
            st.subheader("💰 Insurance Recommendations")
            
            for result in results:
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    st.metric(f"{result['Ward']}", result['Risk Level'])
                
                with col_b:
                    if result['Stress Probability'] > 0.6:
                        st.write("**High Premium (25-40% increase)** - Consider yield protection insurance")
                    elif result['Stress Probability'] > 0.3:
                        st.write("**Moderate Premium (10-20% increase)** - Standard coverage with monitoring")
                    else:
                        st.write("**Low Premium (0-10% increase)** - Basic coverage sufficient")

with tab3:
    st.header("📈 Historical Sweet Potato Performance")
    
    # Generate historical data
    years = list(range(2018, 2024))
    
    # Create ward-specific historical trends
    historical_data = []
    for year in years:
        for ward in GATUNDU_NORTH_WARDS.keys():
            # Base values with some randomness and trend
            base_yield = GATUNDU_NORTH_WARDS[ward]['avg_yield_ton_ha']
            
            # Yearly variation
            if year == 2021:  # Bad year
                yield_mult = 0.7
                stress_level = 0.8
            elif year == 2022:  # Good year
                yield_mult = 1.1
                stress_level = 0.3
            else:
                yield_mult = np.random.uniform(0.9, 1.05)
                stress_level = np.random.uniform(0.4, 0.6)
            
            # Adjust for ward characteristics
            if ward == "Gituamba":
                yield_mult *= 0.9  # Consistently lower yields
                stress_level *= 1.1  # Higher stress
            
            historical_data.append({
                'Year': year,
                'Ward': ward,
                'Yield (ton/ha)': base_yield * yield_mult,
                'Stress Level': stress_level,
                'Rainfall (mm)': np.random.uniform(800, 1400),
                'Temperature (°C)': np.random.uniform(22, 28)
            })
    
    hist_df = pd.DataFrame(historical_data)
    
    # Interactive visualization
    st.subheader("Yield Trends Over Time")
    
    selected_wards_hist = st.multiselect(
        "Select wards for historical view:",
        list(GATUNDU_NORTH_WARDS.keys()),
        default=list(GATUNDU_NORTH_WARDS.keys())[:2]
    )
    
    if selected_wards_hist:
        filtered_df = hist_df[hist_df['Ward'].isin(selected_wards_hist)]
        
        # Line chart for yield trends
        fig = px.line(filtered_df,
                     x='Year',
                     y='Yield (ton/ha)',
                     color='Ward',
                     markers=True,
                     title="Sweet Potato Yield Trends (2018-2023)",
                     color_discrete_map={
                         ward: data['color'] 
                         for ward, data in GATUNDU_NORTH_WARDS.items()
                     })
        st.plotly_chart(fig, use_container_width=True)
        
        # Show 2021 drought impact
        st.subheader(" 2021 Drought Impact Analysis")
        
        # Calculate impact
        impact_data = []
        for ward in selected_wards_hist:
            ward_data = hist_df[hist_df['Ward'] == ward]
            normal_yield = ward_data[ward_data['Year'] == 2020]['Yield (ton/ha)'].values[0]
            drought_yield = ward_data[ward_data['Year'] == 2021]['Yield (ton/ha)'].values[0]
            reduction = ((normal_yield - drought_yield) / normal_yield) * 100
            
            impact_data.append({
                'Ward': ward,
                'Normal Yield (2020)': normal_yield,
                'Drought Yield (2021)': drought_yield,
                'Reduction %': reduction
            })
        
        impact_df = pd.DataFrame(impact_data)
        st.dataframe(impact_df.style.format({
            'Normal Yield (2020)': '{:.1f}',
            'Drought Yield (2021)': '{:.1f}',
            'Reduction %': '{:.1f}%'
        }), use_container_width=True)

# ==================== FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.markdown("###  Sweet Potato Notes")
st.sidebar.info("""
**Key Considerations for Gatundu North:**
- Sweet potatoes prefer well-drained soils
- Sensitive to waterlogging
- Major pest: Sweet potato weevil
- Critical period: Tuber bulking (needs consistent moisture)
- Harvest before heavy rains to avoid rotting
""")

st.sidebar.markdown("###  Ward Characteristics")
st.sidebar.write("""
**Mang'u Ward**: Highest risk, driest area  
**Chania Ward**: Best market access  
**Githobokoni Ward**: Good soils, frost risk  
**Gituamba Ward**: Highest yields, urban pressure
""")