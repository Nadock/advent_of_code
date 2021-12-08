package day8

import (
	"fmt"
	"strings"

	"2021.advent-of-code.rileychase.net/internal"
)

func day8part1(path string) (int, error) {
	lines, err := internal.ReadLines(path)
	if err != nil {
		return 0, err
	}

	var records []*recordEntry
	for _, line := range lines {
		record, err := recordEntryFromLine(line)
		if err != nil {
			return 0, err
		}
		records = append(records, record)
	}

	count := 0
	for _, record := range records {
		for _, value := range record.values {
			if len(value) == 2 || len(value) == 3 || len(value) == 4 || len(value) == 7 {
				count++
			}
		}
	}

	return count, nil
}

type recordEntry struct {
	samples []string
	values  []string
}

func recordEntryFromLine(line string) (*recordEntry, error) {
	lineSplit := strings.Split(line, " | ")
	if len(lineSplit) != 2 {
		return nil, fmt.Errorf("invalid input line: %s", line)
	}

	samples := strings.Split(lineSplit[0], " ")
	values := strings.Split(lineSplit[1], " ")
	return &recordEntry{samples: samples, values: values}, nil
}
