# Demo script (90-180s)

1. Intro (10s)
   - "This demo shows a lightweight E-commerce recommender with LLM-powered explanations."

2. Start server (20s)
   - `uvicorn backend.app.main:app --reload`
   - Show log that server started.

3. Seed & Request (40s)
   - `curl -X POST http://localhost:8000/seed`
   - `curl "http://localhost:8000/recommendations?user_id=demo_user&k=5"`
   - Show JSON response (products with `why` explanations).

4. Frontend (20s)
   - Open `frontend/index.html` in a browser and show interactive request for `demo_user`.

5. Closing (10s)
   - Summarize architecture and next steps (caching, supervised reranker, production DB).

Record voiceover matching these steps and show terminal + browser interactions.
