# Backup and Restore EC2 Tags
This repository contains two Python scripts for backing up and restoring the tags on AWS (Amazon) EC2 instances. These scripts can be useful for scenarios where you need to modify the tags on your EC2 instances, but want to have the option to restore to the previous tag values if necessary.

- The `AWS Tag Editor` allows you to view and edit the tags on your AWS resources but it does not have the ability to create backups or restore of your tags.
- These scripts are designed to work specifically with EC2 instances and their tags. While it is possible to modify the code to work with other AWS resources that support tagging, this may require significant changes to the code.

## Prerequisites
- Python 3
- The boto3 modules
- AWS credentials with permissions to create tags on EC2 instances

## Installation
1. Install Python 3 if it is not already installed on your system.
2. Install the boto3 library:
```bash
pip install boto3
```
3. Set up your AWS credentials as environment variables.
```bash
export AWS_ACCESS_KEY_ID=<ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<SECRET_ACCESS_KEY>
export AWS_REGION=<REGION>
```

## Usage
### backup_ec2_tags.py
This script creates a JSON-formatted file that contains a list of all EC2 instances in the AWS account, along with their associated tags. The tags are saved to a file with a timestamp-based name.

To use this script, run the following command:
```bash
python backup_ec2_tags.py
```

### restore_ec2_tags.py
This script restores the tags on EC2 instances to their previous state by rolling back to a specific JSON-formatted file that was created by `backup_ec2_tags.py`.

To use this script, update the file name in the following line of code to the name of the backup file you want to use:
```bash
tag_data_file = '<tag-data-file>.json'
```

Then run the following command:
```bash
python restore_ec2_tags.py
```

The script will read the contents of the specified backup file and compare the tags in the file to the current tags on the EC2 instances. If the current tags are different from the ones in the backup file, the script will update the tags on the instance to match the ones in the backup file.
