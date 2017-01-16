import requests
import json
import pickle

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


headers = {
       'AccountKey': '2cBiLcQLT1SBQOFQvyr43A==',
       'UniqueUserID': 'caaa7cbb-0abb-4ea8-b26e-df9a1950e9ff',
       'accept': 'application/json'
    }

def fetch_all(url):
    results = []
    while True:
        new_results = requests.get(
            url,
            headers=headers,
            params={'$skip': len(results)}
        ).json()['value']
        if new_results == []:
            break
        else:
            results += new_results
    return results

if __name__ == "__main__":
    stops = fetch_all("http://datamall2.mytransport.sg/ltaodataservice/BusStops")
    services = fetch_all("http://datamall2.mytransport.sg/ltaodataservice/BusServices")
    routes = fetch_all("http://datamall2.mytransport.sg/ltaodataservice/BusRoutes")

    #with open("stops.json", "w") as f:
    #    f.write(json.dumps(stops))
    
    #with open("services.json", "w") as f:
    #    f.write(json.dumps(services))
   
    #with open("routes.json", "w") as f:
    #    f.write(json.dumps(routes))

###################################################

#import json
#import pprint

#stops = json.loads(open("stops.json").read())
#services = json.loads(open("services.json").read())
#routes = json.loads(open("routes.json").read())

routes_map = {}

for route in routes:
    try:
        first_bus = int(route["WD_FirstBus"])
        last_bus = int(route["WD_LastBus"])
    except:
        continue
    if first_bus <= last_bus:
        if not (first_bus <= current_time <= last_bus):
            continue
    if first_bus > last_bus:
        if (last_bus <= current_time <= first_bus):
            continue

    key = (route["ServiceNo"], route["Direction"])
    if key not in routes_map:
        routes_map[key] = []
    # hack around broken data
    if (route["StopSequence"] == 4
            and route["Distance"] == 9.1
            and key == ("34", 1)):
        route["StopSequence"] = 14
    routes_map[key] += [route]


print "Initializing Graph"
graph = {}
for service, path in routes_map.items():
    # hack around broken data
    path.sort(key = lambda r: r["StopSequence"])
    for route_index in range(len(path) - 1):
        key = path[route_index]["BusStopCode"]
        if key not in graph:
            graph[key] = {}
        curr_route_stop = path[route_index]
        next_route_stop = path[route_index + 1]
        curr_distance = curr_route_stop["Distance"] or 0
        next_distance = next_route_stop["Distance"] or curr_distance
        distance = next_distance - curr_distance
        assert distance >= 0, (curr_route_stop, next_route_stop)
        curr_code = curr_route_stop["BusStopCode"]
        next_code = next_route_stop["BusStopCode"]
        graph[curr_code][(next_code, service)] = distance


save_obj(graph, "graph")

stop_desc_map = {stop["Description"]: stop["BusStopCode"] for stop in stops}
save_obj(stop_desc_map, "stop_desc_map")

stop_code_map = {stop["BusStopCode"]: stop["Description"] for stop in stops}
save_obj(stop_code_map, "stop_code_map")


import csv
from collections import defaultdict
reader = csv.DictReader(open("bus-subzone.csv"))
subzone_stops = defaultdict(list)
for row in reader:
    key = row.pop('SUBZONE_N')
    subzone_stops[key].append(row.pop('Description'))
save_obj(subzone_stops, "subzone_stops")


reader = csv.DictReader(open("bus-subzone.csv"))
stops_subzone = {}
for row in reader:
    key = row.pop('Description')
    if key in stops_subzone:
        pass
    stops_subzone[key] = row.pop('SUBZONE_N')
save_obj(stops_subzone, "stops_subzone")



