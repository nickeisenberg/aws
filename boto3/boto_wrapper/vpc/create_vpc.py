"""
VPC and more from the aws consol
"""

import boto3

client = session.client("vpc", region_name=session.region_name)

class VPC:

    def __init__(
        self,
        session
        ):
        self.session = session
        self.client = session.client("vpc", region_name=session.region_name)

    def _make_vpc(self, vpc_config): 
        
        response = client.create_vpc(
            **vpc_config
        )

        return response

    def make_igw(self, igw_config):
        response = client.create_internet_gateway(
            **igw_config
        )

        return response

    def _attach_igw(self, igw_id, vpc_id):

        response = self.session.resource('ec2').Vpc(vpc_id).attach_internet_gateway(
            InternetGatewayId=igw_id
        )

        return response

    def _make_subnet(self, subnet_config):



