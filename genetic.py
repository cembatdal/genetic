import random

def create_population(population_size, chromosome_size):
    population = []
    for i in range(population_size):
        chromosome = random.sample(range(1, chromosome_size+1), chromosome_size)
        population.append(chromosome)
    print(population)
    return population

# Geliştirilmiş fitness fonksiyonu
def fitness(chromosome, prep_matrix):
    total_prep_time = 0
    for i in range(len(chromosome) - 1):
        current_job = chromosome[i]
        next_job = chromosome[i+1]
        total_prep_time += prep_matrix[current_job - 1][next_job - 1]
    return total_prep_time

# Seçim işlemi
def selection(population):
    parent1 = random.choice(population)
    parent2 = random.choice(population)
    print("p1: ", parent1, "p2: ", parent2)
    return parent1, parent2

# PMX Çaprazlama İşlemi
def pmx_crossover(parent1, parent2, part_length):
    n = len(parent1)
    while True:
        crossover_point1 = random.randint(0, n-1)
        crossover_point2 = random.randint(0, n-1)
        while crossover_point2 == crossover_point1:
            crossover_point2 = random.randint(0, n-1)
        if abs(crossover_point2 - crossover_point1) == part_length:
            break
        
    if crossover_point1 > crossover_point2:
        crossover_point1, crossover_point2 = crossover_point2, crossover_point1
        
    print("cross.p1: ", crossover_point1, "cross.p2: ", crossover_point2)

    child1 = [-1] * n
    child2 = [-1] * n

    # child1 oluşturma
    for i in range(crossover_point1, crossover_point2+1):
        child1[i] = parent1[i]

    for i in range(crossover_point1, crossover_point2+1):
        if parent2[i] not in child1:
            j = i
            while parent1[j] in child1[crossover_point1:crossover_point2+1]:
                j = parent2.index(parent1[j])
            child1[j] = parent2[i]

    for i in range(n):
        if child1[i] == -1:
            child1[i] = parent2[i]

    # child2 oluşturma
    for i in range(crossover_point1, crossover_point2+1):
        child2[i] = parent2[i]

    for i in range(crossover_point1, crossover_point2+1):
        if parent1[i] not in child2:
            j = i
            while parent2[j] in child2[crossover_point1:crossover_point2+1]:
                j = parent1.index(parent2[j])
            child2[j] = parent1[i]

    for i in range(n):
        if child2[i] == -1:
            child2[i] = parent1[i]
    print("c1: ", child1, "c2: ", child2)
    print("***************************")
    return child1, child2

# Mutasyon işlemi
def mutation(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# Genetik algoritma
def genetic_algorithm(population_size, chromosome_size, generations, mutation_rate, part_length):
    population = create_population(population_size, chromosome_size)

    for generation in range(generations):
        new_population = []

        # Elitizm
        population = sorted(population, key=lambda chromosome: fitness(chromosome, prep_matrix), reverse=False)
        new_population.append(population[0])

        # Üreme
        while len(new_population) < population_size:
            parent1, parent2 = selection(population)
            child1, child2 = pmx_crossover(parent1, parent2, part_length)
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)
            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    # Sonuçları döndürme
    population = sorted(population, key=lambda chromosome: fitness(chromosome, prep_matrix), reverse=True)
    return population[0]

# Kullanım örneği
chromosome_size = 5
prep_matrix = [[0, 1, 3, 2, 8], 
               [1, 0, 5, 6, 7], 
               [3, 5, 0, 4, 2],
               [2, 6, 4, 0, 9],
               [8, 7, 2, 9, 0]]
#solution = [1]*chromosome_size
result = genetic_algorithm(population_size=50, chromosome_size=chromosome_size, generations=50, mutation_rate=0.1, part_length=2)

#print("Hedef: ", solution)
print("Bulunan: ", result)
