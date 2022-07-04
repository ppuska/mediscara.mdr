"""Module for the yaml operation related code"""

import logging
import re

from yaml import safe_load

def init(yaml_path: str):
    """Loads the yaml file"""
    with open(yaml_path, 'r', encoding='utf-8') as file:
        init.yaml_raw = file.read()


def load_variables(variables: dict) -> dict:
    """Loads the variable dictionary back into the raw file"""

    if not hasattr(init, 'yaml_raw'):
        logging.warning(
            "%s: yaml file not loaded, please use the %s method first", load_variables.__name__, init.__name__
            )
        return None

    string = init.yaml_raw

    for name, value in variables.items():
        name_str = f'<{name}>'

        previous_string = string

        string = re.sub(name_str, value, string)

        if string == previous_string:
            logging.warning("Variable '%s' not found in yaml file", name)

    matches = has_variables(string)

    if matches:
        # the list is not None, not all variables were filled
        for match in matches:
            logging.warning("Variable '%s' was not overridden", match)

    return safe_load(string)  # convert the string back to dict

def has_variables(string: str = ""):
    """Checks if the yaml file has variables with the <variable> syntax"""

    if not string:
        if not hasattr(init, 'yaml_raw'):
            logging.warning(
                "%s: yaml file not loaded, please use the %s method first", load_variables.__name__, init.__name__
                )
            return False

        string = init.yaml_raw

    re_pattern = r'<\w+>'

    return re.findall(re_pattern, string)

def check_yaml_syntax():
    """Checks if the syntax of the variables (if any) are correct in the yaml file"""

    if not hasattr(init, 'yaml_raw'):
        logging.warning(
            "%s: yaml file not loaded, please use the %s method first", load_variables.__name__, init.__name__
            )
        return

    re_pattern = r'<\w+^>'

    errors = re.findall(pattern=re_pattern, string=init.yaml_raw)

    if errors:
        for error in errors:
            logging.warning("Syntax error in variable: %s", str(error))

    else:
        logging.info("Yaml variable syntax is correct")
