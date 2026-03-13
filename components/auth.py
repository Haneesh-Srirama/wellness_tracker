import streamlit as st
from database.db import get_connection

# List of typical Indian names
INDIAN_NAMES = [
    "Aarav Patel", "Vihaan Sharma", "Aditya Singh", "Sai Kumar", "Arjun Reddy",
    "Priya Sharma", "Diya Patel", "Ananya Singh", "Neha Gupta", "Kavya Reddy",
    "Rahul Verma", "Karan Malhotra", "Rohan Das", "Vikram Singh", "Amit Kumar",
    "Sneha Rao", "Riya Mishra", "Pooja Joshi", "Vanya Agarwal", "Ishaan Kapoor",
    "Kabir Bose", "Vivaan Chatterjee", "Krishna Iyer", "Siddharth Nair", "Pranav Menon",
    "Aanya Desai", "Aarohi Kulkarni", "Meera Pillai", "Sanya Ahuja", "Naina Kaur",
    "Aditi Yadav", "Rishi Nath", "Ravi Teja", "Swati Nandi", "Karthik Subramanian"
]

def get_user_mapping():
    """Fetch all unique usernames and deterministically map them to an Indian name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users ORDER BY username")
    users = [row['username'] for row in cursor.fetchall()]
    conn.close()
    
    # Deterministic mapping based on the user ID string
    mapping = {}
    for i, user in enumerate(users):
        name = INDIAN_NAMES[i % len(INDIAN_NAMES)]
        mapping[user] = f"{name} (ID: {user})"
    
    return users, mapping

def authenticate():
    """Authentication using loaded Fitabase User IDs."""
    st.sidebar.title("Login Context")
    
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'user_display_name' not in st.session_state:
        st.session_state['user_display_name'] = None

    users, user_mapping = get_user_mapping()
    
    if st.session_state['username'] is None:
        if not users:
            st.sidebar.error("No data available. Please run `python database/import_fitabase.py` first.")
            return None
            
        with st.sidebar.form("login_form"):
            selected_user = st.selectbox(
                "Select User", 
                options=users, 
                format_func=lambda x: user_mapping[x]
            )
            submitted = st.form_submit_button("Load User Data")
            if submitted:
                st.session_state['username'] = selected_user
                # Store the clean name without the ID suffix for UI greeting
                st.session_state['user_display_name'] = user_mapping[selected_user].split(" (")[0]
                st.rerun()
        return None
    else:
        display_name = st.session_state.get('user_display_name', st.session_state['username'])
        st.sidebar.write(f"Viewing data for: **{display_name}**\n\n*(ID: {st.session_state['username']})*")
        if st.sidebar.button("Logout / Switch User"):
            st.session_state['username'] = None
            st.rerun()
        return st.session_state['username']
