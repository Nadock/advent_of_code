package main

import "testing"

func TestDay1(t *testing.T) {
	answer, err := day1Part1("../inputs/day1/part1/test_input.txt")
	if err != nil {
		t.Fatal(err)
	}

	if answer != 1393 {
		t.Errorf("wanted answer 1393, got %d", answer)
	}
}
