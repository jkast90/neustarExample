# neustarExample
This script takes a json file and reads in the routes then takes the following attributes from the json the puts them into a class:

    nlri - DICT which contains the "prefix" attribute (STRING) 
    age - INT
    stale - BOOLEAN
    source_id - STRING
    neighbor_ip - STRING
    best - BOOLEAN
    local_pref - DICT which has the type 5 (INT) attribute then reads the "value" of that (STRING)
    communities - DICT which has the type 8 (INT) attribute then reads the "communities" of that (list of INT)
    next_hop  - DICT which has the type 14 (INT) attribute then reads the "nexthop" of that (STRING)


This information can also be accessed by running "python3 neustarExample.py -h"