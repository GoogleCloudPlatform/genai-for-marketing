#!/bin/bash
#
# Perform backend APIs deployment to Cloud Run
#

# Function to display usage and exit
usage() {
    echo "Usage: $0 --project <your_project_id> --region <region> --sa <your_cloud_run_sa>"
    exit 1  # Indicate an error
}

# Function to validate a parameter's value
validate_param() {
    local param_name="$1"
    local param_value="$2"

    if [[ -z "$param_value" ]]; then
        echo "Error: Parameter '$param_name' cannot be empty."
        usage  # Show usage and exit if the value is empty
    fi
}

# Check if enough arguments are provided
if [[ $# -lt 6 ]]; then  
    echo "Error: Insufficient arguments."
    usage
fi

# Parse and validate named parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        --project)
            validate_param "$1" "$2"
            project=$2
            shift 2  # Move to the next parameter
            ;;
        --region)
            validate_param "$1" "$2"
            region=$2
            shift 2
            ;;
        --sa)
            validate_param "$1" "$2"
            sa=$2
            shift 2
            ;;
        *)  
            echo "Error: Unknown parameter '$1'."
            usage
            ;;
    esac
done

# Deploys backend to Cloud Run using the provided region and service account
main(){
    echo "Copying config.toml file"
    cp output_config/config.toml ../backend_apis/app
    cd ../backend_apis
    echo "Deploying backend to cloud run"
    gcloud run deploy genai-for-marketing-backend-apis --source . --project="$project" --region="$region" --service-account="$sa" --allow-unauthenticated
    echo "Done"
}
# Deploy
main