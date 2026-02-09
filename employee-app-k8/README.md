

---
employee-app-k8/
├── flask/
│   ├── flask-deployment.yaml
│   └── flask-service.yaml       # NEW: Service for Flask app
├── mysql/
│   ├── mysql-deployment.yaml
│   ├── mysql-initdb-configmap.yaml
│   └── mysql-service.yaml       # NEW: Service for MySQL
├── pv-pvc/
│   └── mysql-pvc.yaml
├── secrets/
│   └── mysql-secret.yaml
├── namespaces/
│   └── emp-app-namespace.yaml
├── README.md


## **Step 0 — Prerequisites**

* Install **Minikube**, **kubectl**, **Docker**.
* Start Minikube:

```bash
minikube start
```
```bash
 cd employee-app-k8

```
* Create namespace for the app:
```bash
kubectl apply -f namespaces/namespace.yaml
kubectl get ns
```

---

## **Step 1 — Clean up previous deployments**

If anything is running from old deployments:

```bash
kubectl delete deployment flask-app mysql -n emp-app
kubectl delete service flask-service mysql -n emp-app
kubectl delete secret mysql-secret -n emp-app
kubectl delete configmap mysql-initdb -n emp-app
kubectl delete pvc mysql-pvc -n emp-app
```

Check everything is deleted:

```bash
kubectl get all -n emp-app
kubectl get pvc -n emp-app
```

---

## **Step 2 — Apply Secrets**

* File: `secrets/mysql-secret.yaml`


Apply:

```bash
kubectl apply -f secrets/mysql-secret.yaml -n emp-app
kubectl get secret -n emp-app
```

**Common Error:**

* `unchanged` → means secret already exists, no problem.

---

## **Step 3 — Apply ConfigMap (MySQL init)**

* File: `mysql/init-configmap.yaml`



Apply:

```bash
kubectl apply -f mysql/init-configmap.yaml -n emp-app
kubectl get configmap -n emp-app
```

---

## **Step 4 — Apply PVC**

* File: `pv-pvc/mysql-pv-pvc.yaml`


Apply:

```bash
kubectl apply -f pv-pvc/mysql-pv-pvc.yaml -n emp-app
kubectl get pvc -n emp-app
```

**Common Error:**

* If PVC shows `Pending` → no PV available → fix storage class or delete & reapply PVC.

---

## **Step 5 — Apply MySQL Deployment**

* File: `mysql/mysql-deployment.yaml`

Apply:

```bash
kubectl apply -f mysql/mysql-deployment.yaml -n emp-app
kubectl get pods -n emp-app -w
```

**Common Error:**

* Pod stuck in `Pending` → usually PVC missing (Step 4).

Check logs:

```bash
kubectl logs <mysql-pod> -n emp-app
```

---

## **Step 6 — Apply Flask Deployment**

* File: `flask/flask-deployment.yaml`


Apply:

```bash
kubectl apply -f flask/flask-deployment.yaml -n emp-app
kubectl get pods -n emp-app
kubectl logs -f <flask-pod-name> -n emp-app
```

**Common Error:**

* `Waiting for MySQL... 1045 (28000)` → Secret mismatch
* `500 Internal Server Error` → Flask cannot connect to DB

---

## **Step 7 — Expose Flask Service**

```bash
kubectl expose deployment flask-app \
  --type=NodePort \
  --name=flask-service \
  --port=5000 \
  -n emp-app
kubectl get svc -n emp-app
```

Access Flask app:

```bash
minikube service flask-service -n emp-app
```

---

## **Step 8 — Test Flask App**

### **POST /employees**

```bash
curl -X POST http://<minikube-ip>:<nodeport>/employees \
-H "Content-Type: application/json" \
-d '{"name": "Ankita", "role": "Developer"}'
```

### **GET /employees**

```bash
curl http://<minikube-ip>:<nodeport>/employees
```

✅ You should see the employee data.

---

## **Common Errors & Fixes**

| Error              | Cause                         | Fix                                        |
| ------------------ | ----------------------------- | ------------------------------------------ |
| Pod Pending        | PVC missing                   | Create PVC (Step 4)                        |
| 1045 Access denied | Secret values mismatch        | Update `mysql-secret.yaml` and reapply     |
| Flask 500 error    | Flask cannot connect to MySQL | Check env vars, MySQL pod logs             |
| Service not found  | Service not created           | Use `kubectl expose` or apply service YAML |

---

This documentation covers **everything** from scratch:

* Create namespace → secrets → configmap → PVC → MySQL → Flask → Service → test endpoints.

---

If you want, I can also **prepare a ready-to-download PDF** of this documentation with **screenshots of commands and logs** so you can share it or keep it as a reference.

Do you want me to do that?
