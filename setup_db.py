# setup_db.py
from app import app, db, User, Business

with app.app_context():
    # Drop all tables if they exist
    db.drop_all()
    db.create_all()

    # Add sample users
    user1 = User(name="John Doe", email="john@example.com", password="hashed_pw", role="consumer")
    user2 = User(name="EcoMart Vendor", email="vendor@example.com", password="hashed_pw", role="vendor")

    # Add sample business
    business1 = Business(
        business_name="Green Earth Store",
        contact_name="Ravi Kumar",
        mobile="9876543210",
        udyam_id="UDYAM-UP-1234",
        address="Gwalior, Madhya Pradesh",
        green_cert="certificate.pdf",
        verified=True
    )

    db.session.add_all([user1, user2, business1])
    db.session.commit()

    print("✅ Database initialized successfully with sample data!")
