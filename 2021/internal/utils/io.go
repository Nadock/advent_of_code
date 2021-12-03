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
