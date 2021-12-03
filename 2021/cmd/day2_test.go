package main

import (
	"testing"

	"2021.advent-of-code.rileychase.net/internal/utils"
)

func TestDay2Part1Example(t *testing.T) {
	commands, err := utils.ReadCommandFile("../inputs/day2/example_input.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 150
	answer, err := day2Part1(commands)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay2Part1Test(t *testing.T) {
	commands, err := utils.ReadCommandFile("../inputs/day2/test_input.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 1693300
	answer, err := day2Part1(commands)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay2Part2Example(t *testing.T) {
	commands, err := utils.ReadCommandFile("../inputs/day2/example_input.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 900
	answer, err := day2Part2(commands)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay2Part2Test(t *testing.T) {
	commands, err := utils.ReadCommandFile("../inputs/day2/test_input.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 1857958050
	answer, err := day2Part2(commands)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
