## Pet-project
[Entity Relationship Diagram](https://dbdiagram.io/d/61f53b7085022f4ee50e4469)
### Running locally
#### Env files:
dbdev.yml
```yaml
echo: True
db:
  type: "sqlite"
  path: "dev_db.db"
```
api.yml
```yaml
title: "API"
version: "1.0.0"

jwt_secret: ""
jwt_algorithm: "HS256"
access_token_expire_minutes: 3600

cors_origins:
  - "http://localhost"
  - "https://my-domain.com"
```

#### Migrations:
```bash
alembic upgrade head
```

#### Run:
```bash
python asgi.py
```
