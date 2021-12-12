package day8

import "testing"

func TestDay7Part1Example(t *testing.T) {
	expected := 26
	answer, err := day8part1("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay7Part1Test(t *testing.T) {
	expected := 261
	answer, err := day8part1("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay7Part2Example(t *testing.T) {
	expected := 26
	answer, err := day8part2("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay7Part2Test(t *testing.T) {
	expected := 262
	answer, err := day8part2("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
