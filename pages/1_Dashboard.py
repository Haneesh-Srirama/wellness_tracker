import streamlit as st
from database.crud import get_user_data_df
from modules.analysis import generate_insights
from modules.visualization import plot_trends, plot_screentime_productivity

# Ensure the user is logged in via session state (set in app.py)
if 'username' not in st.session_state or not st.session_state.username:
    st.warning("Please log in from the main page first.")
    st.stop()

username = st.session_state.username

# Inject Global CSS manually for pages
def inject_custom_css():
    st.markdown("""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* Apply Font */
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .block-container {
            animation: fadeIn 0.8s ease-out;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Glassmorphism Metric Cards */
        div[data-testid="metric-container"] {
            background: rgba(30, 30, 46, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px 20px;
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 40px rgba(108, 99, 255, 0.5);
            border: 1px solid rgba(108, 99, 255, 0.8);
            background: rgba(40, 40, 60, 0.9);
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
            text-shadow: 0 2px 10px rgba(255,255,255,0.2);
        }
        
        /* General expanders and containers */
        .stExpander, .stAlert {
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            background: rgba(30, 30, 46, 0.6) !important;
            backdrop-filter: blur(12px) !important;
        }
        
        /* Headers styling */
        h1, h2, h3 {
            color: #E0E0E0 !important;
            font-weight: 700 !important;
        }
        
        h1 {
            background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #0F0F1A;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# Build the layout
display_name = st.session_state.get('user_display_name', username)
st.title(f"🌿 Dashboard: {display_name}")
df = get_user_data_df(username)

if df.empty:
    st.info("No data found for this user. Please ensure the Fitabase datasets are loaded properly.")
else:
    st.markdown("### Metrics Summary")
    # Top metrics summary
    latest = df.iloc[-1]
    cols = st.columns(6)
    cols[0].metric("🏃 Steps", latest['steps'])
    cols[1].metric("🔥 Calories", latest['calories'])
    cols[2].metric("💓 Avg HR (bpm)", round(latest['heart_rate'], 1))
    cols[3].metric("📱 Screen Time (hrs)", round(latest['screen_time'], 1))
    cols[4].metric("😴 Sleep (hrs)", round(latest['sleep_hours'], 1))
    cols[5].metric("⚡ Productivity", f"{int(latest['productivity'])}/10")
    
    st.markdown("---")
    
    # 70/30 Asymmetric Grid Layout for Hackathon UI
    left_col, right_col = st.columns([7, 3])
    
    with left_col:
        st.subheader("📈 Trends over Time")
        plot_trends(df)
        
        st.subheader("💡 Focus & Productivity")
        plot_screentime_productivity(df)
        
    with right_col:
        st.subheader("🤖 AI Insights & Alerts")
        insights = generate_insights(df)
        for insight in insights:
            if "check!" in insight.lower() or "tip:" in insight.lower() or "balance:" in insight.lower():
                st.warning(insight, icon="⚠️")
            elif "fantastic!" in insight.lower() or "great" in insight.lower() or "amazing!" in insight.lower():
                st.success(insight, icon="✅")
            else:
                st.info(insight, icon="💡")
