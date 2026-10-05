#!/bin/bash

for service in services/data-receiver services/database-handler-in services/database-handler-out services/data-server database
do
    (cd "$service" && uv lock)
done