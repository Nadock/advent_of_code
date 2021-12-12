package day9

import (
	"log"
	"strconv"
	"strings"

	"2021.advent-of-code.rileychase.net/internal"
)

func day9part1(path string) (int, error) {
	lines, err := internal.ReadLines(path)
	if err != nil {
		return 0, err
	}

	hm, err := newHeightmap(lines)
	if err != nil {
		return 0, err
	}
	log.Printf("%v", hm)
	log.Printf("%v", lowPoints(hm))

	sum := 0
	for _, point := range lowPoints(hm) {
		log.Printf("risk at %v = %d", point, riskLevel(hm, point))
		sum += riskLevel(hm, point)
	}

	return sum, nil
}

// x,y grid where 0,0 is the top left corner
func newHeightmap(gridRows []string) ([][]int, error) {
	var hm [][]int

	for _, row := range gridRows {
		var values []int
		for _, rv := range strings.Split(row, "") {
			v, err := strconv.Atoi(rv)
			if err != nil {
				return nil, err
			}
			values = append(values, v)
		}
		hm = append(hm, values)
	}

	return hm, nil
}

func lowPoints(hm [][]int) [][]int {
	var points [][]int

	xMax := len(hm)
	for x := 0; x < xMax; x++ {
		yMax := len(hm[x])
		for y := 0; y < yMax; y++ {
			lower := true

			// up := hm[x][y-1]
			if y-1 >= 0 {
				lower = lower && (hm[x][y] < hm[x][y-1])
			}
			// down := hm[x][y+1]
			if y+1 < yMax {
				lower = lower && (hm[x][y] < hm[x][y+1])
			}
			// left := hm[x-1][y]
			if x-1 >= 0 {
				lower = lower && (hm[x][y] < hm[x-1][y])
			}
			// right := hm[x+1][y]
			if x+1 < xMax {
				lower = lower && (hm[x][y] < hm[x+1][y])
			}

			if lower {
				points = append(points, []int{x, y})
			}
		}
	}

	return points
}

func riskLevel(hm [][]int, point []int) int {
	return hm[point[0]][point[1]] + 1
}
