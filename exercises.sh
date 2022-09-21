#!/bin/bash
docker run --network=host -v $(pwd)/rootfiles:/home/physicist/rootfiles --env="DISPLAY" -it ammitra/timber-docker:latest
