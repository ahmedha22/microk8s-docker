# Platform API practice app

This is the second learning path in the repository. It is separate from the
original `app-test` Argo CD demo and uses Flux CD for deployment.

## Local run

```bash
docker compose -f platform/docker-compose.yml up --build
```

Test the API:

```bash
curl http://localhost:8081/health
```

## MicroK8s deployment

Install Flux once, then apply the Flux source and Kustomization:

```bash
flux install
microk8s kubectl apply -f platform/flux/source.yaml
microk8s kubectl apply -f platform/flux/kustomization.yaml
```

Check deployment:

```bash
microk8s kubectl get pods -n platform-dev
microk8s kubectl get svc -n platform-dev
```

The API is exposed on NodePort `30081`:

```text
http://<microk8s-node-ip>:30081/health
```

The database password in `platform/k8s/postgres.yaml` is only for local
practice. Use an encrypted secret or an external secret manager for real use.
