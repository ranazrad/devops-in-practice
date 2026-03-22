# Acme Terraform AWS Example

This contains a basic Terraform configuration to demonstrate how to authenticate with AWS, initialize the working directory, generate an execution plan, apply the changes, inspect the state, and destroy the infrastructure.

## Prerequisites

* [Terraform](https://developer.hashicorp.com/terraform/downloads) installed.
* An active AWS account with programmatic access (Access Key ID and Secret Access Key).

## Step 1: Authenticate with AWS

Before running Terraform, you must provide your AWS credentials. Choose one of the following methods (for Linux/macOS environments):

### Option A: Using AWS CLI

If you have the AWS CLI installed, you can configure your default credentials by running:

```bash
aws configure
```

You will be prompted to enter your `AWS Access Key ID`, `AWS Secret Access Key`, `Default region name` (e.g., `us-east-1`), and `Default output format`. Terraform will automatically use these saved credentials.

### Option B: Using Environment Variables (Export)

Alternatively, you can export your credentials directly in your current terminal session. This is a quick method for temporary access without saving a profile:

```bash
export AWS_ACCESS_KEY_ID="your_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
export AWS_DEFAULT_REGION="us-east-1"
```

### Option C: Using an AWS Profile

If you manage multiple AWS environments, you can configure named profiles in your `~/.aws/credentials` file. To instruct Terraform to use a specific profile, export the `AWS_PROFILE` environment variable:

```bash
export AWS_PROFILE="my_profile"
```

## Step 2: Initialize Terraform

Initialize the working directory containing the Terraform configuration files. This command downloads the required AWS provider plugin and creates the `.terraform` directory and lock file.

```bash
# Initialize the Terraform working directory
terraform init
```

## Step 3: Generate an Execution Plan

Run the `plan` command to see the changes Terraform will make to your AWS infrastructure. This is a dry run and will not create or modify any real resources.

```bash
# Preview the infrastructure changes
terraform plan
```

## Step 4: Apply the Configuration

Run the `apply` command to execute the actions proposed in the plan and provision the resources in your AWS account. You will be prompted to type `yes` to confirm.

```bash
# Create or update the infrastructure
terraform apply
```

## Step 5: Inspect the State

After a successful apply, Terraform creates a `terraform.tfstate` file (locally, unless a remote backend is configured) to keep track of the resources it manages. You can inspect this state to see the current infrastructure details.

```bash
# View a human-readable output of the current state
terraform show

# List all resources currently tracked in the state file
terraform state list
```

## Step 6: Destroy the Infrastructure

When you no longer need the resources, use the `destroy` command to remove everything created by this Terraform configuration. This prevents unwanted AWS charges. You will be prompted to type `yes` to confirm.

```bash
# Tear down the infrastructure
terraform destroy
```
