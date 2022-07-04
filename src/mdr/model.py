
from dataclasses import dataclass, field
from typing import ClassVar, Dict

@dataclass
class PDFDescriptor:
    """Dataclass to describe the NGSI v2 entity that holds the pdf variables"""

    type: ClassVar[str] = "PDFDescriptor"

    id: str = field()  # pylint: disable=invalid-name

    variables: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_ngsi(cls, ngsi: dict):
        """Creates a PDFDescriptor from an NGSI v2 formatted dictionary"""

        id_ = None
        variables_ = {}

        # check for invalid type
        if ngsi.get('type') != cls.type:
            raise TypeError(f"Type does not match ({ngsi.get('type')} != {cls.type})")

        for key, value in ngsi.items():
            if key == 'id':
                id_ = value

            elif isinstance(value, dict):
                value_inner = value.get('value')
                variables_[key] = value_inner

        if id_ is None:
            raise ValueError("Id cannot be None")

        return cls(id_, variables_)
