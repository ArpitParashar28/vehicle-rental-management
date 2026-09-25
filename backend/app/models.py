from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String,Integer,Date,DateTime,ForeignKey,Numeric,Text,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .database import Base
class Vehicle(Base):
    __tablename__='vehicles'; id:Mapped[int]=mapped_column(primary_key=True); registration:Mapped[str]=mapped_column(String(30),unique=True,index=True); model:Mapped[str]=mapped_column(String(100)); category:Mapped[str]=mapped_column(String(50)); daily_rate:Mapped[Decimal]=mapped_column(Numeric(10,2)); active:Mapped[bool]=mapped_column(Boolean,default=True)
class Customer(Base):
    __tablename__='customers'; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(120)); email:Mapped[str]=mapped_column(String(160),unique=True); phone:Mapped[str|None]=mapped_column(String(40),nullable=True)
class Booking(Base):
    __tablename__='bookings'; id:Mapped[int]=mapped_column(primary_key=True); vehicle_id:Mapped[int]=mapped_column(ForeignKey('vehicles.id')); customer_id:Mapped[int]=mapped_column(ForeignKey('customers.id')); start_date:Mapped[date]=mapped_column(Date); end_date:Mapped[date]=mapped_column(Date); status:Mapped[str]=mapped_column(String(30),default='reserved'); total_amount:Mapped[Decimal]=mapped_column(Numeric(10,2)); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Payment(Base):
    __tablename__='payments'; id:Mapped[int]=mapped_column(primary_key=True); booking_id:Mapped[int]=mapped_column(ForeignKey('bookings.id')); amount:Mapped[Decimal]=mapped_column(Numeric(10,2)); method:Mapped[str]=mapped_column(String(30)); status:Mapped[str]=mapped_column(String(30),default='paid'); paid_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class DamageReport(Base):
    __tablename__='damage_reports'; id:Mapped[int]=mapped_column(primary_key=True); vehicle_id:Mapped[int]=mapped_column(ForeignKey('vehicles.id')); booking_id:Mapped[int|None]=mapped_column(ForeignKey('bookings.id'),nullable=True); severity:Mapped[str]=mapped_column(String(20)); description:Mapped[str]=mapped_column(Text); repair_status:Mapped[str]=mapped_column(String(30),default='open'); estimated_cost:Mapped[Decimal|None]=mapped_column(Numeric(10,2),nullable=True); reported_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
