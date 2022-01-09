import process from "process";
import { Command, InvalidArgumentError } from "commander";
import { readFileSync } from "fs";

export type Solution = (input: string) => number;

interface CommandLineOptions {
    input: string;
    part: 1 | 2;
}

function parseInput(value: string): CommandLineOptions["input"] {
    return value;
}

function parsePart(value: string): CommandLineOptions["part"] {
    const part = parseInt(value);

    if (part !== 1 && part !== 2) {
        throw new InvalidArgumentError(
            `argument --part: invalid choice: ${part} (choose from 1,2)`
        );
    }

    return part;
}

function parseArgs(args: string[]): CommandLineOptions {
    const program = new Command()
        .requiredOption("-i, --input <input>", "type of input", parseInput)
        .requiredOption("-p, --part <part>", "", parsePart)
        .parse(args);

    return program.opts<CommandLineOptions>();
}

export function runSolution(part1: Solution, part2: Solution): number {
    const parsedArgs = parseArgs(process.argv);

    const input = readFileSync(parsedArgs.input).toString();
    const solution = parsedArgs.part === 1 ? part1 : part2;

    const answer = solution(input);

    console.log(`Part ${parsedArgs.part}: ${answer}`);
    return 0;
}
