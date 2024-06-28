import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Create the slab as a rectangle
slab = patches.Rectangle((0, 0), slab_length, slab_thickness, linewidth=1, edgecolor='black', facecolor='gray')
ax.add_patch(slab)

# Create the first slot
slot1 = patches.Rectangle((slot1_x, slab_thickness - slot_depth), slot_length, slot_depth, linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(slot1)

# Create the second slot
slot2 = patches.Rectangle((slot2_x, slab_thickness - slot_depth), slot_length, slot_depth, linewidth=1, edgecolor='black', facecolor='white')
ax.add_patch(slot2)

# Set the limits and aspect ratio
ax.set_xlim(-10, slab_length + 10)
ax.set_ylim(-10, slab_thickness + 10)
ax.set_aspect('equal')

# Add labels and title
ax.set_xlabel('Length (mm)')
ax.set_ylabel('Thickness (mm)')
ax.set_title('Stainless Steel Slab with Slots')

# Show the plot
plt.grid(True)
plt.show()
