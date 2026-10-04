# AWS continuous deployment

CI checks pull requests, pushes to `main`, and manual runs without deploying.
A pushed `v*` version tag starts `release-pypi.yml`, which runs the full test
matrix and package checks before publishing to PyPI. AWS deployment depends on
successful PyPI publication and builds the same tagged source. It publishes an
immutable ECR image, updates ECS through CloudFormation, and verifies the public
HTTPS endpoint and authenticated MCP integrations. A failed PyPI publication
prevents AWS deployment.

## GitHub secrets

Configure repository secrets in `DeepAgentLabs/mcp-server`:

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: credentials for the dedicated
  `deep-agentic-core-mcp-github-deploy` IAM user.
- `MCP_SMOKE_KEY`: a dedicated application API key for authenticated health checks.

These secrets have been installed using the operator's AWS profile. Region
`us-east-2` is configured in the workflow. Never put credentials in the repo.

The scoped IAM policy is managed in AWS IAM. It allows ECR publishing,
CloudFormation change sets on the existing deployment, ECS revision/service
updates, and passing the two existing runtime roles. Read permissions for load-balancer and CloudFront attributes and deployment
events allow CloudFormation to resolve existing resource references and report
failures. Task-definition registration, reads, and deregistration use wildcard
resources where AWS requires them; service and pass-role permissions are scoped.
Infrastructure provisioning and database access are handled separately using the operator profile.

## Deployment behavior

Deployments are serialized. Each image tag includes the release tag, run ID,
and attempt; ECS receives the image digest. Release tags should advance in order;
rerunning an older release deployment would deploy that older version.

The deployment script uses the existing CloudFormation template and preserves
all parameters except `ImageUri`, including the domain and cache credentials.
It refuses changes outside the ECS task definition and service, and refuses
service replacement. ECS's deployment circuit breaker rolls back tasks that fail
to become healthy. A failure of the final MCP smoke check fails the workflow;
it does not automatically roll back an otherwise completed deployment.

For infrastructure changes, use the reviewed operator flow in [README.md](README.md).
To retry a failed release deployment, rerun its failed job in GitHub Actions.
To deploy new code, prepare and publish a new version tag. Rotate the IAM access key by updating both repository secrets, then
remove the old key after a successful run. Rotate or revoke the MCP smoke key
through its application account and update `MCP_SMOKE_KEY` when rotating.
