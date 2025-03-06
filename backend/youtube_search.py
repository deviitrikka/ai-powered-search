import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def youtube_search(query, max_results=5):
    """Fetch YouTube search results based on the query."""
    try:
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "key": YOUTUBE_API_KEY,
            "maxResults": max_results,
            "type": "video",
        }
        response = requests.get(search_url, params=params)
        response.raise_for_status()

        data = response.json()
        videos = []

        for item in data.get("items", []):
            video_info = {
                "title": item["snippet"]["title"],
                "videoId": item["id"]["videoId"],
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "channelTitle": item["snippet"]["channelTitle"],
            }
            videos.append(video_info)

        return videos

    except Exception as e:
        return {"error": str(e)}
