"""
Create a security group and configure the rules of the group

See links...
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/authorize_security_group_ingress.html
"""

import boto3
import json

# get the access and secret keys to the aws account
with open("/home/nicholas/GitRepos/OFFLINE/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

# start the session
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="nick",
    region_name="us-east-1"
)

# create the resource and the client
ec2_res = session.resource('ec2')
ec2_client = session.client("ec2", region_name="us-east-1")

vpcid = ec2_client.describe_vpcs()['Vpcs'][0]['VpcId']
security_group_name = "testfromboto"

sg_config = {
    "Description": 'A test sg',
    "GroupName": security_group_name,
    "VpcId": vpcid,
    "DryRun": False 
}

#--------------------------------------------------
# Create the security group
#--------------------------------------------------

class SecurityGroup:

    def __init__(
        self,
        session,
        client,
        resource,
    ):
        self.session = session
        self.client = client
        self.resource = resource
    
    def _make_security_group(
        self, 
        vpc_id,
        security_group_name,
        remove_default_rules=True,
        dryrun=True
    ):

        sg_config = {
            "Description": 'A test sg',
            "GroupName": security_group_name,
            "VpcId": vpc_id,
            "DryRun": dryrun 
        }

        try:
            self.client.get_waiter('security_group_exists').wait(
                GroupNames=[
                    security_group_name,
                ],
                WaiterConfig={
                    'Delay': 10,
                    'MaxAttempts': 1
                }
            )
            print("A security group with that name already exists")    
        except:
            print("The security group did not exist...")
            print("Now creating the security group...")
            try:
                self.sg_response = self.client.create_security_group(**sg_config)
        
                # If 200 then the status is OK.
                if self.sg_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print("The Status of the security group is OK")
        
                    # Will return None if exists
                    self.client.get_waiter('security_group_exists').wait(
                        GroupNames=[
                            security_group_name,
                        ],
                        WaiterConfig={
                            'Delay': 10,
                            'MaxAttempts': 2
                        }
                    )
                    print("Sucess! The security group has been made")
            except Exception as e:
                print("Failed to create the security group")
                print(type(e), ":", e)
            
        if remove_default_rules:

            default_rules = self.client.describe_security_group_rules(
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [self.sg_response['GroupId']]
                    }
                ]
            )['SecurityGroupRules']

            if len(default_rules) > 0:

                print("Removing the default rules")
                
                for rule in default_rules:
                    
                    ruleid = rule['SecurityGroupRuleId']
                    
                    try:
                        rr_response = self.client.revoke_security_group_egress(
                            GroupId= self.sg_response['GroupId'],
                            SecurityGroupRuleIds=[ruleid]
                        )
                    except Exception as e1:
                        try:
                            rr_response = self.client.revoke_security_group_ingress(
                                GroupId= self.sg_response['GroupId'],
                                SecurityGroupRuleIds=[ruleid]
                            )

                            print("Default Rule successfully removed!")
                        except Exception as e2:
                            print("Both egress and ingress failed")
                            print(type(e1), "", e1)
                            print(type(e2), "", e2)

            rules_after_removal = self.client.describe_security_group_rules(
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [self.sg_response['GroupId']]
                    }
                ]
            )['SecurityGroupRules']

            try:
                if len(rules_after_removal) == 0:
                    print("Successfully removed all default rules")
                    print("Now adding the new rules to the security group.")
            except:
                print("Some default rules were not removed")


    def _add_rules_to_security_group(self):

        try:
        
            sg_rules_config = {
                "GroupId": self.sg_response['GroupId'],
                "IpPermissions":[
                    {
                        'FromPort': 22,
                        'IpProtocol': 'tcp',
                        'IpRanges': [
                            {
                                'CidrIp': '0.0.0.0/0',
                                'Description': 'Allow SSH from everywhere'
                            },
                        ],
                        'ToPort': 22,
                    },
                    {
                        'FromPort': -1,
                        'IpProtocol': 'icmp',
                        'IpRanges': [
                            {
                                'CidrIp': '0.0.0.0/0',
                                'Description': 'Allow ping from everywhere'
                            },
                        ],
                        'ToPort': -1,
                    },
                ],
                "DryRun": False,
            }
            
            sgri_response = self.client.authorize_security_group_ingress(**sg_rules_config)
            if sgri_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("The Status of the ingress rules is OK")

            sgre_response = self.client.authorize_security_group_egress(**sg_rules_config)
            if sgre_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("The Status of the egress rules is OK")
            
            rules_after_addition = self.client.describe_security_group_rules(
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [self.sg_response['GroupId']]
                    }
                ]
            )['SecurityGroupRules']
        
            try:
                if len(rules_after_addition) == 4:
                    print("All rules were successfully added")
            except:
                print("There was an error with adding the rules")
        
        
        except Exception as e:
            print("The rules did not add")
            print(type(e), ":", e)


    def create_security_group(self, security_group_name):

        self._make_security_group(security_group_name)

        self._add_rules_to_security_group()

        return None

