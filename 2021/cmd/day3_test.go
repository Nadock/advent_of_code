package main

import (
	"testing"

	"2021.advent-of-code.rileychase.net/internal/utils"
)

func TestDay3Part1Example(t *testing.T) {
	lines, err := utils.ReadBinaryDiagnosticFile("../inputs/day3/example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 198
	answer, err := day3part1(lines)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay3Part1Test(t *testing.T) {
	lines, err := utils.ReadBinaryDiagnosticFile("../inputs/day3/test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 2743844
	answer, err := day3part1(lines)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
