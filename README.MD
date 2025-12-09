# 🚀 DevOps Demo: FastAPI, PostgreSQL ve Kubernetes

Bu depo, bir Python FastAPI uygulamasının **PostgreSQL** veritabanı ile entegre edilerek **Kubernetes (K8s)** üzerinde dağıtımını (deployment) göstermektedir. Proje, bir `db-count` (veritabanı sayacı) ve basit bir `hello` API işlevine sahiptir.

## 🌟 Proje Mimarisi

* **Uygulama:** Python FastAPI (Uygulama dosyaları: `./app` klasörü)
    * API Endpointleri: `/hello` (Hello World) ve `/db-count` (Veritabanında gelen istek sayısını döndürür)
* **Veritabanı:** PostgreSQL
* **Konteynerleştirme:** Docker
* **Orkestrasyon:** Kubernetes (Dağıtım, Servis, PVC, Secret vb. K8s manifestoları: `./k8s` klasörü)
* **Giriş Kontrolü:** Nginx Ingress Controller

## 🛠️ Önkoşullar

Bu projeyi yerel ortamınızda çalıştırmak için aşağıdaki araçlara ihtiyacınız vardır:

* **Docker**
* **kubectl** (Kubernetes komut satırı aracı)
* **Bir Kubernetes Ortamı** (Yerel Docker Desktop K8s)

---

## ⚙️ Kurulum ve Çalıştırma Adımları

Aşağıdaki adımlar, FastAPI uygulamasını Docker imajı olarak oluşturmayı, Kubernetes ortamını yapılandırmayı ve uygulamayı dağıtmayı içerir.

### 1. Docker İmajını Oluşturma

Uygulamanın Docker imajını oluşturun.

```bash
cd app
docker build -t devops-demo-fastapi:latest ./app
```
### 2. Nginx Ingress Controller Kurulumu

Uygulamaya dışarıdan erişimi sağlamak için Nginx Ingress Controller'ı Kubernetes kümenize kurun.

Ingress Controller'ı kurma
```bash
kubectl apply -f [https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.1/deploy/static/provider/cloud/deploy.yaml](https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.1/deploy/static/provider/cloud/deploy.yaml)
```
Kurulum durumunu kontrol etme
```bash
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```
### 3. Kubernetes Kaynaklarını Dağıtma

Uygulamanın çalışması için gerekli olan Namespace, Secret, PostgreSQL ve FastAPI kaynaklarını sırayla uygulayın.
Namespace, Secret ve PVC oluşturma
```bash
cd ..
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres-pvc.yaml
```
PostgreSQL Veritabanını dağıtma
```bash
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
```
FastAPI Uygulamasını dağıtma
```bash
kubectl apply -f k8s/app-deployment.yaml
kubectl apply -f k8s/app-service.yaml
kubectl apply -f k8s/ingress.yaml
```
### 4. Pod'ların durumunu kontrol etme
```bash
kubectl get pods -n devops-demo
```
### 5. Uygulamaya Yerel Erişim (Port Forwarding)

Uygulama servisine doğrudan erişmek ve test etmek için port yönlendirme (Port Forwarding) kullanın.
```bash
kubectl port-forward -n devops-demo svc/fastapi-svc 8000:80

# Hello 
curl http://localhost:8000/hello

# db-count 
curl http://localhost:8000/db-count

```
### 6. Her şeyi silmek için aşağıdaki komutları kullanın.
```bash
kubectl delete deployment fastapi -n devops-demo
kubectl delete deployment postgres -n devops-demo
kubectl delete ingress fastapi-ingress -n devops-demo
kubectl delete pvc pg-pvc -n devops-demo
kubectl delete svc fastapi-svc -n devops-demo
kubectl delete svc postgres -n devops-demo
kubectl delete namespace devops-demo
kubectl delete namespace ingress-nginx
```
