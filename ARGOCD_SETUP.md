# ArgoCD App of Apps Repository Structure

## 📋 Overview
Repository has been restructured to support ArgoCD's "App of Apps" deployment pattern. This allows ArgoCD to manage multiple Kubernetes applications as a unified system with automatic synchronization and pruning.

---

## 📁 Final Repository Structure

```
microk8s-docker/
├── root-app.yaml                           # Root ArgoCD Application (entry point)
├── components/                              # ArgoCD Application manifests
│   ├── namespace-app.yaml                  # Deploys: app-test namespace
│   ├── secrets-app.yaml                    # Deploys: database credentials
│   ├── db-app.yaml                         # Deploys: PostgreSQL database
│   └── web-app.yaml                        # Deploys: Nginx web server
├── k8s-manifests/                          # Raw Kubernetes manifests
│   ├── namespace/
│   │   └── namespace.yaml                  # app-test Namespace
│   ├── secrets/
│   │   └── secret.yaml                     # DB credentials Secret
│   ├── db/
│   │   └── db.yaml                         # PostgreSQL Deployment & Service
│   └── web/
│       └── app.yaml                        # Nginx Deployment & Service
└── README.md
```

---

## 🔄 How It Works

### 1. **Root Application** (`root-app.yaml`)
- **Name**: `root-app`
- **Namespace**: `argocd`
- **Watches**: `components/` directory
- **Behavior**: 
  - Automatically discovers all ArgoCD Applications in `components/`
  - Manages them as a unified entity
  - Syncs all child applications when any changes are detected

### 2. **Component Applications**

#### Namespace Application (`components/namespace-app.yaml`)
```yaml
name: namespace-app
path: k8s-manifests/namespace
destination: default namespace
```
- Creates the `app-test` namespace
- Deployed first (dependency for secrets and workloads)

#### Secrets Application (`components/secrets-app.yaml`)
```yaml
name: secrets-app
path: k8s-manifests/secrets
destination: app-test namespace
```
- Creates database credentials secret
- Dependency for database application

#### Database Application (`components/db-app.yaml`)
```yaml
name: db-app
path: k8s-manifests/db
destination: app-test namespace
```
- Deploys PostgreSQL database
- Creates Kubernetes Service for connectivity

#### Web Application (`components/web-app.yaml`)
```yaml
name: web-app
path: k8s-manifests/web
destination: app-test namespace
```
- Deploys Nginx web server
- Exposes via NodePort (30080)

---

## 🚀 Deployment Instructions

### Prerequisites
- ArgoCD installed in your cluster (in `argocd` namespace)
- Git repository configured as ArgoCD source
- `kubectl` access to the cluster

### Steps

1. **Add Repository to ArgoCD** (via UI or CLI)
   ```bash
   argocd repo add https://github.com/ahmedha22/microk8s-docker \
	 --username <github-username> \
	 --password <github-token>
   ```

2. **Deploy Root Application**
   ```bash
   kubectl apply -f root-app.yaml
   ```
   Or use ArgoCD UI to create Application from the repository.

3. **Monitor Sync**
   ```bash
   argocd app sync root-app
   kubectl get applications -n argocd
   ```

4. **Verify Deployment**
   ```bash
   kubectl get ns app-test
   kubectl get pods -n app-test
   kubectl get services -n app-test
   ```

---

## 🔑 Key Features

✅ **Automatic Synchronization**
- All child applications sync automatically when changes are pushed to `main` branch

✅ **Self-Healing**
- Automatically restores desired state if resources are manually modified

✅ **Pruning**
- Automatically removes resources when they're removed from manifests

✅ **Namespace Isolation**
- Applications organized in `app-test` namespace for clean separation

✅ **Dependency Management**
- Namespace created first, then secrets, then workloads

---

## 📝 Manifest Details

All ArgoCD Applications use:
- **API Version**: `argoproj.io/v1alpha1`
- **Project**: `default`
- **Sync Policy**: Automatic
- **Pruning**: Enabled
- **Self-Healing**: Enabled
- **Namespace Creation**: Enabled

---

## 🔀 Git Workflow

- **Branch**: `feature/k8s-components-refactor`
- **Main Changes**:
  - Created ArgoCD Application manifests
  - Organized Kubernetes manifests in version-controlled directories
  - Removed duplicate files
  - Implemented App of Apps pattern

---

## ✨ Next Steps

1. Review the pull request on GitHub
2. Merge to `main` branch once approved
3. Install ArgoCD in your cluster if not already done
4. Deploy `root-app.yaml`
5. Monitor applications in ArgoCD dashboard

---

## 🐛 Troubleshooting

**Applications stuck in "OutOfSync"**
- Check branch is correct: `targetRevision: main`
- Verify repository is added to ArgoCD
- Check file paths match repository structure

**Namespace not created**
- Ensure `namespace-app` deploys first
- Check `CreateNamespace=true` syncOption

**Database connection issues**
- Verify Secret is created: `kubectl get secrets -n app-test`
- Check database pods: `kubectl get pods -n app-test`

---

## 📚 References

- [ArgoCD App of Apps Pattern](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern)
- [ArgoCD Application Spec](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)
- [Kubernetes Deployment Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
