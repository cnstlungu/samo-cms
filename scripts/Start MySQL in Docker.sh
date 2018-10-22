#!/usr/bin/env bash

docker run -p 3306:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=$SAMO_DB_PASS -d mysql:latest