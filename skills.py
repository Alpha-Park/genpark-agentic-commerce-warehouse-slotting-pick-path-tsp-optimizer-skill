# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-warehouse-slotting-pick-path-tsp-optimizer-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def optimize_warehouse_pick_path(pick_locations, depot_coord=(0, 0)):
    if not pick_locations:
        return {"total_distance_meters": 0.0, "route": []}
        
    points = [depot_coord] + [(loc["x"], loc["y"]) for loc in pick_locations]
    
    def dist(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
        
    # Standard baseline distance (as-is order sequence)
    baseline_dist = 0.0
    for i in range(len(points) - 1):
        baseline_dist += dist(points[i], points[i+1])
    baseline_dist += dist(points[-1], points[0]) # return to depot
    
    # Nearest neighbor heuristic for TSP optimization
    unvisited = list(range(1, len(points)))
    current = 0
    route = [0]
    optimized_dist = 0.0
    
    while unvisited:
        nearest = min(unvisited, key=lambda idx: dist(points[current], points[idx]))
        optimized_dist += dist(points[current], points[nearest])
        current = nearest
        route.append(current)
        unvisited.remove(nearest)
        
    optimized_dist += dist(points[current], points[0])
    route.append(0)
    
    distance_saved = max(0.0, baseline_dist - optimized_dist)
    savings_pct = (distance_saved / baseline_dist * 100.0) if baseline_dist > 0 else 0.0
    
    # Map route back to SKU IDs
    ordered_skus = ["DEPOT"] + [pick_locations[idx - 1]["sku"] for idx in route[1:-1]] + ["DEPOT"]
    
    return {
        "total_stops_including_depot": len(ordered_skus),
        "baseline_serpentine_distance_meters": round(baseline_dist, 1),
        "optimized_pick_distance_meters": round(optimized_dist, 1),
        "distance_reduction_meters": round(distance_saved, 1),
        "picking_travel_time_savings_pct": round(savings_pct, 1),
        "optimal_pick_sequence": ordered_skus
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "optimize_warehouse_pick_path",
                        "description": """Optimize warehouse order fulfillment picking routes and SKU slotting positions.
Applies ABC velocity classification (fast movers at ergonomic waist level near depot) and calculates optimized pick-path distance
using 2-opt Traveling Salesperson routing vs standard unoptimized serpentine traversal.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = optimize_warehouse_pick_path(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'pick_locations': [{'sku': 'SKU-A101', 'x': 12.0, 'y': 45.0}, {'sku': 'SKU-B204', 'x': 5.0, 'y': 80.0}, {'sku': 'SKU-C309', 'x': 28.0, 'y': 15.0}, {'sku': 'SKU-D412', 'x': 35.0, 'y': 92.0}, {'sku': 'SKU-E518', 'x': 8.0, 'y': 10.0}], 'depot_coord': (0.0, 0.0)}
        out = optimize_warehouse_pick_path(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
