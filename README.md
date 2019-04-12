# Overview

`note: for the original README.md please look at doc/README.md`

## Data Processing


## Datasets
The datasets are created by suscribing from the mqtt topic `carstatus` and `events`.

Created datasets as text files for each vehicle, stored locally for optimal performance:

`raw data`
* `<car>`_carCoordinates

`topic car status`
* `<car>`_carStatus_speed
    * structure:
        ```json
        {"timestamp": "float", "carIndex": "int", "type": "str", "value": "float"}
        ```
* `<car>`_carStatus_position
    * structure:
        ```json
        {"timestamp": "float", "carIndex": "int", "type": "str", "value": "int"}
        ```

## Setup

Configure:

* PYTHONPATH (Make sure the correct `VENV` is being used)

#### Requirements

* Docker environment
* Python 3.6

Assuming that Python, Docker and Java is already setup.

### Tests


### Manual Run


### Run Project as Docker Container


### Results


