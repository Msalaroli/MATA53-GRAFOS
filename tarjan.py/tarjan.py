from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, Set, Dict, Optional

@dataclass
class Edge:
    v1: int
    v2: int
    sign: int = 1  # 1 for regular edge, -1 for back edge

class PlanarityTester:
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph = defaultdict(list)
        self.num = [-1] * vertices
        self.lowpt = [-1] * vertices
        self.lowpt2 = [-1] * vertices
        self.nesting_depth = {}  # Edge nesting depth
        self.parent = [-1] * vertices
        self.counter = 0
        self.edges = []
        self.sorted_edges = []
        
    def add_edge(self, u: int, v: int) -> None:
        """Add an undirected edge between vertices u and v"""
        self.graph[u].append(v)
        self.graph[v].append(u)
        
    def is_planar(self) -> bool:
        """Test if the graph is planar"""
        if not self._compute_numbers(0):
            return False
            
        self._compute_lowpoints()
        self._sort_edges()
        
        return self._test_planarity()
        
    def _compute_numbers(self, v: int) -> bool:
        """Perform DFS and compute DFS numbers"""
        self.counter += 1
        self.num[v] = self.counter
        
        for w in self.graph[v]:
            if self.num[w] == -1:
                self.parent[w] = v
                edge = Edge(v, w)
                self.edges.append(edge)
                if not self._compute_numbers(w):
                    return False
            elif self.num[w] < self.num[v] and w != self.parent[v]:
                edge = Edge(v, w, -1)  # Back edge
                self.edges.append(edge)
                
        return True
        
    def _compute_lowpoints(self) -> None:
        """Compute lowpoint values for vertices"""
        for v in range(self.V):
            if self.num[v] != -1:
                self.lowpt[v] = self.num[v]
                self.lowpt2[v] = self.num[v]
                
                for w in self.graph[v]:
                    if self.num[w] < self.num[v] and self.num[w] != self.parent[v]:  # Back edge
                        self.lowpt[v] = min(self.lowpt[v], self.num[w])
                    elif self.num[w] > self.num[v]:  # Tree edge to child
                        self.lowpt[v] = min(self.lowpt[v], self.lowpt[w])
                        self.lowpt2[v] = min(self.lowpt2[v], self.lowpt2[w])
                        
    def _sort_edges(self) -> None:
        """Sort edges according to the algorithm's requirements"""
        def edge_key(e: Edge) -> tuple:
            if e.sign == 1:  # Tree edge
                return (self.num[e.v2], 0)
            else:  # Back edge
                return (self.num[e.v1], 1)
                
        self.sorted_edges = sorted(self.edges, key=edge_key)
        
    def _test_planarity(self) -> bool:
        """Main planarity testing algorithm"""
        stack: List[List[Edge]] = []
        current_height = 0
        
        for edge in self.sorted_edges:
            if edge.sign == 1:  # Tree edge
                current_height += 1
                new_bucket: List[Edge] = []
                stack.append(new_bucket)
            else:  # Back edge
                height = self._compute_nesting_depth(edge)
                if height > current_height:
                    return False
                    
                while len(stack) > height:
                    bucket = stack.pop()
                    if not self._merge_edges(bucket, stack[-1] if stack else None):
                        return False
                    current_height -= 1
                    
                if stack:
                    stack[-1].append(edge)
                    
        # Clean up remaining stack
        while len(stack) > 1:
            bucket = stack.pop()
            if not self._merge_edges(bucket, stack[-1]):
                return False
                
        return True
        
    def _compute_nesting_depth(self, edge: Edge) -> int:
        """Compute the nesting depth of a back edge"""
        v = edge.v1
        w = edge.v2
        depth = 0
        
        while self.num[v] > self.num[w]:
            depth += 1
            v = self.parent[v]
            
        return depth
        
    def _merge_edges(self, bucket: List[Edge], target: Optional[List[Edge]]) -> bool:
        """Merge a bucket of edges into the target bucket"""
        if not target:
            return True
            
        # Check for edge crossings
        for edge1 in bucket:
            for edge2 in target:
                if self._edges_cross(edge1, edge2):
                    return False
                    
        target.extend(bucket)
        return True
        
    def _edges_cross(self, edge1: Edge, edge2: Edge) -> bool:
        """Check if two edges would cross in a planar embedding"""
        v1, w1 = sorted([edge1.v1, edge1.v2], key=lambda x: self.num[x])
        v2, w2 = sorted([edge2.v1, edge2.v2], key=lambda x: self.num[x])
        
        return (self.num[v1] < self.num[v2] < self.num[w1] < self.num[w2] or
                self.num[v2] < self.num[v1] < self.num[w2] < self.num[w1])
    


# Create a planar graph (K4 - complete graph with 4 vertices)
g = PlanarityTester(4)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(0, 3)
g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(2, 3)

# Test if the graph is planar
is_planar = g.is_planar()
print(f"Graph is planar: {is_planar}")  # Should print True

# Create a non-planar graph (K5 - complete graph with 5 vertices)
g = PlanarityTester(5)
for i in range(5):
    for j in range(i + 1, 5):
        g.add_edge(i, j)

is_planar = g.is_planar()
print(f"Graph is planar: {is_planar}")  # Should print False