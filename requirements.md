# EpiControl AI - Requirements Document

## Project Overview

**Project Name:** EpiControl AI  
**Team:** Neural Nexus  
**Event:** PRAKALP 2026 Hackathon  
**Version:** 1.0  
**Date:** January 2026

---

## 1. Problem Statement

### 1.1 Core Problem
Public health officials and epidemiologists need effective tools to:
- Simulate and predict epidemic spread patterns
- Test intervention strategies before real-world implementation
- Optimize resource allocation during disease outbreaks
- Understand the impact of virus mutations on disease dynamics
- Make data-driven decisions for epidemic control

### 1.2 Current Challenges
- Limited access to sophisticated epidemic modeling tools
- Difficulty in comparing multiple intervention strategies
- Lack of real-time mutation modeling capabilities
- Complex parameter tuning requiring epidemiological expertise
- Need for AI-driven policy optimization

---

## 2. Target Users

### 2.1 Primary Users
- **Public Health Officials**: Decision-makers requiring policy impact analysis
- **Epidemiologists**: Researchers studying disease transmission dynamics
- **Healthcare Administrators**: Planning hospital capacity and resource allocation
- **Policy Makers**: Government officials designing intervention strategies

### 2.2 Secondary Users
- **Students**: Learning epidemiological modeling concepts
- **Researchers**: Conducting comparative studies on intervention effectiveness
- **Data Scientists**: Analyzing epidemic patterns and trends

---

## 3. System Objectives

### 3.1 Primary Objectives
1. Provide accurate SEIR-based epidemic simulation
2. Enable comparison of multiple intervention strategies
3. Model realistic virus mutation dynamics
4. Offer AI-driven policy optimization using reinforcement learning
5. Deliver intuitive visualizations for complex epidemic data

### 3.2 Secondary Objectives
1. Support multiple disease types with WHO-verified parameters
2. Enable multi-language accessibility (11 languages)
3. Provide real-time symptom prediction for emerging viruses
4. Offer city-specific configurations for Indian metropolitan areas
5. Include conversational AI assistant for user guidance

---

## 4. Functional Requirements

### 4.1 Epidemic Simulation Engine
**FR-1.1** System shall implement SEIR (Susceptible-Exposed-Infected-Recovered) model  
**FR-1.2** System shall support agent-based population modeling (500-50,000 agents)  
**FR-1.3** System shall simulate disease transmission based on contact rates  
**FR-1.4** System shall track age-stratified populations (children, adults, elderly)  
**FR-1.5** System shall calculate reproduction number (R₀) dynamically  
**FR-1.6** System shall support simulation periods from 20-120 days

### 4.2 Virus Configuration
**FR-2.1** System shall provide custom virus parameter configuration  
**FR-2.2** System shall integrate WHO disease database (COVID-19, SARS, Measles, Influenza, Ebola)  
**FR-2.3** System shall support configurable parameters:
- R₀ (basic reproduction number)
- Incubation period
- Infectious period
- Mortality rate
- Transmission rate (beta)

### 4.3 Mutation Modeling
**FR-3.1** System shall simulate virus mutations during epidemic progression  
**FR-3.2** System shall trigger mutations based on infection rate thresholds  
**FR-3.3** System shall modify R₀, transmission rate, and mortality upon mutation  
**FR-3.4** System shall enforce 15-day cooldown between mutations  
**FR-3.5** System shall track and visualize mutation timeline

### 4.4 Intervention Policies
**FR-4.1** System shall support mask mandate intervention (30-50% transmission reduction)  
**FR-4.2** System shall support school closure intervention (70% child contact reduction)  
**FR-4.3** System shall support vaccination campaigns (50-85% immunity boost)  
**FR-4.4** System shall allow combination of multiple interventions  
**FR-4.5** System shall calculate economic cost of interventions

### 4.5 Control Modes
**FR-5.1** System shall provide Manual Policy mode for user-controlled interventions  
**FR-5.2** System shall provide AI (Q-Learning) mode for automated policy optimization  
**FR-5.3** System shall provide Policy Comparison mode testing 5 strategies:
- No intervention
- Masks only
- School closure only
- Vaccination only
- Full intervention (all three)

### 4.6 Reinforcement Learning Agent
**FR-6.1** System shall implement Q-Learning agent for policy optimization  
**FR-6.2** Agent shall evaluate 5 discrete actions per simulation day  
**FR-6.3** Agent shall optimize for minimal deaths and economic cost  
**FR-6.4** System shall support agent training (200+ episodes)  
**FR-6.5** System shall load pre-trained Q-tables for inference

### 4.7 Symptom Prediction
**FR-7.1** System shall predict symptom profiles for custom viruses  
**FR-7.2** System shall use ML-based similarity matching with 6 historical pandemics  
**FR-7.3** System shall provide symptom prevalence estimates  
**FR-7.4** System shall calculate confidence scores for predictions  
**FR-7.5** System shall identify similar historical pandemic matches

### 4.8 City Configurations
**FR-8.1** System shall provide preset configurations for 10 Indian cities:
- Mumbai, Delhi, Bangalore, Hyderabad, Chennai
- Kolkata, Pune, Ahmedabad, Jaipur, Lucknow
**FR-8.2** Each city preset shall include:
- Realistic population size
- Population density factor
- Healthcare capacity
- Public transport usage
- Contact rate multipliers

### 4.9 Visualization
**FR-9.1** System shall display SEIR curves (S, E, I, R over time)  
**FR-9.2** System shall generate infection density heatmaps  
**FR-9.3** System shall provide spatial scatter plots of agent distribution  
**FR-9.4** System shall show mutation timeline with parameter changes  
**FR-9.5** System shall display policy comparison bar charts  
**FR-9.6** System shall provide global epidemic surveillance map (50+ countries)  
**FR-9.7** System shall offer 3D globe view for geographic visualization

### 4.10 Conversational AI Assistant
**FR-10.1** System shall provide chatbot for user guidance  
**FR-10.2** Chatbot shall answer questions about SEIR modeling  
**FR-10.3** Chatbot shall explain visualization components  
**FR-10.4** Chatbot shall provide feature tutorials  
**FR-10.5** Chatbot shall support 11 languages

### 4.11 Multi-Language Support
**FR-11.1** System shall support 11 languages:
- English, Spanish, French, German, Hindi
- Chinese, Kannada, Marathi, Tamil, Telugu, Gujarati
**FR-11.2** System shall translate UI elements dynamically  
**FR-11.3** System shall maintain chatbot knowledge base per language

---

## 5. Non-Functional Requirements

### 5.1 Performance
**NFR-1.1** Simulation shall complete within 60 seconds for 5,000 agents over 45 days  
**NFR-1.2** Visualizations shall render within 3 seconds  
**NFR-1.3** Policy comparison mode shall complete all 5 strategies within 5 minutes  
**NFR-1.4** System shall support concurrent user sessions (Streamlit Cloud)

### 5.2 Usability
**NFR-2.1** Interface shall be intuitive for non-technical users  
**NFR-2.2** Parameter tooltips shall provide clear explanations  
**NFR-2.3** Visualizations shall be interactive (zoom, pan, hover)  
**NFR-2.4** System shall provide progress indicators for long operations  
**NFR-2.5** Error messages shall be user-friendly and actionable

### 5.3 Reliability
**NFR-3.1** System shall handle invalid parameter inputs gracefully  
**NFR-3.2** System shall provide fallback when RL features unavailable  
**NFR-3.3** System shall maintain session state across interactions  
**NFR-3.4** System shall recover from visualization rendering errors

### 5.4 Scalability
**NFR-4.1** System shall support population sizes up to 50,000 agents  
**NFR-4.2** System shall handle simulation periods up to 120 days  
**NFR-4.3** System architecture shall allow feature module additions

### 5.5 Maintainability
**NFR-5.1** Code shall follow modular architecture with clear separation  
**NFR-5.2** Configuration files shall be externalized (JSON, Python modules)  
**NFR-5.3** System shall include comprehensive inline documentation  
**NFR-5.4** Database updates shall not require code changes

### 5.6 Portability
**NFR-6.1** System shall run on Windows, macOS, and Linux  
**NFR-6.2** System shall deploy to Streamlit Cloud  
**NFR-6.3** System shall support Python 3.10+  
**NFR-6.4** Dependencies shall be managed via requirements.txt

### 5.7 Security
**NFR-7.1** System shall not store personal health information  
**NFR-7.2** System shall use placeholder data for demonstrations  
**NFR-7.3** System shall validate all user inputs  
**NFR-7.4** System shall prevent code injection attacks

---

## 6. System Architecture

### 6.1 Core Modules
- **app.py**: Main Streamlit dashboard and UI orchestration
- **env/**: SEIR model, population generation, policies, mutations, city configs
- **rl/**: Q-Learning agent, training, environment, utilities
- **simulation/**: Metrics tracking and calculation
- **visualization/**: Plotly-based charts and maps
- **symptom_prediction/**: ML-based symptom predictor
- **data/**: Virus configurations and WHO parameters
- **config/**: Base parameters for age groups

### 6.2 Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Modeling**: NumPy, Pandas
- **Visualization**: Plotly, Matplotlib
- **ML/RL**: Gymnasium, PyTorch
- **Deployment**: Streamlit Cloud, Heroku-compatible

---

## 7. Data Requirements

### 7.1 Input Data
- Virus epidemiological parameters (R₀, incubation, infectious periods)
- Population demographics (age distribution, contact rates)
- City-specific configurations (density, healthcare capacity)
- Historical pandemic data (6 diseases)
- WHO disease database (5 diseases)

### 7.2 Output Data
- SEIR time series data
- Infection metrics (peak, total deaths, recovered)
- Mutation events timeline
- Policy effectiveness comparisons
- Symptom prediction profiles

### 7.3 Data Sources
- World Health Organization (WHO)
- Centers for Disease Control (CDC)
- POLYMOD contact study
- Peer-reviewed epidemiological research

---

## 8. User Interface Requirements

### 8.1 Dashboard Layout
- Professional gradient-based theme
- Responsive multi-column layout
- Collapsible sidebar for configuration
- Tabbed interface for result organization
- Real-time progress indicators

### 8.2 Configuration Panel (Sidebar)
- Population and duration sliders
- City preset selector
- Virus source selection (Custom/WHO)
- Mutation toggle and threshold
- Intervention checkboxes
- Control mode radio buttons
- Visualization toggles
- Language selector
- Chat interface

### 8.3 Main Display Area
- Global epidemic map (flat/3D toggle)
- Quick statistics metrics
- SEIR curve visualization
- Infection heatmap
- Spatial scatter plot
- Mutation timeline
- Policy comparison charts
- Symptom prediction results

---

## 9. Success Criteria

### 9.1 Functional Success
✓ Accurate SEIR model implementation validated against known epidemics  
✓ All 5 intervention policies functional and measurable  
✓ Mutation system triggers and modifies parameters correctly  
✓ RL agent reduces deaths by 20%+ vs no intervention  
✓ Policy comparison identifies optimal strategy  
✓ Symptom predictor achieves 70%+ accuracy on test cases

### 9.2 User Experience Success
✓ 90%+ users can run simulation without documentation  
✓ Average simulation completion time < 2 minutes  
✓ Chatbot answers 80%+ common questions correctly  
✓ Visualizations load without errors 95%+ of time

### 9.3 Technical Success
✓ System deploys successfully to Streamlit Cloud  
✓ Zero critical bugs in production  
✓ Code coverage > 60% for core modules  
✓ Performance benchmarks met for all population sizes

---

## 10. Constraints and Assumptions

### 10.1 Constraints
- Limited to agent-based modeling (not continuous differential equations)
- Maximum population size constrained by computational resources
- RL training requires significant time (hours for convergence)
- Symptom prediction limited to 6 historical pandemic references
- Deployment platform (Streamlit Cloud) has resource limits

### 10.2 Assumptions
- Users have basic understanding of epidemiological concepts
- Internet connectivity available for web deployment
- Python 3.10+ environment available for local deployment
- Users accept simulation results as educational, not clinical
- WHO/CDC data remains accessible and current

---

## 11. Future Enhancements

### 11.1 Planned Features
- Multi-region simulation with travel dynamics
- Hospital capacity modeling with ICU tracking
- Economic impact detailed modeling
- Social network-based contact patterns
- Real-time data integration from public health APIs
- Mobile-responsive interface
- Export simulation results to PDF/CSV
- Custom intervention policy builder

### 11.2 Research Extensions
- Deep reinforcement learning (DQN, PPO)
- Multi-agent RL for distributed policy making
- Genetic algorithm for parameter optimization
- Integration with real-world epidemic data streams
- Predictive analytics for outbreak forecasting

---

## 12. Acceptance Criteria

### 12.1 Minimum Viable Product (MVP)
- [ ] SEIR simulation runs successfully
- [ ] Manual policy mode functional
- [ ] Basic visualizations display correctly
- [ ] WHO database integrated
- [ ] Deployed to Streamlit Cloud

### 12.2 Full Release
- [ ] All 3 control modes operational
- [ ] Mutation system functional
- [ ] Symptom prediction working
- [ ] All 10 city presets available
- [ ] 11 languages supported
- [ ] Chatbot responsive
- [ ] All visualizations rendering
- [ ] Documentation complete

---

## 13. Glossary

**SEIR Model**: Epidemiological model dividing population into Susceptible, Exposed, Infected, Recovered  
**R₀ (R-naught)**: Basic reproduction number - average infections caused by one infected person  
**Beta (β)**: Transmission rate parameter  
**CFR**: Case Fatality Rate - percentage of infected who die  
**Q-Learning**: Model-free reinforcement learning algorithm  
**Agent-based Model**: Simulation where individuals are modeled as autonomous agents  
**Herd Immunity**: Indirect protection when sufficient population is immune  
**Incubation Period**: Time from exposure to symptom onset  
**Infectious Period**: Duration person can transmit disease

---

## Document Control

**Version History:**
- v1.0 (January 2026): Initial requirements document

**Approval:**
- Team Lead: Parth Bhad
- Team: Neural Nexus

**References:**
- WHO Disease Parameters Database
- CDC Epidemiological Guidelines
- POLYMOD Contact Study
- PRAKALP 2026 Hackathon Guidelines

---

*This document serves as the comprehensive requirements specification for EpiControl AI platform.*
