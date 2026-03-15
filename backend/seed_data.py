import json
import random

def generate_industries():
    # San Francisco Bay Area bounds approx
    LAT_MIN, LAT_MAX = 37.3, 38.0
    LON_MIN, LON_MAX = -122.5, -121.8
    
    industries = []
    
    # 50 Producers
    producer_types = [
        "Steel Plant", "Food Processor", "Data Center", "Chemical Plant", 
        "Brewery", "Lumber Mill", "Paper Mill", "Textile Factory", "Auto Manufacturer"
    ]
    
    for i in range(1, 51):
        industries.append({
            "id": f"P_{i}",
            "name": f"Bay Area {random.choice(producer_types)} #{i}",
            "role": "producer",
            "lat": random.uniform(LAT_MIN, LAT_MAX),
            "lon": random.uniform(LON_MIN, LON_MAX),
            "description": "Generates industrial waste streams periodically."
        })

    # 50 Consumers and their demands
    consumer_demands = [
        ("Greenhouse Farm", "Requires CO2 for enhanced plant growth and waste heat for temperature control."),
        ("Biogas Plant", "Needs high-moisture organic waste, sludge, or food scraps for anaerobic digestion."),
        ("District Heating Facility", "Requires clean industrial waste heat or warm water for residential heating systems."),
        ("Algae Biofuel Facility", "Needs high volumes of Carbon Dioxide (CO2) to accelerate algae photosynthesis."),
        ("Recycling Center", "Requires plastic, metal scrap, or glass waste for processing."),
        ("Construction Materials Co", "Needs ash, slag, or mineral residues to mix into concrete and cement."),
        ("Packaging Manufacturer", "Requires secondary paper, cardboard, or recycled pulp fibers."),
        ("Cooling Tower Facility", "Needs treated wastewater or gray water for industrial cooling systems."),
        ("Composting Facility", "Requires solid organic waste, agricultural residue, or wood chips.")
    ]

    for i in range(1, 51):
        c_type, demand = random.choice(consumer_demands)
        industries.append({
            "id": f"C_{i}",
            "name": f"NorCal {c_type} #{i}",
            "role": "consumer",
            "lat": random.uniform(LAT_MIN, LAT_MAX),
            "lon": random.uniform(LON_MIN, LON_MAX),
            "demand": demand
        })

    with open("industries.json", "w") as f:
        json.dump(industries, f, indent=4)

if __name__ == "__main__":
    generate_industries()
    print("industries.json generated successfully.")
