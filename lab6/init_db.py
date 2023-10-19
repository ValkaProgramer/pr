from app import create_app, db, ElectroScooter
    
def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        sample_scooter_1 = ElectroScooter(name="Yamaha", battery_level=100)
        db.session.add(sample_scooter_1)

        db.session.commit()

if __name__ == "__main__":
    init_database()