package day7

import (
	"testing"
)

func TestDay7Part1Example(t *testing.T) {
	positions, err := ReadCrabPositionsFile("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 37
	answer := day7part1(positions)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay7Part1Test(t *testing.T) {
	positions, err := ReadCrabPositionsFile("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 347449
	answer := day7part1(positions)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

// func TestDay7Part2Example(t *testing.T) {
// 	positions, err := ReadCrabPositionsFile("./example.txt")
// 	if err != nil {
// 		t.Fatal(err)
// 	}

// 	expected := 12
// 	answer, err := day7part2(positions)
// 	if err != nil {
// 		t.Fatal(err)
// 	}

// 	if answer != expected {
// 		t.Errorf("expected answer of %d, got %d", expected, answer)
// 	}
// }

// func TestDay7Part2Test(t *testing.T) {
// 	positions, err := ReadCrabPositionsFile("./test.txt")
// 	if err != nil {
// 		t.Fatal(err)
// 	}

// 	expected := 17717
// 	answer, err := day7part2(positions)
// 	if err != nil {
// 		t.Fatal(err)
// 	}

// 	if answer != expected {
// 		t.Errorf("expected answer of %d, got %d", expected, answer)
// 	}
// }
