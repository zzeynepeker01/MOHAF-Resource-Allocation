import random 
import json 

# this is my set of tasks 
TASK_TYPES = [
    "air_quality_monitoring",
    "traffic_management",
    "urban_heat_detection",
    "smart_energy",
    "disaster_early_warning",
    "flood_sensor",
    "emergency_response"
]

# formula from the muhaf #aqi stands for air quality risk others are heat risk trafiic congestion score and energy risk score
def climate_risk_calculation(aqi, heat, traffic, energy):
    score = 0.4* aqi + 0.3*heat + 0.2*traffic + 0.1*energy
    return round(score,3)

def request_production(id):
    aqi = round(random.uniform(0.1, 1.0), 3)
    heat = round(random.uniform(0.1, 1.0), 3)
    traffic = round(random.uniform(0.1, 1.0), 3)
    energy = round(random.uniform(0.1,1.0),3)
                   
    request = {
        "id": f"{id}",
        "task_type": random.choice(TASK_TYPES) , 
        "priority": random.randint(1, 10),

        "aqi_risk": aqi,
        "heat_risk" : heat,
        "traffic_risk" : traffic,
        "energy_risk" : energy,

        "climate_risk" : climate_risk_calculation(aqi,heat,traffic, energy),
        "latency_requirement": round(random.uniform(0.1, 0.8), 3) , 
        "location": 
        [round(random.uniform(40.8, 41.2), 4),
            round(random.uniform(28.6, 29.3), 4)]
    }
    return request


def resource_production(id):

    resource = {
        "id" : f"{id}",
        "capacity" : round(random.uniform(0.3,1.0), 3), # 0.3 to 1 since the capacity of an edge server cannot be 0
        "energy_efficiency" : round(random.uniform(0.1,1.0),3), 
        "latency" : round(random.uniform(0.1, 1.0),3),
        "compute_load" : round(random.uniform(0.1,1.0),3), # if it is 1 then it is full 
        ## I asked for these 3 parameters
        "availability": round(random.uniform(0.5, 1.0), 3),
        "reliability": round(random.uniform(0.5, 1.0), 3),
        "cost_per_unit": round(random.uniform(0.3, 2.0), 3)
    }
    return resource

#dataset production
# I produced 30 and 50 since it was like this in MUHAF  we can change it 
requests = []
resources = []
for i in range(50):
    requests.append(request_production(i))

for i in range(30):
    resources.append(resource_production(i))


dataset = {
    "requests" : requests,
    "resources" : resources
}

with open("smartcity_dataset.json", "w") as file:
    json.dump(dataset, file, indent = 2)


#x = random.choice(TASK_TYPES)
