package day8

import "testing"

func TestDay8Part1Example(t *testing.T) {
	expected := 26
	answer, err := day8part1("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay8Part1Test(t *testing.T) {
	expected := 261
	answer, err := day8part1("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay8Part2Example(t *testing.T) {
	expected := 61229
	answer, err := day8part2("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay8Part2Test(t *testing.T) {
	expected := 987553
	answer, err := day8part2("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
