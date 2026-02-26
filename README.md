# 📱 Samsung Phone RAG API

This project is a FastAPI-based Retrieval-Augmented Generation (RAG) system for Samsung phone data stored in PostgreSQL.

It allows users to:
- Retrieve phone specifications
- Compare two phones
- Get the best phone based on criteria
- Ask natural-language questions

---

# 🚀 Project Structure

```
app/
│── main.py          # FastAPI app & endpoints
│── models.py        # SQLAlchemy models
│── database.py      # Database connection
│── rag.py           # Retrieval logic
```

---

# ⚙️ Requirements

- Python 3.9+
- PostgreSQL
- pip

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

---

# 🗄️ Database Setup

### Start PostgreSQL

Make sure PostgreSQL is running.

### Create Database

```sql
CREATE DATABASE samsung_db;
```

### Update database.py

Make sure your connection string is correct:

```python
DATABASE_URL = "postgresql://username:password@localhost/samsung_db"
```

Replace:
- `username`
- `password`

---

# Insert Sample Data

You must insert Samsung phone data into the `phones` table.

Example:

```sql
INSERT INTO phones 
(model_name, release_date, display_size, battery_mAh, camera_mp, base_ram_gb, storage_options, price_usd)
VALUES
('Galaxy S23 Ultra', '2023-02-17', 6.8, 5000, '200MP+12MP+10MP+10MP', 8, '256GB/512GB', 1199),
('Galaxy S22 Ultra', '2022-02-25', 6.8, 5000, '108MP+12MP+10MP+10MP', 8, '128GB/256GB', 999);
```

---

# Run the API

From project root:

```bash
uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

# 🧪 How to Test the API

You can test using:

- Browser
- Postman
- FastAPI Swagger UI

Open:

```
http://127.0.0.1:8000/docs
```

---

# Available Endpoints

---

## Get Phone Specs

```
GET /phone/{model_name}
```

Example:

```
/phone/Galaxy S23 Ultra
```

---

## Compare Two Phones

```
GET /compare?model1=S23 Ultra&model2=S22 Ultra
```

---

## Get Best Phone by Criteria

```
GET /best?battery=true&camera=true
```

Optional:
```
&max_price=1000
```

---

## Ask Natural Language Question (RAG)

```
GET /ask?query=Best Samsung under 1000 with good camera
```

Examples:

```
/ask?query=Compare Galaxy S23 Ultra and S22 Ultra
/ask?query=Best battery phone
/ask?query=Samsung under 900 dollars
```

---

# How It Works

1. User sends natural language query.
2. `rag.py` retrieves relevant phones from database.
3. `main.py` extracts criteria (battery, camera, ram, price).
4. Phones are scored and ranked.
5. API returns formatted response.

This is a structured RAG system using SQL retrieval instead of vector embeddings.

---

# Future Improvements

- Add embeddings for semantic search
- Use pgvector
- Add authentication
- Add frontend interface
- Deploy on Render / Railway / AWS
