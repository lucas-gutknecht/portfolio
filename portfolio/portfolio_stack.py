from aws_cdk import (
    Size,
    aws_iam as iam,
    aws_lambda as lambda_,
    Stack,
    Duration,
    aws_ec2 as ec2,
    aws_apigateway as apigateway,
    aws_certificatemanager as certificatemanager,
    aws_route53 as route53,
    aws_route53_targets as targets,
)
from constructs import Construct

from . import iam, resources

class PortfolioStack(Stack):
    """Portfolio Stack for deploying the portfolio API."""
    def __init__(
        self, scope: Construct, construct_id: str, configuration, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        role = iam.create_role(
            self, "PortfolioExecutionRole", configuration=configuration
        )
        
        resources.create_app(
            self, "PortfolioExecutionRole", configuration=configuration, lambda_role=role
        )
        
        
