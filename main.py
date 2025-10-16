from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import models, db, recommender, llm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

app = FastAPI(title="E-commerce Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Initialize DB
models.Base.metadata.create_all(bind=db.engine)

reco = recommender.Recommender(db.SessionLocal)
# fit if products exist
reco.fit()
llm_client = llm.LLMClient()

@app.post("/seed")
def seed():
    from .seed import seed_demo
    session = db.SessionLocal()
    seed_demo(session)
    session.close()
    reco.fit()
    return {"status": "seeded"}

@app.post("/interactions")
def add_interaction(payload: dict):
    session = db.SessionLocal()
    try:
        models.get_or_create_user(session, payload["user_id"])
        models.create_interaction(session, payload["user_id"], payload["product_id"], payload.get("type","view"))
        return {"status":"ok"}
    finally:
        session.close()

@app.get("/recommendations")
def get_recommendations(user_id: str, k: int = 5):
    session = db.SessionLocal()
    try:
        if not models.user_exists(session, user_id):
            raise HTTPException(status_code=404, detail="user not found")
        candidates = reco.score_candidates(session, user_id, k=k)
        results = []
        history = models.get_user_history(session, user_id, limit=10)
        for item in candidates:
            why = llm_client.explain_recommendation(user_id, item["product"], history, item.get("feature_trace"))
            results.append({
                "product_id": item["product"].id,
                "title": item["product"].title,
                "score": round(float(item["score"]), 4),
                "why": why
            })
        return JSONResponse({"user_id": user_id, "recommendations": results})
    finally:
        session.close()
