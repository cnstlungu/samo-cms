#!/usr/bin/env bash

docker run -p 3306:3306 --name some-mysql -e MYSQL_ROOT_PASSWORD=[password here] -d mysql:latest