from app import app

with app.test_client() as client:
    response = client.get('/settings', follow_redirects=False)
    print(f'Status: {response.status_code}')
    if response.status_code in [301, 302, 307]:
        print(f'Redirects to: {response.location}')
    else:
        print(f'Response first 200 chars: {response.data[:200].decode(errors="ignore")}')
