#!/bin/bash

/opt/guacamole/bin/start.sh &

# Esperar que o Tomcat esteja totalmente inicializado
while ! curl -sSf http://localhost:8080/guacamole >/dev/null; do
  echo "Aguardando Tomcat iniciar..."
  sleep 2
done

# Executar o script adicional
/opt/guacamole/bin/inject-trigger.sh

# Manter o container em execução
wait

