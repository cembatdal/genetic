import random

def create_population(population_size, chromosome_size):
    population = []
    for i in range(population_size):
        chromosome = random.sample(range(1, chromosome_size+1), chromosome_size)
        population.append(chromosome)
    return population

# Fitness Fonksiyonu:
# Yalnızca reçeteler arası geçiş süreleri dikkate alınır.
def fitness(chromosome, prep_matrix):
    total_prep_time = 0
    for i in range(len(chromosome) - 1):
        current_job = chromosome[i]
        next_job = chromosome[i+1]
        total_prep_time += prep_matrix[current_job - 1][next_job - 1]
    return total_prep_time

# Seçim işlemi tamamen rastgele biçimde yapılır
def selection(population):
    parent1 = random.choice(population)
    parent2 = random.choice(population)
    return parent1, parent2

# PMX Çaprazlama İşlemi
def pmx_crossover(parent1, parent2, part_length):
    n = len(parent1)
    while True:
        crossover_point1 = random.randint(0, n-1)
        crossover_point2 = random.randint(0, n-1)
        # Çaprazlama noktalarının aynı olmasını engelleyen kontrol mekanizması
        while crossover_point2 == crossover_point1:
            crossover_point2 = random.randint(0, n-1)
        if abs(crossover_point2 - crossover_point1) == part_length:
            break
        
    if crossover_point1 > crossover_point2:
        crossover_point1, crossover_point2 = crossover_point2, crossover_point1

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
    return child1, child2

# Mutasyon işlemi
def mutation(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(chromosome)), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome

# Genetik algoritma
def genetic_algorithm(population_size, chromosome_size, generations, mutation_rate, part_length):
    population = create_population(population_size, chromosome_size)

    for generation in range(generations):
        new_population = []

        # Elitizm:  Popülasyonun fitness değerleri hesaplanır ve listede sıralanır.
        #           Listede en üst sırada bulunan kromozom sonraki nesle direkt olarak aktarılır.
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
    population = sorted(population, key=lambda chromosome: fitness(chromosome, prep_matrix), reverse=False)
    return population[0]

# Kullanım örneği
chromosome_size = 8
prep_matrix = [[0, 8, 9, 10, 9, 10, 9, 9], 
               [8, 0, 6, 9, 8, 8, 10, 6], 
               [9, 6, 0, 10, 9, 9, 9, 8],
               [10, 9, 10, 0, 5, 8, 8, 5],
               [9, 8, 9, 5, 0, 10, 5, 10],
               [10, 8, 9, 8, 10, 0, 8, 6],
               [9, 10, 9, 8, 5, 8, 0, 5],
               [9, 6, 8, 5, 10, 6, 5, 0]]
result = genetic_algorithm(population_size=800, chromosome_size=chromosome_size, generations=1000, mutation_rate=0.1, part_length=4)

print("Bulunan: ", result)
print("Elde edilen fitness değeri: ", fitness(result, prep_matrix))
