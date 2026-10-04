# AWS MCP hosting

Deployment region: `us-east-2`, AWS profile: `deepagentlabs`. CloudFront is global;
all regional AWS operations explicitly select us-east-2.

Three CloudFormation stacks own the deployment:

- `deep-agentic-core-mcp-assets`: retained ECR repository with immutable tags.
- `deep-agentic-core-mcp-users`: encrypted on-demand DynamoDB user/key table with
  point-in-time recovery, retained on deletion.
- `deep-agentic-core-mcp`: dedicated VPC, private ALB, CloudFront VPC origin,
  ECS Fargate service, encrypted single-node Valkey sessions, runtime cache
  secrets, scoped IAM roles, and 14-day CloudWatch logs.

## Signup and connecting

Open the deployed `/signup` page. Enter a display name and create your MCP key.
Download or privately save the connection details before leaving the page: keys
are shown once and cannot be recovered. Configure your MCP client with:

```text
Transport: Streamable HTTP
URL: https://<distribution>.cloudfront.net/mcp
Header: Authorization: Bearer <your-key>
```

The display name is an unverified label, not a login or verified identity.
There are no passwords, email verification, or account recovery. Each signup
gets a generated UUID and its own workflow sessions; repeated display names do
not share an account. Anyone with a key can access that user's sessions.

Under “Already have a key?” users can inspect their own account, replace their
key, or revoke it. Replacement preserves the user ID and sessions, and the old
key immediately stops authenticating. Revocation permanently closes access to
that account. Existing in-flight requests may finish. No worker restart is
required. The initial migrated `admin` identity has the same application
permissions as other users; it is not an elevated role.

DynamoDB stores `USER#<id>` records with display name, status, and current key
hash; `KEY#<sha256>` records map hashes to stable user IDs. No plaintext keys
are stored. Transactional signup and rotation prevent partial writes or
concurrent key resurrection. Consistent reads enforce the current key and
revocation status. The task role can get/write/update/delete only this table;
it cannot scan the table or administer AWS.

The public signup API is `POST /api/signup` with JSON
`{"display_name":"Alex"}`. The authenticated `/api/account` endpoint accepts
GET (profile), POST (replace key), and DELETE (revoke key), using the MCP key as
a bearer header. Responses are not cached. Browser origins must match the
configured public origin. Redis enforces signup limits across workers:
10/hour per client address and 100/day globally. These initial limits can be
adjusted in `signup.py`. The CloudFront/ALB proxy suffix is trusted only because
origin and task ingress are restricted to this deployment's proxy chain.

## Infrastructure and availability

CloudFront provides HTTPS and forwards Authorization/MCP headers without caching
responses. Its ALB origin is private. ALB ingress is limited to the CloudFront
origin prefix list, task ingress to the ALB, and cache ingress to tasks. Public
task IPs provide outbound ECR/AWS API access without NAT and accept no direct
client traffic. Valkey requires TLS and a generated AUTH token. Secrets Manager
stores infrastructure credentials, not user API keys.

The image runs as UID 10001 with a read-only root filesystem and a writable
volume at `/tmp/mcp` for temporary reports. Deployments pin image digests. Schema
assets come from a pinned upstream commit with SHA-256 verification.

Initial capacity is one 0.25-vCPU/512-MiB Fargate task and one cache.t4g.micro
Valkey 8.2 node, without high availability. Increase DesiredCount for more HTTP
workers; cache replicas/failover require an infrastructure change. MCP request
limits are per worker. Workflow sessions expire after one hour of inactivity
and are capped at 100 sessions / 4 MiB per user. Cache snapshots retain one day.

AWS charges accrue for running infrastructure, DynamoDB requests/storage/recovery,
CloudFront, public task addresses, secrets, logs, images, and snapshots. No durable
CloudTrail trail was configured; the account had no discoverable trail initially.

## Deployment and migration

### Custom domain

The public domain is `mcp.deepagentlabs.io` (activated and verified on 2026-10-04).
MCP is at `https://mcp.deepagentlabs.io/mcp`; signup is at
`https://mcp.deepagentlabs.io/signup`. CloudFront needs an issued
ACM certificate in us-east-1; the application and data remain in us-east-2.
The certificate request is tracked in the ignored deployment state file.
DNS for deepagentlabs.io uses Wix nameservers. Add these CNAME records there:

| Host (relative to deepagentlabs.io) | Target |
| --- | --- |
| `_6ac6a8a071073fa43af59078da1e2351.mcp` | `_7ae5ca3331873d743a5d1ac736cb345c.wzccmgtwzk.acm-validations.aws` |
| `mcp` | `d3cpcnb99flgof.cloudfront.net` |

Keep the first record for automatic certificate renewal. Wait for ACM status
`ISSUED` before executing the domain change set. Pass `--domain` and
`--certificate-arn` to `scripts/aws_deploy.py prepare --change-set-type UPDATE`.
Future preparations preserve the selected domain/certificate in local state.
The template adds the CloudFront alias, SNI certificate with minimum TLS 1.2,
application host/origin allowlists, canonical signup URL, and output URLs.
The original CloudFront signup origin is explicitly allowed during migration.
After rollout, verify health, MCP access, and signup on the new domain.

### Service lifecycle

Validate templates and inspect change sets before execution. Create the assets
and users stacks first. Before moving an existing deployment from injected
keys to DynamoDB, run:

```bash
.venv/bin/python scripts/migrate_aws_keys.py
```

This reads the old secret in memory, migrates only hashes, preserves existing
user IDs/session ownership, and verifies the migrated keys. It never overwrites
an existing account. The service keeps serving its old image during migration.

Build the AWS image with a unique tag, then use:

```bash
python3 scripts/build_container.py --target aws --tag deep-agentic-core-mcp:<unique-tag>
python3 scripts/aws_deploy.py publish --tag <unique-tag>
python3 scripts/aws_deploy.py prepare --tag <unique-tag> --change-set-type UPDATE
# Review the change set before executing.
python3 scripts/aws_deploy.py execute
python3 scripts/aws_deploy.py status
python3 scripts/aws_deploy.py verify
python3 scripts/verify_signup.py https://<distribution>.cloudfront.net
```

Verification uses the private, git-ignored `.secrets/aws-admin.json` from the
initial deployment. DynamoDB cannot recreate that plaintext key; if it is lost,
use a new signup key and update your private verification file. Do not rotate
or revoke a user's key just to regenerate a verification credential.

After rollout verifies, retire the retained legacy user-key secret through a
recoverable Secrets Manager deletion window. The service no longer reads it.
The initial migration completed on 2026-10-04; its old user-key secret was
scheduled for deletion with a seven-day recovery window after live verification.
Deleting stacks retains user records, cache, cache credentials, and images.
These require separate deliberate cleanup to stop all related charges.

## Continuous deployment

See [CI-CD.md](CI-CD.md) for the GitHub Actions workflow, required secrets, scoped
permissions, deployment checks, and credential rotation.
