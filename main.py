from simulation.display import plot_registered_data
from simulation.helper_functions import world_generator, random_dna_generator

def main():
    dna_gen_pos = random_dna_generator(10,1)
    dna_gen_mid = random_dna_generator(10,0)
    dna_gne_nig = random_dna_generator(10,-1)
    worlds = world_generator(5,dna_gen_pos.generate(),dna_gen_mid.generate())
    worlds.initiate()
    plot_registered_data(worlds.simultaneous_steps(20))


if __name__ == "__main__":
    main()
