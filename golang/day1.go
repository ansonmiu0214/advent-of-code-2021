package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parseMeasurements(input string) []int {
	lines := strings.Split(input, "\n")

	measurements := make([]int, len(lines))
	for idx, line := range lines {
		measurement, err := strconv.Atoi(line)
		if err != nil {
			fmt.Printf("WARNING: failed to parse measurement (%d)\n", measurement)
		} else {
			measurements[idx] = measurement
		}
	}

	return measurements
}

type IntQueue struct {
	elements chan int
}

func NewIntQueue(size int) IntQueue {
	return IntQueue{
		elements: make(chan int, size),
	}
}

func (queue IntQueue) Enqueue(element int) {
	select {
	case queue.elements <- element:
	default:
		panic("Queue full")
	}
}

func (queue IntQueue) Dequeue() int {
	select {
	case element := <-queue.elements:
		return element
	default:
		panic("Queue empty")
	}
}

func countIncrements(measurements []int, windowSize int) int {

	if windowSize <= 0 {
		message := fmt.Sprintf("Window size (%d) must be positive", windowSize)
		panic(message)
	}

	window := NewIntQueue(windowSize)
	prevWindowSum := 0
	for idx := 0; idx < windowSize; idx++ {
		window.Enqueue(measurements[idx])
		prevWindowSum += measurements[idx]
	}

	increments := 0
	for idx := windowSize; idx < len(measurements); idx++ {
		currWindowSum := prevWindowSum - window.Dequeue() + measurements[idx]

		if prevWindowSum < currWindowSum {
			increments++
		}

		window.Enqueue(measurements[idx])
		prevWindowSum = currWindowSum
	}

	return increments
}

func part1(input string) int {
	measurements := parseMeasurements(input)
	return countIncrements(measurements, 1)
}

func part2(input string) int {
	measurements := parseMeasurements(input)
	return countIncrements(measurements, 3)
}

func main() {
	exitCode := runSolution(part1, part2)
	os.Exit(exitCode)
}
