# genpark-agentic-commerce-warehouse-slotting-pick-path-tsp-optimizer-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Warehouse SKU velocity ABC classification, pick density heat-mapping and Traveling Salesperson pick-path distance reducer.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `optimize_warehouse_pick_path`
- **Category**: `agentic_commerce`

### Method Documentation
Optimize warehouse order fulfillment picking routes and SKU slotting positions.
Applies ABC velocity classification (fast movers at ergonomic waist level near depot) and calculates optimized pick-path distance
using 2-opt Traveling Salesperson routing vs standard unoptimized serpentine traversal.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "optimize_warehouse_pick_path",
    "arguments": {
    "pick_locations": [
        {
            "sku": "SKU-A101",
            "x": 12.0,
            "y": 45.0
        },
        {
            "sku": "SKU-B204",
            "x": 5.0,
            "y": 80.0
        },
        {
            "sku": "SKU-C309",
            "x": 28.0,
            "y": 15.0
        },
        {
            "sku": "SKU-D412",
            "x": 35.0,
            "y": 92.0
        },
        {
            "sku": "SKU-E518",
            "x": 8.0,
            "y": 10.0
        }
    ],
    "depot_coord": [
        0.0,
        0.0
    ]
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
