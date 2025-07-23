# Chapter 5: Monitoring Stack Deployment

## Overview

This chapter details the deployment of the monitoring infrastructure using Prometheus, InfluxDB, and Grafana. This stack provides comprehensive metrics collection, storage, and visualization for the MrNamCoinSwarm system.

## 5.1 Prometheus Configuration

Prometheus serves as the primary metrics collection and monitoring system.

### Network Setup
Create the monitoring network:

```bash
sudo docker network create --driver overlay --attachable monitoring
```

### Data Persistence
Create volume for Prometheus data:

```bash
sudo docker volume create prometheus_data
```

### Prometheus Configuration File
Create the main Prometheus configuration:

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    dns_sd_configs:
      - names: ['tasks.node-exporter']
        type: 'A'
        port: 9100

  - job_name: 'docker'
    static_configs:
      - targets: ['172.18.0.1:9323']  # Docker host IP

  - job_name: 'cadvisor'
    dns_sd_configs:
      - names: ['tasks.cadvisor']
        type: 'A'
        port: 8080

remote_write:
  - url: "http://influxdb:8086/api/v1/prom/write?db=prometheus&u=admin&p=admin123"

remote_read:
  - url: "http://influxdb:8086/api/v1/prom/read?db=prometheus&u=admin&p=admin123"
```

### Configuration Details

#### Global Settings
- **Scrape Interval**: 15-second intervals for metric collection
- **Evaluation Interval**: 15-second intervals for rule evaluation

#### Scrape Configurations
- **Prometheus**: Self-monitoring of Prometheus service
- **Node Exporter**: System-level metrics from all nodes
- **Docker**: Docker daemon metrics
- **cAdvisor**: Container-level metrics

#### Remote Storage
- **Remote Write**: Send metrics to InfluxDB for long-term storage
- **Remote Read**: Query historical data from InfluxDB

### Docker Configuration Creation
```bash
sudo docker config create prometheus_config prometheus.yml
```

### Node Exporter Deployment
Deploy Node Exporter on all nodes for system metrics:

```bash
sudo docker service create \
  --name node-exporter \
  --mode global \
  --network monitoring \
  --mount type=bind,source=/proc,target=/host/proc,readonly \
  --mount type=bind,source=/sys,target=/host/sys,readonly \
  --mount type=bind,source=/,target=/rootfs,readonly \
  -e HOST_HOSTNAME={{.Node.Hostname}} \
  --publish published=9100,target=9100 \
  prom/node-exporter:latest \
  --path.procfs=/host/proc \
  --path.sysfs=/host/sys \
  --path.rootfs=/rootfs \
  --collector.filesystem.mount-points-exclude="^/(sys|proc|dev|host|etc)($$|/)"
```

#### Node Exporter Features
- **Global Mode**: Runs on every node in the cluster
- **Host Metrics**: Access to host system information
- **Filesystem Monitoring**: Disk usage and filesystem metrics
- **Network Metrics**: Network interface statistics
- **Process Metrics**: System process information

### Prometheus Service Deployment
Deploy the main Prometheus service:

```bash
sudo docker service create \
  --name prometheus \
  --network monitoring \
  --mount type=volume,source=prometheus_data,target=/prometheus \
  --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock \
  --config source=prometheus_config,target=/etc/prometheus/prometheus.yml \
  -p 9090:9090 \
  prom/prometheus:latest \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.console.libraries=/usr/share/prometheus/console_libraries \
  --web.console.templates=/usr/share/prometheus/consoles
```

#### Prometheus Features
- **Time Series Database**: Built-in TSDB for metrics storage
- **Service Discovery**: Automatic discovery of monitored targets
- **Query Language**: PromQL for metric queries and analysis
- **Alert Manager**: Integration for alerting capabilities

## 5.2 InfluxDB Configuration

InfluxDB provides long-term storage for metrics data with efficient time-series optimization.

### Data Persistence
Create volume for InfluxDB data:

```bash
sudo docker volume create influxdb_data
```

### InfluxDB Deployment
Deploy InfluxDB with authentication:

```bash
sudo docker service create \
    --name influxdb \
    --network monitoring \
    --mount type=volume,source=influxdb_data,target=/var/lib/influxdb \
    -e INFLUXDB_DB=prometheus \
    -e INFLUXDB_ADMIN_USER=admin \
    -e INFLUXDB_ADMIN_PASSWORD=admin123 \
    -e INFLUXDB_HTTP_AUTH_ENABLED=true \
    -p 8086:8086 \
    influxdb:1.8
```

### Configuration Details
- **Database**: Pre-created `prometheus` database
- **Authentication**: Admin user with secure credentials
- **HTTP API**: Port 8086 for Prometheus integration
- **Data Retention**: Configurable retention policies

### Database Operations
Access InfluxDB for data queries:

```bash
sudo docker exec -it $(sudo docker ps --filter name=influxdb --format '{{.ID}}') influx
```

#### Common InfluxDB Commands
```sql
-- Show available databases
SHOW DATABASES

-- Use prometheus database
USE prometheus

-- Show all measurements (metric types)
SHOW MEASUREMENTS

-- Query CPU metrics
SELECT mean("value") FROM "node_cpu_seconds_total"
WHERE "mode" = 'user' AND time > now() - 5m
GROUP BY time(1m), "instance";

-- Query memory metrics
SELECT mean("value") FROM "node_memory_Active_bytes"
WHERE time > now() - 5m
GROUP BY time(1m), "instance";

-- Query network metrics
SELECT derivative(mean("value"), 1s) FROM "node_network_receive_bytes_total"
WHERE "device" != 'lo' AND time > now() - 5m
GROUP BY time(1m), "instance", "device";
```

## 5.3 Grafana Configuration

Grafana provides advanced visualization and dashboarding capabilities.

### Data Persistence
Create volume for Grafana data:

```bash
sudo docker volume create grafana_data
```

### Grafana Deployment
Deploy Grafana with custom settings:

```bash
sudo docker service create \
  --name grafana \
  --network monitoring \
  --mount type=volume,source=grafana_data,target=/var/lib/grafana \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin123" \
  -e "GF_USERS_ALLOW_SIGN_UP=false" \
  --publish published=3000,target=3000 \
  grafana/grafana:latest
```

### Configuration Details
- **Admin Access**: Secure admin password
- **User Registration**: Disabled for security
- **Port 3000**: Standard Grafana web interface
- **Data Sources**: Configure Prometheus and InfluxDB connections

## 5.4 Docker Daemon Metrics Configuration

Enable Docker daemon metrics on all nodes:

```bash
sudo nano /etc/docker/daemon.json
```

**[IMG-12: Docker Daemon Configuration]**
*Location in original text: "3.4. Cấu hình Docker daemon trên tất cả các node để expose metrics (có hình)"*

![Docker Daemon Configuration](../assets/12-docker-daemon-config.png)

Add metrics configuration:
```json
{
  "metrics-addr": "0.0.0.0:9323",
  "experimental": true
}
```

Restart Docker daemon:
```bash
sudo systemctl restart docker
```

## 5.5 Dashboard Creation and Metrics Visualization

### Accessing Grafana
1. Navigate to `http://<manager_ip>:3000`
2. Login with username: `admin`, password: `admin123`
3. Add Prometheus data source: `http://prometheus:9090`
4. Create visualizations and dashboards

**[IMG-13: Grafana Dashboard Setup]**
*Location in original text: "Dashboard sử dụng Promethus/Grafana để phân tích, giám sát hiệu suất swarm - 1. Tạo Dashboard trên GUI (có hình)"*

![Grafana Dashboard Setup](../assets/13-grafana-setup.png)

### Key Metrics and Queries

#### CPU Usage Percentage
```promql
avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) * 100
```

**[IMG-14: CPU Usage Swarm Percentage]**
*Location in original text: "Phần trăm CPU đang sử dụng trên Swarm (có hình)"*

![CPU Usage Panel](../assets/14-cpu-usage-panel.png)

#### Container CPU Usage
```promql
sum(rate(container_cpu_usage_seconds_total[1m])) by (service_name)
```

**[IMG-15: Total Container CPU Usage]**
*Location in original text: "Tổng CPU container đã sử dụng (có hình)"*

![Container CPU Usage](../assets/15-container-cpu-usage.png)

#### Memory Usage Percentage
```promql
avg(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
```

**[IMG-16: Memory Usage Swarm Percentage]**
*Location in original text: "Phần trăm Memory đang sử dụng trên Swarm (có hình)"*

![Memory Usage Panel](../assets/16-memory-usage-panel.png)

#### Network Traffic
```promql
avg(rate(node_network_receive_bytes_total[5m]) + rate(node_network_transmit_bytes_total[5m])) by (instance)
```

**[IMG-17: Total Cluster Network Traffic]**
*Location in original text: "Tổng lưu lượng mạng của toàn cụm (Download + Upload) (có hình)"*

![Network Traffic Panel](../assets/17-network-traffic-panel.png)

#### File Descriptors and Sockets
```promql
sum(node_filefd_allocated)
sum(node_sockstat_TCP_alloc)
```

**[IMG-18: Active Files and Sockets]**
*Location in original text: "Tổng File đang mở và socket đang hoạt động (có hình)"*

![File Descriptors and Sockets](../assets/18-file-sockets-panel.png)

#### Disk Usage
```promql
(node_filesystem_free_bytes{fstype!~"tmpfs|iso9660"}/node_filesystem_size_bytes{fstype!~"tmpfs|iso9660"}) * 100
```

**[IMG-19: Disk Usage Panel]**
*Location in original text: "Disk (có hình)"*

![Disk Usage Panel](../assets/19-disk-usage-panel.png)

### Complete Dashboard Overview

**[IMG-20: Complete Monitoring Dashboard]**
*Location in original text: "Tổng thể Dashboard để giám sát (có hình)"*

![Complete Dashboard Overview](../assets/20-complete-dashboard.png)

### Dashboard Components
Create comprehensive dashboards including:
- **System Overview**: CPU, Memory, Disk, Network
- **Container Metrics**: Per-service resource usage
- **Performance Trends**: Historical performance analysis
- **Alert Status**: Current system alerts and notifications

## 5.6 Integration Verification

### Service Health Check
Verify all monitoring components:

```bash
sudo docker service ls | grep -E "(prometheus|influxdb|grafana|node-exporter)"
```

### Metrics Flow Verification
1. **Prometheus Targets**: Check `http://<manager_ip>:9090/targets`
2. **InfluxDB Data**: Verify metrics storage in InfluxDB
3. **Grafana Dashboards**: Confirm data visualization

### Troubleshooting
Common issues and solutions:
- **Target Discovery**: Verify service names and network connectivity
- **Data Flow**: Check Prometheus scrape intervals and targets
- **Storage Issues**: Monitor InfluxDB disk usage and retention
- **Visualization**: Verify Grafana data source configurations

This monitoring stack provides comprehensive visibility into the MrNamCoinSwarm system performance and health.
