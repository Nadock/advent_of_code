package day12

import "testing"

func TestDay12Part1Example1(t *testing.T) {
	expected := 1656
	answer, err := day12part1("./example1.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
