import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Load env variables (for Gemini API)
load_dotenv()

# Set page config for aesthetics
st.set_page_config(page_title="Wellness Tracker", page_icon="🌿", layout="wide")

# Inject Custom CSS for Modern UI
def inject_custom_css():
    st.markdown("""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* Apply Font */
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        /* Main Background Gradient Header */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Metric Cards Styling */
        div[data-testid="metric-container"] {
            background-color: #1E1E2E; /* Dark elegant card */
            border: 1px solid #2A2A3C;
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(108, 99, 255, 0.4);
            border: 1px solid #6C63FF;
        }

        div[data-testid="metric-container"] > label {
            font-weight: 600 !important;
            color: #A0A0B0 !important;
            font-size: 0.95rem !important;
        }
        
        div[data-testid="metric-container"] > div {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
        }
        
        /* General expanders and containers */
        .stExpander, .stAlert {
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
        }
        
        /* Headers styling */
        h1, h2, h3 {
            color: #E0E0E0 !important;
            font-weight: 700 !important;
        }
        
        h1 {
            background: -webkit-linear-gradient(45deg, #6C63FF, #00FF87);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #151521;
        }
        </style>
    """, unsafe_allow_html=True)

# Call CSS
inject_custom_css()

# Initialize DB on start
from database.db import init_db
init_db()

from components.auth import authenticate

def main():
    # Attempt to log in user
    username = authenticate()
    
    if username is not None:
        # Save to session state so child pages can access it
        st.session_state.username = username
        display_name = st.session_state.get('user_display_name', username)
        
        st.sidebar.markdown("---")
        st.sidebar.success(f"Logged in as: **{display_name}**")
        
        # Welcoming landing page UI
        st.markdown(f"<h1>👋 Welcome back, {display_name}!</h1>", unsafe_allow_html=True)
        st.markdown("""
            ### Overview of the Platform
            Welcome to the **Smart Wellness Tracker**, an advanced, AI-driven personal health monitoring platform designed to provide holistic wellness insights. 
            
            This application intelligently tracks multiple biometric and activity measurements—transforming raw data like daily steps, heart rate averages, sleep duration, and productivity metrics into clear, actionable, and conversational insights.
            
            ### Getting Started 
            👈 **Please select a tool from the sidebar on the left to explore your data:**
            
            - **📊 1_Dashboard**: Access your personalized activity visualizations. Features sleek floating metrics, trend charts, correlation heatmaps, and AI-generated pattern alerts.
            - **🤖 2_Health_Assistant**: Chat directly with your very own AI-powered wellness coach. Ask questions about your recent performance and receive context-aware guidance based on your history.
        """)
        
if __name__ == "__main__":
    main()
