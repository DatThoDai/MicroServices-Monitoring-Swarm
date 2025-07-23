# Chapter 4: ELK Stack Deployment

## Overview

<img width="1264" height="710" alt="image" src="https://github.com/user-attachments/assets/df90e516-d2fe-4e65-b3c9-2e861d471a7f" />

### Dashboard Creation
<img width="1125" height="538" alt="image" src="https://github.com/user-attachments/assets/9c356d25-d80a-4359-8ec0-79275f740b5b" />

Create visualizations and dashboards for:
- **Log Volume**: Track log frequency over time
- **Service Status**: Monitor individual service health
- **Error Analysis**: Identify and analyze error patterns
- **Performance Metrics**: Analyze response times and throughputck (Elasticsearch, Logstash, and Kibana) provides a comprehensive logging solution for the MrNamCoinSwarm system. This chapter details the deployment and configuration of each component for centralized log management.

## 4.1 Elasticsearch Configuration

Elasticsearch serves as the central search and analytics engine for log data storage and retrieval.

### Network Setup
First, create an overlay network for the logging infrastructure:

```bash
sudo docker network create --driver overlay --attachable loggingnet
```

### Data Persistence
Create a volume for Elasticsearch data persistence:

```bash
sudo docker volume create es_data
```

### Elasticsearch Deployment
Deploy Elasticsearch with the following configuration:

```bash
sudo docker service create \
  --name elasticsearch \
  --network loggingnet \
  --replicas 1 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  --mount type=volume,source=es_data,target=/usr/share/elasticsearch/data \
  --publish published=9200,target=9200 \
  --constraint 'node.role==manager' \
  --health-cmd="curl -f http://localhost:9200/_cluster/health || exit 1" \
  --health-interval=30s \
  docker.elastic.co/elasticsearch/elasticsearch:8.12.0
```

### Configuration Details
- **Single Node Mode**: Simplified deployment for development/testing
- **Security Disabled**: For internal cluster communication
- **Memory Limit**: 512MB heap size for resource management
- **Health Checks**: Regular cluster health monitoring
- **Port 9200**: Standard Elasticsearch HTTP port
- **Manager Constraint**: Ensures deployment on manager nodes

## 4.2 Logstash Configuration

Logstash processes and transforms log data before sending it to Elasticsearch.

### Pipeline Configuration
Create the Logstash configuration file:

```bash
cat << 'EOF' > logstash.conf
input {
  gelf {
    port => 12201
    type => docker
    use_tcp => false
    codec => json
  }
}

filter {
  if [container_name] in ["rng", "hasher", "worker", "webui"] {
    mutate {
      add_field => {
        "service_name" => "%{[container_name]}"
        "node_hostname" => "%{[host]}"
        "environment" => "dockercoins"
      }
      remove_field => ["_source", "stream", "tag"]
    }
    
    date {
      match => ["timestamp", "ISO8601"]
      target => "@timestamp"
    }

    if [message] =~ /(?i)(error|failed|exception|critical|fatal)/ {
      mutate { add_field => { "log_level" => "ERROR" } }
    } else if [message] =~ /(?i)(warn|warning|deprecated)/ {
      mutate { add_field => { "log_level" => "WARNING" } }
    } else {
      mutate { add_field => { "log_level" => "INFO" } }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "dockercoins-logs-%{+YYYY.MM.dd}"
    template_name => "dockercoins"
    template_overwrite => true
    retry_on_conflict => 5
  }
  stdout { codec => rubydebug }
}
EOF
```

### Pipeline Breakdown

#### Input Stage
- **GELF Protocol**: Receives logs via GELF (Graylog Extended Log Format)
- **Port 12201**: Standard GELF UDP port
- **JSON Codec**: Processes JSON-formatted log messages

#### Filter Stage
- **Service Classification**: Identifies logs from DockerCoins services
- **Metadata Addition**: Adds service name, hostname, and environment tags
- **Field Cleanup**: Removes unnecessary fields to reduce storage
- **Timestamp Normalization**: Standardizes timestamp format
- **Log Level Classification**: Automatically categorizes log severity

#### Output Stage
- **Elasticsearch Integration**: Sends processed logs to Elasticsearch
- **Daily Indices**: Creates date-based indices for better organization
- **Retry Mechanism**: Handles temporary connection failures
- **Debug Output**: Optional stdout output for troubleshooting

### Docker Configuration
Create Docker config from the Logstash configuration:

```bash
sudo docker config create logstash_config logstash.conf
```

### Logstash Deployment
Deploy Logstash with the following specifications:

```bash
sudo docker service create \
  --name logstash \
  --network loggingnet \
  --replicas 2 \
  -e "xpack.monitoring.enabled=false" \
  -e "LS_JAVA_OPTS=-Xms512m -Xmx512m" \
  --config source=logstash_config,target=/usr/share/logstash/pipeline/logstash.conf \
  --publish mode=host,target=12201,published=12201,protocol=udp \
  --health-cmd="curl -f http://localhost:9600 || exit 1" \
  --health-interval=30s \
  docker.elastic.co/logstash/logstash:8.12.0
```

### Configuration Details
- **2 Replicas**: Provides redundancy and load distribution
- **Memory Limit**: 512MB heap size
- **Host Mode Publishing**: Ensures UDP port accessibility
- **Health Monitoring**: Regular service health checks

## 4.3 Kibana Configuration

Kibana provides the web interface for log visualization and analysis.

### Kibana Deployment
Deploy Kibana with Elasticsearch integration:

```bash
sudo docker service create \
  --name kibana \
  --network loggingnet \
  --replicas 1 \
  -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" \
  -e "XPACK_SECURITY_ENABLED=false" \
  --publish 5601:5601 \
  docker.elastic.co/kibana/kibana:8.12.0
```

### Configuration Details
- **Single Replica**: Sufficient for dashboard access
- **Elasticsearch Integration**: Direct connection to Elasticsearch service
- **Security Disabled**: Matches Elasticsearch configuration
- **Port 5601**: Standard Kibana web interface port

## 4.4 DockerCoins Integration

### Docker Log Driver Configuration

Configure all nodes to send logs to Logstash:

```bash
# Configure on all nodes
sudo tee /etc/docker/daemon.json << 'EOF'
{
  "log-driver": "gelf",
  "log-opts": {
    "gelf-address": "udp://tasks.logstash:12201",
    "tag": "{{.Name}}/{{.ID}}",
    "gelf-compression-type": "none"
  }
}
EOF

# Restart Docker daemon
sudo systemctl restart docker

# Update services to apply new log driver
sudo docker service update --force redis
sudo docker service update --force rng
sudo docker service update --force hasher
sudo docker service update --force worker
sudo docker service update --force webui
```

### Log Driver Benefits
- **Centralized Logging**: All container logs sent to Logstash
- **Automatic Tagging**: Container name and ID included
- **No Compression**: Reduces CPU overhead
- **Service Discovery**: Uses Swarm's built-in service discovery

## 4.5 Kibana Index Pattern Setup

### Creating Index Patterns
1. Access Kibana UI at `http://<manager_ip>:5601`
2. Navigate to **Menu > Stack Management > Index Patterns**
3. Click **"Create index pattern"**
4. Enter **"dockercoins-logs-*"** as the index pattern
5. Select **"@timestamp"** as the Time field
6. Click **"Create index pattern"**

### Dashboard Creation
Create visualizations and dashboards for:
- **Log Volume**: Track log frequency over time
- **Service Status**: Monitor individual service health
- **Error Analysis**: Identify and analyze error patterns
- **Performance Metrics**: Analyze response times and throughput

## Verification and Testing

### Service Health Check
Verify all ELK components are running:

```bash
sudo docker service ls | grep -E "(elasticsearch|logstash|kibana)"
```

### Log Flow Verification
1. Check Elasticsearch indices: `curl http://<manager_ip>:9200/_cat/indices`
2. Verify Logstash is receiving data: Check Kibana Discover tab
3. Confirm log processing: Review Logstash stdout logs

### Troubleshooting
Common issues and solutions:
- **Connection Issues**: Verify network connectivity between services
- **Memory Problems**: Adjust heap sizes if needed
- **Index Creation**: Ensure proper timestamp parsing
- **Service Discovery**: Verify Swarm service names resolution

This ELK Stack deployment provides a robust foundation for centralized logging and log analysis in the MrNamCoinSwarm system.
