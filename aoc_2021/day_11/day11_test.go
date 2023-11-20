package day11

import "testing"

func TestDay11Part1Example(t *testing.T) {
	expected := 1656
	answer, err := day11part1("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay11Part1Test(t *testing.T) {
	expected := 1785
	answer, err := day11part1("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay11Part2Example(t *testing.T) {
	expected := 195
	answer, err := day11part2("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay11Part2Test(t *testing.T) {
	expected := 354
	answer, err := day11part2("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
