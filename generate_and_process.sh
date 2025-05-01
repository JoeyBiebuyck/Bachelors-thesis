#!/bin/bash

start_time=$(date +%s)
batch_start_time=$(date +%s)

amount_of_timesteps=300
n_arms=20
m_top=2
experiment_name="${n_arms}arms_${amount_of_timesteps}t_${m_top}m_NoZeroMean"

dir="results"
full_dir="${dir}/${experiment_name}"
mkdir -p "$full_dir"
mkdir -p "$full_dir/results"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_batch_time() {
    local current=$(date +%s)
    local elapsed=$((current - batch_start_time))
    echo -e "${BLUE}Batch time: $(format_time $elapsed)${NC}"
    batch_start_time=$(date +%s) # update the batch time so the next batch starts correctly
}

echo -e "${GREEN}Script started at $(date)${NC}"

for r in {1..100}
do
python run_bfts_xss.py -s $r -t $amount_of_timesteps -n $n_arms -m $m_top > ${full_dir}/bfts.$r.csv
python postprocess.py -m $m_top -c ${full_dir}/bfts.$r.csv -n $n_arms -s prop_of_success > "${full_dir}/bfts-$r.prop_of_success"
python run_atlucb_xss.py -s $r -t $amount_of_timesteps -n $n_arms -m $m_top > ${full_dir}/atlucb.$r.csv
python postprocess.py -m $m_top -c ${full_dir}/atlucb.$r.csv -n $n_arms -s prop_of_success > "${full_dir}/atlucb-$r.prop_of_success"
python run_uniform_xss.py -s $r -t $amount_of_timesteps -n $n_arms -m $m_top > ${full_dir}/uniform.$r.csv
python postprocess.py -m $m_top -c ${full_dir}/uniform.$r.csv -n $n_arms -s prop_of_success > "${full_dir}/uniform-$r.prop_of_success"

if [ $r -eq 1 ]; then
    current=$(date +%s)
    batch_time=$((current - start_time))
    if [ $batch_time -gt 0 ]; then
        echo -e "${YELLOW}Estimated time for entire process: $(format_time $((batch_time * 100)))${NC}"
    else
        echo -e "${YELLOW}Estimated time for entire process: $(format_time 1)${NC}"
    fi
fi

print_elapsed
print_batch_time

echo "Current progress: $r%"
echo "------------------------------"
done

end_time=$(date +%s)
total_elapsed=$((end_time - start_time))

echo -e "${RED}Generating completed in $(format_time $total_elapsed)${NC}"

python merge_and_plot.py -d $full_dir