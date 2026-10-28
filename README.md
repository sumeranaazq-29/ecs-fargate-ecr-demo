# ECS Fargate + ECR Demo

A small Flask app, packaged as a Docker image, stored in Amazon ECR and run on Amazon ECS (Fargate).

## Architecture
Docker image -> Amazon ECR (private registry) -> ECS task definition -> ECS service on Fargate

## What I did
1. Built a Flask app with a `/` route and a `/health` route
2. Wrote a Dockerfile (python:3.12-slim base, non-root user, gunicorn)
3. Built the image for linux/amd64 and tested it locally
4. Created a private ECR repository (scan on push enabled) and pushed the image
5. Created an ECS cluster, a Fargate task definition (0.25 vCPU, 0.5 GB) and a service
6. Opened the app from the task's public IP, then deleted everything to avoid costs

## Security choices
- Container runs as a non-root user on a slim base image
- Security group allowed port 5000 only from my own IP, not the whole internet
- No task role, because the app calls no AWS services (least privilege)
- Task execution role used only to pull the image and write logs
- No secrets stored in the image or in this repository

## Cost control
- Smallest Fargate size, no load balancer, one task
- Cluster, service and task definition deleted after testing

## Problems I hit
- ECR could not scan the image by tag, because Docker added an attestation entry that made the tag an image index. Scanning by the image digest is the next step.
- The task needs a public IP to pull the image from ECR

## Next steps
- Scan the image by digest and review the findings
- Add a load balancer with a stable DNS name
- Automate build and deploy with GitHub Actions or Jenkins
- Move configuration into Secrets Manager

## Files
- `app.py`, `requirements.txt`, `Dockerfile`: the app and its image
- `task-definition.json`: the ECS task definition (account ID replaced with a placeholder)
- `screenshots/`: the app running on Fargate
