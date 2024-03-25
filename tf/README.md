# Terraform deployment

## Prerequisites:

### Enable Firebase

1. Go to https://console.firebase.google.com/
2. Select add project and laod your GCP project
3. Add Firebase to one of your existing Google Cloud projects
4. Confirm Firebase billing plan
5. Continue and comnplete

### Enable search and Conversation
1. Go to https://console.cloud.google.com/gen-app-builder/start
2. Accept TOS


## Terraform deployment
```
export USER_PROJECT_OVERRIDE=true
export GOOGLE_BILLING_PROJECT=<your_project_id>

terraform apply -var=project_id=<your_project_id>
```


## After Terraform deployment
1. Go to https://firebase.corp.google.com/project/genai-marketing-tf-test/authentication/providers
2. Select google and enable it
3. Set the name for the project and support email for project
4. Save