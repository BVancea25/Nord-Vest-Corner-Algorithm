import random
from typing import List

# Clasa Item definește un obiect cu un nume, greutate și valoare
class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


# Clasa Individual reprezintă o soluție candidat pentru problema rucsacului
class Individual:
    def __init__(self, bits: List[int]):
        self.bits = bits  # Configurația de 0 și 1 care determină selecția obiectelor
    
    def __str__(self):
        return repr(self.bits)  # Reprezentare în format text a soluției

    def __hash__(self):
        return hash(str(self.bits))  # Hash pentru utilizarea în structuri de date, ex. set
    
    # Funcția fitness calculează valoarea totală a soluției dacă greutatea este sub limita admisă
    def fitness(self) -> float:
        total_value = sum([
            bit * item.value
            for item, bit in zip(items, self.bits)  # Valoarea obiectelor selectate
        ])

        total_weight = sum([
            bit * item.weight
            for item, bit in zip(items, self.bits)  # Greutatea obiectelor selectate
        ])

        if total_weight <= MAX_KNAPSACK_WEIGHT:
            return total_value  # Returnează valoarea dacă soluția este validă
        
        return 0  # Returnează 0 dacă soluția depășește greutatea maximă


# Constantele problemei: greutatea maximă a rucsacului și ratele pentru operațiile genetice
MAX_KNAPSACK_WEIGHT = 15
CROSSOVER_RATE = 0.53
MUTATION_RATE = 0.013
REPRODUCTION_RATE = 0.15

# Lista obiectelor care pot fi selectate pentru rucsac
items = [
    Item("A", 7, 5),
    Item("B", 2, 4),
    Item("C", 1, 7),
    Item("D", 9, 2)
]

# Funcția pentru generarea populației inițiale
def generate_initial_population(count=6) -> List[Individual]:
    population = set()  # Utilizăm un set pentru a evita duplicatele

    # Generăm o populație inițială cu `count` indivizi
    while len(population) != count:
        # Generăm o configurație aleatorie de 0 și 1 pentru fiecare obiect
        bits = [
            random.choice([0, 1])
            for _ in items
        ]
        population.add(Individual(bits))

    return list(population)  # Convertim setul într-o listă


# Funcția de selecție a părinților folosind turnee
def selection(population: List[Individual]) -> List[Individual]:
    parents = []
    
    # Amestecăm aleator populația
    random.shuffle(population)

    # Selectăm părinții prin turnee între indivizi
    if population[0].fitness() > population[1].fitness():
        parents.append(population[0])
    else:
        parents.append(population[1])
    
    if population[2].fitness() > population[3].fitness():
        parents.append(population[2])
    else:
        parents.append(population[3])

    return parents


# Funcția de recombinare (crossover) între doi părinți
def crossover(parents: List[Individual]) -> List[Individual]:
    N = len(items)  # Lungimea configurației

    # Creăm doi copii prin combinarea părților din configurațiile părinților
    child1 = parents[0].bits[:N//2] + parents[1].bits[N//2:]
    child2 = parents[0].bits[N//2:] + parents[1].bits[:N//2]

    return [Individual(child1), Individual(child2)]


# Funcția de mutație aplicată indivizilor
def mutate(individuals: List[Individual]) -> List[Individual]:
    for individual in individuals:
        for i in range(len(individual.bits)):
            if random.random() < MUTATION_RATE:  # Cu o probabilitate MUTATION_RATE
                individual.bits[i] = ~individual.bits[i]  # Inversăm bitul


# Funcția pentru generarea următoarei generații
def next_generation(population: List[Individual]) -> List[Individual]:
    next_gen = []
    while len(next_gen) < len(population):
        children = []

        # Selecție pentru a alege părinții
        parents = selection(population)

        # Reproducere directă
        if random.random() < REPRODUCTION_RATE:
            children = parents
        else:
            # Recombinare
            if random.random() < CROSSOVER_RATE:
                children = crossover(parents)
            
            # Mutație
            if random.random() < MUTATION_RATE:
                mutate(children)

        next_gen.extend(children)  # Adăugăm copiii în generația următoare

    return next_gen[:len(population)]  # Limităm dimensiunea generației


# Funcția pentru afișarea unei generații
def print_generation(population: List[Individual]):
    for individual in population:
        print(individual.bits, individual.fitness())  # Afișăm configurația și fitness-ul
    print()
    print("Average fitness", sum([x.fitness() for x in population])/len(population))
    print("-" * 32)


# Funcția care calculează fitness-ul mediu al unei populații
def average_fitness(population: List[Individual]) -> float:
    return sum([i.fitness() for i in population]) / len(population)


# Funcția principală pentru rezolvarea problemei rucsacului
def solve_knapsack() -> Individual:
    population = generate_initial_population()  # Generăm populația inițială

    avg_fitnesses = []

    # Evoluăm populația pentru 500 de generații
    for _ in range(500):
        avg_fitnesses.append(average_fitness(population))
        population = next_generation(population)

    # Sortăm populația după fitness și returnăm cel mai bun individ
    population = sorted(population, key=lambda i: i.fitness(), reverse=True)
    return population[0]


if __name__ == '__main__':
    solution = solve_knapsack()
    print(solution, solution.fitness())  # Afișăm soluția finală și fitness-ul său
