from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from ansible.errors import (
    AnsibleUndefinedVariable,
    AnsibleParserError,
    AnsibleConnectionFailure,
)
from ansible.plugins.vars import BaseVarsPlugin

try:
    import boto3

    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

DOCUMENTATION = """
    name: read_local_tfstate
    version_added: "2.10"
    short_description: Read terraform state
    description: Loads ansible vars from terraform state stored on S3
"""

DIR = os.path.dirname(os.path.realpath(__file__))


class VarsModule(BaseVarsPlugin):
    CACHE = {}

    """
    Loads variables for groups and/or hosts
    """

    def __init__(self, *args):
        super(VarsModule, self).__init__(*args)
        err = []

        self.bucket_name = os.getenv("TF_BACKEND_BUCKET_NAME")
        if self.bucket_name is None:
            err.append("TF_BACKEND_BUCKET_NAME")

        self.CACHE["target"] = os.getenv("TF_TARGET")

        if self.CACHE["target"] is None:
            err.append("TF_TARGET")

        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        if self.aws_access_key_id is None:
            err.append("AWS_ACCESS_KEY_ID")

        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        if self.aws_secret_access_key is None:
            err.append("AWS_SECRET_ACCESS_KEY")

        self.aws_region = os.getenv("AWS_REGION")
        if self.aws_region is None:
            err.append("AWS_REGION")

        if len(err) > 0:
            raise AnsibleUndefinedVariable("Env variables missing: "
                                           + (",".join(err)))

    def get_vars(self, loader, path, entities):
        if not HAS_BOTO3:
            raise AnsibleParserError("Vars plugin requires boto3")

        if "result" in self.CACHE:
            return self.CACHE["result"]

        try:
            s3 = boto3.resource(
                "s3",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region,
            )
            vars = {}

            for target in self.CACHE["target"].split(","):
                if target == "":
                    continue

                content_object = s3.Object(self.bucket_name, target)

                tfstate_content = content_object.get()["Body"]\
                    .read().decode("utf-8")

                tfstate = loader.load(tfstate_content)

                if not tfstate.get("outputs"):
                    continue

                ansible_vars = tfstate["outputs"]["ansible_vars"]["value"]
                vars = vars | loader.load(ansible_vars)

            self.CACHE["result"] = vars
            return self.CACHE["result"]

        except Exception as err:
            raise AnsibleConnectionFailure(err)
