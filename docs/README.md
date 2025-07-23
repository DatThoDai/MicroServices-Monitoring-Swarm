# MrNamCoinSwarm System Documentation

## Overview

This documentation describes the deployment, monitoring, and optimization of the MrNamCoinSwarm software system based on microservices architecture, using Docker Swarm as the orchestration platform.

![System Overview](assets/system-overview.png)

## Table of Contents

1. [Introduction](01-introduction.md) - Project overview and objectives
2. [Reverse Proxy Concepts](02-reverse-proxy-concepts.md) - Theoretical background on Reverse Proxy
3. [System Architecture Overview](03-system-overview.md) - MrNamCoinSwarm system architecture
4. [ELK Stack Deployment](04-elk-stack.md) - Elasticsearch, Logstash, and Kibana setup
5. [Monitoring Stack Deployment](05-monitoring-stack.md) - Prometheus, Grafana, and InfluxDB setup
6. [Reverse Proxy Implementation](06-reverse-proxy-implementation.md) - Nginx Reverse Proxy deployment
7. [Monitoring and Optimization](07-monitoring-optimization.md) - System monitoring and performance optimization
8. [Results and Evaluation](08-results-evaluation.md) - Final results and system evaluation

## System Components

- **Docker Swarm**: Container orchestration platform
- **ELK Stack**: Centralized logging (Elasticsearch, Logstash, Kibana)
- **Monitoring Stack**: Metrics collection and visualization (Prometheus, Grafana, InfluxDB)
- **Reverse Proxy**: Load balancing and routing (Nginx)
- **DockerCoins Services**: Microservices application (WebUI, RNG, Hasher, Worker, Redis)

## Quick Start

1. Review the [system architecture](03-system-overview.md)
2. Follow the deployment guides in order (chapters 4-6)
3. Configure monitoring as described in [chapter 7](07-monitoring-optimization.md)
4. Review performance results in [chapter 8](08-results-evaluation.md)

## Requirements

- Docker Swarm cluster (10 nodes: 3 managers, 7 workers)
- Network: 192.168.10.x/24
- Resources: Minimum 2GB RAM per node
- OS: Linux-based systems

## Assets and Images

All screenshots, diagrams, and visual documentation are stored in the `assets/` directory. Each chapter references relevant images that demonstrate:

- System architecture diagrams
- Configuration screenshots
- Dashboard visualizations
- Monitoring metrics
- Performance analysis results

### Image Placeholders

The documentation includes placeholders for the following image categories:
- **Architecture Diagrams**: System topology and component relationships
- **Configuration Screenshots**: Setup and deployment evidence
- **Dashboard Images**: Grafana, Kibana, and monitoring interfaces
- **Performance Metrics**: CPU, memory, network, and storage analytics
- **Network Topology**: Docker Swarm cluster visualization

## Authors

Project developed as part of Big Data coursework demonstrating microservices orchestration and monitoring capabilities.
