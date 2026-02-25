from .models import Phone
from .database import SessionLocal

db = SessionLocal()

def retrieve_phones(query: str, price_limit: float = None):
    """
    Retrieve relevant phones from the database based on query keywords
    and optional price limit.
    """
    query_lower = query.lower()
    phones = db.query(Phone).all()

    matched = []

    for phone in phones:
        if phone.model_name and phone.model_name.lower() in query_lower:
            if price_limit and phone.price_usd > price_limit:
                continue
            matched.append(phone)
            continue

       
        for keyword in ["galaxy", "note", "samsung", "ultra", "fe", "plus"]:
            if keyword in phone.model_name.lower() and keyword in query_lower:
                if price_limit and phone.price_usd > price_limit:
                    continue
                matched.append(phone)
                break

    
    if not matched and price_limit:
        matched = [p for p in phones if p.price_usd <= price_limit]

  
    if not matched:
        matched = phones

    return matched