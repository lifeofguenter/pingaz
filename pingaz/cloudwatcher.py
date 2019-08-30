import datetime

import boto3


def put(results):
    timestamp = datetime.datetime.now(datetime.timezone.utc)

    metrics = []

    for host, result in results.items():
        if not result:
            continue

        metrics += [
            {
                'MetricName': 'latency',
                'Dimensions': [
                    {
                        'Name': 'Host',
                        'Value': host,
                    },
                ],
                'Timestamp': timestamp,
                'Value': result['latency'],
                'Unit': 'Milliseconds',
                'StorageResolution': 60
            },
            {
                'MetricName': 'loss',
                'Dimensions': [
                    {
                        'Name': 'Host',
                        'Value': host,
                    },
                ],
                'Timestamp': timestamp,
                'Value': result['loss'],
                'Unit': 'Percent',
                'StorageResolution': 60
            },
        ]

    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(
        Namespace='Tidal/PingAZ',
        MetricData=metrics,
    )
