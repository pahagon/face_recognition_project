#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
PROJECT_NAME="face-recognition"
ECR_REPOSITORY_BASE="${PROJECT_NAME}-base"
ECR_REPOSITORY_APP="${PROJECT_NAME}-app"
ECR_REPOSITORY_WEB="${PROJECT_NAME}-web"
ECS_CLUSTER_NAME="${PROJECT_NAME}-cluster"
AWS_ACCOUNT_ID=""

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if AWS CLI is installed
check_aws_cli() {
    print_info "Checking AWS CLI installation..."
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        print_info "Visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
        exit 1
    fi
    print_info "AWS CLI version: $(aws --version)"
}

# Check AWS credentials
check_aws_credentials() {
    print_info "Checking AWS credentials..."
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials are not configured properly."
        print_info "Run 'aws configure' to set up your credentials."
        exit 1
    fi

    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    print_info "AWS Account ID: ${AWS_ACCOUNT_ID}"
    print_info "Current AWS Region: ${AWS_REGION}"
}

# Check if Docker is installed
check_docker() {
    print_info "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install it first."
        exit 1
    fi
    print_info "Docker version: $(docker --version)"
}

# Create ECR repositories
create_ecr_repositories() {
    print_info "Creating ECR repositories..."

    for repo in $ECR_REPOSITORY_BASE $ECR_REPOSITORY_APP $ECR_REPOSITORY_WEB; do
        if aws ecr describe-repositories --repository-names $repo --region $AWS_REGION &> /dev/null; then
            print_warning "ECR repository '$repo' already exists."
        else
            print_info "Creating ECR repository: $repo"
            aws ecr create-repository \
                --repository-name $repo \
                --region $AWS_REGION \
                --image-scanning-configuration scanOnPush=true \
                --encryption-configuration encryptionType=AES256
            print_info "Created ECR repository: $repo"
        fi
    done
}

# Login to ECR
login_to_ecr() {
    print_info "Logging in to Amazon ECR..."
    aws ecr get-login-password --region $AWS_REGION | \
        docker login --username AWS --password-stdin \
        ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
    print_info "Successfully logged in to ECR"
}

# Build and push Docker images
build_and_push_images() {
    print_info "Building and pushing Docker images..."

    # Build and push base image
    print_info "Building base image..."
    docker build -t ${ECR_REPOSITORY_BASE}:latest .
    docker tag ${ECR_REPOSITORY_BASE}:latest \
        ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_BASE}:latest

    print_info "Pushing base image to ECR..."
    docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_BASE}:latest

    # Build and push app image
    if [ -f "app/Dockerfile" ]; then
        print_info "Building app image..."
        docker build -t ${ECR_REPOSITORY_APP}:latest ./app
        docker tag ${ECR_REPOSITORY_APP}:latest \
            ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_APP}:latest

        print_info "Pushing app image to ECR..."
        docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_APP}:latest
    fi

    # Build and push web image
    if [ -f "web/Dockerfile" ]; then
        print_info "Building web image..."
        docker build -t ${ECR_REPOSITORY_WEB}:latest ./web
        docker tag ${ECR_REPOSITORY_WEB}:latest \
            ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_WEB}:latest

        print_info "Pushing web image to ECR..."
        docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_WEB}:latest
    fi
}

# Create ECS cluster
create_ecs_cluster() {
    print_info "Creating ECS cluster..."

    if aws ecs describe-clusters --clusters $ECS_CLUSTER_NAME --region $AWS_REGION \
        --query 'clusters[0].status' --output text 2>/dev/null | grep -q "ACTIVE"; then
        print_warning "ECS cluster '$ECS_CLUSTER_NAME' already exists."
    else
        aws ecs create-cluster \
            --cluster-name $ECS_CLUSTER_NAME \
            --region $AWS_REGION \
            --capacity-providers FARGATE FARGATE_SPOT \
            --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1
        print_info "Created ECS cluster: $ECS_CLUSTER_NAME"
    fi
}

# Create IAM execution role for ECS tasks
create_iam_roles() {
    print_info "Creating IAM roles for ECS..."

    ROLE_NAME="${PROJECT_NAME}-ecs-task-execution-role"

    # Check if role exists
    if aws iam get-role --role-name $ROLE_NAME &> /dev/null; then
        print_warning "IAM role '$ROLE_NAME' already exists."
    else
        print_info "Creating IAM execution role..."

        # Create trust policy
        cat > /tmp/trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

        aws iam create-role \
            --role-name $ROLE_NAME \
            --assume-role-policy-document file:///tmp/trust-policy.json

        # Attach AWS managed policy
        aws iam attach-role-policy \
            --role-name $ROLE_NAME \
            --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

        print_info "Created IAM role: $ROLE_NAME"
        rm /tmp/trust-policy.json
    fi
}

# Create VPC and security groups (simplified - you may want to customize this)
create_network_resources() {
    print_info "Setting up network resources..."

    # Get default VPC
    VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" \
        --query 'Vpcs[0].VpcId' --output text --region $AWS_REGION)

    if [ "$VPC_ID" == "None" ] || [ -z "$VPC_ID" ]; then
        print_warning "No default VPC found. You may need to create VPC resources manually."
        return
    fi

    print_info "Using VPC: $VPC_ID"

    # Create security group
    SG_NAME="${PROJECT_NAME}-sg"
    SG_ID=$(aws ec2 describe-security-groups \
        --filters "Name=group-name,Values=$SG_NAME" "Name=vpc-id,Values=$VPC_ID" \
        --query 'SecurityGroups[0].GroupId' --output text --region $AWS_REGION 2>/dev/null)

    if [ "$SG_ID" != "None" ] && [ -n "$SG_ID" ]; then
        print_warning "Security group '$SG_NAME' already exists: $SG_ID"
    else
        print_info "Creating security group..."
        SG_ID=$(aws ec2 create-security-group \
            --group-name $SG_NAME \
            --description "Security group for ${PROJECT_NAME}" \
            --vpc-id $VPC_ID \
            --region $AWS_REGION \
            --query 'GroupId' --output text)

        # Add ingress rules (customize as needed)
        aws ec2 authorize-security-group-ingress \
            --group-id $SG_ID \
            --protocol tcp \
            --port 80 \
            --cidr 0.0.0.0/0 \
            --region $AWS_REGION

        aws ec2 authorize-security-group-ingress \
            --group-id $SG_ID \
            --protocol tcp \
            --port 443 \
            --cidr 0.0.0.0/0 \
            --region $AWS_REGION

        print_info "Created security group: $SG_ID"
    fi
}

# Display summary
display_summary() {
    print_info "=========================================="
    print_info "AWS Setup Complete!"
    print_info "=========================================="
    print_info "AWS Account ID: ${AWS_ACCOUNT_ID}"
    print_info "Region: ${AWS_REGION}"
    print_info "ECS Cluster: ${ECS_CLUSTER_NAME}"
    print_info ""
    print_info "ECR Repositories:"
    print_info "  - ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_BASE}"
    print_info "  - ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_APP}"
    print_info "  - ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_WEB}"
    print_info ""
    print_info "Next steps:"
    print_info "1. Review and customize ECS task definitions"
    print_info "2. Deploy services to ECS cluster"
    print_info "3. Configure load balancers if needed"
    print_info "4. Set up CloudWatch logging and monitoring"
    print_info "=========================================="
}

# Main execution
main() {
    print_info "Starting AWS setup for Face Recognition Project..."
    print_info "Region: ${AWS_REGION}"

    check_aws_cli
    check_aws_credentials
    check_docker
    create_ecr_repositories
    login_to_ecr
    build_and_push_images
    create_ecs_cluster
    create_iam_roles
    create_network_resources
    display_summary
}

# Run main function
main
