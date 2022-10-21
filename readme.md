# Mediscara MDR

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This package is used to generate MDR documents based on the measurements from a Keyence camera.

## Istallation

After cloning the repository, use the `pip install .` command.
This will install the necessary dependencies.

## Usage

After installation the program can be invoked with the `mdr` command.
The user must specify some required parameters. These are:

> `--yaml`: The path of the yaml specification file
>
> `-p` or `--port`: This specifies the port on which the HTTP server will listen
>
> `-o` or `--output`: This specifies the directory into which the PDF files will be generated

The `--port` and `--output` arguments are optional.

> To get more information about the yaml specification files, please visit [this](https://github.com/ppuska/pdf-generator) GitHub repository.

## Modification
The user can modify this example code to suit their needs.
This can be done by modifying the `parse_payload` method and the `OCB_ATTRIBUTE` variable.
The latter specifies the attribute in the subscription message. The according value will be retrieved.
The former parses the previously mentioned retrieved value. Here is an example payload:
``` json
        {
            "subscriptionId": ...,
            "data": [
                {
                    "id": ...,
                    "type": ...,
                    "<OCB_ATTRIBUTE>": "<this value will be the payload>"
                }
            ]
        }
```

And the `parse_payload` method:
```python
def parse_payload(payload: str) -> dict:
```

This method should return a dictionary. In this dictionary the keys should match the variable template names in the yaml spec file.

```yaml
    - paragraph:
        text: "Incubator - UDI (S/N: <serial_number>)"
        alignment: 'center'
        size: 10
        space_before: 4
        space_after: 20
```

For example, if the `parse_payload` method returns a dictionary of `{ "serial_number": "0123456789" }`, the text rendered to the PDF document will read `Incubator - UDI (S/N: 0123456789)`.
To learn more about this process, please refer to the GitHub repository linked above.
