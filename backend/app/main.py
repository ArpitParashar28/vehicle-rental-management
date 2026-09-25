from decimal import Decimal
from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select,func,and_
from sqlalchemy.orm import Session
from .database import Base,engine,get_db
from .models import Vehicle,Customer,Booking,Payment,DamageReport
from .schemas import *
from .config import settings
Base.metadata.create_all(engine)
app=FastAPI(title='Vehicle Rental Management API',description='Fleet, bookings, customers, payments and damage reports')
app.add_middleware(CORSMiddleware,allow_origins=[settings.cors_origins],allow_methods=['*'],allow_headers=['*'])
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/vehicles',response_model=VehicleOut,status_code=201)
def add_vehicle(x:VehicleCreate,db:Session=Depends(get_db)):
    o=Vehicle(**x.model_dump()); db.add(o); db.commit(); db.refresh(o); return o
@app.get('/vehicles',response_model=list[VehicleOut])
def vehicles(available_from:str|None=None,available_to:str|None=None,db:Session=Depends(get_db)):
    return db.scalars(select(Vehicle).where(Vehicle.active==True).order_by(Vehicle.model)).all()
@app.post('/customers',response_model=CustomerOut,status_code=201)
def add_customer(x:CustomerCreate,db:Session=Depends(get_db)):
    o=Customer(**x.model_dump()); db.add(o); db.commit(); db.refresh(o); return o
@app.get('/customers',response_model=list[CustomerOut])
def customers(db:Session=Depends(get_db)):
    return db.scalars(select(Customer).order_by(Customer.name)).all()
@app.post('/bookings',response_model=BookingOut,status_code=201)
def add_booking(x:BookingCreate,db:Session=Depends(get_db)):
    v=db.get(Vehicle,x.vehicle_id); c=db.get(Customer,x.customer_id)
    if not v or not c: raise HTTPException(400,'Vehicle or customer not found')
    overlap=db.scalar(select(func.count(Booking.id)).where(and_(Booking.vehicle_id==x.vehicle_id,Booking.status.in_(['reserved','active']),Booking.start_date<=x.end_date,Booking.end_date>=x.start_date)))
    if overlap: raise HTTPException(409,'Vehicle is already booked for the selected dates')
    days=(x.end_date-x.start_date).days+1
    total=Decimal(days)*v.daily_rate
    o=Booking(**x.model_dump(),total_amount=total); db.add(o); db.commit(); db.refresh(o); return o
@app.get('/bookings',response_model=list[BookingOut])
def bookings(status:str|None=None,db:Session=Depends(get_db)):
    q=select(Booking).order_by(Booking.start_date.desc())
    q=q.where(Booking.status==status) if status else q
    return db.scalars(q).all()
@app.patch('/bookings/{booking_id}/status',response_model=BookingOut)
def booking_status(booking_id:int,status:str,db:Session=Depends(get_db)):
    o=db.get(Booking,booking_id)
    if not o: raise HTTPException(404,'Booking not found')
    if status not in {'reserved','active','completed','cancelled'}: raise HTTPException(400,'Invalid status')
    o.status=status; db.commit(); db.refresh(o); return o
@app.post('/payments',response_model=PaymentOut,status_code=201)
def payment(x:PaymentCreate,db:Session=Depends(get_db)):
    if not db.get(Booking,x.booking_id): raise HTTPException(404,'Booking not found')
    o=Payment(**x.model_dump()); db.add(o); db.commit(); db.refresh(o); return o
@app.post('/damage-reports',response_model=DamageOut,status_code=201)
def damage(x:DamageCreate,db:Session=Depends(get_db)):
    if not db.get(Vehicle,x.vehicle_id): raise HTTPException(404,'Vehicle not found')
    o=DamageReport(**x.model_dump()); db.add(o); db.commit(); db.refresh(o); return o
@app.get('/damage-reports',response_model=list[DamageOut])
def damages(db:Session=Depends(get_db)):
    return db.scalars(select(DamageReport).order_by(DamageReport.reported_at.desc())).all()
@app.get('/dashboard')
def dashboard(db:Session=Depends(get_db)):
    return {
        'vehicles':db.scalar(select(func.count(Vehicle.id))),
        'active_bookings':db.scalar(select(func.count(Booking.id)).where(Booking.status=='active')),
        'open_damage_reports':db.scalar(select(func.count(DamageReport.id)).where(DamageReport.repair_status!='closed')),
        'revenue':float(db.scalar(select(func.coalesce(func.sum(Payment.amount),0))))
    }
