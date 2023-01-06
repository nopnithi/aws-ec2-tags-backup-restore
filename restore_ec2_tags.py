import boto3
import json


def check_ec2_instance_exists(ec2_client, instance_id):
    """
    This function checks if an EC2 instance with the specified ID exists in the AWS account.

    Parameters:
    - ec2_client (boto3.client): An AWS client for the EC2 service.
    - instance_id (str): The ID of the EC2 instance to check.

    Returns:
    - bool: True if the instance exists, False if it does not.
    """
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    # Check if any instances were returned
    if response['Reservations']:
        return True
    return False


def restore_ec2_tags(ec2_client, tag_data_file):
    """
    This function restores the tags on EC2 instances to their previous state by rolling back to a backup file.

    Parameters:
    - ec2_client (boto3.client): An AWS client for the EC2 service.
    - tag_data_file (str): A JSON file name that contains a list of all EC2 instances, along with their associated tags.
    """
    # Load the JSON input from a file
    with open(tag_data_file, 'r') as f:
        input_data = json.load(f)

    # Iterate through each instance in the input
    for instance in input_data['instances']:
        instance_id = instance['instance_id']
        backup_tags = instance['tags']
        print(f'Instance ID: {instance_id}')

        if check_ec2_instance_exists(ec2_client, instance_id):
            # Get the current tags for the instance
            current_tags = ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [instance_id]}]).get('Tags', [])

            # Create a dictionary to store the current keys and values of the tags
            current_tag_dict = {}
            for tag in current_tags:
                current_tag_dict[tag['Key']] = tag['Value']

            # Iterate through each tag in the backup tags
            for backup_tag in backup_tags:
                backup_key = backup_tag.get('Key')
                backup_value = backup_tag.get('Value')
                # If the tag is not present on the instance, create it
                if backup_key not in current_tag_dict:
                    print(f' - Added tag: "{backup_key}:{backup_value}"')
                    ec2_client.create_tags(Resources=[instance_id], Tags=[{'Key': backup_key, 'Value': backup_value}])
                # If the tag is present on the instance but has a different value, update it
                elif current_tag_dict[backup_key] != backup_value:
                    print(f' - Updated tag: "{backup_key}:{backup_value}"')
                    ec2_client.create_tags(Resources=[instance_id], Tags=[{'Key': backup_key, 'Value': backup_value}])

            # Delete any tags that are present on the instance but not in the backup tags
            for current_tag_key, current_tag_value in current_tag_dict.items():
                if current_tag_key not in [backup_tag['Key'] for backup_tag in backup_tags]:
                    print(f' - Deleted tag: "{current_tag_key}:{current_tag_value}"')
                    ec2_client.delete_tags(Resources=[instance_id], Tags=[{'Key': current_tag_key}])
        else:
            print(f' - Skipped, instance does not exist')


def main():
    tag_data_file = '<tag-data-file>.json'
    ec2_client = boto3.client('ec2')
    restore_ec2_tags(ec2_client, tag_data_file)


if __name__ == "__main__":
    main()
