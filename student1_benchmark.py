import random
import json 
import sys 
import time
import matplotlib.pyplot as plt

sys.path.insert(0, ".")

from mohaf.core import Resource, Request, ResourceType
from mohaf.auction_mechanisms import MOHAFAuction, GreedyAuction, FirstPriceAuction, RandomAuction
from mohaf.utils import calculate_allocation_efficiency, calculate_fairness_index, calculate_satisfaction_rate


with open("smartcity_dataset.json", "r") as file:
    dataset = json.load(file)


raw_requests = dataset["requests"]
raw_resources = dataset["resources"]

#we have the dictionary and we convert it to the resource object
def dict_to_resource(r):
    return Resource(
        id=r["id"],
        type=ResourceType.COMPUTE,
        capacity=r["capacity"]*100,
        cost_per_unit=r["cost_per_unit"],
        location=(0.0, 0.0),
        availability=r["availability"],
        reliability=r["reliability"],
        energy_efficiency=r["energy_efficiency"],
        owner_id = "owner_1"
    )

def dict_to_request(r):
    return Request(
        id=r["id"],
        requester_id=r["id"],
        resource_type=ResourceType.COMPUTE,
        amount=round(r["capacity"] if "capacity" in r else 20.0, 2),
        max_price=50.0,
        deadline=9999999999.0,#no deadline 
        priority=r["priority"],
        location=(r["location"][0], r["location"][1]),
        qos_requirements={
            "min_reliability": 0.5,
            "max_latency": r["latency_requirement"],
            "min_availability": 0.5
        }
    )

def climate_coverage(raw_requests, allocated_ids):
    high_risk = []
    for r in raw_requests:
        if r["climate_risk"] >= 0.5:
            high_risk.append(r)
    
    allocated = []
    for r in high_risk:
        if r["id"] in allocated_ids:
            allocated.append(r)
    
    if len(high_risk) == 0:
        return 0.0
    
    return round(len(allocated) / len(high_risk), 3)


resources = [dict_to_resource(r) for r in raw_resources]
requests = [dict_to_request(r) for r in raw_requests]

mechanisms = [
    MOHAFAuction(),
    GreedyAuction(),
    FirstPriceAuction(),
    RandomAuction()
]

results = []

for mechanism in mechanisms:
    result = mechanism.run_auction(resources, requests)
    
    allocated_ids = [a["request_id"] for a in result["allocations"]]
    
    efficiency   = calculate_allocation_efficiency(result)
    fairness     = calculate_fairness_index(result)
    satisfaction = calculate_satisfaction_rate(result)
    coverage     = climate_coverage(raw_requests, allocated_ids)
    
    print(f"--- {mechanism.name} ---")
    print(f"Efficiency  : {efficiency:.3f}")
    print(f"Fairness    : {fairness:.3f}")
    print(f"Satisfaction: {satisfaction:.3f}")
    print(f"Coverage    : {coverage:.3f}")
    print()

    results.append({
    "name": mechanism.name,
    "efficiency": efficiency,
    "fairness": fairness,
    "satisfaction": satisfaction,
    "coverage": coverage
})


####visualization 

names      = [r["name"]       for r in results]
efficiency = [r["efficiency"] for r in results]
fairness   = [r["fairness"]   for r in results]
coverage   = [r["coverage"]   for r in results]

fig, axes = plt.subplots(1, 3, figsize=(14, 5))

axes[0].bar(names, efficiency, color="steelblue")
axes[0].set_title("Efficiency")
axes[0].set_ylim(0, 1)
axes[0].set_xticklabels(names, rotation=45, ha="right")

axes[1].bar(names, fairness, color="green")
axes[1].set_title("Fairness")
axes[1].set_ylim(0, 1)
axes[1].set_xticklabels(names, rotation=45, ha="right")

axes[2].bar(names, coverage, color="orange")
axes[2].set_title("Climate Coverage")
axes[2].set_ylim(0, 1)
axes[2].set_xticklabels(names, rotation=45, ha="right")

plt.tight_layout()
plt.savefig("student1_results.png")


