import sys
import boto3
from botocore.exceptions import ClientError

ec2_instance_id = sys.argv[2]
ec2_instance_state = sys.argv[1].upper()

ec2_instance = boto3.client('ec2')


if ec2_instance_state == 'ON':
    # dryrun the instance first to verify permissions 
    try:
        ec2_instance.start_instances(InstanceIds=[ec2_instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # permission succeeded, run start_instances without dryrun
    try:
        response = ec2_instance.start_instances(InstanceIds=[ec2_instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)
else:
    # dryrun the instance first to verify permissions
    try:
        ec2_instance.stop_instances(InstanceIds=[ec2_instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2_instance.stop_instances(InstanceIds=[ec2_instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)
