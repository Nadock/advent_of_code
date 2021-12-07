package day7

import (
	"testing"

	"2021.advent-of-code.rileychase.net/internal"
)

func TestDay7Part1Example(t *testing.T) {
	positions, err := internal.ReadIntValues("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 37
	answer := day7part1(positions)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay7Part1Test(t *testing.T) {
	positions, err := internal.ReadIntValues("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 347449
	answer := day7part1(positions)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay7Part2Example(t *testing.T) {
	positions, err := internal.ReadIntValues("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 168
	answer := day7part2(positions)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay7Part2Test(t *testing.T) {
	positions, err := internal.ReadIntValues("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 98039527
	answer := day7part2(positions)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
