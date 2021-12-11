package main

import (
	"errors"
	"flag"
	"fmt"
	"os"
)

type CommandLineArgs struct {
	part  int
	input string
}

func parseArgs() (CommandLineArgs, error) {
	inputPtr := flag.String("input", "", "TODO: usage")
	partPtr := flag.Int("part", 0, "")

	flag.Parse()

	var parsedArgs CommandLineArgs

	input := *inputPtr
	if _, err := os.Stat(input); err != nil {
		message := fmt.Sprintf("Expected input (%s) to exist", input)
		return parsedArgs, errors.New(message)
	}

	parsedArgs.input = input

	part := *partPtr
	if part != 1 && part != 2 {
		message := fmt.Sprintf("Expected part (%d) to be either 1 or 2", part)
		return parsedArgs, errors.New(message)
	}

	parsedArgs.part = part

	return parsedArgs, nil
}

type Solution func(input string) int

func runSolution(part1 Solution, part2 Solution) int {

	parsedArgs, err := parseArgs()
	if err != nil {
		fmt.Println(err)
		return 1
	}

	contents, err := os.ReadFile(parsedArgs.input)
	if err != nil {
		fmt.Println(err)
		return 1
	}

	input := string(contents)

	var solution Solution
	if parsedArgs.part == 1 {
		solution = part1
	} else {
		solution = part2
	}

	answer := solution(input)

	fmt.Printf("Part %d: %d\n", parsedArgs.part, answer)
	return 0
}
