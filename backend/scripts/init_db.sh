#!/bin/bash
docker-compose exec web flask db init
docker-compose exec web flask db migrate
docker-compose exec web flask db upgrade