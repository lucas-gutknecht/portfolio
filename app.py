#!/usr/bin/env python3
import os

import aws_cdk as cdk
import configparser

from portfolio.portfolio_stack import PortfolioStack


app = cdk.App()
env = app.node.try_get_context("env")

config = configparser.ConfigParser()
config.read(f"./config/{env}.ini")
params = config["parameters"]
environ = config["environment"]

PortfolioStack(
    app,
    "stack",
    env=cdk.Environment(account=environ.get("AccountId"),
                        region=environ.get("region")),
    configuration=params,
    stack_name="portfolio-api-stack",
)


app.synth()
