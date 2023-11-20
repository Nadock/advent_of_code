package day9

import "testing"

func TestDay9Part1Example(t *testing.T) {
	expected := 15
	answer, err := day9part1("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay9Part1Test(t *testing.T) {
	expected := 512
	answer, err := day9part1("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay9Part2Example(t *testing.T) {
	expected := 1134
	answer, err := day9part2("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay9Part2Test(t *testing.T) {
	expected := 1600104
	answer, err := day9part2("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
