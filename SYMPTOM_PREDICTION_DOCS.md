# Symptom Prediction Module - Technical Documentation

## Overview

The **Symptom Prediction Engine** is a novel feature that uses comparative epidemiological analysis to predict probable symptom patterns for emerging viruses or future pandemic scenarios. This module addresses a critical gap in early pandemic preparedness when clinical data is limited.

## Scientific Foundation

### Methodology: The 3M Approach

Our implementation is inspired by the **Monitoring-Modelling-Managing (3M)** framework used in modern epidemiology:

1. **Monitoring**: Collect early outbreak indicators (R₀, incubation period, CFR, etc.)
2. **Modelling**: Compare parameters with historical pandemic data
3. **Managing**: Generate actionable symptom predictions for preparedness planning

### Data-Driven Comparative Analysis

Instead of attempting to predict exact biological mutations (which would require molecular modeling beyond the scope), the system:

- Analyzes epidemiological parameters of a new outbreak
- Finds similar historical pandemics using weighted similarity scoring
- Infers probable symptom profiles based on these matches
- Provides confidence scores based on the quality of matches

## Historical Pandemic Database

The module includes comprehensive data from 6 major pandemics:

| Pandemic | Year | Virus Type | R₀ | CFR | Key Characteristics |
|----------|------|------------|-----|-----|---------------------|
| **COVID-19** | 2019 | Coronavirus | 2.5 | 2.3% | High transmissibility, loss of smell/taste signature |
| **SARS** | 2003 | Coronavirus | 3.0 | 9.6% | High severity, nearly 100% hospitalization |
| **MERS** | 2012 | Coronavirus | 0.7 | 34.4% | Very high mortality, limited human transmission |
| **H1N1 (Swine Flu)** | 2009 | Influenza A | 1.5 | 0.02% | Low mortality, high transmissibility in young |
| **Ebola** | 2014 | Filovirus | 2.0 | 50% | Hemorrhagic symptoms, direct contact transmission |
| **Seasonal Flu** | 2020 | Influenza A/B | 1.3 | 0.1% | Baseline comparison for respiratory viruses |

### Data Structure

Each pandemic entry contains:

```python
{
    "epidemiology": {
        "r0": float,                    # Basic reproduction number
        "incubation_period": float,     # Days
        "serial_interval": float,       # Days between successive cases
        "case_fatality_rate": float,    # Percentage
        "hospitalization_rate": float,  # Percentage
        "asymptomatic_rate": float      # Percentage
    },
    "symptoms": {
        "primary": [                    # Main symptoms
            {
                "name": str,
                "prevalence": float,    # Percentage affected
                "severity": str,        # mild/moderate/severe/critical
                "onset_day": int        # Typical day of appearance
            }
        ],
        "secondary": [...],             # Less common symptoms
        "severe_complications": [...]   # Critical outcomes
    },
    "age_impact": {                     # Age-stratified data
        "0-9": {
            "infection_rate": float,
            "severity_score": float,
            "cfr": float
        },
        # ... other age groups
    },
    "mutation_behavior": {
        "mutation_rate": str,           # low/moderate/high/very_high
        "variant_emergence_frequency": int,  # months
        "immune_escape_potential": str,
        "transmissibility_trend": str
    },
    "transmission": {
        "primary_route": str,
        "secondary_routes": [str],
        "superspreading_events": bool,
        "environmental_stability": str
    }
}
```

## Algorithm: Similarity-Based Prediction

### Step 1: Parameter Normalization

The algorithm normalizes input parameters to comparable scales:

```python
normalized_value = value / max_range
```

Where `max_range` depends on parameter type:
- R₀: 10.0
- Incubation/serial interval: 30.0 days
- Rates (CFR, hospitalization, asymptomatic): 100%

### Step 2: Weighted Similarity Scoring

Calculates similarity using weighted Euclidean distance:

```python
similarity = 100 × (1 - sqrt(Σ(weight_i × distance_i²) / Σ(weight_i)))
```

**Feature Weights**:
- R₀: 25%
- Case Fatality Rate: 20%
- Incubation Period: 15%
- Hospitalization Rate: 15%
- Asymptomatic Rate: 15%
- Serial Interval: 10%

### Step 3: Symptom Aggregation

For the top N similar pandemics (default N=3):

1. Weight each pandemic's symptoms by its similarity score
2. Aggregate symptom prevalence across matches
3. Calculate confidence based on consistency across sources
4. Categorize as primary (>30% prevalence) or secondary (10-30%)

### Step 4: Complication Prediction

Based on Case Fatality Rate thresholds:

- **High CFR (>10%)**: Multi-organ failure, ARDS, septic shock
- **Moderate CFR (2-10%)**: Pneumonia, ARDS
- **Low CFR (<2%)**: Pneumonia, bronchitis

## Output Format

### Prediction Report Structure

```python
{
    "virus_name": str,
    "input_parameters": {
        "r0": float,
        "incubation_period": float,
        "case_fatality_rate": float,
        # ... other params
    },
    "transmissibility_category": str,  # Low/Moderate/High/Very High
    "severity_category": str,          # Low/Moderate/High/Very High
    "symptom_predictions": {
        "primary": [
            {
                "name": str,
                "predicted_prevalence": float,
                "severity": str,
                "predicted_onset_day": float,
                "confidence": float  # 0-100%
            }
        ],
        "secondary": [...],
        "severe_complications": [...]
    },
    "age_impact_predictions": {
        "0-9": {
            "predicted_infection_rate": float,
            "predicted_severity_score": float,
            "predicted_cfr": float
        },
        # ... other age groups
    },
    "similar_historical_pandemics": [
        (pandemic_name, similarity_score)
    ],
    "overall_confidence": float,  # 0-100%
    "insights": [str],           # Key actionable insights
    "disclaimer": str
}
```

## Usage Example

```python
from symptom_prediction import SymptomPredictor

# Initialize predictor
predictor = SymptomPredictor()

# Define parameters for a hypothetical new virus
new_virus = {
    'r0': 3.2,
    'incubation_period': 4.5,
    'case_fatality_rate': 1.8,
    'serial_interval': 5.0,
    'hospitalization_rate': 12.0,
    'asymptomatic_rate': 25.0
}

# Generate prediction report
report = predictor.generate_prediction_report(
    new_virus_params=new_virus,
    virus_name="Novel Coronavirus 2026"
)

# Access predictions
print(f"Transmissibility: {report['transmissibility_category']}")
print(f"Severity: {report['severity_category']}")
print(f"Confidence: {report['overall_confidence']}%")

for symptom in report['symptom_predictions']['primary']:
    print(f"- {symptom['name']}: {symptom['predicted_prevalence']}%")
```

## Integration with EpiControl AI

### Sidebar Control

Users can enable symptom prediction via a checkbox in the sidebar:

```python
enable_symptom_prediction = st.sidebar.checkbox(
    "Enable Symptom Predictor",
    value=False,
    help="Predict symptom patterns based on historical data"
)
```

### Automatic Analysis

When enabled, the system:

1. Extracts epidemiological parameters from the selected virus configuration
2. Runs the prediction engine
3. Displays comprehensive results after simulation completes
4. Shows:
   - Transmissibility and severity categories
   - Prediction confidence score
   - Primary and secondary symptoms with prevalence
   - Potential severe complications
   - Similar historical pandemics
   - Actionable insights and recommendations

## Limitations and Disclaimers

### What This Module Does

✅ Predicts **probable symptom patterns** based on epidemiological similarities  
✅ Provides **evidence-based estimates** for early preparedness planning  
✅ Identifies **historical precedents** for comparison  
✅ Offers **confidence scores** based on data quality  

### What This Module Does NOT Do

❌ Predict exact biological mutations at molecular level  
❌ Replace clinical diagnosis or medical advice  
❌ Provide certainty about individual patient outcomes  
❌ Account for novel pathogen mechanisms without historical precedent  

### Appropriate Use Cases

- **Early pandemic preparedness**: When clinical data is scarce
- **Scenario planning**: Testing response strategies for hypothetical outbreaks
- **Resource allocation**: Estimating healthcare needs based on predicted severity
- **Public health communication**: Understanding likely symptom profiles

### Inappropriate Use Cases

- Clinical diagnosis of individual patients
- Definitive prediction of specific mutations
- Replacement for laboratory confirmation
- Sole basis for critical healthcare decisions

## Scientific Basis and References

This module is inspired by established epidemiological frameworks:

1. **The 3M Approach**: Monitoring-Modelling-Managing framework for pandemic response
2. **Comparative Epidemiology**: Using historical outbreak data for prediction
3. **WHO Guidelines**: Standardized parameter definitions and measurement
4. **Peer-Reviewed Research**: Symptom prevalence data from published studies

### Data Sources

- **WHO Reports**: Official pandemic statistics and parameters
- **CDC Databases**: Case fatality rates and age-stratified data
- **Published Literature**: Peer-reviewed symptom prevalence studies
- **ECDC Reports**: European Centre for Disease Prevention and Control data

## Technical Implementation

### Files

```
symptom_prediction/
├── __init__.py              # Module initialization
├── historical_data.py       # Pandemic database (550+ lines)
└── predictor.py            # Prediction engine (350+ lines)
```

### Dependencies

- **NumPy**: Numerical computations for similarity scoring
- **Python 3.8+**: Type hints and modern syntax
- **Streamlit** (for UI integration): Display components

### Performance

- **Prediction time**: <100ms for typical query
- **Memory footprint**: ~2MB for historical database
- **Scalability**: O(N) where N = number of historical pandemics

## Future Enhancements

### Planned Features

1. **Machine Learning Integration**: Train models on larger datasets
2. **Regional Variations**: Account for geographic and demographic factors
3. **Temporal Dynamics**: Model symptom evolution over course of infection
4. **Confidence Intervals**: Statistical bounds on predictions
5. **User-Contributed Data**: Crowdsourced pandemic information

### Research Directions

- Integration with genomic data when available
- Real-time updates from ongoing outbreaks
- Bayesian inference for uncertainty quantification
- Multi-pathogen co-infection modeling

## Conclusion

The Symptom Prediction Engine represents a **unique contribution** to the EpiControl AI platform by:

- Addressing the **early data scarcity problem** in pandemic response
- Leveraging **historical knowledge** for future preparedness
- Providing **transparent, explainable predictions** with confidence scores
- Maintaining **scientific honesty** about capabilities and limitations

This feature distinguishes EpiControl AI from standard SEIR simulators by adding **predictive intelligence** that supports decision-making under uncertainty.

---

**Team Neural Nexus**  
PRAKALP 2026  
EpiControl AI Platform
