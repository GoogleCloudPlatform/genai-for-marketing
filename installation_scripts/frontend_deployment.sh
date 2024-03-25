#!/bin/bash

set -e

PROJECT=$1

cp templates/environments.ts ../frontend/src/environments
cd ../frontend
npm install -g @angular/cli
npm install --legacy-peer-deps
npm install -g firebase-tools
ng build
firebase experiments:enable webframeworks
firebase deploy --only hosting --project="${PROJECT}"