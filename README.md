# Member Data Q&A System

A semantic search-based question answering system that helps you find information about member data using natural language queries. This system uses embeddings and similarity matching to understand questions and retrieve relevant member information.

## Deployment

Cureently it is deployed on Streamlit Cloud platform for the frontend and the backend is deployed on Render.
- **Application Link**: https://member-app-system-ak.streamlit.app/
- **Backend Check**: https://member-qa-system-1.onrender.com/health
  
## Features

- **Semantic Search**: Utilizes transformer-based embeddings to capture context and meaning.
- **Natural Language Processing**: Ask questions in plain English
- **Confidence Scoring**: Every answer has a confidence score based on semantic similarity.
- **Question History**: Track all your queries and answers
- **FastAPI Backend**: High-performance REST API
- **Streamlit Frontend**: Beautiful, interactive user interface
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **No API Keys Required**: Everything runs locally with semantic search

## How It Works

### Semantic Search Process
1. **Question Encoding**: Your question is converted into a semantic embedding using a transformer model
2. **Data Matching**: The system compares your question embedding with member data embeddings
3. **Ranking**: Results are ranked by cosine similarity score (0-1)
4. **Answer Generation**: Top matching member data is formatted and returned with confidence scores

## Quick Start

### Using Docker (Recommended)

In the Dockerfile change the localhost from 10000 to 8501 as currently it is set to the port where I have deployed it.

\`\`\`bash
docker-compose up --build
\`\`\`

Then open:
- Frontend: http://localhost:8501
- API: http://localhost:8000/health

### Local Setup

**Prerequisites**: Python 3.11+

1. **Create virtual environment**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

2. **Install dependencies**
\`\`\`bash
pip install -r streamlit_requirements.txt
pip install -r requirements.txt
\`\`\`

3. **Start backend** (Terminal 1)
\`\`\`bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
\`\`\`

4. **Start frontend** (Terminal 2)
\`\`\`bash
streamlit run streamlit_app.py
\`\`\`

## API Documentation

### Endpoints

#### Ask Question
**POST** `/ask`

Request:
\`\`\`json
{
  "question": "What are the member travel plans?"
}
\`\`\`

Response:
\`\`\`json
{
  "answer": "Layla: Planning trip to London\n- ...",
  "confidence": 0.85,
  "sources": ["Layla", "..."]
}
\`\`\`

## Example Questions

Try asking:
- "Which seat Layla prefers in flight?"
- "What is the new emegency contact number of Amina?"
- "Hans need how many front row tickets ?"
- "Who wants to fly to Tokyo?"

## Project Structure

- **streamlit_app.py**              # Streamlit frontend
- **streamlit_requirements.txt**    # Frontend dependencies
- **app.py**                        # FastAPI backend
- **requirements.txt**               # Backend dependencies
- **docker-compose.yml**            # Docker Compose configuration
- **Dockerfile**                    # Backend Docker image
- **README.md**                     # This file   

## Performance Notes

- **First request**: ~30-60 seconds (model loading)
- **Subsequent requests**: ~1-3 seconds
- **Confidence score**: 0-1 (higher = better match)
- **Recommended threshold**: 0.3+ for reasonable results

## Technologies Used

- **FastAPI**: Modern Python web framework
- **Streamlit**: Data app framework
- **Sentence Transformers**: Semantic embeddings
- **PyTorch**: Deep learning
- **Docker**: Containerization

## Troubleshooting

# Check if backend is running
curl https://member-qa-system-1.onrender.com/health
\`\`\`

### Semantic Search Not Finding Results
- Try simpler question phrasing
- Lower confidence threshold in Streamlit settings
- Check member data format in API

## Alternate Solution Possible

**LARGE LANGUAGE MODELS (LLM) - Claude/GPT**

### What It Is
Uses pre-trained large language models from providers like OpenAI (GPT), Anthropic (Claude), or open-source models to understand and answer questions.

### How It Works

Question: "When is Layla planning her trip to London?"
    **->**
Send to Claude/GPT with member data context
    **->**
Model reasons about the context
    **->**
Generates natural language answer
    **->**
Return formatted response

### Pros
- Most human-like responses
- Understands complex context
- Can reason and infer
- Handles variations naturally
- Single API call
- Very flexible

### Cons
- Uses API key, paid subscription required
- Network latency (500ms-3s per request)
- API costs ($0.01-$0.10 per request)
- Data privacy concerns
- Can hallucinate/make up information
- Less transparent

## Why Semantic Search Instead of LLM?

| Aspect | Semantic Search | LLM (Claude/GPT) |
|--------|-----------------|------------------|
| **Cost** | Free | API charges per request |
| **Speed** | Fast (1-3s) | Slower (3-10s+) |
| **Setup** | No API keys | Requires API key |
| **Transparency** | Clear matching process | Black box inference |
| **Privacy** | Data stays local | Sent to external API |
| **Assessment Fit** | Shows NLP understanding | Shows API integration |

## Anomalies In Member Data

- **Duplicated Member Names**: Several users show up more than once (e.g., the same name with slightly different messages).
Impact: For those users, redundant embeddings lead to biassed similarity results.

- **Unreliable Text Formatting**: There is mixed capitalisation across entries (e.g., “book a Flight” vs “Book a flight”).
Impact: The model interprets these as distinct tokens, which slightly reduces embedding quality.

- **Language and Tone Variation**: Some use shorthand or incomplete phrases.
Impact: Results may be ranked incorrectly by semantic similarity scores because of partial or cross-lingual context.

## License

MIT License

## Support

For issues or questions, review the README, or check console logs in both frontend and backend.
