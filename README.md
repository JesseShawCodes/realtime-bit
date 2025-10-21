# Real Time Data App

Application can be started up using Dokcer

```
docker-compose up
```

## Other useful commands

To start fast api from src

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload      
```

To initialize Database

```
python3 -m src.init_db
```


To run_pipeline

```
python3 -m src.run_pipeline
```
