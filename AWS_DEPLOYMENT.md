# AWS Deployment Guide

This guide explains how to deploy the Face Recognition Project to AWS using the provided setup script.

## Prerequisites

Before running the setup script, ensure you have the following:

1. **AWS Account**: An active AWS account with appropriate permissions
2. **AWS CLI**: Installed and configured on your local machine
3. **Docker**: Installed and running
4. **IAM Permissions**: Your AWS user/role should have permissions for:
   - ECR (Elastic Container Registry)
   - ECS (Elastic Container Service)
   - IAM (for role creation)
   - EC2 (for VPC and security groups)
   - CloudWatch (for logging)

## Installation Steps

### 1. Install AWS CLI

If you haven't installed the AWS CLI yet:

```bash
# For Linux/macOS
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# For macOS using Homebrew
brew install awscli

# Verify installation
aws --version
```

### 2. Configure AWS Credentials

```bash
aws configure
```

You'll be prompted to enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Default output format (json recommended)

### 3. Set Environment Variables (Optional)

Create a configuration file from the template:

```bash
cp aws-config.env.example aws-config.env
```

Edit `aws-config.env` to customize your deployment settings:

```bash
# Load configuration
source aws-config.env
```

### 4. Run the Setup Script

Execute the AWS setup script:

```bash
./setup-aws.sh
```

The script will:
1. ✅ Verify AWS CLI installation
2. ✅ Check AWS credentials
3. ✅ Verify Docker installation
4. ✅ Create ECR repositories
5. ✅ Login to Amazon ECR
6. ✅ Build Docker images
7. ✅ Push images to ECR
8. ✅ Create ECS cluster
9. ✅ Create IAM roles
10. ✅ Set up network resources

## What Gets Created

### ECR Repositories
- `face-recognition-base`: Base Docker image with dependencies
- `face-recognition-app`: Standalone application image
- `face-recognition-web`: Web application image

### ECS Resources
- **Cluster**: `face-recognition-cluster`
- **Execution Role**: `face-recognition-ecs-task-execution-role`

### Network Resources
- Security group in default VPC
- Ingress rules for ports 80 and 443

## Manual Deployment Steps

After running the setup script, you may need to:

### 1. Create ECS Task Definitions

Create task definitions for your services. Example for the web service:

```json
{
  "family": "face-recognition-web",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/face-recognition-ecs-task-execution-role",
  "containerDefinitions": [
    {
      "name": "web",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/face-recognition-web:latest",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/face-recognition-web",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register the task definition:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### 2. Create ECS Service

```bash
aws ecs create-service \
  --cluster face-recognition-cluster \
  --service-name face-recognition-web-service \
  --task-definition face-recognition-web:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

### 3. Set Up Application Load Balancer (Optional)

For production deployments, consider setting up an ALB:

```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name face-recognition-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx

# Create target group
aws elbv2 create-target-group \
  --name face-recognition-targets \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-xxxxx \
  --target-type ip
```

## Updating Images

To update your application:

1. Build new Docker images:
```bash
docker build -t face-recognition-web:latest ./web
```

2. Tag and push to ECR:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker tag face-recognition-web:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/face-recognition-web:latest

docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/face-recognition-web:latest
```

3. Update ECS service:
```bash
aws ecs update-service \
  --cluster face-recognition-cluster \
  --service face-recognition-web-service \
  --force-new-deployment
```

## Monitoring and Logs

### View ECS Service Status

```bash
aws ecs describe-services \
  --cluster face-recognition-cluster \
  --services face-recognition-web-service
```

### View CloudWatch Logs

```bash
aws logs tail /ecs/face-recognition-web --follow
```

## Cost Optimization

- Use **Fargate Spot** for non-critical workloads (up to 70% savings)
- Set up **auto-scaling** based on CPU/memory utilization
- Enable **ECR lifecycle policies** to remove old images
- Use **CloudWatch Alarms** to monitor costs

## Cleanup

To remove all AWS resources:

```bash
# Delete ECS services
aws ecs delete-service --cluster face-recognition-cluster --service face-recognition-web-service --force

# Delete ECS cluster
aws ecs delete-cluster --cluster face-recognition-cluster

# Delete ECR repositories
aws ecr delete-repository --repository-name face-recognition-base --force
aws ecr delete-repository --repository-name face-recognition-app --force
aws ecr delete-repository --repository-name face-recognition-web --force

# Delete IAM role
aws iam detach-role-policy --role-name face-recognition-ecs-task-execution-role --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
aws iam delete-role --role-name face-recognition-ecs-task-execution-role

# Delete security group (get the SG ID first)
aws ec2 delete-security-group --group-id sg-xxxxx
```

## Troubleshooting

### Issue: "Unable to locate credentials"
**Solution**: Run `aws configure` to set up your credentials.

### Issue: "Access Denied" errors
**Solution**: Ensure your IAM user has the necessary permissions. You may need:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonECS_FullAccess`
- `IAMFullAccess` (or specific permissions for role creation)

### Issue: Docker images fail to push
**Solution**:
1. Ensure Docker is running
2. Re-authenticate to ECR: `aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com`

### Issue: ECS tasks fail to start
**Solution**:
1. Check CloudWatch logs for error messages
2. Verify task definition configuration
3. Ensure sufficient CPU/memory allocation
4. Check security group allows necessary traffic

## Additional Resources

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [AWS Fargate Pricing](https://aws.amazon.com/fargate/pricing/)
- [ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/intro.html)
