# E-commerce_Product_Recommender
## 🧠 Project Overview

This project is an **E-commerce Product Recommender System** that combines recommendation logic with AI-powered (LLM-style) explanations.

The goal is to recommend relevant products to a user based on their past behavior and provide a short, human-like explanation for *why* each product was suggested.

---

## 🎯 Objectives

- ✅ Build a **backend API** for product recommendations  
- ✅ Store **user data and interactions** in a database  
- ✅ Use an **LLM-like model** to generate natural explanations  
- ✅ Provide an optional **frontend dashboard** for visualization  
- ✅ Focus on clean code, modular design, and clarity

---

## 🧩 System Architecture

```

```
                    ┌────────────────────┐
                    │    Product DB      │
                    │ (SQLite, Products) │
                    └─────────┬──────────┘
                              │
                 ┌────────────┴────────────┐
                 │      FastAPI Backend    │
                 │  - Recommendation Logic │
                 │  - LLM Explanation Gen  │
                 └────────────┬────────────┘
                              │
                    ┌─────────┴──────────┐
                    │     Frontend UI    │
                    │ (HTML + Tailwind)  │
                    └────────────────────┘
```

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/manya18-git/E-commerce-Product-Recommender
cd E-commerce-Product-Recommender
````

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start the backend server

```bash
uvicorn backend.app.main:app
```

Server will start at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧠 Usage Guide

### Step 1️⃣ — Seed Sample Data

Insert sample users and products:

```bash
Invoke-WebRequest -Uri "http://127.0.0.1:8000/seed" -Method POST
```

Expected response:

```json
{"status": "seeded"}
```

---

### Step 2️⃣ — Get Product Recommendations

Fetch top 5 recommendations for a demo user:

```bash
curl "http://127.0.0.1:8000/recommendations?user_id=demo_user&k=5"
```

Sample Output:

```json
{
  "user_id": "demo_user",
  "recommendations": [
    {
      "product_id": "p1",
      "title": "Wireless Headphones",
      "why": "Recommended based on your interest in tech accessories."
    },
    {
      "product_id": "p2",
      "title": "Smartwatch",
      "why": "You viewed similar fitness gadgets recently."
    }
  ]
}
```

---

### Step 3️⃣ — Open Frontend Dashboard

Open `frontend/index.html` in your browser.
Enter `demo_user` and click **“Get Recommendations”** to see visually appealing product cards with explanations.

---

## 🧩 API Endpoints

| Method | Endpoint                                 | Description                                  |
| ------ | ---------------------------------------- | -------------------------------------------- |
| `POST` | `/seed`                                  | Seed demo data (products + users)            |
| `GET`  | `/recommendations?user_id=demo_user&k=5` | Get top-k product recommendations for a user |

---

## 💡 Recommendation Logic

The backend uses:

* A **content-based filtering approach** based on product categories and user history.
* A mock **LLM-like function** that generates explanation text using templates like:

  > “Recommended because you’ve shown interest in similar products recently.”

You can later extend this to a real LLM API such as OpenAI or Gemini.

---

## 🧰 Tech Stack

| Layer        | Technology                  |
| ------------ | --------------------------- |
| **Backend**  | FastAPI (Python)            |
| **Database** | SQLite                      |
| **Frontend** | HTML, Tailwind CSS, Axios   |
| **LLM Mock** | Template-based Python logic |

---

## 🎨 Frontend Features

✅ Clean, responsive layout using **Tailwind CSS**
✅ Dynamic product cards with image + explanation
✅ Loading animation and error handling
✅ Fully local — no external dependencies required

---

## 🧪 Example Demo Flow

1. Run backend → `uvicorn backend.app.main:app`
2. Seed data → `/seed` endpoint
3. Get recommendations → `/recommendations?user_id=demo_user`
4. Open frontend → `frontend/index.html`
5. Enter `demo_user` → See AI-generated explanations
