package main

import (
	"fmt"
	"log"
	"strconv"

	"2021.advent-of-code.rileychase.net/internal/utils"
)

func day4part1(drawnNumbers []string, boards []*utils.Board) (int, error) {
	// log.Printf("%v, %+v", drawnNumbers, boards)
	// log.Printf("")

	winNumber, winBoard, err := simulateBingoGame(drawnNumbers, boards)
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

func simulateBingoGame(drawnNumbers []string, boards []*utils.Board) (int, *utils.Board, error) {
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
