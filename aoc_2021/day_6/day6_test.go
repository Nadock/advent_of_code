package day6

import (
	"testing"

	"2021.advent-of-code.rileychase.net/internal"
)

func TestDay6Part1Example(t *testing.T) {
	ages, err := internal.ReadIntValues("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 5934
	answer := day6part1(ages)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay6Part1Test(t *testing.T) {
	ages, err := internal.ReadIntValues("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 372984
	answer := day6part1(ages)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay6Part2Example(t *testing.T) {
	ages, err := internal.ReadIntValues("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 26984457539
	answer := day6part2(ages)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay6Part2Test(t *testing.T) {
	ages, err := internal.ReadIntValues("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 1681503251694
	answer := day6part2(ages)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
