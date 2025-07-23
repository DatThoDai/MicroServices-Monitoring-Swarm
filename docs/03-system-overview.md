# Chapter 3: System Architecture Overview

## MrNamCoinSwarm System Overview

**[IMG-01: MrNamCoinSwarm System Architecture Diagram]**
*Location in original text: "1.1. Kiến trúc Tổng thể (có hình)"*

![System Architecture Diagram](../assets/01-system-architecture.png)

MrNamCoinSwarm is a microservices system built on the Docker Swarm platform, consisting of 5 main services that work together to create a distributed coin mining simulation.

## Core Services

### 1. WebUI Service
- **Port**: 8000
- **Image**: webui:coinswarm
- **Function**: User interface that displays the number of coins generated
- **Technology**: Web-based dashboard
- **Purpose**: Provides real-time visualization of the mining process

### 2. RNG (Random Number Generator) Service
- **Port**: 8001
- **Image**: rng:coinswarm
- **Function**: Generates random numbers for the mining process
- **Technology**: RESTful API service
- **Purpose**: Provides entropy for the hashing algorithm

### 3. Hasher Service
- **Port**: 8002
- **Image**: hasher:coinswarm
- **Function**: Calculates hash values from random numbers
- **Technology**: Cryptographic hashing service
- **Purpose**: Performs the computational work of "mining"

### 4. Worker Service
- **Image**: worker:coinswarm
- **Function**: Orchestrates the mining process between RNG and Hasher
- **Technology**: Background processing service
- **Purpose**: Coordinates the workflow and manages service communication

### 5. Redis Service
- **Image**: redis:latest
- **Function**: Stores temporary data and mining results
- **Technology**: In-memory data structure store
- **Purpose**: Provides fast data access and persistence

## System Workflow

**[IMG-02: System Workflow Diagram]**
*Location in original text: "1.2. Luồng Hoạt động (có hình)"*

![System Workflow Diagram](../assets/02-system-workflow.png)

### Detailed Process Flow

1. **Request Initiation**: Worker service requests a random number from RNG service
2. **Random Generation**: RNG service generates and returns a random number
3. **Hash Calculation**: Worker sends the random number to Hasher for computation
4. **Result Storage**: Computed hash result is stored in Redis
5. **Data Retrieval**: WebUI reads data from Redis
6. **User Display**: WebUI displays the coin count and mining statistics

## Docker Swarm Deployment Results

### a. LAN Network Setup Results on VirtualBox

**[IMG-03: VirtualBox Network Configuration]**
*Location in original text: "a. Kết quả xây dựng mạng LAN trên VitualBox (có hình)"*

![VirtualBox Network Setup](../assets/03-virtualbox-network.png)

- Successfully established network with IP range: 192.168.10.1
- Network adapter configuration: Host-only
- Full connectivity between all nodes
- Successful ping tests between all nodes

### b. Docker Swarm Deployment Results

**[IMG-04: Docker Swarm Cluster Structure]**
*Location in original text: "b. Kết quả triển khai Docker Swarm - Cấu trúc cụm (có hình)"*

![Docker Swarm Cluster](../assets/04-swarm-cluster.png)

#### Cluster Architecture
- **Manager Nodes**: 3 nodes (High Availability configuration)
- **Worker Nodes**: 7 nodes
- **Total Nodes**: 10 nodes
- **Quorum**: 2 (minimum managers needed for operation)
- **Leader Election**: Automatic failover when leader fails
- **Manager Distribution**: Even distribution across different nodes

**[IMG-05: Node Status Display]**
*Location in original text: "Trạng thái nodes (có hình)"*

![Node Status](../assets/05-node-status.png)

### c. Service Deployment Results

**[IMG-06: Service Deployment Status]**
*Location in original text: "c. Kết quả triển khai services (có hình)"*

![Service Deployment](../assets/06-service-deployment.png)

### d. High Availability Configuration

**[IMG-07: High Availability Setup]**
*Location in original text: "d. Cấu hình High Availability (có hình)"*

![High Availability Configuration](../assets/07-ha-configuration.png)

#### Manager Node Configuration
- **3 Manager Nodes**: Ensures fault tolerance
- **Raft Consensus**: Distributed consensus algorithm
- **Automatic Failover**: Seamless leader election
- **Load Distribution**: Even workload distribution

### e. System Monitoring Results

**[IMG-08: Service Location Monitoring (WebUI)]**
*Location in original text: "Kiểm tra vị trí service của 1 service (webui) (có hình)"*

![Service Location Monitoring](../assets/08-service-location.png)

**[IMG-09: Resource Monitoring Dashboard]**
*Location in original text: "Monitoring tài nguyên (có hình)"*

![Resource Monitoring](../assets/09-resource-monitoring.png)
    A[Worker Service] --> B[RNG Service]
    B --> C[Random Number]
    A --> D[Hasher Service]
    D --> E[Hash Result]
    E --> F[Redis]
    F --> G[WebUI Service]
    G --> H[User Display]
```

### Detailed Process Flow

1. **Request Initiation**: Worker service requests a random number from RNG service
2. **Random Generation**: RNG service generates and returns a random number
3. **Hash Calculation**: Worker sends the random number to Hasher for computation
4. **Result Storage**: Computed hash result is stored in Redis
5. **Data Retrieval**: WebUI reads data from Redis
6. **User Display**: WebUI displays the coin count and mining statistics

## Docker Swarm Deployment Results

### Network Infrastructure
- **Network Range**: 192.168.10.x/24
- **Network Adapter**: Host-only configuration
- **Connectivity**: Full mesh connectivity between all nodes
- **Verification**: Successful ping tests between all nodes

![Network Configuration](../assets/network-configuration.png)

### Cluster Architecture
- **Manager Nodes**: 3 nodes (High Availability configuration)
- **Worker Nodes**: 7 nodes
- **Total Nodes**: 10 nodes
- **Quorum**: 2 (minimum managers needed for operation)
- **Leader Election**: Automatic failover when leader fails
- **Manager Distribution**: Even distribution across different nodes

![Docker Swarm Cluster](../assets/swarm-cluster.png)

### High Availability Configuration

The system is designed with High Availability in mind:

#### Manager Node Configuration
- **3 Manager Nodes**: Ensures fault tolerance
- **Raft Consensus**: Distributed consensus algorithm
- **Automatic Failover**: Seamless leader election
- **Load Distribution**: Even workload distribution

#### Service Deployment
All services are deployed with considerations for:
- **Replica Management**: Appropriate replica counts for each service
- **Resource Constraints**: Memory and CPU limits
- **Network Isolation**: Service-specific networks
- **Health Checks**: Automated health monitoring

### Monitoring Capabilities

The deployed system includes comprehensive monitoring:

#### Service Location Tracking
- Real-time service placement monitoring
- Container location awareness
- Service migration tracking

![Service Location Monitoring](../assets/service-location.png)

#### Resource Monitoring
- CPU utilization tracking
- Memory usage monitoring
- Network I/O statistics
- Disk usage analytics

![Resource Monitoring](../assets/resource-monitoring.png)

## Network Architecture

### Overlay Networks
The system utilizes multiple overlay networks:

1. **coinswarmnet**: For DockerCoins services communication
2. **monitoring**: For Prometheus, Grafana, InfluxDB
3. **loggingnet**: For ELK Stack components
4. **proxy**: For Nginx reverse proxy integration

### Service Discovery
Docker Swarm provides built-in service discovery:
- **DNS-based Discovery**: Services accessible by name
- **Load Balancing**: Automatic request distribution
- **Health Awareness**: Automatic routing to healthy instances

## Scalability Considerations

The architecture supports horizontal scaling:
- **Service Replicas**: Easy scaling of individual services
- **Node Addition**: Simple addition of new worker nodes
- **Load Distribution**: Automatic load balancing across replicas
- **Resource Management**: Dynamic resource allocation

This foundational architecture provides the base for implementing comprehensive monitoring and logging solutions described in the following chapters.
