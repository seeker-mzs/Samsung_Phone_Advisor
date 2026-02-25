from app.database import SessionLocal
from app.models import Phone

db = SessionLocal()

phone1 = Phone(
    model_name="Samsung Galaxy S23 Ultra",
    release_date="2023",
    display="6.8-inch AMOLED",
    battery="5000mAh",
    camera="200MP",
    ram="12GB",
    storage="256GB",
    price=1199
)

phone2 = Phone(
    model_name="Samsung Galaxy S22 Ultra",
    release_date="2022",
    display="6.8-inch AMOLED",
    battery="5000mAh",
    camera="108MP",
    ram="8GB",
    storage="256GB",
    price=999
)

db.add(phone1)
db.add(phone2)

db.commit()
db.close()

print("Dummy data inserted successfully!")