from argparse import ArgumentParser
from datetime import datetime
import logging
import os
import sys

from flask import Flask, make_response, request

from pdfgen.pdf.objects import PDF
from pdfgen.renderer import render

from . import __version__
from . import yaml

YAML_PATH_KEY = "YAML_PATH"
PORT_KEY = "PORT"
OUTPUT_DIR_KEY = "OUTPUT_DIR"

PORT_DEFAULT_VALUE = 8888

OUTPUT_DIR = ""

OCB_ATTRIBUTE = "measure_assembly_info"

# create Flask app instance
app = Flask(__name__)


def load_args(args):
    """Loads the command line arguments"""
    parser = ArgumentParser(description="")  # TODO add desc
    parser.add_argument(
        "--version", action="version", version=f"MDR version: {__version__}"
    )

    parser.add_argument("-o", "--output", dest=OUTPUT_DIR_KEY)

    parser.add_argument("--yaml", dest=YAML_PATH_KEY, required=True)

    parser.add_argument("-p", "--port", dest=PORT_KEY)

    return parser.parse_args(args)


def main(args=None):
    """Main entrypoint of the package"""
    # load the spec.yaml file with the variable names
    parsed_args = vars(load_args(args[1:]))

    global OUTPUT_DIR  # pylint: disable=global-statement

    yaml_path = parsed_args[YAML_PATH_KEY]
    OUTPUT_DIR = parsed_args.get(OUTPUT_DIR_KEY)
    port = parsed_args.get(PORT_KEY)

    if OUTPUT_DIR is None:
        logging.info("Output directory not specified, using current working directory")
        OUTPUT_DIR = os.getcwd()

    if port is None:
        logging.info(
            "Port is not specified, using default value of: %s", PORT_DEFAULT_VALUE
        )
        port = PORT_DEFAULT_VALUE

    yaml.init(yaml_path)

    logging.info("Checking yaml syntax...")
    yaml.check_yaml_syntax()

    # start the web application
    logging.info("Starting server...")
    app.run(host="localhost", port=port)


@app.route("/measurement", methods=["POST"])
def measurement():
    """This method gets called when a subscription fires in the OCB

    This happens when a new measurement is done

    The incoming subscription syntax is:
        {
            "subscriptionId": ...,
            "data": [
                {
                    "id": ...,
                    "type": ...,
                    "measure_assembly_info": <this is what we need>
                }
            ]
        }
    """

    try:
        if request.is_json:
            payload = request.json  # type: dict
            payload = payload["data"]  # type: list
            payload = payload[0]  # type: dict
            payload = payload[OCB_ATTRIBUTE]  # type: str

    except (IndexError, KeyError) as error:
        logging.warning("Got an error while parsing the request body: %s", error.args)

    else:
        updated_yaml = yaml.load_variables(parse_payload(payload))

        render(
            os.path.join(
                OUTPUT_DIR,
                f"{datetime.now().strftime('%Y_%m_%d__%H_%M_%S')}.pdf",
            ),
            PDF.from_yaml(updated_yaml),
        )

    return make_response("OK", 200)


def parse_payload(payload: str) -> dict:
    """This message parses the ultralight-like formatted payload"""
    tokens = payload.split("|")

    if len(tokens) % 2 != 0:
        # there should not be an odd number of elements
        logging.warning(
            "The number of keys do not match with the number of values, disregarding last"
        )
        tokens = tokens[:-1]

    variables = {}

    for index, token in enumerate(tokens):
        if "m" in token:
            value = float(tokens[index + 1])

            # todo implement correct value check
            if value < 0.5:
                result = "OK"
                color = "#adf288"  # green

            else:
                result = "Not OK"
                color = "#f28f88"  # red

            variables[f"{token}_res"] = result
            variables[f"{token}_color"] = color

            variables[token] = tokens[index + 1]

        else:
            continue

    # add the additional items
    variables["meas_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    variables["serial_number"] = "123_456"
    variables["type"] = "Incubator housing type 1"

    return variables


if __name__ == "__main__":
    main(sys.argv)
