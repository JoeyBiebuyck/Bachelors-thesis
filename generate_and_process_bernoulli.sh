#!/bin/bash

date_time=$(date +"%Y-%m-%d_%Hh%Mm%Ss")
start_time=$(date +%s)
batch_start_time=$(date +%s)
total_time=0

#statistic=prop_of_success
statistic=prop_and_sum
amount_of_timesteps=7000
n_arms=50
m_top=5
experiment_name="${n_arms}arms_${amount_of_timesteps}t_${m_top}m_shuffled_bernoulli_$date_time"

dir="experiments" #results
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
    echo -e "${YELLOW}Elapsed time: $(format_time $elapsed)/${total_time}${NC}"
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
python run_bfts_bernoulli.py -s $r -t $amount_of_timesteps -n $n_arms -m $m_top > ${full_dir}/bfts.$r.csv
python postprocess_bernoulli.py -m $m_top -c ${full_dir}/bfts.$r.csv -n $n_arms -s $statistic > "${full_dir}/bfts-$r.$statistic"
python run_atlucb_bernoulli.py -s $r -t $amount_of_timesteps -n $n_arms -m $m_top > ${full_dir}/atlucb.$r.csv
python postprocess_bernoulli.py -m $m_top -c ${full_dir}/atlucb.$r.csv -n $n_arms -s $statistic > "${full_dir}/atlucb-$r.$statistic"
python run_uniform_bernoulli.py -s $r -t $amount_of_timesteps -n $n_arms -m $m_top > ${full_dir}/uniform.$r.csv
python postprocess_bernoulli.py -m $m_top -c ${full_dir}/uniform.$r.csv -n $n_arms -s $statistic > "${full_dir}/uniform-$r.$statistic"

if [ $r -eq 1 ]; then
    current=$(date +%s)
    batch_time=$((current - start_time))
    if [ $batch_time -gt 0 ]; then
        total_time=$(format_time $((batch_time * 100)))
        echo -e "${YELLOW}Estimated time for entire process: ${total_time} ${NC}"
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

python merge_and_plot.py -d $full_dir -n $n_arms -m $m_top -t $amount_of_timesteps -s $statistic