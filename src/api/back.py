from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import StreamingResponse, FileResponse
from typing import List, Optional, Tuple, Set
from decimal import Decimal, getcontext
import io
import requests
import matplotlib

from src.math_algos.set_theory import SetSimplifier, VennDiagramBuilder
from src.math_algos.binary_relations import BinaryRelation, BinaryRelationGraph
from src.math_algos.bulean_algebra import LogicSimplifier, TruthTableGenerator
from src.math_algos.encoding_decoding_algos import ProbabilityCalculating, ArithmeticCoder, HuffmanCoding, FixedLengthCoding, ShennonFanoCoding

matplotlib.use('Agg')
getcontext().prec = 500
MEDIA_TYPE_PNG = "image/png"

app = FastAPI(title="DiscreteSolver API")

@app.post("/relation-properties/")
def get_relation_properties(set_of_elements: str = Body(...), binary_relation: str = Body(...)) -> dict:
    relation = BinaryRelation(set_of_elements, binary_relation)
    return {"properties": relation.get_properties_as_list()}

@app.post("/generate-relation-graph/")
def generate_relation_graph(set_of_elements: Optional[str] = Body(default=None), binary_relation: str = Body(...)) -> StreamingResponse:
    try:
        relation = BinaryRelation(set_of_elements, binary_relation)
        graph = BinaryRelationGraph(relation.elements, relation.relation_set)
        return StreamingResponse(graph.get_image(), media_type=MEDIA_TYPE_PNG)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")

@app.post("/simplify-boolean-expression/")
def simplify_boolean_expression(expression: str = Body(...)) -> dict:
    simplifier = LogicSimplifier()
    try:
        simplified_expr = simplifier.simplify_expression(expression)
        readable_expr = simplifier.reverse_transform(simplified_expr)
        return {"simplified_expression": readable_expr}
    except Exception as e:
        return {"error": f"Failed to simplify expression. Error: {str(e)}"}

@app.post("/venn-diagram/")
async def create_venn_diagram(expression: str = Body(...)) -> StreamingResponse:
    try:
        diagram_url = VennDiagramBuilder("QA7A2U-Y5YWWV97T5").build_diagram(expression)
        image_response = requests.get(diagram_url)
        if image_response.status_code == 200:
            return StreamingResponse(io.BytesIO(image_response.content), media_type=MEDIA_TYPE_PNG)
        else:
            raise HTTPException(status_code=500, detail="Error while collecting an image")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simplify-boolean-expression/")
def simplify_boolean_expression(expression: str = Body(...)) -> dict:
    simplifier = LogicSimplifier()
    simplified_expr = simplifier.simplify_expression(expression)
    return {"simplified_expression": str(simplified_expr)}

@app.post("/generate-truth-table/")
async def generate_truth_table_endpoint(expression: str = Body(...)):
    try:
        generator = TruthTableGenerator(expression)
        image_buffer = generator.create_truth_table_image()
        return StreamingResponse(image_buffer, media_type=MEDIA_TYPE_PNG)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/arithmetic-encode/")
def arithmetic_encode(string: str = Body(...)):
    try:
        probability_calculator = ProbabilityCalculating(string)
        coder = ArithmeticCoder(probability_calculator)
        encoded_value = coder.encode(string)
        letters, probabilities = probability_calculator.get_probabilities()
        return {
            "encoded_value": str(encoded_value),
            "probabilities": [str(prob) for prob in probabilities],
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

        decimal_probabilities = [Decimal(p) for p in probabilities]
        probability_calculator = create_probability_calculator_from_data(alphabet, decimal_probabilities)

        coder = ArithmeticCoder(probability_calculator)
        decoded_string = coder.decode(Decimal(encoded_value), original_length_of_string)
        return {"decoded_string": decoded_string}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
def create_probability_calculator_from_data(alphabet: List[str], probabilities: List[Decimal]) -> ProbabilityCalculating:
    probability_calculator = ProbabilityCalculating('')
    probability_calculator.letter_counts = {letter: count for letter, count in zip(alphabet, probabilities)}
    probability_calculator.total_letters = sum(probabilities)
    return probability_calculator

@app.post("/huffman-encode/")
def huffman_encode(string: str = Body(...)):
    try:
        probability_calculator = ProbabilityCalculating(string)
        huffman_coder = HuffmanCoding(probability_calculator)
        encoded_string = huffman_coder.encode(string)
        return {"encoded_string": encoded_string, "codes": huffman_coder.code_dict}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/huffman-decode/")
def huffman_decode(encoded_string: str = Body(...), codes: dict = Body(...)):
    try:
        huffman_coder = HuffmanCoding(ProbabilityCalculating(encoded_string))
        decoded_string = huffman_coder.decode(encoded_string, codes)
        return {"decoded_string": decoded_string}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))  

@app.post("/fixed_length-encode/")
def fixed_length_encode(string: str = Body(...)):
    try:
        coder = FixedLengthCoding(string)
        encoded_string, alphabet_dict = coder.encode()
        return {"encoded_string": encoded_string, "alphabet": alphabet_dict}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/fixed_length-decode/")
def fixed_length_decode(encoded_string: str = Body(...), alphabet: dict = Body(...)):
    try:
        coder = FixedLengthCoding.from_alphabet(alphabet)
        return {"decoded_string": coder.decode(encoded_string)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/shennon_fano_encode/")
def shennon_fano_encode(string: str = Body(...)):
    try:
        coder = ShennonFanoCoding(ProbabilityCalculating(string))
        encoded_string = coder.encode(string)
        return {"encoded_string": encoded_string, "codes": coder.code_dict}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/shennon_fano_decode/")
def shennon_fano_decode(encoded_string: str = Body(...), codes: dict = Body(...)):
    try:
        coder = ShennonFanoCoding.recreate_from_codes(codes)
        decoded_string = coder.decode(encoded_string)
        return {"decoded_string": decoded_string}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)