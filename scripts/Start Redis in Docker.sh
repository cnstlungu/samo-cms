#!/usr/bin/env bash
docker run --name redis -p 6379:6379 --network samo-network -d redis