# IFC to Brick

## Requirements

Install Python requirements from `requirements.txt`

Download the appropriate version of `IfcOpenShell` from [this site](http://ifcopenshell.org/python.html) and unzip it into this directoryo

## Running

The `ifc2brick.py` script takes a single argument which is the name of the IFC file. The output is a Turtle-formatted file called `output.ttl`

```
python3 ifc2brick.py example_files/CIEE.ifc
```
