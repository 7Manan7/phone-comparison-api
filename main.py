from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import ollama

app = FastAPI(title="Phone Comparison API")

# Initialize the Ollama client
chat_model = ollama.Client(host='http://localhost:11434')
MODEL_NAME = "gemma3:4b"


class PhoneSpec(BaseModel):
    name: str
    specs: str
    price: float


class ComparisonRequest(BaseModel):
    phones: List[PhoneSpec]
    user_question: str = "Which phone is the best value for money based on these specs?"


@app.post("/compare-phones/", summary="Compare phone specifications using LLM")
async def compare_phones(request: ComparisonRequest):
    """
    Compare multiple phones based on their specifications and price using an LLM.

    Returns a one-line comparison summary.
    """
    if len(request.phones) < 2:
        raise HTTPException(status_code=400, detail="Please provide at least 2 phones for comparison")

    # Prepare the prompt with instruction for one-line response
    prompt = f"""Compare these smartphones and answer in one concise sentence: {request.user_question}

    Phones:
    """

    for phone in request.phones:
        prompt += f"{phone.name} (${phone.price:.2f}, {phone.specs}); "

    prompt += "\nReply with just one clear comparison sentence, no explanations."

    try:
        response = chat_model.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                'temperature': 0.7,  # Lower temperature for more focused response
                'num_predict': 300  # Fewer tokens for shorter response
            }
        )

        # Extract and clean the response
        one_liner = response['response'].strip().split('\n')[0]
        return {"comparison": one_liner}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling LLM: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)