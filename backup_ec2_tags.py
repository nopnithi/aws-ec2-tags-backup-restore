import boto3
import json
from datetime import datetime


def backup_ec2_tags(ec2_client):
    """
    This function backs up the tags for all EC2 instances in the AWS account.
    The tags are saved to a JSON file with a timestamp-based file name.

    Parameters:
    - ec2_client (boto3.client): An AWS client for the EC2 service.
    """
    # List all of the instances in your AWS account
    response = ec2_client.describe_instances()
    reservations = response['Reservations']
    while 'NextToken' in response:
        response = ec2_client.describe_instances(
            NextToken=response['NextToken']
        )
        reservations.extend(response['Reservations'])

    # Create a data structure to store the tags for all of the instances
    data = {'instances': []}

    # Iterate through each instance and add its ID and tags to the data structure
    for reservation in reservations:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            tags = instance.get('Tags', [])
            data['instances'].append({'instance_id': instance_id, 'tags': tags})

    # Convert the data structure to a JSON string
    json_data = json.dumps(data, indent=2)

    # Get the current timestamp and use it to generate a backup file name
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'ec2_tags_backup_{timestamp}.json'

    # Save the JSON string to a file
    with open(file_name, 'w') as f:
        f.write(json_data)


def main():
    ec2_client = boto3.client('ec2')
    backup_ec2_tags(ec2_client)


if __name__ == "__main__":
    main()
