# Elos Google Search MCP Server

A Model Context Protocol (MCP) server that provides Google Search capabilities using FastMCP and the Google Custom Search API.

## Features

- **Google Search**: Perform web searches using Google Custom Search API
- **Image Search**: Search for images using Google Image Search
- **Web Search**: Specialized web search functionality
- **Health Monitoring**: Built-in health checks and status monitoring
- **Flexible Authentication**: Support for API keys and service accounts
- **FastMCP Integration**: Built on the FastMCP framework for optimal performance

## Prerequisites

### Google API Setup

1. **Google Cloud Project**: Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. **Enable APIs**: Enable the following APIs:
   - Custom Search API
   - Custom Search Engine API
3. **Create Custom Search Engine**: 
   - Go to [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
   - Create a new search engine
   - Note the Search Engine ID (cx)
4. **API Key or Service Account**:
   - **Option A**: Create an API key in Google Cloud Console
   - **Option B**: Create a service account and download the JSON credentials

### Local Development Requirements

- Python 3.9+
- Docker/Podman
- Access to quay.io registry

## Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd elos-mcp-google-search
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Set environment variables**:
   ```bash
   export GOOGLE_API_KEY="your-api-key"
   export GOOGLE_CSE_ID="your-search-engine-id"
   # OR for service account:
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
   ```

4. **Run the server**:
   ```bash
   python -m elos_google_search_mcp.server
   ```

### Docker Build

1. **Build the image**:
   ```bash
   podman build -t elos-google-search-mcp:latest .
   ```

2. **Test locally**:
   ```bash
   podman run -p 8000:8000 \
     -e GOOGLE_API_KEY="your-api-key" \
     -e GOOGLE_CSE_ID="your-search-engine-id" \
     elos-google-search-mcp:latest
   ```

## Deployment

### Push to Quay.io

1. **Login to Quay.io**:
   ```bash
   podman login quay.io
   ```

2. **Tag the image**:
   ```bash
   podman tag elos-google-search-mcp:latest quay.io/elostech/elos-mcp-google-search:latest
   ```

3. **Push the image**:
   ```bash
   podman push quay.io/elostech/elos-mcp-google-search:latest
   ```

### Kubernetes Deployment

1. **Update the secret** with your actual credentials:
   ```bash
   # Edit kubernetes/elos-google-search-secret.yaml
   # Replace placeholder values with actual credentials
   ```

2. **Apply the configuration**:
   ```bash
   kubectl apply -k kubernetes/
   ```

3. **Verify deployment**:
   ```bash
   kubectl get pods -l app=elos-google-search-mcp
   kubectl get services -l app=elos-google-search-mcp
   ```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google API key for authentication | Yes (if using API key) |
| `GOOGLE_CSE_ID` | Custom Search Engine ID | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account JSON file | Yes (if using service account) |

### Kubernetes Secrets

The deployment uses Kubernetes secrets to store sensitive information:

- `google-api-key`: Your Google API key
- `google-cse-id`: Your Custom Search Engine ID
- `google-credentials`: Service account JSON (if using service account auth)

## API Endpoints

The MCP server provides the following tools:

### `google_search(query, num_results)`
Perform a general Google search.

**Parameters:**
- `query` (str): Search query string
- `num_results` (int): Number of results (max 10)

**Returns:** List of search results with title, link, and snippet

### `google_search_web(query, num_results)`
Perform a web-specific search.

**Parameters:**
- `query` (str): Search query string
- `num_results` (int): Number of results (max 5)

**Returns:** List of web search results

### `google_search_images(query, num_results)`
Search for images.

**Parameters:**
- `query` (str): Search query string
- `num_results` (int): Number of results (max 5)

**Returns:** List of image search results

### `get_search_health()`
Check server health and configuration.

**Returns:** Health status and configuration information

## Usage Examples

### Basic Search
```python
from elos_google_search_mcp.server import google_search

results = google_search("OpenAI GPT-4", num_results=5)
for result in results:
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
    print(f"Snippet: {result['snippet']}")
    print("---")
```

### Health Check
```python
from elos_google_search_mcp.server import get_search_health

health = get_search_health()
print(f"Status: {health['status']}")
print(f"Credentials Available: {health['credentials_available']}")
```

## Troubleshooting

### Common Issues

1. **"No Google credentials available"**
   - Ensure environment variables are set correctly
   - Check that API key or service account file is valid

2. **"GOOGLE_CSE_ID environment variable not set"**
   - Set the `GOOGLE_CSE_ID` environment variable
   - Verify the Custom Search Engine ID is correct

3. **API Quota Exceeded**
   - Check your Google Cloud Console for quota limits
   - Consider upgrading your API plan

4. **Authentication Errors**
   - Verify API key permissions
   - Check service account roles and permissions

### Debug Mode

Enable debug logging by setting the log level:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Development

### Project Structure
```
elos-mcp-google-search/
├── elos_google_search_mcp/
│   ├── __init__.py
│   └── server.py
├── kubernetes/
│   ├── elos-google-search-deployment.yaml
│   ├── elos-google-search-secret.yaml
│   └── kustomization.yaml
├── Containerfile
├── pyproject.toml
└── README.md
```

### Adding New Tools

To add new search tools, use the `@mcp.tool()` decorator:

```python
@mcp.tool()
def new_search_function(query: str) -> Dict[str, Any]:
    """Description of the new tool."""
    # Implementation here
    return {"result": "data"}
```

### Testing

Run tests locally:
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the Elos Tech team

## Changelog

### v0.1.0
- Initial release
- Google Search functionality
- Image search support
- Health monitoring
- Kubernetes deployment support
