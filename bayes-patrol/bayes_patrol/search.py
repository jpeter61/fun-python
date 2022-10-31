#!/usr/bin/env python3
import sys
import cv2 as cv
import numpy as np
import random
import itertools


class SearchArea:
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
        self.region = img[
            self.ul_bound[1] : self.lr_bound[1],  # Y Range
            self.ul_bound[0] : self.lr_bound[0],  # X Range
        ]
        self.probability = probability
        self.sep = 0


class BayesSearch:
    """Search Map using Bayes."""

    def __init__(self, img, search_areas):
        """Something."""
        self.img = img
        self.search_areas = search_areas

        print("Generating Last Known")
        self.area_starting, self.sailor_last_known = self.gen_random_location()
        print("Generating Actual")
        self.area_actual, self.sailor_actual = self.gen_random_location()

        self.global_last_known = (
            self.sailor_last_known[0]
            + self.search_areas[self.area_starting].ul_bound[0],
            self.sailor_last_known[1]
            + self.search_areas[self.area_starting].ul_bound[1],
        )

        self.global_actual = (
            (self.sailor_actual[0] + self.search_areas[self.area_actual].ul_bound[0]),
            (self.sailor_actual[1] + self.search_areas[self.area_actual].ul_bound[1]),
        )

    def gen_random_location(self):
        """Generate random location in search areas."""
        # Select area from availble options
        area = int(random.triangular(0, len(self.search_areas)))
        print("Area {}".format(area))
        area_actual = self.search_areas[area]
        # Get random location in Search Area
        x = np.random.choice(area_actual.region.shape[1], 1)[0]
        print("X {}".format(x))
        y = np.random.choice(area_actual.region.shape[0], 1)[0]
        print("Y {}".format(y))
        return area, (x, y)

    def calc_search_effectiveness(self):
        """Set decimal search effectiveness values."""
        for area in self.search_areas:
            area.sep = random.uniform(0.2, 0.9)

    def conduct_search(self, area_number, effectiveness_prob):
        """Return search results and list of searched coordinates."""
        selected_area = self.search_areas[area_number]
        y_range = range(selected_area.region.shape[0])
        x_range = range(selected_area.region.shape[1])

        # generate search coordinates
        coords = list(itertools.product(x_range, y_range))
        random.shuffle(coords)
        coords = coords[: int((len(coords) * effectiveness_prob))]

        # Check if sailor is found
        if area_number == self.area_actual and self.sailor_actual in coords:
            return "Found sailor in Area {}.".format(area_number), coords
        else:
            return "Not Found", coords

    def revise_target_probs(self):
        """Update area target probabilities."""
        # Calculate denomitor for Bayes calculation
        denominator = 0.0
        for area in self.search_areas:
            denominator += area.probability * (1 - area.sep)

        # update probabilities
        for area in self.search_areas:
            area.probability = area.probability * (1 - area.sep) / denominator

    def draw_map(self):
        """Display the map with annotations."""
        # Draw the scale bar.
        cv.line(self.img, (20, 370), (70, 370), (0, 0, 0), 2)
        cv.putText(self.img, "0", (8, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(
            self.img,
            "50 Nautical Miles",
            (71, 370),
            cv.FONT_HERSHEY_PLAIN,
            1,
            (0, 0, 0),
        )

        # Draw Search Areas.
        for i, area in enumerate(self.search_areas):
            cv.rectangle(self.img, area.ul_bound, area.lr_bound, (0, 0, 0), 1)
            cv.putText(
                self.img,
                str(i + 1),
                (area.ul_bound[0] + 3, area.ul_bound[1] + 15),
                cv.FONT_HERSHEY_PLAIN,
                1,
                0,
            )

        print("Global Last Known: {}".format(self.global_last_known))
        # Post the last known location of the sailor.
        cv.putText(
            self.img,
            "+",
            (self.global_last_known[0], self.global_last_known[1]),
            cv.FONT_HERSHEY_PLAIN,
            1,
            (0, 0, 255),
        )
        cv.putText(
            self.img,
            "+ = Last Known Position",
            (274, 355),
            cv.FONT_HERSHEY_PLAIN,
            1,
            (0, 0, 255),
        )
        cv.putText(
            self.img,
            "* = Actual Position",
            (275, 370),
            cv.FONT_HERSHEY_PLAIN,
            1,
            (255, 0, 0),
        )

        cv.imshow("Search Area", self.img)
        cv.moveWindow("Search Area", 750, 10)
        cv.waitKey(500)
