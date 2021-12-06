package day6

import (
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

func ReadLanternFishAgeFile(path string) ([]int, error) {
	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var ages []int

	nums := strings.Split(strings.TrimSpace(string(input)), ",")
	for _, n := range nums {
		age, err := strconv.Atoi(strings.TrimSpace(n))
		if err != nil {
			return nil, err
		}
		ages = append(ages, age)
	}

	return ages, nil
}

func day6part1(ages []int) int {
	// log.Printf("initial state: %v (%d)", ages, len(ages))
	// log.Printf("day,ages")
	for day := 0; day < 80; day++ {
		var newFish []int

		for i, fish := range ages {
			if fish == 0 {
				newFish = append(newFish, 8)
				ages[i] = 6
			} else {
				ages[i]--
			}
		}

		ages = append(ages, newFish...)
		// log.Printf("after %d days: %v", day, ages)
		// log.Printf("%d,%d", day+1, len(ages))
	}

	return len(ages)
}
