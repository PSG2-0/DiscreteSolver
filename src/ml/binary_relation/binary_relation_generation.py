import random
import pandas as pd
import string

class ReflexiveRelationGenerator:
    def __init__(self, n, use_letters=False):
        self.n = n
        self.use_letters = use_letters
        self.M = self.generate_base_set()
    
    def generate_base_set(self):
        return set(random.sample(string.ascii_lowercase, self.n)) if self.use_letters else set(range(self.n))
    
    def generate_reflexive_set(self):
        R = {(i, i) for i in self.M}
        additional_pairs_count = random.randint(1, self.n * (self.n - 1))
        additional_pairs = set()
        while len(additional_pairs) < additional_pairs_count:
            i, j = random.sample(self.M, 2)
            additional_pairs.add((i, j))
        R.update(additional_pairs)
        return R, self.M
    
    def generate_antireflexive_set(self):
        R = {(i, j) for i in self.M for j in self.M if i != j and random.choice([True, False])}
        return R, self.M

    def generate_nonreflexive_set(self):
        R, _ = self.generate_antireflexive_set()
        k = random.randint(1, self.n - 1)
        reflexive_elements = random.sample(self.M, k)
        for el in reflexive_elements:
            R.add((el, el))
        return R, self.M
    

class SymmetricRelationGenerator:
    def __init__(self, n, use_letters=False):
        self.n = n
        self.use_letters = use_letters
        self.M = self.generate_base_set()
    
    def generate_base_set(self):
        return set(random.sample(string.ascii_lowercase, self.n)) if self.use_letters else set(range(self.n))
    
    def generate_symmetric_set(self):
        R = set()
        for i in self.M:
            for j in self.M:
                if random.choice([True, False]):
                    R.add((i, j))
                    R.add((j, i))
        return R, self.M

    def generate_asymmetric_set(self):
        R = set()
        for i in self.M:
            for j in self.M:
                if i != j and (j, i) not in R and random.choice([True, False]):
                    R.add((i, j))
        return R, self.M
    
    def generate_antisymmetric_set(self):
        R = set()
        for i in self.M:
            for j in self.M:
                if i != j and random.choice([True, False]):
                    R.add((i, j))
        return R, self.M
    
    def generate_nonsymmetric_set(self):
        R, _ = self.generate_asymmetric_set()
        k = random.randint(1, self.n - 1)
        symmetric_elements = random.sample(self.M, k)
        for el in symmetric_elements:
            R.add((el, random.choice(list(self.M - {el}))))
        return R, self.M
    

class TransitiveRelationGenerator:
    def __init__(self, n, use_letters=False):
        self.n = n
        self.use_letters = use_letters
        self.M = self.generate_base_set()
    
    def generate_base_set(self):
        return set(random.sample(string.ascii_lowercase, self.n)) if self.use_letters else set(range(self.n))
    
    def generate_transitive_set(self):
        R = set()
        for i in self.M:
            for j in self.M:
                if random.choice([True, False]):
                    R.add((i, j))
                    for k in self.M:
                        if (j, k) in R:
                            R.add((i, k))
        return R, self.M

    def generate_antitransitive_set(self):
        R = set()
        for i in self.M:
            for j in self.M:
                if i != j and random.choice([True, False]):
                    R.add((i, j))
        for (i, j) in list(R):
            for k in self.M:
                if (j, k) in R:
                    R.discard((i, k))
        return R, self.M
    
    def generate_nontransitive_set(self):
        R = set()
        elements = list(self.M)
        while len(R) < self.n:
            pairs = [(elements[i], elements[j]) for i in range(self.n) for j in range(i+1, self.n)]
            selected_pair = random.choice(pairs)
            R.add(selected_pair)
            if random.choice([True, False]):
                next_element = random.choice(list(self.M - {selected_pair[1]}))
                R.add((selected_pair[0], next_element))
        return R, self.M

def dataset_creation(num_samples_per_type, relation_type):   
    dataset = []
    for _ in range(num_samples_per_type):
        n = random.randint(2, 26)
        use_letters = random.choice([True, False])

        if relation_type == "Reflexive":
            generator = ReflexiveRelationGenerator(n, use_letters)
            dataset.append((generator.generate_reflexive_set(), "Рефлексивное"))
            dataset.append((generator.generate_antireflexive_set(), "Антирефлексивное"))
            dataset.append((generator.generate_nonreflexive_set(), "Нерефлексивное"))

        elif relation_type == "Symmetric":
            generator = SymmetricRelationGenerator(n, use_letters)
            dataset.append((generator.generate_symmetric_set(), "Симметричное"))
            dataset.append((generator.generate_asymmetric_set(), "Асимметричное"))
            dataset.append((generator.generate_antisymmetric_set(), "Антисимметричное"))
            dataset.append((generator.generate_nonsymmetric_set(), "Несимметричное"))

        elif relation_type == "Transitive":
            generator = TransitiveRelationGenerator(n, use_letters)
            dataset.append((generator.generate_transitive_set(), "Транзитивное"))
            dataset.append((generator.generate_antitransitive_set(), "Антитранзитивное"))
            dataset.append((generator.generate_nontransitive_set(), "Нетранзитивное"))

        else:
            print("ERROR!!! Unidentified property of a binary relation!")

    data_as_dicts = [{
    "M": ', '.join(map(str, item[0][1])),
    "R": ', '.join(map(str, item[0][0])),
    "Type": item[1]
    } for item in dataset]

    df = pd.DataFrame(data_as_dicts)

    if relation_type == "Reflexive":
        df.to_csv("data/df_reflexive.csv", index=False)
    elif relation_type == "Symmetric":
        df.to_csv("data/df_symmetric.csv", index=False)
    elif relation_type == "Transitive":
        df.to_csv("data/df_transitive.csv", index=False)

    return df