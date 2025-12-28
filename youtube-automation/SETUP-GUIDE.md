# Step-by-Step Setup Guide

Complete setup instructions for YouTube automation with n8n - 10-12 minute videos, 5 times per week, natural US voiceover.

## 🚀 Complete Setup (30-45 minutes)

### Part 1: Install Required Software (10 minutes)

#### 1. Install n8n

**Option A: Using Docker (Recommended)**
```bash
# Create directory for n8n data
mkdir -p ~/.n8n

# Run n8n container
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  --restart unless-stopped \
  docker.n8n.io/n8nio/n8n

# Verify it's running
docker ps | grep n8n

# Access n8n at: http://localhost:5678
```

**Option B: Using npm**
```bash
# Install Node.js (if not installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install n8n globally
npm install n8n -g

# Start n8n
n8n start

# Access at: http://localhost:5678
```

#### 2. Install FFmpeg (Required for video processing)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y ffmpeg

# Verify installation
ffmpeg -version
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

#### 3. Install Python & Dependencies (For thumbnail generation)

```bash
# Install Python 3
sudo apt install -y python3 python3-pip

# Install required libraries
pip3 install pillow requests
```

### Part 2: Get API Keys (15 minutes)

#### 1. YouTube Data API (Free)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "YouTube Automation" → Create
4. Wait for project creation (30 seconds)
5. Click "Enable APIs and Services"
6. Search for "YouTube Data API v3"
7. Click "Enable"
8. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
9. Configure consent screen:
   - User Type: External
   - App name: "YouTube Automation"
   - Support email: Your email
   - Save and continue through all steps
10. Create OAuth client ID:
    - Application type: Web application
    - Name: "n8n YouTube"
    - Authorized redirect URIs: `http://localhost:5678/rest/oauth2-credential/callback`
    - Click "Create"
11. **Download JSON file** with client ID and secret

**Note:** YouTube API has 10,000 quota units/day (free). Each video upload uses ~1,600 units, so you can upload 6 videos/day.

#### 2. Google Gemini API (Free - Best for scripts)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Get API Key"
4. Create API key for your project
5. **Copy and save the API key**

**Free tier:** 60 requests per minute

#### 3. ElevenLabs API (Free - Natural voiceover)

1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up for free account
3. Go to Profile Settings → API Keys
4. Click "Generate API Key"
5. **Copy and save the API key**

**Free tier:** 10,000 characters per month
- At ~1,900 words per script = ~10,000 characters
- You can generate 1 video per month on free tier
- **Alternative:** Use Google Cloud TTS (1 million characters/month free)

#### 4. Pexels API (Free - Stock footage)

1. Go to [Pexels API](https://www.pexels.com/api/)
2. Click "Get Started"
3. Sign up for free account
4. Generate API key
5. **Copy and save the API key**

**Free tier:** 200 requests per hour (more than enough)

#### 5. Alternative: Google Cloud Text-to-Speech (Free)

If you want to save ElevenLabs quota:

1. In Google Cloud Console (same project as YouTube)
2. Enable "Cloud Text-to-Speech API"
3. Use same OAuth credentials

**Free tier:** 1 million characters/month (enough for 50+ videos)

### Part 3: Configure n8n (10 minutes)

#### 1. Access n8n

```bash
# Open browser
http://localhost:5678

# Create your admin account
# Username: admin
# Password: [choose secure password]
```

#### 2. Add Credentials

**YouTube OAuth2:**
1. Click Settings (gear icon) → Credentials
2. Click "New" → Search "YouTube"
3. Select "YouTube OAuth2 API"
4. Enter:
   - Client ID: From downloaded JSON
   - Client Secret: From downloaded JSON
5. Click "Connect my account"
6. Authorize in popup window
7. Save

**HTTP Header Auth (for Gemini):**
1. Credentials → New → "Header Auth"
2. Name: "Gemini API"
3. Name: `x-goog-api-key`
4. Value: Your Gemini API key
5. Save

**HTTP Header Auth (for ElevenLabs):**
1. Credentials → New → "Header Auth"
2. Name: "ElevenLabs API"
3. Name: `xi-api-key`
4. Value: Your ElevenLabs API key
5. Save

**HTTP Header Auth (for Pexels):**
1. Credentials → New → "Header Auth"
2. Name: "Pexels API"
3. Name: `Authorization`
4. Value: Your Pexels API key
5. Save

#### 3. Set Environment Variables

Create `.env` file:

```bash
# Navigate to n8n directory
cd ~/.n8n

# Create .env file
cat > .env << 'EOF'
# n8n Configuration
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_HOST=localhost

# Video Settings
VIDEO_LENGTH_MIN=10
VIDEO_LENGTH_MAX=12
VIDEO_DIRECTORY=/home/$USER/youtube-videos/output
TEMP_DIRECTORY=/home/$USER/youtube-videos/temp

# Upload Schedule (5 times per week)
# Monday, Tuesday, Thursday, Friday, Saturday at 9 AM
UPLOAD_SCHEDULE=0 9 * * 1,2,4,5,6

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here

# Content Settings
VIDEO_NICHE=technology
TARGET_AUDIENCE=US viewers 18-45
VOICE_GENDER=female
VOICE_STYLE=natural

# US-Specific Settings
TARGET_COUNTRY=US
PRIMARY_LANGUAGE=en-US
SPEAKING_RATE=155

# YouTube Settings
YOUTUBE_CATEGORY=22
DEFAULT_TAGS=tutorial,howto,2024
EOF

# Create video directories
mkdir -p ~/youtube-videos/output
mkdir -p ~/youtube-videos/temp

# Restart n8n to load env variables
docker restart n8n
# OR if using npm:
# n8n stop && n8n start
```

### Part 4: Import Workflow (5 minutes)

#### 1. Download Workflow File

The workflow file `youtube-automation-workflow.json` is in this repository.

#### 2. Import into n8n

1. In n8n interface, click "Workflows" in left sidebar
2. Click "+ Add Workflow"
3. Click the three dots menu (⋮) → "Import from File"
4. Select `youtube-automation-workflow.json`
5. Workflow will open with all nodes

#### 3. Configure Workflow Nodes

Go through each node and verify/update:

**Schedule Trigger:**
- Cron expression: `0 9 * * 1,2,4,5,6` (Mon, Tue, Thu, Fri, Sat at 9 AM)

**Generate Natural Script node:**
- Update the prompt with your specific niche
- Example niches: "productivity tips", "tech reviews", "cooking tutorials"

**Voice Selection:**
- Choose either ElevenLabs or Google TTS node
- Disable the one you're not using (right-click → Disable)

**YouTube Upload node:**
- Link your YouTube credentials
- Set privacy status: `public`, `unlisted`, or `private`

### Part 5: Test Run (10 minutes)

#### 1. Manual Test (Before Automation)

```bash
# In n8n interface:
# 1. Click "Execute Workflow" button (top right)
# 2. Watch execution in real-time
# 3. Check each node for green checkmark ✓
# 4. Review any errors (red X)
```

#### 2. Test Individual Components

**Test Script Generation:**
```bash
# In n8n, select "Generate Natural Script" node
# Click "Execute Node" (small play button)
# Check output - should be ~1,900 words
```

**Test Voiceover:**
```bash
# Run voiceover node
# Download the audio file
# Listen to ensure it sounds natural
# Duration should be 10-12 minutes
```

**Test Video Assembly:**
```bash
# Make sure temp directory has:
# - voiceover.mp3
# - Several video clips from Pexels
# Then run FFmpeg assembly node
```

#### 3. First Full Upload

```bash
# Before automating, do 1-2 manual test uploads:
# 1. Execute full workflow
# 2. Check YouTube for uploaded video
# 3. Verify:
#    - Title and description are good
#    - Video is 10-12 minutes
#    - Voice sounds natural
#    - Thumbnail looks professional
#    - Video quality is 1080p
```

### Part 6: Activate Automation

#### 1. Enable Workflow

```bash
# In n8n interface:
# 1. Toggle workflow "Active" switch (top right)
# 2. You'll see "Workflow activated" message
# 3. Workflow will now run on schedule
```

#### 2. Monitor First Week

```bash
# Check executions:
# 1. Go to "Executions" tab
# 2. View status of each run
# 3. Debug any failures
# 4. Review uploaded videos on YouTube
```

## 📋 Pre-Flight Checklist

Before going live, verify:

### API Keys
- [ ] YouTube OAuth2 configured and tested
- [ ] Gemini API key working (test with curl)
- [ ] ElevenLabs or Google TTS key working
- [ ] Pexels API key working

### Software
- [ ] n8n running and accessible
- [ ] FFmpeg installed (`ffmpeg -version`)
- [ ] Python installed with Pillow (`python3 -c "import PIL"`)

### Directories
- [ ] Output directory exists and writable
- [ ] Temp directory exists and writable
- [ ] Sufficient disk space (5GB+ recommended)

### Workflow
- [ ] All credentials linked to nodes
- [ ] Schedule set to correct times
- [ ] Script prompt customized for your niche
- [ ] Voice selected (US accent)
- [ ] Test run completed successfully

### YouTube Channel
- [ ] Channel created and verified
- [ ] Channel art and description set
- [ ] About page filled out
- [ ] Default upload settings configured

## 🔧 Configuration for Different Niches

### Tech/Tutorial Channel

```bash
VIDEO_NICHE="technology tutorials"
TARGET_AUDIENCE="beginners learning tech"
VOICE_STYLE="clear and educational"
SPEAKING_RATE=150

# Script prompt addition:
"Use simple explanations, avoid jargon, include step-by-step instructions"
```

### Business/Finance Channel

```bash
VIDEO_NICHE="business and finance"
TARGET_AUDIENCE="US professionals 25-45"
VOICE_STYLE="professional and authoritative"
SPEAKING_RATE=160

# Script prompt addition:
"Use business terminology, include statistics, sound professional yet approachable"
```

### Lifestyle/Entertainment Channel

```bash
VIDEO_NICHE="lifestyle and entertainment"
TARGET_AUDIENCE="US millennials and Gen Z"
VOICE_STYLE="casual and energetic"
SPEAKING_RATE=165

# Script prompt addition:
"Use casual language, be enthusiastic, include pop culture references"
```

### Health/Wellness Channel

```bash
VIDEO_NICHE="health and wellness"
TARGET_AUDIENCE="US health-conscious adults"
VOICE_STYLE="caring and encouraging"
SPEAKING_RATE=155

# Script prompt addition:
"Use encouraging tone, include disclaimers, sound like a helpful friend"
```

## 🛠️ Troubleshooting Common Issues

### Issue: "API quota exceeded"

**Solution:**
```bash
# Check YouTube API quota
# Go to: console.cloud.google.com/apis/api/youtube.googleapis.com/quotas

# If exceeded:
# 1. Wait until quota resets (midnight Pacific Time)
# 2. Request quota increase (takes 2-3 days)
# 3. Reduce upload frequency temporarily
```

### Issue: "Video too short/long"

**Solution:**
```bash
# Adjust script word count in prompt:
# For exactly 10 min: "Write exactly 1,550 words"
# For exactly 11 min: "Write exactly 1,700 words"  
# For exactly 12 min: "Write exactly 1,850 words"

# Or adjust speaking rate in TTS:
"speaking_rate": 1.05  # Slightly faster = shorter video
"speaking_rate": 0.95  # Slightly slower = longer video
```

### Issue: "Voice sounds robotic"

**Solution:**
```bash
# If using ElevenLabs:
# - Try different voice IDs
# - Increase stability to 0.6-0.7
# - Add more conversational language to script

# If using Google TTS:
# - Use Neural2 voices only (most natural)
# - Add SSML breaks and emphasis
# - Adjust prosody settings
```

### Issue: "FFmpeg fails"

**Solution:**
```bash
# Test FFmpeg manually:
cd ~/youtube-videos/temp
ffmpeg -i test.mp4 -c copy test_output.mp4

# If error, check:
# 1. FFmpeg is installed: which ffmpeg
# 2. Input files exist: ls -la
# 3. Sufficient disk space: df -h
# 4. Correct file permissions: chmod 644 *.mp4
```

### Issue: "Can't find stock footage"

**Solution:**
```bash
# Broaden search query:
# Instead of: "specific technical term"
# Use: "technology" or "business" or "people working"

# Fallback: Use static images from Pexels Photos API
# Or: Create slideshow from images only
```

## 📈 Optimization After Launch

### Week 1: Monitor & Adjust
- Check all 5 videos uploaded successfully
- Review YouTube Analytics
- Read comments for feedback
- Adjust voice or script style if needed

### Week 2: Refine SEO
- Analyze which titles get more clicks
- Refine description template
- Test different tag combinations
- Optimize thumbnails

### Week 3: Scale Up
- If all working well, continue
- Consider upgrading API tiers for better voices
- Add more varied content topics
- Experiment with video styles

### Month 2: Analyze & Improve
- Review which videos perform best
- Double down on successful topics
- Improve retention with better hooks
- Engage with community

## 💰 Cost Breakdown (Free Tier Limits)

**Monthly Limits (All Free):**
- YouTube uploads: Unlimited (quota: 6/day)
- Gemini API: 1,800 requests/month (more than enough)
- Google TTS: 1M characters = 50+ videos
- Pexels: Unlimited within rate limits
- n8n: Free (self-hosted)
- FFmpeg: Free (open source)

**Paid Upgrades (Optional):**
- ElevenLabs Creator: $22/month (100k characters)
- Google Cloud credits: $300 free trial
- VPS hosting for n8n: $5-10/month

**Recommended: Start 100% free, upgrade only if needed**

## 🎯 Success Metrics

Track these to ensure system is working:

**Technical:**
- Upload success rate: Should be 100%
- Video duration: 10-12 minutes consistently
- Processing time: <30 minutes per video
- Error rate: <5%

**Content:**
- Average view duration: >50%
- Click-through rate: >4%
- Engagement rate: >3%
- Subscriber conversion: >0.5%

## 🆘 Getting Help

If you encounter issues:

1. **Check n8n logs:**
   ```bash
   docker logs n8n
   # or
   ~/.n8n/logs/
   ```

2. **n8n Community Forum:**
   https://community.n8n.io/

3. **YouTube API Status:**
   https://www.google.com/appsstatus

4. **FFmpeg Documentation:**
   https://ffmpeg.org/ffmpeg.html

## ✅ You're Ready!

Once all steps are complete:
1. Workflow is active ✓
2. First test video uploaded ✓
3. Schedule verified (5x/week) ✓
4. Voice sounds natural ✓
5. Videos are 10-12 minutes ✓

**Your YouTube channel is now fully automated!** 🎉

The system will:
- Find trending topics automatically
- Create scripts for US audience
- Generate natural voiceovers
- Assemble videos
- Upload 5 times per week (Mon, Tue, Thu, Fri, Sat)

**Sit back and let the automation work for you!** 🚀
