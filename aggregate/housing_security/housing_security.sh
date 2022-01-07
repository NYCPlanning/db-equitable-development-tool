#!/bin/bash

#Not ready yet, work on developing in remote container first
docker run --rm\
    --network host\
    -v $(pwd)/python:/home/python\
    -w /home/python\
    nycplanning/docker-geosupport:latest bash -c "
      python3 aggregate/housing_security/evictions_by_city_marshalls.py"