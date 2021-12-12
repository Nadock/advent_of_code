package day10

import "testing"

func TestDay10Part1Example(t *testing.T) {
	expected := 26397
	answer, err := day10part1("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay10Part1Test(t *testing.T) {
	expected := 316851
	answer, err := day10part1("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay10Part2Example(t *testing.T) {
	expected := 288957
	answer, err := day10part2("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay10Part2Test(t *testing.T) {
	expected := 2182912364
	answer, err := day10part2("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
