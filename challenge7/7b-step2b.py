
from definitions import *

manifolddefinitionfilename = './challenge7/manifold.txt'
quantumstatesfilename = './challenge7/quantum-b.txt'

print("reading manifold data...")
with open(manifolddefinitionfilename, "r", encoding="utf-8") as infile:
    lines = infile.read().splitlines()
    objects = [eval(line.strip()) for line in lines]

print("linking...")

objects_by_id = {obj.id: obj for obj in objects}

def link_children_as_refs(objects_by_id):
    for obj in objects_by_id.values():
        if hasattr(obj, "children") and obj.children:
            # Falls bisher IDs drin sind:
            if isinstance(obj.children[0], int):
                # Optional: Duplikate entfernen / Reihenfolge erhalten
                resolved = []
                for cid in obj.children:
                    child = objects_by_id.get(cid)
                    if child is None:
                        # Hier ggf. warnen/loggen statt still zu droppen:
                        # print(f"Warnung: Kind {cid} von Objekt {obj.id} fehlt.")
                        continue
                    resolved.append(child)
                obj.children = resolved

link_children_as_refs(objects_by_id)

print("computing quantum states...")

def dfs_all_paths_iter_refs(start_obj):
    """
    Iterative DFS mit Referenzen, erzeugt alle Pfade (als Tuple aus IDs).
    Speicher: O(Tiefe), Streaming-Ausgabe.
    """
    # Initialisierung
    path = [start_obj.id]
    on_stack = {start_obj.id}

    # Wenn Start bereits Output ist, Pfad liefern und fertig
    if isinstance(start_obj, Output):
        yield tuple(path)
        return

    # Stack-Frames: (node_obj, iterator_over_children)
    stack = [(start_obj, iter(getattr(start_obj, "children", ())))]

    while stack:
        node, it = stack[-1]
        try:
            child = next(it)
            cid = child.id

            # Zyklenschutz: im aktuellen Pfad bereits besucht?
            if cid in on_stack:
                continue

            # Knoten in den Pfad aufnehmen
            path.append(cid)
            on_stack.add(cid)

            # Falls Output oder Blatt -> Pfad ausgeben und direkt zurück
            children = getattr(child, "children", ())
            if isinstance(child, Output) or not children:
                yield tuple(path)
                # Sofortiges Backtracking des Childs (kein Frame pushen)
                on_stack.remove(cid)
                path.pop()
            else:
                # Tiefer gehen: Frame für das Kind pushen
                stack.append((child, iter(children)))

        except StopIteration:
            # Fertig mit den Kindern dieses Knotens: Frame entfernen und backtracken
            stack.pop()
            nid = path.pop()           # path[-1] entspricht dem node.id
            on_stack.remove(nid)

print("streaming all paths to file...")
start_obj = objects_by_id.get(1)
if start_obj is None:
    raise ValueError("Startobjekt mit ID=1 nicht gefunden.")

with open(quantumstatesfilename, "w", encoding="utf-8") as out:
    for p in dfs_all_paths_iter_refs(start_obj):
        out.write(" -> ".join(map(str, p)) + "\n")

print("done")