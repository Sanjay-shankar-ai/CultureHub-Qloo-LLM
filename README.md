# CultureHub: Your Cultural Recommendation Hub

CultureHub is a Streamlit web application developed for the **Qloo LLM Hackathon** (August 1, 2025). It delivers personalized, privacy-first cultural insights using **Qloo’s Taste AI™** and **Google Gemini (gemini-2.5-pro)**. Users select a use case (e.g., Plan a Trip, Discover Content) and input preferences (e.g., “I love jazz and Italian food, plan a trip to New Orleans”) to receive tailored outputs like travel itineraries, lifestyle recommendations, or audience profiles.


## Features

- **Six Use Cases**:
  - Plan a Trip (Travel Itinerary)
  - Lifestyle Recommendations (Dining, Fashion, etc.)
  - Discover Content (Books, Music, etc.)
  - Predict Audience for a Product
  - Personalize a Product Experience
  - Research Cultural Trends
- **Qloo Taste AI Integration**: Queries Qloo’s Insights API for recommendations across:
  - **Music**: Artists, albums, songs (`urn:entity:artist`)
  - **Dining**: Restaurants, cafes, bakeries (`urn:entity:place`)
  - **Television**: TV series, presenters, networks (`urn:entity:tv_show`, `urn:entity:person`)
  - **Sports**: Athletes, teams, stadiums (`urn:entity:person`, `urn:entity:place`)
  - **Products**: Products, brands, companies (`urn:entity:brand`)
  - **Books**: Authors, books, publishers (`urn:entity:book`, `urn:entity:person`)
- **Google Gemini Powered**: Leverages `gemini-2.5-pro` for parsing user inputs, constructing Qloo queries, and generating engaging responses.
- **Privacy-First**: Utilizes Qloo’s ethical, no-personal-data-required approach for recommendations.
- **Polished UI**: Streamlit interface with collapsible itineraries for travel plans and clear affinity score displays (>80 very high, 60-80 high, <50 low).
- **Robust Error Handling**: Manages Qloo API 403 errors with retries and fallbacks, and robust JSON parsing to prevent `ValueError`.

## Prerequisites

- Python 3.8+
- [Google Gemini API key](https://makersuite.google.com/)
- [Qloo API key](https://hackathon.qloo.com/) (provided by hackathon organizers)
- GitHub repository for deployment

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/culturehub.git
   cd culturehub
   ```

2. **Install Dependencies**:
   ```bash
   pip install streamlit google-generativeai requests python-dotenv
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root:
   ```bash
   echo -e "GEMINI_API_KEY=your-gemini-api-key\nQLOO_API_KEY=your-qloo-api-key" > .env
   ```

## Usage

1. **Run the Application Locally**:
   ```bash
   streamlit run app.py
   ```

2. **Interact with the App**:
   - Open the app in your browser (`http://localhost:8501`).
   - Select a use case from the sidebar (e.g., “Plan a Trip (Travel Itinerary)”).
   - Enter preferences in the text area (e.g., “I love jazz and Italian food, plan a trip to New Orleans”).
   - Click **Generate Insights** to view personalized recommendations.

3. **Test Cases**:
   Try these inputs to test each use case:
   - **Plan a Trip**: “Plan a 5-day trip to Paris with a focus on art.”
     - **Expected**: 5-day itinerary with activities (e.g., Louvre, Musée d’Orsay), costs, and transportation.
   - **Lifestyle Recommendations**: “Recommend trendy restaurants in Tokyo.”
     - **Expected**: List of restaurants (e.g., Sushi Saito, Affinity: 90).
   - **Discover Content**: “Suggest sci-fi books and music.”
     - **Expected**: List of books (e.g., *Dune*) and artists (e.g., Vangelis).
   - **Predict Audience**: “Who is the target audience for eco-friendly sneakers?”
     - **Expected**: Audience profile (e.g., 18-35-year-olds, sustainability-focused).
   - **Personalize a Product**: “Personalize a smartwatch for a fitness enthusiast.”
     - **Expected**: Customization suggestions (e.g., heart rate monitor).
   - **Research Cultural Trends**: “What are trending music genres in Miami?”
     - **Expected**: List of trends (e.g., Latin Pop, Hip-Hop).



<p align="center">
  Built for the Qloo LLM Hackathon. Powered by Qloo's Taste AI™ and Google Gemini.
</p>
