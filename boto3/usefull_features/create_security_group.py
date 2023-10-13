"""
Create a security group and configure the rules of the group

See links...
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/authorize_security_group_ingress.html
"""

import boto3
import json


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
        self.name_id = {}
    
    def _init_security_group(
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
            msg = f"Testing to see if a security group with the name of\n"
            msg += f"{security_group_name} already exists..."
            print(msg)

            self.client.get_waiter('security_group_exists').wait(
                GroupNames=[
                    security_group_name,
                ],
                WaiterConfig={
                    'Delay': 10,
                    'MaxAttempts': 1
                }
            )
            print("The security group already existed")

            return None
        except:
            msg = f"The security group did not exist...\n"
            msg += f"Now initializing the security group"
            print(msg)
            try:
                sg_response = self.client.create_security_group(**sg_config)
        
                # If 200 then the status is OK.
                if sg_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print(f"The HTTPStatus of the security group is OK")
        
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

                    self.name_id[security_group_name] = sg_response['GroupId']
                    print("Sucess! The security group has been made")

            except Exception as e:
                msg = f"Failed to create the security group \n"
                msg += f"Either the HTTPStatus is not ok or the check to see if\n"
                msg += f"the security exists failed."
                print(msg)
                print(type(e), ":", e)
            
        if remove_default_rules:

            print("Now retrieving all default rules...")

            default_rules = self.client.describe_security_group_rules(
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [self.name_id[security_group_name]]
                    }
                ]
            )['SecurityGroupRules']

            print(f"There are {len(default_rules)} rules to remove.")

            if len(default_rules) > 0:

                print("Removing the default rules")
                
                for i, rule in enumerate(default_rules):
                    
                    ruleid = rule['SecurityGroupRuleId']
                    
                    try:
                        rr_response = self.client.revoke_security_group_egress(
                            GroupId= self.name_id[security_group_name],
                            SecurityGroupRuleIds=[ruleid]
                        )
                    except Exception as e1:
                        try:
                            rr_response = self.client.revoke_security_group_ingress(
                                GroupId= self.name_id[security_group_name],
                                SecurityGroupRuleIds=[ruleid]
                            )

                            print(f"Default Rule {i} successfully removed!")
                        except Exception as e2:
                            print("Both egress and ingress failed")
                            print(type(e1), "", e1)
                            print(type(e2), "", e2)

            rules_after_removal = self.client.describe_security_group_rules(
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [self.name_id[security_group_name]]
                    }
                ]
            )['SecurityGroupRules']

            try:
                if len(rules_after_removal) == 0:
                    msg=  f"Successfully removed all default rules\n"
                    msg += f"Now adding the new rules to the security group."
                    print(msg)
            except:
                print("Some default rules were not removed")


    def _add_rules_to_security_group(
        self,
        security_group_name,
        IpPermissions,
        dryrun=True
    ):

        try:
        
            sg_rules_config = {
                "GroupId": self.name_id[security_group_name],
                "IpPermissions": IpPermissions,
                "DryRun": dryrun,
            }
    
            try:
                sgri_response = self.client.authorize_security_group_ingress(
                    **sg_rules_config
                )
                if sgri_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print("The HTTPStatus of the ingress rules is OK")

                sgre_response = self.client.authorize_security_group_egress(
                    **sg_rules_config
                )
                if sgre_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print("The HTTPStatus of the egress rules is OK")

            except Exception as e:
                print("Some of the the IpPermissions were not successfully added.")
                print(type(e), ":", e)
            
            rules_after_addition = self.client.describe_security_group_rules(
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [self.name_id[security_group_name]]
                    }
                ]
            )['SecurityGroupRules']

            egress_after_add = [
                x for x in rules_after_addition if x["IsEgress"] == True
            ]
            ingress_after_add = [
                x for x in rules_after_addition if x["IsEgress"] == False
            ]
        
            try:
                if len(egress_after_add) == len(IpPermissions):
                    print("All egress rules were successfully added!")
            except:
                print("There was an error with adding the egress rules")

            try:
                if len(ingress_after_add) == len(IpPermissions):
                    print("All ingress rules were successfully added!")
            except:
                print("There was an error with adding the egress rules")

            print("Security group was successfully added")
        
        except Exception as e:
            print("The security group was NOT successfully added.")
            print(type(e), ":", e)


    def create_security_group(
        self,
        vpc_id,
        security_group_name,
        Ip_Permissions,
        dryrun=False
    ):

        self._init_security_group(
            vpc_id,
            security_group_name,
            dryrun=dryrun
        )

        self._add_rules_to_security_group(
            security_group_name,
            Ip_Permissions,
            dryrun=dryrun
        )

        return None


#--------------------------------------------------
# Test the class
#--------------------------------------------------


# get the access and secret keys to the aws account
with open("/home/nicholas/GitRepos/OFFLINE/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="nick",
    region_name="us-east-1"
)

# create the resource and the client
ec2_res = session.resource('ec2')
ec2_client = session.client("ec2", region_name="us-east-1")

vpc_id = ec2_client.describe_vpcs()['Vpcs'][0]['VpcId']
security_group_name = "testfromboto"

sec_group = SecurityGroup(
    session,
    ec2_client,
    ec2_res
)

IpPermissions = [
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
]

sec_group.create_security_group(
    vpc_id=vpc_id,
    security_group_name="test_from_boto_class",
    Ip_Permissions=IpPermissions
)
