# YouTube Channel Automation with n8n - Full Video Production

This project provides a **complete end-to-end automation system** for running a YouTube channel using n8n and free tools. The system automatically finds content topics, generates scripts, creates 10-12 minute videos, optimizes for SEO, and uploads to YouTube **5 times per week**.

## 🎯 Features

- **Fully Automated Video Creation**: Creates complete 10-12 minute videos automatically
- **Content Discovery**: Finds trending topics and content automatically
- **Script Generation**: AI-powered script writing optimized for video length
- **Video Production**: Automated video generation with voiceover, visuals, and music
- **SEO Optimization**: Generate SEO-optimized titles, descriptions, and tags
- **Automatic Upload**: Upload videos to YouTube on schedule (5x per week)
- **Thumbnail Generation**: Create eye-catching thumbnails automatically
- **Scheduling**: Monday, Tuesday, Thursday, Friday, Saturday uploads

## 📋 Prerequisites

### Required Free Tools

1. **n8n** (Free, self-hosted)
   - Workflow automation platform
   - [Installation Guide](https://docs.n8n.io/hosting/)

2. **Video Generation Tools** (All Free)
   - **D-ID API** (Free tier - AI avatars & voiceover)
   - **Remotion** (Free - programmatic video creation)
   - **FFmpeg** (Free - video processing)
   - **Pexels API** (Free - stock footage)

3. **AI Content Tools** (Free)
   - **Hugging Face API** (Free tier)
   - **Google Gemini API** (Free tier)
   - **Perplexity API** (Free tier for research)

4. **YouTube & Google**
   - YouTube account with channel
   - Google Cloud Platform (free tier)
   - YouTube Data API v3 credentials

## 🚀 Quick Start

### Step 1: Install Required Software

```bash
# Install n8n
npm install n8n -g

# Install FFmpeg (for video processing)
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (use Chocolatey)
choco install ffmpeg

# Install Remotion (for programmatic video creation)
npm install -g @remotion/cli
```

### Step 2: Get API Keys (All Free)

1. **YouTube API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create project → Enable YouTube Data API v3
   - Create OAuth 2.0 credentials

2. **Google Gemini API** (Free)
   - Visit [Google AI Studio](https://makersuite.google.com/)
   - Generate free API key

3. **D-ID API** (Free 20 credits/month)
   - Sign up at [D-ID](https://www.d-id.com/)
   - Get API key from dashboard

4. **Pexels API** (Free)
   - Sign up at [Pexels](https://www.pexels.com/api/)
   - Generate API key

5. **ElevenLabs** (Free 10k characters/month)
   - Sign up at [ElevenLabs](https://elevenlabs.io/)
   - Get API key for voiceover

### Step 3: Configure Environment

Create `.env` file:

```env
# n8n Configuration
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_HOST=localhost

# YouTube API
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret
YOUTUBE_REDIRECT_URI=http://localhost:5678/rest/oauth2-credential/callback

# Video Settings
VIDEO_LENGTH_MIN=10
VIDEO_LENGTH_MAX=12
VIDEO_DIRECTORY=/home/user/videos/output
TEMP_DIRECTORY=/home/user/videos/temp

# Upload Schedule (5 times per week)
# Monday, Tuesday, Thursday, Friday, Saturday at 9 AM
UPLOAD_SCHEDULE=0 9 * * 1,2,4,5,6

# AI APIs (Free tiers)
GEMINI_API_KEY=your_gemini_key
HUGGINGFACE_API_KEY=your_hf_key
ELEVENLABS_API_KEY=your_elevenlabs_key
DID_API_KEY=your_did_key

# Content Discovery
PEXELS_API_KEY=your_pexels_key
VIDEO_NICHE=technology,tutorials,how-to
TARGET_AUDIENCE=beginners

# SEO Settings
PRIMARY_LANGUAGE=en
TARGET_COUNTRY=US
```

### Step 4: Import n8n Workflow

1. Start n8n: `n8n start`
2. Open: `http://localhost:5678`
3. Import: `youtube-automation-workflow.json`
4. Configure all credentials

## 🎬 Complete Automation Pipeline

### Phase 1: Content Discovery (Automated)

**Frequency**: Runs 5 times per week (Mon, Tue, Thu, Fri, Sat)

```
┌─────────────────────────────────────┐
│  Cron Trigger (5x per week)        │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Find Trending Topics               │
│  - Google Trends API                │
│  - YouTube Search Trends            │
│  - Reddit API (trending posts)      │
│  - Twitter/X trending hashtags      │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Topic Validation                   │
│  - Check competition                │
│  - Verify search volume             │
│  - Assess content freshness         │
└─────────────┬───────────────────────┘
              │
              ▼
        [Selected Topic]
```

### Phase 2: Script Generation (10-12 Minutes)

```
┌─────────────────────────────────────┐
│  Research Phase                     │
│  - Gather information (Gemini API)  │
│  - Find key points                  │
│  - Collect statistics               │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Script Writing (AI)                │
│  - Generate 1800-2000 word script   │
│  - Structure for 10-12 min video    │
│  - Add timestamps                   │
│  - Include hooks and CTAs           │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Script Validation                  │
│  - Check word count (1800-2000)     │
│  - Verify structure                 │
│  - Ensure engagement hooks          │
└─────────────┬───────────────────────┘
              │
              ▼
        [Final Script]
```

### Phase 3: Video Production (Automated)

```
┌─────────────────────────────────────┐
│  Voiceover Generation               │
│  - Text-to-Speech (ElevenLabs)      │
│  - Natural voice selection          │
│  - Pacing for 10-12 minutes         │
│  - Export as MP3                    │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Visual Content Collection          │
│  - Stock footage (Pexels API)       │
│  - AI-generated images              │
│  - Screen recordings (if tutorial)  │
│  - Animations                       │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Video Assembly (FFmpeg/Remotion)   │
│  - Sync visuals with voiceover      │
│  - Add transitions                  │
│  - Insert text overlays             │
│  - Add background music             │
│  - Color grading                    │
│  - Export as MP4 (1080p)            │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Quality Check                      │
│  - Verify duration (10-12 min)      │
│  - Check audio sync                 │
│  - Validate resolution              │
│  - Test playback                    │
└─────────────┬───────────────────────┘
              │
              ▼
        [Final Video MP4]
```

### Phase 4: SEO & Upload

```
┌─────────────────────────────────────┐
│  SEO Optimization                   │
│  - Generate title                   │
│  - Create description               │
│  - Research tags                    │
│  - Create thumbnail                 │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  YouTube Upload                     │
│  - Upload video file                │
│  - Set metadata                     │
│  - Add thumbnail                    │
│  - Publish or schedule              │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Post-Upload                        │
│  - Log to database                  │
│  - Send notification                │
│  - Archive files                    │
└─────────────────────────────────────┘
```

## 📝 Script Generation for 10-12 Minutes

### Target Metrics
- **Word Count**: 1,800 - 2,000 words
- **Speaking Rate**: 150-160 words per minute
- **Duration**: 10-12 minutes
- **Sections**: 5-7 main sections

### Script Structure

```
[HOOK - 30 seconds / 75 words]
- Attention-grabbing opening
- State the problem/topic
- Promise of value

[INTRODUCTION - 1 minute / 150 words]
- Welcome viewers
- Preview what's covered
- Build credibility

[MAIN CONTENT - 8 minutes / 1,200 words]
Section 1: [Topic A - 2 minutes / 300 words]
Section 2: [Topic B - 2 minutes / 300 words]
Section 3: [Topic C - 2 minutes / 300 words]
Section 4: [Topic D - 2 minutes / 300 words]

[PRACTICAL EXAMPLES - 1.5 minutes / 225 words]
- Real-world applications
- Tips and tricks
- Common mistakes to avoid

[CALL TO ACTION - 30 seconds / 75 words]
- Like, subscribe, comment
- Related videos
- Social media links

[OUTRO - 30 seconds / 75 words]
- Summary of key points
- Thank viewers
- Preview next video
```

## 🎥 Automated Video Creation Methods

### Method 1: AI Avatar with Stock Footage (Recommended)

**Tools**: D-ID + Pexels + FFmpeg

```javascript
// Workflow pseudocode
1. Generate voiceover from script (ElevenLabs API)
2. Create AI avatar video (D-ID API) OR
3. Download relevant stock footage (Pexels API)
4. Assemble with FFmpeg:
   - Add voiceover
   - Insert stock clips
   - Add transitions
   - Include text overlays
   - Add background music
5. Export final video
```

### Method 2: Slideshow Style Video

**Tools**: Remotion + Pexels + FFmpeg

```javascript
// Create programmatic video with Remotion
- Generate slides from script sections
- Add images from Pexels
- Animate text overlays
- Sync with voiceover
- Add background music
- Export as MP4
```

### Method 3: Screen Recording + Voiceover

**For tutorials/how-to content**

```javascript
// Automated screen recording
- Use puppeteer for browser automation
- Record screen with FFmpeg
- Add voiceover narration
- Include callouts and highlights
- Export final video
```

## 🗓️ Upload Schedule (5 Times Per Week)

```
Week Schedule:
├── Monday    09:00 AM - Upload Video 1
├── Tuesday   09:00 AM - Upload Video 2
├── Wednesday (OFF - Content preparation)
├── Thursday  09:00 AM - Upload Video 3
├── Friday    09:00 AM - Upload Video 4
├── Saturday  09:00 AM - Upload Video 5
└── Sunday    (OFF - Analytics review)
```

**n8n Cron Expression**: `0 9 * * 1,2,4,5,6`

## 🎨 Automated Thumbnail Generation

```python
# Using Python + Pillow (via n8n Python node)
from PIL import Image, ImageDraw, ImageFont
import requests

def create_thumbnail(title, background_image_url):
    # Download background image
    img = Image.open(requests.get(background_image_url, stream=True).raw)
    img = img.resize((1280, 720))
    
    # Add dark overlay
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 128))
    img = Image.alpha_composite(img.convert('RGBA'), overlay)
    
    # Add text
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 80)
    
    # Draw title (word wrap)
    draw.text((50, 300), title, font=font, fill='white')
    
    # Save thumbnail
    img.save('thumbnail.jpg', 'JPEG', quality=95)
    return 'thumbnail.jpg'
```

## 🔍 Content Discovery Algorithms

### 1. Trend Analysis

```javascript
// n8n HTTP Request nodes
sources = [
  'https://trends.google.com/trending',
  'https://www.youtube.com/feed/trending',
  'https://api.reddit.com/r/[niche]/hot',
  'https://api.twitter.com/2/trends'
]

topics = analyze_trends(sources)
filtered = filter_by_niche(topics, YOUR_NICHE)
scored = score_by_potential(filtered)
selected = pick_top_topic(scored)
```

### 2. Competitor Analysis

```javascript
// Find what's working for competitors
competitors = ['channel_id_1', 'channel_id_2']
recent_videos = get_recent_uploads(competitors)
high_performing = filter_by_views(recent_videos, min_views=10000)
topics = extract_topics(high_performing)
opportunities = find_gaps(topics)
```

### 3. Keyword Research

```javascript
// Using Google Trends & YouTube Search
seed_keyword = "your niche"
related = get_related_queries(seed_keyword)
search_volume = check_volume(related)
competition = analyze_competition(related)
best_keywords = rank_by_opportunity(related)
```

## 🤖 Free AI Tools Integration

### Script Writing (Choose one)

**Option 1: Google Gemini (Free)**
```javascript
// n8n HTTP Request
POST https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent
{
  "contents": [{
    "parts": [{
      "text": "Write a 1800-word YouTube script about [topic] for a 10-12 minute video..."
    }]
  }]
}
```

**Option 2: Hugging Face (Free)**
```javascript
// Using GPT-2 or similar free models
POST https://api-inference.huggingface.co/models/gpt2
{
  "inputs": "Create a detailed YouTube script about [topic]...",
  "parameters": {
    "max_length": 2000
  }
}
```

### Voiceover Generation (Choose one)

**Option 1: ElevenLabs (Free 10k chars/month)**
```javascript
POST https://api.elevenlabs.io/v1/text-to-speech/[voice_id]
{
  "text": "[your script]",
  "model_id": "eleven_monolingual_v1"
}
```

**Option 2: Edge TTS (FREE - No Billing Required)**
```bash
# Install
pip3 install edge-tts

# Generate voiceover (completely free, no API key)
edge-tts --voice en-US-GuyNeural --text "[your script]" --write-media voiceover.mp3

# Available voices: en-US-GuyNeural, en-US-JennyNeural, en-US-AriaNeural, etc.
```

**Option 3: Google Text-to-Speech (Requires Billing)**
⚠️ **Note:** Requires credit card even for free tier
```javascript
POST https://texttospeech.googleapis.com/v1/text:synthesize
{
  "input": {"text": "[your script]"},
  "voice": {"languageCode": "en-US", "name": "en-US-Neural2-J"},
  "audioConfig": {"audioEncoding": "MP3"}
}
```

### Video Assembly (Free Tools)

**FFmpeg Commands**:

```bash
# Combine voiceover with stock footage
ffmpeg -i footage.mp4 -i voiceover.mp3 -c:v copy -c:a aac -shortest output.mp4

# Add text overlay
ffmpeg -i input.mp4 -vf "drawtext=text='Your Title':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=50" output.mp4

# Concatenate multiple clips
ffmpeg -f concat -i filelist.txt -c copy output.mp4

# Add background music
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "[1:a]volume=0.2[a1];[0:a][a1]amix=inputs=2[a]" -map 0:v -map "[a]" output.mp4
```

## 📊 Content Calendar

The system automatically manages a content calendar:

```
Week 1:
├── Mon: [Auto-discovered topic 1]
├── Tue: [Auto-discovered topic 2]
├── Thu: [Auto-discovered topic 3]
├── Fri: [Auto-discovered topic 4]
└── Sat: [Auto-discovered topic 5]

Week 2:
├── Mon: [Auto-discovered topic 6]
├── Tue: [Auto-discovered topic 7]
... and so on
```

## 🎯 Video Quality Targets

### Technical Specifications
- **Resolution**: 1920x1080 (1080p)
- **Frame Rate**: 30 fps
- **Bitrate**: 8-12 Mbps
- **Audio**: 128 kbps AAC
- **Duration**: 600-720 seconds (10-12 min)
- **File Size**: ~800MB - 1.2GB

### Content Quality
- Clear audio (no background noise)
- Engaging visuals (change every 3-5 seconds)
- Professional transitions
- Consistent branding
- Proper pacing (not too fast/slow)

## 🔧 n8n Workflow Nodes

### Complete Node Structure

```
1. Cron Node (5x weekly trigger)
2. Content Discovery Node
3. Topic Research Node (HTTP Request)
4. Script Generation Node (HTTP Request - Gemini API)
5. Script Validation Node (Function)
6. Voiceover Generation Node (HTTP Request - ElevenLabs)
7. Visual Content Collection Node (HTTP Request - Pexels)
8. Video Assembly Node (Execute Command - FFmpeg)
9. Quality Check Node (Function)
10. Thumbnail Generation Node (Python)
11. SEO Optimization Node (HTTP Request - Gemini API)
12. YouTube Upload Node (YouTube API)
13. Notification Node (Email/Slack)
14. Archive Node (Move Files)
```

## 🚨 Troubleshooting

### Video Generation Fails

**Problem**: FFmpeg errors
```bash
# Check FFmpeg installation
ffmpeg -version

# Test basic conversion
ffmpeg -i test.mp4 -c copy test_output.mp4
```

**Problem**: Out of memory
- Reduce video resolution
- Process in smaller chunks
- Increase swap space

### API Rate Limits

- **YouTube**: 10,000 units/day (each upload = ~1600 units)
- **Gemini**: 60 requests/minute (free tier)
- **ElevenLabs**: 10,000 characters/month (free tier)
- **Pexels**: 200 requests/hour (free tier)

**Solution**: Implement retry logic with exponential backoff

### Audio Sync Issues

```bash
# Fix audio sync
ffmpeg -i input.mp4 -itsoffset 0.5 -i input.mp4 -map 0:v -map 1:a -c copy output.mp4
```

## 📈 Performance Optimization

### Batch Processing
- Generate multiple scripts at once
- Download stock footage in bulk
- Pre-generate thumbnails
- Queue uploads

### Caching
- Cache API responses
- Store frequently used assets
- Reuse video segments
- Keep template files

### Parallel Processing
```javascript
// Process multiple videos simultaneously
parallel_tasks = [
  generate_voiceover(script1),
  generate_voiceover(script2),
  download_footage(topic1),
  download_footage(topic2)
]
await Promise.all(parallel_tasks)
```

## 📚 Free Learning Resources

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [n8n Community Workflows](https://n8n.io/workflows)
- [YouTube Creator Academy](https://creatoracademy.youtube.com/)
- [Remotion Docs](https://www.remotion.dev/)
- [Video Editing Basics](https://www.youtube.com/watch?v=videoid)

## ⚡ Quick Tips

1. **Test locally first** before automating uploads
2. **Monitor API quotas** to avoid interruptions
3. **Keep backups** of generated content
4. **Review first 5 videos** manually before full automation
5. **A/B test** different thumbnail styles
6. **Track analytics** to optimize content
7. **Engage with comments** (can be semi-automated)

## 🎓 Best Practices

### Content Strategy
- Focus on one niche
- Maintain consistent style
- Follow content calendar
- Monitor trends regularly
- Analyze competitor success

### Technical
- Version control workflows
- Log all operations
- Implement error handling
- Set up monitoring alerts
- Regular backup system

### SEO
- Research keywords weekly
- Optimize for suggested videos
- Use cards and end screens
- Create playlists automatically
- Cross-promote content

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Important Disclaimers

1. **Content Quality**: Always review first few videos manually
2. **Copyright**: Ensure all content is original or properly licensed
3. **YouTube TOS**: Follow all YouTube policies and guidelines
4. **API Limits**: Respect rate limits of all services
5. **Authenticity**: Disclose use of AI if required by platform

## 🆘 Support

- **GitHub Issues**: Report bugs and request features
- **n8n Community**: Get workflow help
- **Documentation**: Check this README first
- **Examples**: See `/examples` folder for sample workflows

---

**Start automating your YouTube success today! 🚀📹**

*This system handles everything from finding content to uploading videos 5 times per week automatically!*
