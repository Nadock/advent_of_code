package day4

import (
	"fmt"
	"log"
	"strconv"
)

func day4part1(drawnNumbers []string, boards []*Board) (int, error) {
	// log.Printf("%v, %+v", drawnNumbers, boards)
	// log.Printf("")

	winNumber, winBoard, err := simulateWinFirstBingoGame(drawnNumbers, boards)
	if err != nil {
		return 0, err
	}
	log.Printf("winning number: %d, winning board: %+v", winNumber, winBoard)

	score, err := winBoard.Score()
	if err != nil {
		return 0, err
	}
	log.Printf("winning board score: %d", score)

	return score * winNumber, nil
}

func day4part2(drawnNumbers []string, boards []*Board) (int, error) {

	winNumber, winBoard, err := simulateWinLastBingoGame(drawnNumbers, boards)
	if err != nil {
		return 0, err
	}
	log.Printf("last winning number: %d, last winning board: %+v", winNumber, winBoard)

	score, err := winBoard.Score()
	if err != nil {
		return 0, err
	}
	log.Printf("last winning board score: %d", score)

	return score * winNumber, nil
}

func simulateWinFirstBingoGame(drawnNumbers []string, boards []*Board) (int, *Board, error) {
	for _, draw := range drawnNumbers {
		// log.Printf("draw %s", draw)
		for _, board := range boards {
			board.Draw(draw)
		}

		// log.Printf("check winners: %+v", boards)
		for _, board := range boards {
			if board.IsWinner() {
				winningDraw, err := strconv.Atoi(draw)
				return winningDraw, board, err
			}
		}
	}

	return 0, nil, fmt.Errorf("no winner after drawing all numbers")
}

func simulateWinLastBingoGame(drawnNumbers []string, boards []*Board) (int, *Board, error) {
	boardsHaveWon := make([]bool, len(boards))

	for _, draw := range drawnNumbers {
		// log.Printf("drawing %s", draw)
		for _, board := range boards {
			board.Draw(draw)
		}

		for idx, board := range boards {
			if !boardsHaveWon[idx] {
				if board.IsWinner() {
					// log.Printf("board %d has won", idx)

					winnersCount := 0
					for _, hasWon := range boardsHaveWon {
						if hasWon {
							winnersCount++
						}
					}

					if winnersCount == len(boardsHaveWon)-1 {
						// log.Printf("board %d is last to win", idx)
						winningDraw, err := strconv.Atoi(draw)
						return winningDraw, board, err
					}

					boardsHaveWon[idx] = true
				}
			}

		}
	}

	return 0, nil, fmt.Errorf("no last winner after drawing all numbers")
}
