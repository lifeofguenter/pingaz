import datetime

import boto3
from ec2_metadata import ec2_metadata


def put(results):
    timestamp = datetime.datetime.now(datetime.timezone.utc)

    metrics = []

    for host, result in results.items():
        if not result:
            continue

        dimensions = [
            {
                'Name': 'Host',
                'Value': result['name'],
            },
            {
                'Name': 'SourceAZ',
                'Value': ec2_metadata.availability_zone,
            },
            {
                'Name': 'SourceInstanceId',
                'Value': ec2_metadata.instance_id,
            },
        ]

        metrics += [
            {
                'MetricName': 'latency',
                'Dimensions': dimensions,
                'Timestamp': timestamp,
                'Value': result['latency'],
                'Unit': 'Milliseconds',
                'StorageResolution': 60
            },
            {
                'MetricName': 'loss',
                'Dimensions': dimensions,
                'Timestamp': timestamp,
                'Value': result['loss'],
                'Unit': 'Percent',
                'StorageResolution': 60
            },
        ]

    cloudwatch = boto3.client('cloudwatch', region_name=ec2_metadata.region)
    cloudwatch.put_metric_data(
        Namespace='Tidal/PingAZ',
        MetricData=metrics,
    )
