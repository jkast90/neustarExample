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
        #Needed to replace the keys that had -'s in them because the the __init__ class names were not matching and Python cannot use -'s in variable names
        corrected_dict = { k.replace('-', '_'): v for k, v in json_dict.items() }
        #Needed to add the "best" key if it was missing otherwise the init class was complaining about a missing key
        if "best" not in corrected_dict.keys():
            corrected_dict["best"] = False
        #Converted the types to make it easier to read in the output
        for attr in corrected_dict["attrs"]:
            if attr["type"] == 5:
                corrected_dict["local_pref"] = attr["value"]
            if attr["type"] == 8:
                corrected_dict["communities"] = attr["communities"]
            if attr["type"] == 14:
                corrected_dict["next_hop"] = attr["nexthop"]
        #Dropping the attrs list from the dict because the useful information has already been extracted and added as dictionary items
        corrected_dict.pop("attrs")
        return cls(**corrected_dict)

    def printRouteAttributes(self):
            print(f"Prefix {self.prefix}")
            print(f"\tLocal Pref:  {self.local_pref}")
            print(f"\tNext Hop:    {self.next_hop}")
            print(f"\tRoute Age:   {self.age}")
            print(f"\tBest Route?: {self.best}")
            print(f"\tCommunities: {self.communities}")
            print()
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-filename', help='Please give me the filename of json from the route output', required=True)
    args = parser.parse_args()
    #Used context manager on the file so that it closes automatically after it is done being used
    with open(args.filename) as jsonFile:
        routes = json.loads(jsonFile.read())
        routeObjects = []
        for rt in routes:
            Route = route.from_json(rt)
            routeObjects.append(Route)
        for Route in routeObjects:
            Route.printRouteAttributes()
