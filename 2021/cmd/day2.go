package main

import (
	"fmt"

	"2021.advent-of-code.rileychase.net/internal/utils"
)

type submarine struct {
	horizontal int
	depth      int
}

func (s *submarine) Forward(x int) {
	s.horizontal += x
}

func (s *submarine) Down(x int) {
	// Go down -> increase depth
	s.depth += x
}

func (s *submarine) Up(x int) {
	s.depth -= x
}

func day2Part1(commands []utils.Command) (int, error) {
	var sub submarine

	for _, command := range commands {
		switch command.Direction {
		case "forward":
			sub.Forward(command.Magnitude)
		case "down":
			sub.Down(command.Magnitude)
		case "up":
			sub.Up(command.Magnitude)
		default:
			return 0, fmt.Errorf("unknown submarine command %+v", command)
		}
	}

	return sub.depth * sub.horizontal, nil
}
