# EpiControl AI

An epidemic simulation and control platform that combines SEIR epidemiological modeling with reinforcement learning for policy optimization. Built for the PRAKALP 2026 Hackathon.

**Live Dashboard:** [https://apicontrolai.streamlit.app](https://apicontrolai.streamlit.app/)
**AWS Hosting:** [http://51.21.228.87:8501/](http://51.21.228.87:8501/)
**Repository:** [github.com/yugrajmangate-dev/api_control_ai](https://github.com/yugrajmangate-dev/api_control_ai)

---

## What It Does

EpiControl AI simulates disease outbreaks using an agent-based SEIR (Susceptible-Exposed-Infected-Recovered) model. Users can configure pathogen parameters, apply intervention policies, and watch how an epidemic unfolds across a population — then let a trained Q-Learning agent find the optimal policy automatically.

Core capabilities:
- Simulate outbreaks with WHO-verified pathogen parameters (COVID-19, SARS, Measles, Influenza, Ebola)
- Apply interventions: mask mandates, school closures, vaccination drives
- Compare 5 policy strategies side-by-side with quantified outcomes
- Track virus mutations that dynamically alter transmission and mortality
- Predict symptom profiles for emerging viruses based on historical pandemic data
- Visualize infection spread through SEIR curves, heatmaps, and spatial scatter plots

---

## Quick Start

### Run Locally

```bash
git clone https://github.com/yugrajmangate-dev/api_control_ai.git
cd api_control_ai
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

### AWS Bedrock Chatbot

The in-app chatbot now uses AWS Bedrock Converse. By default it connects to `eu-north-1` and uses this model/inference profile:

`arn:aws:bedrock:eu-north-1:420859418876:inference-profile/eu.anthropic.claude-opus-4-5-20251101-v1:0`

Optional environment variables:

- `BEDROCK_REGION`
- `BEDROCK_MODEL_ID`
- `BEDROCK_MAX_TOKENS`
- `BEDROCK_TEMPERATURE`
- `BEDROCK_TOP_K`

The app expects valid AWS credentials or an EC2 IAM role with Bedrock access.

### Train the RL Agent (Optional)

The AI mode requires a pre-trained Q-table. To train locally:

```bash
python rl/train.py
```

Trains for 200 episodes and saves the Q-table to `rl/q_table_covid19.pkl`.

---

## Usage

1. **Set parameters** — population size, simulation duration, and city preset (10 Indian metros available)
2. **Pick a pathogen** — choose from custom virus models or the WHO database
3. **Enable features** — toggle virus mutations and symptom prediction
4. **Select control mode:**
   - **Manual** — you choose which interventions to apply
   - **AI (Q-Learning)** — the trained agent selects policies each day
   - **Policy Comparison** — runs all 5 strategies and ranks them
5. **Run the simulation** and analyze the results

---

## Project Structure

```
epicontrol_ai/
├── app.py                      # Streamlit dashboard (main entry point)
├── chatbot.py                  # In-app conversational assistant
├── translations.py             # Multi-language support (11 languages)
│
├── config/
│   └── base_params.py          # Age-group parameters (immunity, severity, contact rates)
│
├── data/
│   ├── virus_configs.py        # COVID-19, Influenza, SARS-like configs
│   └── who_params.json         # WHO-sourced disease parameters
│
├── env/
│   ├── seir.py                 # SEIR state transition engine
│   ├── population.py           # Agent population generator
│   ├── mutation.py             # Virus mutation system
│   ├── policies.py             # Intervention policy definitions
│   └── city.py                 # Indian city presets (Mumbai, Delhi, etc.)
│
├── rl/
│   ├── agent.py                # Q-Learning agent
│   ├── env.py                  # Gymnasium RL environment
│   ├── train.py                # Training loop
│   ├── load_agent.py           # Load pre-trained Q-table
│   └── utils.py                # State discretization
│
├── simulation/
│   └── metrics.py              # Rt, attack rate, incidence tracking
│
├── symptom_prediction/
│   ├── predictor.py            # Similarity-based symptom prediction
│   └── historical_data.py      # 6 historical pandemic datasets
│
├── visualization/
│   └── plotly_plots.py         # SEIR curves, heatmaps, scatter, mutation timeline
│
├── requirements.txt
├── Procfile                    # Streamlit Cloud deployment
├── runtime.txt                 # Python 3.10.12
└── .streamlit/
    └── config.toml             # Dark theme config
```

---

## Key Technical Details

### SEIR Model

Each individual in the population is an agent with attributes: age group, immunity, contact rate, spatial coordinates, and disease state. State transitions follow standard SEIR dynamics:

- **S → E** — contact with an infected agent, probability = `beta * contact_rate * (1 - immunity)`
- **E → I** — after incubation period (pathogen-specific, e.g. 5 days for COVID-19)
- **I → R** — after infectious period (pathogen-specific, e.g. 7 days for COVID-19)

Contacts per day are calibrated from the WHO POLYMOD study: children average 10.4 contacts, adults 8.0.

### Mutation System

When infection rates cross configurable thresholds, mutations can trigger — modifying R0, transmission rate, and mortality with biologically-constrained changes. A 15-day cooldown prevents unrealistic mutation frequency.

### Reinforcement Learning

The Q-Learning agent operates over a 5-action discrete space (no action, masks, school closure, masks + school closure, vaccination). State is discretized from the observation vector: `[infected_ratio, child_infected, adult_infected, hospital_load, economic_cost]`. The reward balances infection reduction against economic cost.

### Symptom Prediction

Uses weighted Euclidean distance to compare a new virus's epidemiological parameters (R0, CFR, incubation period, etc.) against 6 historical pandemics (COVID-19, SARS, MERS, H1N1, Ebola, Seasonal Flu). Outputs predicted symptom profiles with prevalence estimates and confidence scores.

---

## Intervention Policies

| Policy | Effect |
|---|---|
| Mask Mandate | 40% reduction in contact rate for all agents |
| School Closure | Additional 70% contact reduction for children |
| Vaccination | Immunity boost (50–85% effectiveness, scaled by pathogen severity) |

---

## Troubleshooting

**Q-table not found (AI mode):**
Train locally first with `python rl/train.py`. The dashboard falls back to manual mode if no Q-table exists.

**Mutations not appearing:**
Enable "Virus Mutations" in the sidebar. Use no intervention to let infection rates climb above the mutation threshold. Run for 60+ days.

**Module import errors:**
Run from the project root directory where `app.py` is located. Install all dependencies with `pip install -r requirements.txt`.

---

## Team

**Team Neural Mavericks** — PRAKALP 2026, Hope Foundation's I²IT, Pune

- Team Lead: Parth Bhad (parthbhad2@gmail.com)

---

## License

Educational use — created for PRAKALP 2026 Hackathon.
