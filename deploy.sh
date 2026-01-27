#!/bin/bash

# Deployment script for job-app-tracker
# This script runs Terraform to provision infrastructure and prepares for Ansible deployment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TERRAFORM_DIR="${SCRIPT_DIR}/infra/terraform"
ANSIBLE_DIR="${SCRIPT_DIR}/infra/ansible"  # Placeholder for future Ansible setup

# Default values
SKIP_PLAN=false
AUTO_APPROVE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-plan)
            SKIP_PLAN=true
            shift
            ;;
        --auto-approve)
            AUTO_APPROVE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-plan      Skip terraform plan and go directly to apply"
            echo "  --auto-approve   Auto-approve terraform apply (non-interactive)"
            echo "  --help           Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    print_error "Terraform is not installed. Please install Terraform first."
    exit 1
fi

print_info "Terraform version: $(terraform version | head -n 1)"

# Check if we're in the right directory
if [ ! -d "$TERRAFORM_DIR" ]; then
    print_error "Terraform directory not found: $TERRAFORM_DIR"
    exit 1
fi

# Change to terraform directory
cd "$TERRAFORM_DIR"

print_info "Working directory: $(pwd)"

# Check for required variables
print_info "Checking for required Terraform variables..."

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    print_warn "terraform.tfvars not found. You may need to create it with required variables:"
    echo "  - owner_email"
    echo "  - ssh_public_key"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Initialize Terraform
print_info "Initializing Terraform..."
terraform init

if [ $? -ne 0 ]; then
    print_error "Terraform init failed"
    exit 1
fi

# Run terraform plan (unless skipped)
if [ "$SKIP_PLAN" = false ]; then
    print_info "Running Terraform plan..."
    terraform plan -out=tfplan
    
    if [ $? -ne 0 ]; then
        print_error "Terraform plan failed"
        exit 1
    fi
    
    print_info "Plan completed successfully. Review the plan above."
    
    if [ "$AUTO_APPROVE" = false ]; then
        read -p "Do you want to apply this plan? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_warn "Deployment cancelled by user"
            exit 0
        fi
    fi
fi

# Apply Terraform
print_info "Applying Terraform configuration..."
if [ "$AUTO_APPROVE" = true ] || [ "$SKIP_PLAN" = true ]; then
    terraform apply -auto-approve
else
    terraform apply tfplan
fi

if [ $? -ne 0 ]; then
    print_error "Terraform apply failed"
    exit 1
fi

print_info "Terraform apply completed successfully!"

# Display outputs
print_info "Terraform outputs:"
terraform output

# Get VM public IP and SSH connection info for Ansible
VM_PUBLIC_IP=$(terraform output -raw vm_public_ip 2>/dev/null || echo "")
SSH_CONNECTION=$(terraform output -raw ssh_connection_command 2>/dev/null || echo "")

if [ -n "$VM_PUBLIC_IP" ]; then
    print_info "VM Public IP: $VM_PUBLIC_IP"
    if [ -n "$SSH_CONNECTION" ]; then
        print_info "SSH Connection: $SSH_CONNECTION"
    else
        print_info "SSH Connection: ssh localadmin@${VM_PUBLIC_IP}"
    fi
fi

# Ansible deployment section (placeholder)
print_info "Ansible deployment section (not yet implemented)"
if [ -d "$ANSIBLE_DIR" ]; then
    print_warn "Ansible directory exists but deployment is not configured yet"
    # Future Ansible deployment code will go here
    # Example:
    # print_info "Running Ansible playbook..."
    # cd "$ANSIBLE_DIR"
    # ansible-playbook -i inventory.yml deploy.yml
else
    print_info "Ansible directory does not exist yet. Skipping Ansible deployment."
fi

print_info "Deployment script completed!"
