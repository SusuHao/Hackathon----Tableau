import sys
import pickle

end1 = sys.argv[1]
end2 = sys.argv[2]
sub = sys.argv[3]
#current_time = int(sys.argv[3])
#cost_per_stop = float(sys.argv[4])
#cost_per_transfer = float(sys.argv[5])


def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def dijkstras(graph, start, end):
    import heapq
    seen = set()
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    heapq.heappush(queue, (0, 0, 0, [(start, None)]))
    while queue:
        # get the first path from the queue
        (curr_cost, curr_distance, curr_transfers, path) = heapq.heappop(queue)

        # get the last node from the path
        (node, curr_service) = path[-1]

        # path found
        if node == end:
            return (curr_cost, curr_distance, curr_transfers, path)

        if (node, curr_service) in seen:
            continue

        seen.add((node, curr_service))
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for (adjacent, service), distance in graph.get(node, {}).items():
            new_path = list(path)
            new_path.append((adjacent, service))
            new_distance = curr_distance + distance
            new_cost = distance + curr_cost
            new_transfers = curr_transfers
            if curr_service != service:
                new_cost += cost_per_transfer
                new_transfers += 1
            new_cost += cost_per_stop

            heapq.heappush(queue, (new_cost, new_distance, new_transfers, new_path))

current_time = int(900)
cost_per_stop = float(0.1)
cost_per_transfer = float(5.0)

graph = load_obj("graph")
stop_desc_map = load_obj("stop_desc_map")
stop_code_map = load_obj("stop_code_map")
#stops_subzone = load_obj("stops_subzone")
subzone_stops = load_obj("subzone_stops")

data = {}
i = 0
for start_stop in subzone_stops[sub]:
    (cost1, distance1, transfers1, path1) = dijkstras(graph, stop_desc_map[start_stop], stop_desc_map[end1])
    (cost2, distance2, transfers2, path2) = dijkstras(graph, stop_desc_map[start_stop], stop_desc_map[end2])
    data[i] = ((start_stop),(cost1 + cost2),(distance1),(distance2),(transfers1 - 1),(transfers2 - 1),(path1),(path2))
    i = i + 1

element = min(data.items(), key=lambda x: x[1][1])[0] #get min total cost

name = data[element][0]
overall_cost = data[element][1]
distance1 = data[element][2]
distance2 = data[element][3]
transfers1 = data[element][4]
transfers2 = data[element][5]
stops1 = len(data[element][6]) - 1
stops2 = len(data[element][7]) - 1
time1 = int((distance1 / 23.0) * 60 + stops1 * 1/4 + transfers1 * 8)
time2 = int((distance2 / 23.0) * 60 + stops2 * 1/4 + transfers2 * 8)

services1 = set()
for x in data[element][6]:
    if x[1] is not None:
        services1.add(x[1][0])
services1_ = list(services1)
services1 = ', '.join(str(e) for e in services1_)

services2 = set()
for x in data[element][7]:
    if x[1] is not None:
        services2.add(x[1][0])
services2_ = list(services2)
services2 = ', '.join(str(e) for e in services2_)

print name, "+", time1, "-", time2, "*", services1, "%", services2, "_", 
