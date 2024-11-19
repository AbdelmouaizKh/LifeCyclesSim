import random
from abc import ABC,abstractmethod

class creature(ABC):
    creatures = []
    def __init__(self,dna):
        self.dna = dna
        self.express_dna()
        creature.creatures.append(self)

    @abstractmethod
    def express_dna(self):
        pass
    
    def clone(self):
        return creature(self.dna)

class animal(creature):
    animals = []
    def __init__(self,dna,food=0):
        self.food = food
        self.size = None
        self.reproduction_threshold = None
        self.speed = None
        self.toxicity_resistance = None
        super().__init__(dna)
        animal.animals.append(self)

    def express_dna(self):
        dna_mapping = {
            'size': {"a": 100, "b": 80, "c": 60, "d": 40, "e": 20, "f": 10},
            'reproduction_threshold': {"a": 10, "b": 20, "c": 50, "d": 100, "e": 200, "f": 1000},
            'speed': {"a": 100, "b": 80, "c": 60, "d": 40, "e": 20, "f": 10},
            'toxicity_resistance': {"a": 1, "b": 0.5, "c": 0.25, "d": 0.1, "e": 0.01, "f": 0}
        }
        self.size = dna_mapping['size'][self.dna[0]]
        self.reproduction_threshold = dna_mapping['reproduction_threshold'][self.dna[1]]
        self.speed = dna_mapping['speed'][self.dna[2]]
        self.toxicity_resistance = dna_mapping['toxicity_resistance'][self.dna[3]]



    def reproduce(parent_dna, mutation_rate=0.1):
        
        possible_genes = "abcdef"
        
        offspring_dna = ""
        for gene in parent_dna:
            if random.random() < mutation_rate:
                new_gene = random.choice([g for g in possible_genes if g != gene])
                offspring_dna += new_gene
            else:
                offspring_dna += gene
        
        return offspring_dna


class tree(creature):
    trees = []
    def __init__(self,dna,position):
        self.position = position
        self.caloric_value = None
        self.fruit_count = None
        self.size = None
        self.toxicity = None
        super().__init__(dna)
        tree.trees.append(self)

    def express_dna(self):
        dna_mapping = {
            'caloric_value': {"a": 200, "b": 100, "c": 50, "d": 10, "e": 0, "f": -50},
            'fruit_count': {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1, "f": 0},
            'size': {"a": 10, "b": 5, "c": 3, "d": 2, "e": 1, "f": 0},
            'toxicity': {"a": 0, "b": 0.01, "c": 0.1, "d": 0.25, "e": 0.5, "f": 1}
        }
        self.caloric_value = dna_mapping['caloric_value'][self.dna[0]]
        self.fruit_count = dna_mapping['fruit_count'][self.dna[1]]
        self.size = dna_mapping['size'][self.dna[2]]
        self.toxicity = dna_mapping['toxicity'][self.dna[3]]

    def grow_fruit(self):
        pass

class world():
    worlds = []
    def __init__(self,size,trees=[],animals=[],max_animals=100):
        self.size = size
        self.trees = trees
        self.animals = animals
        self.max_animals = max_animals
        world.worlds.append(self)

    def create_trees(self,trees_dna):
        trees_dna = set(trees_dna)
        if len(self.trees)+len(trees_dna)>(self.size-1)**2:
            return "insufficient space"
        while trees_dna:
            possible_positions = [(x,y) for x in range(1,self.size) for y in range(1,self.size) if (x,y) not in [i.position for i in self.trees]]
            self.trees.append(tree(trees_dna.pop(),random.choice(possible_positions)))
        return "Planting complete"

    def create_animals(self,animals):
        pass
    
    def step(self):
        pass