"""
VPC and more from the aws consol
"""

class VPC:

    def __init__(
        self,
        session
        ):
        self.session = session
        self.client = session.client("vpc", region_name=session.region_name)

    def _make_vpc(self, vpc_config): 
        
        response = self.client.create_vpc(
            **vpc_config
        )

        return response

    def _make_igw(self, igw_config):
        response = self.client.create_internet_gateway(
            **igw_config
        )

        return response

    def _attach_igw(self, igw_id, vpc_id):

        response = self.session.resource('ec2').Vpc(vpc_id).attach_internet_gateway(
            InternetGatewayId=igw_id
        )

        return response

    def _make_subnet(self, vpc_id, subnet_config):
        response = self.session.resource('ec2').Vpc(vpc_id).create_subnet(
            **subnet_config
        )

        return response

    def _create_route_table(self, rt_config):

        response = self.client.create_route_table(**rt_config)

        return response


    def _create_route(self, cr_config):
        response = self.client.create_route(**cr_config)

        return response
    

    def _associate_route_table(self, **art_config):

        response = self.client.associate_route_table(**art_config)

        return response
