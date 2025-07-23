# Chapter 1: Introduction

## Project Background

In the context of rapidly evolving information technology, microservices architecture has become a significant trend, enabling the development of flexible, scalable, and maintainable software systems. However, the complexity of managing and monitoring independent services requires effective solutions to ensure system performance and reliability. Docker Swarm, as a powerful orchestration tool, combined with monitoring tools such as ELK Stack, Prometheus, Grafana, InfluxDB, and Reverse Proxy (Nginx), provides an ideal platform for deploying and optimizing microservices systems.

## Project Objectives

This report presents the deployment, monitoring, and optimization process of the MrNamCoinSwarm software system based on microservices architecture, using Docker Swarm as the orchestration platform. The main objectives are:

### Primary Goals
- Establish a stable system
- Collect and analyze important metrics including:
  - CPU Usage
  - Memory Usage
  - Network I/O
  - Block I/O
- Implement efficient log management for timely issue detection and resolution

### Technology Stack
- **ELK Stack**: Used for log processing and visualization
- **Prometheus, Grafana, and InfluxDB**: Support monitoring and long-term metrics storage
- **Nginx Reverse Proxy**: Deployed to optimize access to services

## Project Scope

The report focuses on describing in detail the deployment process of system components, including:

1. **ELK Stack Configuration**
   - Logstash setup and configuration
   - Elasticsearch deployment
   - Kibana dashboard creation

2. **Monitoring Pipeline Setup**
   - Prometheus metrics collection
   - Grafana visualization
   - InfluxDB long-term storage

3. **System Analysis**
   - Monitoring results analysis
   - Optimization method proposals
   - System effectiveness evaluation based on established criteria

## Expected Outcomes

- Fully functional microservices system running on Docker Swarm
- Comprehensive monitoring and logging infrastructure
- Performance optimization recommendations
- Detailed documentation for future maintenance and scaling

## Document Structure

This documentation is organized into logical chapters that guide readers through the complete system deployment and monitoring process, from initial setup to performance evaluation and optimization recommendations.
