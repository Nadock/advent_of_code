package day3

import (
	"testing"
)

func TestDay3Part1Example(t *testing.T) {
	lines, err := ReadBinaryDiagnosticFile("./example.txt")
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
	lines, err := ReadBinaryDiagnosticFile("./test.txt")
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

func TestDay3Part2Example(t *testing.T) {
	lines, err := ReadBinaryDiagnosticFile("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 230
	answer, err := day3part2(lines)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay3Part2Test(t *testing.T) {
	lines, err := ReadBinaryDiagnosticFile("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 6677951
	answer, err := day3part2(lines)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
