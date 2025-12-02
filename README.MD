# Project Scraping crmv.gov.br

Flask API para consulta de registros CRMV usando web scraping.

## Instalação Local

### Requirements for Ubuntu

Install Chromium Browser
```bash
sudo apt update && sudo apt install chromium-browser
```

and XDG-UTILS
```bash
sudo apt install xdg-utils
```

### Install
```bash
pip install -r requirements.txt
```

### Run
```bash
python app.py
```

## Unit Test

```bash
pip install -r requirements.txt && pytest
```

## Docker (Recomendado)

### Build e execução
```bash
docker-compose up --build
```

### Execução em background
```bash
docker-compose up -d
```

### Parar serviços
```bash
docker-compose down
```

### API Endpoints
- `GET /` - Hello World
- `GET /api/health` - Health check
- `GET /api/crmv/<numero>/<estado>` - Buscar CRMV por número e estado
- `GET /apidocs/` - Documentação Swagger da API
