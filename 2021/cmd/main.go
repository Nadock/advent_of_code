package main

import (
	"flag"
	"fmt"
	"log"
)

type config struct {
	day        int
	part       int
	input_path string
}

func main() {
	var cfg config

	flag.IntVar(&cfg.day, "day", 0, "The day of the challenge to run")
	flag.IntVar(&cfg.part, "part", 0, "The part of the day's challenge to run")
	flag.StringVar(&cfg.input_path, "input-path", "", "The path to the input file for the day and part being run")

	flag.Parse()

	if cfg.day == 0 {
		log.Fatal("The challenge day must be specified")
	}
	if cfg.part == 0 {
		log.Fatal("The challenge part must be specified")
	}
	if cfg.input_path == "" {
		log.Fatal("The challenge input-path must be specified")
	}

	answer, err := runChallenge(cfg.day, cfg.part, cfg.input_path)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("The answer is %d\n", answer)
}

func runChallenge(day, part int, input_path string) (int, error) {
	if day == 1 {
		if part == 1 {
			return day1Part1(input_path)
		}
	}

	return 0, fmt.Errorf("could not find challenge day %d, part %d to run", day, part)
}
