import unittest
import random
import networkx as nx
from sybil import votetrust
from math import floor
from collections import defaultdict
from util import graph_creation

class VoteTrustTests(unittest.TestCase):
    def create_honest_region(self):
        # Create graph
        g = nx.watts_strogatz_graph(2000, 30, 0.02)

        """
        with open('G://Downloads/BlogCatalog-dataset/BlogCatalog-dataset/data/edges.csv','rb') as f:
            g= nx.read_edgelist(f, delimiter=",")
        print(nx.is_connected(g))
        """

        g = nx.DiGraph(g)
        nx.set_node_attributes(g, 'type', 'honest')
        sorted_edges = sorted(g.edges(), key= lambda tup: tup[0])
        for e in sorted_edges:
            if e[0] < e[1]:
                r = random.random()
                if r < 0.5:
                    g.remove_edge(e[0], e[1])
                    g[e[1]][e[0]]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())
                else:
                    g.remove_edge(e[1], e[0])
                    g[e[0]][e[1]]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())
        to_remove = []
        for i in nx.strongly_connected_components(g):
            if len(i) == 1:
                to_remove.append(i.pop())
        for i in to_remove:
            g.remove_node(i)
        mapping = dict(zip(g.nodes(), range(len(g.nodes()))))
        nx.relabel_nodes(g, mapping, copy=False)
        """
        for e in g.edges():
            if count%1000 == 0:
                print(count)
            if (e[1], e[0]) not in removed and e not in removed:
                r = random.random()
                if r < 0.5:
                    g.remove_edge(e[0], e[1])
                    removed.append((e[0], e[1]))
                    g[e[1]][e[0]]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())
                else:
                    g.remove_edge(e[1], e[0])
                    removed.append((e[1], e[0]))
                    g[e[0]][e[1]]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())
            elif e not in removed:
                g[e[0]][e[1]]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())
            count+=1
            """

        return g

    def add_sybil_region(self, g, SIZE_SYBIL, NUMBER_IN):
        ### Add sybil region ###

        NUM_NODES = len(g.nodes())

        for i in range(SIZE_SYBIL):
            g.add_node(NUM_NODES + i)
        for i in range(SIZE_SYBIL):
            for j in range(SIZE_SYBIL):
                if j != i:
                    g.add_edge(i + NUM_NODES, j + NUM_NODES, trust=1)

        selected = []
        for i in range(NUMBER_IN):
            while True:
                r = floor(random.random() * NUM_NODES)
                if r not in selected:
                    selected.append(r)
                    sybil = floor(random.random() * SIZE_SYBIL + NUM_NODES)
                    g.add_edge(r, sybil, trust=1)
                    break

    def test_collusion_iterative(self):
        NUM_NODES = 2000
        SIZE_SYBIL = 100
        NUM_IN = 10

        g = self.create_honest_region(self, NUM_NODES)
        self.add_sybil_region(g, SIZE_SYBIL, NUM_IN)


        votetrust.vote_assignment(g, (0, 500, 1500))
        undetected_edges = [0] * SIZE_SYBIL
        while True:
            for i in range(SIZE_SYBIL):
                while True:
                    r = floor(random.random() * NUM_NODES)
                    if (NUM_NODES+i, r) not in g.edges():
                        break
                g.add_edge(NUM_NODES+i, r, trust=-1)
            votetrust.vote_propagation(g)
            votetrust.vote_aggregation(g)
            found = False
            for i in range(SIZE_SYBIL):
                if g.node[i+NUM_NODES]['p'] > 0.5:
                    undetected_edges[i]+=1
                    found = True
            print(undetected_edges)
            if not found:
                break
        ####### Run VoteTrust ###########
        #print('vote assign done')
        #votetrust.vote_propagation(g)
        #print('vote prop done')
        #votetrust.vote_aggregation(g)
        #print('vote agg done')
        #print('sibil sensitivity')

     #   print(sum([g.node[x]['vote_capacity'] for x in range(1000, 1020)])/20)
      #  print(sum([g.node[x]['vote_capacity'] for x in range(NUM_NODES, NUM_NODES+SIZE_SYBIL)])/SIZE_SYBIL)

        """

        """

        for i in range(SIZE_SYBIL):
            print(g.node[i+NUM_NODES])

    def test_collusion_once(self):
        SIZE_SYBIL = 100
        NUM_IN = 10

        g = self.create_honest_region()
        NUM_NODES = len(g.nodes())
        self.add_sybil_region(g, SIZE_SYBIL, NUM_IN)
        print('done creating')

        for i in range(SIZE_SYBIL):
            edges = []
            for j in range(8):
                while True:
                    r = floor(random.random() * NUM_NODES)
                    if (NUM_NODES+i, r) not in edges:
                        break
                edges.append((NUM_NODES+i,r))
                g.add_edge(NUM_NODES+i, r, trust=-1)

        votetrust.vote_assignment(g, (0,1000,1500))
        print('start propagation')

        votetrust.vote_propagation_mat(g)
        print('done aggregation')

        votetrust.vote_aggregation(g)

        print(sum([g.node[x]['p'] for x in range(NUM_NODES)]))
        print(sum(1 for x in range(NUM_NODES, NUM_NODES+SIZE_SYBIL) if g.node[x]['p']<0.5)/SIZE_SYBIL)
        print(sum(1 for x in range(NUM_NODES) if g.node[x]['p']<0.5)/NUM_NODES)

    def test_peripheral(self):

        g = self.create_honest_region()
        NUM_NODES = len(g.nodes())
        #Add 10 periphereral sybil and honest nodes
        NUM_PERIPHERAL = 40
        for i in range(NUM_PERIPHERAL):
            g.add_node(NUM_NODES+i)
            g.add_node(NUM_NODES+i+NUM_PERIPHERAL)
            g.node[NUM_NODES+i]['type'] = 'sybil'
            g.node[NUM_NODES+i+NUM_PERIPHERAL]['type'] = 'honest'
            for j in range(10):
                r = floor(random.random()*NUM_NODES)
                g.add_edge(NUM_NODES+i, r)
                #give random attacks a high probability to fail
                g[NUM_NODES+i][r]['trust'] = (lambda x: -1 if x < 0.7 else 1)(random.random())

                g.add_edge(NUM_NODES+i+NUM_PERIPHERAL, r)
                g[NUM_NODES+i+NUM_PERIPHERAL][r]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())

        ### Run VoteTrust ###
        votetrust.vote_assignment(g, (0, 500, 1500))
        print('start prop')
        votetrust.vote_propagation_mat(g)
        print('done prop')

        votetrust.vote_aggregation(g)

        #### Assert Peripheral sybils recognized correctly ###
        count = {'mainRegion':0, 'sybil':0, 'sybilPeripheral':0}
        for i in range(NUM_NODES + 2*NUM_PERIPHERAL):
            if g.node[i]['p'] < 0.5:
                if i < NUM_NODES:
                    count['mainRegion'] += 1
                elif i >= NUM_NODES and i < NUM_NODES+NUM_PERIPHERAL:
                    count['sybil'] += 1
                else:
                    count['sybilPeripheral'] += 1
        count['mainRegion'] /= NUM_NODES
        count['sybil'] /= NUM_PERIPHERAL
        count['sybilPeripheral'] /= NUM_PERIPHERAL
        print(count)
        print(sum([g.node[x]['vote_capacity'] for x in range(NUM_NODES, NUM_NODES+NUM_PERIPHERAL)]))

    def test_attack(self):
        g = self.create_honest_region()
        #g = nx.DiGraph()

        """
        for i in range(5):
            for j in range(1,10):
                g.add_edge(i*10,i*10+j, {'trust':1})
        """
        NUM_NODES = len(g.nodes())
        requested = []
        depth = 2


        ATTACKER = len(g.nodes())

        for i in range(depth):
            if i == 0:
                for j in range(20):
                    r = floor(random.random()*NUM_NODES)
                    trust =  votetrust.getTrustByProb(0)
                    g.add_edge(ATTACKER, r, {'trust': trust})
                    requested.append(r)

            else:
                friends_attacker = votetrust.getFriends(g, ATTACKER)
                for n in friends_attacker :
                    friends_n = votetrust.getFriends(g, n)
                    if ATTACKER in friends_n:
                        friends_n.remove(ATTACKER)
                    for m in friends_n:
                        if m not in requested:
                            friends_m = votetrust.getFriends(g, m)
                            friends_attacker = votetrust.getFriends(g, ATTACKER)
                            common_friends = list(set(friends_attacker).intersection(friends_m))
                            trust = votetrust.getTrustByProb(len(common_friends))
                            g.add_edge(ATTACKER, m, {'trust' : trust})
                            requested.append((ATTACKER, m, trust))



        votetrust.vote_assignment(g,[0])
        votetrust.vote_propagation_mat(g)
        votetrust.vote_aggregation(g)
        print(sum(1 for x in g.out_edges(ATTACKER) if g[ATTACKER][x[1]]['trust']==1)/len(g[ATTACKER]))
        print(g[ATTACKER])

    def test_assignment(self):
        g = nx.DiGraph()
        g.add_edges_from([(0, 1), (1, 2), (2, 3), (1,3)])
        votetrust.vote_assignment(g, (0, 3))
        self.assertEqual(g.node[0]['initial_trust'], 2, 'Node zero has trust 2')
        self.assertEqual(g.node[3]['initial_trust'], 2, 'Node zero has trust 2')
        self.assertEqual(sum([g.node[i]['initial_trust'] for i in (1,2)]), 0)

    def test_propagation(self):
        NUM_NODES = 2000
        g = graph_creation.create_directed_smallWorld(NUM_NODES,40)
        p = nx.shortest_path_length(g)
        votetrust.vote_assignment(g, [0])
        votetrust.vote_propagation(g)

        trust = defaultdict(lambda : [0,0])
        dist = 1
        while True:
            found = False
            for i in range(NUM_NODES):
                if nx.shortest_path_length(g, source=0, target=i) == dist:
                    trust[dist][0] += g.node[i]['vote_capacity']
                    trust[dist][1] += 1
                    found = True
            if not found:
                break
            else:
                dist += 1

        trust2 = [trust[x+1][0]/trust[x+1][1] for x in range(len(trust))]
        print(trust)
        print(trust2)

    def test_propagation_base(self):
        g = nx.DiGraph()
        g.add_edges_from([(0,2),(1,2),(2,3),(3,4),(4,2),(3,5)])
        nx.set_edge_attributes(g, 'trust', 1)
        g[1][2]['trust'] = -1
        nx.set_node_attributes(g,'initial_trust',0)
        g.node[0]['initial_trust'] = 2
        g.node[1]['initial_trust'] = 2

        votetrust.vote_propagation_mat(g)
        print(g.node)

        self.assertAlmostEqual(g.node[0]['vote_capacity'], 0.4, places = 3)
        self.assertAlmostEqual(g.node[1]['vote_capacity'], 0.4, places = 3)
        self.assertAlmostEqual(g.node[2]['vote_capacity'], 0.856, places = 2)
        self.assertAlmostEqual(g.node[3]['vote_capacity'], 0.685, places = 2)
        self.assertAlmostEqual(g.node[4]['vote_capacity'], 0.274, places = 2)

        self.assertEqual(g.node[4]['vote_capacity'], g.node[5]['vote_capacity'])

        votetrust.vote_aggregation(g)
        print(g.node)

    def test_aggregation(self):
        g = nx.DiGraph()
        g.add_edges_from([(0, 1), (0, 2), (0, 3), (0,4)])
        g.node[1]['vote_capacity'] = 1
        g.node[2]['vote_capacity'] = 0.5
        g.node[3]['vote_capacity'] = 0
        g.node[4]['vote_capacity'] = 1

        g[0][1]['trust'] = 1
        g[0][2]['trust'] = 1
        g[0][3]['trust'] = 1
        g[0][4]['trust'] = 0

        votetrust.vote_aggregation(g)
        print(g.node)

    def test_toy_propagation(self):
        g = nx.DiGraph()
        edges = []
        for i in range(3):
            for j in range(3):
                if i!=j:
                    edges.append((i,j))

        g.add_edges_from([(3,4),(4,5),(5,3)])

        edges.append((2,3))

        g.add_edges_from(edges)

        for i in range(len(g.nodes()), 50):
            print(i)
            g.add_node(i)
        votetrust.vote_combined(g, [0])
        #votetrust.vote_propagation(g)
        print(sum([g.node[x]['vote_capacity'] for x in range(len(g.nodes()))]))
        print(sum([g.node[x]['vote_capacity'] for x in range(3,6)]))
        print(g.node[2]['vote_capacity'])
        print(g.out_degree(2))


    def test_propagation_mult(self):
        g = nx.DiGraph()
        g.add_node(0)
        graph_creation.add_sybil_region(g,40,1)
        #g.add_edges_from([(0,1),(1,2),(2,3),(3,1)])
        votetrust.vote_assignment(g, [0])
        votetrust.vote_propagation_mat(g, d=0.99)
        print(g.node[0]['vote_capacity'])
        print(sum([g.node[x]['vote_capacity'] for x in range(1,41)]))

    def test_getFriends(self):
        g = nx.DiGraph()
        g.add_edges_from([(0,1,{'trust':1}),(0,2,{'trust':1}),(3,0,{'trust':1})])

        friends = votetrust.getFriends(g,0)
        print(friends)

    def test_Collusion_vs_d(self):
        g = graph_creation.create_directed_smallWorld(2000, 40)
        NUM_NODES = len(g.nodes())
        DUMMY = NUM_NODES
        ATTACKER = DUMMY+1
        requested = []
        for i in range(40):
            while True:
                r = floor(random.random()*NUM_NODES)
                if r not in requested:
                    g.add_edge(r,DUMMY,{'trust':1})
                    requested.append(r)
                    break

        g.add_edge(DUMMY, ATTACKER, {'trust':1})
        g.add_edge(ATTACKER, ATTACKER + 1, {'trust':1})
        g.add_edge(ATTACKER+1,ATTACKER + 2, {'trust':1})
        g.add_edge(ATTACKER+2,ATTACKER,{'trust':1})
        g.add_edge(ATTACKER+1,ATTACKER+3,{'trust':1})
        g.add_edge(ATTACKER+3,ATTACKER-10,{'trust':1})
        g.add_edge(ATTACKER+3,ATTACKER-11,{'trust':1})
        g.add_edge(ATTACKER+3,ATTACKER-12,{'trust':1})
        g.add_edge(ATTACKER+3,ATTACKER-13,{'trust':1})
        g.add_edge(ATTACKER+3,ATTACKER-14,{'trust':1})


        votetrust.vote_assignment(g, [0])
        votetrust.vote_propagation(g, d=0.95)
        print(g.node[DUMMY]['vote_capacity'])
        print(g.node[ATTACKER]['vote_capacity'])

        print(sum(g.node[x]['vote_capacity'] for x in g.nodes()))

    def test_voteComb(self):
        g = nx.DiGraph()
        g.add_edges_from([(0,1, {'trust': 1}),(0,2, {'trust': 1}),(3,1, {'trust': 1}),(3,2,{'trust': 0}),(3,0,{'trust':0})])
        votetrust.vote_assignment(g, [0])
        #votetrust.vote_propagation_mat(g)
        votetrust.vote_combined(g)