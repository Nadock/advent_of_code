package utils

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type Command struct {
	Direction string
	Magnitude int
}

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

func ReadCommandFile(path string) ([]Command, error) {
	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	lines := strings.Split(string(input), "\n")
	var commands []Command

	for _, line := range lines {
		if line != "" {
			parts := strings.Split(line, " ")
			if len(parts) != 2 {
				return nil, fmt.Errorf("found bad command line: %s", line)
			}

			direction := parts[0]
			magnitude, err := strconv.Atoi(parts[1])
			if err != nil {
				return nil, err
			}

			commands = append(commands, Command{Direction: direction, Magnitude: magnitude})
		}
	}

	return commands, nil
}

func ReadBinaryDiagnosticFile(path string) ([]string, error) {
	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	return strings.Split(string(input), "\n"), nil
}

type Board struct {
	Grid      []string
	gridDraws []bool
}

func NewBoard(rows []string) *Board {
	var grid []string
	var gridDraws []bool
	for _, row := range rows {
		rowNumbers := strings.Split(row, " ")
		for _, num := range rowNumbers {
			trimedNum := strings.TrimSpace(num)
			if trimedNum != "" {
				grid = append(grid, trimedNum)
				gridDraws = append(gridDraws, false)
			}
		}
	}
	// log.Printf("creating new board with grid: %v", grid)
	return &Board{Grid: grid, gridDraws: gridDraws}
}

func (b *Board) Draw(d string) {
	for idx, value := range b.Grid {
		if value == d {
			b.gridDraws[idx] = true
		}
	}
}

func (b *Board) IsWinner() bool {
	// Check all rows
	for i := 0; i < len(b.gridDraws); i += 5 {
		rowComplete := true
		for _, gridDraw := range b.gridDraws[i : i+5] {
			rowComplete = rowComplete && gridDraw
		}

		if rowComplete {
			return true
		}
	}

	// Check all columns
	for i := 0; i < 5; i++ {
		colComplete := true
		for j := 0; j < 5; j++ {
			// log.Printf("checking col %d, row %d, index %d", i, j, i+(j*5))
			colComplete = colComplete && b.gridDraws[i+(j*5)]
		}

		if colComplete {
			return true
		}
	}

	return false
}

func (b *Board) Score() (int, error) {
	tally := 0
	for idx, value := range b.Grid {
		if !b.gridDraws[idx] {
			score, err := strconv.Atoi(value)
			if err != nil {
				return 0, err
			}

			tally += score
		}
	}
	return tally, nil
}

func ReadBingoGameFile(path string) ([]string, []*Board, error) {
	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, nil, err
	}

	lines := strings.Split(string(input), "\n")
	drawnNumbers := strings.Split(lines[0], ",")
	var boards []*Board

	// Start with i=1 to skip of drawn numbers on first line
	for i := 1; i < len(lines); i++ {
		if lines[i] == "" {
			continue
		}

		// log.Printf("reading lines %d to %d as a new Board", i, i+5)
		boards = append(boards, NewBoard(lines[i:i+5]))
		i += 5
	}

	return drawnNumbers, boards, nil
}

type Point struct {
	X int
	Y int
}

func NewPointFromCoordString(coord string) (*Point, error) {
	values := strings.Split(coord, ",")
	if len(values) != 2 {
		return nil, fmt.Errorf("coord string must be two comma seperated numbers")
	}

	x, err := strconv.Atoi(values[0])
	if err != nil {
		return nil, err
	}
	y, err := strconv.Atoi(values[1])
	if err != nil {
		return nil, err
	}

	return &Point{X: x, Y: y}, nil
}

type Line struct {
	Start *Point
	End   *Point
}

func NewLineFromCoordStrings(coord1, coord2 string) (*Line, error) {
	p1, err := NewPointFromCoordString(coord1)
	if err != nil {
		return nil, err
	}

	p2, err := NewPointFromCoordString(coord2)
	if err != nil {
		return nil, err
	}

	if p1.X != p2.X {
		if p1.X < p2.X {
			return &Line{Start: p1, End: p2}, nil
		} else {
			return &Line{Start: p2, End: p1}, nil
		}
	} else {
		if p1.Y < p2.Y {
			return &Line{Start: p1, End: p2}, nil
		} else {
			return &Line{Start: p2, End: p1}, nil
		}
	}

	// return &Line{Start: p1, End: p2}, nil
}

func ReadHydrothermalVentsMapFile(path string) ([]*Line, error) {
	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var lines []*Line

	fileLines := strings.Split(string(input), "\n")
	for _, fileLine := range fileLines {
		if fileLine == "" {
			continue
		}

		coords := strings.Split(fileLine, " -> ")
		if len(coords) != 2 {
			return nil, fmt.Errorf("input line must match format 'x1,y1 -> x2,y2'")
		}

		line, err := NewLineFromCoordStrings(coords[0], coords[1])
		if err != nil {
			return nil, err
		}
		lines = append(lines, line)
	}

	return lines, nil
}
