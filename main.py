# main.py

from simulation.content import world, tree, animal

def main():
    # Initialize the world
    my_world = world(size=100, max_animals=50)

    # Create some trees with random DNA
    tree_dnas = ["abcf", "abcf", "abcf"]
    animal_dnas = ["bbbb","bbbb","bbbb","bbbb"]
    print(my_world.create_trees(tree_dnas))
    my_world.create_animals(animal_dnas)

    # Run a simulation step
    print("Initial state:")
    print(f"Trees: {len(my_world.trees)}, Animals: {len(my_world.animals)}")
    my_world.step()
    print("Simulation step completed!")
    print(f"Trees: {len(my_world.trees)}, Animals: {len(my_world.animals)}")
    my_world.step()
    print("Simulation step completed!")
    print(f"Trees: {len(my_world.trees)}, Animals: {len(my_world.animals)}")

if __name__ == "__main__":
    main()
