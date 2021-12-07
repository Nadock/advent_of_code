package day7

import (
	"io/ioutil"
	"log"
	"math"
	"strconv"
	"strings"
)

func ReadCrabPositionsFile(path string) ([]int, error) {
	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	values := strings.Split(strings.TrimSpace(string(input)), ",")
	var positions []int
	for _, value := range values {
		if value != "" {
			val, err := strconv.Atoi(value)
			if err != nil {
				return nil, err
			}
			positions = append(positions, val)
		}
	}

	return positions, nil
}

func day7part1(positions []int) int {
	min, max := listMinMax(positions)

	minCost := -1
	// minPos := 0
	for i := min; i <= max; i++ {
		cost := calcFuelCost(positions, i)
		log.Printf("cost to move to position %d is %d", i, cost)
		if minCost == -1 || cost < minCost {
			minCost = cost
			// minPos = i
		}
	}

	return minCost
}

func listMinMax(l []int) (int, int) {
	min, max := 0, 0
	for _, v := range l {
		min = int(math.Min(float64(min), float64(v)))
		max = int(math.Max(float64(max), float64(v)))
	}
	return min, max
}

func calcFuelCost(positions []int, moveTo int) int {
	total := 0
	for _, p := range positions {
		total += int(math.Abs(float64(p - moveTo)))
	}
	return total
}
