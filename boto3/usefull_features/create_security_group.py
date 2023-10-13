"""
Create a security group and configure the rules of the group

See links...
for adding ingress or egress
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/authorize_security_group_ingress.html

for waiters
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceRunning.html#
"""

import boto3
import json


#--------------------------------------------------
# Create the security group
#--------------------------------------------------

class SecurityGroup:

    def __init__(
        self,
        vpc_id,
        session,
    ):
        self.vpc_id = vpc_id 
        self.session = session
        self.client = session.client("ec2", region_name=session.region_name)
        self.name_id = {}
        self.name_ingress_rules = {}
        self.name_egress_rules = {}
        self._init_name_id_dic()

    def _init_name_id_dic(self):
        try:
            for sg in sec_group.client.describe_security_groups()['SecurityGroups']:
                if sg['VpcId'] != self.vpc_id:
                    continue
                if sg['GroupName'] not in self.name_id.keys():
                    self.name_id[sg['GroupName']] = sg['GroupId']
            return None
        except:
            pass

    def make_name_permissions_dic(self):
        for name in self.name_id.keys():

            if name not in self.name_ingress_rules.keys():
                self.name_ingress_rules = {name: []}

            if name not in self.name_egress_rules.keys():
                self.name_egress_rules = {name: []}

            rules = self.client.describe_security_group_rules(
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [self.name_id[name]]
                    }
                ]
            )['SecurityGroupRules']

            egress_after_add = [
                x for x in rules if x["IsEgress"] == True
            ]
            ingress_after_add = [
                x for x in rules if x["IsEgress"] == False
            ]
    
    def _init_security_group(
        self, 
        security_group_name,
        remove_default_rules=True,
        dryrun=True
    ):

        sg_config = {
            "Description": 'A test sg',
            "GroupName": security_group_name,
            "VpcId": self.vpc_id,
            "DryRun": dryrun 
        }

        try:
            msg = f"Testing to see if a security group with the name of\n"
            msg += f"{security_group_name} already exists..."
            print(msg)

            if security_group_name in self.name_id.keys():
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

                    self.name_id[security_group_name] = sg_response['GroupId']
        
                    # Will return None if exists
                    self.client.get_waiter('security_group_exists').wait(
                        Filters=[
                            {
                                "Key": "vpc-id",
                                "Values": [self.vpc_id] 
                            }
                        ],
                        GroupIds=[self.name_id[security_group_name]],
                        # GroupNames=[
                        #     security_group_name,
                        # ],
                        WaiterConfig={
                            'Delay': 10,
                            'MaxAttempts': 2
                        }
                    )

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
        security_group_name,
        Ip_Permissions,
        dryrun=False
    ):

        self._init_security_group(
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

session.region_name

# create the resource and the client
ec2_res = session.resource('ec2')
ec2_client = session.client("ec2", region_name="us-east-1")


vpc_ids = {}
for vpc in ec2_client.describe_vpcs()['Vpcs']:
    try:
        for tag in vpc['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
    except:
        name = 'NotNamed'
    id = vpc['VpcId']
    vpc_ids[name] = id

vpc_ids

security_group_name = "testfrombotoclass"

sec_group = SecurityGroup(
    vpc_id=vpc_ids['copysteps-vpc'],
    session=session,
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
    vpc_id=vpc_ids['copysteps-vpc'],
    security_group_name="copystep-sg",
    Ip_Permissions=IpPermissions
)




security_group_name

vpc_ids['copysteps-vpc']

sec_group_ids = {}
for sg in sec_group.client.describe_security_groups()['SecurityGroups']:
    sec_group_ids[sg['VpcId']] = {
        "GroupId"sg['GroupId']
    }


sec_group.client.describe_security_groups()['SecurityGroups'][0].keys()

sec_group.client.describe_security_groups()['SecurityGroups'][0]['IpPermissions']

sec_group.name_id

default_rules = sec_group.client.describe_security_group_rules(
    Filters=[
        {
            "Name": "group-id",
            "Values": [sec_group.name_id['copystep-sg']]
        }
    ]
)['SecurityGroupRules']


x  = []
for sg in sec_group.client.describe_security_groups()['SecurityGroups']:
    if sg['GroupName'] == 'copystep-sg':
        x.append(sg)

len(x[0]['IpPermissions'])

x[0]['IpPermissionsEgress']

default_rules[1]






