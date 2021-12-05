package day1

import (
	"io/ioutil"
	"strconv"
	"strings"
)

func ReadDepthFile(path string) ([]int, error) {
	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	lines := strings.Split(string(input), "\n")
	var depths []int

	// Convert depth strings to integers
	for _, line := range lines {
		if line != "" {
			depth, err := strconv.Atoi(line)
			if err != nil {
				return nil, err
			}
			depths = append(depths, depth)
		}
	}

	return depths, nil
}
