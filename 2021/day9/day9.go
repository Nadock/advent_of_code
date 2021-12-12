package day9

import (
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

	sum := 0
	for _, point := range hm.lowPoints() {
		sum += hm.riskLevel(point[0], point[1])
	}

	return sum, nil
}

type heightmap [][]int

// x,y grid where 0,0 is the top left corner
func newHeightmap(gridRows []string) (*heightmap, error) {
	var hm heightmap

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

	return &hm, nil
}

func (hm *heightmap) inHeightmap(x, y int) bool {
	if x < 0 || x >= len(*hm) {
		return false
	}
	if y < 0 || y >= len((*hm)[x]) {
		return false
	}
	return true
}

func (hm *heightmap) lowPoints() [][]int {
	var points [][]int

	for x := 0; x < len(*hm); x++ {
		for y := 0; y < len((*hm)[x]); y++ {
			lower := true

			// up := hm[x][y-1]
			if hm.inHeightmap(x, y-1) {
				lower = lower && ((*hm)[x][y] < (*hm)[x][y-1])
			}
			// down := hm[x][y+1]
			if hm.inHeightmap(x, y+1) {
				lower = lower && ((*hm)[x][y] < (*hm)[x][y+1])
			}
			// left := hm[x-1][y]
			if hm.inHeightmap(x-1, y) {
				lower = lower && ((*hm)[x][y] < (*hm)[x-1][y])
			}
			// right := hm[x+1][y]
			if hm.inHeightmap(x+1, y) {
				lower = lower && ((*hm)[x][y] < (*hm)[x+1][y])
			}

			if lower {
				points = append(points, []int{x, y})
			}
		}
	}

	return points
}

func (hm *heightmap) riskLevel(x, y int) int {
	return (*hm)[x][y] + 1
}
