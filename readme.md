# dockercompose-guacamole-for-msp-remoteadmin

## Overview
This project is an adapted version of Docker Compose for use with the MSP Remoteadmin application, based on Apache Guacamole. It provides a solution for remote administration with web-based access to desktops and servers.

The image was adapted to provide a service for automating connections made by Frappe through the [MSP Remoteadmin](https://github.com/itsdave-de/msp_remoteadmin) application

For this, the Guacamole [AD-Hoc extension](https://guacamole.apache.org/doc/gug/adhoc-connections.html) was used (which does not come in the default image of the Guacamole project)

## Requirements

- Docker
- Docker Compose
- Git
- Debian 12

## Repository structure

- **docker-compose.yml**: File that defines the services that will be used in the project
- **docker-guacamole-custom**: Folder that contains the Dockerfile and the configuration files for the Guacamole service
- **docker-monitor**: Folder that contains the Dockerfile and the configuration files for the Monitor service

## Monitor Service

The Monitor service is a simple script written in Python that monitors the Guacamole GUACD logging and filter informations about the connections made by the MSP Remoteadmin application and sends them to the Frappe application for historical purposes and auditing.

#### Monitor Service Configuration

```yaml
  monitor_service:
    container_name: monitor_service
    build: ./docker-monitor
    restart: unless-stopped
    environment:
      FRAPPE_URL: "https://frappe.website.com" # You need to change this to your Frappe URL
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - guacd
```

## Installation

1. Clone the repository
```bash
git clone https://git.labexposed.com/itsdave/dockercompose-guacamole-for-msp-remoteadmin.git
cd dockercompose-guacamole-for-msp-remoteadmin
```

2. Grab the latest sql info from the latest images
```bash
docker run --rm guacamole/guacamole:1.5.5 /opt/guacamole/bin/initdb.sh --mysql > initdb.sql
```

3. Run the composer file with DB configuration to initialize the database
```bash
docker-compose -f composer-db.yml up -d
```

4. Next you need to copy the SQL file into the docker database container and load the file into the MariaDB database
```bash
docker cp initdb.sql guacamole_db:/initdb.sql
docker exec -i guacamole_db mysql -u root -p"$MYSQL_ROOT_PASSWORD" guacamole_db < /initdb.sql
```

5. Turn off the database container
```bash
docker-compose -f composer-db.yml down -v
```

6. Now you can start the services
```bash
docker-compose up --build -d
```

## How do I access Guacamole?
Very simple just open your browser and put in your Guacamole IP with port 8080

For example: http://mylocalip.home:8080/guacamole <- guacamole cant be access via root directory, so you will have to add /guacamole.

The original username/password are guacadmin/guacadmin

