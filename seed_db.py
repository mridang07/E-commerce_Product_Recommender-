from backend.app.db import SessionLocal
from backend.app.seed import seed_demo

if __name__ == '__main__':
    session = SessionLocal()
    seed_demo(session)
    print('Seeded demo data.')
