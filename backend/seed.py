from app.database import Base,engine,SessionLocal
from app.models import Vehicle,Customer
Base.metadata.create_all(engine);db=SessionLocal()
if not db.query(Vehicle).first():
 db.add_all([Vehicle(registration='B-MB 1001',model='Mercedes-Benz Vito',category='Van',daily_rate=89),Vehicle(registration='B-MB 1002',model='Mercedes-Benz Sprinter',category='Transporter',daily_rate=119),Vehicle(registration='B-EQ 1003',model='Mercedes-Benz eVito',category='Electric Van',daily_rate=99)])
 db.add(Customer(name='Demo Customer',email='demo@example.com',phone='+49 000 000'))
 db.commit()
print('Seeded')
