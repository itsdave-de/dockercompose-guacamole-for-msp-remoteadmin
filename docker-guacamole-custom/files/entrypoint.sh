#!/bin/bash

/opt/guacamole/bin/start.sh &

# Wait for Tomcat to be fully initialized
while ! curl -sSf http://localhost:8080/guacamole >/dev/null; do
  echo "Waiting for Tomcat to start..."
  sleep 2
done

# Run the additional script
/opt/guacamole/bin/inject-trigger.sh

# Keep the container running
wait

