package day10

import (
	"log"
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
				log.Printf("expected %s, but found %s instead", e, c)
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
	v := (*s)[len(*s)-1]
	*s = (*s)[:len(*s)-1]
	return v
}
