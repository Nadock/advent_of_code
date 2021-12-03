package main

import (
	"testing"

	"2021.advent-of-code.rileychase.net/internal/utils"
)

func TestDay1Part1Example(t *testing.T) {
	depths, err := utils.ReadDepthFile("../inputs/day1/example_input.txt")
	if err != nil {
		t.Fatal(err)
	}

	answer, err := day1Part1(depths)
	if err != nil {
		t.Fatal(err)
	}

	if answer != 7 {
		t.Errorf("wanted answer 7, got %d", answer)
	}
}

func TestDay1Part1Test(t *testing.T) {
	depths, err := utils.ReadDepthFile("../inputs/day1/test_input.txt")
	if err != nil {
		t.Fatal(err)
	}

	answer, err := day1Part1(depths)
	if err != nil {
		t.Fatal(err)
	}

	if answer != 1393 {
		t.Errorf("wanted answer 1393, got %d", answer)
	}
}

func TestDay1Part2Example(t *testing.T) {
	depths, err := utils.ReadDepthFile("../inputs/day1/example_input.txt")
	if err != nil {
		t.Fatal(err)
	}

	answer, err := day1Part2(depths)
	if err != nil {
		t.Fatal(err)
	}

	if answer != 5 {
		t.Errorf("wanted answer 5, got %d", answer)
	}
}

func TestDay1Part2Test(t *testing.T) {
	depths, err := utils.ReadDepthFile("../inputs/day1/test_input.txt")
	if err != nil {
		t.Fatal(err)
	}

	answer, err := day1Part2(depths)
	if err != nil {
		t.Fatal(err)
	}

	if answer != 1359 {
		t.Errorf("wanted answer 1359, got %d", answer)
	}
}
