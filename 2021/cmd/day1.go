package main

func day1Part1(depths []int) (int, error) {
	return countDepthIncreases(depths), nil
}

// Find number of times the depth value increased
func countDepthIncreases(depths []int) int {
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
	return increase_count
}

func day1Part2(depths []int) (int, error) {

	// Calculate depths for a 3-wide sliding window
	window_size := 3
	var window_depths []int

	for idx := range depths {
		if idx+window_size > len(depths) {
			break
		}

		window_depth := 0
		for widx := 0; widx < window_size; widx++ {
			window_depth += depths[idx+widx]
		}

		window_depths = append(window_depths, window_depth)
	}

	return countDepthIncreases(window_depths), nil
}
