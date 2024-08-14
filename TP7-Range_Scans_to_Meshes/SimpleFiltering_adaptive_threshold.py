import numpy as np
from scipy.spatial import Delaunay

def calculate_normal(p1, p2, p3):
    v1, v2 = p2 - p1, p3 - p1
    normal = np.cross(v1, v2)
    norm = np.linalg.norm(normal)
    return normal if norm == 0 else normal / norm

def circumradius(p1, p2, p3):
    # Edge lengths
    a = np.linalg.norm(p2 - p1)
    b = np.linalg.norm(p3 - p2)
    c = np.linalg.norm(p1 - p3)
    # Semiperimeter
    s = (a + b + c) / 2
    # Triangle area using Heron's formula
    area = np.sqrt(s * (s - a) * (s - b) * (s - c))
    # Circumradius formula for a triangle
    return (a * b * c) / (4 * area) if area > 0 else 0

# Load the vertices
points3D = np.loadtxt("Bunny.xyz")

# Delaunay triangulation
tri = Delaunay(points3D)

# Calculate circumradii
radii = np.array([circumradius(points3D[tetra[0]], points3D[tetra[1]], points3D[tetra[2]]) for tetra in tri.simplices])

# Adaptive threshold based on circumradii statistics
mean_radius, std_radius = np.mean(radii), np.std(radii)
threshold = mean_radius + std_radius  # Example: One standard deviation above the mean

# Filter triangles and write to STL
stl_content = ["solid bunny\n"]
for tetra, radius in zip(tri.simplices, radii):
    if radius <= threshold:  # Apply adaptive threshold
        p1, p2, p3 = points3D[tetra[:3]]
        normal = calculate_normal(p1, p2, p3)
        stl_content.extend([
            f"facet normal {' '.join(map(str, normal))}\n",
            "\touter loop\n",
            *[f"\t\tvertex {' '.join(map(str, point))}\n" for point in (p1, p2, p3)],
            "\tendloop\n",
            "endfacet\n"
        ])
stl_content.append("endsolid bunny")

with open("bunny_filtered.stl", "w") as o:
    o.writelines(stl_content)
