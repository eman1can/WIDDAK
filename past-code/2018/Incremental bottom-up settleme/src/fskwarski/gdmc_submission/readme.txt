Incremental bottom-up settlement generator

The algorithm makes use of an implemention of the A* algorithm by Christian Careaga (which has been released by the author under the MIT License)

---

NOTE:

Before applying the filter, the area of the map where settlements should be generated should be selected manually. Using "select all" keyboard shortcut in Mcedit on default maps may cause the filter to get stuck / run at abysmally low speed.

The selection box must reach below the ground at its lowest point and above the ground at its highest point - if it includes a column of nothing but air at any point, the buildings will end generated at the very bottom of the map.

(Ideally, the box should reach above trees, otherwise bits of leaves or trunks may remain above the settlement.)

---

Assuming the default setting (50 structures) and a box containing a 256x256 gameplay area, the algorithm should not run substantially longer than 5 minutes - if the log doesn't move on to step 2 (generating structures), something has gone wrong. The step "Clearing trees..." may take a while, as it is currently unoptimized.