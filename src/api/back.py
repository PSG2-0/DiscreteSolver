from fastapi import FastAPI, HTTPException, Body
import requests
from fastapi.responses import StreamingResponse
import io
from decimal import Decimal, getcontext
from typing import List
from src.math_algos.binary_relation.properties_of_relation import BinaryRelation
from src.math_algos.set_theory.set_simplifier import SetSimplifier
from fastapi.responses import FileResponse
from src.math_algos.set_theory.building_diagram import VennDiagramBuilder
from src.math_algos.set_theory.calc_elements_of_set import SetCalculator
from src.math_algos.coding_encoding_algos.arithmetic_coding_encoding_algo import ProbabilityCalculating, ArithmeticCoder
from src.math_algos.coding_encoding_algos.huffman_encoding_decoding import HuffmanCoding
from src.math_algos.bulean_algebra.bulean_simplifier import LogicSimplifier
from src.math_algos.bulean_algebra.truth_table import TruthTableGenerator
from src.math_algos.binary_relation.graph_generator import BinaryRelationGraph
import matplotlib
from typing import Optional
from pydantic import BaseModel

matplotlib.use('Agg')

getcontext().prec = 500

app = FastAPI(title="DiscreteSolver API")

@app.post("/relation-properties/")
def get_relation_properties(set_of_elements: str = Body(...), binary_relation: str = Body(...)):
    try:
        relation = BinaryRelation(set_of_elements, binary_relation)
        properties_list = relation.get_properties_as_list()
        
        return {"properties": properties_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-relation-graph/")
def generate_relation_graph(set_of_elements: Optional[str] = Body(default=None), binary_relation: str = Body(...)):
    try:
        binary_relation_tuples = [tuple(int(x) for x in pair.split(',')) for pair in binary_relation.replace(" ", "").strip('()').split("),(")]

        if not set_of_elements:
            elements_set = {element for pair in binary_relation_tuples for element in pair}
        else:
            elements_set = {int(x) for x in set_of_elements.replace(" ", "").split(',')}

        graph = BinaryRelationGraph(elements_set, binary_relation_tuples)
        image_stream = graph.get_image()

        return StreamingResponse(image_stream, media_type="image/png")
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

@app.post("/venn-diagram/")
async def create_venn_diagram(expression: str = Body(...)):
    try:
        diagram_builder = VennDiagramBuilder("YOUR API KEY")
        diagram_url = diagram_builder.build_diagram(expression)
        if diagram_url.startswith("http"):
            image_response = requests.get(diagram_url)
            if image_response.status_code == 200:
                return StreamingResponse(io.BytesIO(image_response.content), media_type="image/png")
            else:
                raise HTTPException(status_code=500, detail="Error while collecting an image")
        else:
            raise HTTPException(status_code=400, detail=diagram_url)
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

        encoded_value_str = str(encoded_value)
        probabilities_str = [str(prob) for prob in probabilities]

        return {
            "encoded_value": encoded_value_str,
            "probabilities": probabilities_str,
            "alphabet": letters,
            "original_length_of_string": len(string),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/arithmetic-decode/")
def arithmetic_decode(encoded_value: str = Body(...), probabilities: List[str] = Body(...), alphabet: List[str] = Body(...), original_length_of_string: int = Body(...)):
    try:
        if len(alphabet) != len(probabilities):
            raise ValueError("Alphabet and probabilities list must be of the same length")

        encoded_value = Decimal(encoded_value)
        probabilities = [Decimal(p) for p in probabilities]

        length = len(alphabet)
        coder = ArithmeticCoder(alphabet, probabilities)
        decoded_string = coder.decode(encoded_value, original_length_of_string)

        return {"decoded_string": decoded_string}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/huffman-encode/")
def huffman_encode(string: str = Body(...)):
    try:
        huffman_coder = HuffmanCoding(string)
        encoded_string = huffman_coder.encode(string)
        alphabet_and_codes = huffman_coder.code_dict

        return {
            "encoded_string": encoded_string,
            "codes": alphabet_and_codes,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/huffman-decode/")
def huffman_decode(encoded_string: str = Body(...), codes: dict = Body(...)):
    try:
        alphabet = list(codes.keys())
        probabilities = [len(code) for code in codes.values()]
        huffman_coder = HuffmanCoding.recreate_from_alphabet_and_probabilities(alphabet, probabilities)
        decoded_string = huffman_coder.decode(encoded_string, codes)

        return {"decoded_string": decoded_string}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simplify-boolean-expression/")
def simplify_boolean_expression(expression: str = Body(...)):
    try:
        simplifier = LogicSimplifier()
        simplified_expr = simplifier.simplify_expression(expression)
        result = simplifier.reverse_transform(simplified_expr
                                              )
        return {"simplified_expression": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    
    
@app.post("/generate-truth-table/")
async def generate_truth_table_endpoint(expression: str = Body(...)):
    try:
        generator = TruthTableGenerator(expression)
        image_buffer = generator.create_truth_table_image()

        return StreamingResponse(image_buffer, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)