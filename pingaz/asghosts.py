import boto3
from ec2_metadata import ec2_metadata

def get_autoscaling_group_name(client):
    response = client.describe_tags(
        Filters=[
            {
                'Name': 'resource-id',
                'Values': [ec2_metadata.instance_id]
            },
        ],
    )

    for tag in response['Tags']:
        if tag['Key'] == 'aws:autoscaling:groupName':
            return tag['Value']


def find():
    client = boto3.client('ec2', region_name=ec2_metadata.region)

    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:aws:autoscaling:groupName',
                'Values': [get_autoscaling_group_name(client)]
            },
        ],
    )

    hosts = []
    for instance in response['Reservations'][0]['Instances']:
        # skip self
        if instance['InstanceId'] == ec2_metadata.instance_id:
            continue

        hosts += [{
            'name': instance['Placement']['AvailabilityZone'],
            'host': instance['NetworkInterfaces'][0]['PrivateIpAddress']
        }]

    return hosts
