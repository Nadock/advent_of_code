package day10

import (
	"log"
	"sort"
	"strings"

	"2021.advent-of-code.rileychase.net/internal"
)

func day10part1(path string) (int, error) {
	lines, err := internal.ReadLines(path)
	if err != nil {
		return 0, err
	}

	sum := 0
	for _, line := range lines {
		invalidChar := findErrors(line)
		// log.Printf("line %s invalid, found %s", line, invalidChar)

		if invalidChar != "" {
			switch invalidChar {
			case ")":
				sum += 3
				log.Printf("invalid char %s, incrementing sum by %d to %d", invalidChar, 3, sum)
			case "]":
				sum += 57
				log.Printf("invalid char %s, incrementing sum by %d to %d", invalidChar, 57, sum)
			case "}":
				sum += 1197
				log.Printf("invalid char %s, incrementing sum by %d to %d", invalidChar, 1197, sum)
			case ">":
				sum += 25137
				log.Printf("invalid char %s, incrementing sum by %d to %d", invalidChar, 25137, sum)
			}
		}
	}

	return sum, nil
}

func findErrors(line string) string {
	var s stack
	for _, c := range strings.Split(line, "") {
		if c == "(" || c == "[" || c == "{" || c == "<" {
			s.Push(c)
		} else {
			v := s.Pop()
			e := ""

			switch v {
			case "(":
				e = ")"
			case "[":
				e = "]"
			case "{":
				e = "}"
			case "<":
				e = ">"
			}

			if c != e {
				return c
			}
		}
	}
	return ""
}

type stack []string

func (s *stack) Push(v string) {
	*s = append(*s, v)
}

func (s *stack) Pop() string {
	if s.Empty() {
		return ""
	}
	v := (*s)[len(*s)-1]
	*s = (*s)[:len(*s)-1]
	return v
}

func (s *stack) Empty() bool {
	return len(*s) == 0
}

func day10part2(path string) (int, error) {
	lines, err := internal.ReadLines(path)
	if err != nil {
		return 0, err
	}

	var scores []int
	for _, line := range lines {
		if i := findErrors(line); i == "" {
			fixes := repairLine(line)
			score := 0
			for _, c := range fixes {
				score *= 5
				switch c {
				case ")":
					score += 1
				case "]":
					score += 2
				case "}":
					score += 3
				case ">":
					score += 4
				}
			}
			log.Printf("fix line=%s by adding %s — score %d", line, strings.Join(fixes, ""), score)
			scores = append(scores, score)
		}
	}

	sort.Ints(scores)
	log.Printf("scores: %v, mid: %d, val: %d", scores, (len(scores) / 2), scores[(len(scores)/2)])

	return scores[(len(scores) / 2)], nil
}

func repairLine(line string) []string {
	var s stack
	for _, c := range strings.Split(line, "") {
		if c == "(" || c == "[" || c == "{" || c == "<" {
			s.Push(c)
		} else {
			s.Pop()
		}
	}

	var repair []string
	for !s.Empty() {
		next := s.Pop()
		switch next {
		case "(":
			repair = append(repair, ")")
		case "[":
			repair = append(repair, "]")
		case "{":
			repair = append(repair, "}")
		case "<":
			repair = append(repair, ">")
		}
	}

	return repair
}
