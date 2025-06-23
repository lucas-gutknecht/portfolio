from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    aws_lambda as lambda_,
    Size,
    Duration,
    aws_ec2 as ec2,
    # aws_lambda_event_sources as eventsources,
    aws_apigateway as apigateway,
    aws_certificatemanager as certificatemanager,
    aws_route53 as route53,
    aws_route53_targets as targets,
)


def create_app(scope: Construct, id: str, configuration: any, lambda_role):

    api = apigateway.RestApi(
        scope,
        "portfolio-api-gw",
        rest_api_name="portfolio-api-gateway",
        description="API that serves professional portfolio.",
        binary_media_types=["image/jpeg", "image/png", "image/*",
                            "application/octet-stream", "application/pdf", 
                            "video/mp4", "application/*"],
        deploy_options=apigateway.StageOptions(stage_name="prod"),
    )

    portfolio_lambda_layer = lambda_.LayerVersion(
        scope,
        "Portfolio-Lambda-Layer",
        code=lambda_.Code.from_asset(path="lambda_layer"),
        compatible_runtimes=[lambda_.Runtime.PYTHON_3_11],
        description="supporting libs for portfolio lambda",
        layer_version_name="portfolio-lambda-layer",
    )

    portfolio_lambda = lambda_.Function(
        scope,
        "lambda",
        runtime=lambda_.Runtime.PYTHON_3_11,
        handler="main.lambda_handler",
        code=lambda_.Code.from_asset(path="lambda_code"),
        role=lambda_role,
        function_name="portfolio-lambda",
        architecture=lambda_.Architecture.X86_64,
        timeout=Duration.minutes(15),
        ephemeral_storage_size=Size.mebibytes(4096),
        memory_size=2048,
        layers=[portfolio_lambda_layer],
        environment={
            "test": "test",
        },
        # vpc=my_vpc,
        # security_groups=[my_security_group],
        # vpc_subnets=ec2.SubnetSelection(
        #    subnets=[my_subnet_1, my_subnet_2, my_subnet_3, my_subnet_4]
        # ),
    )

    # Add a catch-all proxy resource
    proxy_resource = api.root.add_resource("{proxy+}")

    proxy_resource.add_method(
        "ANY", apigateway.LambdaIntegration(portfolio_lambda))

    api.root.add_method(
        "ANY", apigateway.LambdaIntegration(portfolio_lambda)
    )

    hosted_zone = route53.HostedZone.from_lookup(
        scope,
        "HostedZone",
        domain_name=configuration.get("zone_name"),
    )
    """
    cert = certificatemanager.Certificate(
        scope,
        "PortfolioCertificate",
        domain_name=configuration.get("domain_name"),
        validation=certificatemanager.CertificateValidation.from_dns(
            hosted_zone),
    )
    """

    cert = certificatemanager.Certificate.from_certificate_arn(
        scope,
        "Certificate",
        certificate_arn=configuration.get("certificate"),
    )

    # Use this certificate for your API Gateway custom domain
    domain_name = apigateway.DomainName(
        scope,
        'DomainName',
        # mapping=api,
        certificate=cert,
        domain_name=configuration.get("domain_name"),
    )

    apigateway.BasePathMapping(
        scope,
        "BasePathMapping",
        domain_name=domain_name,
        rest_api=api,
        stage=api.deployment_stage,
        base_path="",
    )

    # add IPV4 record to hosted zone
    route53.ARecord(scope,
                    "Arecord",
                    zone=hosted_zone,
                    target=route53.RecordTarget.from_alias(
                        targets.ApiGatewayDomain(domain_name)),
                    record_name="www",
                    )
    
