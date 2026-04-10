# AWS AI for Bharat Hackathon Final Deliverables

## 1. Three-Minute Video Pitch Script

Hello judges, we are Team Neural Mavericks, and this is EpiControl AI plus Project Sentinel.

Let me start with the question from the earlier feedback: will this predict the upcoming pandemic just like COVID-19?

Our answer is precise. No model can promise the exact identity of the next COVID-scale pandemic. But what we can do, and what India urgently needs, is detect weak outbreak signals earlier, translate them into actionable epidemiological parameters, and simulate intervention strategies before the crisis becomes nationwide. That is exactly what Project Sentinel does.

EpiControl AI is an advanced epidemic simulation platform built to shift pandemic management from reactive response to proactive decision intelligence.

On the screen, this is our manual SEIR simulation engine. At the core is a vectorized agent-based epidemiological model built in Python, Streamlit, and NumPy. We model a population across the four disease states: Susceptible, Exposed, Infected, and Recovered. Users can configure pathogen behavior using transmission rate, incubation period, infectious duration, and mortality rate. We also support city-level presets, intervention policies, and mutation-aware epidemic dynamics.

Here, I can choose the simulation duration, population size, pathogen profile, and public health controls such as mask mandates, school closures, and vaccination. When I run the simulation, the platform generates epidemic curves, spatial spread views, and operational metrics. This gives public health planners a transparent baseline model they can trust and inspect.

Now let us move to the innovation layer: Sentinel AI.

In real outbreaks, decision-makers do not receive clean epidemiological tables on day one. They receive fragmented news, local alerts, and unstructured field reports. So we integrated Amazon Bedrock with Anthropic Claude 3 Sonnet for syndromic surveillance.

I paste in a sample intelligence report: fifty children in Pune have developed a mysterious cough, the spread appears highly contagious, no deaths are reported yet, and the incubation period seems to be four days.

When I click Run AWS Bedrock Analysis, Bedrock parses that unstructured text and returns strict JSON with the extracted outbreak parameters: estimated R0, incubation days, infectious days, mortality rate, and a trigger warning flag. This is important because our system does not stop at summarization. It converts language into machine-readable simulation inputs.

That means even before lab-confirmed structured datasets are available, health teams can initialize a scenario and start testing containment policies.

Next is the RL engine. We trained a Q-Learning policy agent over roughly three hundred thousand episodes to optimize localized intervention strategies. Instead of imposing blanket lockdowns by default, the agent learns how to balance infection reduction against intervention cost. In AI mode, the system evaluates the epidemic state continuously and recommends actions such as masks, school closures, combined restrictions, or vaccination drives.

The outcome is not only fewer infections. It is smarter control with lower social and economic disruption, which is critical in a country as large and diverse as India.

Our AWS stack made this practical and deployable. The application runs on Amazon EC2, background services are managed with tmux, Bedrock powers the generative AI extraction layer, and IAM roles secure cloud access without hardcoded credentials.

To close, the impact for Bharat is clear.

India cannot afford to wait for outbreaks to become obvious. Project Sentinel gives hospitals, districts, and administrators a proactive system that can detect weak signals early, simulate likely spread, and recommend targeted interventions before escalation. This is not just outbreak visualization. It is decision intelligence for resilient public health in India.

Thank you.

## 2. AWS Builder Center Blog Post Draft

### Project Sentinel: Using Amazon Bedrock and RL to Predict and Prevent Pandemics in India

Pandemic response is still largely reactive. Public health teams usually act only after outbreaks are visible in confirmed case data, hospital admissions, or laboratory reporting pipelines. By the time structured datasets are available, disease transmission may already be widespread. For a country like India, where population density, mobility patterns, and healthcare access vary dramatically by region, delayed action can turn a local cluster into a large-scale emergency.

Our hackathon prototype, Project Sentinel with EpiControl AI, was built to address that gap. The system combines epidemic simulation, reinforcement learning, and generative AI on AWS to move decision-making from reactive to proactive. Instead of waiting for perfect data, we ingest early unstructured outbreak signals, convert them into strict epidemiological parameters, and use them to test containment strategies before the situation escalates.

### Why reactive epidemiological modeling falls short

Traditional dashboards are useful for monitoring what has already happened. They show case counts, fatalities, or historical trends, but they often do not help officials answer the more urgent question: what should we do next, and how early can we act?

EpiControl AI addresses this by combining a manual SEIR simulation engine with an RL-based control layer. The core platform is built in Python and Streamlit, with a vectorized agent-based SEIR model powered by NumPy. Users can configure pathogen behavior through transmission rate, incubation period, infectious duration, mortality rate, and intervention policies such as masking, school closure, and vaccination. This creates an interactive sandbox where outbreak scenarios can be evaluated quickly.

But for emerging threats, the real challenge is not only simulation. It is initialization. Early in an outbreak, data may exist only as fragmented intelligence: a local news report, a hospital bulletin, or a field observation that “dozens of children in Pune have a mysterious cough.” We wanted to turn these weak signals into simulation-ready inputs.

### Using Amazon Bedrock for syndromic surveillance

To solve that problem, we integrated Amazon Bedrock with Anthropic Claude 3 Sonnet. Our Sentinel module accepts unstructured outbreak text and prompts the model to extract a strict JSON object containing parameters such as estimated R0, incubation period, infectious period, mortality rate, and whether a warning should be triggered.

This design choice was deliberate. We were not looking for a narrative summary. We needed machine-readable outputs that could feed directly into a simulation workflow. The prompt enforces a JSON-only response with a tightly constrained schema, reducing downstream parsing complexity and making the output usable inside an epidemiological pipeline.

In practice, this means a district health team could paste a field report into the app and immediately obtain structured assumptions for scenario testing. Even if those values are preliminary, they allow planners to start exploring intervention outcomes earlier than they could with conventional surveillance workflows.

That early-start capability is the core innovation of Project Sentinel: generative AI as a front-end intelligence extractor for epidemiological decision support.

### Reinforcement learning for policy optimization

Once the initial conditions are available, our reinforcement learning layer takes over. We trained a Q-Learning agent over approximately 300,000 episodes to optimize localized public health actions. The action space includes options such as no intervention, mask mandates, school closure, combined restrictions, and vaccination campaigns.

The reward function balances epidemic suppression against the social and economic cost of intervention. This matters in the Indian context, where blanket restrictions can impose heavy secondary costs. Rather than assuming maximum lockdown is always optimal, the system learns targeted actions that reduce infections while preserving normal activity where possible.

The result is a more nuanced public health engine: one part epidemic simulator, one part policy optimizer, and one part early warning system.

### Deploying on Amazon EC2 with secure IAM roles

We deployed the Streamlit application on an Amazon EC2 instance running Amazon Linux. EC2 gave us direct control over the runtime environment, which mattered because our stack included scientific Python libraries, model artifacts, and cloud inference calls.

For operational reliability, background processes were managed with tmux, allowing the app and related long-running tasks to remain active across SSH sessions. For security, we used AWS IAM roles attached to the EC2 instance instead of storing credentials in source code or environment files. That allowed boto3 to access Bedrock securely using temporary credentials provided by the instance profile.

This was an important architectural decision: it simplified deployment while aligning with cloud security best practices.

### Overcoming the PyTorch bottleneck on EC2

One of the biggest engineering hurdles we hit was package installation time and footprint. Standard PyTorch installations can be large, and in our case the dependency path was creating a roughly 900 MB bottleneck during deployment. That significantly slowed setup and made iteration painful on the EC2 instance.

We resolved this by switching to CPU-only PyTorch wheels. Since our inference and reinforcement learning demo path did not require GPU acceleration on the deployed instance, CPU wheels were the right tradeoff. This reduced installation overhead, improved provisioning speed, and made the application more practical to deploy within hackathon constraints.

It was a simple optimization, but it had a major impact on delivery velocity.

### Why this matters for India

India needs outbreak intelligence systems that can work with incomplete information, adapt across regions, and support early intervention. Project Sentinel is designed around that reality. By combining Amazon Bedrock for structured signal extraction, EC2 for controlled deployment, IAM roles for secure access, and reinforcement learning for policy optimization, we built a prototype that helps decision-makers act before an outbreak becomes unmanageable.

We do not claim to predict the exact next pandemic. We do claim that earlier signal detection plus scenario-based intervention planning can improve preparedness. For India, that shift from reactive monitoring to proactive response could be the difference between local containment and system-wide crisis.

## 3. Submission Presentation Deck Outline

### Slide 1: Title Slide
- EpiControl AI + Project Sentinel
- Team Neural Mavericks
- AWS AI for Bharat Hackathon Final Prototype
- Tagline: From reactive outbreak response to proactive epidemic intelligence

### Slide 2: The Problem
- Pandemic systems often react only after structured case data becomes available
- Early outbreak signals usually appear first in unstructured local reports
- India needs faster, localized, lower-cost public health decision support
- Existing tools monitor spread, but do not convert weak signals into action plans

### Slide 3: Our Solution
- Project Sentinel combines early warning, simulation, and policy optimization
- Unstructured news or field intelligence is converted into epidemiological inputs
- SEIR simulation tests likely spread scenarios before escalation
- RL recommends targeted interventions instead of default blanket lockdowns

### Slide 4: Core Platform Architecture
- Frontend and control layer built in Python and Streamlit
- Vectorized agent-based SEIR engine implemented with NumPy
- Policy engine supports masks, school closures, vaccination, and comparison mode
- Modular design allows simulation, AI control, and Bedrock parsing to work together

### Slide 5: Manual SEIR Walkthrough
- User selects pathogen, population, days, and city configuration
- Core parameters include R0, incubation period, infectious period, and mortality rate
- Simulation outputs SEIR curves, spatial spread, and operational metrics
- Transparent manual mode builds trust and interpretability for decision-makers

### Slide 6: RL Policy Optimization
- Q-Learning agent trained on roughly 300,000 episodes
- Agent evaluates outbreak state and chooses localized control actions
- Reward balances infection reduction against intervention cost
- Goal: minimize health impact while reducing unnecessary disruption

### Slide 7: Sentinel Innovation with Amazon Bedrock
- User pastes unstructured outbreak text such as a local news report
- Amazon Bedrock with Claude 3 Sonnet extracts strict JSON parameters
- Output schema includes R0, incubation days, infectious days, mortality rate, and trigger warning
- Converts weak surveillance signals into machine-readable simulation inputs

### Slide 8: AWS Architecture
- Amazon EC2 hosts the Streamlit application on Amazon Linux
- Amazon Bedrock powers the generative AI extraction workflow
- AWS IAM roles secure service access with no hardcoded keys
- tmux keeps long-running app processes stable in the cloud environment

### Slide 9: Technical Excellence
- Vectorized simulation for fast scenario evaluation
- Strict JSON prompt design for robust Bedrock integration
- Secure cloud architecture using instance roles
- Deployment optimization using CPU-only PyTorch wheels to avoid installation bottlenecks

### Slide 10: Impact for India
- Enables earlier response in dense urban and resource-constrained settings
- Supports district-level scenario planning before outbreaks scale nationally
- Reduces dependence on late structured datasets alone
- Promotes proactive healthcare operations and resilient public health systems

### Slide 11: Market Opportunity and Users
- Public health departments and smart city command centers
- Hospitals, emergency planning teams, and disaster response units
- State and district administrations needing localized outbreak planning
- Future potential for integration with health surveillance and civic response platforms

### Slide 12: Roadmap
- Auto-populate simulation inputs from Bedrock JSON directly into scenario controls
- Expand multilingual surveillance ingestion for Bharat-scale accessibility
- Add district-level mobility and hospital capacity datasets
- Evolve from prototype to operational public health decision-support platform