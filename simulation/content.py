import random
from abc import ABC,abstractmethod

class creature(ABC):
    creatures = []
    def __init__(self,dna):
        self.dna = dna
        self.express_dna()
        #creature.creatures.append(self)

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
        self.alive = True
        super().__init__(dna)
        #animal.animals.append(self)

    def express_dna(self):
        dna_mapping = {
            'size': {"a":100,"b":80,"c":60,"d":40,"e":20,"f":10},
            'reproduction_threshold': {"a": 100, "b": 200, "c": 300, "d": 500, "e": 750, "f": 1000},
            'speed': {"a":100,"b":80,"c":60,"d":40,"e":20,"f":10},
            'toxicity_resistance': {"a": 1, "b": 0.5, "c": 0.25, "d": 0.1, "e": 0.01, "f": 0}
        }
        self.size = dna_mapping['size'][self.dna[0]]
        self.reproduction_threshold = dna_mapping['reproduction_threshold'][self.dna[1]]
        self.speed = dna_mapping['speed'][self.dna[2]]
        self.toxicity_resistance = dna_mapping['toxicity_resistance'][self.dna[3]]



    def reproduce(self,mutation_rate=0.1):
        
        possible_genes = "abcdef"
        
        offspring_dna = ""
        for gene in self.dna:
            if random.random() < mutation_rate:
                new_gene = random.choice([g for g in possible_genes if g != gene])
                offspring_dna += new_gene
            else:
                offspring_dna += gene
        
        return offspring_dna
    def die(self,msg):
        #print(msg)
        self.alive = False

    def consume(self,fruit):
        self.food += fruit[0]
        poison_chance = fruit[1]*(1-self.toxicity_resistance)
        if random.choices((0,1),weights=[1-poison_chance,poison_chance]):
            self.die("dies of poison")
    
    def energy_consumption(self):
        self.food -= self.size+self.speed
        if self.food <=0:
            self.die("dies of hunger")
        
        number_of_ofspring = self.food//self.reproduction_threshold
        chance = random.choices((0,1),weights=[(1-self.food)/self.reproduction_threshold,self.food/self.reproduction_threshold])[0]
        number_of_ofspring += chance
        self.food = self.food*(1-chance)
        return [self.reproduce() for i in range(number_of_ofspring)]


class tree(creature):
    trees = []
    def __init__(self,dna,position):
        self.position = position
        self.caloric_value = None
        self.fruit_count = None
        self.size = None
        self.toxicity = None
        super().__init__(dna)
        #tree.trees.append(self)

    def express_dna(self):
        dna_mapping = {
            'caloric_value': {"a":200,"b":100,"c":50,"d":10,"e":0,"f":-50},
            'fruit_count': {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1, "f": 0},
            'size': {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1, "f": 0},
            'toxicity': {"a": 0, "b": 0.01, "c": 0.1, "d": 0.25, "e": 0.5, "f": 1}
        }
        self.caloric_value = dna_mapping['caloric_value'][self.dna[0]]
        self.fruit_count = dna_mapping['fruit_count'][self.dna[1]]
        self.size = dna_mapping['size'][self.dna[2]]
        self.toxicity = dna_mapping['toxicity'][self.dna[3]]

    def grow_fruit(self):
        return [(self.caloric_value,self.toxicity) for i in range(self.fruit_count)]
    
    def host_animals(self,animals):
        animals.sort(key=lambda x:x.size+x.speed)
        fruits = self.grow_fruit()
        if len(animals)==0 or len(fruits)==0:
            return None
        while len(fruits)>len(animals):
            animals[0].consume(fruits.pop())
        for i in range(len(fruits)):
            animals[i].consume(fruits[i])


class world():
    worlds = []
    def __init__(self,size,trees=[],animals=[],max_animals=100):
        self.size = size
        self.trees = trees
        self.animals = animals
        self.max_animals = max_animals
        world.worlds.append(self)

    def create_trees(self,trees_dna):
        if len(self.trees)+len(trees_dna)>(self.size-1)**2:
            return "insufficient space"
        while trees_dna:
            possible_positions = [(x,y) for x in range(1,self.size) for y in range(1,self.size) if (x,y) not in [i.position for i in self.trees]]
            self.trees.append(tree(trees_dna.pop(),random.choice(possible_positions)))
        return "Planting complete"

    def create_animals(self,animal_dnas):
        while self.max_animals>len(self.animals) and animal_dnas:
            self.animals.append(animal(animal_dnas.pop()))
        return animal_dnas
    
    def step(self):
        self.animals = list(filter(lambda x:x.alive,self.animals))
        hosted_animals_counter = 0
        for i in range(len(self.trees)):
            if hosted_animals_counter == len(self.animals):
                break
            bound = min(len(self.animals),hosted_animals_counter+self.trees[i].size)
            self.trees[i].host_animals(self.animals[hosted_animals_counter:bound])
            hosted_animals_counter += self.trees[i].size
        
        new_animals_dnas = []
        for i in self.animals:
            new_animals_dnas += i.energy_consumption()
        
        self.create_animals(new_animals_dnas)
