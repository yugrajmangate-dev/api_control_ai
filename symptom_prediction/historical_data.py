"""
Historical Pandemic Data Repository
Contains comprehensive epidemiological data from past pandemics for comparative analysis
Based on WHO reports, CDC data, and peer-reviewed research
"""

HISTORICAL_PANDEMICS = {
    "COVID-19": {
        "name": "COVID-19 (SARS-CoV-2)",
        "year": 2019,
        "virus_type": "Coronavirus",
        "epidemiology": {
            "r0": 2.5,  # Basic reproduction number
            "incubation_period": 5.1,  # days (mean)
            "serial_interval": 4.7,  # days
            "case_fatality_rate": 2.3,  # percentage (varies by region/variant)
            "hospitalization_rate": 14.0,  # percentage
            "asymptomatic_rate": 30.0,  # percentage
        },
        "symptoms": {
            "primary": [
                {"name": "Fever", "prevalence": 87.9, "severity": "moderate", "onset_day": 1},
                {"name": "Dry Cough", "prevalence": 67.7, "severity": "moderate", "onset_day": 2},
                {"name": "Fatigue", "prevalence": 38.1, "severity": "moderate", "onset_day": 1},
                {"name": "Loss of Smell/Taste", "prevalence": 64.0, "severity": "mild", "onset_day": 3},
                {"name": "Shortness of Breath", "prevalence": 18.6, "severity": "severe", "onset_day": 5},
            ],
            "secondary": [
                {"name": "Sore Throat", "prevalence": 13.9, "severity": "mild", "onset_day": 2},
                {"name": "Headache", "prevalence": 13.6, "severity": "mild", "onset_day": 1},
                {"name": "Muscle Pain", "prevalence": 14.8, "severity": "moderate", "onset_day": 2},
                {"name": "Diarrhea", "prevalence": 3.7, "severity": "mild", "onset_day": 4},
            ],
            "severe_complications": [
                {"name": "Pneumonia", "prevalence": 14.0, "severity": "severe", "onset_day": 7},
                {"name": "ARDS", "prevalence": 6.1, "severity": "critical", "onset_day": 8},
                {"name": "Septic Shock", "prevalence": 4.9, "severity": "critical", "onset_day": 10},
            ]
        },
        "age_impact": {
            "0-9": {"infection_rate": 1.0, "severity_score": 0.2, "cfr": 0.0},
            "10-19": {"infection_rate": 1.2, "severity_score": 0.3, "cfr": 0.1},
            "20-29": {"infection_rate": 1.5, "severity_score": 0.4, "cfr": 0.2},
            "30-39": {"infection_rate": 1.4, "severity_score": 0.5, "cfr": 0.3},
            "40-49": {"infection_rate": 1.3, "severity_score": 0.7, "cfr": 0.5},
            "50-59": {"infection_rate": 1.2, "severity_score": 1.5, "cfr": 1.3},
            "60-69": {"infection_rate": 1.1, "severity_score": 3.0, "cfr": 3.6},
            "70-79": {"infection_rate": 1.0, "severity_score": 5.0, "cfr": 8.0},
            "80+": {"infection_rate": 0.9, "severity_score": 8.0, "cfr": 14.8},
        },
        "mutation_behavior": {
            "mutation_rate": "moderate",
            "variant_emergence_frequency": 6,  # months
            "immune_escape_potential": "high",
            "transmissibility_trend": "increasing",
        },
        "transmission": {
            "primary_route": "respiratory_droplets",
            "secondary_routes": ["aerosol", "fomites"],
            "superspreading_events": True,
            "environmental_stability": "moderate",  # hours on surfaces
        }
    },
    
    "SARS": {
        "name": "SARS (Severe Acute Respiratory Syndrome)",
        "year": 2003,
        "virus_type": "Coronavirus",
        "epidemiology": {
            "r0": 3.0,
            "incubation_period": 4.6,
            "serial_interval": 8.4,
            "case_fatality_rate": 9.6,
            "hospitalization_rate": 100.0,  # Nearly all symptomatic cases
            "asymptomatic_rate": 5.0,
        },
        "symptoms": {
            "primary": [
                {"name": "Fever", "prevalence": 99.0, "severity": "severe", "onset_day": 1},
                {"name": "Cough", "prevalence": 62.0, "severity": "moderate", "onset_day": 3},
                {"name": "Myalgia", "prevalence": 49.0, "severity": "moderate", "onset_day": 1},
                {"name": "Dyspnea", "prevalence": 42.0, "severity": "severe", "onset_day": 5},
                {"name": "Chills", "prevalence": 39.0, "severity": "moderate", "onset_day": 1},
            ],
            "secondary": [
                {"name": "Headache", "prevalence": 35.0, "severity": "mild", "onset_day": 1},
                {"name": "Diarrhea", "prevalence": 23.0, "severity": "moderate", "onset_day": 3},
                {"name": "Sore Throat", "prevalence": 13.0, "severity": "mild", "onset_day": 2},
            ],
            "severe_complications": [
                {"name": "Pneumonia", "prevalence": 90.0, "severity": "severe", "onset_day": 7},
                {"name": "ARDS", "prevalence": 20.0, "severity": "critical", "onset_day": 8},
                {"name": "Respiratory Failure", "prevalence": 20.0, "severity": "critical", "onset_day": 9},
            ]
        },
        "age_impact": {
            "0-9": {"infection_rate": 0.5, "severity_score": 0.1, "cfr": 0.0},
            "10-19": {"infection_rate": 0.6, "severity_score": 0.2, "cfr": 0.0},
            "20-29": {"infection_rate": 1.0, "severity_score": 0.5, "cfr": 1.0},
            "30-39": {"infection_rate": 1.2, "severity_score": 1.0, "cfr": 3.0},
            "40-49": {"infection_rate": 1.3, "severity_score": 2.0, "cfr": 6.0},
            "50-59": {"infection_rate": 1.2, "severity_score": 4.0, "cfr": 13.0},
            "60-69": {"infection_rate": 1.0, "severity_score": 7.0, "cfr": 43.0},
            "70-79": {"infection_rate": 0.8, "severity_score": 9.0, "cfr": 50.0},
            "80+": {"infection_rate": 0.7, "severity_score": 10.0, "cfr": 55.0},
        },
        "mutation_behavior": {
            "mutation_rate": "low",
            "variant_emergence_frequency": 0,
            "immune_escape_potential": "low",
            "transmissibility_trend": "stable",
        },
        "transmission": {
            "primary_route": "respiratory_droplets",
            "secondary_routes": ["fomites", "fecal_oral"],
            "superspreading_events": True,
            "environmental_stability": "high",
        }
    },
    
    "MERS": {
        "name": "MERS (Middle East Respiratory Syndrome)",
        "year": 2012,
        "virus_type": "Coronavirus",
        "epidemiology": {
            "r0": 0.7,  # <1 indicates limited human-to-human transmission
            "incubation_period": 5.2,
            "serial_interval": 7.6,
            "case_fatality_rate": 34.4,
            "hospitalization_rate": 95.0,
            "asymptomatic_rate": 12.0,
        },
        "symptoms": {
            "primary": [
                {"name": "Fever", "prevalence": 98.0, "severity": "severe", "onset_day": 1},
                {"name": "Cough", "prevalence": 83.0, "severity": "severe", "onset_day": 2},
                {"name": "Dyspnea", "prevalence": 72.0, "severity": "severe", "onset_day": 4},
                {"name": "Myalgia", "prevalence": 32.0, "severity": "moderate", "onset_day": 1},
            ],
            "secondary": [
                {"name": "Diarrhea", "prevalence": 26.0, "severity": "moderate", "onset_day": 3},
                {"name": "Nausea/Vomiting", "prevalence": 21.0, "severity": "mild", "onset_day": 2},
                {"name": "Abdominal Pain", "prevalence": 17.0, "severity": "moderate", "onset_day": 3},
            ],
            "severe_complications": [
                {"name": "Pneumonia", "prevalence": 89.0, "severity": "severe", "onset_day": 5},
                {"name": "ARDS", "prevalence": 50.0, "severity": "critical", "onset_day": 6},
                {"name": "Renal Failure", "prevalence": 50.0, "severity": "critical", "onset_day": 8},
                {"name": "Multi-organ Failure", "prevalence": 30.0, "severity": "critical", "onset_day": 10},
            ]
        },
        "age_impact": {
            "0-9": {"infection_rate": 0.3, "severity_score": 1.0, "cfr": 5.0},
            "10-19": {"infection_rate": 0.4, "severity_score": 1.5, "cfr": 8.0},
            "20-29": {"infection_rate": 0.8, "severity_score": 2.0, "cfr": 15.0},
            "30-39": {"infection_rate": 1.0, "severity_score": 3.0, "cfr": 20.0},
            "40-49": {"infection_rate": 1.2, "severity_score": 4.5, "cfr": 28.0},
            "50-59": {"infection_rate": 1.3, "severity_score": 6.0, "cfr": 35.0},
            "60-69": {"infection_rate": 1.4, "severity_score": 8.0, "cfr": 45.0},
            "70-79": {"infection_rate": 1.2, "severity_score": 9.0, "cfr": 52.0},
            "80+": {"infection_rate": 1.0, "severity_score": 10.0, "cfr": 60.0},
        },
        "mutation_behavior": {
            "mutation_rate": "low",
            "variant_emergence_frequency": 0,
            "immune_escape_potential": "low",
            "transmissibility_trend": "stable",
        },
        "transmission": {
            "primary_route": "respiratory_droplets",
            "secondary_routes": ["zoonotic", "nosocomial"],
            "superspreading_events": True,
            "environmental_stability": "moderate",
        }
    },
    
    "H1N1_2009": {
        "name": "H1N1 Influenza (Swine Flu)",
        "year": 2009,
        "virus_type": "Influenza A",
        "epidemiology": {
            "r0": 1.5,
            "incubation_period": 1.9,
            "serial_interval": 2.8,
            "case_fatality_rate": 0.02,  # Much lower than initially feared
            "hospitalization_rate": 2.0,
            "asymptomatic_rate": 15.0,
        },
        "symptoms": {
            "primary": [
                {"name": "Fever", "prevalence": 94.0, "severity": "moderate", "onset_day": 1},
                {"name": "Cough", "prevalence": 92.0, "severity": "moderate", "onset_day": 1},
                {"name": "Sore Throat", "prevalence": 66.0, "severity": "mild", "onset_day": 1},
                {"name": "Runny Nose", "prevalence": 53.0, "severity": "mild", "onset_day": 1},
                {"name": "Muscle Pain", "prevalence": 84.0, "severity": "moderate", "onset_day": 1},
            ],
            "secondary": [
                {"name": "Headache", "prevalence": 84.0, "severity": "moderate", "onset_day": 1},
                {"name": "Chills", "prevalence": 76.0, "severity": "moderate", "onset_day": 1},
                {"name": "Fatigue", "prevalence": 89.0, "severity": "moderate", "onset_day": 1},
                {"name": "Diarrhea", "prevalence": 25.0, "severity": "mild", "onset_day": 2},
                {"name": "Vomiting", "prevalence": 25.0, "severity": "mild", "onset_day": 2},
            ],
            "severe_complications": [
                {"name": "Pneumonia", "prevalence": 8.0, "severity": "severe", "onset_day": 5},
                {"name": "ARDS", "prevalence": 2.0, "severity": "critical", "onset_day": 6},
                {"name": "Secondary Bacterial Infection", "prevalence": 10.0, "severity": "severe", "onset_day": 7},
            ]
        },
        "age_impact": {
            "0-9": {"infection_rate": 2.0, "severity_score": 0.8, "cfr": 0.03},
            "10-19": {"infection_rate": 2.5, "severity_score": 0.5, "cfr": 0.02},
            "20-29": {"infection_rate": 2.2, "severity_score": 0.6, "cfr": 0.02},
            "30-39": {"infection_rate": 1.8, "severity_score": 0.8, "cfr": 0.03},
            "40-49": {"infection_rate": 1.5, "severity_score": 1.2, "cfr": 0.05},
            "50-59": {"infection_rate": 1.0, "severity_score": 1.8, "cfr": 0.08},
            "60-69": {"infection_rate": 0.7, "severity_score": 2.5, "cfr": 0.15},
            "70-79": {"infection_rate": 0.5, "severity_score": 3.5, "cfr": 0.25},
            "80+": {"infection_rate": 0.4, "severity_score": 4.5, "cfr": 0.40},
        },
        "mutation_behavior": {
            "mutation_rate": "high",
            "variant_emergence_frequency": 3,  # months
            "immune_escape_potential": "high",
            "transmissibility_trend": "variable",
        },
        "transmission": {
            "primary_route": "respiratory_droplets",
            "secondary_routes": ["aerosol", "fomites"],
            "superspreading_events": False,
            "environmental_stability": "low",
        }
    },
    
    "Ebola": {
        "name": "Ebola Virus Disease",
        "year": 2014,  # West Africa outbreak
        "virus_type": "Filovirus",
        "epidemiology": {
            "r0": 2.0,
            "incubation_period": 11.4,
            "serial_interval": 15.3,
            "case_fatality_rate": 50.0,  # Varies by outbreak 25-90%
            "hospitalization_rate": 90.0,
            "asymptomatic_rate": 1.0,
        },
        "symptoms": {
            "primary": [
                {"name": "Fever", "prevalence": 87.0, "severity": "severe", "onset_day": 1},
                {"name": "Fatigue", "prevalence": 76.0, "severity": "severe", "onset_day": 1},
                {"name": "Muscle Pain", "prevalence": 60.0, "severity": "severe", "onset_day": 2},
                {"name": "Headache", "prevalence": 53.0, "severity": "moderate", "onset_day": 1},
                {"name": "Vomiting", "prevalence": 68.0, "severity": "severe", "onset_day": 3},
            ],
            "secondary": [
                {"name": "Diarrhea", "prevalence": 66.0, "severity": "severe", "onset_day": 3},
                {"name": "Abdominal Pain", "prevalence": 44.0, "severity": "moderate", "onset_day": 3},
                {"name": "Unexplained Bleeding", "prevalence": 18.0, "severity": "critical", "onset_day": 5},
            ],
            "severe_complications": [
                {"name": "Hemorrhagic Manifestations", "prevalence": 40.0, "severity": "critical", "onset_day": 6},
                {"name": "Multi-organ Failure", "prevalence": 50.0, "severity": "critical", "onset_day": 8},
                {"name": "Shock", "prevalence": 45.0, "severity": "critical", "onset_day": 7},
            ]
        },
        "age_impact": {
            "0-9": {"infection_rate": 1.2, "severity_score": 8.0, "cfr": 80.0},
            "10-19": {"infection_rate": 1.1, "severity_score": 6.0, "cfr": 60.0},
            "20-29": {"infection_rate": 1.3, "severity_score": 5.0, "cfr": 45.0},
            "30-39": {"infection_rate": 1.4, "severity_score": 5.5, "cfr": 48.0},
            "40-49": {"infection_rate": 1.3, "severity_score": 6.0, "cfr": 52.0},
            "50-59": {"infection_rate": 1.1, "severity_score": 7.0, "cfr": 60.0},
            "60-69": {"infection_rate": 0.9, "severity_score": 8.5, "cfr": 70.0},
            "70-79": {"infection_rate": 0.7, "severity_score": 9.5, "cfr": 80.0},
            "80+": {"infection_rate": 0.5, "severity_score": 10.0, "cfr": 90.0},
        },
        "mutation_behavior": {
            "mutation_rate": "moderate",
            "variant_emergence_frequency": 12,
            "immune_escape_potential": "moderate",
            "transmissibility_trend": "stable",
        },
        "transmission": {
            "primary_route": "direct_contact",
            "secondary_routes": ["bodily_fluids", "contaminated_surfaces"],
            "superspreading_events": True,
            "environmental_stability": "moderate",
        }
    },
    
    "Seasonal_Flu": {
        "name": "Seasonal Influenza",
        "year": 2020,  # Representative year
        "virus_type": "Influenza A/B",
        "epidemiology": {
            "r0": 1.3,
            "incubation_period": 2.0,
            "serial_interval": 3.0,
            "case_fatality_rate": 0.1,
            "hospitalization_rate": 1.5,
            "asymptomatic_rate": 16.0,
        },
        "symptoms": {
            "primary": [
                {"name": "Fever", "prevalence": 68.0, "severity": "moderate", "onset_day": 1},
                {"name": "Cough", "prevalence": 93.0, "severity": "moderate", "onset_day": 1},
                {"name": "Sore Throat", "prevalence": 84.0, "severity": "mild", "onset_day": 1},
                {"name": "Runny Nose", "prevalence": 91.0, "severity": "mild", "onset_day": 1},
                {"name": "Muscle Aches", "prevalence": 94.0, "severity": "moderate", "onset_day": 1},
            ],
            "secondary": [
                {"name": "Headache", "prevalence": 91.0, "severity": "mild", "onset_day": 1},
                {"name": "Fatigue", "prevalence": 98.0, "severity": "moderate", "onset_day": 1},
                {"name": "Chills", "prevalence": 43.0, "severity": "mild", "onset_day": 1},
            ],
            "severe_complications": [
                {"name": "Pneumonia", "prevalence": 5.0, "severity": "severe", "onset_day": 5},
                {"name": "Bronchitis", "prevalence": 8.0, "severity": "moderate", "onset_day": 4},
            ]
        },
        "age_impact": {
            "0-9": {"infection_rate": 1.8, "severity_score": 1.2, "cfr": 0.05},
            "10-19": {"infection_rate": 2.0, "severity_score": 0.3, "cfr": 0.01},
            "20-29": {"infection_rate": 1.5, "severity_score": 0.3, "cfr": 0.01},
            "30-39": {"infection_rate": 1.2, "severity_score": 0.4, "cfr": 0.02},
            "40-49": {"infection_rate": 1.0, "severity_score": 0.6, "cfr": 0.04},
            "50-59": {"infection_rate": 0.9, "severity_score": 1.0, "cfr": 0.08},
            "60-69": {"infection_rate": 0.8, "severity_score": 2.0, "cfr": 0.20},
            "70-79": {"infection_rate": 0.7, "severity_score": 4.0, "cfr": 0.50},
            "80+": {"infection_rate": 0.6, "severity_score": 6.0, "cfr": 1.00},
        },
        "mutation_behavior": {
            "mutation_rate": "very_high",
            "variant_emergence_frequency": 1,  # months (antigenic drift)
            "immune_escape_potential": "very_high",
            "transmissibility_trend": "variable",
        },
        "transmission": {
            "primary_route": "respiratory_droplets",
            "secondary_routes": ["aerosol", "fomites"],
            "superspreading_events": False,
            "environmental_stability": "low",
        }
    }
}

# Epidemiological parameter ranges for categorization
PARAMETER_RANGES = {
    "r0": {
        "very_low": (0, 1.0),
        "low": (1.0, 1.5),
        "moderate": (1.5, 2.5),
        "high": (2.5, 4.0),
        "very_high": (4.0, 10.0)
    },
    "cfr": {
        "very_low": (0, 0.1),
        "low": (0.1, 1.0),
        "moderate": (1.0, 5.0),
        "high": (5.0, 20.0),
        "very_high": (20.0, 100.0)
    },
    "incubation_period": {
        "very_short": (0, 2.0),
        "short": (2.0, 4.0),
        "moderate": (4.0, 7.0),
        "long": (7.0, 14.0),
        "very_long": (14.0, 30.0)
    }
}

def get_pandemic_by_characteristic(characteristic, value_range):
    """
    Find historical pandemics matching specific epidemiological characteristics
    """
    matching = []
    for name, data in HISTORICAL_PANDEMICS.items():
        if characteristic in data['epidemiology']:
            val = data['epidemiology'][characteristic]
            if value_range[0] <= val <= value_range[1]:
                matching.append(name)
    return matching
