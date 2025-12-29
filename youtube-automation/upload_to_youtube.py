#!/usr/bin/env python3
"""
YouTube Video Uploader for n8n Automation
Uploads videos to YouTube with metadata using YouTube Data API v3
"""

import os
import sys
import json
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service(credentials_path='credentials.json', token_path='token.pickle'):
    """
    Authenticate and return YouTube API service
    
    Args:
        credentials_path: Path to OAuth2 credentials JSON file
        token_path: Path to store/retrieve authentication token
    
    Returns:
        YouTube API service object
    """
    creds = None
    
    # Load existing token
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                print(json.dumps({
                    'error': f'Credentials file not found: {credentials_path}',
                    'status': 'failed'
                }))
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, video_file, title, description, tags=None, category_id='22', 
                 privacy_status='public', thumbnail_file=None):
    """
    Upload video to YouTube
    
    Args:
        youtube: Authenticated YouTube API service
        video_file: Path to video file
        title: Video title (max 100 chars)
        description: Video description (max 5000 chars)
        tags: List of tags (optional)
        category_id: YouTube category ID (default: 22 = People & Blogs)
        privacy_status: 'public', 'private', or 'unlisted'
        thumbnail_file: Path to thumbnail image (optional)
    
    Returns:
        dict with video_id, url, and status
    """
    if not os.path.exists(video_file):
        return {
            'error': f'Video file not found: {video_file}',
            'status': 'failed'
        }
    
    # Prepare video metadata
    body = {
        'snippet': {
            'title': title[:100],  # Max 100 chars
            'description': description[:5000],  # Max 5000 chars
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status,
            'selfDeclaredMadeForKids': False
        }
    }
    
    if tags:
        # Tags can be string (comma-separated) or list
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',')]
        body['snippet']['tags'] = tags[:500]  # Max 500 tags
    
    # Upload video
    try:
        media = MediaFileUpload(
            video_file,
            chunksize=1024*1024,  # 1MB chunks
            resumable=True
        )
        
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f'Upload progress: {progress}%', file=sys.stderr)
        
        video_id = response['id']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        # Upload thumbnail if provided
        if thumbnail_file and os.path.exists(thumbnail_file):
            try:
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(thumbnail_file)
                ).execute()
                print(f'Thumbnail uploaded successfully', file=sys.stderr)
            except HttpError as e:
                print(f'Warning: Thumbnail upload failed: {e}', file=sys.stderr)
        
        return {
            'video_id': video_id,
            'url': video_url,
            'title': title,
            'status': 'success',
            'privacy_status': privacy_status
        }
    
    except HttpError as e:
        error_content = e.content.decode('utf-8') if e.content else str(e)
        return {
            'error': f'YouTube API error: {error_content}',
            'status': 'failed',
            'error_code': e.resp.status
        }
    except Exception as e:
        return {
            'error': f'Upload failed: {str(e)}',
            'status': 'failed'
        }

def main():
    """Main function for command-line usage"""
    
    # Parse command-line arguments or read from stdin
    if len(sys.argv) > 1:
        # Command-line mode
        import argparse
        parser = argparse.ArgumentParser(description='Upload video to YouTube')
        parser.add_argument('video_file', help='Path to video file')
        parser.add_argument('--title', required=True, help='Video title')
        parser.add_argument('--description', required=True, help='Video description')
        parser.add_argument('--tags', help='Comma-separated tags')
        parser.add_argument('--category', default='22', help='Category ID (default: 22)')
        parser.add_argument('--privacy', default='public', 
                          choices=['public', 'private', 'unlisted'],
                          help='Privacy status')
        parser.add_argument('--thumbnail', help='Path to thumbnail file')
        parser.add_argument('--credentials', default='credentials.json',
                          help='Path to OAuth credentials')
        parser.add_argument('--token', default='token.pickle',
                          help='Path to token file')
        
        args = parser.parse_args()
        
        video_file = args.video_file
        title = args.title
        description = args.description
        tags = args.tags
        category_id = args.category
        privacy_status = args.privacy
        thumbnail_file = args.thumbnail
        credentials_path = args.credentials
        token_path = args.token
    else:
        # JSON input mode (for n8n)
        try:
            input_data = json.loads(sys.stdin.read())
            video_file = input_data.get('video_file')
            title = input_data.get('title', 'Untitled Video')
            description = input_data.get('description', '')
            tags = input_data.get('tags')
            category_id = input_data.get('category_id', '22')
            privacy_status = input_data.get('privacy_status', 'public')
            thumbnail_file = input_data.get('thumbnail_file')
            credentials_path = input_data.get('credentials_path', 'credentials.json')
            token_path = input_data.get('token_path', 'token.pickle')
        except json.JSONDecodeError as e:
            print(json.dumps({
                'error': f'Invalid JSON input: {e}',
                'status': 'failed'
            }))
            sys.exit(1)
        except Exception as e:
            print(json.dumps({
                'error': f'Error reading input: {e}',
                'status': 'failed'
            }))
            sys.exit(1)
    
    # Authenticate and upload
    try:
        youtube = get_authenticated_service(credentials_path, token_path)
        result = upload_video(
            youtube, video_file, title, description, tags,
            category_id, privacy_status, thumbnail_file
        )
        
        # Output result as JSON for n8n
        print(json.dumps(result, indent=2))
        
        # Exit with error code if upload failed
        if result.get('status') == 'failed':
            sys.exit(1)
    
    except Exception as e:
        print(json.dumps({
            'error': f'Unexpected error: {str(e)}',
            'status': 'failed'
        }))
        sys.exit(1)

if __name__ == '__main__':
    main()
