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

```bash
curl -s "http://<IP_Node>:9090/api/v1/query?query=node_cpu_seconds_total" | jq
```

<img width="1125" height="390" alt="image" src="https://github.com/user-attachments/assets/8e82220c-e46d-4e6d-b574-0604ccccf4f3" />
<img width="1125" height="673" alt="image" src="https://github.com/user-attachments/assets/41f2eaee-c7d5-45eb-a15c-7408a6a444d4" />

### CPU Analysis Queries
```promql
# CPU usage percentage across cluster
avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) * 100

# Per-node CPU utilization
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Container CPU usage by service
sum(rate(container_cpu_usage_seconds_total[1m])) by (service_name)
```
<img width="1125" height="615" alt="image" src="https://github.com/user-attachments/assets/d30a33e3-938a-4deb-9bfb-d944d3ff7e20" />
<img width="1125" height="615" alt="image" src="https://github.com/user-attachments/assets/1174ab91-582c-4edb-badb-42796936934d" />

## 7.3 Memory Metrics

### Memory Utilization Metrics
- **node_memory_MemTotal_bytes**: Total physical memory capacity
<img width="1125" height="400" alt="image" src="https://github.com/user-attachments/assets/f0ba533e-c302-4caa-8dab-ad4a1d893f91" />

- **node_memory_MemAvailable_bytes**: Available memory for applications
<img width="1125" height="383" alt="image" src="https://github.com/user-attachments/assets/03d3d21f-f402-4fa8-b28a-e8786a1ab78a" />

- **node_memory_Active_bytes**: Memory currently in active use
- **node_memory_Inactive_bytes**: Memory that was recently used but is now inactive
<img width="1125" height="400" alt="image" src="https://github.com/user-attachments/assets/99fd2f18-6d88-48ff-af2d-5d003dfeada2" />

- **node_memory_Cached_bytes**: Memory used for file system cache
- **node_memory_Buffers_bytes**: Memory used for system buffers
<img width="1125" height="394" alt="image" src="https://github.com/user-attachments/assets/28b92690-8266-4ae7-a206-d63c1ca82374" />

- **node_memory_SwapTotal_bytes**: Total swap memory
- **node_memory_SwapFree_bytes**: Available swap memory
<img width="1125" height="379" alt="image" src="https://github.com/user-attachments/assets/e24d345f-c221-4216-a4a0-f38c23b29d6b" />

### CLI Query Example

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
<img width="973" height="523" alt="image" src="https://github.com/user-attachments/assets/f6622d2b-38c0-4dc2-be9b-db18ceffd77d" />

## 7.4 File Descriptors and Socket Metrics

### File System Metrics
- **node_filefd_allocated**: Number of file descriptors currently in use

<img width="1125" height="404" alt="image" src="https://github.com/user-attachments/assets/f43a60d8-a6b8-4c35-b224-d5bd82bde210" />

- **node_filefd_maximum**: Maximum number of file descriptors that can be opened

<img width="1125" height="410" alt="image" src="https://github.com/user-attachments/assets/1fa4b08d-3815-4ec0-9a17-aaa1577f0962" />

- **node_sockstat_TCP_inuse**: Number of TCP connections currently in use

<img width="1125" height="402" alt="image" src="https://github.com/user-attachments/assets/2a91b34a-6643-4c9f-8b13-c1ec75514735" />

- **node_sockstat_UDP_inuse**: Number of UDP connections currently open

<img width="1125" height="406" alt="image" src="https://github.com/user-attachments/assets/6a3c98db-eceb-4961-954c-f425726452b0" />

- **node_sockstat_sockets_used**: Total number of active sockets

<img width="1125" height="394" alt="image" src="https://github.com/user-attachments/assets/77248cef-495b-46b9-bbd3-3f4b637a1598" />

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

<img width="1125" height="717" alt="image" src="https://github.com/user-attachments/assets/0a512b82-b769-43e2-9621-e80b5f8bb6a2" />

- **node_disk_reads_completed_total**: Number of completed read operations
- **node_disk_writes_completed_total**: Number of completed write operations

<img width="1125" height="604" alt="image" src="https://github.com/user-attachments/assets/3dfc1603-ba1b-462b-b282-3a1ddc53ab14" />

- **node_disk_io_time_seconds_total**: Total time device was busy processing I/O

<img width="1125" height="617" alt="image" src="https://github.com/user-attachments/assets/e1b1eb66-c3c2-4fcd-a550-33a8c7ef601a" />

- **node_filesystem_avail_bytes**: Available space on filesystems

<img width="1125" height="735" alt="image" src="https://github.com/user-attachments/assets/5a2eb291-35d6-4591-85ae-a6aa68681b4b" />

### Network I/O Metrics
- **node_network_receive_bytes_total**: Bytes received through network interfaces
- **node_network_transmit_bytes_total**: Bytes transmitted through network interfaces

<img width="1125" height="575" alt="image" src="https://github.com/user-attachments/assets/f7e1b725-df3f-4509-b0ca-788c2fdcfdaf" />

- **node_network_receive_packets_total**: Packets received through network interfaces
- **node_network_transmit_packets_total**: Packets transmitted through network interfaces

<img width="1125" height="373" alt="image" src="https://github.com/user-attachments/assets/c56f7738-2dc7-4632-a5e5-4cf82da43aaf" />

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
<img width="1125" height="88" alt="image" src="https://github.com/user-attachments/assets/adc4e2b5-8393-4b10-bfd6-22383752465d" />


### Database Operations
```sql
-- Show available databases
SHOW DATABASES

-- Access prometheus database
USE prometheus

-- Display all metrics (measurements)
SHOW MEASUREMENTS
```
<img width="1125" height="221" alt="image" src="https://github.com/user-attachments/assets/db806f8d-a84c-4ae4-b9f1-dbf63449cded" />
<img width="1125" height="165" alt="image" src="https://github.com/user-attachments/assets/8e39582d-58c3-4b7f-900a-5fe8a82766ee" />
<img width="1125" height="394" alt="image" src="https://github.com/user-attachments/assets/19274633-f68a-4600-990b-c839b1a85597" />

### Data Analysis Queries

#### CPU Data Analysis
```sql
SELECT mean("value") FROM "node_cpu_seconds_total"
WHERE "mode" = 'user' AND time > now() - 5m
GROUP BY time(1m), "instance";
```

<img width="1125" height="233" alt="image" src="https://github.com/user-attachments/assets/5276199c-d004-4721-ba9c-f688c09e30a1" />

#### Memory Data Analysis
```sql
SELECT mean("value") FROM "node_memory_Active_bytes"
WHERE time > now() - 5m
GROUP BY time(1m), "instance";
```

<img width="1125" height="229" alt="image" src="https://github.com/user-attachments/assets/75164ec0-5dc4-4bae-8df1-0e5ba3ee5bc6" />

#### Network Traffic Analysis
```sql
SELECT derivative(mean("value"), 1s) FROM "node_network_receive_bytes_total"
WHERE "device" != 'lo' AND time > now() - 5m
GROUP BY time(1m), "instance", "device";
```

<img width="1125" height="456" alt="image" src="https://github.com/user-attachments/assets/bd791a7f-eda0-434c-bd24-aa228b131e16" />

#### Resource Usage Queries
```sql
-- File descriptors
SELECT "value" FROM "node_filefd_allocated"
WHERE time > now() - 5m;

-- TCP connections
SELECT "value" FROM "node_sockstat_TCP_alloc"
WHERE time > now() - 5m;
```

<img width="1125" height="323" alt="image" src="https://github.com/user-attachments/assets/867e6482-7655-4ff8-9e9d-8dd66a85fb49" />
<img width="1125" height="269" alt="image" src="https://github.com/user-attachments/assets/e4e01ca3-55a5-4678-a51c-db9dc405ce43" />

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
<img width="1125" height="615" alt="image" src="https://github.com/user-attachments/assets/94cbdaf4-0d17-44aa-8703-642712b10045" />

**Memory Usage Panel**
```promql
(avg(node_memory_MemAvailable_bytes) / avg(node_memory_MemTotal_bytes)) * 100
```
<img width="973" height="523" alt="image" src="https://github.com/user-attachments/assets/4362c482-6aa0-4add-81a3-8941e229a3b7" />

**Network Traffic Panel**
```promql
avg(rate(node_network_receive_bytes_total[5m]) + rate(node_network_transmit_bytes_total[5m])) by (instance)
```
<img width="1125" height="604" alt="image" src="https://github.com/user-attachments/assets/76476bf0-164b-4c3f-a36a-97e976fbd7a6" />

**Disk Usage Panel**
```promql
(node_filesystem_free_bytes{fstype!~"tmpfs|iso9660"} / node_filesystem_size_bytes{fstype!~"tmpfs|iso9660"}) * 100
```
<img width="1125" height="610" alt="image" src="https://github.com/user-attachments/assets/80a24afa-9274-4638-b40b-77ca0ea61f00" />


#### Container-Specific Dashboard
Monitor individual service performance:

**Container CPU Usage**
```promql
sum(rate(container_cpu_usage_seconds_total[1m])) by (service_name)
```
<img width="1125" height="596" alt="image" src="https://github.com/user-attachments/assets/bf7352a6-8e46-4178-adf3-49ce7c47fba2" />

**Container Memory Usage**
```promql
sum(rate(container_cpu_usage_seconds_total[1m])) by (service_name)
```
<img width="1125" height="596" alt="image" src="https://github.com/user-attachments/assets/341b4889-b75e-4db1-b3cd-cac3f6444130" />

### Dashboard Features
- **Real-time Monitoring**: Live data updates every 15 seconds
- **Historical Analysis**: Time-range selection for trend analysis
- **Alert Integration**: Visual indicators for threshold breaches
- **Multi-Panel Layout**: Comprehensive system overview in single view

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
