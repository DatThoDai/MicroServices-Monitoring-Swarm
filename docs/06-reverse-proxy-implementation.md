# Chapter 6: Reverse Proxy Implementation with Nginx

## Overview

This chapter details the implementation of Nginx as a Reverse Proxy for the MrNamCoinSwarm system. The Reverse Proxy plays a crucial role in ensuring that client requests are accurately routed to microservices such as Prometheus, Grafana, Kibana, and DockerCoins services (rng, hasher, webui), while providing features like load balancing and security.

## 6.1 Network Setup for Reverse Proxy

### Creating Proxy Network
Create an overlay network for Nginx to communicate with all services:

```bash
sudo docker network create --driver overlay --attachable proxy
```

### Network Benefits
This network enables Nginx to communicate with services across different networks:
- **monitoring**: Prometheus, Grafana, InfluxDB
- **loggingnet**: ELK Stack components
- **coinswarmnet**: DockerCoins services

## 6.2 Nginx Configuration

### Main Configuration File (nginx.conf)

**[IMG-21: Nginx Main Configuration]**
*Location in original text: "nginx.conf: Định nghĩa cấu hình chính của Nginx (có hình)"*

![Nginx Configuration](../assets/21-nginx-config.png)

Create the primary Nginx configuration:

```nginx
user nginx;
worker_processes 1;

error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    keepalive_timeout 65;

    include /etc/nginx/conf.d/*.conf;
}
```

#### Configuration Breakdown
- **User Security**: Runs with nginx user for security
- **Worker Processes**: Single worker for development environment (use `auto` for production)
- **Logging**: Comprehensive access and error logging
- **Connections**: Supports up to 1024 concurrent connections per worker
- **HTTP Settings**: Standard HTTP configuration with MIME types

### Routing Configuration (default.conf)

**[IMG-22: Nginx Routing Configuration]**
*Location in original text: "Routing rules cho services (có hình)"*

![Nginx Routing Configuration](../assets/22-nginx-routing.png)

Create the routing rules for services:

```nginx
server {
    listen 80;
    server_name localhost;

    # Prometheus routing
    location /prometheus/ {
        proxy_pass http://tasks.prometheus:9090/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Grafana routing
    location /grafana/ {
        proxy_pass http://tasks.grafana:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Kibana routing
    location /kibana/ {
        proxy_pass http://tasks.kibana:5601/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # DockerCoins WebUI routing
    location /webui/ {
        proxy_pass http://tasks.webui:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # RNG service routing
    location /rng/ {
        proxy_pass http://tasks.rng:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Hasher service routing
    location /hasher/ {
        proxy_pass http://tasks.hasher:8002/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Node Exporter metrics routing
    location /metrics/ {
        proxy_pass http://tasks.node-exporter:9100/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Default location
    location / {
        return 200 'MrNamCoinSwarm Reverse Proxy - Services Available at /prometheus/, /grafana/, /kibana/, /webui/, /rng/, /hasher/, /metrics/';
        add_header Content-Type text/plain;
    }
}
```

#### Routing Strategy
- **Path-based Routing**: Uses URL paths to route to different services
- **Service Discovery**: Utilizes `tasks.<service_name>` for Swarm service discovery
- **Header Forwarding**: Preserves client information for backend services
- **Load Balancing**: Automatic distribution across service replicas

#### Service Endpoints
- **/prometheus/**: Routes to Prometheus monitoring interface
- **/grafana/**: Routes to Grafana dashboards
- **/kibana/**: Routes to Kibana log analysis
- **/webui/**: Routes to DockerCoins web interface
- **/rng/**: Routes to Random Number Generator API
- **/hasher/**: Routes to Hasher computation service
- **/metrics/**: Routes to Node Exporter metrics

### Benefits of This Configuration
1. **Accurate Routing**: Service discovery ensures flexible routing even when containers move
2. **Port Consolidation**: All services accessible through port 80
3. **Scalability**: Easy addition of new services by adding location blocks
4. **Transparency**: Backend services receive proper client information

## 6.3 Docker Configuration Creation

Convert configuration files to Docker configs:

```bash
# Create nginx.conf Docker config
sudo docker config create nginx_conf nginx.conf

# Create default.conf Docker config
sudo docker config create default_conf default.conf
```

## 6.4 Nginx Service Deployment

**[IMG-23: Nginx Service Deployment Result]**
*Location in original text: "Deploy Nginx service với multi-network (có hình)"*

![Nginx Deployment](../assets/23-nginx-deployment.png)

Deploy the Nginx service with multi-network connectivity:

```bash
sudo docker service create \
  --name nginx \
  --config source=nginx_conf,target=/etc/nginx/nginx.conf \
  --config source=default_conf,target=/etc/nginx/conf.d/default.conf \
  --network proxy \
  --network monitoring \
  --network loggingnet \
  --network coinswarmnet \
  --publish published=80,target=80 \
  nginx:latest
```

### Deployment Features
- **Multi-Network**: Connected to all service networks
- **Configuration Management**: Uses Docker configs for file management
- **Port Publishing**: Accessible on port 80 from any cluster node
- **Routing Mesh**: Swarm automatically routes requests to Nginx container

## 6.5 Verification and Testing

### Service Status Check

**[IMG-24: Nginx Service Status]**
*Location in original text: "Kiểm tra trạng thái Nginx service (có hình)"*

![Nginx Service Status](../assets/24-nginx-service-status.png)

Verify Nginx deployment:

```bash
sudo docker service ls | grep nginx
sudo docker service ps nginx
```

### Network Connectivity Verification

**[IMG-25: Network Inspection Results]**
*Location in original text: "Kiểm tra network connections (có hình)"*

![Network Inspection](../assets/25-network-inspection.png)

Check network connections:

```bash
sudo docker network inspect proxy
```

This should show Nginx and all connected services in the network.

### Endpoint Testing
Test routing functionality:

```bash
# Test Prometheus access
curl http://192.168.10.91/prometheus/

# Test Grafana access
curl http://192.168.10.91/grafana/

# Test Kibana access
curl http://192.168.10.91/kibana/

# Test WebUI access
curl http://192.168.10.91/webui/

# Test RNG service
curl http://192.168.10.91/rng/

# Test Hasher service
curl http://192.168.10.91/hasher/

# Test metrics endpoint
curl http://192.168.10.91/metrics/
```

### Expected Results

**[IMG-26: Endpoint Testing Results]**
*Location in original text: "Kết quả test các endpoints (có hình)"*

![Endpoint Testing Results](../assets/26-endpoint-testing.png)

- **/prometheus/**: Returns redirect to `/graph` or Prometheus interface
- **/grafana/**: Returns Grafana login page or interface
- **/kibana/**: Returns Kibana interface or ready status
- **/webui/**: Returns DockerCoins web interface
- **/rng/**: Returns RNG service API response
- **/hasher/**: Returns Hasher service API response
- **/metrics/**: Returns Node Exporter metrics data

## 6.6 Troubleshooting

### Log Analysis
Check Nginx logs for issues:

```bash
sudo docker service logs nginx
```

### Common Issues and Solutions

#### Service Discovery Problems
- **Issue**: Backend services not reachable
- **Solution**: Verify service names and network connectivity
- **Command**: `sudo docker service ls` and `sudo docker network inspect <network>`

#### Routing Issues
- **Issue**: Incorrect path routing
- **Solution**: Check URL patterns in configuration
- **Debug**: Review Nginx access logs for request patterns

#### Load Balancing Problems
- **Issue**: Uneven request distribution
- **Solution**: Verify service replica counts and health
- **Monitor**: Use Grafana dashboards to monitor traffic distribution

### CLI Benefits for Operations
- **Deployment Verification**: Ensures proper Reverse Proxy configuration
- **Issue Detection**: Logs help identify connection or backend service problems
- **Operational Support**: Provides tools for managing and monitoring the Reverse Proxy

## 6.7 Results and Benefits

### Achieved Outcomes
The Nginx Reverse Proxy implementation successfully provides:

1. **Unified Access**: Single entry point (port 80) for all system services
2. **Load Balancing**: Automatic distribution among service replicas
3. **Security**: Hides backend server information from clients
4. **Flexible Routing**: URL-based routing supports easy service management
5. **Swarm Integration**: Seamless integration with Docker Swarm's routing mesh
6. **High Availability**: Swarm ensures proxy availability across cluster nodes

### Operational Benefits
- **Simplified Client Access**: Users only need to remember one port and host
- **Service Abstraction**: Backend changes don't affect client access patterns
- **Centralized Management**: Single point for routing policies and rules
- **Easy Scaling**: New services can be added without client reconfiguration
- **Monitoring Integration**: Centralized access logging and metrics collection

This Reverse Proxy implementation provides a robust foundation for accessing all MrNamCoinSwarm services through a single, well-organized interface.
