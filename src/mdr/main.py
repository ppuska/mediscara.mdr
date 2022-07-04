
from argparse import ArgumentParser
import logging
import os
import sys

from pdfgen.pdf.objects import PDF
from pdfgen.renderer import render

from . import __version__
from . import json
from . import yaml

YAML_PATH = "YAML_PATH"
SERVER_URL = "SERVER_URL"
OUTPUT_FILE = "OUTPUT_FILE"

def load_args(args):
    """Loads the command line arguments """
    parser = ArgumentParser(description="") # TODO add desc
    parser.add_argument('--version', action='version', version=f'MDR version: {__version__}')

    parser.add_argument('--yaml', dest=YAML_PATH, required=True)

    parser.add_argument('--server-url', dest=SERVER_URL, required=True)

    parser.add_argument('-o', '--output', dest=OUTPUT_FILE, required=False)

    return parser.parse_args(args)

def main(args=None):
    """Main entrypoint of the package"""
    # load the spec.yaml file with the variable names
    parsed_args = vars(load_args(args))

    yaml_path = parsed_args[YAML_PATH]
    server_url = parsed_args[SERVER_URL]
    output_file = parsed_args[OUTPUT_FILE]

    json.init(server_url)
    yaml.init(yaml_path)

    logging.info("Checking yaml syntax...")
    yaml.check_yaml_syntax()

    pdf = json.get_next_pdf()

    updated_yaml = yaml.load_variables(variables=pdf.variables)

    if output_file is None:
        output_file = f"{os.getcwd()}/{pdf.id}.pdf"

    pdf_obj = PDF.from_yaml(updated_yaml)

    success = render(output_file, pdf_obj)

    if success:
        logging.info("Object successfully rendered")


if __name__ == "__main__":
    main(sys.argv)
