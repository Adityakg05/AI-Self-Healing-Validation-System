# Troubleshooting Guide

## Common Issues and Solutions

### 1. FastAPI Backend Not Running

**Problem:** "FastAPI app is not running" error in Streamlit UI

**Solutions:**
- Wait 2-3 minutes for backend to wake up (Render free tier limitation)
- Check backend health: `https://ai-self-healing-validation-system.onrender.com/health`
- If backend is down, it will auto-restart with built-in self-ping mechanism

### 2. Self-Healing Workflow Not Working

**Problem:** "No logs found" or workflow execution fails

**Solutions:**
- Trigger a crash first using "🔥 Trigger System Crash" button
- Check if logs are being generated: `https://ai-self-healing-validation-system.onrender.com/api/logs`
- Verify GROQ_API_KEY is set in Render dashboard environment variables

### 3. Deployment Issues

**Problem:** Services fail to deploy on Render

**Solutions:**
- Check Dockerfile syntax
- Verify all required files are committed to Git
- Ensure environment variables are properly set
- Check Render logs for specific error messages

### 4. Environment Variable Issues

**Problem:** API keys not working or validation errors

**Solutions:**
- Ensure GROQ_API_KEY is set in Render dashboard (not in code)
- Check that LLM_PROVIDER is set to "groq"
- Verify GITHUB_TOKEN has proper scopes (repo, workflow)

### 5. Memory/Performance Issues

**Problem:** Service runs slowly or crashes

**Solutions:**
- Render free tier has limited resources (512MB RAM)
- Consider upgrading to paid plan for better performance
- Monitor logs for memory usage patterns

### 6. Git Push Issues

**Problem:** Changes not reflecting in deployed application

**Solutions:**
- Ensure all changes are committed and pushed to main/master branch
- Wait for Render auto-deploy to complete (2-3 minutes)
- Check Render dashboard for deployment status

### 7. UI Connection Issues

**Problem:** Streamlit UI cannot connect to backend

**Solutions:**
- Verify BACKEND_URL is correctly set in render.yaml
- Check if backend service is running
- Ensure both services are in same region (Ohio/Oregon)

### 8. Log File Issues

**Problem:** Logs not being written or accessible

**Solutions:**
- Check LOG_FILE environment variable
- Verify file permissions in container
- Use /api/logs endpoint to access logs remotely

### 9. GitHub Integration Issues

**Problem:** Pull requests not being created

**Solutions:**
- Verify GITHUB_TOKEN is valid and has proper permissions
- Check GITHUB_REPO environment variable
- Ensure repository exists and is accessible

### 10. Self-Healing Agent Errors

**Problem:** Agent fails to analyze or fix issues

**Solutions:**
- Check LLM API key validity
- Verify internet connectivity
- Review agent logs for specific error messages
- Ensure proper error logging is enabled

## Debugging Steps

### 1. Check Service Status
```bash
# Backend health
curl https://ai-self-healing-validation-system.onrender.com/health

# Frontend health
curl https://ai-self-healing-validation-system-ui.onrender.com/_stcore/health
```

### 2. Check Logs
```bash
# Backend logs
curl https://ai-self-healing-validation-system.onrender.com/api/logs
```

### 3. Test API Endpoints
```bash
# Test basic connectivity
curl https://ai-self-healing-validation-system.onrender.com/test

# Trigger bug
curl -H "X-Trigger-Bug: true" https://ai-self-healing-validation-system.onrender.com/api/data
```

### 4. Monitor Render Dashboard
- Check service logs
- Verify environment variables
- Monitor resource usage
- Check deployment status

## Performance Optimization

### 1. Reduce Cold Start Time
- Keep service warm with regular requests
- Consider paid plan for better performance
- Optimize Docker image size

### 2. Memory Management
- Monitor memory usage
- Clean up temporary files
- Optimize logging levels

### 3. Network Optimization
- Use efficient HTTP clients
- Implement proper timeout handling
- Cache frequently accessed data

## Security Considerations

### 1. API Key Management
- Never commit API keys to repository
- Use environment variables
- Rotate keys regularly

### 2. Input Validation
- Validate all user inputs
- Sanitize data before processing
- Implement rate limiting

### 3. Error Handling
- Don't expose sensitive information
- Log errors securely
- Implement proper error responses

## Contact Support

If issues persist:
1. Check Render status page
2. Review GitHub issues
3. Check documentation
4. Contact Render support for platform issues
5. Create GitHub issue for code-related problems

## Maintenance

### Regular Tasks
- Monitor service health
- Update dependencies
- Review logs for errors
- Backup important data
- Test self-healing workflow

### Updates
- Keep dependencies current
- Test updates in staging
- Monitor for breaking changes
- Update documentation

### Monitoring
- Set up health checks
- Monitor resource usage
- Track error rates
- Set up alerts for critical issues
