import heapq

mock_graph = {
    'Zone A': {'Zone B': (5, 2), 'Zone C': (10, 1)},
    'Zone B': {'Zone A': (5, 2), 'Zone D': (3, 3), 'Zone E': (8, 1)},
    'Zone C': {'Zone A': (10, 1), 'Zone F': (12, 1)},
    'Zone D': {'Zone B': (3, 3), 'Zone G': (4, 2)},
    'Zone E': {'Zone B': (8, 1), 'Zone H': (6, 1)},
    'Zone F': {'Zone C': (12, 1), 'Zone H': (7, 2)},
    'Zone G': {'Zone D': (4, 2), 'Zone I': (5, 1)},
    'Zone H': {'Zone E': (6, 1), 'Zone F': (7, 2), 'Zone I': (4, 1)},
    'Zone I': {'Zone G': (5, 1), 'Zone H': (4, 1)}
}

mock_node_risks = {
    'Zone A': 10, 'Zone B': 50, 'Zone C': 10,
    'Zone D': 80, 'Zone E': 20, 'Zone F': 10,
    'Zone G': 90, 'Zone H': 30, 'Zone I': 10
}

def calculate_route(start, end):
    if start not in mock_graph or end not in mock_graph:
        return {"error": "Invalid start or end zone."}
        
    distances = {node: float('infinity') for node in mock_graph}
    distances[start] = 0
    previous_nodes = {node: None for node in mock_graph}
    
    pq = [(0, start)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_distance > distances[current_node]:
            continue
            
        if current_node == end:
            break
            
        for neighbor, (dist, traffic) in mock_graph[current_node].items():
            risk = mock_node_risks.get(neighbor, 0)
            
            # weight = distance + risk + traffic
            weight = dist + (risk * 0.1) + (traffic * 2)
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes.get(current)
    path = path[::-1]
    
    if path and path[0] == start:
        total_distance = distances[end]
        avg_risk = sum(mock_node_risks.get(n, 0) for n in path) / len(path)
        safety_score = max(0, 100 - avg_risk)
        eta_mins = round(total_distance * 1.5 + (100 - safety_score) * 0.2)
        
        return {
            "path": path,
            "cost": round(total_distance, 2),
            "distance_km": round(total_distance, 1),
            "eta_mins": int(eta_mins),
            "safety_score": round(safety_score, 1)
        }
    else:
        return {"error": "No path found."}
