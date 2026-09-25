from datetime import date,datetime
from decimal import Decimal
from pydantic import BaseModel,ConfigDict,EmailStr,model_validator
class VehicleCreate(BaseModel): registration:str; model:str; category:str; daily_rate:Decimal; active:bool=True
class VehicleOut(VehicleCreate): id:int; model_config=ConfigDict(from_attributes=True)
class CustomerCreate(BaseModel): name:str; email:EmailStr; phone:str|None=None
class CustomerOut(CustomerCreate): id:int; model_config=ConfigDict(from_attributes=True)
class BookingCreate(BaseModel):
    vehicle_id:int; customer_id:int; start_date:date; end_date:date
    @model_validator(mode='after')
    def dates(self):
        if self.end_date < self.start_date: raise ValueError('end_date must be on/after start_date')
        return self
class BookingOut(BaseModel): id:int; vehicle_id:int; customer_id:int; start_date:date; end_date:date; status:str; total_amount:Decimal; created_at:datetime; model_config=ConfigDict(from_attributes=True)
class PaymentCreate(BaseModel): booking_id:int; amount:Decimal; method:str='card'; status:str='paid'
class PaymentOut(PaymentCreate): id:int; paid_at:datetime; model_config=ConfigDict(from_attributes=True)
class DamageCreate(BaseModel): vehicle_id:int; booking_id:int|None=None; severity:str='minor'; description:str; repair_status:str='open'; estimated_cost:Decimal|None=None
class DamageOut(DamageCreate): id:int; reported_at:datetime; model_config=ConfigDict(from_attributes=True)
