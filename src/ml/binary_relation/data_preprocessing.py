import pandas as pd

class RelationDataPreprocessing:

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def remove_rows_with_nan(self):
        self.dataframe.dropna(inplace=True)

    def compute_power_of_set(self):
        self.dataframe['Power Of Set'] = self.dataframe['M'].apply(lambda x: len(x.split(',')))

    def compute_power_of_relation(self):
        self.dataframe['Power Of Relation'] = self.dataframe['R'].apply(lambda x: len([i.strip() for i in x.split('),') if i.strip()]))

    def compute_relation_dimension(self, relation_type: str):
        if relation_type == "Reflexive":
            self.dataframe['Relation Dimension'] = self.dataframe['R'].apply(self._get_dimension_reflexive)

        elif relation_type not in ["Symmetric", "Transitive"]:
            print("ERROR!!! Unidentified property of a binary relation!")

    def _get_dimension_reflexive(self, s):
        if isinstance(s, str):
            pairs = eval('[' + s + ']')
            elements = {item for pair in pairs for item in pair}
            return len(elements)
        else:
            return 0

    def count_symmetric_pairs(self, relation_type: str):
        if relation_type == "Symmetric":
            self.dataframe['Symmetric Pairs Count'] = self.dataframe['R'].apply(self._get_symmetric_count)
        elif relation_type not in ["Reflexive", "Transitive"]:
            print("ERROR!!! Unidentified property of a binary relation!")

    def _get_symmetric_count(self, s):
        if isinstance(s, str):
            pairs = eval('[' + s + ']')
            count = 0
            counted_pairs = set()
            for (a, b) in pairs:
                if a != b and (b, a) in pairs and (b, a) not in counted_pairs:
                    count += 1
                    counted_pairs.add((a, b))
            return count
        else:
            return 0

    def count_transitive_pairs(self, relation_type: str):
        if relation_type == "Transitive":
            self.dataframe['Transitive Triples Count'] = self.dataframe['R'].apply(self._get_transitive_count)
        elif relation_type not in ["Reflexive", "Symmetric"]:
            print("ERROR!!! Unidentified property of a binary relation!")

    def _get_transitive_count(self, s):
        if isinstance(s, str):
            pairs = eval('[' + s + ']')
            count = 0
            for (a, b) in pairs:
                for (c, d) in pairs:
                    if b == c and (a, d) in pairs:
                        count += 1
            return count
        else:
            return 0

    def move_type_to_end(self):
        cols = [col for col in self.dataframe.columns if col != 'Type'] + ['Type']
        self.dataframe = self.dataframe[cols]

    def get_dataframe(self) -> pd.DataFrame:
        return self.dataframe
