package main

import (
	"testing"

	"2021.advent-of-code.rileychase.net/internal/utils"
)

func TestDay5Part1Example(t *testing.T) {
	lines, err := utils.ReadHydrothermalVentsMapFile("../inputs/day5/example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 50
	answer, err := day5part1(lines)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay5Part1Test(t *testing.T) {
	lines, err := utils.ReadHydrothermalVentsMapFile("../inputs/day5/test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 4728
	answer, err := day5part1(lines)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
