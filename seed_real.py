from app.database import SessionLocal
from app.models import Phone
from data.phones_data import phones  

db = SessionLocal()

for phone in phones:
    existing = db.query(Phone).filter_by(model_name=phone["model_name"]).first()
    if existing:
        print(f"⚠ Skipped duplicate {phone['model_name']}")
        continue
    
    try:
        db_phone = Phone(
            model_name=phone["model_name"],
            release_date=phone["release_date"],
            display_size=phone["display_size"],
            battery_mAh=phone["battery_mAh"],
            camera_mp=phone["camera_mp"],       # JSON column
            base_ram_gb=phone["base_ram_gb"],
            storage_options=phone["storage_options"],
            price_usd=phone["price_usd"]
        )
        
        db.add(db_phone)   # <-- use the correct variable
        db.commit()
        print(f"✅ Inserted {phone['model_name']}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding {phone['model_name']}: {e}")

db.close()
print("🎉 Database seeding completed!")