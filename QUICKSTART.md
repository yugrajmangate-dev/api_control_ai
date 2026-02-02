# ⚡ QUICK START COMMANDS - EPICONTROL AI

## 📋 Pre-Hackathon Setup (Do This Once)

### 1. Install Dependencies
```bash
pip install streamlit plotly numpy gym
```

### 2. Train the RL Agent (Takes ~2 minutes)
```bash
python rl/train.py
```
**Expected Output:**
```
============================================================
  RL TRAINING: COVID-19
============================================================
Episodes: 200
Population: 1000
Days per Episode: 60
Virus R0: 2.5
Base Beta: 0.3
============================================================

Starting training...
Episode 0/200 | Reward: -450.23 | Epsilon: 0.950
Episode 20/200 | Reward: -320.15 | Epsilon: 0.749
...
✅ Training completed!
💾 Q-table saved successfully as: rl/q_table_covid-19.pkl
```

---

## 🎬 Demo Commands (Day of Hackathon)

### Launch Interactive Dashboard
```bash
streamlit run app.py
```
**Opens:** http://localhost:8501

**Demo Flow:**
1. **Mutation Demo:**
   - Select: Manual Policy
   - Enable Mutations: ✓
   - Threshold: 30%
   - Interventions: None
   - Click "Run Simulation"
   - **Watch:** Mutation warnings appear

2. **Heatmap Demo:**
   - Scroll down after simulation
   - See red hotspots on heatmap
   - **Explain:** "These are outbreak centers"

3. **Policy Comparison:**
   - Switch to: Policy Comparison mode
   - Click "Run Simulation"
   - **Wait:** ~30 seconds (progress bar)
   - **Show:** Bar charts comparing 5 policies

---

### Test Transfer Learning
```bash
python rl/evaluate_transfer.py
```
**Expected Output:**
```
============================================================
  TRANSFER LEARNING DEMO: City A → City B
============================================================

[1] Loading agent trained on City A...
✅ Loaded Q-table from rl/q_table_covid19.pkl

[2] Evaluating on City A (original environment)...
   Total Reward: -280.45
   Peak Infected: 245
   Final Recovered: 856

[3] Deploying on City B (transfer learning)...
   Population: 1000 → 1500
   Total Reward: -420.12
   Peak Infected: 368
   Final Recovered: 1284

📊 Performance Comparison:
   City A Reward: -280.45
   City B Reward: -420.12
   Reward Change: +49.8%
...
```

---

### Run Tests (Optional - for debugging)
```bash
python test_features.py
```
**Expected:** 7/7 tests pass

---

## 🐛 Emergency Fixes

### "Streamlit not found"
```bash
pip install streamlit
```

### "No Q-table found"
```bash
python rl/train.py
```
*(Takes 2 minutes)*

### Dashboard shows error
**Check terminal output for specific error**

Common fix:
```bash
pip install plotly numpy gym
```

### Mutations not appearing
**In dashboard sidebar:**
- ✓ Enable Virus Mutations
- Set threshold lower: 0.20
- Use "No Intervention" policy
- Run for 60 days

---

## 📊 Dashboard Settings for Best Demo

### **For Mutation Demo:**
```
Population: 1000
Days: 60
Virus: COVID-19
Enable Mutations: ✓
Mutation Threshold: 0.30
Control Mode: Manual Policy
Interventions: All unchecked (to allow outbreak)
Show Heatmap: ✓
```
**Result:** Mutations will trigger around day 15-25

---

### **For Policy Comparison:**
```
Population: 1000
Days: 60
Virus: COVID-19
Enable Mutations: ✓
Control Mode: Policy Comparison
```
**Click "Run Simulation"**  
**Wait:** ~30 seconds  
**Result:** Bar charts showing 5 policy comparisons

---

### **For AI Demo:**
```
Population: 1000
Days: 60
Virus: COVID-19
Enable Mutations: ✓
Control Mode: AI (RL) Policy
```
**Result:** Shows AI's policy choices day by day

---

## ⏱️ Time Estimates

| Task | Duration |
|------|----------|
| Install dependencies | 1-2 min |
| Train RL agent | 2-3 min |
| Launch dashboard | 10 sec |
| Run one simulation | 5-10 sec |
| Policy comparison | 30-40 sec |
| Transfer learning | 30 sec |

---

## 📂 File Locations

**Important Files:**
- `app.py` - Main dashboard
- `rl/train.py` - Train agent
- `rl/evaluate_transfer.py` - Transfer demo
- `test_features.py` - Test suite

**Generated Files:**
- `rl/q_table_covid-19.pkl` - Trained agent
- `rl/q_table_covid-19_metadata.pkl` - Training info
- `rl/transfer_results.pkl` - Transfer results

---

## 🎤 Presentation Order

1. Open PowerPoint/Slides (intro slides)
2. Switch to browser (dashboard already open at localhost:8501)
3. **Demo 1:** Mutation (Manual mode, no intervention)
4. **Demo 2:** Heatmap (scroll down, point to red zones)
5. **Demo 3:** Policy Comparison (switch mode, run)
6. Switch back to slides (conclusion)

**Total Demo Time:** 5 minutes

---

## 🚨 If Demo Fails

### **Backup Plan:**
1. Have screen recording ready (record beforehand)
2. Have screenshots in slides
3. Can run `python rl/evaluate_transfer.py` in terminal (shows output)

### **Live Debugging:**
If dashboard crashes:
1. Check terminal for error
2. Restart: Ctrl+C, then `streamlit run app.py` again
3. If persists, show video/screenshots

---

## 💡 Pro Tips

1. **Before presenting:**
   - Close unnecessary tabs
   - Set zoom to 100%
   - Test projector connection
   - Have dashboard already open

2. **During demo:**
   - Talk while simulation runs ("Notice how...")
   - Point to specific visualizations
   - Use mouse to highlight areas

3. **If judges ask to see code:**
   - Open `env/mutation.py` (show MutationTracker class)
   - Open `visualization/plotly_plots.py` (show heatmap function)
   - These are most impressive implementations

---

## 📞 Emergency Contacts

- **Parth:** 9067829174
- **Student Coordinator 1:** 9860520386
- **Student Coordinator 2:** 7387081978

---

## ✅ Final Checklist (5 min before presentation)

- [ ] Dashboard running: `streamlit run app.py`
- [ ] Projector connected and working
- [ ] Browser zoom at 100%
- [ ] Terminal visible (for transfer demo if needed)
- [ ] Backup video ready
- [ ] Water bottle nearby
- [ ] Registration receipt in pocket
- [ ] Team members know their parts

---

## 🎯 Success Criteria

**You know it's working when:**
- ✅ Dashboard loads without errors
- ✅ Mutations appear with warning messages
- ✅ Heatmap shows red/orange zones
- ✅ Policy comparison shows 5 bar charts
- ✅ AI mode shows day-by-day decisions

**If all 5 work → You're ready! 🚀**

---

**Team: Neural Nexus**  
**Good Luck! 🏆**
