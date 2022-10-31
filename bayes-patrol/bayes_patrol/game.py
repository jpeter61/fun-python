#!/usr/bin/env python3
import sys
import search
import cv2 as cv

MAP_FILE = "cape_python.png"
# Assign search area (SA) corner point locations based on image pixels.
SA_CONSTANTS = [
    ((130, 265), (180, 315), 0.2),
    ((80, 255), (130, 305), 0.5),
    ((105, 205), (155, 255), 0.3),
]


def main():
    """UI Driver Code."""
    img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
    if img is None:
        print("Can not load file {}".format(MAP_FILE), file=sys.stderr)
        sys.exit(1)

    search_areas = []
    for area in SA_CONSTANTS:
        search_areas.append(search.SearchArea(img, area[0], area[1], area[2]))
    print("Starting the game:")
    app = search.BayesSearch(img, search_areas)
    app.draw_map()


if __name__ == "__main__":
    main()
