# 🚀 EpiControl AI - Deployment Guide

## Live Demo Deployment on Streamlit Community Cloud

### Prerequisites
1. GitHub account
2. Streamlit Community Cloud account (free) - https://streamlit.io/cloud

### Step-by-Step Deployment

#### 1️⃣ Create GitHub Repository
```bash
# Initialize git in your project (if not already done)
cd d:\epicontrol_ai
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - EpiControl AI for PRAKALP 2026"

# Create a new repository on GitHub (https://github.com/new)
# Name it: epicontrol-ai

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/epicontrol-ai.git
git branch -M main
git push -u origin main
```

#### 2️⃣ Deploy on Streamlit Community Cloud

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click** "New app"
4. **Fill in**:
   - Repository: `YOUR_USERNAME/epicontrol-ai`
   - Branch: `main`
   - Main file path: `app.py`
5. **Click** "Deploy!"

⏱️ **Deployment takes 2-5 minutes**

#### 3️⃣ Your Live URL
You'll get a URL like: `https://YOUR_USERNAME-epicontrol-ai-app-xxxxx.streamlit.app`

---

## Alternative Deployment Options

### Option 2: Heroku Deployment

1. **Install Heroku CLI**: https://devcli.com/
2. **Create files**:

**Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt:**
```
python-3.10.12
```

3. **Deploy**:
```bash
heroku login
heroku create epicontrol-ai
git push heroku main
heroku open
```

### Option 3: Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build & Run:**
```bash
docker build -t epicontrol-ai .
docker run -p 8501:8501 epicontrol-ai
```

---

## 📋 Pre-Deployment Checklist

✅ **Files Ready**:
- [x] `requirements.txt` - All dependencies listed
- [x] `.gitignore` - Excludes unnecessary files
- [x] `.streamlit/config.toml` - Theme configuration
- [x] `README.md` - Project documentation

✅ **Code Ready**:
- [x] No hardcoded paths (use relative paths)
- [x] No secrets in code
- [x] Error handling for missing files
- [x] Graceful fallbacks for optional features

✅ **Performance**:
- [x] Session state properly managed
- [x] Large computations cached
- [x] Efficient data loading

---

## 🔧 Troubleshooting

### Issue: "Module not found"
**Fix**: Ensure all dependencies are in `requirements.txt` with correct versions

### Issue: "Memory limit exceeded"
**Fix**: Reduce default population size or add `@st.cache_data` decorators

### Issue: "App won't start"
**Fix**: Check logs in Streamlit Cloud dashboard, ensure all imports work

---

## 📱 Share Your App

Once deployed, share your link at:
- **PRAKALP 2026 Submission Portal**
- **LinkedIn**: Tag #PRAKALP2026 #EpiControlAI
- **Twitter**: Share with hackathon organizers
- **GitHub README**: Add badge with live demo link

### Deployment Badge
Add to your README.md:
```markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_APP_URL)
```

---

## 🎯 Post-Deployment

1. **Monitor**: Check Streamlit Cloud dashboard for usage
2. **Update**: Push to GitHub → Auto-deploys to cloud
3. **Feedback**: Share with judges and get feedback
4. **Iterate**: Improve based on usage analytics

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Community Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: For bug reports

---

**Good luck with PRAKALP 2026! 🚀**
