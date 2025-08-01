# CultureHub: Your Cultural Recommendation Hub
CultureHub is a Streamlit web application built for the Qloo LLM Hackathon, delivering personalized, privacy-first cultural insights using Qloo’s Taste AI™ and Google Gemini (gemini-2.5-pro). Users select a use case (e.g., Plan a Trip, Discover Content) and input preferences (e.g., “I love jazz and Italian food, plan a trip to New Orleans”) to receive tailored recommendations, such as travel itineraries, lifestyle suggestions, or audience profiles.


#Features

Six Use Cases: Supports Plan a Trip, Lifestyle Recommendations, Discover Content, Predict Audience, Personalize a Product, and Research Cultural Trends.
Qloo Taste AI Integration: Queries Qloo’s Insights API for culturally relevant recommendations across music (artists), dining (restaurants, cafes), television (TV series, presenters), sports (athletes, stadiums), products (brands), and books (authors, books).
Google Gemini Powered: Uses gemini-2.5-pro to parse user inputs, build Qloo queries, and generate engaging responses.
Privacy-First: Emphasizes Qloo’s ethical, no-personal-data-required approach.
Polished UI: Streamlit interface with collapsible itineraries for travel plans and clear affinity score displays (>80 very high, 60-80 high, <50 low).
Error Handling: Manages Qloo API 403 errors with retries and fallbacks, and robust JSON parsing to avoid ValueError.


# Installation

## Clone the Repository:
git clone https://github.com/your-username/culturehub.git
cd culturehub


## Install Dependencies:
pip install streamlit google-generativeai requests python-dotenv


## Set Up Environment Variables:Create a .env file in the project root and add:
GEMINI_API_KEY=your-gemini-api-key
QLOO_API_KEY=your-qloo-api-key


# Usage

## Run the Application Locally:
streamlit run app.py


## Interact with the App:

Open the app in your browser (typically http://localhost:8501).
Select a use case from the sidebar (e.g., “Plan a Trip (Travel Itinerary)”).
Enter preferences in the text area (e.g., “I love jazz and Italian food, plan a trip to New Orleans”).
Click “Generate Insights” to view personalized recommendations.


Built for the Qloo LLM Hackathon. Powered by Qloo's Taste AI™ and Google Gemini.
