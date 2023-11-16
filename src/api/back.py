from fastapi import FastAPI, HTTPException, Body
from typing import List
from src.math_algos.binary_relation.properties_of_relation import BinaryRelation
from src.math_algos.set_theory.set_simplifier import SetSimplifier
from src.math_algos.set_theory.calc_elements_of_set import SetCalculator
from src.math_algos.coding_encoding_algos.arithmetic_coding_encoding_algo import ProbabilityCalculating, ArithmeticCoder

app = FastAPI(title="DiscreteSolver API")

@app.post("/relation-properties/")
def get_relation_properties(set_of_elements: str = Body(...), binary_relation: str = Body(...)):
    try:
        relation = BinaryRelation(set_of_elements, binary_relation)
        properties_list = relation.get_properties_as_list()
        return {"properties": properties_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simplify-set/")
def simplify_set(expression: str = Body(...)):
    try:
        simplifier = SetSimplifier()
        simplified_expr = simplifier.simplify_expression(expression)
        result = simplifier.reverse_transform(simplified_expr)
        return {"simplified_expression": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/calculate-set/")
def calculate_elements_of_set(expression: str = Body(...), variable_values: str = Body(...)):
    try:
        calculator = SetCalculator()
        calculator.parse_variable_values(variable_values)
        result_set = calculator.calculate(expression)
        return {"result_set": result_set}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/arithmetic-encode/")
def arithmetic_encode(string: str = Body(...)):
    try:
        probability_calculator = ProbabilityCalculating(string)
        letters, probabilities = probability_calculator.get_probabilities()
        coder = ArithmeticCoder(letters, probabilities)
        encoded_value = coder.encode(string)
        return {
            "encoded_value": encoded_value,
            "alphabet": letters,
            "probabilities": probabilities
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/arithmetic-decode/")
def arithmetic_decode(encoded_value: float = Body(...), probabilities: List[float] = Body(...), alphabet: List[str] = Body(...), original_length_of_string: int = Body(...)):
    try:
        if len(alphabet) != len(probabilities):
            raise ValueError("Alphabet and probabilities list must be of the same length")

        length = len(alphabet)
        coder = ArithmeticCoder(alphabet, probabilities)
        decoded_string = coder.decode(encoded_value, original_length_of_string)
        return {"decoded_string": decoded_string}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)