# AWS deployment and package releases

From **0.4.1**, GitHub Actions does not deploy AWS. Pull requests and main pushes
run checks; a `v*` tag validates and publishes PyPI, GitHub Release and MCP Registry
metadata. Publishing or retrying a release does not update the running AWS service.

The existing Docker build, ECR/CloudFormation deployment and smoke-check scripts
remain manual operator tools. Follow the reviewed operator flow in
[README.md](README.md) for an explicit deployment. The service template and runtime
resources are unchanged by this pipeline change. Do not infer hosted deployment
version or health from a successful package release.

Standalone images pin Lens 0.13.0, Chaos 0.11.0, Evals 0.12.0 and Sidecar
0.10.1. Live Sidecar controls require explicit host runtime bindings and an
independently authorized operator; installing Sidecar does not create a binding. Use an immutable image reference for manual deployments.
Existing GitHub AWS secrets are not consumed by the release workflow. Credential
rotation and infrastructure provisioning remain separate operator responsibilities.

See [MCP 0.7 upgrade, smoke checks and rollback](../../docs/release-readiness.md)
for operational acceptance. Restore an immutable prior image only after
reconciling in-flight effects and dispatch guards; never restore revoked keys.
