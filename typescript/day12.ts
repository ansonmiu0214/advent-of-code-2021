import { runSolution } from "./util";

type Cave = string;
type Path = Cave[];
type Passage = [Cave, Cave];
type Layout = {
    [cave: Cave]: Set<Cave>;
};
type Counter<T> = Map<T, number>;
type CaveVisitStrategy = (cave: Cave, visitCount: Counter<Cave>) => boolean;

function parsePassage(line: string): Passage {
    const passage = line.split("-");
    if (passage.length !== 2) {
        throw new Error(
            `Expected 2 tokens on line '${line}', found ${passage.length}`
        );
    }

    return passage as Passage;
}

function parseLayout(input: string): Layout {
    const layout: Layout = {};

    input.split("\n").forEach((line) => {
        const [cave1, cave2]: [string, string] = parsePassage(line);

        if (!(cave1 in layout)) {
            layout[cave1] = new Set();
        }
        layout[cave1].add(cave2);

        if (!(cave2 in layout)) {
            layout[cave2] = new Set();
        }
        layout[cave2].add(cave1);
    });

    return layout;
}

const isStart = (cave: Cave) => cave === "start";
const isEnd = (cave: Cave) => cave === "end";
const isTerminal = (cave: Cave) => isStart(cave) || isEnd(cave);
const isSmallCave = (cave: Cave) =>
    !isTerminal(cave) &&
    Array.from(cave).every((letter) => letter.toLowerCase() === letter);
const isBigCave = (cave: Cave) =>
    !isTerminal(cave) &&
    Array.from(cave).every((letter) => letter.toUpperCase() === letter);

function findPaths(
    layout: Layout,
    pathSoFar: Path,
    currCave: Cave,
    visitCount: Counter<Cave>,
    canVisitCave: CaveVisitStrategy
): Path[] {
    const allPaths: Path[] = [];

    if (!canVisitCave(currCave, visitCount)) {
        return allPaths;
    }

    if (!visitCount.has(currCave)) {
        visitCount.set(currCave, 0);
    }
    visitCount.set(currCave, visitCount.get(currCave)! + 1);
    pathSoFar.push(currCave);

    if (isEnd(currCave)) {
        allPaths.push([...pathSoFar]);
    } else {
        layout[currCave].forEach((neighbour) => {
            allPaths.push(
                ...findPaths(
                    layout,
                    pathSoFar,
                    neighbour,
                    visitCount,
                    canVisitCave
                )
            );
        });
    }

    pathSoFar.pop();
    visitCount.set(currCave, visitCount.get(currCave)! - 1);

    return allPaths;
}

function part1(input: string): number {
    const canVisitCave: CaveVisitStrategy = (cave, prevVisitCounts) => {
        if (!prevVisitCounts.has(cave) || prevVisitCounts.get(cave)! === 0) {
            return true;
        }

        if (isStart(cave) || isSmallCave(cave)) {
            return false;
        }

        return true;
    };

    const layout = parseLayout(input);
    const paths = findPaths(layout, [], "start", new Map(), canVisitCave);

    return paths.length;
}

function part2(input: string): number {
    const canVisitCave: CaveVisitStrategy = (cave, prevVisitCounts) => {
        if (!prevVisitCounts.has(cave) || prevVisitCounts.get(cave)! === 0) {
            return true;
        }

        if (isStart(cave)) {
            return false;
        }

        if (isSmallCave(cave)) {
            const prevCountForCave = prevVisitCounts.get(cave);
            if (prevCountForCave !== undefined && prevCountForCave > 1) {
                return false;
            }

            const visitedOtherSmallCaveMoreThanOnce = Array.from(
                prevVisitCounts.entries()
            ).filter(
                ([existingSmallCave, visitCount]) =>
                    isSmallCave(existingSmallCave) &&
                    existingSmallCave !== cave &&
                    visitCount > 1
            );

            if (visitedOtherSmallCaveMoreThanOnce.length > 0) {
                return false;
            }
        }

        return true;
    };

    const layout = parseLayout(input);
    const paths = findPaths(layout, [], "start", new Map(), canVisitCave);

    return paths.length;
}

process.exit(runSolution(part1, part2));
