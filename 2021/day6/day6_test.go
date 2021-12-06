package day6

import "testing"

func TestDay6Part1Example(t *testing.T) {
	ages, err := ReadLanternFishAgeFile("./example.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 5934
	answer := day6part1(ages)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}

func TestDay6Part1Test(t *testing.T) {
	ages, err := ReadLanternFishAgeFile("./test.txt")
	if err != nil {
		t.Fatal(err)
	}

	expected := 372984
	answer := day6part1(ages)

	if answer != expected {
		t.Errorf("expected answer of %d, got %d", expected, answer)
	}
}
