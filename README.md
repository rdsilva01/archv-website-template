# `archv` Website Template
This repository provides a template for setting up a Flask-based website with a Redis database backend. This template is designed to work as part of the [archv package](https://github.com/rdsilva01/archv). for reconstructing and archiving news content.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Requirements
- Docker

## Installation
1. Clone the repository
```bash
git clone https://github.com/rdsilva01/archv-website-template.git
cd archv-website-template
```

## Configuration
This project uses Docker Compose to run all services, including Redis, Flask, and Nginx. Follow these steps to configure and start each service.

1. Edit the `docker-compose.yml` file, specifying the correct Redis path, from where was it cloned:
```bash
   device: '/.../archv/redis/redis_dir'  # <-- Replace this with your own path
```

2. To start `redis`, go to the `redis_module` directory run:
```bash
docker-compose up -d
```
This will pull the `redis` image, start the container in the ports 6379 and 8001 and mount a volume `/data` for the data.

3. To start the `nginx` and the website, go to the `website` directory and then run:
```bash
docker-compose up -d
```
This will start the `nginx` container, which proxies the requests to the `Flask` app.

## Usage
The `redis` interface is accessible via browser, on `http://localhost:8001`.
The website is accessible via browser, on `http://localhost:90/demo`

## Troubleshooting
- **Network Issues**: Make sure the `redis_redis-network` network is created as an external network. To confirm, run `docker network l`, or create it manually with:
```bash
docker network create redis_redis-network
```


