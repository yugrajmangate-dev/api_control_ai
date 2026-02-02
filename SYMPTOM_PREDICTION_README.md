# 🔬 Symptom Prediction Feature - Quick Guide

## What's New?

EpiControl AI now includes a **Symptom Prediction Engine** - a unique ML-based feature that predicts probable symptom patterns for emerging viruses based on historical pandemic data.

## 🎯 Key Features

### 1. **Historical Data Analysis**
- Compares your virus parameters with 6 major historical pandemics:
  - COVID-19 (2019)
  - SARS (2003)
  - MERS (2012)
  - H1N1 Swine Flu (2009)
  - Ebola (2014)
  - Seasonal Flu (2020)

### 2. **Symptom Pattern Prediction**
- **Primary Symptoms**: Most common symptoms with prevalence estimates
- **Secondary Symptoms**: Less common but significant symptoms
- **Severe Complications**: Critical outcomes based on severity
- **Onset Timelines**: Expected day of symptom appearance

### 3. **Age-Specific Impact**
- Infection rates by age group
- Severity scores for different demographics
- Case fatality rates across age ranges

### 4. **Confidence Scoring**
- Each prediction includes a confidence score (0-100%)
- Based on similarity to historical pandemics
- Transparent methodology

## 🚀 How to Use

### Step 1: Enable the Feature
1. Run the application: `streamlit run app.py`
2. In the sidebar, find **"🔬 Symptom Prediction"**
3. Check **"Enable Symptom Predictor"**

### Step 2: Configure Your Virus
1. Select a pathogen from WHO Database or Custom Models
2. Set population and duration parameters
3. Enable any other features (mutations, etc.)

### Step 3: Run Simulation
1. Click **"▶ Run Simulation"**
2. Wait for the simulation to complete
3. Scroll down to see **"🔬 Symptom Prediction Analysis"** section

### Step 4: Interpret Results

The prediction report includes:

#### **Transmissibility & Severity Categories**
- Low / Moderate / High / Very High
- Based on R₀ and Case Fatality Rate

#### **Predicted Symptoms**
Each symptom shows:
- **Name**: e.g., "Fever", "Cough", "Fatigue"
- **Predicted Prevalence**: Percentage of infected showing symptom
- **Severity**: mild / moderate / severe / critical
- **Expected Onset**: Day when symptom typically appears
- **Confidence**: How reliable the prediction is

#### **Similar Historical Pandemics**
- Top 3 most similar past outbreaks
- Similarity percentage (higher = better match)
- Detailed comparison of parameters

#### **Key Insights**
- Actionable recommendations
- Risk assessments
- Resource planning suggestions

## 📊 Example Output

```
Predictive Analysis for: COVID-19

Transmissibility: High (R₀ = 2.50)
Severity: Moderate (CFR = 2.30%)
Prediction Confidence: 95%
Closest Match: COVID-19 (96% similar)

Primary Symptoms (Expected):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fever
  Predicted Prevalence: 87.9%
  Severity: Moderate
  Expected Onset: Day 1.0
  Confidence: 100%

Dry Cough
  Predicted Prevalence: 67.7%
  Severity: Moderate
  Expected Onset: Day 2.0
  Confidence: 100%

Loss of Smell/Taste
  Predicted Prevalence: 64.0%
  Severity: Mild
  Expected Onset: Day 3.0
  Confidence: 95%

Potential Severe Complications:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pneumonia: Moderate risk (11.5%)
ARDS: Moderate risk (5.8%)

Key Insights:
⚠️ High transmissibility (R₀=2.5) suggests rapid spread
🔍 Closest match: COVID-19 (96% similarity)
```

## 🧠 Scientific Methodology

### The 3M Approach
Our implementation follows the **Monitoring-Modelling-Managing** framework:

1. **Monitoring**: Collect early outbreak indicators
2. **Modelling**: Compare with historical data
3. **Managing**: Generate actionable predictions

### Similarity Scoring Algorithm

```python
similarity = 100 × (1 - sqrt(Σ(weight × distance²) / Σ(weight)))
```

**Feature Weights:**
- R₀ (transmissibility): 25%
- Case Fatality Rate: 20%
- Incubation Period: 15%
- Hospitalization Rate: 15%
- Asymptomatic Rate: 15%
- Serial Interval: 10%

### Data Sources
- **WHO**: World Health Organization pandemic reports
- **CDC**: Centers for Disease Control databases
- **ECDC**: European Centre for Disease Prevention
- **Peer-reviewed**: Published epidemiological studies

## ⚠️ Important Disclaimers

### ✅ What This Feature Does
- Predicts **probable symptom patterns** based on epidemiological similarities
- Provides **evidence-based estimates** for preparedness planning
- Identifies **historical precedents** for comparison
- Offers **confidence scores** for transparency

### ❌ What This Feature Does NOT Do
- Predict exact biological mutations
- Replace clinical diagnosis
- Provide certainty about individual outcomes
- Account for completely novel mechanisms

### 🎯 Appropriate Use Cases
- **Early pandemic preparedness** when clinical data is limited
- **Scenario planning** for hypothetical outbreaks
- **Resource allocation** based on predicted severity
- **Public health communication** about likely symptoms

### 🚫 Inappropriate Use Cases
- Clinical diagnosis of patients
- Definitive mutation prediction
- Replacement for lab confirmation
- Sole basis for critical decisions

## 🧪 Testing the Feature

Run the test suite:

```bash
python test_symptom_prediction.py
```

This validates:
- ✅ Historical pandemic database loading
- ✅ Similarity scoring accuracy
- ✅ Symptom aggregation logic
- ✅ Age-specific predictions
- ✅ Confidence score calculation

## 📚 Complete Documentation

For detailed technical documentation, see:
- **[SYMPTOM_PREDICTION_DOCS.md](SYMPTOM_PREDICTION_DOCS.md)** - Full technical specs
- **[symptom_prediction/](symptom_prediction/)** - Module source code
  - `historical_data.py` - Pandemic database (550+ lines)
  - `predictor.py` - Prediction engine (350+ lines)

## 🎓 Research Foundation

This feature is inspired by:

1. **Fraser et al. (2009)**: "Pandemic Potential of a Strain of Influenza A (H1N1)"
2. **WHO Guidelines**: Pandemic Influenza Severity Assessment
3. **Riley et al. (2003)**: "Transmission Dynamics of SARS"
4. **Chowell et al. (2014)**: "The 3M Approach in Epidemic Forecasting"

## 💡 Tips for Best Results

1. **Use realistic parameters**: Based on early outbreak data
2. **Check confidence scores**: Higher = more reliable
3. **Review similar pandemics**: Learn from historical responses
4. **Combine with simulation**: Symptom prediction + SEIR modeling
5. **Update as data emerges**: Re-run with refined parameters

## 🏆 Why This Feature Matters

### Unique Value Proposition
- **First-of-its-kind** in hackathon SEIR simulators
- **Data-driven** predictions, not speculation
- **Transparent** methodology with confidence scores
- **Actionable** insights for decision-makers

### Real-World Impact
- Helps health systems prepare when data is scarce
- Supports early resource allocation
- Guides public health communication
- Enables evidence-based scenario planning

## 🤝 Credits

**Team Neural Nexus**  
PRAKALP 2026

**Data Sources:**
- World Health Organization (WHO)
- Centers for Disease Control (CDC)
- European Centre for Disease Prevention (ECDC)
- Various peer-reviewed epidemiological studies

---

## 📞 Support

For questions about the Symptom Prediction feature:
1. Use the **AI Chat Assistant** in the sidebar
2. Ask about "symptom prediction", "historical data", or "ML features"
3. Check the **"🔬 Features"** tab in the app

**Sample Questions:**
- "How does symptom prediction work?"
- "What historical data is used?"
- "How accurate are the predictions?"
- "What is the 3M approach?"

---

**🎯 Start predicting symptom patterns today!**

Enable the feature in the sidebar and run your first simulation with ML-powered symptom forecasting.
