# AWS continuous deployment

The CI workflow tests Python 3.10–3.13 and builds the Python distributions.
After these checks pass, pushes to `main` build and publish an immutable Docker
image to ECR, update the existing ECS deployment through CloudFormation, and
check the public HTTPS endpoint and authenticated MCP integrations. Pull requests
run checks without AWS deployment credentials.

## GitHub secrets

Configure repository secrets in `DeepAgentLabs/mcp-server`:

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: credentials for the dedicated
  `deep-agentic-core-mcp-github-deploy` IAM user.
- `MCP_SMOKE_KEY`: a dedicated application API key for authenticated health checks.

These secrets have been installed using the operator's AWS profile. Region
`us-east-2` is configured in the workflow. Never put credentials in the repo.

The scoped IAM policy is managed in AWS IAM. It allows ECR publishing,
CloudFormation change sets on the existing deployment, ECS revision/service
updates, and passing the two existing runtime roles. Infrastructure provisioning
and database access are handled separately using the operator profile.

## Deployment behavior

Deployments are serialized. A queued run skips deployment if its commit has
already been superseded on `main`. Each image tag includes the commit, run ID,
and attempt; ECS receives the image digest.

The deployment script uses the existing CloudFormation template and preserves
all parameters except `ImageUri`, including the domain and cache credentials.
It refuses changes outside the ECS task definition and service, and refuses
service replacement. ECS's deployment circuit breaker rolls back tasks that fail
to become healthy. A failure of the final MCP smoke check fails the workflow;
it does not automatically roll back an otherwise completed deployment.

For infrastructure changes, use the reviewed operator flow in [README.md](README.md).
To redeploy the current `main` commit, run the CI workflow manually in GitHub
Actions. Rotate the IAM access key by updating both repository secrets, then
remove the old key after a successful run. Rotate or revoke the MCP smoke key
through its application account and update `MCP_SMOKE_KEY` when rotating.
