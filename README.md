# IFC to Brick

This is a work in progress! Suggestions, improvements are very welcome.

This currently converts the following IFC structures:
- `IfcBuildingStorey` to `brick:Floor`
- `IfcZone` to `brick:HVAC_Zone`
- `IfcSpacee` to `brick:Room`
- use `IfcRelAggregates` to associate rooms with HVAC zones and floors

## Requirements

Install Python requirements from `requirements.txt`

Download the appropriate version of `IfcOpenShell` from [this site](http://ifcopenshell.org/python.html) and unzip it into this directoryo

## Running

The `ifc2brick.py` script takes a single argument which is the name of the IFC file. The output is a Turtle-formatted file called `output.ttl`

```
python3 ifc2brick.py example_files/CIEE.ifc
```
