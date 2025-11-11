from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import requests
import numpy as np
from typing import List, Optional

app = FastAPI(title="Question Answering API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the semantic model
model = SentenceTransformer('all-MiniLM-L6-v2')

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str] = []

# Store member data in memory with embeddings
member_data = []
member_embeddings = None

def fetch_member_data():
    """Fetch member data from the public API"""
    global member_data, member_embeddings
    try:
        response = requests.get("https://november7-730026606190.europe-west1.run.app/messages")
        # Adjust the URL to your actual public API endpoint
        # This is a placeholder - replace with your actual API
        if response.status_code == 200:
            data = response.json()
            member_data = data.get("items", [])
            # Create embeddings for all member data
            member_texts = [f"{item.get('user_name', '')}: {item.get('message', '')}" for item in member_data]
            member_embeddings = model.encode(member_texts, convert_to_tensor=True)
            return True
    except Exception as e:
        print(f"Error fetching data: {e}")
    return False

@app.on_event("startup")
async def startup_event():
    """Load member data on startup"""
    fetch_member_data()

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Answer a question using semantic search over member data"""
    if not member_data or member_embeddings is None:
        raise HTTPException(status_code=503, detail="Member data not loaded")
    
    # Encode the question
    question_embedding = model.encode(request.question, convert_to_tensor=True)
    
    # Compute similarity scores
    similarity_scores = util.pytorch_cos_sim(question_embedding, member_embeddings)
    
    # Get top 3 most similar results
    top_k = 3
    top_indices = np.argsort(-similarity_scores[0].cpu().numpy())[:top_k]
    
    # Build answer from most relevant results
    relevant_items = [member_data[i] for i in top_indices if similarity_scores[0][i] > 0.3]
    
    if not relevant_items:
        return AnswerResponse(
            answer="I couldn't find relevant information to answer this question.",
            confidence=0.0
        )
    
    # Format answer
    answer_parts = []
    sources = []
    for item in relevant_items:
        answer_parts.append(f"- {item.get('user_name', '')}: {item.get('message', '')}")
        sources.append(f"{item.get('user_name', '')}: {item.get('message', '')}")
    
    answer = str(answer_parts[0])
    confidence = float(similarity_scores[0][top_indices[0]].cpu().numpy())
    
    return AnswerResponse(
        answer=answer,
        confidence=confidence,
        sources=sources
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
