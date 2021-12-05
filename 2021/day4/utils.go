package day4

import (
	"io/ioutil"
	"strconv"
	"strings"
)

type Board struct {
	Grid      []string
	gridDraws []bool
}

func NewBoard(rows []string) *Board {
	var grid []string
	var gridDraws []bool
	for _, row := range rows {
		rowNumbers := strings.Split(row, " ")
		for _, num := range rowNumbers {
			trimedNum := strings.TrimSpace(num)
			if trimedNum != "" {
				grid = append(grid, trimedNum)
				gridDraws = append(gridDraws, false)
			}
		}
	}
	// log.Printf("creating new board with grid: %v", grid)
	return &Board{Grid: grid, gridDraws: gridDraws}
}

func (b *Board) Draw(d string) {
	for idx, value := range b.Grid {
		if value == d {
			b.gridDraws[idx] = true
		}
	}
}

func (b *Board) IsWinner() bool {
	// Check all rows
	for i := 0; i < len(b.gridDraws); i += 5 {
		rowComplete := true
		for _, gridDraw := range b.gridDraws[i : i+5] {
			rowComplete = rowComplete && gridDraw
		}

		if rowComplete {
			return true
		}
	}

	// Check all columns
	for i := 0; i < 5; i++ {
		colComplete := true
		for j := 0; j < 5; j++ {
			// log.Printf("checking col %d, row %d, index %d", i, j, i+(j*5))
			colComplete = colComplete && b.gridDraws[i+(j*5)]
		}

		if colComplete {
			return true
		}
	}

	return false
}

func (b *Board) Score() (int, error) {
	tally := 0
	for idx, value := range b.Grid {
		if !b.gridDraws[idx] {
			score, err := strconv.Atoi(value)
			if err != nil {
				return 0, err
			}

			tally += score
		}
	}
	return tally, nil
}

func ReadBingoGameFile(path string) ([]string, []*Board, error) {
	input, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, nil, err
	}

	lines := strings.Split(string(input), "\n")
	drawnNumbers := strings.Split(lines[0], ",")
	var boards []*Board

	// Start with i=1 to skip of drawn numbers on first line
	for i := 1; i < len(lines); i++ {
		if lines[i] == "" {
			continue
		}

		// log.Printf("reading lines %d to %d as a new Board", i, i+5)
		boards = append(boards, NewBoard(lines[i:i+5]))
		i += 5
	}

	return drawnNumbers, boards, nil
}
