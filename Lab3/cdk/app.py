#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack

app = cdk.App()

CdkStack(
    app,
    "WebAppStack",
    # Uncomment and fill in to target a specific account/region:
    # env=cdk.Environment(
    #     account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    #     region=os.getenv("CDK_DEFAULT_REGION"),
    # ),
    description="Private S3 bucket + CloudFront distribution for web app hosting",
)

app.synth()
