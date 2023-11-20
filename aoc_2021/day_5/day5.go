package day5

import (
	"log"
	"math"
)

func day5part1(lines []*Line) (int, error) {
	x, y := findGridSize(lines)
	grid := NewGrid(x, y)

	for _, line := range lines {
		grid.PlotLinePart1(line)
	}

	return grid.countGridIntersections(), nil
}

func day5part2(lines []*Line) (int, error) {
	x, y := findGridSize(lines)
	grid := NewGrid(x, y)

	for _, line := range lines {
		grid.PlotLinePart2(line)
	}

	return grid.countGridIntersections(), nil
}

func findGridSize(lines []*Line) (int, int) {
	xMax := 0
	yMax := 0
	for _, line := range lines {
		xMax = int(math.Max(float64(xMax), float64(line.Start.X)))
		yMax = int(math.Max(float64(yMax), float64(line.Start.Y)))

		xMax = int(math.Max(float64(xMax), float64(line.End.X)))
		yMax = int(math.Max(float64(yMax), float64(line.End.Y)))
	}

	return xMax, yMax
}

func (g *Grid) countGridIntersections() int {
	count := 0
	for x, row := range g.Points {
		for y, p := range row {
			if p >= 2 {
				log.Printf("point %d,%d has count %d", x, y, p)
				count++
			}
		}
	}
	return count
}

type Grid struct {
	Points [][]int
	Size   int
}

func NewGrid(x, y int) *Grid {
	g := &Grid{Size: x}
	for i := 0; i <= x; i++ {
		g.Points = append(g.Points, make([]int, y+1))
	}
	return g
}

func (g *Grid) Mark(x, y int) {
	log.Printf("marking %d,%d", x, y)
	g.Points[x][y]++
}

func (g *Grid) PlotLinePart1(line *Line) {
	// Ignore diagonal lines
	if line.Start.X != line.End.X && line.Start.Y != line.End.Y {
		return
	}

	// Determine if line is horizontal (x varying), or vertical (y varying)
	isHorizontal := false
	if line.Start.X != line.End.X {
		isHorizontal = true
	}

	log.Printf("marking line from %d,%d to %d,%d", line.Start.X, line.Start.Y, line.End.X, line.End.Y)
	if isHorizontal {
		for i := line.Start.X; i <= line.End.X; i++ {
			g.Mark(i, line.Start.Y)
		}
	} else {
		for i := line.Start.Y; i <= line.End.Y; i++ {
			g.Mark(line.Start.X, i)
		}
	}
}

func (g *Grid) PlotLinePart2(line *Line) {

	log.Printf("plotting line from %d,%d to %d,%d", line.Start.X, line.Start.Y, line.End.X, line.End.Y)
	if line.Start.X == line.End.X && line.Start.Y != line.End.Y {
		// Vertical (varying Y)
		for i := line.Start.Y; i <= line.End.Y; i++ {
			g.Mark(line.Start.X, i)
		}
	} else if line.Start.X != line.End.X && line.Start.Y == line.End.Y {
		// Horizontal (varying X)
		for i := line.Start.X; i <= line.End.X; i++ {
			g.Mark(i, line.Start.Y)
		}
	} else {
		// Diagonal (varying X & Y)
		xMod := 1
		if line.Start.X > line.End.X {
			xMod = -1
		}
		yMod := 1
		if line.Start.Y > line.End.Y {
			yMod = -1
		}

		log.Printf("Diagonal line -> xMod=%d, yMod=%d", xMod, yMod)

		x := line.Start.X
		y := line.Start.Y
		for {
			g.Mark(x, y)
			if x == line.End.X && y == line.End.Y {
				break
			}
			x += xMod
			y += yMod
		}

		log.Printf("")
	}

}
