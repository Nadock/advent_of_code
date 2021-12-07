package day6

func day6part1(ages []int) int {
	fc := newFishCounter()
	return fc.countForDays(ages, 80)
}

func day6part2(ages []int) int {
	fc := newFishCounter()
	return fc.countForDays(ages, 256)
}

type fishCounter struct {
	cache map[int]int
}

func newFishCounter() *fishCounter {
	return &fishCounter{cache: make(map[int]int)}
}

func (fc *fishCounter) countForDays(ages []int, day int) int {
	total := 0
	for _, fish := range ages {
		total += fc.countFish(day - 1 - fish)
	}
	return total
}

func (fc *fishCounter) countFish(life int) int {
	if life < 0 {
		return 1
	}
	if value, found := fc.cache[life]; found {
		return value
	}
	result := fc.countFish(life-7) + fc.countFish(life-9)
	fc.cache[life] = result
	return result
}
