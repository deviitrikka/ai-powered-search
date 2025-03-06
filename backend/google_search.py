import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key and Search Engine ID from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
    raise ValueError("Missing GOOGLE_API_KEY or GOOGLE_CSE_ID in environment variables")

def google_search(query, num_results=5):
    """Fetch Google search results using Google's Custom Search API."""
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "num": num_results,
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract search results
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            })

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google search results: {e}")
        return []
