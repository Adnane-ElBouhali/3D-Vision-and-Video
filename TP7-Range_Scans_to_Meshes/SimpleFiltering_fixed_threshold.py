# -*- coding: utf-8 -*-

import numpy as np
from scipy.spatial import Delaunay
import math

def vectorized_circumradius(p1, p2, p3):
    # Vectorized calculation of distances between points
    a = np.linalg.norm(p2 - p1)
    b = np.linalg.norm(p3 - p2)
    c = np.linalg.norm(p1 - p3)
    s = (a + b + c) / 2
    # Heron's formula for area
    A = np.sqrt(s * (s - a) * (s - b) * (s - c))
    # Circumradius formula
    r = (a * b * c) / (4 * A + 1e-10)
    return r

# Load the vertices
points3D = np.loadtxt("Bunny.xyz")

# Delaunay triangulation
tri = Delaunay(points3D)

# Preparing to write to STL file
stl_content = ["solid bunny\n"]
for tetra in tri.simplices:
    p1, p2, p3 = points3D[tetra[:3]]
    R = vectorized_circumradius(p1, p2, p3)
    if R < 0.005:
        stl_content.append("facet normal 0 0 0\n")
        stl_content.append("\touter loop\n")
        for point in (p1, p2, p3):
            stl_content.append(f"\t\tvertex {' '.join(map(str, point))}\n")
        stl_content.append("\tendloop\n")
        stl_content.append("endfacet\n")
stl_content.append("endsolid bunny")

# Write to the STL file in one go
with open("bunny.stl", "w") as o:
    o.writelines(stl_content)
