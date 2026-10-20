# AWS deployment and package releases

From **0.4.1**, GitHub Actions does not deploy AWS. Pull requests and main pushes
run checks; a `v*` tag validates and publishes PyPI, GitHub Release and MCP Registry
metadata. Publishing or retrying a release does not update the running AWS service.

The existing Docker build, ECR/CloudFormation deployment and smoke-check scripts
remain manual operator tools. Follow the reviewed operator flow in
[README.md](README.md) for an explicit deployment. The service template and runtime
resources are unchanged by this pipeline change. Do not infer hosted deployment
version or health from a successful package release.

Standalone image recipes pin Sidecar 0.9.0 for package discovery; they expose no
live Sidecar task controls. Use an immutable image reference for manual deployments.
Existing GitHub AWS secrets are not consumed by the release workflow. Credential
rotation and infrastructure provisioning remain separate operator responsibilities.
