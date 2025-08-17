from datetime import date
from app.models.database import Member
from app.database import SessionLocal

def seed():
    db = SessionLocal()
    if not db.query(Member).first():
        new_member = Member(
            preferred_name="Aryan",
            dob=date(2002, 5, 15),   # 👈 required, adjust to valid DOB
            age=23,
            gender="Male",           # 👈 required
            residence="Kharagpur",
            travel_hubs=["IIT KGP"],
            occupation="Student",
            pa="N/A",                # 👈 required if not nullable
            tech_preferences=["Mobile", "Web"],
            health_goals=["Fitness"],
            communication_preferences=["Email"],
            scheduling_preferences=["Morning"]
        )
        db.add(new_member)
        db.commit()
        print("Dummy member inserted ✅")
    else:
        print("Member already exists")
    db.close()


if __name__ == "__main__":
    seed()
