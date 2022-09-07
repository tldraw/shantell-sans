"""
    Uses FontTools buildStatTable to add a defined STAT table to a variable font
"""

from fontTools.otlLib.builder import buildStatTable, _addName
from fontTools.ttLib import TTFont
import sys


AXES = [
    dict(
        tag="wght",
        name="Weight",
        ordering=0,
        values=[
            dict(value=300, name="Light"),
            dict(value=400, name="Regular", flags=0x2, linkedValue=700),
            dict(value=500, name="Medium"),
            dict(value=600, name="SemiBold"),
            dict(value=700, name="Bold"),
            dict(value=800, name="ExtraBold"),
        ],
    ),
    dict(
        tag="ital",
        name="Italic",
        ordering=1,
        values=[
            dict(value=0, name="Roman", flags=0x2, linkedValue=1),
            dict(value=1,  name="Italic"),
        ],
    ),
    dict(
        tag="BNCE",
        name="Bounce",
        ordering=2,
        values=[
            dict(nominalValue=0, rangeMinValue=0, rangeMaxValue=0, name="No Bounce", flags=0x2),
            dict(nominalValue=62.5, rangeMinValue=0.00001, rangeMaxValue=62.5,  name="Bouncy"),
            dict(nominalValue=100, rangeMinValue=62.50001, rangeMaxValue=100,  name="ExtraBouncy"),
        ],
    ),
    dict(
        tag="IRGL",
        name="Irregularity",
        ordering=3,
        values=[
            dict(nominalValue=0, rangeMinValue=0, rangeMaxValue=25, name="Normalized", flags=0x2),
            dict(nominalValue=100, rangeMinValue=25.00001, rangeMaxValue=100,  name="Irregular"),
        ],
    ),
    dict(
        tag="TRAK",
        name="Tracking",
        ordering=4,
        values=[
            dict(nominalValue=0, rangeMinValue=0, rangeMaxValue=0, name="No Tracking", flags=0x2),
            dict(nominalValue=500, rangeMinValue=0.00001, rangeMaxValue=500,  name="Tracked"),
        ],
    ),
]

## adds 
def update_fvar(ttfont):
    fvar = ttfont['fvar']
    nametable = ttfont['name']
    family_name = nametable.getName(16, 3, 1, 1033) or nametable.getName(1, 3, 1, 1033)
    family_name = family_name.toUnicode().replace(" ", "")
    nametable.setName(family_name, 25, 3, 1, 1033)
    for instance in fvar.instances:
        instance_style = nametable.getName(instance.subfamilyNameID, 3, 1, 1033).toUnicode()
        ps_name = f"{family_name}-{instance_style.replace(' ', '')}"
        instance.postscriptNameID = _addName(nametable, ps_name, 256)


def main():
    filepath = sys.argv[1]
    tt = TTFont(filepath)

    buildStatTable(tt, AXES)
    update_fvar(tt)
    tt.save(filepath)
    print(f"Added STAT table to {filepath}")


if __name__ == "__main__":
    main()
