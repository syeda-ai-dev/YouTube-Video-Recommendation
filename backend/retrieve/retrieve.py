import os
import json
from tavily import TavilyClient
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

def get_recommendation(keyword: str):
    search_results = tavily_client.search(
        query=f"best youtube videos about {keyword}",
        search_depth="advanced",
        max_results=5
    )

    prompt = f"""Based on the search results for '{keyword}', provide exactly 1 relevant YouTube video.
    Context: {search_results}

    IMPORTANT: Return ONLY a valid JSON array containing exactly 1 video.
    The video must have:
    - A 'title' field with the video title (no special characters)
    - A 'video_id' field with exactly 11 characters from the YouTube URL

    Return in this exact format:
    [
        {{"title": "Video Title 1", "video_id": "xxxxxxxxxxx"}}
    ]"""

    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that returns clean JSON arrays. Avoid special characters in titles. Ensure video_ids are exactly 11 characters."
                },
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.1,
            max_tokens=1000
        )

        response_text = completion.choices[0].message.content.strip()
        response_text = response_text.replace("```json", "").replace("```", "").strip()

        recommendations = json.loads(response_text)
        if recommendations and isinstance(recommendations, list):
            rec = recommendations[0]
            if 'video_id' in rec and 'title' in rec and len(rec['video_id']) == 11:
                video_url = f"https://youtu.be/{rec['video_id']}"
                return {
                    "title": rec['title'],
                    "video_url": video_url
                }
        return {}

    except Exception as e:
        return {"error": str(e)}
