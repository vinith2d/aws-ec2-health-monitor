import subprocess
import json
from datetime import datetime, timedelta


def run_command(command):
    """
    Runs an AWS CLI command and returns parsed JSON output.
    """
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Command failed:", result.stderr)
        return None
    return json.loads(result.stdout)


print("\n==============================")
print(" AWS EC2 HEALTH MONITOR ")
print("==============================")

# Get AWS region
region_cmd = ["aws", "configure", "get", "region"]
region_result = subprocess.run(region_cmd, capture_output=True, text=True)
region = region_result.stdout.strip()

print(f"AWS Region: {region}\n")

# Get EC2 instances
instances_data = run_command(["aws", "ec2", "describe-instances"])

if not instances_data:
    print("Unable to fetch EC2 instances.")
    exit(1)

for reservation in instances_data["Reservations"]:
    for instance in reservation["Instances"]:
        instance_id = instance["InstanceId"]
        instance_type = instance["InstanceType"]
        state = instance["State"]["Name"]

        # Get instance Name tag
        name = "N/A"
        if "Tags" in instance:
            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    name = tag["Value"]

        # Time range for CloudWatch metrics (last 10 minutes)
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=10)

        start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # CloudWatch CPU Utilization command
        cpu_command = [
            "aws", "cloudwatch", "get-metric-statistics",
            "--namespace", "AWS/EC2",
            "--metric-name", "CPUUtilization",
            "--dimensions", f"Name=InstanceId,Value={instance_id}",
            "--start-time", start,
            "--end-time", end,
            "--period", "300",
            "--statistics", "Average"
        ]

        cpu_data = run_command(cpu_command)

        cpu_usage = "No data"
        if cpu_data and cpu_data["Datapoints"]:
            cpu_usage = round(cpu_data["Datapoints"][0]["Average"], 2)

        # Output
        print(f"Instance ID : {instance_id}")
        print(f"Name        : {name}")
        print(f"Type        : {instance_type}")
        print(f"State       : {state}")
        print(f"CPU Usage   : {cpu_usage}%")

        # Alert logic
        if cpu_usage != "No data" and cpu_usage > 70:
            print("⚠ ALERT: High CPU Utilization")

        print("-" * 40)
