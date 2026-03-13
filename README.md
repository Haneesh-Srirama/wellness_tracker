# Wellness Tracker Web App 🌿

A comprehensive wellness tracker built with **Streamlit** that allows users to manually monitor their daily health metrics, detect patterns, and receive AI-driven insights via the **Gemini API**.

## Features

- **User Authentication:** Select an available user ID from the datasets using the sidebar dropdown.
- **Automated Data Integration:** Loads real wellness user metrics directly from Fitabase CSV datasets instead of requiring manual input. Tracks daily Steps, Calories, Heart Rate, Screen Time, Sleep Hours, and Productivity on a 1-10 scale.
- **Dashboard & Analytics:** Interactive Plotly charts showing your trends over time, alongside a correlation heatmap to help reveal patterns.
- **AI Insights & Alerts:** Automated pattern analysis alerting you of low sleep or unusual resting heart rates, plus a dedicated AI chatbot powered by the **Gemini 2.5 Flash API** to answer specific questions regarding your health context.

## Local Setup

1. **Navigate to the core directory:**
   ```bash
   cd wellness_tracker
   ```
2. **Setup Virtual Environment:**
   *(Optional but recommended)*
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables:**
   Create a `.env` file in the root directory (`wellness_tracker`) and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
5. **Load the Fitabase Datasets into the Database:**
   *(Make sure your Fitabase CSV folders are located in this directory)*
   ```bash
   python database/import_fitabase.py
   ```
6. **Run the App:**
   ```bash
   streamlit run app.py
   ```

## Deployment on Streamlit Cloud

1. Commit and push your local repository to a platform like GitHub.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and create a new app linked to your repository.
3. Set the **Main file path** to `app.py`.
4. In the Streamlit app's advanced settings (on your cloud dashboard), add your Gemini API key to your **Secrets**:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key"
   ```
   The application is already configured to automatically default to Streamlit secrets (`st.secrets`) if the `.env` variable is not found in production environments.

## File Structure

- `app.py`: Main Streamlit web application.
- `database/db.py`: Connects and initializes SQLite databases.
- `database/crud.py`: Functions to write and fetch tracking data.
- `components/`: UI wrappers like `auth.py` and `input_form.py`.
- `modules/`: Contains business logic for `analysis.py`, `visualization.py`, and `chatbot.py`.
