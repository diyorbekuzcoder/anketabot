from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

response1 = client.get('/admin?status=Yangi')
print('Cookie set:', response1.cookies.get('admin_filters'))

response2 = client.get('/admin', cookies=response1.cookies)
print('Yangi in HTML:', 'value="Yangi" selected' in response2.text)
