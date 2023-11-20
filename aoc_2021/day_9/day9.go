package day9

import (
	"log"
	"sort"
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

func day9part2(path string) (int, error) {
	lines, err := internal.ReadLines(path)
	if err != nil {
		return 0, err
	}

	hm, err := newHeightmap(lines)
	if err != nil {
		return 0, err
	}

	var basinSizes []int
	for _, point := range hm.lowPoints() {
		size := hm.basinSize(point[0], point[1])
		basinSizes = append(basinSizes, size)
		log.Printf("basin size at %v = %d", point, size)
	}

	sort.Sort(sort.Reverse(sort.IntSlice(basinSizes)))
	mul := 1
	for _, size := range basinSizes[:3] {
		mul *= size
	}

	return mul, nil
}

func (hm *heightmap) basinSize(x, y int) int {
	// Keep track of all points we've already seen
	var seen [][]bool
	for x := range *hm {
		seen = append(seen, make([]bool, len((*hm)[x])))
	}

	return hm.search(&seen, x, y)
}

func (hm *heightmap) search(seen *[][]bool, x, y int) int {
	if !hm.inHeightmap(x, y) || (*seen)[x][y] || (*hm)[x][y] == 9 {
		return 0
	}

	// Mark current point as seen so we don't double count it
	(*seen)[x][y] = true

	count := 1

	// Search up, down, left, and right of x,y
	count += hm.search(seen, x-1, y)
	count += hm.search(seen, x+1, y)
	count += hm.search(seen, x, y-1)
	count += hm.search(seen, x, y+1)

	return count
}
