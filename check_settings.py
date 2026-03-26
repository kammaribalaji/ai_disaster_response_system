import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Login
login_data = {'username': 'admin', 'password': 'admin123'}
r = session.post('http://localhost:5000/login', data=login_data, allow_redirects=False)
print(f'Login: {r.status_code}')

# Get settings page
r = session.get('http://localhost:5000/settings')
print(f'Settings page status: {r.status_code}')
print(f'Page length: {len(r.text)} chars')

# Parse HTML
soup = BeautifulSoup(r.text, 'html.parser')

# Check for expected elements
checks = [
    ('System Settings title', 'System Settings' in r.text),
    ('Save button', 'Save Changes' in r.text),
    ('Settings sections', 'System Configuration' in r.text),
    ('Toggle switches', 'toggle-switch' in r.text),
    ('Input fields', 'settings-input' in r.text),
]

print('\nPage content checks:')
for check_name, result in checks:
    status = '✓' if result else '✗'
    print(f'  {status} {check_name}')

if all(result for _, result in checks):
    print('\n✅ Settings page is FULLY WORKING!')
else:
    print('\n❌ Some elements are missing')
    print(f'\nFirst 500 chars of response:\n{r.text[:500]}')
