package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

func day3part1(lines []string) (int, error) {

	colCounts := countColumns(lines)
	mCommon := mostCommon(colCounts)
	lCommon := leastCommon(colCounts)

	log.Printf("%+v", colCounts)

	gRate, err := gammaRate(mCommon)
	if err != nil {
		return 0, err
	}
	log.Printf("gammaRate: %d", gRate)

	eRate, err := epsilonRate(lCommon)
	if err != nil {
		return 0, err
	}
	log.Printf("epsilonRate: %d", eRate)

	return gRate * eRate, nil
}

func day3part2(lines []string) (int, error) {
	oxyRate, err := oxygenRating(lines)
	if err != nil {
		return 0, err
	}
	log.Printf("oxygenRate: %d", oxyRate)

	c02Rate, err := c02Rating(lines)
	if err != nil {
		return 0, err
	}
	log.Printf("oxygenRate: %d", c02Rate)

	return oxyRate * c02Rate, nil
}

// Count the 0s and 1s in each column, the output a 2 element array for each column where the first element is the count
// of 0s for that column and the second element is the count of 1s for that column
func countColumns(lines []string) [][]int {
	var colCounts [][]int

	// Create 1 sub-array for each column
	for i := 0; i < len(strings.Split(lines[0], "")); i++ {
		col := make([]int, 2)
		colCounts = append(colCounts, col)
	}

	// For each line, add each columns 0 or 1 to the corresponding count
	for _, line := range lines {
		columns := strings.Split(line, "")
		for idx, col := range columns {
			switch col {
			case "0":
				colCounts[idx][0] += 1
			case "1":
				colCounts[idx][1] += 1
			}
		}
	}

	return colCounts
}

// For each counted column, output the most common value in that column
func mostCommon(colCounts [][]int) []int {
	var mostCommon []int
	for _, columnCount := range colCounts {
		if columnCount[0] > columnCount[1] {
			mostCommon = append(mostCommon, 0)
		} else {
			mostCommon = append(mostCommon, 1)
		}
	}
	return mostCommon
}

// For each counted column, output the least common value in that column
func leastCommon(colCounts [][]int) []int {
	var leastCommon []int
	for _, columnCount := range colCounts {
		if columnCount[0] > columnCount[1] {
			leastCommon = append(leastCommon, 1)
		} else {
			leastCommon = append(leastCommon, 0)
		}
	}
	return leastCommon
}

func gammaRate(mostCommon []int) (int, error) {
	var mostCommonString string
	for _, v := range mostCommon {
		mostCommonString = fmt.Sprintf("%s%d", mostCommonString, v)
	}

	gRate, err := strconv.ParseInt(mostCommonString, 2, 64)
	if err != nil {
		return 0, err
	}
	return int(gRate), nil
}

func epsilonRate(leastCommon []int) (int, error) {
	var leastCommonString string
	for _, v := range leastCommon {
		leastCommonString = fmt.Sprintf("%s%d", leastCommonString, v)
	}

	gRate, err := strconv.ParseInt(leastCommonString, 2, 64)
	if err != nil {
		return 0, err
	}
	return int(gRate), nil
}

func oxygenRating(lines []string) (int, error) {

	retainedLines := lines
	colCount := countColumns(retainedLines)
	mCommon := mostCommon(colCount)

	for i := 0; i < len(mCommon) && len(retainedLines) > 1; i++ {
		common := mCommon[i]

		retainedLines = filterLines(retainedLines, i, common)
		log.Printf("after column %d, retaining %d, remaining lines are %+v", i, common, retainedLines)

		colCount = countColumns(retainedLines)
		mCommon = mostCommon(colCount)
		log.Printf("next loop: colCount: %+v, mCommon: %+v", colCount, mCommon)
		log.Println("")
	}

	oxyRate, err := strconv.ParseInt(retainedLines[0], 2, 64)
	if err != nil {
		return 0, err
	}

	return int(oxyRate), nil
}

func c02Rating(lines []string) (int, error) {
	retainedLines := lines
	colCount := countColumns(retainedLines)
	lCommon := leastCommon(colCount)

	for i := 0; i < len(lCommon) && len(retainedLines) > 1; i++ {
		common := lCommon[i]

		retainedLines = filterLines(retainedLines, i, common)
		log.Printf("after column %d, retaining %d, remaining lines are %+v", i, common, retainedLines)

		colCount = countColumns(retainedLines)
		lCommon = leastCommon(colCount)
		log.Printf("next loop: colCount: %+v, lCommon: %+v", colCount, lCommon)
		log.Println("")
	}

	c02Rate, err := strconv.ParseInt(retainedLines[0], 2, 64)
	if err != nil {
		return 0, err
	}

	return int(c02Rate), nil
}

// For each line, check the bit in the specified column and filter it out if it does not match
func filterLines(lines []string, column, bit int) []string {
	bitString := fmt.Sprintf("%d", bit)

	var matchingLines []string
	for _, line := range lines {
		if line != "" {
			if string(line[column]) == bitString {
				matchingLines = append(matchingLines, line)
			}
		}
	}

	return matchingLines
}
