package main

import (
	"log"
	"strconv"
	"strings"
)

func day3part1(lines []string) (int, error) {

	var column_counts []map[string]int
	for i := 0; i < len(strings.Split(lines[0], "")); i++ {
		new_col_count := make(map[string]int)
		new_col_count["0"] = 0
		new_col_count["1"] = 0

		column_counts = append(column_counts, new_col_count)
	}

	for _, line := range lines {
		columns := strings.Split(line, "")
		for idx, column := range columns {
			column_counts[idx][column] += 1
		}
	}

	log.Printf("%+v", column_counts)

	gRate, err := gammaRate(column_counts)
	if err != nil {
		return 0, err
	}
	log.Printf("%d", gRate)

	eRate, err := epsilonRate(column_counts)
	if err != nil {
		return 0, err
	}
	log.Printf("%d", eRate)

	return gRate * eRate, nil
}

func gammaRate(column_counts []map[string]int) (int, error) {
	var parts []string

	for _, counts := range column_counts {
		if counts["0"] > counts["1"] {
			parts = append(parts, "0")
		} else {
			parts = append(parts, "1")
		}
	}

	gRate, err := strconv.ParseInt(strings.Join(parts, ""), 2, 64)
	if err != nil {
		return 0, err
	}
	return int(gRate), nil
}

func epsilonRate(column_counts []map[string]int) (int, error) {
	var parts []string

	for _, counts := range column_counts {
		if counts["0"] > counts["1"] {
			parts = append(parts, "1")
		} else {
			parts = append(parts, "0")
		}
	}

	gRate, err := strconv.ParseInt(strings.Join(parts, ""), 2, 64)
	if err != nil {
		return 0, err
	}
	return int(gRate), nil
}
