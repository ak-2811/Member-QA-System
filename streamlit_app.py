import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Member Q&A System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stTitle {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .answer-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #f0f7ff;
        border-left: 4px solid #1f77b4;
    }
    .confidence-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Member Data Q&A System")
    st.markdown("*Ask questions about member information using semantic search*")

# Initialize session state
if "question_history" not in st.session_state:
    st.session_state.question_history = []
if "api_status" not in st.session_state:
    st.session_state.api_status = False

# Sidebar Configuration
with st.sidebar:
    st.header("Settings")
    
    # API Configuration
    st.subheader("API Configuration")
    api_url = st.text_input(
        "API Endpoint URL",
        value="https://member-qa-system-1.onrender.com",
        help="Enter the backend API URL (default: localhost:10000)"
    )
    
    # Test connection
    if st.button("Test Connection", key="test_conn"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                st.success("Connected to API successfully!")
                st.session_state.api_status = True
            else:
                st.error(f"API returned status code: {response.status_code}")
        except Exception as e:
            st.error(f"Cannot connect to API: {str(e)}")
    
    st.markdown("---")
    
    # Example Questions
    st.subheader("Example Questions")
    st.markdown("""
    Try asking questions like:
    - Which seat Layla prefers in flight?
    - What is the new emegency contact number of Amina?
    - Hans need how many front row tickets ?
    - Who wants to fly to Tokyo?
    """)
    
    st.markdown("---")
    
    # Advanced Options
    st.subheader("Advanced Option")
    min_confidence = st.slider(
        "Minimum Confidence Threshold",
        min_value=0.3,
        max_value=1.0,
        value=0.3,
        step=0.05,
        help="Filter results by confidence score"
    )
    

# Main Content Area
st.markdown("---")

# Question Input Section
st.subheader("Ask Your Question")
col1, col2 = st.columns([4, 1])

with col1:
    user_question = st.text_input(
        "Enter your question:",
        placeholder="e.g., What are the travel plans for members?",
        key="question_input"
    )

with col2:
    submit_button = st.button("Search", type="primary", use_container_width=True)

# Process Question
if submit_button and user_question:
    if not st.session_state.api_status:
        st.warning("Testing API connection first...")
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            st.session_state.api_status = True
        except:
            st.error(f"Cannot connect to API at {api_url}. Please check if the backend is running.")
            st.stop()
    
    with st.spinner("Searching member data using semantic search..."):
        try:
            response = requests.post(
                f"{api_url}/ask",
                json={"question": user_question},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "No answer found")
                confidence = result.get("confidence", 0.0)
                sources = result.get("sources", [])
                
                # Check confidence threshold
                if confidence < min_confidence:
                    st.warning(f"Answer confidence ({confidence:.2%}) is below threshold ({min_confidence:.0%}). Result may not be relevant.")
                
                # Display Results
                st.markdown("---")
                st.subheader("Results")
                
                # Confidence Badge
                confidence_color = "green" if confidence > 0.7 else "orange" if confidence > 0.4 else "red"
                st.markdown(
                    f"""<div class="confidence-badge" style="background-color: {confidence_color}20; border: 1px solid {confidence_color};">
                    Confidence: {confidence:.1%}
                    </div>""",
                    unsafe_allow_html=True
                )
                
                # Answer Box
                st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
                
                # Sources
                if sources:
                    with st.expander("View Sources"):
                        for source in sources:
                            st.write(f"• {source}")
                
                # Add to history
                st.session_state.question_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "question": user_question,
                    "answer": answer,
                    "confidence": confidence
                })
                
                st.success("Answer retrieved successfully!")
                
            else:
                st.error(f"API Error: {response.status_code}")
                try:
                    error_detail = response.json()
                    st.error(f"Details: {error_detail.get('detail', 'Unknown error')}")
                except:
                    st.error(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error(f"Cannot connect to API at {api_url}. Make sure the backend is running.")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The API took too long to respond.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# History Section
st.markdown("---")
st.subheader("Question History")

if st.session_state.question_history:
    col1, col2 = st.columns([4, 1])
    
    with col2:
        if st.button("Clear History", key="clear_history"):
            st.session_state.question_history = []
            st.rerun()
    
    # Display history
    for i, item in enumerate(reversed(st.session_state.question_history), 1):
        with st.expander(f"#{len(st.session_state.question_history) - i + 1} - {item['question'][:60]}..."):
            st.write(f"**Time:** {item['timestamp']}")
            st.write(f"**Question:** {item['question']}")
            st.write(f"**Confidence:** {item['confidence']:.1%}")
            st.markdown(f"**Answer:** {item['answer']}")
else:
    st.info("No questions asked yet. Start by asking a question above!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px;">
    Member Data Q&A System | Powered by Semantic Search | Made with Streamlit
</div>
""", unsafe_allow_html=True)
