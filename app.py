import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.model import load_model, predict_yield
from utils.recommendations import get_crop_recommendations, get_optimization_suggestions
from data.states_data import INDIAN_STATES, CROP_TYPES

# Configure page
st.set_page_config(
    page_title="My Land - Crop Yield Prediction",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_model():
    """Load the trained model with caching"""
    return load_model()

@st.cache_data
def preprocess_inputs(state, rainfall, temperature, soil_ph, crop_type):
    """Preprocess user inputs for model prediction"""
    return {
        'state': state,
        'rainfall': rainfall,
        'temperature': temperature,
        'soil_ph': soil_ph,
        'crop_type': crop_type
    }

@st.cache_data
def get_historical_prediction(state, crop_type):
    """Get historical yield data for the region and crop"""
    # Historical average yields by state and crop (kg/ha)
    historical_data = {
        'Punjab': {
            'Rice': 4200, 'Wheat': 4800, 'Maize': 3800, 'Cotton': 1800
        },
        'Haryana': {
            'Rice': 3900, 'Wheat': 4600, 'Maize': 3600, 'Cotton': 1700
        },
        'Uttar Pradesh': {
            'Rice': 2400, 'Wheat': 3200, 'Sugarcane': 68000, 'Potato': 22000
        },
        'Maharashtra': {
            'Cotton': 1200, 'Sugarcane': 78000, 'Soybean': 1800, 'Rice': 2800
        },
        'Karnataka': {
            'Rice': 3200, 'Cotton': 1400, 'Sugarcane': 82000, 'Maize': 4500
        },
        'Tamil Nadu': {
            'Rice': 3600, 'Cotton': 1600, 'Sugarcane': 98000, 'Groundnut': 1900
        },
        'Gujarat': {
            'Cotton': 1500, 'Groundnut': 2100, 'Wheat': 3400, 'Rice': 2600
        },
        'West Bengal': {
            'Rice': 3400, 'Wheat': 3000, 'Potato': 24000, 'Jute': 2200
        },
        'Rajasthan': {
            'Wheat': 3800, 'Mustard': 1200, 'Barley': 2800, 'Cotton': 900
        }
    }
    
    # Default values if state/crop combination not found
    default_yields = {
        'Rice': 3000, 'Wheat': 3200, 'Maize': 4000, 'Cotton': 1200,
        'Sugarcane': 70000, 'Soybean': 1800, 'Groundnut': 1700, 'Pulses': 1200
    }
    
    state_data = historical_data.get(state, {})
    historical_yield = state_data.get(crop_type, default_yields.get(crop_type, 2500))
    
    return {
        'historical_yield': historical_yield,
        'data_source': f'Average yield data for {crop_type} in {state}',
        'reliability': 85.0 if state in historical_data else 70.0
    }

def main():
    # Header
    st.markdown("<div class='main-header'>", unsafe_allow_html=True)
    st.title("🌾 My Land - Crop Yield Prediction")
    st.markdown("*Empowering Indian farmers with AI-powered crop yield predictions*")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Initialize model
    with st.spinner("Loading prediction model..."):
        model = initialize_model()
    
    if model is None:
        st.error("❌ Failed to load the prediction model. Please check the model file.")
        return
    
    # Sidebar for inputs
    st.sidebar.header("🌾 My Land Inputs")
    
    # State selection
    state = st.sidebar.selectbox(
        "🗺️ Select Your State",
        options=list(INDIAN_STATES.keys()),
        help="Choose your state for location-specific predictions"
    )
    
    # Environmental parameters
    st.sidebar.subheader("🌡️ Environmental Conditions")
    
    rainfall = st.sidebar.slider(
        "🌧️ Rainfall (mm)",
        min_value=200,
        max_value=3000,
        value=800,
        step=50,
        help="Annual rainfall in millimeters"
    )
    
    temperature = st.sidebar.slider(
        "🌡️ Temperature (°C)",
        min_value=15,
        max_value=40,
        value=25,
        step=1,
        help="Average temperature in Celsius"
    )
    
    soil_ph = st.sidebar.slider(
        "🧪 Soil pH Level",
        min_value=4.0,
        max_value=9.0,
        value=6.5,
        step=0.1,
        help="Soil acidity/alkalinity level"
    )
    
    # Crop type selection
    crop_type = st.sidebar.selectbox(
        "🌱 Select Crop Type",
        options=CROP_TYPES,
        help="Choose the crop you want to grow"
    )
    
    # Predict button
    predict_button = st.sidebar.button("🔮 Predict Yield", type="primary", use_container_width=True)
    
    # Main content area
    if predict_button:
        with st.spinner("Analyzing conditions and predicting yield..."):
            # Preprocess inputs
            inputs = preprocess_inputs(
                state, rainfall, temperature, soil_ph, crop_type
            )
            
            # Get both user-input prediction and historical data
            prediction_result = predict_yield(model, inputs)
            historical_result = get_historical_prediction(state, crop_type)
            
            if prediction_result is None:
                st.error("❌ Failed to generate prediction. Please check your inputs.")
                return
            
            # Store results in session state
            st.session_state.prediction_result = prediction_result
            st.session_state.historical_result = historical_result
            st.session_state.inputs = inputs
    
    # Display results if available
    if 'prediction_result' in st.session_state:
        display_results(
            st.session_state.prediction_result, 
            st.session_state.historical_result,
            st.session_state.inputs
        )

def display_results(prediction_result, historical_result, inputs):
    """Display prediction results, visualizations, and recommendations"""
    
    # Success message
    st.success("✅ Prediction completed successfully!")
    
    # Get yield values for comparison
    user_yield = prediction_result['yield']
    historical_yield = historical_result['historical_yield']
    confidence = prediction_result['confidence']
    
    # Calculate market value (Indian Rupees per kg - approximate rates)
    crop_market_rates = {
        'Rice': 20, 'Wheat': 22, 'Maize': 18, 'Cotton': 55, 'Sugarcane': 3.5,
        'Soybean': 45, 'Groundnut': 52, 'Pulses': 65, 'Mustard': 50, 'Sunflower': 55
    }
    
    market_rate = crop_market_rates.get(inputs['crop_type'], 25)
    user_revenue = user_yield * market_rate
    historical_revenue = historical_yield * market_rate
    
    # Determine farmer mood and message based on yield comparison
    yield_ratio = user_yield / historical_yield if historical_yield > 0 else 1
    
    if yield_ratio > 1.2:
        farmer_emoji = "😊🎉"
        mood_color = "#28a745"
        motivation = "Excellent! Your conditions are perfect for farming success!"
        achievement = "🏆 Outstanding Performance"
    elif yield_ratio > 1.0:
        farmer_emoji = "😊🌾"
        mood_color = "#28a745"
        motivation = "Great work! You're above average - keep it up!"
        achievement = "✨ Above Average"
    elif yield_ratio > 0.8:
        farmer_emoji = "😐🌱"
        mood_color = "#ffc107"
        motivation = "Don't worry! Every farmer faces challenges. 'The farmer has to be an optimist or he wouldn't still be a farmer.' - Will Rogers"
        achievement = "💪 Room for Growth"
    else:
        farmer_emoji = "😔🌾"
        mood_color = "#dc3545"
        motivation = "Stay strong! 'Agriculture is our wisest pursuit, because it will in the end contribute most to real wealth.' - Thomas Jefferson. Better days ahead!"
        achievement = "🌱 Learning Journey"
    
    # Main prediction display with farmer graphics
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%); border-radius: 15px; margin: 20px 0;'>
        <h1 style='color: {mood_color}; margin: 0;'>{farmer_emoji}</h1>
        <h2 style='color: {mood_color}; margin: 10px 0;'>{achievement}</h2>
        <p style='font-style: italic; color: #666; margin: 10px 0; font-size: 16px;'>{motivation}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two prediction comparisons
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Your Input Prediction")
        st.markdown(f"""
        <div class='prediction-card' style='background: linear-gradient(135deg, #e3f2fd 0%, #f1f8fd 100%); border-left: 5px solid #2196f3;'>
            <h2 style='text-align: center; color: #1976d2; margin: 0;'>
                {user_yield:.0f} kg/ha
            </h2>
            <p style='text-align: center; margin: 10px 0; color: #666;'>
                Based on Your Conditions
            </p>
            <p style='text-align: center; margin: 5px 0; color: #666;'>
                Confidence: {confidence:.0f}%
            </p>
            <hr style='margin: 15px 0;'>
            <p style='text-align: center; color: #1976d2; font-weight: bold; margin: 0;'>
                💰 ₹{user_revenue:,.0f} per hectare
            </p>
            <p style='text-align: center; color: #666; font-size: 12px; margin: 5px 0 0 0;'>
                @ ₹{market_rate}/kg market rate
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📈 Historical Average")
        reliability_color = "#28a745" if historical_result['reliability'] > 80 else "#ffc107"
        st.markdown(f"""
        <div class='prediction-card' style='background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%); border-left: 5px solid #4caf50;'>
            <h2 style='text-align: center; color: #388e3c; margin: 0;'>
                {historical_yield:.0f} kg/ha
            </h2>
            <p style='text-align: center; margin: 10px 0; color: #666;'>
                {historical_result['data_source']}
            </p>
            <p style='text-align: center; margin: 5px 0; color: {reliability_color};'>
                Reliability: {historical_result['reliability']:.0f}%
            </p>
            <hr style='margin: 15px 0;'>
            <p style='text-align: center; color: #388e3c; font-weight: bold; margin: 0;'>
                💰 ₹{historical_revenue:,.0f} per hectare
            </p>
            <p style='text-align: center; color: #666; font-size: 12px; margin: 5px 0 0 0;'>
                Historical average revenue
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Comparison metrics
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        yield_diff = user_yield - historical_yield
        yield_diff_percent = ((user_yield / historical_yield) - 1) * 100 if historical_yield > 0 else 0
        st.metric(
            "Yield Difference", 
            f"{yield_diff:+.0f} kg/ha",
            delta=f"{yield_diff_percent:+.1f}%"
        )
    
    with col_b:
        revenue_diff = user_revenue - historical_revenue
        st.metric(
            "Revenue Difference",
            f"₹{revenue_diff:+,.0f}",
            delta=f"{yield_diff_percent:+.1f}%"
        )
    
    with col_c:
        acres_revenue = user_revenue * 0.4047  # Revenue per acre
        st.metric(
            "Revenue per Acre",
            f"₹{acres_revenue:,.0f}",
            delta=None
        )
    
    # Comparison gauge chart
    st.subheader("⚖️ Yield Comparison Gauge")
    
    fig_gauge = go.Figure()
    
    # Add historical yield as reference line
    fig_gauge.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = user_yield,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Your Yield vs Historical Average"},
        delta = {'reference': historical_yield, 'valueformat': '.0f'},
        gauge = {
            'axis': {'range': [None, max(user_yield, historical_yield) * 1.5]},
            'bar': {'color': mood_color},
            'steps': [
                {'range': [0, historical_yield * 0.8], 'color': "#ffebee"},
                {'range': [historical_yield * 0.8, historical_yield * 1.2], 'color': "#fff8e1"},
                {'range': [historical_yield * 1.2, max(user_yield, historical_yield) * 1.5], 'color': "#e8f5e8"}
            ],
            'threshold': {
                'line': {'color': "#4caf50", 'width': 4},
                'thickness': 0.75,
                'value': historical_yield
            }
        }
    ))
    
    fig_gauge.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Environmental factor analysis
    st.subheader("🌍 Environmental Impact Analysis")
    
    factors = prediction_result['factor_importance']
    
    fig_factors = px.bar(
        x=list(factors.values()),
        y=list(factors.keys()),
        orientation='h',
        title="Which factors affect your yield the most?",
        color=list(factors.values()),
        color_continuous_scale="Viridis",
        text=list(factors.values())
    )
    fig_factors.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_factors.update_layout(
        height=400, 
        margin=dict(l=100, r=20, t=60, b=20),
        xaxis_title="Impact Percentage (%)",
        yaxis_title="Environmental Factors"
    )
    st.plotly_chart(fig_factors, use_container_width=True)
    
    # Visualizations section
    st.subheader("📈 Analysis & Insights")
    
    tab1, tab2, tab3 = st.tabs(["📊 Parameter Analysis", "🗺️ Regional Comparison", "📅 Seasonal Trends"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Environmental conditions radar chart
            env_params = ['Rainfall', 'Temperature', 'Soil pH']
            env_values = [
                min(inputs['rainfall']/1500, 1.0),  # Normalize rainfall to 0-1
                inputs['temperature']/40,  # Normalize temperature to 0-1
                inputs['soil_ph']/10  # Normalize pH to 0-1
            ]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=env_values,
                theta=env_params,
                fill='toself',
                name='Current Conditions',
                line_color='rgb(75, 192, 192)'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                title="Environmental Conditions Profile"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            # Climate suitability chart
            climate_data = {
                'Parameter': ['Temperature', 'Rainfall', 'Overall Climate'],
                'Suitability': [
                    prediction_result['climate_suitability']['temperature'],
                    prediction_result['climate_suitability']['rainfall'],
                    prediction_result['climate_suitability']['overall']
                ]
            }
            
            fig_climate = px.bar(
                climate_data,
                x='Parameter',
                y='Suitability',
                title="Climate Suitability Score",
                color='Suitability',
                color_continuous_scale="RdYlGn"
            )
            fig_climate.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig_climate, use_container_width=True)
    
    with tab2:
        # Regional comparison (mock data for demonstration)
        regional_data = prediction_result['regional_comparison']
        
        fig_map = px.bar(
            x=list(regional_data.keys()),
            y=list(regional_data.values()),
            title=f"Average {inputs['crop_type']} Yield by Region (kg/ha)",
            color=list(regional_data.values()),
            color_continuous_scale="Greens"
        )
        fig_map.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.info(f"Your predicted yield of {user_yield:.2f} kg/ha is compared against regional averages.")
    
    with tab3:
        # Seasonal trends
        seasonal_data = prediction_result['seasonal_trends']
        
        fig_seasonal = px.line(
            x=list(seasonal_data.keys()),
            y=list(seasonal_data.values()),
            title=f"Seasonal Yield Trends for {inputs['crop_type']}",
            markers=True
        )
        fig_seasonal.update_layout(
            xaxis_title="Month",
            yaxis_title="Expected Yield (kg/ha)"
        )
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    # Recommendations section
    st.subheader("💡 Recommendations & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌱 Crop Optimization")
        crop_recommendations = get_crop_recommendations(inputs, prediction_result)
        
        for i, rec in enumerate(crop_recommendations, 1):
            if rec['type'] == 'success':
                st.success(f"**{i}.** {rec['message']}")
            elif rec['type'] == 'warning':
                st.warning(f"**{i}.** {rec['message']}")
            else:
                st.info(f"**{i}.** {rec['message']}")
    
    with col2:
        st.markdown("#### 💰 Profit Optimization")
        profit_suggestions = get_optimization_suggestions(inputs, prediction_result)
        
        for i, suggestion in enumerate(profit_suggestions, 1):
            if suggestion['type'] == 'success':
                st.success(f"**{i}.** {suggestion['message']}")
            elif suggestion['type'] == 'warning':
                st.warning(f"**{i}.** {suggestion['message']}")
            else:
                st.info(f"**{i}.** {suggestion['message']}")
    
    # Action items with farmer-friendly language
    st.subheader("🎯 Your Next Steps")
    
    # Smart action items based on conditions
    action_items = []
    
    if user_yield > historical_yield:
        action_items.append("🌟 Your conditions are great! Focus on maintaining current practices")
        action_items.append("📈 Consider expanding cultivation area for increased profits")
    else:
        action_items.append("💧 Monitor water supply and plan irrigation carefully")
        action_items.append("🌱 Consider soil health improvement measures")
    
    action_items.extend([
        "📱 Keep track of market prices for best selling time",
        "🌦️ Watch weather forecasts and plan accordingly",
        "🤝 Connect with local agricultural extension officers for guidance"
    ])
    
    for item in action_items:
        st.markdown(f"- {item}")
    
    # Market information card
    st.markdown("---")
    st.subheader("💰 Market Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **Current Market Rate**  
        ₹{market_rate}/kg for {inputs['crop_type']}
        """)
    
    with col2:
        total_revenue_1_acre = acres_revenue
        st.success(f"""
        **Expected Revenue (1 Acre)**  
        ₹{total_revenue_1_acre:,.0f}
        """)
    
    with col3:
        if st.button("📊 Show Market Trends", use_container_width=True):
            st.info("🚀 Market trend analysis feature coming soon! Track price movements and plan your selling strategy.")

if __name__ == "__main__":
    main()
