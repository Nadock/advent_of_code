package day8

import (
	"fmt"
	"log"
	"math"
	"strings"

	"2021.advent-of-code.rileychase.net/internal"
)

func day8part1(path string) (int, error) {
	lines, err := internal.ReadLines(path)
	if err != nil {
		return 0, err
	}

	var records []*recordEntry
	for _, line := range lines {
		record, err := recordEntryFromLine(line)
		if err != nil {
			return 0, err
		}
		records = append(records, record)
	}

	count := 0
	for _, record := range records {
		for _, value := range record.values {
			if len(value) == 2 || len(value) == 3 || len(value) == 4 || len(value) == 7 {
				count++
			}
		}
	}

	return count, nil
}

type recordEntry struct {
	samples []string
	values  []string
}

func recordEntryFromLine(line string) (*recordEntry, error) {
	lineSplit := strings.Split(line, " | ")
	if len(lineSplit) != 2 {
		return nil, fmt.Errorf("invalid input line: %s", line)
	}

	samples := strings.Split(lineSplit[0], " ")
	values := strings.Split(lineSplit[1], " ")
	return &recordEntry{samples: samples, values: values}, nil
}

func day8part2(path string) (int, error) {
	lines, err := internal.ReadLines(path)
	if err != nil {
		return 0, err
	}

	sum := 0
	for _, line := range lines {
		o := newObservation(line)
		// break
		log.Printf("%s => %d", strings.Split(line, "|")[1], o.outputValue())
		sum += o.outputValue()
	}

	return sum, nil
}

type observation struct {
	uniqueSignals []*displaySignal
	outputSignals []*displaySignal
}

func newObservation(line string) *observation {
	lineSplit := strings.Split(line, " | ")
	var uniqueSignals []*displaySignal
	var outputSignals []*displaySignal

	for _, sig := range strings.Split(lineSplit[0], " ") {
		uniqueSignals = append(uniqueSignals, newDisplaySignal(sig))
	}
	for _, sig := range strings.Split(lineSplit[1], " ") {
		outputSignals = append(outputSignals, newDisplaySignal(sig))
	}

	o := &observation{uniqueSignals: uniqueSignals, outputSignals: outputSignals}
	o.determineDigits()
	return o
}

func (o *observation) determineDigits() {
	// Find 1, 4, 7, and 8 first as they have unique lengths of 2, 4, 3, and 8
	var one, four, seven, eight *displaySignal
	for _, signal := range o.uniqueSignals {
		switch countActiveSignals(signal.signal) {
		// Number 1 has two active signals
		case 2:
			// log.Printf("signal '%s' => %.7b is number 1", signal.source, signal.signal)
			signal.digit = 1
			one = signal
		// Number 4 has four active signals
		case 4:
			// log.Printf("signal '%s' => %.7b is number 4", signal.source, signal.signal)
			signal.digit = 4
			four = signal
		// Number 7 has three active signals
		case 3:
			// log.Printf("signal '%s' => %.7b is number 7", signal.source, signal.signal)
			signal.digit = 7
			seven = signal
		// Number 8 has eight active signals
		case 7:
			// log.Printf("signal '%s' => %.7b is number 8", signal.source, signal.signal)
			signal.digit = 8
			eight = signal
		}
	}

	for _, signal := range o.uniqueSignals {
		if len(signal.source) == 6 {
			// Numbers 0, 6, and 9 all have len=6

			if countActiveSignals(signal.signal^four.signal) == 2 {
				// log.Printf("signal '%s' => %.7b is number 9", signal.source, signal.signal)
				signal.digit = 9
			} else if countActiveSignals(signal.signal&(eight.signal^one.signal)) == 5 {
				// log.Printf("signal '%s' => %.7b is number 6", signal.source, signal.signal)
				signal.digit = 6
			} else if countActiveSignals(signal.signal&(eight.signal^one.signal)) == 4 {
				// log.Printf("signal '%s' => %.7b is number 0", signal.source, signal.signal)
				signal.digit = 0
			}
		} else if len(signal.source) == 5 {
			// Numbers 2, 3, and all have len=5

			if countActiveSignals(signal.signal^seven.signal) == 2 {
				// log.Printf("signal '%s' => %.7b is number 3", signal.source, signal.signal)
				signal.digit = 3
			} else if countActiveSignals(signal.signal&(eight.signal^four.signal)) == 2 {
				// log.Printf("signal '%s' => %.7b is number 5", signal.source, signal.signal)
				signal.digit = 5
			} else if countActiveSignals(signal.signal&(eight.signal^four.signal)) == 3 {
				// log.Printf("signal '%s' => %.7b is number 2", signal.source, signal.signal)
				signal.digit = 2
			}
		}
	}

	// We now know which digit each unique observation corresponds to, so to find the digits for each output we find the unique observation that matches
	for _, outSignal := range o.outputSignals {
		for _, uniqueSignal := range o.uniqueSignals {
			if outSignal.signal == uniqueSignal.signal {
				// log.Printf("output signal '%s' (%.7b) matches unique signal '%s' (%.7b) which has digit %d", outSignal.source, outSignal.signal, uniqueSignal.source, uniqueSignal.signal, uniqueSignal.digit)
				outSignal.digit = uniqueSignal.digit
				break
			}
		}
	}
}

func (o *observation) outputValue() int {
	value := 0
	for i, signal := range o.outputSignals {
		value += signal.digit * int(math.Pow(10, float64(len(o.outputSignals)-1-i)))
	}
	return value
}

func countActiveSignals(signal int) int {
	return strings.Count(fmt.Sprintf("%.7b", signal), "1")
}

type displaySignal struct {
	source string
	signal int
	digit  int
}

var (
	a = 0b00000001
	b = 0b00000010
	c = 0b00000100
	d = 0b00001000
	e = 0b00010000
	f = 0b00100000
	g = 0b01000000
	h = 0b10000000
)

func newDisplaySignal(s string) *displaySignal {
	var signal int

	// log.Printf("%s", s)
	for _, r := range s {
		// log.Printf("%s -> %d -> %d", string(r), r, r-97)

		switch string(r) {
		case "a":
			// log.Printf("%.7b (%d) |= %.7b => %.7b", signal, signal, a, signal|int(a))
			signal |= int(a)
		case "b":
			// log.Printf("%.7b (%d) |= %.7b => %.7b", signal, signal, b, signal|int(b))
			signal |= int(b)
		case "c":
			// log.Printf("%.7b (%d) |= %.7b => %.7b", signal, signal, c, signal|int(c))
			signal |= int(c)
		case "d":
			// log.Printf("%.7b (%d) |= %.7b => %.7b", signal, signal, d, signal|int(d))
			signal |= int(d)
		case "e":
			// log.Printf("%.7b (%d) |= %.7b => %.7b", signal, signal, e, signal|int(e))
			signal |= int(e)
		case "f":
			// log.Printf("%.7b (%d) |= %.7b => %.7b", signal, signal, f, signal|int(f))
			signal |= int(f)
		case "g":
			// log.Printf("%.7b (%d) |= %.7b => %.7b", signal, signal, g, signal|int(g))
			signal |= int(g)
		case "h":
			// log.Printf("%.7b (%d) |= %.7b => %.7b", signal, signal, h, signal|int(h))
			signal |= int(h)
		}
	}
	// log.Printf("signal '%s' => %.7b", s, signal)

	return &displaySignal{
		source: s,
		signal: signal,
	}
}
