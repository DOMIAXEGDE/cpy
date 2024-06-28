import FreeCAD, Part

# Create a new document
doc = FreeCAD.newDocument("Stainless_Steel_Slab")

# Create the stainless steel slab
slab = Part.makeBox(135, 63, 6)
slab_obj = doc.addObject("Part::Feature", "Slab")
slab_obj.Shape = slab

# Create the first slot (one-third down from the top, starting from the top face)
slot1 = Part.makeBox(5, 63, 3, FreeCAD.Vector((135-5)/3, 0, 6 - 3))

# Create the second slot (two-thirds down from the top, starting from the top face)
slot2 = Part.makeBox(5, 63, 3, FreeCAD.Vector(2*(135-5)/3, 0, 6 - 3))

# Cut the slots from the slab
cut1 = slab.cut(slot1)
cut2 = cut1.cut(slot2)
slab_obj.Shape = cut2

# Recompute the document
doc.recompute()

