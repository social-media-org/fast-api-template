# ⚡ Quick Start Guide

Guide rapide pour démarrer avec le template FastAPI Clean Architecture.

## 🚀 Démarrage en 5 Minutes

### 1. Configuration MongoDB Atlas

```bash
# Visitez https://www.mongodb.com/cloud/atlas
# 1. Créez un compte gratuit
# 2. Créez un cluster (Free tier M0)
# 3. Database Access → Add New User
#    - Username: votre_user
#    - Password: votre_password (notez-le!)
# 4. Network Access → Add IP Address → Allow Access from Anywhere (0.0.0.0/0)
# 5. Connect → Connect your application → Copy connection string
```

### 2. Configuration Projet

```bash
# Cloner et installer
git clone <repo-url>
cd <project-name>
pip install -r requirements.txt

# Configurer .env
cp .env.example .env
nano .env  # Éditer MONGODB_URL avec votre connection string
```

**Exemple .env:**
```env
MONGODB_URL=mongodb+srv://myuser:mypassword@cluster0.xxxxx.mongodb.net/
MONGODB_DATABASE=fastapi_db
DEBUG=true
```

### 3. Lancer l'Application

```bash
# Option 1: Makefile (recommandé)
make run

# Option 2: Uvicorn direct
uvicorn app.main:app --reload

# Option 3: Docker
docker-compose up
```

### 4. Tester l'API

Ouvrez votre navigateur: **http://localhost:8000/docs**

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Créer un exemple
```bash
curl -X POST http://localhost:8000/api/v1/examples \
  -H "Content-Type: application/json" \
  -d '{"name": "Mon premier exemple", "description": "Test API", "is_active": true}'
```

#### Lister les exemples
```bash
curl http://localhost:8000/api/v1/examples
```

## 📝 Commandes Utiles

```bash
# Développement
make run              # Lancer l'app (hot reload)
make format           # Formatter le code
make lint             # Vérifier le code
make type-check       # Vérifier les types
make clean            # Nettoyer les caches

# Docker
make run-docker       # Lancer avec Docker
make stop             # Arrêter Docker

# Installation
make install          # Installer les dépendances
make dev              # Setup environnement complet
```

## 🔧 Personnaliser le Template

### Renommer "Example" par votre Entité

```bash
# Exemple: Créer une entité "Product"

# 1. Copier les fichiers exemple
cp app/models/example_model.py app/models/product_model.py
cp app/repositories/example_repository.py app/repositories/product_repository.py
cp app/services/example_service.py app/services/product_service.py
cp app/api/v1/endpoints/example_endpoint.py app/api/v1/endpoints/product_endpoint.py
cp app/api/v1/routers/example_router.py app/api/v1/routers/product_router.py

# 2. Éditer chaque fichier:
# - Remplacer "Example" par "Product"
# - Remplacer "example" par "product"
# - Adapter les champs du model

# 3. Ajouter les dependencies
# Dans app/api/dependencies/__init__.py
# Ajouter get_product_repository() et get_product_service()

# 4. Enregistrer le router
# Dans app/main.py
# app.include_router(product_router.router, prefix=settings.api_v1_prefix)
```

## 🧪 Tests Rapides

### Vérifier les Imports

```bash
python -c "from app.main import app; print('✅ OK')"
```

### Vérifier les Types

```bash
mypy app/
```

### Tester un Endpoint

```python
# test_quick.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# Run: pytest test_quick.py
```

## 🐛 Troubleshooting

### Erreur: MongoDB Connection Failed

```bash
# Vérifier votre connection string
echo $MONGODB_URL

# Tester la connexion
python -c "from pymongo import MongoClient; client = MongoClient('YOUR_URL'); print(client.server_info())"
```

### Erreur: Module not found

```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur: Port 8000 déjà utilisé

```bash
# Trouver le process
lsof -i :8000

# Tuer le process
kill -9 <PID>

# OU utiliser un autre port
uvicorn app.main:app --reload --port 8001
```

## 📖 Prochaines Étapes

1. **Lire l'architecture:** `ARCHITECTURE.md`
2. **Personnaliser les models:** `app/models/`
3. **Ajouter votre logique:** `app/services/`
4. **Créer vos endpoints:** `app/api/v1/endpoints/`
5. **Configurer la prod:** Dockerfile & .env

## 🔗 Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Motor](https://motor.readthedocs.io/)
- [Pydantic](https://docs.pydantic.dev/)
- [Docker Compose](https://docs.docker.com/compose/)

---

**Besoin d'aide?** Consultez `README.md` et `ARCHITECTURE.md` pour plus de détails!
