#!/bin/bash

ssh k6zma@194.146.242.41 << EOF
    cd projects/DiscreteSolver/
    git pull
    docker-compose down
    docker-compose up --build -d
EOF