# API Documentation

## FastAPI Backend Endpoints

### Base URL
```
https://ai-self-healing-validation-system.onrender.com
```

### Authentication
No authentication required for demo endpoints.

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-05-07T22:57:00.000Z",
  "service": "AI-Self-Healing-Validation-System",
  "version": "1.0.0",
  "uptime": "active"
}
```

#### 2. Ping
```http
GET /ping
```

**Response:**
```json
{
  "message": "pong",
  "timestamp": "2026-05-07T22:57:00.000Z"
}
```

#### 3. Test
```http
GET /test
```

**Response:**
```json
{
  "status": "working"
}
```

#### 4. Get Data (with intentional bug)
```http
GET /api/data
Headers:
  X-Trigger-Bug: true  # Optional - triggers the bug
```

**Normal Response:**
```json
{
  "data": {
    "user_id": 12345,
    "username": "demo_user",
    "roles": ["admin", "developer"]
  },
  "message": "Success",
  "timestamp": "2026-05-07T22:57:00.000Z"
}
```

**Bug Triggered Response:**
```json
{
  "error": "Internal Server Error"
}
```
Status: 500

#### 5. Trigger Self-Healing Agent
```http
POST /run-agent
```

**Response:**
```json
{
  "status": "completed",
  "message": "Self-healing process executed successfully",
  "details": {
    "root_cause_found": true,
    "fix_validated": true,
    "iterations": 2,
    "pr_url": "https://github.com/your-repo/pull/123"
  }
}
```

#### 6. Get Logs
```http
GET /api/logs
```

**Response:**
```json
{
  "logs": "2026-05-07 22:57:00 - INFO - Application started...",
  "status": "success"
}
```

#### 7. API Documentation
```http
GET /docs
```
Redirects to Swagger UI documentation.

#### 8. OpenAPI Schema
```http
GET /openapi.json
```
Returns the OpenAPI schema in JSON format.

### Error Responses

#### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["header", "x-trigger-bug"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Internal Server Error (500)
```json
{
  "error": "Internal Server Error"
}
```

### Rate Limits
No rate limiting implemented for demo purposes.

### CORS
CORS enabled for all origins in demo mode.

### WebSocket Support
No WebSocket endpoints implemented.

### File Upload Support
No file upload endpoints implemented.

### Database Integration
No database connections - uses file-based logging.

### Environment Variables
- `PORT`: Server port (default: 8000)
- `LOG_FILE`: Path to log file (default: /tmp/app_logs.txt)
- `PYTHONUNBUFFERED`: Set to 1 for proper logging

### Deployment Notes
- Self-ping mechanism runs every 10 minutes to keep service alive
- Uses Render free tier with automatic health checks
- Logs are written to /tmp/app_logs.txt

### Monitoring
- Health endpoint available for monitoring systems
- Self-healing agent can be triggered via API
- Logs accessible via /api/logs endpoint

### Security Considerations
- No authentication in demo mode
- All endpoints publicly accessible
- Intentional bug present for demonstration
- No input validation on some endpoints

### Performance
- Lightweight FastAPI application
- Minimal resource usage
- Suitable for demonstration purposes
