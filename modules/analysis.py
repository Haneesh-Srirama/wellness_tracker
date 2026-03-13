import pandas as pd

def generate_insights(df):
    """Analyze the dataframe and generate friendly, conversational suggestions."""
    if df.empty:
        return ["👋 Hey there! It looks like there's no data yet. Let's get some tracking going!"]

    insights = []
    
    # Sort chronologically just in case
    df = df.sort_values(by='date')
    latest = df.iloc[-1]
    
    # 1. Alert for sleep < 8 hours today
    if latest['sleep_hours'] < 7:
        insights.append(f"😴 **Sleep check!** You got about {round(latest['sleep_hours'], 1)} hours of rest. Try winding down a bit earlier tonight to help recharge your energy and productivity tomorrow!")
    elif latest['sleep_hours'] >= 8:
        insights.append(f"🌟 **Great sleep!** You locked in {round(latest['sleep_hours'], 1)} hours of rest. You should be feeling pretty sharp today!")
    
    # 2. Activity / Steps
    if latest['steps'] > 10000:
        insights.append(f"🔥 **Fantastic!** You crushed your step goal with {int(latest['steps'])} steps. Keep the momentum going!")
    elif latest['steps'] < 5000:
        insights.append(f"🚶 **Moving more:** Your step count was {int(latest['steps'])} recently. Try taking a short 15-minute walk to boost your circulation and mood!")

    # 3. Anomaly: High heart rate vs low activity
    if latest['heart_rate'] > 85 and latest['steps'] < 4000:
        insights.append(f"💓 **Heart rate check:** Your resting heart rate seemed a bit elevated ({int(latest['heart_rate'])} bpm) while your steps were on the lower side. Make sure to stay hydrated and take a moment to breathe and destress!")
        
    # Pattern Analysis (requires a few days of data to be meaningful)
    if len(df) >= 3:
        # Sleep vs Productivity
        corr_sleep_prod = df['sleep_hours'].corr(df['productivity'])
        if pd.notna(corr_sleep_prod):
            if corr_sleep_prod > 0.4:
                insights.append("💡 **Did you notice?** There's a clear pattern showing that when you get better sleep, your productivity scores consistently shoot up! Keep prioritizing that rest.")
            elif corr_sleep_prod < -0.4:
                insights.append("⚖️ **Finding balance:** It looks like your productivity has been fighting against your sleep lately. Remember that long-term focus requires good rest!")
            
        # Screen time vs Sleep
        corr_screen_sleep = df['screen_time'].corr(df['sleep_hours'])
        if pd.notna(corr_screen_sleep):
            if corr_screen_sleep < -0.4:
                insights.append("📱 **Screen time tip:** The data shows that higher screen time might be cutting into your sleep duration. Maybe try a digital sunset 30 minutes before bed?")
            
    if not insights:
        insights.append("🏆 **You're doing amazing!** All of your recent metrics look nicely balanced. Keep up the great work!")
        
    return insights
