import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from tqdm import tqdm

class RelationDataPreprocessing:
    TOKENIZER_PATH = 'bert-base-multilingual-cased'
    MODEL_PATH = 'bert-base-multilingual-cased'
    MAX_TOKEN_LENGTH = 512

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.tokenizer = BertTokenizer.from_pretrained(self.TOKENIZER_PATH)
        self.model = BertModel.from_pretrained(self.MODEL_PATH)

    def remove_rows_with_nan(self):
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def compute_power_of_set(self):
        self.df['Power Of Set'] = self.df['M'].apply(lambda x: len(x.split(',')))

    def compute_power_of_relation(self):
        self.df['Power Of Relation'] = self.df['R'].apply(lambda x: len([i.strip() for i in x.split('),') if i.strip()]))

    def compute_relation_dimension(self, relation_type: str):
        if relation_type == "Reflexive":
            self.df['Relation Dimension'] = self.df['R'].apply(self._get_dimension_reflexive)

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
            self.df['Symmetric Pairs Count'] = self.df['R'].apply(self._get_symmetric_count)
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
            self.df['Transitive Triples Count'] = self.df['R'].apply(self._get_transitive_count)
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
        cols = [col for col in self.df.columns if col != 'Type'] + ['Type']
        self.df = self.df[cols]

    def tokenizing_data(self):
        column_r_list = self.df['R'].astype(str).tolist()
        column_m_list = self.df['M'].astype(str).tolist()

        final_r = self._tokenize_column(column_r_list)
        final_m = self._tokenize_column(column_m_list)

        r_dim = len(final_r[0])
        m_dim = len(final_m[0])

        r_columns = [f"R_{i}" for i in range(r_dim)]
        m_columns = [f"M_{i}" for i in range(m_dim)]

        df_r = pd.DataFrame(final_r, columns=r_columns)
        df_m = pd.DataFrame(final_m, columns=m_columns)

        self.df.drop(['R', 'M'], axis=1, inplace=True)

        self.df = pd.concat([df_r, df_m, self.df], axis=1)

    def _tokenize_column(self, column_list):
        results = []
        for el in tqdm(column_list):
            inputs = self.tokenizer(el, return_tensors='pt', truncation=True, padding=True, max_length=self.MAX_TOKEN_LENGTH)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            results.append(outputs['last_hidden_state'].mean(dim=1).squeeze().numpy())
        return results

    def get_dataframe(self) -> pd.DataFrame:
        return self.df