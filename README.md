🎥 Demo Video: https://drive.google.com/file/d/11vPdgGNy0Uu9NjOP0JA8etD41AiH1alD/view?usp=sharing


## Architecture Overview
This project was built as part of the NextYou Wellness RAG Micro-App Challenge to demonstrate the design of a safe, production-oriented RAG system for wellness applications.


This application is a full-stack Retrieval-Augmented Generation (RAG) micro-app designed for wellness-related queries, specifically focused on Yoga.

The system follows a clean, modular architecture with clear separation between the frontend, backend, RAG components, and database logging.

### High-Level Flow

1. The user enters a yoga-related question in the frontend UI.
2. The frontend sends the query to a FastAPI backend.
3. The backend passes the query to the RAG pipeline.
4. Relevant yoga knowledge is retrieved using semantic search.
5. The language model generates an answer grounded strictly in the retrieved content.
6. The final response, retrieved sources, and safety metadata are logged into MongoDB.
7. The answer is returned to the user along with its supporting sources.

### Core Components

- **Frontend**
  - Simple web interface for asking yoga-related questions
  - Displays answers along with retrieved knowledge sources

- **Backend (FastAPI)**
  - Handles API requests from the frontend
  - Coordinates the RAG pipeline
  - Applies safety checks for wellness-related queries
  - Logs all interactions to MongoDB

- **RAG Engine**
  - Loads a structured yoga knowledge base (JSON)
  - Generates embeddings using a sentence-transformer model
  - Performs semantic retrieval using FAISS
  - Supplies grounded context to the language model

- **Database (MongoDB)**
  - Stores user queries
  - Stores retrieved knowledge chunks
  - Stores generated responses
  - Stores safety flags and timestamps for observability


## RAG Pipeline Design

The application uses a Retrieval-Augmented Generation (RAG) pipeline to ensure responses are grounded in a trusted yoga knowledge base rather than relying on model hallucinations.

### Knowledge Base
- The knowledge base is stored as structured JSON documents.
- Each document contains:
  - An `id`
  - A `title`
  - A `text` field describing a specific yoga concept, practice, or guideline.

### Chunking Strategy
- Each yoga article is treated as a single semantic chunk.
- Given the small and well-scoped nature of the dataset, additional sub-chunking was not required.
- This keeps retrieval simple and avoids loss of semantic meaning.

### Embeddings
- Text embeddings are generated using the `all-MiniLM-L6-v2` sentence-transformer model.
- To improve retrieval accuracy, both the document title and content are embedded together.
- This ensures better matching for specific yoga practices (e.g., Surya Namaskar).

### Vector Search & Retrieval
- Embeddings are indexed using FAISS for efficient semantic similarity search.
- For each user query, the system retrieves the top-k most relevant documents.
- Retrieved documents are selected purely based on semantic similarity, not keywords.

### Augmented Generation
- The retrieved yoga documents are passed as context to the language model.
- The model is instructed to generate answers strictly based on this retrieved context.
- This grounding approach significantly reduces hallucinations and improves factual reliability.

### Runtime Design Choice
- Embeddings are generated in-memory at application startup.
- This design avoids stale indexes during rapid iteration and keeps the system simple for a micro-app use case.


## Safety Logic for Wellness Queries

Since the application operates in the wellness domain, special care is taken to handle sensitive or health-related queries responsibly.

### Safety Detection
- Each user query is evaluated to determine whether it may involve medical, mental health, or sensitive wellness advice.
- Examples include queries related to curing diseases, replacing medical treatment, or diagnosing mental health conditions.

### Safety Flagging
- The backend assigns a boolean safety flag (`isUnsafe`) to each query.
- This flag allows the system to differentiate between general wellness questions and potentially sensitive requests.

### Safe Response Handling
- When a query is flagged as unsafe, the system avoids providing medical diagnoses or prescriptive advice.
- Responses are framed with appropriate disclaimers and focus on general wellness support rather than treatment claims.
- Users are gently encouraged to consult qualified healthcare professionals when appropriate.

### Design Rationale
- This safety layer helps prevent misuse of the application for medical decision-making.
- It ensures that yoga is presented as a supportive wellness practice, not a substitute for professional medical care.


## Logging & Observability

To support transparency, debugging, and future improvements, the application logs all interactions using MongoDB.

### What Is Logged
For every user query, the following information is stored:
- The original user query
- Retrieved knowledge sources used for answering
- The generated response
- Safety flag (`isUnsafe`)
- Timestamp of the interaction

### Purpose of Logging
- Enables auditing of responses generated by the RAG system
- Helps analyze retrieval quality and safety behavior
- Supports monitoring of potentially sensitive wellness queries
- Provides a foundation for future analytics and system improvements

### Implementation Details
- MongoDB is used as the logging database due to its flexibility with semi-structured data.
- Database credentials are managed securely using environment variables.
- A `.env.example` file is provided to document required configuration without exposing secrets.

## Future Improvements
- Persistent vector storage for larger knowledge bases
- More advanced safety classification using LLM-based moderation
