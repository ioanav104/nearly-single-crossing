from preflibtools import io
import numpy as np
import networkx as nx
import matplotlib

def diff_orders(rank_maps, prev_rank, num_cand):
  """ Calculates the delta(<, <^) = {{a,b}| a < b and b <^ a}"""
  delta = []
  for rank_map in rank_maps:
      d = set([])
      for c1 in range(1, num_cand+1):
          for c2 in range(1, num_cand+1):
              if prev_rank[c1] < prev_rank[c2] and rank_map[c2] < rank_map[c1]:
                  d.add((c1, c2))
      delta.append(d)
  return delta
  

def build_graph(root, rank_maps, counts, num_cand):
  """ Builds n subgraphs starting at U_i_i """
  votes = len(rank_maps)
  dag = nx.DiGraph()
  dag.add_nodes_from(range(votes))
  delta = diff_orders(rank_maps, rank_maps[root], num_cand)
  for v1 in range(votes):
      for v2 in range(votes):
          if v1!=v2 and delta[v1].issubset(delta[v2]):
              dag.add_weighted_edges_from([(v1,v2,counts[v2])])
  return dag

def total_voters(path, counts):
    s = 0
    for v in path:
        s = s + v
    return s
            
def main():
  filename = input("Preference profile file: ")
  input_file = open(filename, 'r')
  cand_map, rank_maps, rank_map_counts, num_voters = io.read_election_file(input_file)
  print(rank_map_counts)
  for i in range(1):
    dag = build_graph(i, rank_maps, rank_map_counts, len(cand_map))
    nx.draw_networkx(dag)
    print(nx.dag_longest_path(dag, weight='weight'))
if __name__ == "__main__":
  main()
