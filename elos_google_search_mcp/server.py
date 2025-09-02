"""Google Search MCP Server using FastMCP."""

import os
import logging
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.auth import default
from google.auth.exceptions import DefaultCredentialsError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Google Search MCP Server")

def get_google_credentials():
    """Get Google API credentials from environment or service account."""
    # Try to get credentials from environment variables first
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if credentials_path and os.path.exists(credentials_path):
        try:
            return service_account.Credentials.from_service_account_file(credentials_path)
        except Exception as e:
            logger.warning(f"Failed to load service account from {credentials_path}: {e}")
    
    # Try to get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        return api_key
    
    # Try default credentials
    try:
        credentials, project = default()
        return credentials
    except DefaultCredentialsError:
        logger.error("No Google credentials found. Please set GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_API_KEY")
        return None

@mcp.tool()
def google_search(query: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """
    Perform a Google search and return results.
    
    Args:
        query: The search query string
        num_results: Number of results to return (max 10)
    
    Returns:
        List of search results with title, link, and snippet
    """
    try:
        credentials = get_google_credentials()
        if not credentials:
            return {"error": "No Google credentials available"}
        
        # Use Custom Search API if available, otherwise fall back to basic search
        if isinstance(credentials, str):  # API key
            service = build("customsearch", "v1", developerKey=credentials)
            search_engine_id = os.getenv('GOOGLE_CSE_ID')
            if search_engine_id:
                # Use Custom Search API
                results = service.list(
                    q=query,
                    cx=search_engine_id,
                    num=min(num_results, 10)
                ).execute()
                
                items = results.get('items', [])
                return [
                    {
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': 'Google Custom Search'
                    }
                    for item in items
                ]
            else:
                return {"error": "GOOGLE_CSE_ID environment variable not set for Custom Search API"}
        else:
            # Use standard Google Search API (requires different setup)
            return {"error": "Service account authentication not yet implemented for search API"}
            
    except HttpError as e:
        logger.error(f"Google API error: {e}")
        return {"error": f"Google API error: {e}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": f"Unexpected error: {e}"}

@mcp.tool()
def google_search_web(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a web search using Google and return results.
    
    Args:
        query: The search query string
        num_results: Number of results to return (max 5)
    
    Returns:
        List of web search results
    """
    try:
        credentials = get_google_credentials()
        if not credentials:
            return {"error": "No Google credentials available"}
        
        if isinstance(credentials, str):  # API key
            service = build("customsearch", "v1", developerKey=credentials)
            search_engine_id = os.getenv('GOOGLE_CSE_ID')
            if search_engine_id:
                results = service.list(
                    q=query,
                    cx=search_engine_id,
                    num=min(num_results, 5),
                    searchType='web'
                ).execute()
                
                items = results.get('items', [])
                return [
                    {
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': 'Google Web Search'
                    }
                    for item in items
                ]
            else:
                return {"error": "GOOGLE_CSE_ID environment variable not set"}
        else:
            return {"error": "Service account authentication not yet implemented"}
            
    except HttpError as e:
        logger.error(f"Google API error: {e}")
        return {"error": f"Google API error: {e}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": f"Unexpected error: {e}"}

@mcp.tool()
def google_search_images(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for images using Google and return results.
    
    Args:
        query: The search query string
        num_results: Number of results to return (max 5)
    
    Returns:
        List of image search results
    """
    try:
        credentials = get_google_credentials()
        if not credentials:
            return {"error": "No Google credentials available"}
        
        if isinstance(credentials, str):  # API key
            service = build("customsearch", "v1", developerKey=credentials)
            search_engine_id = os.getenv('GOOGLE_CSE_ID')
            if search_engine_id:
                results = service.list(
                    q=query,
                    cx=search_engine_id,
                    num=min(num_results, 5),
                    searchType='image'
                ).execute()
                
                items = results.get('items', [])
                return [
                    {
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'image': item.get('image', {}),
                        'source': 'Google Image Search'
                    }
                    for item in items
                ]
            else:
                return {"error": "GOOGLE_CSE_ID environment variable not set"}
        else:
            return {"error": "Service account authentication not yet implemented"}
            
    except HttpError as e:
        logger.error(f"Google API error: {e}")
        return {"error": f"Google API error: {e}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": f"Unexpected error: {e}"}

@mcp.tool()
def get_search_health() -> Dict[str, Any]:
    """
    Check the health and configuration of the Google Search MCP server.
    
    Returns:
        Dictionary containing health status and configuration info
    """
    credentials = get_google_credentials()
    search_engine_id = os.getenv('GOOGLE_CSE_ID')
    
    return {
        "status": "healthy" if credentials else "unhealthy",
        "credentials_available": bool(credentials),
        "search_engine_id_set": bool(search_engine_id),
        "environment_variables": {
            "GOOGLE_APPLICATION_CREDENTIALS": os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
            "GOOGLE_API_KEY": "***" if os.getenv('GOOGLE_API_KEY') else None,
            "GOOGLE_CSE_ID": search_engine_id
        }
    }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport='sse', host='0.0.0.0', port=8000)
