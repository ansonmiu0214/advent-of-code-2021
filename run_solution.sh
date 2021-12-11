#!/usr/bin/env bash

function error {
    echo $1
    exit 1
}


###############################################################################
#                      ADAPTERS PER SUPPORTED LANGUAGE                        #
###############################################################################

function golangSolution {
    SCRIPT_DIR=$1
    DAY=$2
    INPUT_FILE=$3
    PART=$4
    
    SOLUTION="$SCRIPT_DIR/day$DAY.go"
    if [[ ! -f $SOLUTION ]]; then
        error "Cannot find solution: $SOLUTION"
    fi

    set -x
    go run $SOLUTION $SCRIPT_DIR/util.go -input $INPUT_FILE -part $PART
}

function pythonSolution {
    SCRIPT_DIR=$1
    DAY=$2
    INPUT_FILE=$3
    PART=$4
    
    SOLUTION="$SCRIPT_DIR/day$DAY.py"
    if [[ ! -f $SOLUTION ]]; then
        error "Cannot find solution: $SOLUTION"
    fi

    set -x
    python3.8 -m python.day$DAY --input $INPUT_FILE --part $PART
}

###############################################################################
#                                     MAIN                                    #
###############################################################################

LANGUAGE=$1
HERE=$(realpath $(dirname $0))

shift

# Note that we use `"$@"' to let each command-line parameter expand to a 
# separate word. The quotes around '$@' are essential!
# We need TEMP as the `eval set --' would nuke the return value of getopt.
TEMP=$(getopt -o d:i:p: --long day:,input:,part: -n $(basename $0) -- "$@")

if [ $? != 0 ]; then
    echo "Terminating..." >&2 
    exit 1
fi

# Note the quotes around '$TEMP': they are essential!
eval set -- "$TEMP"

while true; do
    case "$1" in
        -d|--day)
            DAY=$2
            shift 2
            ;;
        -i|--input)
            INPUT=$2
            shift 2
            ;;
        -p|--part)
            PART=$2
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Internal error!" 
            exit 1
            ;;
    esac
done

# Sanity check for arguments.
[[ -v DAY ]]    || error "Missing option '-d|--day'"
[[ -v INPUT ]]  || error "Missing option '-i|--input'"
[[ -v PART ]]   || error "Missing option '-p|--part'"

INPUT_FILE="$HERE/data/$INPUT/day$DAY.txt"
if [[ ! -f $INPUT_FILE ]]; then
    error "Cannot find input file: $INPUT_FILE"
fi

# Select the adapter function based on the user-specified language.
case "$LANGUAGE" in
    python)
        RUN_SOLUTION=pythonSolution  
        ;;
    golang)
        RUN_SOLUTION=golangSolution
        ;;
    *)
        error "Unsupported language: $LANGUAGE" 
        ;;
esac

# Sanity check for 
SCRIPT_DIR="$HERE/$LANGUAGE"
if [[ ! -d $SCRIPT_DIR ]]; then
    error "Cannot find directory for language solutions: $SCRIPT_DIR"
fi

$RUN_SOLUTION $SCRIPT_DIR $DAY $INPUT_FILE $PART