import streamlit as st
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QLOO_API_KEY = os.getenv("QLOO_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

# Qloo API setup
QLOO_API_URL = "https://hackathon.api.qloo.com/v2/insights/"
QLOO_HEADERS = {"X-Api-Key": QLOO_API_KEY}

# Valid Qloo entity types per documentation
VALID_ENTITY_TYPES = [
    "urn:entity:artist",
    "urn:entity:book",
    "urn:entity:brand",
    "urn:entity:destination",
    "urn:entity:movie",
    "urn:entity:person",
    "urn:entity:place",
    "urn:entity:podcast",
    "urn:entity:tv_show",
    "urn:entity:video_game"
]

# Streamlit UI
st.set_page_config(page_title="CultureHub", layout="wide")
st.title("CultureHub: Your Cultural Recommendation Hub")
st.markdown(
    "Select a use case and share your preferences to get personalized, privacy-first insights powered by Qloo's Taste AI™ and Google Gemini."
)

# Sidebar for use case selection
use_case = st.sidebar.selectbox(
    "Choose a Use Case",
    [
        "Plan a Trip (Travel Itinerary)",
        "Lifestyle Recommendations (Dining, Fashion, etc.)",
        "Discover Content (Books, Music, etc.)",
        "Predict Audience for a Product",
        "Personalize a Product Experience",
        "Research Cultural Trends"
    ],
    help="Select the type of recommendation or insight you want."
)

# Main input area
user_input = st.text_area(
    "Your Preferences or Goals",
    placeholder="e.g., I love jazz and Italian food, plan a trip to New Orleans; or Predict audience for a sci-fi podcast",
    height=150
)
submit = st.button("Generate Insights", type="primary")

# Helper function to query Qloo API
def query_qloo(params, retry=False):
    # Ensure filter.type and signal.interests.tags are comma-separated strings
    if isinstance(params.get("filter.type"), list):
        params["filter.type"] = ",".join(params["filter.type"])
    if isinstance(params.get("signal.interests.tags"), list):
        params["signal.interests.tags"] = ",".join(params["signal.interests.tags"])
    
    try:
        #st.write(f"Qloo API URL: {requests.Request('GET', QLOO_API_URL, headers=QLOO_HEADERS, params=params).prepare().url}")
        response = requests.get(QLOO_API_URL, headers=QLOO_HEADERS, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.HTTPError as e:
        if response.status_code == 403 and not retry:
            #st.warning("Qloo API access denied (403). Retrying with simplified parameters.")
            # Retry with minimal parameters
            simplified_params = {
                "filter.type": "urn:entity:place",
                "filter.location.query": params.get("filter.location.query", "New York City"),
                "signal.interests.tags": params["signal.interests.tags"].split(",")[0] if params.get("signal.interests.tags") else "culture"
            }
            return query_qloo(simplified_params, retry=True)
        elif response.status_code == 403:
            st.error("Qloo API access denied (403) after retry. Please check the API key or contact hackathon support (Discord/Devpost). Using fallback data.")
        else:
            st.warning(f"Qloo API error: {str(e)}. Using fallback data.")
        return []
    except requests.RequestException as e:
        st.warning(f"Qloo API error: {str(e)}. Using fallback data.")
        return []

# Use case-specific Qloo query templates
USE_CASE_QUERIES = {
    "Plan a Trip (Travel Itinerary)": {
        "filter.type": "urn:entity:place,urn:entity:destination",
        "signal.interests.tags": [],
        "filter.location.query": ""
    },
    "Lifestyle Recommendations (Dining, Fashion, etc.)": {
        "filter.type": "urn:entity:place,urn:entity:brand",
        "signal.interests.tags": []
    },
    "Discover Content (Books, Music, etc.)": {
        "filter.type": "urn:entity:book,urn:entity:artist,urn:entity:podcast,urn:entity:movie,urn:entity:tv_show",
        "signal.interests.tags": []
    },
    "Predict Audience for a Product": {
        "filter.type": "urn:entity:person",
        "signal.interests.tags": []
    },
    "Personalize a Product Experience": {
        "filter.type": "urn:entity:brand",
        "signal.interests.tags": []
    },
    "Research Cultural Trends": {
        "filter.type": "urn:entity:tag",
        "signal.interests.tags": []
    }
}

# Process request
if submit and user_input:
    with st.spinner("Generating your cultural insights..."):
        # Step 1: Use Gemini to parse input and build Qloo query
        prompt = f"""
        You are an intelligent cultural recommendation agent for Qloo's Taste AI API. The user selected the use case: "{use_case}".
        Their input is: "{user_input}".

        Instructions:
        1. Extract key preferences (e.g., music genres, cuisines, locations, product ideas).
        2. Determine Qloo API parameters based on the use case:
           - For 'Plan a Trip', use filter.type=urn:entity:place,urn:entity:destination and include filter.location.query (specific city, e.g., 'New York City' if 'USA' is input).
           - For 'Lifestyle Recommendations', use filter.type=urn:entity:place,urn:entity:brand.
           - For 'Discover Content', use filter.type=urn:entity:book,urn:entity:artist,urn:entity:podcast,urn:entity:movie,urn:entity:tv_show.
           - For 'Predict Audience', use filter.type=urn:entity:person.
           - For 'Personalize a Product', use filter.type=urn:entity:brand.
           - For 'Research Cultural Trends', use filter.type=urn:entity:tag.
        3. Suggest up to 2 specific tags for signal.interests.tags (e.g., 'jazz', 'Italian'). Avoid location-specific tags like 'French Quarter'.
        4. Ensure filter.type is a comma-separated string of valid types: {', '.join(VALID_ENTITY_TYPES)}.
        5. Ensure signal.interests.tags is a comma-separated string.
        6. Specify a response format (e.g., '5-day itinerary with daily activities, estimated costs, and transportation', 'bulleted list', 'audience profile').
        7. Output valid JSON with no extra text, comments, or trailing commas.

        Return:
        ```json
        {{
            "preferences": ["key1", "key2"],
            "qloo_params": {{
                "filter.type": "urn:entity:type1,urn:entity:type2",
                "filter.location.query": "specific city",
                "signal.interests.tags": "tag1,tag2"
            }},
            "response_format": "format description"
        }}
        ```

        Example for input "Plan a 5-day trip to USA" and use case "Plan a Trip":
        ```json
        {{
            "preferences": ["adventure", "history"],
            "qloo_params": {{
                "filter.type": "urn:entity:place,urn:entity:destination",
                "filter.location.query": "New York City",
                "signal.interests.tags": "adventure,history"
            }},
            "response_format": "5-day itinerary with daily activities, estimated costs, and transportation"
        }}
        ```
        """
        try:
            response = model.generate_content(prompt)
            json_text = re.search(r'```json\n(.*?)\n```', response.text, re.DOTALL)
            if json_text:
                agent_output = json.loads(json_text.group(1))
            else:
                raise ValueError("No valid JSON block found in Gemini response")
        except Exception as e:
            st.error(f"Error parsing Gemini response: {str(e)}. Using default parameters.")
            agent_output = {
                "preferences": ["culture", "history"],
                "qloo_params": USE_CASE_QUERIES[use_case].copy(),
                "response_format": "5-day itinerary with daily activities, estimated costs, and transportation" if use_case == "Plan a Trip (Travel Itinerary)" else "bulleted list of recommendations"
            }
            agent_output["qloo_params"]["filter.location.query"] = "New York City" if use_case == "Plan a Trip (Travel Itinerary)" else ""

        # Step 2: Build Qloo query
        qloo_params = USE_CASE_QUERIES[use_case].copy()
        qloo_params.update(agent_output["qloo_params"])
        if not qloo_params.get("signal.interests.tags") and agent_output["preferences"]:
            qloo_params["signal.interests.tags"] = ",".join(agent_output["preferences"][:2])  # Limit to 2 tags

        # Validate filter.type
        if qloo_params.get("filter.type"):
            types = qloo_params["filter.type"].split(",")
            valid_types = [t for t in types if t in VALID_ENTITY_TYPES]
            if not valid_types:
                qloo_params["filter.type"] = USE_CASE_QUERIES[use_case]["filter.type"]
            else:
                qloo_params["filter.type"] = ",".join(valid_types)

        # Step 3: Query Qloo API
        qloo_data = query_qloo(qloo_params)

        # Step 4: Generate final response with Gemini
        final_prompt = f"""
        You are a cultural insights expert. Based on the use case "{use_case}", user preferences "{user_input}",
        and Qloo API data:
        {json.dumps(qloo_data, indent=2)},
        generate a response in the format: {agent_output['response_format']}.

        Instructions:
        - Highlight affinity scores (0-100, >80 is very high, 60-80 is high, <50 is low).
        - Make it engaging, concise, and culturally insightful.
        - Emphasize Qloo’s privacy-first Taste AI for ethical personalization.
        - If Qloo data is empty, provide a fallback response based on preferences {agent_output['preferences']} and location {qloo_params.get('filter.location.query', 'New York City')}.
        - For 'Plan a Trip', format as a 5-day itinerary with daily activities, estimated costs, and transportation (e.g., walking, subway).
        - For other use cases, use a bulleted list or appropriate format (e.g., audience profile).
        """
        try:
            final_response = model.generate_content(final_prompt)
            output = final_response.text
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            output = f"Based on your preferences '{user_input}', we suggest exploring options in {qloo_params.get('filter.location.query', 'New York City')} for {use_case.lower()}."

        # Step 5: Display results with enhanced formatting
        st.subheader("Your Cultural Insights")
        st.markdown("---")
        if qloo_data:
            st.markdown(f"**Results powered by Qloo’s Taste AI (Affinity Scores: >80 Very High, 60-80 High, <50 Low)**")
            if use_case == "Plan a Trip (Travel Itinerary)":
                for day in range(1, 6):
                    with st.expander(f"Day {day}"):
                        st.markdown(output.split(f"**Day {day}")[1].split(f"**Day {day+1}")[0] if f"**Day {day}" in output else f"- Explore {qloo_params.get('filter.location.query', 'New York City')} (Affinity: 80).")
            else:
                st.markdown(output)
        else:
            st.warning(f"No specific Qloo data found. Here's a general recommendation for {qloo_params.get('filter.location.query', 'New York City')} based on your input:")
            if use_case == "Plan a Trip (Travel Itinerary)":
                for day in range(1, 6):
                    with st.expander(f"Day {day}"):
                        st.markdown(output.split(f"**Day {day}")[1].split(f"**Day {day+1}")[0] if f"**Day {day}" in output else f"- Explore {qloo_params.get('filter.location.query', 'New York City')} (Affinity: 80).")
            else:
                st.markdown(output)
        st.markdown("---")
        st.info("All insights are generated using Qloo’s privacy-first Taste AI, ensuring no personal data is required.")

# Footer
st.markdown(
    """
    ---
    Built for the Qloo LLM Hackathon. Powered by Qloo's Taste AI™ and Google Gemini. 
    Privacy-first cultural insights with no personal data required.
    """
)
