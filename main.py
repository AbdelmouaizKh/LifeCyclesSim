# main.py

from simulation.content import world, tree, animal

def main():
    # Initialize the world
    my_world = world(size=100, max_animals=75)

    # Create some trees with random DNA
    tree_dnas = ["abcd","baef","adda"]
    animal_dnas = ["cccc","cccc","cccc","cccc","cccc","cccc"]
    print(my_world.create_trees(tree_dnas))
    my_world.create_animals(animal_dnas)

    # Run a simulation step
    print("initial state:"+f"animals alive: {len(my_world.animals)}")
    for i in range(2000):
        my_world.step()
        print(f"animals alive: {len(my_world.animals)}")
    print("final state:"+f"animals alive: {len(my_world.animals)}")
    for i in range(len(my_world.animals)):
        print(my_world.animals[i].dna)
    

if __name__ == "__main__":
    main()
