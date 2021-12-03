package main

import (
	"fmt"
	"log"

	"2021.advent-of-code.rileychase.net/internal/utils"
)

type submarine struct {
	horizontal int
	depth      int
	aim        int
	aimEnabled bool
}

func (s *submarine) Forward(x int) {
	if s.aimEnabled {
		s.depth += s.aim * x
	}
	s.horizontal += x
}

func (s *submarine) Down(x int) {
	if s.aimEnabled {
		s.aim += x
	} else {
		s.depth += x
	}
}

func (s *submarine) Up(x int) {
	if s.aimEnabled {
		s.aim -= x
	} else {
		s.depth -= x
	}
}

func day2Part1(commands []utils.Command) (int, error) {
	sub := submarine{aimEnabled: false}

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

func day2Part2(commands []utils.Command) (int, error) {
	sub := submarine{aimEnabled: true}

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
		log.Printf("%+v -> %+v", command, sub)
	}

	return sub.depth * sub.horizontal, nil
}
