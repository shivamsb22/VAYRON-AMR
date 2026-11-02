import FreeCAD as App
import Part
import Import
import os

step_file = os.path.expanduser(
    "~/Downloads/4WD arduino buggy.stp"
)

doc = App.newDocument("VAYRON_INSPECTION")

print("\n========== IMPORTING STEP ==========")
Import.insert(step_file, doc.Name)
doc.recompute()

print("\n========== CAD OBJECT REPORT ==========")

total_solids = 0

for obj in doc.Objects:
    if not hasattr(obj, "Shape"):
        continue

    shape = obj.Shape

    if shape.isNull():
        continue

    solids = shape.Solids
    total_solids += len(solids)

    bb = shape.BoundBox

    print("\nObject:", obj.Name)
    print("Label:", obj.Label)
    print("Solids:", len(solids))
    print("Bounds (mm):",
          round(bb.XLength, 3),
          round(bb.YLength, 3),
          round(bb.ZLength, 3))
    print("Position (mm):",
          round(bb.XMin, 3),
          round(bb.YMin, 3),
          round(bb.ZMin, 3))

print("\n========== SUMMARY ==========")
print("Objects:", len(doc.Objects))
print("Total solids:", total_solids)

App.closeDocument(doc.Name)
