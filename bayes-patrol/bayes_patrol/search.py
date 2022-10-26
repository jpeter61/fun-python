#!/usr/bin/env python3
import sys
import cv2 as cv

MAP_FILE = "cape_python.png"
# Assign search area (SA) corner point locations based on image pixels.
SA_CONSTANTS = [((130, 265), (180, 315), 0.2),
                ((80, 255), (130, 305), 0.5),
                ((105, 205), (155, 255), 0.3)]

# ((UL-X, UL-Y), (LR-X, LR-Y), probability)
LAST_KNOWN = (105, 255)


class SearchArea():
    """Object for Search Areas."""

    def __init__(self, img, ul_bound, lr_bound, probability):
        """Create the Search Area.

        img = cv image array
        ul_bound = upper-left point of the search area
        lr_bound = lower-left point of the search area
        probability = float
        """
        self.ul_bound = ul_bound
        self.lr_bound = lr_bound
        self.region = img[self.ul_bound[1]:self.lr_bound[1],  # Y Range
                          self.ul_bound[0]:self.lr_bound[0]]  # X Range
        self.probability = probability
        self.sep = 0


class BayesSearch():
    """Search Map using Bayes."""

    def __init__(self):
        """Something."""
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        if self.img is None:
            print("Can not load file {}".format(MAP_FILE), file=sys.stderr)
            sys.exit(1)

        self.area_actual = 0
        self.sailor_actual = [0, 0]

        self.search_areas = []
        for area in SA_CONSTANTS:
            self.search_areas.append(
                SearchArea(self.img, area[0], area[1], area[2]))

    def draw_map(self):
        """Display the map with annotations."""
        # Draw the scale bar.
        cv.line(self.img, (20, 370), (70, 370), (0, 0, 0), 2)
        cv.putText(self.img, '0', (8, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, '50 Nautical Miles', (71, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        # Draw Search Areas.
        for i, area in enumerate(self.search_areas):
            cv.rectangle(self.img, area.ul_bound, area.lr_bound,
                         (0, 0, 0), 1)
            cv.putText(self.img, str(i+1),
                       (area.ul_bound[0] + 3, area.ul_bound[1] + 15),
                       cv.FONT_HERSHEY_PLAIN, 1, 0)

        # Post the last known location of the sailor.
        cv.putText(self.img, '+', (LAST_KNOWN),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.img, '+ = Last Known Position', (274, 355),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.img, '* = Actual Position', (275, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

        cv.imshow('Search Area', self.img)
        cv.moveWindow('Search Area', 750, 10)
        cv.waitKey(50000)
