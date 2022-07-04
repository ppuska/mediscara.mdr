"""Module for the FIWARE json related code"""
from typing import List
import sys
import logging

from fiware.fiware import FIWARE

from .model import PDFDescriptor

def init(server_url: str):
    """Initializes the module"""
    try:
        init.connector =  FIWARE(server_url)

    except ConnectionError:
        logging.error("Could not connect to the FIWARE OCB")
        sys.exit(1)

def get_next_pdf() -> PDFDescriptor:
    """Fetches the next pdf from the OCB"""

    if not hasattr(init, 'connector'):
        logging.warning("Please initialize the module with the '%s' method", init.__name__)
        return None

    pdfs = get_pdfs()

    pdfs_in_order = sorted(pdfs, key=lambda item: item.id)  # sort the items by their id

    return pdfs_in_order[0]  # return the first element of the sorted list


def get_pdfs() -> List[PDFDescriptor]:
    """Fetches the objects with type 'PDFDescriptor' from the OCB"""

    if not hasattr(init, 'connector'):
        logging.warning("Please initialize the module with the '%s' method", init.__name__)
        return None

    type_ = PDFDescriptor.__name__

    connector = init.connector

    assert isinstance(connector, FIWARE)

    entities = connector.get_entities_with_type(type_)

    pdfs = []

    for entity in entities:
        pdfs.append(PDFDescriptor.from_ngsi(entity))

    return pdfs