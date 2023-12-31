"""
Create a security group and configure the rules of the group

See links...
for adding ingress or egress
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/authorize_security_group_ingress.html

for waiters
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceRunning.html#
"""

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
        self._init_permissions_dic()

    def _init_name_id_dic(self):
        try:
            for sg in self.client.describe_security_groups()['SecurityGroups']:
                if sg['VpcId'] != self.vpc_id:
                    continue
                if sg['GroupName'] not in self.name_id.keys():
                    self.name_id[sg['GroupName']] = sg['GroupId']
            return None
        except:
            pass

        return None

    def _init_permissions_dic(self):

        self.name_ingress_rules = {name: [] for name in self.name_id.keys()}
        self.name_egress_rules = {name: [] for name in self.name_id.keys()}

        for name in self.name_id.keys():

            rules = self.client.describe_security_group_rules(
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [self.name_id[name]]
                    }
                ]
            )['SecurityGroupRules']

            if len(rules) > 0:

                self.name_ingress_rules[name] = [
                    x for x in rules if x["IsEgress"] == True
                ]
                self.name_egress_rules[name] = [
                    x for x in rules if x["IsEgress"] == False
                ]
        
        return None

    def update_permissions_dic(self, name):
        if name not in self.name_id.keys():
            msg = "The ID of this security group has not been recorded\n"
            msg += "Update the SecurityGroup.name_id with the corresponding pair"
            raise Exception(msg)

        rules = self.client.describe_security_group_rules(
            Filters=[
                {
                    "Name": "group-id",
                    "Values": [self.name_id[name]]
                }
            ]
        )['SecurityGroupRules']

        self.name_ingress_rules[name] = [
            x for x in rules if x["IsEgress"] == True
        ]
        self.name_egress_rules[name] = [
            x for x in rules if x["IsEgress"] == False
        ]

        return None

    
    def _init_security_group(
        self, 
        sg_config: dict,
        remove_default_rules=True,
    ):
        """
        Parameters
        ----------
        sg_config: dict
            The **kwargs for boto3.EC2.Client.create_security_group(**kwargs)
        remove_default_rules: boolean
            Remove the default rules that are auto set when creating a new 
            security group.
        """

        try:
            msg = f"Testing to see if {sg_config['GroupName']} already exists..."
            print(msg)

            _ = self.name_id[sg_config['GroupName']]

            print("The security group already existed")

            return False

        except:
            msg = f"The security group did not exist...\n"
            msg += f"Now initializing the security group"
            print(msg)
            try:
                sg_response = self.client.create_security_group(**sg_config)
        
                if sg_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print(f"The HTTPStatus of the security group is OK")

                    self.name_id[sg_config['GroupName']] = sg_response['GroupId']
        
                    # Will return None if exists
                    self.client.get_waiter('security_group_exists').wait(
                        Filters=[
                            {
                                "Name": "vpc-id",
                                "Values": [self.vpc_id] 
                            }
                        ],
                        GroupIds=[self.name_id[sg_config['GroupName']]],
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

                return False
            
        if remove_default_rules:

            print("Now retrieving all default rules...")


            self.update_permissions_dic(sg_config['GroupName'])

            default_rules = self.name_egress_rules[sg_config['GroupName']]
            default_rules += self.name_ingress_rules[sg_config['GroupName']]

            print(f"There are {len(default_rules)} rules to remove.")

            if len(default_rules) > 0:

                print("Removing the default rules")
                
                for i, rule in enumerate(default_rules):
                    
                    ruleid = rule['SecurityGroupRuleId']
                    
                    try:
                        rr_response = self.client.revoke_security_group_egress(
                            GroupId= self.name_id[sg_config['GroupName']],
                            SecurityGroupRuleIds=[ruleid]
                        )
                    except Exception as e1:
                        try:
                            rr_response = self.client.revoke_security_group_ingress(
                                GroupId= self.name_id[sg_config['GroupName']],
                                SecurityGroupRuleIds=[ruleid]
                            )

                            print(f"Default Rule {i} successfully removed!")
                        except Exception as e2:
                            print("Both egress and ingress failed")
                            print(type(e1), "", e1)
                            print(type(e2), "", e2)
                            return False

            self.update_permissions_dic(sg_config['GroupName'])


            rules_after_removal = self.name_egress_rules[sg_config['GroupName']]
            rules_after_removal += self.name_ingress_rules[sg_config['GroupName']]

            try:
                if len(rules_after_removal) == 0:
                    msg=  f"Successfully removed all default rules\n"
                    print(msg)

                    return True
            except:
                print("Some default rules were not removed")
                return False


    def _add_rules_to_security_group(
        self,
        security_group_name,
        ingress_config,
        egress_config
    ):
        """
        Parameters
        ----------
        security_group_name: str
            The name of the security group
        ingress_config: dict 
            The kwargs client.authorize_security_group_ingress(**ingress_config)
            Do not enter the group name into the dictionary though.
        egress_config: dict 
            The kwargs client.authorize_security_group_egress(**egress_config)
            Do not enter the group name into the dictionary though.
        """

        print(f"Now adding the new rules to the security group.")
        try:

            ingress_config["GroupId"] = self.name_id[security_group_name]
            egress_config["GroupId"] = self.name_id[security_group_name]
    
            try:
                sgri_response = self.client.authorize_security_group_ingress(
                    **ingress_config
                )
                if sgri_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print("The HTTPStatus of the ingress rules is OK")

                sgre_response = self.client.authorize_security_group_egress(
                    **egress_config
                )
                if sgre_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print("The HTTPStatus of the egress rules is OK")

            except Exception as e:

                print("Some of the the IpPermissions were not successfully added.")
                print(type(e), ":", e)

                return None
            

            self.update_permissions_dic(security_group_name)
        
            try:

                if len(
                    self.name_ingress_rules[security_group_name]
                ) == len(ingress_config['IpPermissions']):

                    print("All egress rules were successfully added!")

            except:

                print("There was an error with adding the egress rules")

            try:

                if len(
                    self.name_egress_rules[security_group_name]
                ) == len(egress_config["IpPermissions"]):

                    print("All ingress rules were successfully added!")

            except:

                print("There was an error with adding the egress rules")

            print("Security group was successfully added")
        
        except Exception as e:
            print("The security group was NOT successfully added.")
            print(type(e), ":", e)


    def create_security_group(
        self,
        sg_config,
        ingress_config,
        egress_config,
    ):

        moveon = self._init_security_group(
            sg_config,
        )
    
        if moveon:
            self._add_rules_to_security_group(
                sg_config['GroupName'],
                ingress_config,
                egress_config,
            )

        return None
