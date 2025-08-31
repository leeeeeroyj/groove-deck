"""
YouTube service for searching and extracting audio URLs using yt-dlp.
"""
import logging
from typing import Optional, List, Dict
import yt_dlp

logger = logging.getLogger(__name__)

class YouTubeService:
    """Service for YouTube operations using yt-dlp."""
    
    def __init__(self):
        # Configure yt-dlp options for audio extraction
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        
    def search_video(self, query: str) -> Optional[Dict]:
        """
        Search for a video on YouTube and return metadata.
        
        Args:
            query: Search query (song name, artist, or URL)
            
        Returns:
            Dictionary with video metadata or None if not found
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Try to extract info from the query
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                
                if info and 'entries' in info and info['entries']:
                    video_info = info['entries'][0]
                    return {
                        'title': video_info.get('title', 'Unknown Title'),
                        'url': video_info.get('webpage_url', ''),
                        'duration': video_info.get('duration'),
                        'thumbnail': video_info.get('thumbnail', ''),
                        'uploader': video_info.get('uploader', 'Unknown'),
                        'view_count': video_info.get('view_count', 0)
                    }
                    
        except Exception as e:
            logger.error(f"Error searching for video '{query}': {e}")
            return None
            
        return None
        
    def get_audio_url(self, video_url: str) -> Optional[str]:
        """
        Extract the direct audio URL from a YouTube video URL.
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Direct audio URL or None if extraction fails
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
                if info and 'url' in info:
                    return info['url']
                    
        except Exception as e:
            logger.error(f"Error extracting audio URL from '{video_url}': {e}")
            return None
            
        return None
        
    def validate_url(self, url: str) -> bool:
        """
        Check if a URL is a valid YouTube URL.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid YouTube URL, False otherwise
        """
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com']
        return any(domain in url.lower() for domain in youtube_domains)

# Global YouTube service instance
youtube_service = YouTubeService()
