# Chapter 7: Monitoring and Optimization

## Overview

This chapter focuses on the comprehensive monitoring capabilities and optimization strategies implemented for the MrNamCoinSwarm system. We detail the metrics collection process, data analysis, and performance optimization techniques used to ensure system reliability and efficiency.

## 7.1 Metrics Collection from Nodes

### Node Exporter Implementation
To collect comprehensive metrics, we utilized Node Exporter, a popular Prometheus exporter that gathers detailed information about hardware, operating system, and resources from each server (node).

### Collected Metrics Categories

## 7.2 CPU Metrics

### Core CPU Metrics
**node_cpu_seconds_total{mode=...}** - Total CPU time spent in various modes:
- **user**: Time spent processing user tasks
- **system**: Time spent processing system tasks
- **idle**: Time when CPU is not in use
- **iowait**: Time waiting for I/O operations
- **steal**: Time stolen by hypervisor (in virtualized environments)
- **nice**: Time spent on low-priority processes
- **irq**: Time spent handling hardware interrupts
- **softirq**: Time spent handling software interrupts

### Load Average Metrics
- **node_load1**: Load average over 1 minute
- **node_load5**: Load average over 5 minutes
- **node_load15**: Load average over 15 minutes

### CLI Query Example

**[IMG-27: CPU Metrics Query Result]**
*Location in original text: "Kết quả query CPU metrics (có hình)"*

![CPU Metrics Query Result](../assets/27-cpu-metrics-query.png)

```bash
curl -s "http://<IP_Node>:9090/api/v1/query?query=node_cpu_seconds_total" | jq
```

### CPU Analysis Queries
```promql
# CPU usage percentage across cluster
avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) * 100

# Per-node CPU utilization
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Container CPU usage by service
sum(rate(container_cpu_usage_seconds_total[1m])) by (service_name)
```

## 7.3 Memory Metrics

### Memory Utilization Metrics
- **node_memory_MemTotal_bytes**: Total physical memory capacity
- **node_memory_MemAvailable_bytes**: Available memory for applications
- **node_memory_Active_bytes**: Memory currently in active use
- **node_memory_Inactive_bytes**: Memory that was recently used but is now inactive
- **node_memory_Cached_bytes**: Memory used for file system cache
- **node_memory_Buffers_bytes**: Memory used for system buffers
- **node_memory_SwapTotal_bytes**: Total swap memory
- **node_memory_SwapFree_bytes**: Available swap memory

### CLI Query Example

**[IMG-28: Memory Metrics Dashboard]**
*Location in original text: "Dashboard memory metrics (có hình)"*

![Memory Metrics](../assets/28-memory-metrics.png)

```bash
curl -s "http://<IP_Node>:9090/api/v1/query?query=node_memory_" | jq
```

### Memory Analysis Queries
```promql
# Memory usage percentage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Available memory percentage
(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100

# Memory pressure indicator
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes
```

## 7.4 File Descriptors and Socket Metrics

### File System Metrics
- **node_filefd_allocated**: Number of file descriptors currently in use

**[IMG-29: File Descriptors Allocated]**
*Location in original text: "File descriptors được phân bổ (có hình)"*

![File Descriptors Allocated](../assets/29-file-descriptors-allocated.png)

- **node_filefd_maximum**: Maximum number of file descriptors that can be opened

**[IMG-30: File Descriptors Maximum]**
*Location in original text: "Giới hạn tối đa file descriptors (có hình)"*

![File Descriptors Maximum](../assets/30-file-descriptors-maximum.png)

- **node_sockstat_TCP_inuse**: Number of TCP connections currently in use

**[IMG-31: TCP Connections]**
*Location in original text: "Số lượng TCP connections (có hình)"*

![TCP Connections](../assets/31-tcp-connections.png)

- **node_sockstat_UDP_inuse**: Number of UDP connections currently open

**[IMG-32: UDP Connections]**
*Location in original text: "Số lượng UDP connections (có hình)"*

![UDP Connections](../assets/32-udp-connections.png)

- **node_sockstat_sockets_used**: Total number of active sockets

**[IMG-33: Active Sockets]**
*Location in original text: "Tổng số sockets đang hoạt động (có hình)"*

![Active Sockets](../assets/33-active-sockets.png)

### Resource Monitoring Queries
```promql
# File descriptor usage
node_filefd_allocated

# Socket usage
sum(node_sockstat_TCP_alloc)
sum(node_sockstat_UDP_inuse)
sum(node_sockstat_sockets_used)
```

## 7.5 I/O Operations (Disk and Network)

### Disk I/O Metrics
- **node_disk_read_bytes_total**: Total bytes read from storage devices
- **node_disk_written_bytes_total**: Total bytes written to storage devices

**[IMG-34: Disk I/O Bytes]**
*Location in original text: "Bytes đọc/ghi trên disk (có hình)"*

![Disk I/O Bytes](../assets/34-disk-io-bytes.png)

- **node_disk_reads_completed_total**: Number of completed read operations
- **node_disk_writes_completed_total**: Number of completed write operations

**[IMG-35: Disk Operations]**
*Location in original text: "Số lượng operations trên disk (có hình)"*

![Disk Operations](../assets/35-disk-operations.png)

- **node_disk_io_time_seconds_total**: Total time device was busy processing I/O

**[IMG-36: Disk I/O Time]**
*Location in original text: "Thời gian I/O trên disk (có hình)"*

![Disk I/O Time](../assets/36-disk-io-time.png)

- **node_filesystem_avail_bytes**: Available space on filesystems

**[IMG-37: Filesystem Available Space]**
*Location in original text: "Dung lượng có sẵn trên filesystem (có hình)"*

![Filesystem Available](../assets/37-filesystem-available.png)

### Network I/O Metrics
- **node_network_receive_bytes_total**: Bytes received through network interfaces
- **node_network_transmit_bytes_total**: Bytes transmitted through network interfaces

**[IMG-38: Network I/O Bytes]**
*Location in original text: "Bytes nhận/gửi qua network (có hình)"*

![Network I/O Bytes](../assets/38-network-io-bytes.png)

- **node_network_receive_packets_total**: Packets received through network interfaces
- **node_network_transmit_packets_total**: Packets transmitted through network interfaces

**[IMG-39: Network I/O Packets]**
*Location in original text: "Packets network I/O (có hình)"*

![Network I/O Packets](../assets/39-network-io-packets.png)

### I/O Analysis Queries
```promql
# Disk read/write rate
rate(node_disk_read_bytes_total[5m])
rate(node_disk_written_bytes_total[5m])

# Network traffic rate
rate(node_network_receive_bytes_total[5m])
rate(node_network_transmit_bytes_total[5m])

# Combined network traffic
rate(node_network_receive_bytes_total[5m]) + rate(node_network_transmit_bytes_total[5m])

# Disk utilization percentage
(node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes * 100
```

## 7.6 InfluxDB Data Querying

### Database Access
Access InfluxDB for historical data analysis:

```bash
sudo docker exec -it $(sudo docker ps --filter name=influxdb --format '{{.ID}}') influx
```

**[IMG-40: InfluxDB Access Interface]**
*Location in original text: "Giao diện truy cập InfluxDB (có hình)"*

![InfluxDB Access](../assets/40-influxdb-access.png)

### Database Operations
```sql
-- Show available databases
SHOW DATABASES

-- Access prometheus database
USE prometheus

-- Display all metrics (measurements)
SHOW MEASUREMENTS
```

**[IMG-41: InfluxDB Database Operations]**
*Location in original text: "Các thao tác database trong InfluxDB (có hình)"*

![InfluxDB Database Operations](../assets/41-influxdb-operations.png)

### Data Analysis Queries

#### CPU Data Analysis
```sql
SELECT mean("value") FROM "node_cpu_seconds_total"
WHERE "mode" = 'user' AND time > now() - 5m
GROUP BY time(1m), "instance";
```

**[IMG-42: CPU Data Analysis Results]**
*Location in original text: "Kết quả phân tích dữ liệu CPU (có hình)"*

![CPU Data Analysis](../assets/42-cpu-data-analysis.png)

#### Memory Data Analysis
```sql
SELECT mean("value") FROM "node_memory_Active_bytes"
WHERE time > now() - 5m
GROUP BY time(1m), "instance";
```

**[IMG-43: Memory Data Analysis Results]**
*Location in original text: "Kết quả phân tích dữ liệu Memory (có hình)"*

![Memory Data Analysis](../assets/43-memory-data-analysis.png)

#### Network Traffic Analysis
```sql
SELECT derivative(mean("value"), 1s) FROM "node_network_receive_bytes_total"
WHERE "device" != 'lo' AND time > now() - 5m
GROUP BY time(1m), "instance", "device";
```

**[IMG-44: Network Traffic Analysis Results]**
*Location in original text: "Kết quả phân tích network traffic (có hình)"*

![Network Traffic Analysis](../assets/44-network-traffic-analysis.png)

#### Resource Usage Queries
```sql
-- File descriptors
SELECT "value" FROM "node_filefd_allocated"
WHERE time > now() - 5m;

-- TCP connections
SELECT "value" FROM "node_sockstat_TCP_alloc"
WHERE time > now() - 5m;
```

**[IMG-45: Resource Usage Query Results]**
*Location in original text: "Kết quả queries sử dụng tài nguyên (có hình)"*

![Resource Usage Queries](../assets/45-resource-usage-queries.png)

## 7.7 Grafana Dashboard Creation

### Dashboard Access
1. Navigate to `http://<manager_ip>:3000`
2. Login with credentials: `admin` / `admin123`
3. Add Prometheus data source
4. Create visualizations and dashboards

### Key Dashboard Panels

#### System Overview Dashboard
Create comprehensive system monitoring with the following panels:

**CPU Usage Panel**
```promql
avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) * 100
```

**[IMG-46: CPU Usage Panel in Grafana]**
*Location in original text: "Panel CPU Usage trong Grafana (có hình)"*

![CPU Usage Panel](../assets/46-cpu-usage-panel.png)

**Memory Usage Panel**
```promql
(1 - (avg(node_memory_MemAvailable_bytes) / avg(node_memory_MemTotal_bytes))) * 100
```

**[IMG-47: Memory Usage Panel in Grafana]**
*Location in original text: "Panel Memory Usage trong Grafana (có hình)"*

![Memory Usage Panel](../assets/47-memory-usage-panel.png)

**Network Traffic Panel**
```promql
avg(rate(node_network_receive_bytes_total[5m]) + rate(node_network_transmit_bytes_total[5m])) by (instance)
```

![Network Traffic Panel](../assets/network-traffic-panel.png)

**Disk Usage Panel**
```promql
(1 - (node_filesystem_free_bytes{fstype!~"tmpfs|iso9660"} / node_filesystem_size_bytes{fstype!~"tmpfs|iso9660"})) * 100
```

**[IMG-48: Disk Usage Panel in Grafana]**
*Location in original text: "Panel Disk Usage trong Grafana (có hình)"*

![Disk Usage Panel](../assets/48-disk-usage-panel.png)

#### Container-Specific Dashboard
Monitor individual service performance:

**Container CPU Usage**
```promql
sum(rate(container_cpu_usage_seconds_total[1m])) by (service_name)
```

**[IMG-49: Container CPU Usage Dashboard]**
*Location in original text: "Dashboard Container CPU Usage (có hình)"*

![Container CPU Usage](../assets/49-container-cpu-usage.png)

**Container Memory Usage**
```promql
sum(container_memory_usage_bytes) by (service_name)
```

**[IMG-50: Container Memory Usage Dashboard]**
*Location in original text: "Dashboard Container Memory Usage (có hình)"*

![Container Memory Usage](../assets/50-container-memory-usage.png)

**Service Health Status**
```promql
up{job="prometheus"}
```

**[IMG-51: Service Health Status Dashboard]**
*Location in original text: "Dashboard Service Health Status (có hình)"*

![Service Health Status](../assets/51-service-health-status.png)

### Dashboard Features
- **Real-time Monitoring**: Live data updates every 15 seconds
- **Historical Analysis**: Time-range selection for trend analysis
- **Alert Integration**: Visual indicators for threshold breaches
- **Multi-Panel Layout**: Comprehensive system overview in single view

![Complete Dashboard Overview](../assets/complete-dashboard.png)

## 7.8 Performance Optimization Strategies

### Resource Optimization
Based on monitoring data, implement the following optimizations:

#### Memory Management
- **Container Limits**: Set appropriate memory limits for services
- **Cache Optimization**: Monitor and optimize cache usage patterns
- **Garbage Collection**: Tune JVM settings for Java-based services

#### CPU Optimization
- **Load Balancing**: Distribute workload evenly across nodes
- **Process Prioritization**: Use CPU affinity for critical services
- **Scaling Decisions**: Auto-scale based on CPU utilization thresholds

#### Storage Optimization
- **Volume Management**: Monitor disk usage and implement cleanup policies
- **I/O Optimization**: Optimize disk access patterns
- **Log Rotation**: Implement automatic log rotation to prevent disk filling

### Network Optimization
- **Bandwidth Monitoring**: Track network utilization patterns
- **Connection Pooling**: Optimize service-to-service communication
- **Compression**: Enable data compression where appropriate

## 7.9 Alerting and Notifications

### Alert Rules Configuration
Define critical system alerts:

```yaml
# High CPU usage alert
- alert: HighCPUUsage
  expr: avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) * 100 > 80
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High CPU usage detected"

# Memory usage alert
- alert: HighMemoryUsage
  expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High memory usage detected"

# Disk space alert
- alert: LowDiskSpace
  expr: (1 - (node_filesystem_free_bytes / node_filesystem_size_bytes)) * 100 > 90
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Low disk space detected"
```

### Monitoring Best Practices
1. **Threshold Setting**: Establish meaningful alert thresholds
2. **Alert Fatigue Prevention**: Avoid over-alerting on minor issues
3. **Escalation Procedures**: Define clear escalation paths
4. **Documentation**: Maintain runbooks for common alerts

## 7.10 Capacity Planning

### Growth Analysis
Use historical data for capacity planning:
- **Trend Analysis**: Identify growth patterns in resource usage
- **Peak Load Planning**: Prepare for expected traffic spikes
- **Resource Forecasting**: Predict future resource requirements

### Scaling Recommendations
Based on monitoring data:
- **Horizontal Scaling**: Add nodes when cluster utilization is high
- **Vertical Scaling**: Increase resources for specific bottlenecked services
- **Load Distribution**: Rebalance services across available nodes

This comprehensive monitoring and optimization approach ensures the MrNamCoinSwarm system operates efficiently and can scale to meet future demands.
