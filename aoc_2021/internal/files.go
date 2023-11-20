package internal

import (
	"io/ioutil"
	"strconv"
	"strings"
)

// Read a text file and split it by some delimeter
func ReadInput(path, delimeter string) ([]string, error) {
	f, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}
	return strings.Split(strings.TrimSpace(string(f)), delimeter), nil
}

// Read a text file as a collection of lines
func ReadLines(path string) ([]string, error) {
	return ReadInput(path, "\n")
}

// Read a list set of comma separated string values.
func ReadStringValues(path string) ([]string, error) {
	return ReadInput(path, ",")
}

// Read a list set of comma separated integer values.
func ReadIntValues(path string) ([]int, error) {
	s, err := ReadStringValues(path)
	if err != nil {
		return nil, err
	}
	return StringsToInts(s)
}

// Convert a list of strings to a list of integers
func StringsToInts(strings []string) ([]int, error) {
	var ints []int
	for _, s := range strings {
		i, err := strconv.Atoi(s)
		if err != nil {
			return nil, err
		}
		ints = append(ints, i)
	}
	return ints, nil
}
