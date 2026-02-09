# Employee App Kubernetes Deployment

## 1. Create Namespace
kubectl apply -f namespaces/namespace.yaml

## 2. Create Secrets
kubectl apply -f secrets/mysql-secret.yaml

## 3. Create PV + PVC
kubectl apply -f pv-pvc/mysql-pv-pvc.yaml

## 4. Deploy MySQL
kubectl apply -f mysql/mysql-deployment.yaml
kubectl apply -f mysql/mysql-service.yaml

## 5. Deploy Flask App
kubectl apply -f flask/flask-deployment.yaml
kubectl apply -f flask/flask-service.yaml

## 6. Verify
kubectl get pods -n emp-app
kubectl get pvc -n emp-app
kubectl get svc -n emp-app

## 7. Access Flask App in browser (Minikube)
minikube service flask-service -n emp-app
