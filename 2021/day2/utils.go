package day2

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
