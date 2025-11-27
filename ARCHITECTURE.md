# 🏗️ Architecture Détaillée

## Vue d'ensemble

Ce projet suit les principes de **Clean Architecture** avec une séparation claire des responsabilités en 4 couches principales:

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
│  Endpoints → Routers → Dependencies (Dependency Injection)   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Service Layer                             │
│     Business Logic · Orchestration · Validation              │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Repository Layer                            │
│     Data Access · MongoDB Operations · Query Logic           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   Database (MongoDB)                         │
│                  Persistent Storage                          │
└─────────────────────────────────────────────────────────────┘
```

## Structure des Fichiers

```
app/
├── __init__.py
├── main.py                          # 🚀 Entry point FastAPI
│
├── api/                             # 🌐 API Layer
│   ├── __init__.py
│   ├── dependencies/                # Dependency Injection
│   │   └── __init__.py              # get_*_service, get_*_repository
│   └── v1/                          # API Version 1
│       ├── __init__.py
│       ├── routers/                 # Route organization
│       │   ├── __init__.py
│       │   └── example_router.py    # Group endpoints by domain
│       └── endpoints/               # HTTP endpoints
│           ├── __init__.py
│           └── example_endpoint.py  # CRUD operations
│
├── core/                            # ⚙️ Core Configuration
│   ├── __init__.py
│   ├── config.py                    # Settings (Pydantic)
│   ├── database.py                  # DB connection management
│   ├── logging.py                   # Structured logging
│   └── exceptions.py                # Custom exceptions + handlers
│
├── services/                        # 💼 Business Logic Layer
│   ├── __init__.py
│   └── example_service.py           # Business rules & orchestration
│
├── repositories/                    # 🗄️ Data Access Layer
│   ├── __init__.py
│   └── example_repository.py        # MongoDB CRUD operations
│
└── models/                          # 📋 Data Models
    ├── __init__.py
    └── example_model.py             # Pydantic models (DTOs)
```

## Flux de Données Détaillé

### 1. Request Flow (Création d'un exemple)

```
┌─────────────┐
│   Client    │
│  HTTP POST  │
└──────┬──────┘
       │ POST /api/v1/examples
       │ Body: {"name": "test"}
       ▼
┌─────────────────────────────────────────────────┐
│  API Layer - example_endpoint.py                │
│  @router.post("")                               │
│  • Reçoit ExampleCreate (Pydantic validation)  │
│  • Injecte ExampleService via Depends()         │
└──────┬──────────────────────────────────────────┘
       │ service.create_example(example)
       ▼
┌─────────────────────────────────────────────────┐
│  Service Layer - example_service.py             │
│  • Logique métier (logging, validation)        │
│  • Orchestration des opérations                │
└──────┬──────────────────────────────────────────┘
       │ repository.create(example)
       ▼
┌─────────────────────────────────────────────────┐
│  Repository Layer - example_repository.py       │
│  • Génère UUID                                  │
│  • Ajoute timestamps                            │
│  • Exécute collection.insert_one()             │
└──────┬──────────────────────────────────────────┘
       │ MongoDB async operation
       ▼
┌─────────────────────────────────────────────────┐
│  MongoDB Atlas                                  │
│  • Stockage persistant                         │
│  • Retourne document créé                      │
└──────┬──────────────────────────────────────────┘
       │
       ▼
    Response
```

### 2. Dependency Injection Flow

```
FastAPI Request
    ↓
get_example_service()
    ↓
    └─> Depends(get_example_repository)
            ↓
            └─> Depends(get_database)
                    ↓
                    └─> Returns AsyncIOMotorDatabase
                        ↓
                    ExampleRepository instantiated
                    ↓
                ExampleService instantiated
                ↓
            Injected in endpoint
```

## Couches Détaillées

### 🌐 API Layer (`app/api/`)

**Responsabilité:** Gérer les requêtes HTTP et les réponses

**Composants:**
- **Endpoints** (`endpoints/`): Fonctions qui reçoivent les requêtes HTTP
- **Routers** (`routers/`): Regroupent les endpoints par domaine
- **Dependencies** (`dependencies/`): Gère l'injection de dépendances

**Règles:**
- ✅ Validation des données d'entrée (Pydantic)
- ✅ Sérialisation des réponses
- ✅ Gestion des status codes HTTP
- ❌ PAS de logique métier
- ❌ PAS d'accès direct à la DB

### 💼 Service Layer (`app/services/`)

**Responsabilité:** Implémenter la logique métier

**Composants:**
- Services métier qui orchestrent les opérations

**Règles:**
- ✅ Logique métier complexe
- ✅ Validation business rules
- ✅ Orchestration de plusieurs repositories
- ✅ Logging des opérations importantes
- ❌ PAS de dépendance à FastAPI (Request, Response, etc.)
- ❌ PAS d'accès direct à MongoDB

### 🗄️ Repository Layer (`app/repositories/`)

**Responsabilité:** Abstraction de l'accès aux données

**Composants:**
- Repositories qui interagissent avec MongoDB

**Règles:**
- ✅ CRUD operations
- ✅ Queries MongoDB
- ✅ Gestion des erreurs DB
- ✅ Transformation DB ↔ Models
- ❌ PAS de logique métier
- ❌ PAS de validation business

### 📋 Models Layer (`app/models/`)

**Responsabilité:** Définir les structures de données

**Composants:**
- Pydantic models pour validation

**Types de Models:**
- **Base**: Champs communs partagés
- **Create**: Pour créer une nouvelle entité
- **Update**: Pour mettre à jour (champs optionnels)
- **InDB**: Représentation en base (avec id, timestamps)
- **Response**: Pour les réponses API

### ⚙️ Core Layer (`app/core/`)

**Responsabilité:** Configuration et utilitaires transversaux

**Composants:**
- **config.py**: Configuration centralisée (Settings)
- **database.py**: Gestion connexion MongoDB
- **logging.py**: Configuration logging structuré
- **exceptions.py**: Exceptions personnalisées + handlers

## Principes SOLID Appliqués

### 1. Single Responsibility Principle (SRP)

Chaque module a UNE seule raison de changer:

```python
# ✅ CORRECT
class ExampleRepository:
    """Responsabilité: Accès aux données UNIQUEMENT"""
    async def create(self, example: ExampleCreate) -> ExampleInDB:
        # Seulement des opérations MongoDB
        pass

class ExampleService:
    """Responsabilité: Logique métier UNIQUEMENT"""
    async def create_example(self, example: ExampleCreate) -> ExampleResponse:
        # Validation business, logging, orchestration
        pass
```

### 2. Open/Closed Principle (OCP)

Ouvert à l'extension, fermé à la modification:

```python
# ✅ Ajouter un nouveau service SANS modifier l'existant
class NewFeatureService:
    """Nouveau service pour nouvelle fonctionnalité"""
    def __init__(self, repository: NewFeatureRepository):
        self.repository = repository
    
    async def new_operation(self):
        # Nouvelle logique sans toucher ExampleService
        pass
```

### 3. Liskov Substitution Principle (LSP)

Les abstractions sont substituables:

```python
# ✅ Repository peut être remplacé par un mock ou une autre implémentation
class MockRepository(ExampleRepository):
    """Mock pour les tests - même interface"""
    async def create(self, example: ExampleCreate) -> ExampleInDB:
        # Implementation de test
        return ExampleInDB(...)
```

### 4. Interface Segregation Principle (ISP)

Petites interfaces spécifiques:

```python
# ✅ Service ne dépend QUE du repository dont il a besoin
class ExampleService:
    def __init__(self, repository: ExampleRepository):
        # Pas de dépendance à un "god object"
        self.repository = repository
```

### 5. Dependency Inversion Principle (DIP)

Dépendre des abstractions, pas des implémentations:

```python
# ✅ Service reçoit repository via injection (abstraction)
# Pas d'instanciation directe dans le service
async def get_example_service(
    repository: Annotated[ExampleRepository, Depends(get_example_repository)]
) -> ExampleService:
    return ExampleService(repository)
```

## Configuration & Environment

### Settings Hierarchy

```
1. Environment Variables (.env file)
   ↓
2. Pydantic Settings (validation + type conversion)
   ↓
3. get_settings() - Singleton cached
   ↓
4. settings imported throughout the app
```

### Database Connection Management

```python
# Lifespan events in main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ↓ Startup: Initialize connection pool
    database.mongo_client = AsyncIOMotorClient(...)
    
    yield  # ← Application running
    
    # ↓ Shutdown: Close connections
    database.mongo_client.close()
```

## Testing Strategy

### Unit Tests

```python
# Test Service avec Mock Repository
class MockExampleRepository:
    async def create(self, example):
        return ExampleInDB(id="test-123", **example.dict())

def test_create_example():
    mock_repo = MockExampleRepository()
    service = ExampleService(mock_repo)
    result = await service.create_example(ExampleCreate(name="test"))
    assert result.name == "test"
```

### Integration Tests

```python
# Test Endpoint avec TestClient
from fastapi.testclient import TestClient

def test_create_example_endpoint():
    client = TestClient(app)
    response = client.post(
        "/api/v1/examples",
        json={"name": "test", "is_active": True}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "test"
```

## Extension du Template

### Ajouter une Nouvelle Entité (ex: User)

**1. Créer le Model**
```bash
touch app/models/user_model.py
```

**2. Créer le Repository**
```bash
touch app/repositories/user_repository.py
```

**3. Créer le Service**
```bash
touch app/services/user_service.py
```

**4. Créer les Endpoints**
```bash
touch app/api/v1/endpoints/user_endpoint.py
touch app/api/v1/routers/user_router.py
```

**5. Ajouter les Dependencies**
```python
# Dans app/api/dependencies/__init__.py
def get_user_repository(
    database: Annotated[AsyncIOMotorDatabase, Depends(get_database)]
) -> UserRepository:
    return UserRepository(database)

def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    return UserService(repository)
```

**6. Enregistrer le Router**
```python
# Dans app/main.py
from app.api.v1.routers import user_router
app.include_router(user_router.router, prefix=settings.api_v1_prefix)
```

## Bonnes Pratiques

### ✅ DO

- Typer tous les paramètres et retours de fonctions
- Utiliser Depends() pour l'injection
- Logger les opérations importantes dans les services
- Valider les données avec Pydantic
- Utiliser des UUIDs (pas ObjectId MongoDB)
- Documenter les fonctions avec docstrings
- Gérer les exceptions de manière explicite

### ❌ DON'T

- Accéder directement à MongoDB depuis un endpoint
- Mettre de la logique métier dans les endpoints
- Utiliser des variables globales
- Ignorer les erreurs silencieusement
- Hardcoder des valeurs (utiliser settings)
- Mixer les responsabilités des couches

---

**Cette architecture garantit:**
- 🔧 Maintenabilité
- 🧪 Testabilité
- 📈 Scalabilité
- 🔄 Évolutivité
- 📚 Lisibilité
