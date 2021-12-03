package main

import (
	"flag"
	"fmt"
	"log"

	"2021.advent-of-code.rileychase.net/internal/utils"
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
		depths, err := utils.ReadDepthFile(input_path)
		if err != nil {
			return 0, err
		}

		if part == 1 {
			return day1Part1(depths)
		}
		if part == 2 {
			return day1Part2(depths)
		}
	} else if day == 2 {
		commands, err := utils.ReadCommandFile(input_path)
		if err != nil {
			return 0, err
		}

		if part == 1 {
			return day2Part1(commands)
		}
	}

	return 0, fmt.Errorf("could not find challenge day %d, part %d to run", day, part)
}
