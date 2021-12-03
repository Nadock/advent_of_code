package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

func main() {
	answer, err := day1("./inputs/day1/part1/test_input.txt")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("The answer is %d\n", answer)
}

func day1(path string) (int, error) {
	day1Input, err := ioutil.ReadFile(path)
	if err != nil {
		return 0, err
	}

	lines := strings.Split(string(day1Input), "\n")
	var depths []int

	// Convert depth strings to integers
	for _, line := range lines {
		if line != "" {
			depth, err := strconv.Atoi(line)
			if err != nil {
				return 0, err
			}
			depths = append(depths, depth)
		}
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
