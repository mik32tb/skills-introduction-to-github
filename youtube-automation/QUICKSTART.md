# Quick Start Guide - YouTube Automation

Get your automated YouTube channel running in under 1 hour!

## 🚀 Super Fast Setup (For the impatient!)

### Step 1: Install n8n (5 minutes)

```bash
# Using Docker (easiest)
docker run -d --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n docker.n8n.io/n8nio/n8n

# OR using npm
npm install n8n -g && n8n start
```

### Step 2: Get Free API Keys (15 minutes)

**YouTube** (Required):
1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create project → Enable "YouTube Data API v3"
3. Create OAuth credentials → Download JSON
4. ✅ Done!

**Google Gemini** (For scripts - Free):
1. Go to [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Copy key
4. ✅ Done!

**Google Cloud TTS** (For voiceover - Free):
1. Same project as YouTube
2. Enable "Cloud Text-to-Speech API"
3. Use same OAuth credentials
4. ✅ Done!

**Pexels** (For stock footage - Free):
1. Go to [pexels.com/api](https://www.pexels.com/api/)
2. Sign up → Generate key
3. Copy key
4. ✅ Done!

### Step 3: Install FFmpeg (2 minutes)

```bash
# Ubuntu/Debian
sudo apt install ffmpeg -y

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### Step 4: Configure (5 minutes)

```bash
# Create directories
mkdir -p ~/youtube-videos/{output,temp,archive}

# Copy environment template
cp youtube-automation/.env.example ~/.n8n/.env

# Edit with your API keys
nano ~/.n8n/.env

# Add your keys:
# - GEMINI_API_KEY
# - PEXELS_API_KEY
# - YOUTUBE_CLIENT_ID
# - YOUTUBE_CLIENT_SECRET

# Save and exit (Ctrl+X, Y, Enter)
```

### Step 5: Import Workflow (3 minutes)

1. Open n8n: `http://localhost:5678`
2. Create account (any email/password)
3. Click "+ Add Workflow"
4. Click ⋮ → "Import from File"
5. Select `youtube-automation-workflow.json`
6. Click "Save"

### Step 6: Add Credentials (10 minutes)

In n8n:

**YouTube:**
1. Settings → Credentials → New
2. Search "YouTube OAuth2 API"
3. Enter Client ID and Secret
4. Click "Connect my account"
5. Authorize

**Other APIs:**
1. Create "Header Auth" credentials
2. For Gemini: Header = `x-goog-api-key`, Value = your key
3. For Pexels: Header = `Authorization`, Value = your key

### Step 7: Customize (5 minutes)

In the workflow, update these nodes:

**"Select Topic for US Audience"** node:
- Change `targetAudience` to match your niche
- Example: "US tech enthusiasts", "US fitness beginners"

**"Generate Natural Script"** node:
- Update the niche in the prompt
- Example: Change "technology" to your niche

**"Voice Selection"**:
- Choose male or female voice
- Use voice ID from VOICEOVER-GUIDE.md

### Step 8: Test Run (10 minutes)

```bash
# In n8n interface:
# 1. Make sure workflow is open
# 2. Click "Execute Workflow" (top right)
# 3. Watch the execution
# 4. Check for any errors
# 5. If successful, check YouTube for uploaded video!
```

### Step 9: Activate Automation (1 minute)

```bash
# In n8n:
# 1. Toggle "Active" switch (top right)
# 2. Workflow will now run automatically 5x per week!
```

### Step 10: Done! 🎉

Your channel will now:
- ✅ Find trending topics automatically
- ✅ Generate natural-sounding scripts (1,800-1,900 words)
- ✅ Create 10-12 minute videos
- ✅ Upload 5 times per week (Mon, Tue, Thu, Fri, Sat at 9 AM)
- ✅ Use natural US voiceover
- ✅ Optimize for SEO
- ✅ Target US audience

---

## 📝 Checklist

Before going live, make sure:

- [ ] n8n is running (`docker ps` or check `localhost:5678`)
- [ ] FFmpeg installed (`ffmpeg -version`)
- [ ] All API keys added to `.env`
- [ ] Credentials configured in n8n
- [ ] Workflow imported and saved
- [ ] Test run completed successfully
- [ ] First video uploaded to YouTube
- [ ] Workflow activated (toggle switch ON)
- [ ] Schedule verified (5x per week)

---

## 🆘 Quick Troubleshooting

**"Can't connect to YouTube"**
→ Check OAuth credentials, make sure redirect URI is correct

**"Script too short/long"**
→ Adjust word count in script generation prompt (1,800-1,900 words for 10-12 min)

**"Voice sounds robotic"**
→ Use Neural2 voices from Google TTS, not Standard voices

**"No stock footage found"**
→ Broaden your search query, try generic terms like "technology" or "business"

**"FFmpeg error"**
→ Run `ffmpeg -version` to verify installation

**"Workflow won't activate"**
→ Check that all required credentials are configured

**"Video upload fails"**
→ Check YouTube API quota at console.cloud.google.com

---

## 📊 Expected Results

**Week 1:**
- 5 videos uploaded (Mon, Tue, Thu, Fri, Sat)
- Each 10-12 minutes long
- Natural US voiceover
- SEO optimized

**Week 2:**
- Another 5 videos
- Start seeing analytics
- Adjust based on performance

**Month 1:**
- ~20 videos total
- Growing subscriber base
- Refined content strategy

---

## 🎯 Next Steps

After setup:

1. **Monitor First Week**
   - Check that all 5 videos upload successfully
   - Review video quality
   - Read YouTube comments for feedback

2. **Optimize Based on Data**
   - Check YouTube Analytics after 2 weeks
   - See which topics perform best
   - Adjust script style if needed

3. **Scale Up**
   - Consider upgrading API tiers for better voices
   - Experiment with different video styles
   - Add more variety to content

4. **Engage with Audience**
   - Reply to comments (can semi-automate)
   - Create content based on requests
   - Build community

---

## 💰 Costs (All Free Tier)

- **n8n**: Free (self-hosted)
- **YouTube API**: Free (10k quota/day)
- **Google Gemini**: Free (60 req/min)
- **Google TTS**: Free (1M chars/month = 50+ videos)
- **Pexels**: Free (200 req/hour)
- **FFmpeg**: Free (open source)

**Total: $0/month** ✅

Optional upgrades:
- ElevenLabs: $22/month (more natural voice)
- VPS hosting: $5/month (run 24/7)

---

## 📚 Full Documentation

For detailed guides, see:

- **README.md** - Complete feature overview
- **SETUP-GUIDE.md** - Detailed step-by-step setup
- **VOICEOVER-GUIDE.md** - Natural voiceover configuration
- **EXAMPLE-SCRIPTS.md** - Sample scripts for reference
- **.env.example** - All configuration options

---

## 🎬 Example Timeline

**Sunday Evening:**
- System finds trending topics for the week
- Generates 5 scripts (one for each upload day)
- Pre-processes content

**Monday 9 AM:**
- Video 1 generates automatically
- Uploads to YouTube
- You get notification

**Tuesday 9 AM:**
- Video 2 generates and uploads

**Wednesday:**
- No upload (planning day)

**Thursday 9 AM:**
- Video 3 generates and uploads

**Friday 9 AM:**
- Video 4 generates and uploads

**Saturday 9 AM:**
- Video 5 generates and uploads

**Sunday:**
- Review week's performance
- System plans next week's content
- Repeat!

---

## ✅ You're All Set!

Your YouTube channel is now fully automated. The system will handle:

- Content discovery ✓
- Script writing ✓
- Voiceover generation ✓
- Video creation ✓
- SEO optimization ✓
- Thumbnail creation ✓
- YouTube upload ✓
- Scheduling ✓

All you need to do is:
- Monitor performance
- Engage with comments
- Adjust strategy based on analytics

**Welcome to automated content creation!** 🚀🎉

---

Need help? Check the troubleshooting section or review the full documentation files!
