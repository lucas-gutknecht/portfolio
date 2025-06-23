from constructs import Construct
from aws_cdk import (
    aws_iam as iam
)


def create_role(scope: Construct, id: str, configuration: any) -> iam.Role:

        portfolio_exection_role = iam.Role(
            scope=scope,
            id="portfolio-execution-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name=configuration.get("portfolio_execution_role"),
            )

        # Policy statement for s3.
        policy_statement = iam.PolicyStatement()
        policy_statement.effect = iam.Effect.ALLOW

        policy_statement.add_actions("s3:GetObject")

        policy = iam.ManagedPolicy(
            scope=scope,
            id="portfolio-execution-s3-policy",
            managed_policy_name="portfolio-execution-s3-policy",
            statements=[policy_statement],
        )

        policy_statement.add_resources(
            f"arn:aws:s3:::portfolio-gutknecht")
        policy_statement.add_resources(
            f"arn:aws:s3:::portfolio-gutknecht/*")

        portfolio_exection_role.add_managed_policy(policy)

        # Policy statement for Lambda.
        portfolio_exection_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaVPCAccessExecutionRole")
        )
        
        return portfolio_exection_role
