# Disease parameters (WHO-inspired, simplified)
BASE_BETA = 0.3
INCUBATION_DAYS = 5
INFECTIOUS_DAYS = 7

# Age-wise parameters
AGE_PARAMS = {
    "child": {
        "immunity": 0.6,
        "severity": 0.2,
        "contact_rate": 1.3
    },
    "adult": {
        "immunity": 0.3,
        "severity": 0.8,
        "contact_rate": 1.0
    }
}
