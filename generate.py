#!/usr/bin/env python3
"""Generate obby.rbxlx — Floating Islands Obby (10 stages). Pure stdlib."""

import os

R = 0  # referent counter


def ref():
    global R
    R += 1
    return f"RBX{R}"


def pack(r, g, b):
    return (255 << 24) | (r << 16) | (g << 8) | b


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def strval(name, value):
    return (f'<Item class="StringValue" referent="{ref()}"><Properties>'
            f'<string name="Name">{esc(name)}</string>'
            f'<string name="Value">{esc(value)}</string></Properties></Item>')


def part(name, size, pos, color, mat=272, transparency=0.0, cancollide=True,
         cls="Part", values=None):
    x, y, z = pos
    sx, sy, sz = size
    children = "".join(strval(k, v) for k, v in (values or {}).items())
    return (f'<Item class="{cls}" referent="{ref()}"><Properties>'
            f'<string name="Name">{esc(name)}</string>'
            f'<bool name="Anchored">true</bool>'
            f'<bool name="CanCollide">{str(cancollide).lower()}</bool>'
            f'<token name="Material">{mat}</token>'
            f'<Color3uint8 name="Color3uint8">{pack(*color)}</Color3uint8>'
            f'<float name="Transparency">{transparency}</float>'
            f'<Vector3 name="size"><X>{sx}</X><Y>{sy}</Y><Z>{sz}</Z></Vector3>'
            f'<CoordinateFrame name="CFrame"><X>{x}</X><Y>{y}</Y><Z>{z}</Z>'
            f'<R00>1</R00><R01>0</R01><R02>0</R02>'
            f'<R10>0</R10><R11>1</R11><R12>0</R12>'
            f'<R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame>'
            f'<token name="TopSurface">0</token>'
            f'<token name="BottomSurface">0</token>'
            f'</Properties>{children}</Item>')


# materials
GRASS, PLASTIC, NEON, PLATE = 1280, 272, 288, 1056
# colors
C_ISLAND = (96, 150, 72)
C_PATH = (200, 196, 188)
C_KILL = (255, 64, 64)
C_CP = (120, 255, 120)
C_PAD = (0, 220, 255)
C_WIN = (255, 200, 40)
C_WARN = (255, 140, 0)
C_CONV = (80, 84, 88)
C_CLOUD = (240, 240, 245)

parts = []  # (folder, xml)

def add(folder, xml):
    parts.append((folder, xml))


def island(name, size, pos, color=C_ISLAND):
    add("Terrain", part(name, size, pos, color, GRASS))


def checkpoint(idx, pos):
    add("Checkpoints", part(f"Checkpoint{idx}", (4, 0.6, 4), pos, C_CP, NEON))


# ---- spawn ----
island("SpawnIsland", (24, 1, 24), (0, 0, 0))
spawn_xml = (
    f'<Item class="SpawnLocation" referent="{ref()}"><Properties>'
    f'<string name="Name">Spawn</string><bool name="Anchored">true</bool>'
    f'<bool name="Neutral">true</bool><float name="Duration">0</float>'
    f'<token name="Material">{PLASTIC}</token>'
    f'<Color3uint8 name="Color3uint8">{pack(230, 230, 230)}</Color3uint8>'
    f'<Vector3 name="size"><X>12</X><Y>1</Y><Z>12</Z></Vector3>'
    f'<CoordinateFrame name="CFrame"><X>0</X><Y>1</Y><Z>0</Z>'
    f'<R00>1</R00><R01>0</R01><R02>0</R02><R10>0</R10><R11>1</R11><R12>0</R12>'
    f'<R20>0</R20><R21>0</R21><R22>1</R22></CoordinateFrame>'
    f'<token name="TopSurface">0</token><token name="BottomSurface">0</token>'
    f'</Properties></Item>')
spawn_part = spawn_xml

# ---- stage 1: jump gaps ----
for z in (19, 29, 39, 49):
    island(f"S1Platform{z}", (6, 1, 6), (0, 0, z))
island("S1Island", (14, 1, 14), (0, 0, 65))
checkpoint(1, (0, 0.8, 65))

# ---- stage 2: kill strips ----
island("S2Base", (14, 1, 36), (0, 0, 96))
for z in (86, 96, 106):
    add("Kill", part(f"S2KillStrip{z}", (14, 0.5, 2), (0, 0.75, z), C_KILL, NEON))
island("S2Island", (14, 1, 14), (0, 0, 127))
checkpoint(2, (0, 0.8, 127))

# ---- stage 3: moving platform chasm ----
island("S3LedgeA", (8, 1, 8), (0, 0, 142))
island("S3LedgeB", (8, 1, 8), (0, 0, 182))
add("Movers", part("S3Slider", (8, 1, 8), (0, 0, 162), C_PATH, PLASTIC,
                   values={"Slide": "12|6"}))
island("S3Island", (14, 1, 14), (0, 0, 199))
checkpoint(3, (0, 0.8, 199))

# ---- stage 4: spinner ----
island("S4Island", (18, 1, 18), (0, 0, 221))
add("Movers", part("S4Spinner", (18, 1, 1.5), (0, 1.75, 221), C_WARN, PLASTIC,
                   values={"Spin": "90"}))
island("S4IslandCP", (14, 1, 14), (0, 0, 243))
checkpoint(4, (0, 0.8, 243))

# ---- stage 5: jump pads up ----
add("Pads", part("S5Pad1", (6, 0.6, 6), (0, 0.3, 257), C_PAD, NEON,
                 values={"Launch": "115"}))
island("S5Ledge1", (6, 1, 6), (0, 8, 269))
add("Pads", part("S5Pad2", (6, 0.6, 6), (0, 8.8, 266), C_PAD, NEON,
                 values={"Launch": "115"}))
island("S5Ledge2", (6, 1, 6), (0, 16, 279))
add("Pads", part("S5Pad3", (6, 0.6, 6), (0, 16.8, 277), C_PAD, NEON,
                 values={"Launch": "115"}))
island("S5Ledge3", (6, 1, 6), (0, 24, 289))
island("S5Island", (14, 1, 14), (0, 24, 307))
checkpoint(5, (0, 24.8, 307))

# ---- stage 6: balance beam ----
island("S6Beam", (2, 1, 36), (0, 24, 338), C_PATH)
island("S6Island", (14, 1, 14), (0, 24, 369))
checkpoint(6, (0, 24.8, 369))

# ---- stage 7: conveyor pushback ----
island("S7Base", (14, 1, 36), (0, 24, 400))
add("Movers", part("S7Conveyor", (14, 0.5, 34), (0, 24.35, 400), C_CONV, PLATE,
                   values={"Conveyor": "-8"}))
island("S7Island", (14, 1, 14), (0, 24, 431))
checkpoint(7, (0, 24.8, 431))

# ---- stage 8: truss climb ----
island("S8Island", (12, 1, 12), (0, 24, 450))
add("Terrain", part("S8Wall", (12, 24, 2), (0, 36, 457), C_PATH, PLASTIC))
add("Terrain", part("S8Truss", (2, 24, 2), (0, 36, 454), (120, 120, 124),
                    PLATE, cls="TrussPart"))
island("S8Ledge", (12, 1, 12), (0, 48, 462))
checkpoint(8, (0, 48.8, 462))

# ---- stage 9: zigzag stairs + kill brick ----
xs = (-4, 4, -4, 4, -4, 4)
for k in range(6):
    y = 48.5 + 2 * k
    z = 472 + 6 * k
    island(f"S9Step{k+1}", (4, 1, 4), (xs[k], y, z), C_PATH)
add("Kill", part("S9Kill", (2, 1, 2), (-3, 53.5, 486), C_KILL, NEON))
island("S9Top", (12, 1, 12), (0, 60, 514))
checkpoint(9, (0, 60.8, 514))

# ---- stage 10: final gauntlet + win ----
island("S10Bridge", (4, 1, 24), (0, 60, 538), C_PATH)
add("Movers", part("S10Spin1", (8, 1, 1.5), (0, 61.75, 534), C_WARN, PLASTIC,
                   values={"Spin": "120"}))
add("Movers", part("S10Spin2", (8, 1, 1.5), (0, 61.75, 544), C_WARN, PLASTIC,
                   values={"Spin": "-120"}))
island("WinIsland", (16, 1, 16), (0, 60, 564))
add("WinPad", part("WinPad", (8, 0.6, 8), (0, 60.8, 564), C_WIN, NEON))
add("Decor", part("WinBeam", (2, 40, 2), (0, 82, 564), C_WIN, NEON,
                  transparency=0.5, cancollide=False))

# ---- void kill floor ----
add("Kill", part("VoidFloor", (300, 1, 700), (0, -25, 280), (0, 0, 0), PLASTIC,
                 transparency=1.0, cancollide=False))

# ---- decor islands + clouds ----
for i, (x, y, z, s) in enumerate([(40, -6, 100, 12), (-45, -10, 220, 16),
                                  (35, -14, 380, 14), (-40, -18, 500, 12),
                                  (25, -4, 40, 8), (-30, -8, 540, 10)]):
    island(f"DecoIsland{i}", (s, 1, s), (x, y, z), (82, 130, 62))
for i, (x, y, z) in enumerate([(30, 10, 150), (-35, 14, 300), (28, 20, 460),
                               (-30, 8, 80)]):
    add("Decor", part(f"Cloud{i}", (14, 2, 8), (x, y, z), C_CLOUD, PLASTIC,
                      transparency=0.35, cancollide=False))

# ---- assemble XML ----
folders = {"Terrain": [], "Checkpoints": [], "Kill": [], "Movers": [],
           "Pads": [], "WinPad": [], "Decor": []}
for folder, xml in parts:
    folders[folder].append(xml)

obby_inner = ""
for fname, items in folders.items():
    obby_inner += (f'<Item class="Folder" referent="{ref()}"><Properties>'
                   f'<string name="Name">{fname}</string></Properties>'
                   + "".join(items) + "</Item>")

with open(os.path.join(os.path.dirname(__file__), "ObbyLogic.lua"),
          encoding="utf-8") as f:
    lua = f.read()
assert "]]>" not in lua, "CDATA break"

script_xml = (f'<Item class="Script" referent="{ref()}"><Properties>'
              f'<string name="Name">ObbyLogic</string>'
              f'<bool name="Disabled">false</bool>'
              f'<ProtectedString name="Source"><![CDATA[{lua}]]></ProtectedString>'
              f'</Properties></Item>')

lighting = (
    f'<Item class="Lighting" referent="{ref()}"><Properties>'
    f'<Color3uint8 name="Ambient">{pack(120, 110, 120)}</Color3uint8>'
    f'<Color3uint8 name="OutdoorAmbient">{pack(150, 130, 125)}</Color3uint8>'
    f'<float name="Brightness">2.5</float><float name="ClockTime">17.2</float>'
    f'<Color3uint8 name="FogColor">{pack(255, 160, 120)}</Color3uint8>'
    f'<float name="FogStart">150</float><float name="FogEnd">700</float>'
    f'<bool name="GlobalShadows">true</bool>'
    f'</Properties></Item>')

workspace_xml = (f'<Item class="Workspace" referent="{ref()}"><Properties>'
                 f'<string name="Name">Workspace</string></Properties>'
                 + spawn_part + obby_inner + "</Item>")

sss_xml = (f'<Item class="ServerScriptService" referent="{ref()}"><Properties>'
           f'<string name="Name">ServerScriptService</string></Properties>'
           + script_xml + "</Item>")

doc = ('<roblox version="4">' + workspace_xml + sss_xml + lighting
       + "</roblox>")

out = os.path.join(os.path.dirname(__file__), "obby.rbxlx")
with open(out, "w", encoding="utf-8") as f:
    f.write(doc)

# self-check: XML parses, counts sane
import xml.etree.ElementTree as ET
tree = ET.parse(out)
n_parts = doc.count("<Item class=")
n_cp = sum(1 for i in range(1, 10) if f">Checkpoint{i}<" in doc)
assert n_cp == 9, n_cp
print(f"OK {out}: {os.path.getsize(out)} bytes, {n_parts} items, {n_cp} checkpoints")
