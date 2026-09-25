from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').status_code==200
def test_invalid_booking_dates():
 r=client.post('/bookings',json={'vehicle_id':1,'customer_id':1,'start_date':'2026-10-10','end_date':'2026-10-01'})
 assert r.status_code==422
