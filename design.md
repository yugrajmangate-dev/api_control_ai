# EpiControl AI - System Design Document

## Project Overview

**Project Name:** EpiControl AI  
**Team:** Neural Nexus  
**Event:** PRAKALP 2026 Hackathon  
**Version:** 1.0  
**Date:** January 2026  
**Document Type:** Technical Design Specification

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Architecture](#2-system-architecture)
3. [Module Design](#3-module-design)
4. [Data Models](#4-data-models)
5. [Algorithm Design](#5-algorithm-design)
6. [User Interface Design](#6-user-interface-design)
7. [Database Design](#7-database-design)
8. [API Design](#8-api-design)
9. [Security Design](#9-security-design)
10. [Performance Design](#10-performance-design)
11. [Deployment Architecture](#11-deployment-architecture)
12. [Testing Strategy](#12-testing-strategy)

---

## 1. Introduction

### 1.1 Purpose
This document provides the technical design specification for EpiControl AI, an advanced epidemic simulation and control platform combining SEIR epidemiological modeling with reinforcement learning for policy optimization.

### 1.2 Scope
The design covers:
- System architecture and component interactions
- Module-level design and interfaces
- Data structures and algorithms
- User interface design patterns
- Deployment and scalability considerations

### 1.3 Design Principles
- **Modularity**: Clear separation of concerns across modules
- **Extensibility**: Easy addition of new diseases, policies, and features
- **Performance**: Optimized for simulations up to 50,000 agents
- **Usability**: Intuitive interface for non-technical users
- **Maintainability**: Clean code with comprehensive documentation


---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
│                    (Streamlit Dashboard - app.py)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Configuration│  │ Visualization│  │   Chatbot    │          │
│  │    Panel     │  │   Display    │  │  Interface   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Logic Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Simulation   │  │      RL      │  │   Symptom    │          │
│  │   Engine     │  │    Agent     │  │  Predictor   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Core Engine Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ SEIR Model   │  │  Population  │  │   Mutation   │          │
│  │   Engine     │  │  Generator   │  │    System    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Policies   │  │    Metrics   │  │     City     │          │
│  │   Manager    │  │   Tracker    │  │   Configs    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Data Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Virus     │  │     WHO      │  │  Historical  │          │
│  │   Configs    │  │  Parameters  │  │   Pandemic   │          │
│  │              │  │    (JSON)    │  │     Data     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │     Base     │  │   Q-Table    │                            │
│  │  Parameters  │  │   (Pickle)   │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Architecture Patterns

**Pattern 1: Model-View-Controller (MVC)**
- **Model**: SEIR engine, population data, metrics
- **View**: Streamlit UI components, Plotly visualizations
- **Controller**: app.py orchestration logic

**Pattern 2: Strategy Pattern**
- Used for policy selection (Manual, AI, Comparison)
- Allows runtime switching between control strategies

**Pattern 3: Observer Pattern**
- Metrics tracking observes simulation state changes
- Real-time updates to visualization components

**Pattern 4: Factory Pattern**
- Population generation with configurable parameters
- Virus configuration instantiation

### 2.3 Component Interaction Flow

```
User Input → Configuration → Simulation Engine → SEIR Update Loop
                                    ↓
                            Policy Application
                                    ↓
                            Mutation Check
                                    ↓
                            Metrics Recording
                                    ↓
                            Visualization → Display
```


---

## 3. Module Design

### 3.1 Core Modules Overview

| Module | File Path | Responsibility | Dependencies |
|--------|-----------|----------------|--------------|
| Main Dashboard | `app.py` | UI orchestration, user interaction | All modules |
| SEIR Engine | `env/seir.py` | Disease state transitions | numpy, population |
| Population | `env/population.py` | Agent generation and management | numpy, config |
| Policies | `env/policies.py` | Intervention implementation | population |
| Mutation | `env/mutation.py` | Virus evolution logic | seir, population |
| City Configs | `env/city.py` | Geographic presets | None |
| RL Agent | `rl/agent.py` | Q-Learning implementation | gymnasium, numpy |
| RL Environment | `rl/env.py` | Gymnasium-compatible env | seir, policies |
| Metrics | `simulation/metrics.py` | Performance tracking | numpy, pandas |
| Visualizations | `visualization/plotly_plots.py` | Chart generation | plotly, pandas |
| Symptom Predictor | `symptom_prediction/predictor.py` | ML-based prediction | numpy, historical_data |
| Chatbot | `chatbot.py` | Conversational assistant | translations |
| Translations | `translations.py` | Multi-language support | None |

### 3.2 Module: SEIR Engine (`env/seir.py`)

**Purpose**: Core epidemiological model implementing state transitions

**Key Functions**:
```python
def set_virus_params(config: dict) -> None:
    """Set global virus parameters for simulation"""
    
def seed_infection(population: np.ndarray, initial_infected: int) -> None:
    """Initialize infection in random agents"""
    
def update_seir(population: np.ndarray, 
                mutation_tracker: dict = None,
                current_day: int = 0) -> None:
    """Execute one day of SEIR state transitions"""
```

**State Transition Logic**:
1. **S → E (Susceptible to Exposed)**
   - Calculate contact probability based on spatial proximity
   - Apply transmission rate (beta) and immunity factors
   - Check for successful infection

2. **E → I (Exposed to Infected)**
   - Check if incubation period elapsed
   - Transition to infectious state

3. **I → R (Infected to Recovered)**
   - Check if infectious period elapsed
   - Apply mortality rate for death probability
   - Transition survivors to recovered

**Data Structures**:
```python
# Population array structure (NumPy structured array)
population = np.array([
    (x, y, age_group, state, immunity, contact_rate, 
     days_in_state, severity, vaccinated)
], dtype=[
    ('x', 'f4'), ('y', 'f4'),
    ('age_group', 'U10'),
    ('state', 'U1'),  # S, E, I, R
    ('immunity', 'f4'),
    ('contact_rate', 'f4'),
    ('days_in_state', 'i4'),
    ('severity', 'f4'),
    ('vaccinated', 'bool')
])
```

### 3.3 Module: Population Generator (`env/population.py`)

**Purpose**: Create agent-based population with realistic demographics

**Key Functions**:
```python
def generate_population(size: int, virus_config: dict) -> np.ndarray:
    """Generate population with age-stratified attributes"""
```

**Age Distribution**:
- Children (0-17): 30% of population
- Adults (18-64): 55% of population
- Elderly (65+): 15% of population

**Attribute Assignment**:
- **Spatial Distribution**: Uniform random (0-100, 0-100)
- **Contact Rates**: Age-specific (children: 10.4, adults: 8.0, elderly: 6.5)
- **Immunity**: Base + age-specific boost
- **Severity**: Age-dependent disease severity

### 3.4 Module: Policy Manager (`env/policies.py`)

**Purpose**: Implement intervention strategies

**Key Functions**:
```python
def apply_policy(population: np.ndarray, 
                 policy: dict,
                 virus_config: dict) -> None:
    """Apply single policy to population"""
    
def apply_policy_batch(population: np.ndarray,
                       policy: dict,
                       virus_config: dict) -> None:
    """Optimized batch policy application"""
```

**Policy Effects**:

| Policy | Target | Effect | Implementation |
|--------|--------|--------|----------------|
| Mask Mandate | All agents | -40% contact rate | Multiply contact_rate by 0.6 |
| School Closure | Children | -70% contact rate | Additional 0.3 multiplier for age_group='child' |
| Vaccination | Unvaccinated | +50-85% immunity | Increase immunity, set vaccinated=True |

**Economic Cost Model**:
```python
cost = {
    'mask_mandate': 0.05 * population_size,
    'school_closure': 0.10 * population_size,
    'vaccination': 0.15 * population_size
}
```


### 3.5 Module: Mutation System (`env/mutation.py`)

**Purpose**: Model realistic virus evolution during epidemics

**Key Functions**:
```python
def reset_mutation_tracker() -> dict:
    """Initialize mutation tracking state"""
    
def check_and_apply_mutation(population: np.ndarray,
                             mutation_tracker: dict,
                             current_day: int,
                             threshold: float = 0.30) -> bool:
    """Check conditions and trigger mutation if met"""
```

**Mutation Trigger Conditions**:
1. Infection rate > threshold (default 30%)
2. Cooldown period elapsed (15 days since last mutation)
3. Random probability check (50% chance when conditions met)

**Parameter Modifications**:
```python
# R0 change: ±10-30%
new_R0 = current_R0 * (1 + random.uniform(-0.30, 0.30))

# Transmission rate: ±15-25%
new_beta = current_beta * (1 + random.uniform(-0.25, 0.25))

# Mortality rate: ±5-15%
new_mortality = current_mortality * (1 + random.uniform(-0.15, 0.15))
```

**Mutation Event Record**:
```python
mutation_event = {
    'day': current_day,
    'old_R0': old_R0,
    'new_R0': new_R0,
    'old_beta': old_beta,
    'new_beta': new_beta,
    'old_mortality': old_mortality,
    'new_mortality': new_mortality,
    'infection_rate': current_infection_rate
}
```

### 3.6 Module: RL Agent (`rl/agent.py`)

**Purpose**: Q-Learning agent for optimal policy selection

**Algorithm**: Tabular Q-Learning with ε-greedy exploration

**State Space** (Discretized):
- Infected ratio: [0-5%, 5-15%, 15-30%, 30%+] → 4 bins
- Child infected: [0-10%, 10-25%, 25%+] → 3 bins
- Adult infected: [0-10%, 10-25%, 25%+] → 3 bins
- Hospital load: [0-50%, 50-80%, 80%+] → 3 bins
- Economic cost: [Low, Medium, High] → 3 bins

**Total States**: 4 × 3 × 3 × 3 × 3 = 324 states

**Action Space**:
```python
actions = {
    0: "No action",
    1: "Mask mandate",
    2: "School closure",
    3: "Mask + School closure",
    4: "Vaccination"
}
```

**Q-Learning Update**:
```python
Q(s, a) ← Q(s, a) + α[r + γ max Q(s', a') - Q(s, a)]

where:
  α = learning rate (0.1)
  γ = discount factor (0.95)
  r = reward (negative deaths + economic cost)
```

**Reward Function**:
```python
reward = -1.0 * (new_deaths + 0.1 * economic_cost)
```

**Training Parameters**:
- Episodes: 200
- Max steps per episode: 45 days
- Initial ε: 1.0 (100% exploration)
- Final ε: 0.01 (1% exploration)
- ε decay: Linear over episodes

### 3.7 Module: Symptom Predictor (`symptom_prediction/predictor.py`)

**Purpose**: ML-based symptom profile prediction for emerging viruses

**Algorithm**: Weighted Euclidean Distance Similarity

**Feature Vector**:
```python
features = [
    'R0',                    # Basic reproduction number
    'CFR',                   # Case fatality rate
    'incubation_days',       # Incubation period
    'infectious_days',       # Infectious duration
    'transmission_route',    # Encoded: respiratory=1, contact=2, etc.
    'severity_score'         # Composite severity metric
]
```

**Similarity Calculation**:
```python
# Feature weights (importance)
weights = {
    'R0': 0.25,
    'CFR': 0.30,
    'incubation_days': 0.15,
    'infectious_days': 0.10,
    'transmission_route': 0.10,
    'severity_score': 0.10
}

# Weighted Euclidean distance
distance = sqrt(sum(w_i * (x_i - y_i)^2))

# Similarity score (inverse distance)
similarity = 1 / (1 + distance)
```

**Prediction Process**:
1. Extract features from input virus parameters
2. Calculate similarity to all 6 historical pandemics
3. Rank by similarity score
4. Weighted average of top 3 matches for symptom prevalence
5. Generate confidence score based on similarity distribution

**Output Structure**:
```python
prediction = {
    'primary_symptoms': [
        {'name': 'Fever', 'prevalence': 0.85, 'onset_day': 2},
        {'name': 'Cough', 'prevalence': 0.75, 'onset_day': 3}
    ],
    'secondary_symptoms': [...],
    'severe_complications': [...],
    'age_specific_impact': {...},
    'confidence_score': 0.78,
    'similar_pandemics': [
        {'name': 'COVID-19', 'similarity': 0.82},
        {'name': 'SARS', 'similarity': 0.71}
    ]
}
```


---

## 4. Data Models

### 4.1 Agent Data Model

**Structure**: NumPy Structured Array

```python
Agent = {
    'x': float32,              # X coordinate (0-100)
    'y': float32,              # Y coordinate (0-100)
    'age_group': string,       # 'child', 'adult', 'elderly'
    'state': char,             # 'S', 'E', 'I', 'R'
    'immunity': float32,       # 0.0 to 1.0
    'contact_rate': float32,   # Daily contacts (4.0-12.0)
    'days_in_state': int32,    # Days in current SEIR state
    'severity': float32,       # Disease severity (0.0-1.0)
    'vaccinated': bool         # Vaccination status
}
```

**Memory Footprint**: ~40 bytes per agent
- 5,000 agents ≈ 200 KB
- 50,000 agents ≈ 2 MB

### 4.2 Virus Configuration Model

```python
VirusConfig = {
    'name': str,
    'R0': float,                    # Basic reproduction number (1.0-5.0)
    'incubation_days': int,         # Days before infectious (2-14)
    'infectious_days': int,         # Days of infectiousness (5-14)
    'base_beta': float,             # Transmission rate (0.01-0.10)
    'mortality_rate': float,        # Case fatality rate (0.001-0.50)
    'child_immunity_boost': float,  # Additional immunity for children
    'adult_severity': float         # Severity multiplier for adults
}
```

**Example Configurations**:
```python
COVID_19 = {
    'R0': 2.5,
    'incubation_days': 5,
    'infectious_days': 7,
    'base_beta': 0.045,
    'mortality_rate': 0.023,
    'child_immunity_boost': 0.20,
    'adult_severity': 0.80
}

EBOLA = {
    'R0': 2.0,
    'incubation_days': 8,
    'infectious_days': 10,
    'base_beta': 0.055,
    'mortality_rate': 0.50,
    'child_immunity_boost': 0.05,
    'adult_severity': 0.95
}
```

### 4.3 Metrics Data Model

```python
Metrics = {
    'day': List[int],
    'susceptible': List[int],
    'exposed': List[int],
    'infected': List[int],
    'recovered': List[int],
    'deaths': List[int],
    'new_infections': List[int],
    'Rt': List[float],              # Effective reproduction number
    'attack_rate': List[float],     # Cumulative infection rate
    'hospital_load': List[float]    # Healthcare capacity usage
}
```

### 4.4 Policy Data Model

```python
Policy = {
    'mask_mandate': bool,
    'school_closure': bool,
    'vaccination': bool,
    'economic_cost': float,
    'effectiveness': float          # Calculated post-simulation
}
```

### 4.5 City Configuration Model

```python
CityConfig = {
    'name': str,
    'population_size': int,
    'density': str,                 # 'very_high', 'high', 'medium'
    'healthcare_capacity': float,   # 0.0-1.0
    'public_transport_usage': float,# 0.0-1.0
    'contact_multiplier': float,    # Density-based multiplier
    'days': int,                    # Recommended simulation days
    'description': str
}
```

### 4.6 Q-Table Data Model

```python
QTable = {
    'state_space': Dict[Tuple[int, ...], int],  # State tuple → state_id
    'q_values': np.ndarray,                      # Shape: (324, 5)
    'visit_counts': np.ndarray,                  # Shape: (324, 5)
    'metadata': {
        'episodes_trained': int,
        'final_epsilon': float,
        'avg_reward': float,
        'virus_name': str
    }
}
```


---

## 5. Algorithm Design

### 5.1 SEIR State Transition Algorithm

```
Algorithm: SEIR_Update(population, virus_params, day)
Input: population array, virus configuration, current day
Output: Updated population with new states

1. FOR each agent i in population:
   
   2. IF agent.state == 'S' (Susceptible):
      3. infected_neighbors = COUNT(agents within contact_radius AND state='I')
      4. infection_prob = 1 - (1 - beta)^(infected_neighbors * contact_rate)
      5. infection_prob *= (1 - immunity)
      6. IF random() < infection_prob:
         7. agent.state = 'E'
         8. agent.days_in_state = 0
   
   9. ELSE IF agent.state == 'E' (Exposed):
      10. agent.days_in_state += 1
      11. IF agent.days_in_state >= incubation_days:
          12. agent.state = 'I'
          13. agent.days_in_state = 0
   
   14. ELSE IF agent.state == 'I' (Infected):
       15. agent.days_in_state += 1
       16. IF agent.days_in_state >= infectious_days:
           17. death_prob = mortality_rate * severity
           18. IF random() < death_prob:
               19. agent.state = 'D' (Dead)
           20. ELSE:
               21. agent.state = 'R'
               22. agent.immunity = 0.95
   
   23. ELSE IF agent.state == 'R' (Recovered):
       24. CONTINUE (no state change)

25. RETURN population
```

**Time Complexity**: O(n²) for contact checking, O(n) with spatial optimization
**Space Complexity**: O(n) for population array

### 5.2 Contact Detection Optimization

**Naive Approach**: Check all pairs → O(n²)

**Optimized Approach**: Spatial Grid Partitioning

```
Algorithm: Spatial_Grid_Contact_Detection(population, radius)
Input: population array, contact radius
Output: Contact pairs

1. grid_size = 100 / radius
2. grid = CREATE 2D grid of size (grid_size × grid_size)

3. FOR each agent in population:
   4. grid_x = floor(agent.x / radius)
   5. grid_y = floor(agent.y / radius)
   6. grid[grid_x][grid_y].append(agent)

7. contacts = []
8. FOR each cell in grid:
   9. FOR each agent in cell:
      10. FOR each neighbor_cell in adjacent_cells(cell):
          11. FOR each other_agent in neighbor_cell:
              12. IF distance(agent, other_agent) < radius:
                  13. contacts.append((agent, other_agent))

14. RETURN contacts
```

**Time Complexity**: O(n) average case
**Space Complexity**: O(n + grid_cells)

### 5.3 Mutation Trigger Algorithm

```
Algorithm: Check_Mutation(population, tracker, day, threshold)
Input: population, mutation tracker, current day, infection threshold
Output: Boolean (mutation occurred)

1. infected_count = COUNT(agent.state == 'I' for agent in population)
2. infection_rate = infected_count / len(population)

3. IF infection_rate < threshold:
   4. RETURN False

5. days_since_last = day - tracker['last_mutation_day']
6. IF days_since_last < 15:  # Cooldown period
   7. RETURN False

8. IF random() < 0.5:  # 50% chance when conditions met
   9. RETURN False

10. # Apply mutation
11. R0_change = uniform(-0.30, 0.30)
12. beta_change = uniform(-0.25, 0.25)
13. mortality_change = uniform(-0.15, 0.15)

14. virus_params['R0'] *= (1 + R0_change)
15. virus_params['base_beta'] *= (1 + beta_change)
16. virus_params['mortality_rate'] *= (1 + mortality_change)

17. tracker['last_mutation_day'] = day
18. tracker['mutations'].append(mutation_event)

19. RETURN True
```

### 5.4 Q-Learning Training Algorithm

```
Algorithm: Train_QL_Agent(env, episodes, alpha, gamma, epsilon_decay)
Input: Environment, number of episodes, learning rate, discount factor
Output: Trained Q-table

1. Q = INITIALIZE Q-table with zeros (324 states × 5 actions)
2. epsilon = 1.0

3. FOR episode in range(episodes):
   
   4. state = env.reset()
   5. total_reward = 0
   
   6. FOR step in range(max_steps):
      
      7. # Epsilon-greedy action selection
      8. IF random() < epsilon:
         9. action = random_choice(actions)
      10. ELSE:
          11. action = argmax(Q[state, :])
      
      12. next_state, reward, done = env.step(action)
      
      13. # Q-learning update
      14. best_next_action = argmax(Q[next_state, :])
      15. td_target = reward + gamma * Q[next_state, best_next_action]
      16. td_error = td_target - Q[state, action]
      17. Q[state, action] += alpha * td_error
      
      18. state = next_state
      19. total_reward += reward
      
      20. IF done:
          21. BREAK
   
   22. # Decay epsilon
   23. epsilon = max(0.01, epsilon - epsilon_decay)
   
   24. IF episode % 10 == 0:
       25. PRINT("Episode {episode}, Reward: {total_reward}, Epsilon: {epsilon}")

26. RETURN Q
```

**Convergence**: Typically 150-200 episodes
**Training Time**: ~2-3 hours for 200 episodes

### 5.5 Symptom Prediction Algorithm

```
Algorithm: Predict_Symptoms(virus_params, historical_db)
Input: Virus parameters, historical pandemic database
Output: Predicted symptom profile with confidence

1. features = EXTRACT_FEATURES(virus_params)
2. similarities = []

3. FOR each historical_pandemic in historical_db:
   4. hist_features = EXTRACT_FEATURES(historical_pandemic)
   5. distance = WEIGHTED_EUCLIDEAN(features, hist_features)
   6. similarity = 1 / (1 + distance)
   7. similarities.append((historical_pandemic, similarity))

8. similarities = SORT(similarities, by=similarity, descending=True)
9. top_matches = similarities[:3]

10. # Weighted average of symptom profiles
11. predicted_symptoms = {}
12. total_weight = SUM(match.similarity for match in top_matches)

13. FOR symptom in all_symptoms:
    14. weighted_prevalence = 0
    15. FOR match in top_matches:
        16. weight = match.similarity / total_weight
        17. prevalence = match.pandemic.symptoms[symptom].prevalence
        18. weighted_prevalence += weight * prevalence
    19. predicted_symptoms[symptom] = weighted_prevalence

20. # Calculate confidence
21. confidence = (top_matches[0].similarity - top_matches[2].similarity) / 2
22. confidence = CLAMP(confidence, 0.0, 1.0)

23. RETURN {
    'symptoms': predicted_symptoms,
    'confidence': confidence,
    'similar_pandemics': top_matches
}
```

**Time Complexity**: O(k × m) where k = historical pandemics, m = symptoms
**Space Complexity**: O(k + m)


---

## 6. User Interface Design

### 6.1 Layout Architecture

**Framework**: Streamlit (Python-based web framework)

**Layout Structure**:
```
┌─────────────────────────────────────────────────────────────┐
│                         Header Banner                        │
│              EpiControl AI | Team Neural Nexus               │
│                    Quick Stats Metrics                       │
└─────────────────────────────────────────────────────────────┘
┌──────────────┬──────────────────────────────────────────────┐
│              │                                               │
│   Sidebar    │           Main Content Area                  │
│              │                                               │
│  Language    │  ┌─────────────────────────────────────┐    │
│  Selector    │  │   Global Epidemic Map               │    │
│              │  │   (Flat / 3D Globe Toggle)          │    │
│  Config      │  └─────────────────────────────────────┘    │
│  Parameters  │                                               │
│              │  ┌─────────────────────────────────────┐    │
│  City        │  │   Simulation Results                │    │
│  Selection   │  │   - SEIR Curves                     │    │
│              │  │   - Infection Heatmap               │    │
│  Virus       │  │   - Spatial Scatter                 │    │
│  Config      │  │   - Mutation Timeline               │    │
│              │  │   - Policy Comparison               │    │
│  Mutations   │  │   - Symptom Predictions             │    │
│              │  └─────────────────────────────────────┘    │
│  Policies    │                                               │
│              │  ┌─────────────────────────────────────┐    │
│  Control     │  │   Key Metrics Summary               │    │
│  Mode        │  │   Peak | Deaths | Recovered | Rt   │    │
│              │  └─────────────────────────────────────┘    │
│  Viz         │                                               │
│  Options     │                                               │
│              │                                               │
│  Chatbot     │                                               │
│  Interface   │                                               │
│              │                                               │
│  [Run Sim]   │                                               │
│              │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

### 6.2 Color Scheme and Theming

**Primary Colors**:
- Primary: `#667eea` (Purple-blue)
- Secondary: `#764ba2` (Deep purple)
- Accent: `#f093fb` (Pink)
- Success: `#059669` (Green)
- Warning: `#f59e0b` (Orange)
- Error: `#dc2626` (Red)

**SEIR State Colors**:
- Susceptible: `#3b82f6` (Blue)
- Exposed: `#fbbf24` (Yellow)
- Infected: `#ef4444` (Red)
- Recovered: `#10b981` (Green)

**Gradient Backgrounds**:
```css
background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
animation: gradient-shift 15s ease infinite;
```

### 6.3 Component Design Specifications

**Metric Cards**:
```
┌─────────────────────────────┐
│  📊 Peak Infected           │
│                             │
│      2,345                  │
│      ↑ 12.3%                │
│                             │
│  Day 23 of simulation       │
└─────────────────────────────┘
```

**Configuration Sliders**:
```
Population Size
[====●=================] 5,000
Min: 500        Max: 50,000
```

**Policy Checkboxes**:
```
☑ Mask Mandate        (-40% transmission)
☐ School Closure      (-70% child contacts)
☑ Vaccination         (+50-85% immunity)
```

**Control Mode Radio Buttons**:
```
◉ Manual Policy
○ AI (RL) Policy
○ Policy Comparison
```

### 6.4 Visualization Design

**SEIR Curve Chart**:
- Type: Multi-line time series
- X-axis: Days (0 to simulation_days)
- Y-axis: Population count
- Lines: 4 (S, E, I, R) with distinct colors
- Interactive: Hover tooltips, zoom, pan
- Legend: Top-right corner

**Infection Heatmap**:
- Type: 2D density heatmap
- Dimensions: 100×100 grid
- Color scale: Blue (low) → Yellow → Red (high)
- Colorbar: Right side with scale
- Interactive: Hover shows exact count

**Spatial Scatter Plot**:
- Type: 2D scatter with color coding
- X-axis: X coordinate (0-100)
- Y-axis: Y coordinate (0-100)
- Point color: SEIR state
- Point size: 5px
- Interactive: Hover shows agent details

**Mutation Timeline**:
- Type: Vertical timeline with markers
- Events: Mutation occurrences
- Details: R₀ change, mortality change
- Color: Gradient based on severity

**Policy Comparison Bar Chart**:
- Type: Grouped horizontal bar chart
- Groups: 5 policies
- Metrics: Deaths, Peak Infected, Economic Cost
- Color: Policy-specific
- Interactive: Click to highlight

### 6.5 Responsive Design Considerations

**Desktop (>1200px)**:
- Sidebar: 300px fixed width
- Main content: Remaining width
- Charts: Full width with 2-column layout for smaller charts

**Tablet (768px - 1200px)**:
- Sidebar: Collapsible
- Main content: Full width
- Charts: Single column, full width

**Mobile (<768px)**:
- Sidebar: Hidden by default, slide-in menu
- Main content: Full width, vertical scroll
- Charts: Simplified, touch-optimized

### 6.6 Animation and Transitions

**Page Load**:
- Fade-in animation (0.8s)
- Staggered component appearance

**Simulation Progress**:
- Progress bar with percentage
- Animated gradient background
- Status text updates

**Chart Rendering**:
- Smooth fade-in (0.5s)
- Data point animation (line drawing effect)

**Hover Effects**:
- Metric cards: Lift effect (translateY -5px)
- Buttons: Scale and shadow increase
- Charts: Highlight on hover


---

## 7. Database Design

### 7.1 Data Storage Strategy

**Storage Types**:
1. **Static Configuration Data**: Python modules (`.py`)
2. **Structured Parameters**: JSON files (`.json`)
3. **Trained Models**: Pickle files (`.pkl`)
4. **Session State**: Streamlit session state (in-memory)

### 7.2 Virus Configuration Database

**File**: `data/virus_configs.py`

**Structure**:
```python
VIRUS_CONFIGS = {
    'COVID-19': {
        'R0': 2.5,
        'incubation_days': 5,
        'infectious_days': 7,
        'base_beta': 0.045,
        'mortality_rate': 0.023,
        'child_immunity_boost': 0.20,
        'adult_severity': 0.80
    },
    'SARS': {...},
    'Influenza': {...},
    'Measles': {...},
    'Ebola': {...}
}
```

**Access Pattern**: Direct dictionary lookup
**Update Frequency**: Rare (only for new diseases)
**Size**: ~5 KB

### 7.3 WHO Parameters Database

**File**: `data/who_params.json`

**Structure**:
```json
{
  "COVID-19": {
    "disease_name": "COVID-19 (SARS-CoV-2)",
    "R0": 2.5,
    "incubation_days": 5,
    "infectious_days": 7,
    "base_beta": 0.045,
    "mortality_rate": 0.023,
    "source": "WHO",
    "last_updated": "2024-01"
  },
  "SARS": {...}
}
```

**Access Pattern**: JSON load at startup
**Update Frequency**: Monthly (WHO data updates)
**Size**: ~3 KB

### 7.4 Historical Pandemic Database

**File**: `symptom_prediction/historical_data.py`

**Structure**:
```python
HISTORICAL_PANDEMICS = {
    'COVID-19': {
        'epidemiological_params': {
            'R0': 2.5,
            'CFR': 0.023,
            'incubation_days': 5,
            'infectious_days': 7,
            'transmission_route': 'respiratory'
        },
        'symptoms': {
            'fever': {'prevalence': 0.88, 'onset_day': 1, 'duration': 7},
            'cough': {'prevalence': 0.68, 'onset_day': 2, 'duration': 14},
            'loss_of_smell': {'prevalence': 0.64, 'onset_day': 4, 'duration': 21},
            # ... more symptoms
        },
        'age_impact': {
            'children': {'hospitalization': 0.01, 'mortality': 0.001},
            'adults': {'hospitalization': 0.05, 'mortality': 0.015},
            'elderly': {'hospitalization': 0.20, 'mortality': 0.08}
        },
        'complications': [...]
    },
    'SARS': {...},
    'MERS': {...},
    'H1N1': {...},
    'Ebola': {...},
    'Seasonal_Flu': {...}
}
```

**Access Pattern**: Load at predictor initialization
**Update Frequency**: Quarterly (new research data)
**Size**: ~15 KB

### 7.5 City Configuration Database

**File**: `env/city.py`

**Structure**:
```python
CITY_CONFIGS = {
    'Mumbai': {
        'population_size': 10000,
        'density': 'very_high',
        'healthcare_capacity': 0.65,
        'public_transport_usage': 0.85,
        'contact_multiplier': 1.4,
        'days': 60,
        'description': 'Financial capital, very high density...'
    },
    'Delhi': {...},
    # ... 8 more cities
}
```

**Access Pattern**: Direct lookup by city name
**Update Frequency**: Rare (city parameters stable)
**Size**: ~2 KB

### 7.6 Q-Table Storage

**File**: `rl/q_table.pkl` (or `q_table_covid19.pkl`)

**Structure** (Pickled):
```python
{
    'q_table': np.ndarray,        # Shape: (324, 5)
    'state_mapping': dict,        # State tuple → index
    'metadata': {
        'episodes': 200,
        'final_epsilon': 0.01,
        'avg_reward': -1234.5,
        'virus_name': 'COVID-19',
        'training_date': '2026-01-15'
    }
}
```

**Access Pattern**: Load once at startup (if AI mode enabled)
**Update Frequency**: After each training session
**Size**: ~50 KB

### 7.7 Session State Management

**Storage**: Streamlit `st.session_state` (in-memory)

**Key Variables**:
```python
session_state = {
    'running': bool,                    # Simulation in progress
    'simulation_complete': bool,        # Simulation finished
    'simulation_results': dict,         # Full results data
    'last_params': dict,                # Previous configuration
    'language': str,                    # Current language code
    'chatbot': AdvancedChatbot,        # Chatbot instance
    'chatbot_context': str,            # Current context
    'symptom_predictor': SymptomPredictor,  # Predictor instance
    'show_symptom_prediction': bool    # Feature toggle
}
```

**Persistence**: Session-scoped (cleared on browser refresh)
**Size**: Variable (typically 1-5 MB with simulation results)

### 7.8 Data Flow Diagram

```
┌─────────────┐
│   User      │
│   Input     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Streamlit Session State         │
│  (In-Memory Configuration Storage)  │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│   Configuration Databases           │
│  ┌──────────┐  ┌──────────┐        │
│  │  Virus   │  │   WHO    │        │
│  │ Configs  │  │  Params  │        │
│  └──────────┘  └──────────┘        │
│  ┌──────────┐  ┌──────────┐        │
│  │  City    │  │Historical│        │
│  │ Configs  │  │ Pandemic │        │
│  └──────────┘  └──────────┘        │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│      Simulation Engine              │
│   (Runtime Data Processing)         │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│   Results Storage                   │
│  (Session State + Visualizations)   │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│   Display   │
│   to User   │
└─────────────┘
```


---

## 8. API Design

### 8.1 Internal Module APIs

#### 8.1.1 SEIR Engine API

```python
# Module: env/seir.py

def set_virus_params(config: dict) -> None:
    """
    Set global virus parameters for simulation.
    
    Args:
        config: Dictionary containing virus parameters
            - R0: float
            - incubation_days: int
            - infectious_days: int
            - base_beta: float
            - mortality_rate: float
    
    Returns:
        None (modifies global state)
    """

def seed_infection(population: np.ndarray, 
                   initial_infected: int = 10) -> None:
    """
    Initialize infection in random agents.
    
    Args:
        population: NumPy structured array of agents
        initial_infected: Number of agents to infect initially
    
    Returns:
        None (modifies population in-place)
    """

def update_seir(population: np.ndarray,
                mutation_tracker: Optional[dict] = None,
                current_day: int = 0) -> None:
    """
    Execute one day of SEIR state transitions.
    
    Args:
        population: NumPy structured array of agents
        mutation_tracker: Optional mutation tracking dictionary
        current_day: Current simulation day
    
    Returns:
        None (modifies population in-place)
    
    Side Effects:
        - Updates agent states (S→E→I→R)
        - Increments days_in_state
        - May trigger mutations if tracker provided
    """
```

#### 8.1.2 Population API

```python
# Module: env/population.py

def generate_population(size: int, 
                       virus_config: dict) -> np.ndarray:
    """
    Generate agent-based population with demographics.
    
    Args:
        size: Total number of agents
        virus_config: Virus configuration dictionary
    
    Returns:
        NumPy structured array with fields:
            - x, y: float (spatial coordinates)
            - age_group: str ('child', 'adult', 'elderly')
            - state: str ('S', 'E', 'I', 'R')
            - immunity: float (0.0-1.0)
            - contact_rate: float
            - days_in_state: int
            - severity: float
            - vaccinated: bool
    
    Raises:
        ValueError: If size < 100 or size > 50000
    """
```

#### 8.1.3 Policy API

```python
# Module: env/policies.py

def apply_policy(population: np.ndarray,
                policy: dict,
                virus_config: dict) -> None:
    """
    Apply intervention policy to population.
    
    Args:
        population: Agent array
        policy: Dictionary with keys:
            - mask_mandate: bool
            - school_closure: bool
            - vaccination: bool
        virus_config: Virus configuration
    
    Returns:
        None (modifies population in-place)
    
    Effects:
        - Mask mandate: Reduces contact_rate by 40%
        - School closure: Reduces child contact_rate by 70%
        - Vaccination: Increases immunity, sets vaccinated=True
    """

def calculate_policy_cost(policy: dict, 
                         population_size: int) -> float:
    """
    Calculate economic cost of policy.
    
    Args:
        policy: Policy dictionary
        population_size: Total population
    
    Returns:
        Total cost as float
    
    Cost Formula:
        - Mask: 0.05 * population_size
        - School closure: 0.10 * population_size
        - Vaccination: 0.15 * population_size
    """
```

#### 8.1.4 Metrics API

```python
# Module: simulation/metrics.py

def init_metrics() -> dict:
    """
    Initialize metrics tracking dictionary.
    
    Returns:
        Dictionary with empty lists for:
            - day, susceptible, exposed, infected, recovered
            - deaths, new_infections, Rt, attack_rate, hospital_load
    """

def record_metrics(metrics: dict,
                  population: np.ndarray,
                  mortality_rate: float,
                  generation_time: float) -> None:
    """
    Record current simulation state metrics.
    
    Args:
        metrics: Metrics dictionary from init_metrics()
        population: Current population state
        mortality_rate: Virus mortality rate
        generation_time: Average generation time
    
    Returns:
        None (modifies metrics in-place)
    
    Calculations:
        - Rt: Effective reproduction number
        - Attack rate: Cumulative infection percentage
        - Hospital load: Estimated from infected count
    """

def calculate_Rt(infected_history: List[int],
                generation_time: float) -> float:
    """
    Calculate effective reproduction number.
    
    Args:
        infected_history: List of infected counts over time
        generation_time: Average time between infections
    
    Returns:
        Rt value as float
    
    Formula:
        Rt = (I_t / I_{t-g}) where g = generation_time
    """
```

#### 8.1.5 Visualization API

```python
# Module: visualization/plotly_plots.py

def plot_seir_plotly(metrics: dict, 
                    title: str = "SEIR Epidemic Curve") -> go.Figure:
    """
    Generate interactive SEIR time series plot.
    
    Args:
        metrics: Metrics dictionary with time series data
        title: Chart title
    
    Returns:
        Plotly Figure object
    
    Features:
        - 4 lines (S, E, I, R)
        - Interactive hover tooltips
        - Zoom and pan enabled
        - Legend with toggle
    """

def plot_infection_heatmap(population: np.ndarray,
                          grid_size: int = 20) -> go.Figure:
    """
    Generate infection density heatmap.
    
    Args:
        population: Agent array with spatial coordinates
        grid_size: Grid resolution (20 = 20×20 grid)
    
    Returns:
        Plotly Figure object
    
    Algorithm:
        1. Partition space into grid_size × grid_size cells
        2. Count infected agents per cell
        3. Generate heatmap with color scale
    """

def plot_mutation_timeline(mutation_events: List[dict]) -> go.Figure:
    """
    Generate mutation timeline visualization.
    
    Args:
        mutation_events: List of mutation event dictionaries
    
    Returns:
        Plotly Figure object
    
    Display:
        - Vertical timeline
        - Markers for each mutation
        - Annotations with parameter changes
    """

def plot_policy_comparison(comparison_results: dict) -> go.Figure:
    """
    Generate policy comparison bar chart.
    
    Args:
        comparison_results: Dictionary mapping policy names to metrics
    
    Returns:
        Plotly Figure object
    
    Metrics Displayed:
        - Total deaths
        - Peak infected
        - Economic cost
        - Final recovered
    """
```

#### 8.1.6 RL Agent API

```python
# Module: rl/agent.py

class QLearningAgent:
    """Q-Learning agent for epidemic control."""
    
    def __init__(self, 
                 state_space_size: int = 324,
                 action_space_size: int = 5,
                 learning_rate: float = 0.1,
                 discount_factor: float = 0.95,
                 epsilon: float = 1.0):
        """
        Initialize Q-Learning agent.
        
        Args:
            state_space_size: Number of discrete states
            action_space_size: Number of actions
            learning_rate: Alpha parameter
            discount_factor: Gamma parameter
            epsilon: Exploration rate
        """
    
    def select_action(self, state: int) -> int:
        """
        Select action using epsilon-greedy policy.
        
        Args:
            state: Current state index
        
        Returns:
            Action index (0-4)
        """
    
    def update(self, 
               state: int,
               action: int,
               reward: float,
               next_state: int) -> None:
        """
        Update Q-table using Q-learning rule.
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Resulting state
        
        Returns:
            None (updates internal Q-table)
        """
    
    def save(self, filepath: str) -> None:
        """Save Q-table to pickle file."""
    
    def load(self, filepath: str) -> None:
        """Load Q-table from pickle file."""
```

#### 8.1.7 Symptom Predictor API

```python
# Module: symptom_prediction/predictor.py

class SymptomPredictor:
    """ML-based symptom profile predictor."""
    
    def __init__(self):
        """Initialize predictor with historical pandemic data."""
    
    def predict(self, virus_params: dict) -> dict:
        """
        Predict symptom profile for virus.
        
        Args:
            virus_params: Dictionary with:
                - R0: float
                - mortality_rate: float (CFR)
                - incubation_days: int
                - infectious_days: int
        
        Returns:
            Dictionary with:
                - primary_symptoms: List[dict]
                - secondary_symptoms: List[dict]
                - severe_complications: List[dict]
                - age_specific_impact: dict
                - confidence_score: float (0-1)
                - similar_pandemics: List[dict]
        
        Algorithm:
            1. Extract feature vector from virus_params
            2. Calculate similarity to historical pandemics
            3. Weighted average of top 3 matches
            4. Generate confidence score
        """
    
    def calculate_similarity(self,
                           features1: np.ndarray,
                           features2: np.ndarray) -> float:
        """
        Calculate weighted Euclidean similarity.
        
        Args:
            features1: Feature vector 1
            features2: Feature vector 2
        
        Returns:
            Similarity score (0-1, higher = more similar)
        """
```

### 8.2 External API Considerations

**Current Status**: No external APIs (standalone application)

**Future API Endpoints** (if REST API added):

```
GET  /api/v1/diseases          - List available diseases
GET  /api/v1/diseases/{id}     - Get disease parameters
POST /api/v1/simulate          - Run simulation
GET  /api/v1/simulate/{id}     - Get simulation results
POST /api/v1/predict-symptoms  - Predict symptom profile
GET  /api/v1/cities            - List city configurations
```


---

## 9. Security Design

### 9.1 Security Principles

1. **No Personal Data Storage**: System does not collect or store personal health information
2. **Input Validation**: All user inputs validated and sanitized
3. **Safe Execution**: No code execution from user input
4. **Data Privacy**: Simulation data remains session-scoped

### 9.2 Input Validation

**Numeric Parameters**:
```python
def validate_population_size(size: int) -> int:
    """
    Validate population size input.
    
    Rules:
        - Must be integer
        - Range: 500 to 50,000
        - Default: 5,000 if invalid
    """
    if not isinstance(size, int):
        return 5000
    return max(500, min(50000, size))

def validate_days(days: int) -> int:
    """
    Validate simulation days.
    
    Rules:
        - Must be integer
        - Range: 20 to 120
        - Default: 45 if invalid
    """
    if not isinstance(days, int):
        return 45
    return max(20, min(120, days))
```

**String Parameters**:
```python
def validate_virus_name(name: str, 
                       valid_names: List[str]) -> str:
    """
    Validate virus name selection.
    
    Rules:
        - Must be in predefined list
        - Default to 'COVID-19' if invalid
    """
    if name not in valid_names:
        return 'COVID-19'
    return name
```

**Boolean Parameters**:
```python
def validate_policy(policy: dict) -> dict:
    """
    Validate policy configuration.
    
    Rules:
        - All values must be boolean
        - Unknown keys ignored
        - Missing keys default to False
    """
    valid_keys = ['mask_mandate', 'school_closure', 'vaccination']
    validated = {}
    for key in valid_keys:
        validated[key] = bool(policy.get(key, False))
    return validated
```

### 9.3 Data Sanitization

**File Path Sanitization**:
```python
def sanitize_filepath(filepath: str) -> str:
    """
    Sanitize file paths to prevent directory traversal.
    
    Rules:
        - Remove '..' sequences
        - Remove absolute path indicators
        - Restrict to project directory
    """
    # Remove dangerous patterns
    filepath = filepath.replace('..', '')
    filepath = filepath.replace('~', '')
    
    # Ensure relative path
    if os.path.isabs(filepath):
        filepath = os.path.basename(filepath)
    
    return filepath
```

**JSON Data Validation**:
```python
def validate_json_config(data: dict, schema: dict) -> dict:
    """
    Validate JSON configuration against schema.
    
    Args:
        data: Input JSON data
        schema: Expected schema definition
    
    Returns:
        Validated and sanitized data
    
    Raises:
        ValueError: If data doesn't match schema
    """
    validated = {}
    for key, expected_type in schema.items():
        if key not in data:
            raise ValueError(f"Missing required key: {key}")
        if not isinstance(data[key], expected_type):
            raise ValueError(f"Invalid type for {key}")
        validated[key] = data[key]
    return validated
```

### 9.4 Session Security

**Session State Isolation**:
- Each user session has isolated `st.session_state`
- No cross-session data leakage
- Session data cleared on browser close

**Memory Management**:
```python
def clear_simulation_data():
    """
    Clear large simulation data from session state.
    
    Called when:
        - User changes parameters
        - Session timeout
        - Explicit user action
    """
    if 'simulation_results' in st.session_state:
        del st.session_state.simulation_results
    if 'population' in st.session_state:
        del st.session_state.population
```

### 9.5 Dependency Security

**Requirements Pinning**:
```txt
# requirements.txt with version pinning
streamlit==1.28.0
numpy==1.24.0
pandas==2.0.0
matplotlib==3.7.0
plotly==5.14.0
gymnasium==1.0.0
torch==2.0.0
```

**Security Scanning**:
```bash
# Regular dependency vulnerability scanning
pip install safety
safety check --file requirements.txt
```

### 9.6 Deployment Security

**Streamlit Cloud Security**:
- HTTPS enforced for all connections
- Secrets management via Streamlit secrets
- No sensitive data in repository
- Environment variables for configuration

**Access Control**:
- Public access (educational tool)
- No authentication required
- Rate limiting by Streamlit Cloud
- DDoS protection by hosting platform

### 9.7 Error Handling

**Safe Error Messages**:
```python
try:
    result = run_simulation(params)
except Exception as e:
    # Log full error internally
    logger.error(f"Simulation error: {str(e)}", exc_info=True)
    
    # Show safe message to user
    st.error("Simulation encountered an error. Please check your parameters.")
    
    # Don't expose internal details
    # BAD: st.error(f"Error: {str(e)}")
```

**Graceful Degradation**:
```python
# Feature availability checks
if FEATURES_AVAILABLE['rl']:
    # Show RL mode
else:
    st.info("RL features unavailable. Using manual mode.")

if FEATURES_AVAILABLE['symptom_prediction']:
    # Show symptom predictor
else:
    st.info("Symptom prediction unavailable.")
```

### 9.8 Code Injection Prevention

**No Dynamic Code Execution**:
```python
# NEVER do this:
# eval(user_input)
# exec(user_input)
# __import__(user_input)

# SAFE: Use predefined mappings
VIRUS_MAPPING = {
    'covid': VIRUS_CONFIGS['COVID-19'],
    'sars': VIRUS_CONFIGS['SARS']
}
selected_virus = VIRUS_MAPPING.get(user_input, VIRUS_CONFIGS['COVID-19'])
```

**SQL Injection Prevention**:
- Not applicable (no SQL database)
- All data in Python structures or JSON files

**XSS Prevention**:
- Streamlit handles HTML escaping automatically
- No raw HTML rendering from user input
- Markdown rendering sanitized by Streamlit


---

## 10. Performance Design

### 10.1 Performance Requirements

| Metric | Target | Maximum |
|--------|--------|---------|
| Simulation time (5K agents, 45 days) | 30s | 60s |
| Visualization rendering | 2s | 5s |
| Page load time | 3s | 8s |
| Memory usage (5K agents) | 200MB | 500MB |
| Memory usage (50K agents) | 1GB | 2GB |

### 10.2 Optimization Strategies

#### 10.2.1 NumPy Vectorization

**Before (Slow - Python loops)**:
```python
# O(n) with Python overhead
for i in range(len(population)):
    if population[i]['state'] == 'I':
        infected_count += 1
```

**After (Fast - NumPy vectorization)**:
```python
# O(n) with C-level optimization
infected_count = np.sum(population['state'] == 'I')
```

**Performance Gain**: 10-50x faster

#### 10.2.2 Spatial Indexing

**Naive Contact Detection**: O(n²)
```python
# Check all pairs - SLOW
for agent1 in population:
    for agent2 in population:
        if distance(agent1, agent2) < radius:
            contacts.append((agent1, agent2))
```

**Optimized with Grid Partitioning**: O(n)
```python
# Grid-based spatial indexing - FAST
grid = create_spatial_grid(population, cell_size=10)
for cell in grid:
    for agent in cell:
        for neighbor_cell in adjacent_cells(cell):
            for other in neighbor_cell:
                if distance(agent, other) < radius:
                    contacts.append((agent, other))
```

**Performance Gain**: 100-1000x faster for large populations

#### 10.2.3 Batch Policy Application

**Before (Multiple passes)**:
```python
if policy['mask_mandate']:
    apply_masks(population)
if policy['school_closure']:
    apply_school_closure(population)
if policy['vaccination']:
    apply_vaccination(population)
```

**After (Single pass)**:
```python
def apply_policy_batch(population, policy, virus_config):
    """Apply all policies in single pass over population."""
    mask_factor = 0.6 if policy['mask_mandate'] else 1.0
    
    for i in range(len(population)):
        # Apply mask effect
        population[i]['contact_rate'] *= mask_factor
        
        # Apply school closure (children only)
        if policy['school_closure'] and population[i]['age_group'] == 'child':
            population[i]['contact_rate'] *= 0.3
        
        # Apply vaccination
        if policy['vaccination'] and not population[i]['vaccinated']:
            population[i]['immunity'] += 0.7
            population[i]['vaccinated'] = True
```

**Performance Gain**: 3x faster

#### 10.2.4 Caching and Memoization

**Streamlit Caching**:
```python
@st.cache_data
def load_who_database():
    """Cache WHO database loading."""
    with open('data/who_params.json') as f:
        return json.load(f)

@st.cache_data
def load_historical_pandemics():
    """Cache historical pandemic data."""
    return HISTORICAL_PANDEMICS

@st.cache_resource
def load_rl_agent():
    """Cache RL agent loading (singleton)."""
    return load_trained_agent('rl/q_table.pkl')
```

**Performance Gain**: Eliminates redundant I/O operations

#### 10.2.5 Lazy Loading

**Visualization Lazy Rendering**:
```python
# Only render visualizations when tab is active
with st.tabs(['SEIR Curve', 'Heatmap', 'Scatter']):
    with tab1:
        if st.session_state.get('show_seir', True):
            fig = plot_seir_plotly(metrics)
            st.plotly_chart(fig)
    
    with tab2:
        if st.session_state.get('show_heatmap', False):
            fig = plot_infection_heatmap(population)
            st.plotly_chart(fig)
```

### 10.3 Memory Optimization

#### 10.3.1 Data Type Selection

**Optimized NumPy dtypes**:
```python
# Use smallest sufficient data types
population = np.array([...], dtype=[
    ('x', 'f4'),           # float32 instead of float64 (4 bytes vs 8)
    ('y', 'f4'),
    ('age_group', 'U10'),  # Unicode string, max 10 chars
    ('state', 'U1'),       # Single character
    ('immunity', 'f4'),
    ('contact_rate', 'f4'),
    ('days_in_state', 'i4'),  # int32 instead of int64
    ('severity', 'f4'),
    ('vaccinated', 'bool')    # 1 byte
])
```

**Memory Savings**: 40% reduction vs default types

#### 10.3.2 Result Data Compression

**Store only essential metrics**:
```python
# Don't store full population history
# BAD: population_history = [population.copy() for day in range(DAYS)]

# GOOD: Store only aggregated metrics
metrics = {
    'day': [],
    'susceptible': [],
    'exposed': [],
    'infected': [],
    'recovered': []
}
```

**Memory Savings**: 99% reduction (MB vs GB)

### 10.4 Computational Complexity Analysis

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Population generation | O(n) | Linear in population size |
| SEIR update (naive) | O(n²) | All-pairs contact check |
| SEIR update (optimized) | O(n) | Grid-based spatial indexing |
| Policy application | O(n) | Single pass over population |
| Metrics calculation | O(n) | Count states |
| Mutation check | O(1) | Simple threshold check |
| Visualization rendering | O(n) | Plot all data points |
| Q-Learning action selection | O(1) | Table lookup |
| Symptom prediction | O(k×m) | k pandemics, m symptoms |

### 10.5 Profiling and Monitoring

**Performance Profiling**:
```python
import cProfile
import pstats

def profile_simulation():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run simulation
    run_simulation(params)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
```

**Key Metrics to Monitor**:
- Simulation time per day
- Memory usage growth
- Visualization rendering time
- Cache hit rates
- NumPy operation efficiency

### 10.6 Scalability Considerations

**Horizontal Scaling** (Future):
- Multi-processing for policy comparison mode
- Parallel simulation runs
- Distributed training for RL agent

**Vertical Scaling**:
- Current: Single-threaded, single-machine
- Supports up to 50K agents on 8GB RAM
- GPU acceleration potential for RL training

**Code Example - Parallel Policy Comparison**:
```python
from multiprocessing import Pool

def run_single_policy(policy_config):
    """Run simulation for one policy."""
    population = generate_population(POP_SIZE, virus_config)
    # ... simulation logic
    return results

# Parallel execution
with Pool(processes=5) as pool:
    results = pool.map(run_single_policy, policies_to_test)
```

**Performance Gain**: 5x faster for policy comparison (5 policies)


---

## 11. Deployment Architecture

### 11.1 Deployment Options

#### Option 1: Streamlit Cloud (Primary)
- **Platform**: Streamlit Community Cloud
- **URL**: https://epicontrolai.streamlit.app
- **Cost**: Free tier
- **Resources**: 1 CPU, 800MB RAM
- **Limitations**: Public access only, resource constraints

#### Option 2: Heroku (Alternative)
- **Platform**: Heroku
- **Dyno Type**: Standard-1X
- **Cost**: ~$7/month
- **Resources**: 512MB RAM
- **Configuration**: Procfile, runtime.txt

#### Option 3: Local Deployment
- **Platform**: Any machine with Python 3.10+
- **Command**: `streamlit run app.py`
- **Port**: 8501 (default)
- **Resources**: Depends on machine

### 11.2 Streamlit Cloud Deployment

**Repository Structure**:
```
epicontrol_ai/
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── app.py                   # Main entry point
├── requirements.txt         # Python dependencies
├── packages.txt            # System dependencies (if needed)
└── [all other modules]
```

**config.toml**:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

**Deployment Steps**:
1. Push code to GitHub repository
2. Connect repository to Streamlit Cloud
3. Configure main file path: `app.py`
4. Deploy (automatic on push)

**Environment Variables** (if needed):
```
# .streamlit/secrets.toml (not in git)
[general]
debug_mode = false
```

### 11.3 Heroku Deployment

**Procfile**:
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh**:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

**runtime.txt**:
```
python-3.10.12
```

**Deployment Steps**:
```bash
# Install Heroku CLI
heroku login

# Create app
heroku create epicontrol-ai

# Deploy
git push heroku main

# Open app
heroku open
```

### 11.4 Docker Deployment (Future)

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  epicontrol-ai:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
    volumes:
      - ./data:/app/data
      - ./rl:/app/rl
    restart: unless-stopped
```

**Deployment**:
```bash
docker-compose up -d
```

### 11.5 CI/CD Pipeline

**GitHub Actions Workflow** (.github/workflows/deploy.yml):
```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
  
  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### 11.6 Monitoring and Logging

**Application Logging**:
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('epicontrol.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info("Simulation started")
logger.error("Simulation failed", exc_info=True)
```

**Performance Monitoring**:
```python
import time

def monitor_performance(func):
    """Decorator to monitor function performance."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"{func.__name__} took {end_time - start_time:.2f}s")
        return result
    return wrapper

@monitor_performance
def run_simulation(params):
    # Simulation logic
    pass
```

**User Analytics** (Privacy-respecting):
```python
# Track feature usage (no personal data)
def track_feature_usage(feature_name):
    """Log feature usage for analytics."""
    logger.info(f"Feature used: {feature_name}")
    
    # Could send to analytics service
    # analytics.track('feature_usage', {'feature': feature_name})
```

### 11.7 Backup and Recovery

**Data Backup Strategy**:
- Configuration files: Version controlled in Git
- Q-tables: Stored in repository (small size)
- No user data to backup (stateless application)

**Disaster Recovery**:
1. Code: Restore from GitHub
2. Dependencies: Reinstall from requirements.txt
3. Configuration: Restore from .streamlit/config.toml
4. Trained models: Retrain if necessary (2-3 hours)

**Recovery Time Objective (RTO)**: < 1 hour
**Recovery Point Objective (RPO)**: 0 (no data loss, stateless)

### 11.8 Scaling Strategy

**Current Capacity**:
- Concurrent users: ~10-20 (Streamlit Cloud free tier)
- Simulations per hour: ~100-200
- Response time: < 5s for typical simulation

**Scaling Triggers**:
- CPU usage > 80% sustained
- Memory usage > 700MB
- Response time > 10s
- Error rate > 5%

**Scaling Actions**:
1. **Vertical Scaling**: Upgrade to paid Streamlit tier
2. **Horizontal Scaling**: Deploy multiple instances with load balancer
3. **Optimization**: Implement caching, reduce computation
4. **CDN**: Use CDN for static assets

**Load Balancing** (Future):
```
                    ┌─────────────┐
                    │Load Balancer│
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐    ┌─────▼─────┐    ┌─────▼─────┐
    │ Instance 1│    │ Instance 2│    │ Instance 3│
    └───────────┘    └───────────┘    └───────────┘
```


---

## 12. Testing Strategy

### 12.1 Testing Pyramid

```
                    ┌─────────────┐
                    │   Manual    │  5%
                    │   Testing   │
                ┌───┴─────────────┴───┐
                │   Integration Tests │  15%
                │   (Module-to-Module)│
            ┌───┴─────────────────────┴───┐
            │      Unit Tests              │  80%
            │   (Individual Functions)     │
            └─────────────────────────────┘
```

### 12.2 Unit Testing

**Test Framework**: pytest

**Test Structure**:
```
tests/
├── __init__.py
├── test_seir.py
├── test_population.py
├── test_policies.py
├── test_mutation.py
├── test_metrics.py
├── test_rl_agent.py
├── test_symptom_predictor.py
└── test_visualizations.py
```

**Example Unit Tests**:

```python
# tests/test_seir.py
import pytest
import numpy as np
from env.seir import set_virus_params, seed_infection, update_seir
from env.population import generate_population

def test_set_virus_params():
    """Test virus parameter setting."""
    config = {
        'R0': 2.5,
        'incubation_days': 5,
        'infectious_days': 7,
        'base_beta': 0.045,
        'mortality_rate': 0.023
    }
    set_virus_params(config)
    # Verify global state updated
    assert True  # Add actual assertions

def test_seed_infection():
    """Test initial infection seeding."""
    population = generate_population(1000, {'R0': 2.5})
    seed_infection(population, initial_infected=10)
    
    infected_count = np.sum(population['state'] == 'I')
    assert infected_count == 10

def test_seir_transitions():
    """Test SEIR state transitions."""
    population = generate_population(100, {'R0': 2.5})
    seed_infection(population, initial_infected=5)
    
    initial_infected = np.sum(population['state'] == 'I')
    
    # Run one day
    update_seir(population)
    
    # Check that some transitions occurred
    final_infected = np.sum(population['state'] == 'I')
    assert final_infected >= 0  # May increase or decrease

def test_mortality():
    """Test mortality application."""
    population = generate_population(1000, {
        'R0': 2.5,
        'mortality_rate': 1.0  # 100% mortality for testing
    })
    
    # Set all to infected with max days
    population['state'] = 'I'
    population['days_in_state'] = 10
    
    update_seir(population)
    
    # All should be dead or recovered
    assert np.sum(population['state'] == 'I') == 0
```

```python
# tests/test_policies.py
import pytest
import numpy as np
from env.population import generate_population
from env.policies import apply_policy, calculate_policy_cost

def test_mask_mandate():
    """Test mask mandate reduces contact rate."""
    population = generate_population(100, {'R0': 2.5})
    original_contact = population['contact_rate'].copy()
    
    policy = {'mask_mandate': True, 'school_closure': False, 'vaccination': False}
    apply_policy(population, policy, {'R0': 2.5})
    
    # Contact rate should be reduced
    assert np.all(population['contact_rate'] < original_contact)

def test_vaccination():
    """Test vaccination increases immunity."""
    population = generate_population(100, {'R0': 2.5})
    original_immunity = population['immunity'].copy()
    
    policy = {'mask_mandate': False, 'school_closure': False, 'vaccination': True}
    apply_policy(population, policy, {'R0': 2.5})
    
    # Immunity should increase
    assert np.mean(population['immunity']) > np.mean(original_immunity)

def test_policy_cost():
    """Test policy cost calculation."""
    policy = {'mask_mandate': True, 'school_closure': True, 'vaccination': True}
    cost = calculate_policy_cost(policy, 1000)
    
    expected_cost = (0.05 + 0.10 + 0.15) * 1000
    assert cost == expected_cost
```

```python
# tests/test_rl_agent.py
import pytest
from rl.agent import QLearningAgent

def test_agent_initialization():
    """Test Q-Learning agent initialization."""
    agent = QLearningAgent(state_space_size=324, action_space_size=5)
    
    assert agent.q_table.shape == (324, 5)
    assert agent.epsilon == 1.0

def test_action_selection():
    """Test epsilon-greedy action selection."""
    agent = QLearningAgent()
    agent.epsilon = 0.0  # No exploration
    
    # Set Q-values to prefer action 2
    agent.q_table[0, 2] = 10.0
    
    action = agent.select_action(0)
    assert action == 2

def test_q_update():
    """Test Q-learning update rule."""
    agent = QLearningAgent(learning_rate=0.1, discount_factor=0.9)
    
    initial_q = agent.q_table[0, 1]
    agent.update(state=0, action=1, reward=10.0, next_state=1)
    
    # Q-value should have changed
    assert agent.q_table[0, 1] != initial_q
```

### 12.3 Integration Testing

**Test Module Interactions**:

```python
# tests/test_integration.py
import pytest
from env.population import generate_population
from env.seir import set_virus_params, seed_infection, update_seir
from env.policies import apply_policy
from simulation.metrics import init_metrics, record_metrics

def test_full_simulation_flow():
    """Test complete simulation workflow."""
    # Setup
    virus_config = {
        'R0': 2.5,
        'incubation_days': 5,
        'infectious_days': 7,
        'base_beta': 0.045,
        'mortality_rate': 0.023
    }
    
    set_virus_params(virus_config)
    population = generate_population(1000, virus_config)
    seed_infection(population, initial_infected=10)
    metrics = init_metrics()
    
    # Run simulation for 10 days
    for day in range(10):
        update_seir(population)
        record_metrics(metrics, population, 0.023, 6.0)
    
    # Verify results
    assert len(metrics['day']) == 10
    assert metrics['infected'][-1] >= 0
    assert sum(metrics['susceptible'][-1:]) + sum(metrics['infected'][-1:]) + \
           sum(metrics['recovered'][-1:]) <= 1000

def test_policy_impact():
    """Test that policies reduce infections."""
    virus_config = {'R0': 2.5, 'incubation_days': 5, 'infectious_days': 7,
                   'base_beta': 0.045, 'mortality_rate': 0.023}
    
    # Simulation without policy
    set_virus_params(virus_config)
    pop_no_policy = generate_population(1000, virus_config)
    seed_infection(pop_no_policy, 10)
    
    for _ in range(20):
        update_seir(pop_no_policy)
    
    infections_no_policy = np.sum(pop_no_policy['state'] == 'I')
    
    # Simulation with policy
    set_virus_params(virus_config)
    pop_with_policy = generate_population(1000, virus_config)
    seed_infection(pop_with_policy, 10)
    
    policy = {'mask_mandate': True, 'school_closure': True, 'vaccination': True}
    apply_policy(pop_with_policy, policy, virus_config)
    
    for _ in range(20):
        update_seir(pop_with_policy)
    
    infections_with_policy = np.sum(pop_with_policy['state'] == 'I')
    
    # Policy should reduce infections
    assert infections_with_policy < infections_no_policy
```

### 12.4 Performance Testing

```python
# tests/test_performance.py
import pytest
import time
from env.population import generate_population
from env.seir import update_seir

@pytest.mark.performance
def test_simulation_speed():
    """Test simulation completes within time limit."""
    population = generate_population(5000, {'R0': 2.5})
    
    start_time = time.time()
    
    for _ in range(45):
        update_seir(population)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Should complete in under 60 seconds
    assert duration < 60.0

@pytest.mark.performance
def test_memory_usage():
    """Test memory usage stays within limits."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    population = generate_population(50000, {'R0': 2.5})
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    # Should use less than 500MB for 50K agents
    assert memory_increase < 500
```

### 12.5 End-to-End Testing

**Manual Test Cases**:

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC-001: Basic Simulation | 1. Set population=1000, days=30<br>2. Select COVID-19<br>3. Run simulation | SEIR curves display, metrics show results |
| TC-002: Policy Application | 1. Enable all policies<br>2. Run simulation | Lower infection rates than no policy |
| TC-003: Mutation Trigger | 1. Set mutation threshold=0.2<br>2. Run 60 days<br>3. Check timeline | Mutation events appear on timeline |
| TC-004: AI Mode | 1. Select AI (RL) mode<br>2. Run simulation | Agent makes policy decisions automatically |
| TC-005: Policy Comparison | 1. Select Policy Comparison<br>2. Run simulation | 5 strategies compared with bar chart |
| TC-006: Symptom Prediction | 1. Enable symptom predictor<br>2. Run simulation | Symptom profile displayed with confidence |
| TC-007: Language Switch | 1. Change language to Hindi<br>2. Navigate UI | All text translated correctly |
| TC-008: City Preset | 1. Select Mumbai preset<br>2. Run simulation | Parameters auto-filled, realistic results |

### 12.6 Test Coverage Goals

**Coverage Targets**:
- Overall: > 70%
- Core modules (seir, population, policies): > 85%
- RL agent: > 75%
- Visualizations: > 60%
- UI (app.py): > 40% (harder to test)

**Running Tests**:
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_seir.py -v

# Run performance tests
pytest tests/ -m performance
```

### 12.7 Continuous Testing

**Pre-commit Hooks**:
```bash
# .git/hooks/pre-commit
#!/bin/bash
pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=70
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

**Automated Testing in CI**:
- Run on every push to main branch
- Run on every pull request
- Generate coverage reports
- Fail build if coverage < 70%


---

## 13. Design Patterns Used

### 13.1 Creational Patterns

#### Factory Pattern
**Usage**: Population generation with configurable parameters

```python
def generate_population(size: int, virus_config: dict) -> np.ndarray:
    """
    Factory method for creating population with different configurations.
    Encapsulates complex initialization logic.
    """
    # Create agents with age-stratified attributes
    # Returns configured population array
```

**Benefits**:
- Centralized population creation logic
- Easy to modify population characteristics
- Supports different virus configurations

#### Singleton Pattern
**Usage**: Global virus parameters, RL agent instance

```python
# Global virus parameters (singleton-like)
_VIRUS_PARAMS = {}

def set_virus_params(config: dict):
    """Set global virus parameters (singleton pattern)."""
    global _VIRUS_PARAMS
    _VIRUS_PARAMS = config

# Streamlit resource caching (singleton)
@st.cache_resource
def load_rl_agent():
    """Load RL agent once per session (singleton)."""
    return QLearningAgent.load('rl/q_table.pkl')
```

**Benefits**:
- Single source of truth for virus parameters
- Efficient resource usage (one agent instance)
- Consistent state across simulation

### 13.2 Structural Patterns

#### Adapter Pattern
**Usage**: Gymnasium environment adapter for RL

```python
class EpiControlEnv(gym.Env):
    """
    Adapter pattern: Wraps SEIR simulation to conform to Gymnasium API.
    Allows standard RL algorithms to work with custom simulation.
    """
    
    def reset(self):
        """Gymnasium interface method."""
        # Initialize SEIR simulation
        return observation
    
    def step(self, action):
        """Gymnasium interface method."""
        # Run one day of simulation
        return observation, reward, done, info
```

**Benefits**:
- Standard RL interface
- Reusable with different RL algorithms
- Clean separation of concerns

#### Facade Pattern
**Usage**: Simplified simulation interface in app.py

```python
def run_simulation(population_size, days, virus_config, policy):
    """
    Facade pattern: Provides simple interface to complex subsystems.
    Hides complexity of SEIR engine, metrics, policies, mutations.
    """
    # Initialize all subsystems
    set_virus_params(virus_config)
    population = generate_population(population_size, virus_config)
    seed_infection(population)
    metrics = init_metrics()
    
    # Run simulation loop
    for day in range(days):
        update_seir(population)
        apply_policy(population, policy, virus_config)
        record_metrics(metrics, population)
    
    return metrics, population
```

**Benefits**:
- Simple API for complex operations
- Reduces coupling between UI and engine
- Easy to understand and use

### 13.3 Behavioral Patterns

#### Strategy Pattern
**Usage**: Control mode selection (Manual, AI, Comparison)

```python
class ControlStrategy:
    """Base strategy interface."""
    def execute(self, population, virus_config, days):
        raise NotImplementedError

class ManualStrategy(ControlStrategy):
    """User-controlled policy strategy."""
    def execute(self, population, virus_config, days):
        # Apply user-selected policies
        pass

class AIStrategy(ControlStrategy):
    """RL agent-controlled strategy."""
    def execute(self, population, virus_config, days):
        # Let agent decide policies
        pass

class ComparisonStrategy(ControlStrategy):
    """Compare all policies strategy."""
    def execute(self, population, virus_config, days):
        # Run all policy combinations
        pass

# Usage
strategy = get_strategy(control_mode)
results = strategy.execute(population, virus_config, days)
```

**Benefits**:
- Easy to add new control modes
- Runtime strategy switching
- Clean separation of policy logic

#### Observer Pattern
**Usage**: Metrics tracking observes simulation state

```python
class MetricsObserver:
    """
    Observer pattern: Metrics system observes simulation state changes.
    Updates metrics whenever simulation state changes.
    """
    
    def __init__(self):
        self.metrics = init_metrics()
    
    def update(self, population, day):
        """Called when simulation state changes."""
        record_metrics(self.metrics, population, day)
    
    def get_metrics(self):
        return self.metrics

# Usage in simulation loop
observer = MetricsObserver()
for day in range(days):
    update_seir(population)
    observer.update(population, day)  # Notify observer
```

**Benefits**:
- Decoupled metrics from simulation logic
- Easy to add new metrics
- Real-time tracking

#### Template Method Pattern
**Usage**: Simulation loop structure

```python
def simulation_template(population, virus_config, days, policy_strategy):
    """
    Template method: Defines skeleton of simulation algorithm.
    Subclasses can override specific steps.
    """
    # Setup (fixed)
    set_virus_params(virus_config)
    seed_infection(population)
    metrics = init_metrics()
    
    # Main loop (fixed structure)
    for day in range(days):
        # Step 1: Update SEIR (fixed)
        update_seir(population)
        
        # Step 2: Apply policy (variable - strategy pattern)
        policy_strategy.apply(population, day)
        
        # Step 3: Record metrics (fixed)
        record_metrics(metrics, population)
    
    # Cleanup (fixed)
    return metrics, population
```

**Benefits**:
- Consistent simulation structure
- Flexible policy application
- Easy to maintain

### 13.4 Architectural Patterns

#### Model-View-Controller (MVC)
**Implementation**:

```
Model (Data + Logic):
├── env/seir.py          - SEIR model
├── env/population.py    - Population data
├── simulation/metrics.py - Metrics data
└── rl/agent.py          - RL agent

View (Presentation):
├── visualization/plotly_plots.py - Charts
└── app.py (UI components)        - Streamlit widgets

Controller (Orchestration):
└── app.py (main logic)  - User input handling
                         - Simulation execution
                         - View updates
```

**Benefits**:
- Clear separation of concerns
- Independent testing of components
- Easy to modify UI without changing logic

#### Layered Architecture

```
┌─────────────────────────────────────┐
│     Presentation Layer (UI)         │  Streamlit components
├─────────────────────────────────────┤
│     Application Layer (Logic)       │  Simulation orchestration
├─────────────────────────────────────┤
│     Domain Layer (Core)             │  SEIR, policies, RL
├─────────────────────────────────────┤
│     Data Layer (Storage)            │  Configs, databases
└─────────────────────────────────────┘
```

**Benefits**:
- Organized code structure
- Clear dependencies (top-down)
- Easy to test each layer

### 13.5 Anti-Patterns Avoided

#### God Object (Avoided)
**Bad**: Single class doing everything
**Good**: Modular design with focused responsibilities

#### Spaghetti Code (Avoided)
**Bad**: Tangled dependencies, unclear flow
**Good**: Clear module boundaries, documented interfaces

#### Magic Numbers (Avoided)
**Bad**: Hardcoded values throughout code
**Good**: Named constants and configuration files

```python
# BAD
if infection_rate > 0.30:  # What is 0.30?
    trigger_mutation()

# GOOD
MUTATION_THRESHOLD = 0.30  # 30% infection rate
if infection_rate > MUTATION_THRESHOLD:
    trigger_mutation()
```

#### Premature Optimization (Avoided)
**Approach**: 
1. First: Make it work (correct implementation)
2. Second: Make it right (clean code)
3. Third: Make it fast (optimize bottlenecks)

---

## 14. Future Enhancements

### 14.1 Short-term (3-6 months)

1. **Enhanced Visualizations**
   - Animated SEIR curves
   - 3D spatial visualization
   - Network graph of contacts

2. **Additional Policies**
   - Travel restrictions
   - Quarantine zones
   - Testing and tracing

3. **Improved RL Agent**
   - Deep Q-Network (DQN)
   - Multi-agent RL
   - Transfer learning across diseases

4. **Export Functionality**
   - PDF report generation
   - CSV data export
   - Shareable simulation links

### 14.2 Medium-term (6-12 months)

1. **Multi-Region Simulation**
   - Inter-city travel
   - Regional policy differences
   - Border controls

2. **Hospital Capacity Modeling**
   - ICU tracking
   - Ventilator availability
   - Healthcare worker infections

3. **Economic Impact Modeling**
   - GDP impact
   - Unemployment tracking
   - Industry-specific effects

4. **Real-time Data Integration**
   - Live epidemic data feeds
   - Automatic parameter updates
   - Comparison with real outbreaks

### 14.3 Long-term (1-2 years)

1. **Mobile Application**
   - iOS and Android apps
   - Offline simulation capability
   - Push notifications for results

2. **API Service**
   - RESTful API for simulations
   - Webhook support
   - Rate limiting and authentication

3. **Collaborative Features**
   - Multi-user scenarios
   - Shared simulations
   - Discussion forums

4. **Advanced ML Features**
   - Outbreak prediction
   - Parameter estimation from data
   - Automated policy optimization

---

## 15. Conclusion

### 15.1 Design Summary

EpiControl AI employs a modular, layered architecture that separates concerns across presentation, application, domain, and data layers. The system leverages established design patterns (Factory, Strategy, Observer, MVC) to achieve flexibility, maintainability, and extensibility.

Key design strengths:
- **Modularity**: Clear separation of SEIR engine, RL agent, visualization, and UI
- **Performance**: NumPy vectorization, spatial indexing, caching strategies
- **Scalability**: Supports 500-50,000 agents with linear complexity
- **Usability**: Intuitive Streamlit interface with multi-language support
- **Extensibility**: Easy to add new diseases, policies, and features

### 15.2 Technical Achievements

- Agent-based SEIR modeling with realistic demographics
- Real-time virus mutation dynamics
- Q-Learning agent for automated policy optimization
- ML-based symptom prediction for emerging viruses
- Comprehensive visualization suite (7+ chart types)
- Multi-language support (11 languages)
- City-specific configurations for Indian metros

### 15.3 Design Trade-offs

| Decision | Benefit | Trade-off |
|----------|---------|-----------|
| NumPy arrays | Performance | Less flexible than objects |
| Streamlit | Rapid development | Limited customization |
| Tabular Q-Learning | Simple, interpretable | Less powerful than deep RL |
| In-memory state | Fast access | No persistence |
| Single-threaded | Simple debugging | Limited parallelism |

### 15.4 Lessons Learned

1. **Vectorization is critical**: NumPy operations 10-100x faster than Python loops
2. **Spatial indexing essential**: O(n²) → O(n) for contact detection
3. **Caching improves UX**: Streamlit caching eliminates redundant I/O
4. **Modular design pays off**: Easy to add features without breaking existing code
5. **User testing matters**: Iterative UI improvements based on feedback

### 15.5 Acknowledgments

**Team Neural Nexus**:
- System architecture and design
- SEIR model implementation
- RL agent development
- UI/UX design
- Documentation

**Data Sources**:
- World Health Organization (WHO)
- Centers for Disease Control (CDC)
- POLYMOD contact study
- Peer-reviewed epidemiological research

**Technologies**:
- Streamlit (UI framework)
- NumPy, Pandas (data processing)
- Plotly (visualizations)
- Gymnasium (RL environment)
- PyTorch (future deep RL)

---

## Document Control

**Version**: 1.0  
**Date**: January 2026  
**Status**: Final  
**Author**: Team Neural Nexus  
**Reviewers**: PRAKALP 2026 Technical Committee  

**Change History**:
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | Jan 2026 | Initial design document | Team Neural Nexus |

**References**:
1. Requirements Document (requirements.md)
2. SEIR Model Literature
3. Q-Learning Algorithm Papers
4. Streamlit Documentation
5. NumPy Performance Guide

---

*This document provides the comprehensive technical design specification for EpiControl AI platform.*
