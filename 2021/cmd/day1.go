package main

import "2021.advent-of-code.rileychase.net/internal/utils"

func day1Part1(path string) (int, error) {
	depths, err := utils.ReadDepthFile(path)
	if err != nil {
		return 0, err
	}

	// Find number of times the depth value increased
	previous_depth := -1
	increase_count := 0
	for _, depth := range depths {
		if previous_depth >= 0 {
			if depth > previous_depth {
				increase_count++
			}
		}

		previous_depth = depth
	}

	return increase_count, nil
}
