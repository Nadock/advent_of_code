package day4

import (
	"testing"
)

func TestDay4Part1Example(t *testing.T) {
	drawnNumbers, boards, err := ReadBingoGameFile("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 4512
	answer, err := day4part1(drawnNumbers, boards)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay4Part1Test(t *testing.T) {
	drawnNumbers, boards, err := ReadBingoGameFile("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 39984
	answer, err := day4part1(drawnNumbers, boards)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay4Part2Example(t *testing.T) {
	drawnNumbers, boards, err := ReadBingoGameFile("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 1924
	answer, err := day4part2(drawnNumbers, boards)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay4Part2Test(t *testing.T) {
	drawnNumbers, boards, err := ReadBingoGameFile("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 8468
	answer, err := day4part2(drawnNumbers, boards)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
