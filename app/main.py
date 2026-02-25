from fastapi import FastAPI, Query
from .models import Phone
from .rag import retrieve_phones
from .database import SessionLocal
import re

app = FastAPI()
db = SessionLocal()


PHONE_KEYWORDS = ["galaxy", "note", "samsung", "ultra", "fe", "plus"]
CRITERIA_KEYWORDS = {
    "battery": ["battery", "batteries", "longest battery", "best battery"],
    "ram": ["ram", "memory"],
    "camera": ["camera", "photography", "rear", "front camera", "selfie"],
    "price": ["price", "cheap", "cost", "under", "budget"]
}




def extract_data(phone_list):
    """
    Convert Phone objects to dict with numeric values for scoring.
    """
    extracted = []
    for phone in phone_list:
        camera_mp_total = 0
        if phone.camera_mp:
            if isinstance(phone.camera_mp, str):
                try:
                    camera_mp_total = sum(int(x.replace('MP','')) for x in phone.camera_mp.split('+'))
                except:
                    camera_mp_total = 0
            else:
                camera_mp_total = 0
        extracted.append({
            "model_name": phone.model_name,
            "battery": phone.battery_mAh or 0,
            "ram": phone.base_ram_gb or 0,
            "camera": camera_mp_total,
            "price": phone.price_usd or 0
        })
    return extracted


def generate_review(phone_data, criteria):
    """
    Generate natural language review or comparison based on criteria.
    """
    if not phone_data:
        return "❌ No matching phones found."
    
    if len(phone_data) == 1:
        phone = phone_data[0]
        return f"📱 {phone['model_name']} Specs:\n" + \
               "\n".join([f"- {c.capitalize()}: {phone[c]}" for c in criteria])
    
    elif len(phone_data) == 2:
        p1, p2 = phone_data
        result = f"🔍 Comparing {p1['model_name']} vs {p2['model_name']}\n"
        for key in criteria:
            if p1[key] > p2[key]:
                result += f"✅ Better {key.capitalize()}: {p1['model_name']} ({p1[key]})\n"
            elif p2[key] > p1[key]:
                result += f"✅ Better {key.capitalize()}: {p2['model_name']} ({p2[key]})\n"
            else:
                result += f"⚖ {key.capitalize()} Equal: {p1[key]}\n"
        return result
    
    else:
        scored = [(phone, sum(phone[c] for c in criteria if c in phone)) for phone in phone_data]
        scored.sort(key=lambda x: x[1], reverse=True)
        best = scored[0][0]
        return f"🏆 Best Phone: {best['model_name']}\n" + \
               "\n".join([f"- {c.capitalize()}: {best[c]}" for c in criteria])


def get_specs(model_name: str):
    """
    Return formatted specs of a single phone.
    """
    phone = db.query(Phone).filter(Phone.model_name.ilike(f"%{model_name}%")).first()
    if not phone:
        return f"❌ Phone '{model_name}' not found."
    
    camera_info = phone.camera_mp if phone.camera_mp else "N/A"
    
    return (
        f"📱 {phone.model_name} Specs:\n"
        f"- Release Date: {phone.release_date}\n"
        f"- Display Size: {phone.display_size}\"\n"
        f"- Battery: {phone.battery_mAh} mAh\n"
        f"- Camera: {camera_info}\n"
        f"- RAM: {phone.base_ram_gb} GB\n"
        f"- Storage Options: {phone.storage_options}\n"
        f"- Price: ${phone.price_usd}"
    )


def compare_phones(model1: str, model2: str):
    """
    Compare two phones on battery, RAM, display, price, and camera.
    """
    p1 = db.query(Phone).filter(Phone.model_name.ilike(f"%{model1}%")).first()
    p2 = db.query(Phone).filter(Phone.model_name.ilike(f"%{model2}%")).first()

    if not p1 or not p2:
        return "❌ One or both phones not found."
    
    result = f"🔍 Comparison: {p1.model_name} vs {p2.model_name}\n"
    
    
    if p1.battery_mAh > p2.battery_mAh:
        result += f"✅ Better Battery: {p1.model_name} ({p1.battery_mAh} mAh)\n"
    elif p2.battery_mAh > p1.battery_mAh:
        result += f"✅ Better Battery: {p2.model_name} ({p2.battery_mAh} mAh)\n"
    else:
        result += f"⚖ Battery Equal: {p1.battery_mAh} mAh\n"
    
    
    if p1.base_ram_gb > p2.base_ram_gb:
        result += f"✅ More RAM: {p1.model_name} ({p1.base_ram_gb} GB)\n"
    elif p2.base_ram_gb > p1.base_ram_gb:
        result += f"✅ More RAM: {p2.model_name} ({p2.base_ram_gb} GB)\n"
    else:
        result += f"⚖ RAM Equal: {p1.base_ram_gb} GB\n"
    
    
    if p1.display_size > p2.display_size:
        result += f"✅ Larger Display: {p1.model_name} ({p1.display_size}\")\n"
    elif p2.display_size > p1.display_size:
        result += f"✅ Larger Display: {p2.model_name} ({p2.display_size}\")\n"
    else:
        result += f"⚖ Display Equal: {p1.display_size}\"\n"
    
    
    if p1.price_usd < p2.price_usd:
        result += f"💰 Cheaper: {p1.model_name} (${p1.price_usd})\n"
    elif p2.price_usd < p1.price_usd:
        result += f"💰 Cheaper: {p2.model_name} (${p2.price_usd})\n"
    else:
        result += f"⚖ Same Price: ${p1.price_usd}\n"
    

    try:
        p1_rear = sum(int(x.replace('MP','')) for x in p1.camera_mp.split('+')) if p1.camera_mp else 0
        p2_rear = sum(int(x.replace('MP','')) for x in p2.camera_mp.split('+')) if p2.camera_mp else 0
        if p1_rear > p2_rear:
            result += f"📸 Better Rear Camera: {p1.model_name} ({p1_rear}MP total)\n"
        elif p2_rear > p1_rear:
            result += f"📸 Better Rear Camera: {p2.model_name} ({p2_rear}MP total)\n"
        else:
            result += f"⚖ Rear Cameras Equal: {p1_rear}MP total\n"
    except:
        result += "📸 Camera info unavailable\n"
    
    return result


def best_phone(criteria: list[str], price_limit: float = None):
    """
    Return best phone based on criteria and optional price limit.
    """
    phones = db.query(Phone).all()
    if not phones:
        return "❌ No phones in database."
    
    scored = []
    for phone in phones:
        score = 0
        if "battery" in criteria and phone.battery_mAh:
            score += phone.battery_mAh / 1000
        if "ram" in criteria and phone.base_ram_gb:
            score += phone.base_ram_gb
        if "price" in criteria and phone.price_usd:
            max_price = max(p.price_usd for p in phones)
            score += max_price - phone.price_usd
        if "camera" in criteria and phone.camera_mp:
            try:
                total_mp = sum(int(x.replace('MP','')) for x in phone.camera_mp.split('+'))
            except:
                total_mp = 0
            score += total_mp / 10
        if price_limit and phone.price_usd > price_limit:
            score = -1  
        scored.append((phone, score))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    best = scored[0][0]
    
    return f"🏆 Best Phone: {best.model_name}\n" \
           f"- Battery: {best.battery_mAh} mAh\n" \
           f"- RAM: {best.base_ram_gb} GB\n" \
           f"- Price: ${best.price_usd}\n" \
           f"- Camera: {best.camera_mp}"




@app.get("/phone/{model_name}")
def phone_info(model_name: str):
    return {"answer": get_specs(model_name)}


@app.get("/compare")
def compare(model1: str = Query(...), model2: str = Query(...)):
    return {"answer": compare_phones(model1, model2)}


@app.get("/best")
def best_endpoint(battery: bool = False, camera: bool = False, ram: bool = False, price: bool = False, max_price: float = None):
    criteria = []
    if battery: criteria.append("battery")
    if camera: criteria.append("camera")
    if ram: criteria.append("ram")
    if price: criteria.append("price")
    return {"answer": best_phone(criteria, max_price)}


@app.get("/ask")
def ask(query: str):
    """
    Advanced natural-language query handler using RAG.
    """
    q = query.lower()
    
    detected_criteria = [key for key, kws in CRITERIA_KEYWORDS.items() if any(k in q for k in kws)]
    

    price_limit = None
    match = re.search(r'under \$?(\d+)', q)
    if match:
        price_limit = float(match.group(1))
    
   
    phones = retrieve_phones(query, price_limit)
    normalized_data = extract_data(phones)
    
    answer = generate_review(normalized_data, detected_criteria)
    return {"answer": answer}