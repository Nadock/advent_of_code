package day6

import "testing"

func TestDay6Part1Example(t *testing.T) {
	lines, err := ReadLanternFishAgeFile("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 5934
	answer, err := day6part1(lines)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay6Part1Test(t *testing.T) {
	lines, err := ReadLanternFishAgeFile("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 372984
	answer, err := day6part1(lines)
	if err != nil {
		t.Fatal(err)
	}

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

// func TestDay6Part2Example(t *testing.T) {
// 	lines, err := ReadLanternFishAgeFile("./example.txt")
// 	if err != nil {
// 		t.Fatal(err)
// 	}

// 	expected := 12
// 	answer, err := day6part2(lines)
// 	if err != nil {
// 		t.Fatal(err)
// 	}

// 	if answer != expected {
// 		t.Errorf("expected answer of %d, got %d", expected, answer)
// 	}
// }

// func TestDay6Part2Test(t *testing.T) {
// 	lines, err := ReadLanternFishAgeFile("./test.txt")
// 	if err != nil {
// 		t.Fatal(err)
// 	}

// 	expected := 17717
// 	answer, err := day6part2(lines)
// 	if err != nil {
// 		t.Fatal(err)
// 	}

// 	if answer != expected {
// 		t.Errorf("expected answer of %d, got %d", expected, answer)
// 	}
// }
