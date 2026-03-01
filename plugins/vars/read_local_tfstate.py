from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from ansible.errors import AnsibleUndefinedVariable, AnsibleConnectionFailure
from ansible.plugins.vars import BaseVarsPlugin

DOCUMENTATION = """
    name: read_local_tfstate
    version_added: "2.10"
    short_description: Read terraform state
    description: Loads ansible vars from local terraform state
"""

DIR = os.path.dirname(os.path.realpath(__file__))


def _deep_merge(base, override):
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        elif (
            key in result and isinstance(result[key], list) and isinstance(value, list)
        ):
            result[key] = result[key] + value
        else:
            result[key] = value
    return result


class VarsModule(BaseVarsPlugin):
    CACHE = {}

    """
    Loads variables for groups and/or hosts
    """

    def __init__(self, *args):
        super(VarsModule, self).__init__(*args)

        self.tf_states_paths = os.getenv("TF_STATES_PATHS")
        err = []

        if self.tf_states_paths is None:
            err.append("TF_STATES_PATHS")

        if len(err) > 0:
            raise AnsibleUndefinedVariable("Env variables missing: " + (",".join(err)))

    def get_vars(self, loader, path, entities):
        if "result" in self.CACHE:
            return self.CACHE["result"]

        try:
            vars = {}
            for tf_state_path in self.tf_states_paths.split(","):
                if tf_state_path == "":
                    continue

                with open(tf_state_path) as tf_state_file:
                    tfstate = loader.load(tf_state_file.read())
                    if not tfstate.get("outputs"):
                        continue

                    ansible_vars = tfstate["outputs"]["ansible_vars"]["value"]
                    loaded = loader.load(ansible_vars)
                    vars = _deep_merge(vars, loaded)

            self.CACHE["result"] = vars
            return self.CACHE["result"]

        except Exception as err:
            raise AnsibleConnectionFailure(err)
