# CI/CD Pipeline Setup Guide

## Overview
This repository uses GitHub Actions for CI/CD with two main workflows:
- **CI (ci.yml)**: Code quality checks on all pushes and PRs
- **CD (deploy.yml)**: Automatic deployment to AWS Elastic Beanstalk on `main` branch

## GitHub Repository Setup

### 1. Required GitHub Secrets
Navigate to your repository → Settings → Secrets and variables → Actions

Add the following **Repository Secrets**:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | AWS IAM user access key with EB permissions | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM user secret key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |

### 2. GitHub Environment (Optional but Recommended)
For additional security, create a **production** environment:

1. Go to Settings → Environments
2. Click "New environment" 
3. Name it: `production`
4. Configure protection rules:
   - ✅ Required reviewers (add team members)
   - ✅ Wait timer: 5 minutes (optional)
   - ✅ Deployment branches: `main` only

## AWS IAM Setup

### Create IAM User for GitHub Actions

1. **Create IAM User**:
   ```bash
   aws iam create-user --user-name github-actions-fabman-deploy
   ```

2. **Create IAM Policy** with minimum required permissions:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "elasticbeanstalk:*",
           "s3:GetObject",
           "s3:GetObjectVersion",
           "s3:PutObject",
           "s3:DeleteObject",
           "s3:ListBucket",
           "autoscaling:*",
           "ec2:*",
           "ecs:*",
           "elasticloadbalancing:*",
           "iam:ListRoles",
           "iam:PassRole",
           "logs:*",
           "cloudformation:*"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

3. **Attach Policy and Create Access Keys**:
   ```bash
   # Create and attach policy
   aws iam put-user-policy --user-name github-actions-fabman-deploy \
     --policy-name EBDeployPolicy --policy-document file://policy.json
   
   # Create access keys
   aws iam create-access-key --user-name github-actions-fabman-deploy
   ```

## Workflow Details

### CI Pipeline (ci.yml)
**Triggers**: Push/PR to `main` or `develop` branches

**Steps**:
1. ✅ Code checkout
2. ✅ Python 3.9 setup with dependency caching
3. ✅ Black formatting check
4. ✅ isort import sorting check  
5. ✅ Flake8 linting
6. ✅ Requirements validation

### CD Pipeline (deploy.yml) 
**Triggers**: Push to `main` branch or manual dispatch

**Steps**:
1. ✅ Code checkout and dependency installation
2. ✅ Basic smoke test
3. ✅ Create deployment package (excludes dev files)
4. ✅ Deploy to Elastic Beanstalk with version labeling
5. ✅ Wait for deployment completion
6. ✅ Cleanup temporary files

## Branch Strategy

- **`main`**: Production branch - triggers automatic deployment
- **`develop`**: Development branch - runs CI only
- **Feature branches**: Run CI on PRs to `main`/`develop`

## Deployment Package
The CD pipeline automatically excludes:
- Git files (`.git*`)
- Python cache (`__pycache__`, `*.pyc`)
- Environment files (`.env`)
- Development dependencies (`requirements-dev.txt`)
- GitHub workflows (`.github/`)
- Documentation (`README.md`)

## Monitoring and Troubleshooting

### GitHub Actions Logs
- View workflow runs: Repository → Actions
- Check individual job logs for detailed error information

### Elastic Beanstalk Logs
- AWS Console → Elastic Beanstalk → Environment → Logs
- Or via CLI: `eb logs`

### Common Issues
1. **AWS Permission Errors**: Verify IAM user has required permissions
2. **Deployment Timeout**: Check EB environment health and scaling settings
3. **Import Errors**: Ensure all dependencies in `requirements.txt` are production-ready

## Manual Deployment
To deploy manually (bypass CI):
```bash
# From repository root
gh workflow run deploy.yml
```

## Rollback Strategy
If deployment fails:
1. AWS Console → Elastic Beanstalk → Application Versions
2. Select previous working version → Deploy

Or via EB CLI:
```bash
eb deploy --version=previous-version-label
```