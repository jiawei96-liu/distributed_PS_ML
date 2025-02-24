import json
from collections import defaultdict
from os import link

class TopoGenerator(object):
    def __init__(self, topo=defaultdict(list)):
        self.topo = topo
    
    def __str__(self) -> str:
        return str(self.topo)

    def add_edge(self, src, dst, weight):
        self.topo[src].append({dst: weight})
        self.topo[dst].append({src: weight})

    def add_edges(self, edge_list):
        for e in edge_list:
            self.add_edge(e[0], e[1], e[2])

    def remove_edge(self, src, dst):
        if self.topo[src]:
            for node in self.topo[dst]:
                if node.keys()[0] is dst:
                    self.topo[src].remove(node)
                    break
    
    def construct_path_set(self,host_set,switch_set,max_len=3):
        path=defaultdict(dict)
        for h in host_set:
            for s in switch_set:
                path[h][s]=[
                    Path(p) for p in self._get_feasible_path(h,s,max_len)]
        return path
    
    def _get_feasible_path(self, src, dst, max_len, path=[]):
        path=path+[src]

        if src == dst:
            return [path]

        if len(path) > max_len:
            return

        paths=[]

        for node in self.topo[src].keys():
            if node not in path:
                results=self._get_feasible_path(node,dst,max_len,path)
                if results is not None:
                    for p in results:
                        paths.append(p)

        return paths
    
    def generate_json(self,json_file):
        json_str = json.dumps(self.topo, indent=4)
        with open(json_file, 'w') as f:
            f.write(json_str)


class Path(object):
    def __init__(self, node_list):
        self.node_list=node_list
    
    def __repr__(self):
        p_str=self.node_list[0]
        for node in self.node_list[1:]:
            p_str=p_str+'->'+ node
        return p_str
        
    def get_link(self,topo):
        link_set=defaultdict(dict)
        for i in range(len(self.node_list)-1):
            node1=self.node_list[i]
            node2=self.node_list[i+1]
            link_set[node1][node2]=topo[node1][node2]
        return link_set
    
    def get_path(self):
        return self.node_list


if __name__ == '__main__':
    topo=TopoGenerator(json.load(open('/home/sdn/fj/distributed_PS_ML/routing/data/topo/fattree80.json')))
    host_set=['h1','h2','h3']
    switch_set=['v1','v2','v3']
    path=topo.construct_path_set(host_set,switch_set,6)
    print(path[host_set[1]][switch_set[1]][0])
    print(path[host_set[1]][switch_set[1]][0].get_link(topo.topo))
    
