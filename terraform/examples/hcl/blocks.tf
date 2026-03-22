# Define core Terraform settings and required providers
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Create a new VPC
resource "aws_vpc" "acme_vpc" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "acme-network"
  }
}

# Fetch an existing Amazon Linux 2 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Define an input variable for the instance type
variable "instance_type" {
  description = "The EC2 instance type"
  type        = string
  default     = "t2.micro"
}

# Output the ID of the created VPC
output "vpc_id" {
  value       = aws_vpc.acme_vpc.id
  description = "The ID of the Acme VPC"
}

# Define local variables for reuse
locals {
  common_tags = {
    Company     = "acme"
    Environment = "Production"
  }
}
