import urllib.request
import json
import os

endpoints = ['/', '/dashboard', '/prediction', '/routes', '/relief', '/api/dashboard', '/api/risk-map', '/api/route?start=Zone%20A&end=Zone%20G', '/api/relief-priority', '/api/predict']
results = {}

for ep in endpoints:
    url = f'http://127.0.0.1:5000{ep}'
    try:
        req = urllib.request.Request(url)
        if ep == '/api/predict':
            req = urllib.request.Request(url, data=json.dumps({"rainfall": 120, "wind_speed": 65, "river_level": 6.5, "humidity": 85, "temperature": 28, "pressure": 995}).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            results[ep] = {"status": response.getcode()}
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
        except:
            body = str(e)
        results[ep] = {"status": e.code, "error": body}
    except Exception as e:
        results[ep] = {"error": str(e)}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.json')
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)
