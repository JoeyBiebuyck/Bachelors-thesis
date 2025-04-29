def print_header(m):
    header = ['m %i' % i for i in range(1, m + 1)]
    print("t," + ",".join(header), flush=True)
    
def run(algo, steps):
    for t in range(1, steps + 1):
        J_t = algo.step(t)
        J_t = [str(i) for i in J_t]
        # print(f"Current means of all the arms: {algo.mean_per_arm}")
        # arm_with_mean = list(zip(range(0, 20), algo.mean_per_arm)) # MOET JE AANPASSEN ALS JE MEER ARMS WIL
        # print(f"This is each arm with its respective mean: {arm_with_mean}")
        # print(f"Here is how much each arm has been sampled: {algo.has_arm_been_played}")
        print(str(t) + "," + ",".join(J_t), flush=True)
