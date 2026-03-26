import requests

session = requests.Session()

# Login first
login_data = {'username': 'admin', 'password': 'admin123'}
r = session.post('http://localhost:5000/login', data=login_data, allow_redirects=False)
print(f'Login status: {r.status_code}')

# Now access settings
r = session.get('http://localhost:5000/settings')
print(f'Settings status: {r.status_code}')
has_content = 'System Settings' in r.text or 'System Configuration' in r.text
print(f'Has settings content: {has_content}')
if r.status_code == 200 and has_content:
    print('SUCCESS! Settings page is fully working!')
else:
    print(f'ERROR: Got status {r.status_code}')
    if 'Page Not Found' in r.text:
        print('Settings page returning 404!')
