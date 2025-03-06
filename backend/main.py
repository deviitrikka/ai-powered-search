from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from google_search import google_search  # Import Google search function
from youtube_search import youtube_search  # Import YouTube search function
from linkedin_search import search_linkedin_jobs
 # Import LinkedIn search function

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set CORS for frontend communication
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://ai-powered-search-iota.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set API Key for Groq securely
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY in environment variables")

class QueryGenerator:
    def __init__(self):
        """Initialize the LLM model with Groq API"""
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile"
        )

    def generate_queries(self, search_query):
        """Generate relevant search queries based on the user input"""

        # Define the prompt
        prompt_template = PromptTemplate.from_template(
            """
            ### USER SEARCH QUERY:
            {search_query}

            ### INSTRUCTION:
            Generate **5 relevant and diverse search queries** based on the given user query.
            The queries should be **semantically similar** but **cover different aspects** of the topic.

            ### OUTPUT FORMAT:
            Return the queries in **valid JSON format** like this:
            ```json
            {{"queries": [
                "Alternative search query 1",
                "Alternative search query 2",
                "Alternative search query 3",
                "Alternative search query 4",
                "Alternative search query 5"
            ]}}
            ```
            """
        )

        # Combine prompt and LLM
        chain = prompt_template | self.llm

        try:
            # Invoke the AI model
            response = chain.invoke({"search_query": search_query})
            raw_output = response.content.strip()

            # Extract JSON from response manually
            json_start = raw_output.find("{")
            json_end = raw_output.rfind("}") + 1
            formatted_json = raw_output[json_start:json_end]

            # Convert string to dictionary
            import json
            parsed_data = json.loads(formatted_json)

            return parsed_data  # Should return {"queries": [...]}

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing AI response: {str(e)}")

# Initialize Query Generator
query_gen = QueryGenerator()

@app.get("/relevant_queries/")
async def get_relevant_queries(query: str = Query(..., title="Search Query")):
    """API Endpoint to fetch AI-generated relevant queries"""
    try:
        generated_queries = query_gen.generate_queries(query)
        return {"queries": generated_queries.get("queries", [])}  # Fixed response key

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/google_search/")
async def get_google_results(query: str = Query(..., title="Search Query")):
    """API Endpoint to fetch Google search results"""
    try:
        results = google_search(query)
        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/youtube_search/")
async def get_youtube_results(query: str = Query(..., title="Search Query")):
    """API Endpoint to fetch YouTube search results"""
    try:
        results = youtube_search(query)
        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/linkedin_search/")
async def get_jobs(query: str = Query(..., description="Job search query")):
    """Endpoint to search for LinkedIn jobs based on the query."""
    try:
        jobs = search_linkedin_jobs(query)
        return {"jobs": jobs}  # Ensure the response key is "jobs"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
     
@app.get("/")
async def welcome():
    return {"message": "hi"}  # Return a dictionary (FastAPI converts it to JSON)

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
