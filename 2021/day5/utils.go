package day5

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

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
