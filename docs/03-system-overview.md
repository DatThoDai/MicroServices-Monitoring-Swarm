# Chapter 3: System Architecture Overview

## MrNamCoinSwarm System Overview

<img width="1180" height="729" alt="image" src="https://github.com/user-attachments/assets/b691bd6e-82c3-4ebe-9649-7eb9798b1133" />

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
<img width="890" height="519" alt="image" src="https://github.com/user-attachments/assets/d823efdc-a747-42c7-8844-40d8a1ed7433" />

### Detailed Process Flow

1. **Request Initiation**: Worker service requests a random number from RNG service
2. **Random Generation**: RNG service generates and returns a random number
3. **Hash Calculation**: Worker sends the random number to Hasher for computation
4. **Result Storage**: Computed hash result is stored in Redis
5. **Data Retrieval**: WebUI reads data from Redis
6. **User Display**: WebUI displays the coin count and mining statistics

## Docker Swarm Deployment Results

### a. LAN Network Setup Results on VirtualBox
<img width="741" height="292" alt="image" src="https://github.com/user-attachments/assets/6376e3c9-5abb-4efb-b63b-3d56aff88181" />

- Successfully established network with IP range: 192.168.10.1
- Network adapter configuration: Host-only
- Full connectivity between all nodes
- Successful ping tests between all nodes

### b. Docker Swarm Deployment Results
<img width="206" height="63" alt="image" src="https://github.com/user-attachments/assets/e70f9558-a24b-49a7-90ee-0295565f9f00" />

#### Cluster Architecture
- **Manager Nodes**: 3 nodes (High Availability configuration)
- **Worker Nodes**: 7 nodes
- **Total Nodes**: 10 nodes
- **Quorum**: 2 (minimum managers needed for operation)
- **Leader Election**: Automatic failover when leader fails
- **Manager Distribution**: Even distribution across different nodes

<img width="962" height="256" alt="image" src="https://github.com/user-attachments/assets/e9162308-7507-4a03-ab47-f43172f1ffb7" />

### c. Service Deployment Results
<img width="960" height="31" alt="image" src="https://github.com/user-attachments/assets/9262f463-7bfe-4685-b324-33f06ef2b8d5" />

<img width="960" height="89" alt="image" src="https://github.com/user-attachments/assets/6caab232-9118-42fd-8629-563fe702c131" />

### d. High Availability Configuration
<img width="964" height="95" alt="image" src="https://github.com/user-attachments/assets/d7fea6bd-e386-4b9a-b9d7-0694975af47e" />

#### Manager Node Configuration
- **3 Manager Nodes**: Ensures fault tolerance
- **Raft Consensus**: Distributed consensus algorithm
- **Automatic Failover**: Seamless leader election
- **Load Distribution**: Even workload distribution

### e. System Monitoring Results
<img width="891" height="269" alt="image" src="https://github.com/user-attachments/assets/c577af94-f7ac-4740-a518-4618f672009d" />

<img width="884" height="48" alt="image" src="https://github.com/user-attachments/assets/a0b28976-a4ab-462e-9af2-193cd64f991c" />

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

### Cluster Architecture
- **Manager Nodes**: 3 nodes (High Availability configuration)
- **Worker Nodes**: 7 nodes
- **Total Nodes**: 10 nodes
- **Quorum**: 2 (minimum managers needed for operation)
- **Leader Election**: Automatic failover when leader fails
- **Manager Distribution**: Even distribution across different nodes

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

#### Resource Monitoring
- CPU utilization tracking
- Memory usage monitoring
- Network I/O statistics
- Disk usage analytics

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
