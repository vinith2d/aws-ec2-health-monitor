# AWS EC2 Health Monitoring using Python and AWS CLI

This project monitors AWS EC2 instance health using Python and AWS CLI.
It retrieves instance details and CPU utilization metrics from AWS CloudWatch.

## Features
- Fetch EC2 instance status
- Retrieve CPU utilization metrics
- Basic alert for high CPU usage
- Uses Python automation with AWS CLI

## Technologies Used
- Python
- AWS CLI
- AWS EC2
- AWS CloudWatch

## How It Works
The Python script executes AWS CLI commands, parses JSON output, and displays
instance health and performance metrics.

## Prerequisites
- AWS Account
- AWS CLI configured
- Python 3.x

## Run the Script
```bash
python ec2_monitor.py
