import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3deploy,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ── 1. Private S3 bucket (no public access) ──────────────────────────
        website_bucket = s3.Bucket(
            self,
            "WebsiteBucket",
            # Block all public access – content is served exclusively via CloudFront
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            # Enforce HTTPS-only access to the bucket
            enforce_ssl=True,
            # Enable versioning for easier rollbacks
            versioned=True,
            # Automatically remove bucket on stack deletion (change to RETAIN for production)
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # ── 2. CloudFront Origin Access Control (OAC) ────────────────────────
        # OAC is the recommended replacement for the legacy Origin Access Identity (OAI).
        oac = cloudfront.S3OriginAccessControl(
            self,
            "WebsiteOAC",
            description="OAC for private S3 website bucket",
            signing=cloudfront.Signing.SIGV4_NO_OVERRIDE,
        )

        # ── 3. CloudFront distribution ────────────────────────────────────────
        distribution = cloudfront.Distribution(
            self,
            "WebsiteDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(
                    website_bucket,
                    origin_access_control=oac,
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                compress=True,
            ),
            # Serve index.html for the root path
            default_root_object="index.html",
            # Return index.html for 403/404 to support single-page applications
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=cdk.Duration.seconds(0),
                ),
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=cdk.Duration.seconds(0),
                ),
            ],
            # Enable HTTP/2 and HTTP/3 for better performance
            http_version=cloudfront.HttpVersion.HTTP2_AND_3,
            # Enable IPv6
            enable_ipv6=True,
            comment="CloudFront distribution for private S3 website",
        )

        # ── 4. Stack outputs ─────────────────────────────────────────────────
        CfnOutput(
            self,
            "BucketName",
            value=website_bucket.bucket_name,
            description="Name of the private S3 bucket hosting the web application",
        )

        CfnOutput(
            self,
            "DistributionId",
            value=distribution.distribution_id,
            description="CloudFront distribution ID",
        )

        CfnOutput(
            self,
            "DistributionDomainName",
            value=f"https://{distribution.distribution_domain_name}",
            description="CloudFront distribution URL (use this to access the web application)",
        )
