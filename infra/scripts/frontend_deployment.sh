#!/bin/bash
#
# Perform frontend deployment to Firebase
#

# Function to display usage and exit
usage() {
    echo "Usage: $0 --project <your_project_id>"
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
if [[ $# -lt 2 ]]; then
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
        *)
            echo "Error: Unknown parameter '$1'."
            usage
            ;;
    esac
done

# Deploys backend to Firebase
main(){
    echo "Copying configuration files"
    cp output_config/environments.ts ../frontend/src/environments
    cp output_config/form-config.json ../frontend/src/assets/config/

    cd ../frontend
    echo "Deploying frontend to firebase"
    npm install -g @angular/cli
    npm install --legacy-peer-deps
    npm install -g firebase-tools
    ng build
    firebase experiments:enable webframeworks
    firebase deploy --only hosting --project="$project"
}

# Deploy
main