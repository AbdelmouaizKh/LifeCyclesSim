from simulation.display import plot_data
from simulation.helper_functions import world_generator, random_dna_generator

def main():
    dna_gen_pos = random_dna_generator(20,1)
    dna_gen_mid = random_dna_generator(100,0)
    dna_gen_nig = random_dna_generator(10,-1)
    worlds = world_generator(5,dna_gen_nig.generate(),dna_gen_pos.generate())
    worlds.initiate()
    plot_data(worlds.simultaneous_steps(40))


if __name__ == "__main__":
    main()
