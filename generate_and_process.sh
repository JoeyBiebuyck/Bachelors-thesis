#!/bin/bash

start_time=$(date +%s)
dir="results"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # no color

# Function to format elapsed time in a readable format
format_time() {
    local seconds=$1
    local hours=$((seconds / 3600))
    local minutes=$(((seconds % 3600) / 60))
    local secs=$((seconds % 60))
    
    if [[ $hours -gt 0 ]]; then
        echo "${hours}h ${minutes}m ${secs}s"
    elif [[ $minutes -gt 0 ]]; then
        echo "${minutes}m ${secs}s"
    else
        echo "${secs}s"
    fi
}

# Print elapsed time
print_elapsed() {
    local current=$(date +%s)
    local elapsed=$((current - start_time))
    echo -e "${YELLOW}Elapsed time: $(format_time $elapsed)${NC}"
}

echo -e "${GREEN}Script started at $(date)${NC}"

for r in {1..100}
do
python run_atlucb_xss.py -s $r -t 10000 -m 2 > $dir/atlucb.$r.csv
python postprocess.py -m 2 -c $dir/atlucb.$r.csv -s prop_of_success > "$dir/atlucb-$r.prop_of_success"
python run_uniform_xss.py -s $r -t 10000 -m 2 > $dir/uniform.$r.csv
python postprocess.py -m 2 -c $dir/uniform.$r.csv -s prop_of_success > "$dir/uniform-$r.prop_of_success"
print_elapsed
echo "Current progress: $r%"
done

end_time=$(date +%s)
total_elapsed=$((end_time - start_time))

echo -e "${RED}Generating completed in $(format_time $total_elapsed)${NC}"

python merge_and_plot.py