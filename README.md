# Overview

`note: for the original README.md please look at doc/README.md`

The assignment is to create the connection of subscribing and publishing data from the topics from the mqtt broker.

## Project structure

The project structure has been cleaned a little bit from its original state.

The code regarding the application logic with the mqtt process is located in the root of the `src` folder.

Inside `src` there is a subfolder called `helper`. The idea with helper is to gather all computation functions at the
same place, basically things that could be unrelated to the mqtt tasks, and could be used by other applications.

All tests are gathered under `tests` and they test the logic of the project.

Under the folder `tools` things associated to `docker` is found. The current app has its own Dockerfile
and it has been included in the docker-compose file, to make it unified.

## Data Processing

Data processing is fairly straight forward, when the application subscribes from the `carStatus` topic, the code will
create separate files for each car, can be seen under `data/raw_data` and `data/topic_carstatus`.

This is to increase the speed of particularly read operations, not having to go through all of the file 
searching for a specific car.

### Datasets
More in detail, the datasets are created by suscribing from the mqtt topic `carstatus` and `events`.

It is currently stored as text files for each vehicle, stored locally for optimal performance:

`raw data`
* `<car>`_carCoordinates
    * structure:
        ```json
        {"carIndex":"int","location":{"lat":"float","long":"float"},"timestamp":"int"}
        ```

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

You will need to create the folders for the data, run in project root:

 * `mkdir data`
 * `cd data` --> `mkdir raw_data`, `mkdir topic_carstatus`


* Docker environment
* Python 3.6

Configure:

* PYTHONPATH (Make sure the correct `VENV` is being used)

Example:

```bash
# Python
PYTHONPATH=/usr/bin/python3.6
export PYTHONPATH=$PYTHONPATH:~/MAT-Coding-Challenge
alias python=/usr/bin/python3.6
```

### Unittest

Stand inside the project root and run:

`python3 -m unittest discover tests/ -v`

Quick explanation:

* test_MQTT - unittests the logic regarding the mqtt connection
* test_publish_events_topic - tests the logic of the mqtt client publishing
* test_rw_subscribed_topics - tests the logic in regards to R/W data from the topics
* test_helper - test in regards to the helper functions, calculations and similar

Result of the test is:

```json
test_run_exception (test_MQTT.TestMQTT) ... ok
test_run_path_exception (test_MQTT.TestMQTT) ... ok
test_run_success (test_MQTT.TestMQTT) ... ok
test_create_carstatus_topic_data (test_helper.TestHelper) ... ok
test_create_carstatus_topic_data_failure (test_helper.TestHelper) ... ok
test_event_car_position_msg_success (test_helper.TestHelper) ... ok
test_extract_gps_data_failure (test_helper.TestHelper) ... ok
test_extract_gps_data_success (test_helper.TestHelper) ... ok
test_extract_timestamp_failure (test_helper.TestHelper) ... ok
test_extract_timestamp_success (test_helper.TestHelper) ... ok
test_find_distance_meter_failure (test_helper.TestHelper) ... ok
test_find_distance_meter_success (test_helper.TestHelper) ... ok
test_find_velocity_mph_failure (test_helper.TestHelper) ... ok
test_find_velocity_success (test_helper.TestHelper) ... ok
test_write_file_datatype_failure (test_helper.TestHelper) ... ok
test_write_file_sucess (test_helper.TestHelper) ... ok
test_publish_carstatus_topic_exception (test_publish_events_topic.TestPublish_events_topic) ... ok
test_publish_carstatus_topic_success (test_publish_events_topic.TestPublish_events_topic) ... ok
test_publish_events_topic_exception (test_publish_events_topic.TestPublish_events_topic) ... ok
test_publish_events_topic_success (test_publish_events_topic.TestPublish_events_topic) ... ok
test_load_subscribed_topics_sucess (test_rw_subscribed_topics.TestRWsubscribedTopis) ... ok
test_transform_topic_data_success (test_rw_subscribed_topics.TestRWsubscribedTopis) ... ok
test_write_raw_data_success (test_rw_subscribed_topics.TestRWsubscribedTopis) ... ok
test_write_raw_data_topic_exception (test_rw_subscribed_topics.TestRWsubscribedTopis) ... ok

----------------------------------------------------------------------
Ran 24 tests in 0.144s

```

### Manual Run

Stand inside the project root and run:

`python3 src/main.py`

### Run Project as Docker Container

Run following command:

`docker-compose -f tools/docker/docker-compose.yaml build && docker-compose -f tools/docker/docker-compose.yaml up -d
`

This will spin up all the images including the app, now surf into:

`http://localhost:8084`

This will automatically also run the tests within the docker environment.
### Conclusions

The exercise has been good and fun. Currently the speed in `mph` is displaying in the correct format of the speedometers.
I have not managed to create a good algorithm to determine when a car drives past  another car in a good way, 
however the connectivity is stable and I have been able to prove I can communicate with the
broker, write tests and make it totally encapsulated with `docker-compose`, in that sense production ready.

Each car has its own data, in regards to speed and position. It has been separated to several files within the
project to make it easier to read and gather the data from subscribing from the carstatus topic. In a real life scenario
this might have been a `s3` bucket or even some kind of `no-sql` database.


If I had some more time, I would try to figure out a better way determine when a car drives by another car. Would
probably need to discuss it with somebody to test my current idea and how it could be improved.
