# Indian Metropolitan Cities with Realistic Parameters
CITY_CONFIGS = {
    "Mumbai": {
        "population_size": 25000,
        "days": 90,
        "density": "very_high",  # 20,000+ per km²
        "contact_multiplier": 1.8,  # High crowding
        "healthcare_capacity": 0.85,
        "public_transport_usage": 0.88,
        "description": "India's financial capital, highest population density"
    },
    "Pune": {
        "population_size": 18000,
        "days": 90,
        "density": "high",  # 10,000+ per km²
        "contact_multiplier": 1.5,
        "healthcare_capacity": 0.78,
        "public_transport_usage": 0.72,
        "description": "IT hub with growing population"
    },
    "Delhi": {
        "population_size": 30000,
        "days": 90,
        "density": "very_high",  # 11,000+ per km²
        "contact_multiplier": 1.7,
        "healthcare_capacity": 0.82,
        "public_transport_usage": 0.85,
        "description": "National capital, dense urban core"
    },
    "Bangalore": {
        "population_size": 20000,
        "days": 90,
        "density": "high",  # 4,000+ per km²
        "contact_multiplier": 1.4,
        "healthcare_capacity": 0.80,
        "public_transport_usage": 0.65,
        "description": "Tech city, moderate density"
    },
    "Chennai": {
        "population_size": 17000,
        "days": 90,
        "density": "high",  # 26,000+ per km²
        "contact_multiplier": 1.6,
        "healthcare_capacity": 0.76,
        "public_transport_usage": 0.70,
        "description": "Southern metro, coastal city"
    },
    "Hyderabad": {
        "population_size": 16000,
        "days": 90,
        "density": "medium",  # 18,000+ per km²
        "contact_multiplier": 1.3,
        "healthcare_capacity": 0.75,
        "public_transport_usage": 0.60,
        "description": "Pharma hub, planned urban areas"
    },
    "Kolkata": {
        "population_size": 22000,
        "days": 90,
        "density": "very_high",  # 24,000+ per km²
        "contact_multiplier": 1.7,
        "healthcare_capacity": 0.72,
        "public_transport_usage": 0.80,
        "description": "Cultural capital, old dense neighborhoods"
    },
    "Ahmedabad": {
        "population_size": 14000,
        "days": 90,
        "density": "medium",  # 12,000+ per km²
        "contact_multiplier": 1.3,
        "healthcare_capacity": 0.70,
        "public_transport_usage": 0.55,
        "description": "Industrial city, Gujarat"
    },
    "Surat": {
        "population_size": 12000,
        "days": 90,
        "density": "medium",  # 13,000+ per km²
        "contact_multiplier": 1.2,
        "healthcare_capacity": 0.68,
        "public_transport_usage": 0.50,
        "description": "Diamond & textile hub"
    },
    "Jaipur": {
        "population_size": 10000,
        "days": 90,
        "density": "low",  # 6,000+ per km²
        "contact_multiplier": 1.1,
        "healthcare_capacity": 0.65,
        "public_transport_usage": 0.45,
        "description": "Tourist city, lower density"
    }
}

# Legacy configs for backward compatibility
CITY_A = {
    "population_size": 10000,
    "days": 60
}

CITY_B = {
    "population_size": 15000,
    "days": 60
}
