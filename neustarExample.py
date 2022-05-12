#!/c/Users/Jeremy/AppData/Local/Programs/Python/Python38-32/python
"""This script takes a json file and reads in the routes then takes the following attributes from the json the puts them into a class:

    nlri - DICT which contains the "prefix" attribute (STRING) 
    age - INT
    stale - BOOLEAN
    source_id - STRING
    neighbor_ip - STRING
    best - BOOLEAN
    local_pref - DICT which has the type 5 (INT) attribute then reads the "value" of that (STRING)
    communities - DICT which has the type 8 (INT) attribute then reads the "communities" of that (list of INT)
    next_hop  - DICT which has the type 14 (INT) attribute then reads the "nexthop" of that (STRING)
    """

import argparse, json

class route():
    '''This class is used to hold route information'''
    def __init__(self, nlri, age, stale, source_id, neighbor_ip, best, local_pref, communities, next_hop):
        self.prefix = nlri["prefix"]
        self.age = age
        self.best = best
        self.stale = stale
        self.source_ip = source_id
        self.neighbor_ip = neighbor_ip
        self.local_pref = local_pref
        self.communities = communities
        self.next_hop = next_hop

    @classmethod
    def from_json(cls, json_dict):
        corrected_dict = { k.replace('-', '_'): v for k, v in json_dict.items() }
        if "best" not in corrected_dict.keys():
            corrected_dict["best"] = False
        for attr in corrected_dict["attrs"]:
            if attr["type"] == 5:
                corrected_dict["local_pref"] = attr["value"]
            if attr["type"] == 8:
                corrected_dict["communities"] = attr["communities"]
            if attr["type"] == 14:
                corrected_dict["next_hop"] = attr["nexthop"]
        corrected_dict.pop("attrs")
        return cls(**corrected_dict)
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-filename', help='Please give me the filename of json from the route output', required=True)
    args = parser.parse_args()
    with open(args.filename) as jsonFile:
        routes = json.loads(jsonFile.read())
        for rt in routes:
            Route = route.from_json(rt)
            print(f"Prefix {Route.prefix}")
            print(f"\tLocal Pref:  {Route.local_pref}")
            print(f"\tNext Hop:    {Route.next_hop}")
            print(f"\tRoute Age:   {Route.age}")
            print(f"\tBest Route?: {Route.best}")
            print(f"\tCommunities: {Route.communities}")
            print()