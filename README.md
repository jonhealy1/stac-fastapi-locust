# stac-fastapi-locust
Locust load balancing for stac-fastapi


## Run stac-fastapi pgstac 
```$ docker-compose build```   
```$ docker-compose up```

## Ingest test data
```$ make ingest```

## Install
```$ pip install -e .```

## Start Locust
```$ locust```

## Run Locust Load Balancing   
- go to ```http://localhost:8089``` and start with desired settings
- for testing locally from docker-compose in this repo, set Host to: ```http://localhost:8083```

## Run Taurus Load Balancing
```$ bzt taurus_locust.yml```

## References  
  
- https://betterprogramming.pub/introduction-to-locust-an-open-source-load-testing-tool-in-python-2b2e89ea1ff
