import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Slab dimensions
slab_length = 135
slab_width = 63
slab_thickness = 6

# Slot dimensions
slot_length = 5
slot_width = 63
slot_depth = 3

# Slot positions
slot1_x = (slab_length - slot_length) / 3
slot2_x = 2 * (slab_length - slot_length) / 3
slot_y = 0
slot_z = slab_thickness - slot_depth

# Create figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create the vertices of the slab
vertices = np.array([
    [0, 0, 0], [slab_length, 0, 0], [slab_length, slab_width, 0], [0, slab_width, 0],  # Bottom face
    [0, 0, slab_thickness], [slab_length, 0, slab_thickness], [slab_length, slab_width, slab_thickness], [0, slab_width, slab_thickness]  # Top face
])

# Define the 6 faces of the slab
faces = [
    [vertices[0], vertices[1], vertices[5], vertices[4]],  # Front face
    [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right face
    [vertices[2], vertices[3], vertices[7], vertices[6]],  # Back face
    [vertices[3], vertices[0], vertices[4], vertices[7]],  # Left face
    [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom face
    [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top face
]

# Add the faces of the slab to the plot
ax.add_collection3d(Poly3DCollection(faces, facecolors='gray', linewidths=1, edgecolors='black', alpha=0.5))

# Define the slots as smaller boxes and add them to the plot
slot1_vertices = np.array([
    [slot1_x, slot_y, slot_z], [slot1_x + slot_length, slot_y, slot_z], [slot1_x + slot_length, slot_y + slot_width, slot_z], [slot1_x, slot_y + slot_width, slot_z],
    [slot1_x, slot_y, slab_thickness], [slot1_x + slot_length, slot_y, slab_thickness], [slot1_x + slot_length, slot_y + slot_width, slab_thickness], [slot1_x, slot_y + slot_width, slab_thickness]
])

slot2_vertices = np.array([
    [slot2_x, slot_y, slot_z], [slot2_x + slot_length, slot_y, slot_z], [slot2_x + slot_length, slot_y + slot_width, slot_z], [slot2_x, slot_y + slot_width, slot_z],
    [slot2_x, slot_y, slab_thickness], [slot2_x + slot_length, slot_y, slab_thickness], [slot2_x + slot_length, slot_y + slot_width, slab_thickness], [slot2_x, slot_y + slot_width, slab_thickness]
])

slot_faces1 = [
    [slot1_vertices[0], slot1_vertices[1], slot1_vertices[5], slot1_vertices[4]],
    [slot1_vertices[1], slot1_vertices[2], slot1_vertices[6], slot1_vertices[5]],
    [slot1_vertices[2], slot1_vertices[3], slot1_vertices[7], slot1_vertices[6]],
    [slot1_vertices[3], slot1_vertices[0], slot1_vertices[4], slot1_vertices[7]],
    [slot1_vertices[0], slot1_vertices[1], slot1_vertices[2], slot1_vertices[3]],
    [slot1_vertices[4], slot1_vertices[5], slot1_vertices[6], slot1_vertices[7]]
]

slot_faces2 = [
    [slot2_vertices[0], slot2_vertices[1], slot2_vertices[5], slot2_vertices[4]],
    [slot2_vertices[1], slot2_vertices[2], slot2_vertices[6], slot2_vertices[5]],
    [slot2_vertices[2], slot2_vertices[3], slot2_vertices[7], slot2_vertices[6]],
    [slot2_vertices[3], slot2_vertices[0], slot2_vertices[4], slot2_vertices[7]],
    [slot2_vertices[0], slot2_vertices[1], slot2_vertices[2], slot2_vertices[3]],
    [slot2_vertices[4], slot2_vertices[5], slot2_vertices[6], slot2_vertices[7]]
]

ax.add_collection3d(Poly3DCollection(slot_faces1, facecolors='white', linewidths=1, edgecolors='black'))
ax.add_collection3d(Poly3DCollection(slot_faces2, facecolors='white', linewidths=1, edgecolors='black'))

# Set the limits and labels
ax.set_xlim([0, slab_length])
ax.set_ylim([0, slab_width])
ax.set_zlim([0, slab_thickness])
ax.set_xlabel('Length (mm)')
ax.set_ylabel('Width (mm)')
ax.set_zlabel('Thickness (mm)')
ax.set_title('3D View of Stainless Steel Slab with Slots')

# Equal aspect ratio
ax.set_box_aspect([slab_length, slab_width, slab_thickness])  # Aspect ratio is 1:1:1

# Show the plot
plt.show()
