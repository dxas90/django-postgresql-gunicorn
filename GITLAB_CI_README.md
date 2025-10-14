# GitLab CI/CD Pipeline Documentation

## Overview

This GitLab CI/CD pipeline automates the build, test, containerization, and deployment process for the Django PostgreSQL Gunicorn application.

## Pipeline Stages

The pipeline consists of 7 stages:

1. **initialize** - Install dependencies and prepare environment
2. **build** - Build the Django application (collect static files)
3. **test** - Run Django tests
4. **containerize** - Build and push Docker images (tags only)
5. **deployment** - Deploy to staging environment (tags only)
6. **promote** - Promote image to production (manual, tags only)
7. **notify** - Send notifications about pipeline status

## Pipeline Behavior

### For All Commits (Any Branch)
The following stages will **always** run on every commit to any branch:
- `initialize` - Install Python dependencies
- `build` - Collect static files
- `test` - Run Django tests
- `notify` - Send success/failure notifications

### For Tagged Commits Only
The following stages run **only** when a commit is tagged:
- `containerize` - Build Docker image and push to registry
- `deployment` - Deploy to staging environment
- `promote` - Manual job to promote to production

## Jobs Description

### initialize
- **Stage**: initialize
- **Runs**: Always
- **Purpose**: Install Python dependencies
- **Artifacts**: Creates `venv/` directory (expires in 1 hour)

### build
- **Stage**: build
- **Runs**: Always
- **Purpose**: Collect Django static files
- **Dependencies**: Requires `initialize` job
- **Artifacts**: Creates `static/` directory (expires in 1 hour)

### test
- **Stage**: test
- **Runs**: Always
- **Purpose**: Run Django test suite
- **Dependencies**: Requires `initialize` job

### containerize
- **Stage**: containerize
- **Runs**: Only on tags
- **Purpose**: Build Docker image and push to registry
- **Images Created**:
  - `$CI_REGISTRY_IMAGE:$CI_COMMIT_TAG` - Tagged version
  - `$CI_REGISTRY_IMAGE:latest` - Latest version

### deploy_staging
- **Stage**: deployment
- **Runs**: Only on tags
- **Purpose**: Deploy application to staging environment
- **Dependencies**: Requires `containerize` job
- **Environment**: staging

### promote_production
- **Stage**: promote
- **Runs**: Only on tags (manual trigger required)
- **Purpose**: Promote Docker image to production
- **When**: Manual
- **Environment**: production
- **Action**: Tags image as `production` and pushes to registry

### notify_success / notify_failure
- **Stage**: notify
- **Runs**: Always (based on pipeline status)
- **Purpose**: Send notifications about build status
- **Note**: Configure webhook URLs or notification services as needed

## Required GitLab CI/CD Variables

To use this pipeline, configure the following variables in GitLab:

### Required Variables (Auto-provided by GitLab)
- `CI_REGISTRY` - GitLab Container Registry URL
- `CI_REGISTRY_USER` - Registry username
- `CI_REGISTRY_PASSWORD` - Registry password
- `CI_REGISTRY_IMAGE` - Full image path
- `CI_COMMIT_TAG` - Git tag name

### Optional Variables for Notifications
- `SLACK_WEBHOOK` - Slack webhook URL for notifications
- `TEAMS_WEBHOOK` - Microsoft Teams webhook URL
- Any other notification service webhooks

## Usage Examples

### Regular Development Workflow
```bash
# Make changes and commit to any branch
git add .
git commit -m "Add new feature"
git push origin feature-branch

# Pipeline will run: initialize → build → test → notify
```

### Release Workflow
```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Pipeline will run: 
# initialize → build → test → containerize → deployment (staging) → notify
# Then manually trigger: promote (to production)
```

### Manual Production Promotion
1. Go to GitLab CI/CD → Pipelines
2. Find the pipeline for your tag
3. Click on the `promote_production` job
4. Click "Play" to manually trigger production deployment

## Customization

### Deployment Configuration
Edit the `deploy_staging` and `promote_production` jobs to add your specific deployment commands:

- For Kubernetes: Use `kubectl` commands
- For Docker Compose: Use `docker-compose` commands
- For other platforms: Add appropriate deployment scripts

### Notification Configuration
Edit the `notify_success` and `notify_failure` jobs to configure your notification system:

```yaml
script:
  - curl -X POST -H 'Content-type: application/json' 
    --data '{"text":"Build Success"}' $SLACK_WEBHOOK
```

### Environment URLs
Update the environment URLs in the deployment jobs:

```yaml
environment:
  name: staging
  url: https://your-staging-url.com
```

## Pipeline Visualization

```
┌─────────────┐
│  COMMIT     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ initialize  │ (always)
└─────┬───────┘
      │
      ▼
┌─────────────┐
│   build     │ (always)
└─────┬───────┘
      │
      ▼
┌─────────────┐
│    test     │ (always)
└─────┬───────┘
      │
      ▼
   Is Tag?
      │
  Yes │ No
      │  │
      │  └──────────┐
      ▼             ▼
┌─────────────┐  ┌──────────────┐
│containerize │  │   notify     │ (always)
└─────┬───────┘  └──────────────┘
      │
      ▼
┌─────────────┐
│ deployment  │ (staging)
└─────┬───────┘
      │
      ▼
┌─────────────┐
│  promote    │ (manual, production)
└─────┬───────┘
      │
      ▼
┌─────────────┐
│   notify    │ (always)
└─────────────┘
```

## Troubleshooting

### Pipeline fails at initialize stage
- Check that `requirements.txt` is valid
- Verify Python version compatibility

### Pipeline fails at build stage
- Check Django settings for static files configuration
- Ensure `STATIC_ROOT` is properly configured

### Pipeline fails at test stage
- Review test output in job logs
- Ensure test database configuration is correct

### Docker image build fails
- Check Dockerfile syntax
- Verify all required files are present
- Check Docker registry credentials

### Deployment fails
- Verify deployment credentials
- Check target environment accessibility
- Review deployment scripts

## Security Best Practices

1. **Never commit secrets** - Use GitLab CI/CD variables for sensitive data
2. **Use protected tags** - Restrict who can create tags in repository settings
3. **Protected environments** - Configure production environment as protected
4. **Registry access** - Use appropriate access controls for container registry
5. **Review manual jobs** - Require approvals for production promotions

## Additional Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
