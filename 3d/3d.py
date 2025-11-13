import open3d as o3d
import numpy as np

file = "psyduck.ply"

mesh = o3d.io.read_triangle_mesh(file)
mesh.compute_vertex_normals()


# Loading and Visualisation
print("\n./*~~*\. MESH INFO ./*~~*\.")
print("Vertices:", len(mesh.vertices))
print("Triangles:", len(mesh.triangles))
print("Has Colors:", mesh.has_vertex_colors())
print("Has Normals", mesh.has_vertex_normals())

mesh.paint_uniform_color([0.99, 0.73, 0.17])

o3d.visualization.draw_geometries([mesh], window_name="original mesh", width=500, height=500)


# Conversion to Point Cloud
point_cloud = o3d.io.read_point_cloud(file)

# o3d.visualization.draw_geometries([point_cloud], window_name="point_cloud", width=500, height=500)

print("\n./*~~*\. POINT CLOUD INFO ./*~~*\.")
print("Points:", len(point_cloud.points))
print("Has Colors:", point_cloud.has_colors())


#Surface Reconstruction from Point Cloud
recon_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=8)

bbox = point_cloud.get_axis_aligned_bounding_box()
mesh_crop = recon_mesh.crop(bbox)

# o3d.visualization.draw_geometries([recon_mesh], window_name="reconstructed mesh", width=500, height=500)

print("\n./*~~*\. RECONSTRUCTED MESH INFO ./*~~*\.")
print("Vertices:", len(recon_mesh.vertices))
print("Triangles:", len(recon_mesh.triangles))
print("Has Colors:", recon_mesh.has_vertex_colors())


# Voxelization
voxel_size = 0.05
voxel = o3d.geometry.VoxelGrid.create_from_point_cloud(point_cloud, voxel_size=voxel_size)

# o3d.visualization.draw_geometries([voxel], window_name="voxel grid", width=500, height=500)

print("\n./*~~*\. VOXEL GRID INFO ./*~~*\.")
print("Voxel size:", voxel_size)
print("Voxels:", len(voxel.get_voxels()))
print("Has Colors:", voxel.has_colors())


# Adding a Plane
plane = o3d.geometry.TriangleMesh.create_box(width=4, height=0.01, depth=2.5)
plane.paint_uniform_color([0.8, 0.1, 0.1])
plane.translate([-2, 0.05, 0.2])

rx = np.pi / 2
ry = 0
rz = np.pi / 8
R = plane.get_rotation_matrix_from_xyz([rx, ry, rz])
plane.rotate(R, center=plane.get_center())

# o3d.visualization.draw_geometries([mesh, plane], window_name="mesh and plane", width=500, height=500)


# Surface Clipping
vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)
plane_center = np.asarray(plane.get_center())
plane_normal = np.array([0, 1, 0])

R = plane.get_rotation_matrix_from_xyz([rx, ry, rz])
plane_normal = R @ plane_normal

mask = np.dot(plane_center - vertices, plane_normal) > 0

tri_mask = np.all(mask[triangles], axis=1)

mesh_clipped = o3d.geometry.TriangleMesh()
mesh_clipped.vertices = o3d.utility.Vector3dVector(vertices[mask])
old_to_new = np.full(len(vertices), -1)
old_to_new[mask] = np.arange(np.count_nonzero(mask))
new_triangles = [old_to_new[tri] for tri, keep in zip(triangles, tri_mask) if keep]
mesh_clipped.triangles = o3d.utility.Vector3iVector(np.array(new_triangles))

if mesh.has_vertex_colors():
    mesh_clipped.vertex_colors = o3d.utility.Vector3dVector(np.asarray(mesh.vertex_colors)[mask])

mesh_clipped.compute_vertex_normals()

# o3d.visualization.draw_geometries([mesh_clipped], window_name="Clipped Mesh", width=500, height=500)

print("\n./*~~*\. CLIPPED MESH INFO ./*~~*\.")
print("Vertices:", len(mesh_clipped.vertices))
print("Triangles:", len(mesh_clipped.triangles))
print("Has Colors:", mesh_clipped.has_vertex_colors())
print("Has Normals", mesh_clipped.has_vertex_normals())


# Working with Color and Extremes
axis = 2
vertices = np.asarray(mesh.vertices)
vals = vertices[:, axis]
vals_norm = (vals - vals.min()) / (vals.max() - vals.min() + 1e-8)
colors = np.stack([vals_norm, 0.5 * np.ones_like(vals_norm), 1 - vals_norm], axis=1)
mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

min_idx = np.argmin(vals)
max_idx = np.argmax(vals)
p_min, p_max = vertices[min_idx], vertices[max_idx]

sphere_min = o3d.geometry.TriangleMesh.create_box(width=0.3, height=0.3, depth=0.3)
sphere_min.translate(p_min)
sphere_min.paint_uniform_color([0, 0, 1])

sphere_max = o3d.geometry.TriangleMesh.create_box(width=0.3, height=0.3, depth=0.3)
sphere_max.translate(p_max)
sphere_max.paint_uniform_color([1, 0, 0])

wire_min = o3d.geometry.LineSet.create_from_triangle_mesh(sphere_min)
wire_max = o3d.geometry.LineSet.create_from_triangle_mesh(sphere_max)

o3d.visualization.draw_geometries([mesh, wire_min, wire_max],window_name="Gradient and Extrema", width=500, height=500)

print("\n./*~~*\. EXTREMES ./*~~*\.")
print("Min", ['X','Y','Z'][axis], ": {p_min}")
print("Max", ['X','Y','Z'][axis], ": {p_max}")
