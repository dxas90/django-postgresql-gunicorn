# GitLab CI/CD Quick Reference

## Pipeline Execution Flow

### Regular Commits (Any Branch)
```
Commit → Push
    ↓
┌─────────────┐
│ initialize  │  Install Python dependencies
└─────┬───────┘
      ↓
┌─────────────┐
│   build     │  Collect Django static files
└─────┬───────┘
      ↓
┌─────────────┐
│    test     │  Run Django test suite
└─────┬───────┘
      ↓
┌─────────────┐
│   notify    │  Send build status notification
└─────────────┘
```

### Tagged Commits (Release)
```
Tag → Push
    ↓
┌─────────────┐
│ initialize  │  Install Python dependencies
└─────┬───────┘
      ↓
┌─────────────┐
│   build     │  Collect Django static files
└─────┬───────┘
      ↓
┌─────────────┐
│    test     │  Run Django test suite
└─────┬───────┘
      ↓
┌─────────────┐
│containerize │  Build & push Docker image (tag + latest)
└─────┬───────┘
      ↓
┌─────────────┐
│deploy_staging│ Deploy to staging environment
└─────┬───────┘
      ↓
┌─────────────┐
│   promote   │  [MANUAL] Promote to production
└─────┬───────┘
      ↓
┌─────────────┐
│   notify    │  Send build status notification
└─────────────┘
```

## Common Commands

### Development Workflow
```bash
# Make changes
git add .
git commit -m "Add new feature"
git push origin feature-branch

# Pipeline runs: initialize → build → test → notify
```

### Release Workflow
```bash
# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Pipeline runs all stages including containerize and deploy_staging
# Then manually click "Play" on promote_production in GitLab UI
```

### Hotfix Workflow
```bash
# Create hotfix tag
git tag -a v1.0.1 -m "Hotfix: Critical bug fix"
git push origin v1.0.1

# Review staging deployment, then manually promote to production
```

## Job Details

| Job | Stage | When | Purpose |
|-----|-------|------|---------|
| initialize | initialize | Always | Install dependencies, create venv |
| build | build | Always | Collect static files |
| test | test | Always | Run Django tests |
| containerize | containerize | Tags only | Build & push Docker images |
| deploy_staging | deployment | Tags only | Deploy to staging |
| promote_production | promote | Manual (tags only) | Promote to production |
| notify_success | notify | On success | Notify build success |
| notify_failure | notify | On failure | Notify build failure |

## Docker Images Created

When a tag is pushed, the following images are created:
- `$CI_REGISTRY_IMAGE:$CI_COMMIT_TAG` (e.g., `registry.example.com/app:v1.0.0`)
- `$CI_REGISTRY_IMAGE:latest` (e.g., `registry.example.com/app:latest`)

When promoted to production:
- `$CI_REGISTRY_IMAGE:production` (e.g., `registry.example.com/app:production`)

## Environment Variables

### Auto-configured by GitLab
- `CI_REGISTRY` - Container registry URL
- `CI_REGISTRY_USER` - Registry username  
- `CI_REGISTRY_PASSWORD` - Registry password
- `CI_REGISTRY_IMAGE` - Full image path
- `CI_COMMIT_TAG` - Git tag name
- `CI_COMMIT_REF_NAME` - Branch/tag name
- `CI_COMMIT_SHORT_SHA` - Short commit SHA

### Optional (configure in GitLab)
- `SLACK_WEBHOOK` - Slack webhook for notifications
- `TEAMS_WEBHOOK` - Teams webhook for notifications

## Customization Points

### Add Deployment Commands
Edit `deploy_staging` job in `.gitlab-ci.yml`:
```yaml
script:
  - kubectl set image deployment/myapp myapp=$DOCKER_IMAGE
  # or
  - docker-compose -f docker-compose.staging.yml up -d
```

### Add Notifications
Edit `notify_success` and `notify_failure` jobs:
```yaml
script:
  - curl -X POST $SLACK_WEBHOOK -d '{"text":"Build Success"}'
```

### Customize Environment URLs
```yaml
environment:
  name: staging
  url: https://your-staging-url.com
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pipeline fails at initialize | Check requirements.txt is valid |
| Build fails | Verify Django settings for STATIC_ROOT |
| Tests fail | Check database configuration in tests |
| Docker build fails | Verify Dockerfile and registry credentials |
| Deployment fails | Check deployment scripts and credentials |

## Security Notes

1. Never commit secrets - use GitLab CI/CD variables
2. Use protected tags for releases
3. Configure production as a protected environment
4. Require manual approval for production deployments
5. Review staging deployment before promoting to production

## Further Reading

- Full documentation: [GITLAB_CI_README.md](GITLAB_CI_README.md)
- GitLab CI/CD docs: https://docs.gitlab.com/ee/ci/
- Django deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
