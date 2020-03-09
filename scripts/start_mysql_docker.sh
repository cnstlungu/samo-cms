#!/usr/bin/env bash

docker run -p 33060:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=$SAMO_DB_PASS -d mysql:latest