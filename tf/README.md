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
### Enable Firebase authentication
1. Go to https://firebase.corp.google.com/project/<your_project_id>/authentication/providers
2. Select google and enable it
3. Set the name for the project and support email for project
4. Save

### Enable Dialogflow CX Messenger
1. Go to https://dialogflow.cloud.google.com/cx/projects/<your_project_id> and select the agent
2. Click in Publish
3. Select Unauthenticated API (anonymous access)
4. Click in Enable the unauthenticated API