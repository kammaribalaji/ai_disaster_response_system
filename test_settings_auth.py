from app import app
from auth import login_user

with app.test_client() as client:
    # First, manually set a session with admin role
    with client.session_transaction() as sess:
        sess['user_id'] = 'admin'
        sess['username'] = 'admin'
        sess['role'] = 'admin'
        sess['name'] = 'Admin User'
        sess['email'] = 'admin@example.com'
    
    # Now try to access settings
    response = client.get('/settings', follow_redirects=False)
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        print('SUCCESS! Settings page loaded')
        print(f'Content includes "Settings": {"Settings" in response.data.decode()}')
    elif response.status_code in [301, 302, 307]:
        print(f'Redirects to: {response.location}')
    else:
        print(f'Error response: {response.data[:200].decode(errors="ignore")}')
