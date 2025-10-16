import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from . import models
import math

class Recommender:
    def __init__(self, SessionLocal):
        self.SessionLocal = SessionLocal
        self.item_ids = []
        self.item_matrix = None
        self.tfidf = None

    def fit(self):
        """Build item vectors (TF-IDF over title+description+tags)."""
        session = self.SessionLocal()
        try:
            products = models.list_products(session)
            docs = []
            ids = []
            for p in products:
                tags = ''
                try:
                    tags = ' '.join(eval(p.tags))
                except:
                    tags = ''
                docs.append(' '.join([p.title or '', p.description or '', tags]))
                ids.append(p.id)
            if not docs:
                self.item_matrix = None
                self.item_ids = []
                return
            self.tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=1000)
            self.item_matrix = self.tfidf.fit_transform(docs)
            self.item_ids = ids
        finally:
            session.close()

    def score_candidates(self, session, user_id, k=5):
        """Return top-k products with simple hybrid scoring."""
        if self.item_matrix is None:
            self.fit()
        products = models.list_products(session)
        # build user profile vector: simple sum of item vectors for items user viewed/purchased
        history = session.query(models.Interaction).filter(models.Interaction.user_id==user_id).all()
        if not history:
            # cold start -> small uniform score
            scored = []
            for p in products:
                scored.append({'product': p, 'score': 0.1, 'feature_trace': {'reason':'cold_start'}})
            scored = sorted(scored, key=lambda x: x['score'], reverse=True)[:k]
            return scored

        # map product id to index
        id_to_index = {pid: idx for idx,pid in enumerate(self.item_ids)}
        user_vec = None
        for h in history:
            pid = h.product_id
            idx = id_to_index.get(pid)
            if idx is None:
                continue
            weight = 1.0
            if h.type == 'purchase':
                weight = 3.0
            elif h.type == 'add_to_cart':
                weight = 2.0
            vec = self.item_matrix[idx].toarray()[0] * weight
            if user_vec is None:
                user_vec = vec
            else:
                user_vec += vec
        if user_vec is None:
            user_vec = np.zeros(self.item_matrix.shape[1])

        sims = cosine_similarity([user_vec], self.item_matrix.toarray())[0]
        scored = []
        for idx, sim in enumerate(sims):
            pid = self.item_ids[idx]
            p = session.query(models.Product).get(pid)
            purchased = any((h.product_id==pid and h.type=='purchase') for h in history)
            final_score = float(sim) * (0.5 if purchased else 1.0)
            trace = {'similarity': float(round(sim,4)), 'purchased_before': purchased}
            scored.append({'product': p, 'score': final_score, 'feature_trace': trace})
        scored = sorted(scored, key=lambda x: x['score'], reverse=True)
        scored = [s for s in scored if s['score']>0][:k]
        return scored
