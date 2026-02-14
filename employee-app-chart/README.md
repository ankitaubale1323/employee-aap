
# 📘 Employee App – Kubernetes Helm Deployment

This project deploys a **Flask + MySQL Employee Application** on Kubernetes using **Helm**.

It demonstrates:

* Flask Deployment
* MySQL StatefulSet
* Headless Service
* Persistent Volume
* Secrets
* Ingress
* Helm templating

---

# 🚀 What is Helm?

Helm is the **package manager for Kubernetes**.

It helps you:

* Install applications
* Upgrade applications
* Manage configurations
* Version control deployments
* Reuse templates

Think of it like:

| Tool     | Platform   |
| -------- | ---------- |
| npm      | Node.js    |
| pip      | Python     |
| apt      | Linux      |
| **Helm** | Kubernetes |

---

# 📦 What is a Helm Chart?

A **Helm Chart** is a collection of Kubernetes YAML templates packaged together.

### Chart Structure

```
employee-app-chart/
│
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── statefulset.yaml
│   ├── service.yaml
│   ├── mysql-headless.yaml
│   ├── ingress.yaml
│   ├── secret.yaml
│   └── configmap.yaml
```

---

# 📄 Chart.yaml

Contains chart metadata:

```yaml
apiVersion: v2
name: employee-app
description: Helm chart for Flask + MySQL application
version: 0.1.0
appVersion: "1.0"
```

Defines:

* Chart name
* Chart version
* App version

---

# ⚙️ values.yaml

Stores configurable values.

Example:

```yaml
namespace: emp-app

flask:
  image: employee-app-flask:latest
  service:
    port: 5000

mysql:
  image: mysql:8
  rootPassword: root
  user: employee_user
  password: root
  database: employee_db
```

Purpose:

* Avoid hardcoding values
* Environment-based configuration
* Used inside templates with `{{ .Values }}`

---

# 🔐 Secret

Stores sensitive data securely.

Used by:

* MySQL
* Flask

Avoids storing passwords in plain YAML files.

---

# 🗄 MySQL – StatefulSet

Used because MySQL requires:

* Persistent storage
* Stable pod identity
* Ordered startup

---

# 🌐 Headless Service

```
clusterIP: None
```

Provides:

* Stable DNS
* Internal communication

Flask connects using:

```
mysql-headless.emp-app.svc.cluster.local
```

---

# 🌍 Flask – Deployment

Used because:

* Stateless
* Scalable
* No persistent identity required

---

# 🔄 Traffic Flow

Using Port Forward:

```
Browser → localhost:5000 → Flask Service → Flask Pod → MySQL
```

Using Ingress:

```
Browser → Ingress → Flask Service → Flask Pod → MySQL
```

---


## Step 1 – Create Helm Chart Folder Automatically

Helm can generate the chart structure for you.

Run:
```bash
helm create employee-app-chart
```

This automatically creates:

employee-app-chart/
│
├── Chart.yaml
├── values.yaml
├── charts/
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl
│   └── tests/


You can then:

Remove unnecessary default files

Add your MySQL StatefulSet

Add Secret

Add Headless Service

📁 Final Project Structure
employee-app/
│
├── employee-app-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── README.md
│   └── templates/
│       ├── flask-deployment.yaml
│       ├── flask-service.yaml
│       ├── mysql-statefulset.yaml
│       ├── mysql-headless.yaml
│       ├── secret.yaml
│       └── ingress.yaml

🚀 Step 2 – Start Minikube
minikube start --driver=docker


Enable ingress (optional):

minikube addons enable ingress


# 🚀 Helm Commands Used in This Project

---

## 🔹 1️⃣ Install Chart

Deploy application:

```bash
helm install empapp . --namespace emp-app --create-namespace
```

* `empapp` → Release name
* `.` → Current chart directory
* `--namespace` → Target namespace
* `--create-namespace` → Creates namespace if missing

---

## 🔹 2️⃣ Upgrade Chart

After making changes:

```bash
helm upgrade empapp . -n emp-app
```

Updates running deployment without deleting resources.

---

## 🔹 3️⃣ Uninstall Chart

Remove entire application:

```bash
helm uninstall empapp -n emp-app
```

Deletes:

* Deployment
* StatefulSet
* Services
* Secrets
* PVC (unless retained)

---

## 🔹 4️⃣ List Releases

```bash
helm list -n emp-app
```

Shows installed Helm releases.

---

## 🔹 5️⃣ Check Release Status

```bash
helm status empapp -n emp-app
```

Shows:

* Deployment info
* Resources created
* Last upgrade time

---

## 🔹 6️⃣ View Rendered YAML (Dry Run)

Very useful for debugging:

```bash
helm template empapp .
```

Shows final Kubernetes YAML before applying.

---

## 🔹 7️⃣ Dry Run Install

```bash
helm install empapp . -n emp-app --dry-run --debug
```

Checks for errors without deploying.

---

## 🔹 8️⃣ Rollback to Previous Version

If upgrade fails:

```bash
helm rollback empapp 1 -n emp-app
```

Rolls back to revision 1.

---

## 🔹 9️⃣ Get Release History

```bash
helm history empapp -n emp-app
```

Shows version history.

---

## 🔹 🔟 Validate Chart

```bash
helm lint .
```

Checks for syntax errors in chart.

---

# 🛠 Kubernetes Commands Used

```bash
kubectl get pods -n emp-app
kubectl get svc -n emp-app
kubectl logs <pod-name> -n emp-app
kubectl describe pod <pod-name> -n emp-app
kubectl port-forward svc/flask-service 5000:5000 -n emp-app
```

---

# 🧠 Why Use Helm Instead of Plain YAML?

Without Helm:

* Multiple static YAML files
* Hardcoded values
* Hard to manage environments

With Helm:

* Reusable templates
* Easy upgrades
* Environment configuration
* Version control
* Production ready

---

# 📚 Technologies Used

* Kubernetes
* Helm
* Minikube
* Docker
* Flask
* MySQL

---

# 🏁 Conclusion

This project demonstrates:

✅ Stateful application deployment
✅ Stateless application deployment
✅ Secrets management
✅ Persistent storage
✅ Helm templating
✅ Kubernetes networking
✅ Ingress configuration

---
