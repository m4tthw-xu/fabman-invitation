"""
Accessing AWS Secretes Manager for pulling API keys for Canvas and Fabman.
"""

# standard library imports
import base64
import json
import os

# 3rd party imports
import boto3
from botocore.exceptions import ClientError


class Secrets:
    def __init__(self) -> None:
        """
        Initialize Secrets class to pull secrets from AWS Secrets Manager.
        """
        secret_name = "prod/portal/canvasApiKey"
        region_name = "us-east-1"

        try:
            # Create the client directly without session
            client = boto3.client(
                service_name="secretsmanager",
                region_name=region_name,
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            )

            secrets_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "DecryptionFailureException":
                # Secrets Manager can't decrypt the protected secret text using the
                # provided
                # KMS key. Deal with the exception here, and/or rethrow at your
                # discretion.
                raise e
            if e.response["Error"]["Code"] == "InternalServiceErrorException":
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            if e.response["Error"]["Code"] == "InvalidParameterException":
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            if e.response["Error"]["Code"] == "InvalidRequestException":
                # You provided a parameter value that is not valid for the current state
                # of the resource. Deal with the exception here, and/or rethrow at your
                # discretion.
                raise e
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e

        # string Secrets
        if "SecretString" in secrets_response:
            secrets = json.loads(secrets_response["SecretString"])
            self.__canvas_api_key = secrets["CANVAS_TEACHER_KEY"]
            self.__fabman_api_key = secrets["FABMAN_KEY"]
            self.__dev_api_key = secrets["DEV_TEACHER_KEY"]

        # binary Secrets
        if "SecretBinary" in secrets_response:
            print("We have binary secrets")
            secrets = base64.b64decode(secrets_response["SecretBinary"])
            # we don't have any binary secrets
            pass

    @property
    def canvas_api_key(self) -> str:
        """
        Canvas API key.

        :return: Canvas API key
        :rtype: str
        """
        return self.__canvas_api_key

    @property
    def fabman_api_key(self) -> str:
        """
        Fabman API key.

        :return: Fabman API key
        :rtype: str
        """
        return self.__fabman_api_key

    @property
    def dev_api_key(self) -> str:
        """
        Dev/Idea to production API key

        :return: Dev/Idea to production API key
        :return type: str
        """
        return self.__dev_api_key
