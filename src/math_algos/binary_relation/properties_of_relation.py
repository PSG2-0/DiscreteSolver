class BinaryRelation:
    def __init__(self, set_of_elements=None, binary_relation=None):
        self.relation_set = self._create_relation_set(binary_relation)
        self.elements = self._create_set_of_elements(set_of_elements, binary_relation)
        print("relation_set:", self.relation_set)
        print("elements:", self.elements)

    def _create_set_of_elements(self, set_of_elements, binary_relation):
        if set_of_elements:
            elements = set_of_elements.replace(" ", "").split(',')
            return set(self._convert_to_number(e) for e in elements)
        else:
            return set(self._convert_to_number(x) for pair in self.relation_set for x in pair)

    def _convert_to_number(self, element):
        try:
            return int(element)
        except ValueError:
            return element


    def _create_relation_set(self, binary_relation):
        if isinstance(binary_relation, str):
            binary_relation = binary_relation.replace(" ", "")
            binary_relation = binary_relation.strip('()')
            binary_relation_list = binary_relation.split("),(")
            relation_set = set()
            for pair in binary_relation_list:
                elements = pair.split(',')
                try:
                    el1, el2 = int(elements[0]), int(elements[1])
                except ValueError:
                    el1, el2 = elements[0], elements[1]
                relation_set.add((el1, el2))
            return relation_set
        elif binary_relation:
            return set(binary_relation)
        else:
            return set()

    def check_reflexive_property(self):
        is_reflexive = all((e, e) in self.relation_set for e in self.elements)
        is_antireflexive = all((e, e) not in self.relation_set for e in self.elements)
        is_nonreflexive = not is_reflexive and not is_antireflexive

        return {
            "Рефлексивно": is_reflexive,
            "Антирефлексивно": is_antireflexive,
            "Нерефлексивно": is_nonreflexive
        }

    def check_symmetry_properties(self):
        is_symmetric = all((b, a) in self.relation_set for a, b in self.relation_set)
        is_asymmetric = all((b, a) not in self.relation_set for a, b in self.relation_set) and not is_symmetric
        is_antisymmetric = all((b, a) not in self.relation_set or a == b for a, b in self.relation_set) and not is_asymmetric
        is_nonsymmetric = not is_symmetric and not is_asymmetric and any((b, a) in self.relation_set for a, b in self.relation_set if a != b)

        return {
            "Симметрично": is_symmetric,
            "Асимметрично": is_asymmetric,
            "Антисимметрично": is_antisymmetric,
            "Несимметрично": is_nonsymmetric
        }
    
    def check_transitivity_properties(self):
        is_transitive = True
        for a, b in self.relation_set:
            for c, d in self.relation_set:
                if b == c and (a, d) not in self.relation_set:
                    is_transitive = False
                    break

        is_antitransitive = not is_transitive and all((a, c) not in self.relation_set
                                                    for a, b in self.relation_set
                                                    for c, d in self.relation_set
                                                    if b == c and a != d)

        is_nontransitive = not is_transitive and not is_antitransitive

        return {
            "Транзитивно": is_transitive,
            "Антитранзитивно": is_antitransitive,
            "Нетранзитивно": is_nontransitive
        }

    def get_properties_as_list(self):
        properties_list = []
        reflexive_properties = self.check_reflexive_property()
        symmetry_properties = self.check_symmetry_properties()
        transitive_properties = self.check_transitivity_properties()

        for property_name, is_true in reflexive_properties.items():
            if is_true:
                properties_list.append(property_name)
        
        print(symmetry_properties)
        if symmetry_properties["Антисимметрично"]:
            properties_list.append("Антисимметрично")
        else:
            if symmetry_properties["Симметрично"]:
                properties_list.append("Симметрично")
            elif symmetry_properties["Асимметрично"]:
                properties_list.append("Асимметрично")
            if symmetry_properties["Несимметрично"]:
                properties_list.append("Несимметрично")
                
        for property_name, is_true in transitive_properties.items():
            if is_true:
                properties_list.append(property_name)
        
        return properties_list