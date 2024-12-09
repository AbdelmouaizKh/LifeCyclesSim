import random
from simulation.content import world

# a class to generate, initiate, encompass and also terminate multiple worlds
class world_generator():
    def __init__(self,world_count,starting_tree_dnas,starting_animal_dnas,world_size=100):
        self.world_count = world_count
        self.world_size = world_size
        self.starting_tree_dnas = starting_tree_dnas
        self.starting_animal_dnas = starting_animal_dnas

    def initiate(self):
        self.worlds = [world(self.world_size) for i in range(self.world_count)]
        for i in range(self.world_count):
            self.worlds[i].create_trees(self.starting_tree_dnas)
            self.worlds[i].create_animals(self.starting_animal_dnas)
            
    
    def simultaneous_steps(self,steps):
        registers = list()
        registers += [[self.worlds[i].animal_dna()] for i in range(self.world_count)]
        for j in range(steps):
            for i in range(self.world_count):
                self.worlds[i].step()
                registers[i].append(self.worlds[i].animal_dna())
        return registers
    
    def terminate(self):
        for i in range(self.worlds):
            del self.worlds[i]


# a class to generate random dnas for creating varying batch of animals or/and 
# trees with a bias (0 for none 1 for bias to high traits and -1 for low traits)
class random_dna_generator():
    def __init__(self,count,bias=0):
        self.count = count
        assert bias in [-1,0,1]
        self.bias = bias
    
    def set_param(self,count,bias=0):
        self.count = count
        assert bias in [-1,0,1]
        self.bias = bias

    def generate(self):
        dnas = list()

        if self.bias == 1: letters = ["a","b","c"]
        elif self.bias == -1: letters = ["d","e","f"]
        else : letters = ["a","b","c","d","e","f"]

        for i in range(self.count):
            dnas.append("".join([random.choice(letters) for i in range(4)]))
        
        return(dnas)
