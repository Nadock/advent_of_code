package day11

import (
	"log"
	"strconv"
	"strings"

	"2021.advent-of-code.rileychase.net/internal"
)

func day11part1(path string) (int, error) {
	lines, err := internal.ReadLines(path)
	if err != nil {
		return 0, err
	}
	og, err := newGrid(lines)
	if err != nil {
		return 0, err
	}

	og.simulate(100)

	return og.flashes, nil
}

type octopusGrid struct {
	grid    [][]int
	flashed [][]bool
	flashes int
}

func newGrid(lines []string) (*octopusGrid, error) {
	g := octopusGrid{}
	for _, l := range lines {
		var row []int
		for _, s := range strings.Split(l, "") {
			v, err := strconv.Atoi(s)
			if err != nil {
				return nil, err
			}
			row = append(row, v)
		}
		g.grid = append(g.grid, row)
		g.flashed = append(g.flashed, make([]bool, len(row)))
	}

	return &g, nil
}

func (og *octopusGrid) simulate(steps int) {
	for i := 0; i < steps; i++ {
		og.increaseEneryStep()
		og.flashOctopusesStep()
		og.resetFlashedStep()
		log.Printf("after %d steps, %d flashes", i+1, og.flashes)
	}
}

func (g *octopusGrid) increaseEneryStep() {
	// log.Printf("incrementing each grid point by 1")
	for x := 0; x < len(g.grid); x++ {
		for y := 0; y < len(g.grid[x]); y++ {
			g.grid[x][y]++
		}
	}
}

func (og *octopusGrid) flashOctopusesStep() {
	// log.Printf("checking each grid for point for values > 9 to flash")
	for x := 0; x < len(og.grid); x++ {
		for y := 0; y < len(og.grid[x]); y++ {
			if og.grid[x][y] > 9 {
				// log.Printf("flashing grid point %d,%d=%d", x, y, og.grid[x][y])
				og.flash(x, y)
			}
		}
	}
}

func (og *octopusGrid) flash(x, y int) {
	if og.flashed[x][y] {
		// log.Printf("%d,%d already flashed this step", x, y)
		return
	}

	// log.Printf("marking %d,%d as flashed and incrementing flashes counter", x, y)
	og.flashed[x][y] = true
	og.flashes++

	// Increment adjacent grids
	adjacent := [][]int{
		{x + 1, y}, {x - 1, y},
		{x, y - 1}, {x, y + 1},
		{x + 1, y + 1}, {x + 1, y - 1},
		{x - 1, y + 1}, {x - 1, y - 1},
	}
	for _, adj := range adjacent {
		if og.inGrid(adj[0], adj[1]) {
			og.grid[adj[0]][adj[1]]++
			// Flash any adjacent grid > 9
			if og.grid[adj[0]][adj[1]] > 9 {
				og.flash(adj[0], adj[1])
			}
		}
	}
}

func (og *octopusGrid) inGrid(x, y int) bool {
	if x < 0 || x >= len(og.grid) || y < 0 || y >= len(og.grid[x]) {
		return false
	}
	return true
}

func (og *octopusGrid) resetFlashedStep() {
	for x := 0; x < len(og.grid); x++ {
		for y := 0; y < len(og.grid[x]); y++ {
			if og.flashed[x][y] {
				og.flashed[x][y] = false
				og.grid[x][y] = 0
			}
		}
	}
}
