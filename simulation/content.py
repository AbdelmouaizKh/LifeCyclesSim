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
    def __str__(self):
        return str(self.dna)

class animal(creature):
    animals = []
    def __init__(self,dna,sex,age=0,food=0):
        self.age = age
        self.sex = sex
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
            'size': {"a":50,"b":40,"c":30,"d":20,"e":10,"f":5},
            'reproduction_threshold': {"a": 50, "b": 750, "c": 100, "d": 125, "e": 150, "f": 200},
            'speed': {"a":100,"b":80,"c":60,"d":40,"e":20,"f":10},
            'toxicity_resistance': {"a": 1, "b": 0.75, "c": 0.5, "d": 0.25, "e": 0.1, "f": 0}
        }
        self.size = dna_mapping['size'][self.dna[0]]
        self.reproduction_threshold = dna_mapping['reproduction_threshold'][self.dna[1]]
        self.speed = dna_mapping['speed'][self.dna[2]]
        self.toxicity_resistance = dna_mapping['toxicity_resistance'][self.dna[3]]



    def reproduce(self,other,mutation_rate=0.1):
        
        possible_genes = "abcdef"
        
        offspring_dna = ""
        for i in range(4):
            offspring_dna += random.choices([self.dna[i],other.dna[i],random.choice(possible_genes)],[0.5*(1-mutation_rate),0.5*(1-mutation_rate),mutation_rate])[0]
        return offspring_dna

    def die(self,msg):
        #print(msg)
        self.alive = False

    def consume(self,fruit):
        self.food += fruit[0]
        poison_chance = fruit[1]*(1-self.toxicity_resistance)
        if random.choices((0,1),weights=[1-poison_chance,poison_chance])[0]:
            self.die("dies of poison")
    
    def energy_consumption(self):
        self.food -= (self.size+self.speed)//7
        if self.food <=0:
            self.die("dies of hunger")
        elif self.age > 5:
            self.die("dies of old age")
        
    def mate(self,other):
        number_of_ofspring = min(min(self.food//self.reproduction_threshold,other.food//other.reproduction_threshold),3)
        self.food -= number_of_ofspring*self.reproduction_threshold
        other.food -+ number_of_ofspring*other.reproduction_threshold
        self.age += 1
        return [self.reproduce(other) for i in range(number_of_ofspring)]


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
            'caloric_value': {"a":2000,"b":1500,"c":1000,"d":750,"e":200,"f":100},
            'fruit_count': {"a": 10, "b": 7, "c": 5, "d": 3, "e": 2, "f": 1},
            'size': {"a": 10, "b": 7, "c": 5, "d": 3, "e": 2, "f": 1},
            'toxicity': {"a": 0, "b": 0.01, "c": 0.1, "d": 0.25, "e": 0.5, "f": 1}
        }
        self.caloric_value = dna_mapping['caloric_value'][self.dna[0]]
        self.fruit_count = dna_mapping['fruit_count'][self.dna[1]]
        self.size = dna_mapping['size'][self.dna[2]]
        self.toxicity = dna_mapping['toxicity'][self.dna[3]]

    def grow_fruit(self):
        return [(self.caloric_value,self.toxicity) for i in range(self.fruit_count)]
    
    def host_animals(self,animals):
        animals.sort(key=lambda x:2*x.size+x.speed)
        fruits = self.grow_fruit()
        if len(animals)==0 or len(fruits)==0:
            return None
        while len(fruits)>len(animals):
            animals[0].consume(fruits.pop())
        for i in range(len(fruits)):
            animals[i].consume(fruits[i])


class world():
    def __init__(self,size,trees=[],animals=[],max_animals=100):
        self.size = size
        self.trees = [tree(trees[i]) for i in range(len(trees))]
        self.animals = [animal(animals[i]) for i in range(len(animals))]
        self.max_animals = max_animals

    def create_trees(self,tree_dnas):
        assert len(self.trees)+len(tree_dnas)<=(self.size-1)**2
        i = 0
        while i<len(tree_dnas):
            possible_positions = [(x,y) for x in range(1,self.size) for y in range(1,self.size) if (x,y) not in [i.position for i in self.trees]]
            self.trees.append(tree(tree_dnas[i],random.choice(possible_positions)))
            i += 1
        return "Planting complete"

    def create_animals(self,animal_dnas):
        i = 0
        while self.max_animals>len(self.animals) and i<len(animal_dnas):
            self.animals.append(animal(animal_dnas[i],random.choice(["male","female"])))
            i += 1
        return animal_dnas
    
    def tree_dna(self):
        return [self.trees[i].dna for i in range(len(self.trees))]
    
    def animal_dna(self):
        return [self.animals[i].dna for i in range(len(self.animals))]
    
    def step(self):
        random.shuffle(self.animals)
        male_animals = list(filter(lambda x:x.sex == "male",self.animals))
        female_animals = list(filter(lambda x:x.sex == "female",self.animals))
        hosted_animals_counter = 0
        for i in range(len(self.trees)):
            if hosted_animals_counter == len(self.animals):
                break
            bound = min(len(self.animals),hosted_animals_counter+self.trees[i].size)
            self.trees[i].host_animals(self.animals[hosted_animals_counter:bound])
            hosted_animals_counter += self.trees[i].size
        new_animals_dnas = []
        for i in self.animals:
            i.energy_consumption()
        self.animals = list(filter(lambda x:x.alive,self.animals))
        for i in range(min([len(male_animals),len(female_animals)])):
            new_animals_dnas += male_animals[i].mate(female_animals[i])
        self.create_animals(new_animals_dnas)

    def reset_world(self):
        self.__init__(size=self.size,max_animals=self.max_animals)
