package day3

import (
	"io/ioutil"
	"strings"
)

func ReadBinaryDiagnosticFile(path string) ([]string, error) {
	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	return strings.Split(string(input), "\n"), nil
}
