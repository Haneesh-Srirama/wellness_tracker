import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def plot_trends(df):
    if df.empty:
        st.info("Log some data to see trends over time.")
        return
        
    # Steps over time
    fig_steps = px.line(df, x='date', y='steps', title="Steps Over Time", markers=True)
    fig_steps.update_traces(line_color="#00FF87", line_width=3, marker=dict(size=8, color="#FFFFFF"))
    fig_steps.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2A2A3C'),
        font=dict(family="Inter", color="#A0A0B0")
    )
    st.plotly_chart(fig_steps, use_container_width=True)
    
    # Sleep and Productivity
    fig_sleep_prod = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_sleep_prod.add_trace(
        go.Bar(x=df['date'], y=df['sleep_hours'], name="Sleep (hrs)", marker_color='#6C63FF', opacity=0.8, marker_line_width=0),
        secondary_y=False,
    )
    fig_sleep_prod.add_trace(
        go.Scatter(x=df['date'], y=df['productivity'], mode='lines+markers', name="Productivity", marker_color='#FFB86C', line=dict(width=3)),
        secondary_y=True,
    )
    
    fig_sleep_prod.update_layout(
        title_text="Sleep vs Productivity",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Inter", color="#A0A0B0")
    )
    fig_sleep_prod.update_xaxes(showgrid=False)
    fig_sleep_prod.update_yaxes(title_text="Sleep (hrs)", secondary_y=False, showgrid=False)
    fig_sleep_prod.update_yaxes(title_text="Productivity Score", secondary_y=True, showgrid=True, gridcolor='#2A2A3C')
    
    st.plotly_chart(fig_sleep_prod, use_container_width=True)

def plot_screentime_productivity(df):
    """Plot Screen Time vs Productivity relationship."""
    if len(df) < 2:
        return
        
    # Create an overlaid combo chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add Screen Time as a filled area/bar
    fig.add_trace(
        go.Bar(
            x=df['date'], 
            y=df['screen_time'], 
            name="Screen Time (hrs)", 
            marker_color='#FF6B6B',
            opacity=0.7,
            marker_line_width=0
        ),
        secondary_y=False,
    )
    
    # Add Productivity as a striking line
    fig.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['productivity'], 
            mode='lines+markers', 
            name="Productivity Score", 
            marker_color='#00FF87', 
            line=dict(width=4, shape='spline'), # Spline for smooth UI feel
            marker=dict(size=8, color='#FFFFFF', line=dict(width=2, color='#00FF87'))
        ),
        secondary_y=True,
    )
    
    fig.update_layout(
        title_text="Impact of Screen Time on Productivity",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Inter", color="#A0A0B0")
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text="Screen Time (hrs)", secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="Productivity Score (1-10)", secondary_y=True, showgrid=True, gridcolor='#2A2A3C')
    
    st.plotly_chart(fig, use_container_width=True)
