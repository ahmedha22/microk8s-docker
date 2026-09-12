# microk8s-docker

Small DevOps practice project: a static web app is built into a Docker image,
published to GitHub Container Registry, and deployed to MicroK8s by Argo CD.

## Pipeline flow

1. Change `index.html` and push to the `main` branch.
2. GitHub Actions builds and publishes `ghcr.io/ahmedha22/microk8s-docker:<commit-sha>`.
3. GitHub Actions updates `components/app.yaml` with that image tag.
4. Argo CD detects the manifest change and deploys the new image.

Before the first deployment, open the package settings for the GitHub Container
Registry package and make the package public. This keeps the MicroK8s cluster
from needing registry credentials for this practice project.

Test the image locally:

```bash
docker build -t microk8s-docker-test .
docker run --rm -p 8080:80 microk8s-docker-test
```

Open `http://localhost:8080` to view the app.

## Direct deployment

```bash
microk8s kubectl apply -f components/namespace.yaml
microk8s kubectl apply -f components/secrets.yaml
microk8s kubectl apply -f components/db.yaml
microk8s kubectl apply -f components/app.yaml
```

Check the workloads and services:

```bash
microk8s kubectl get pods,svc -n app-test
```

The web service is exposed on NodePort `30080`:

```text
http://<microk8s-node-ip>:30080
```

After pushing a change, watch the rollout:

```bash
microk8s kubectl get application root-app-umbrella -n argocd
microk8s kubectl rollout status deployment/web-deployment -n app-test
microk8s kubectl get pods -n app-test
```

## Argo CD

Apply `k8s-test/root-app.yaml` after Argo CD is installed. It points Argo CD at
the `components` directory and enables automated sync, pruning, and self-healing.

## Test-only configuration

`components/secrets.yaml` contains a plain-text test password. Do not use that
password or commit real credentials for anything beyond a local test cluster.

## Second practice app

The `platform` directory contains a separate Flask API and PostgreSQL practice
application. It uses two workflows and Flux CD instead of Argo CD:

- `platform-ci.yml` tests and publishes the API image.
- `platform-cd.yml` updates the GitOps image tag.
- Flux CD watches `platform/k8s` and deploys the change.

See `platform/README.md` for local Compose and MicroK8s instructions.