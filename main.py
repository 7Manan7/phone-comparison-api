from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import ollama
from starlette.responses import FileResponse

from phone_database import PHONE_DATABASE  # Import from the separate file

app = FastAPI(title="Phone Comparison API")

# Initialize the Ollama client
chat_model = ollama.Client(host='http://localhost:11434')
MODEL_NAME = "gemma3:4b"


class PhoneSpec(BaseModel):
    name: str
    specs: Optional[str] = None
    price: Optional[float] = None


class ComparisonRequest(BaseModel):
    phones: List[PhoneSpec]
    user_question: str = "Which phone is the best value for money based on these specs?"


def get_phone_details(phone_name: str) -> PhoneSpec:
    """Get phone details from database if they exist"""
    phone_name_lower = phone_name.lower()
    for name, details in PHONE_DATABASE.items():
        if name.lower() == phone_name_lower:
            return PhoneSpec(name=name, specs=details["specs"], price=details["price"])
    return None


@app.get("/")
async def serve_html():
    return FileResponse("smarthphone_home.html")


@app.post("/compare-phones/", summary="Compare phone specifications using LLM")
async def compare_phones(request: ComparisonRequest):
    """
    Compare multiple phones based on their specifications and price using an LLM.
    If specs or price are missing, tries to find them in the internal database.

    Returns a one-line comparison summary.
    """
    if len(request.phones) < 2:
        raise HTTPException(status_code=400, detail="Please provide at least 2 phones for comparison")

    # Complete missing information from database
    completed_phones = []
    for phone in request.phones:
        if phone.specs is None or phone.price is None:
            db_phone = get_phone_details(phone.name)
            if db_phone:
                # Use provided details where available, fall back to database
                completed_phones.append(PhoneSpec(
                    name=phone.name,
                    specs=phone.specs if phone.specs else db_phone.specs,
                    price=phone.price if phone.price is not None else db_phone.price
                ))
            else:
                # If we can't find the phone and details are missing
                missing_fields = []
                if phone.specs is None:
                    missing_fields.append("specs")
                if phone.price is None:
                    missing_fields.append("price")
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing {', '.join(missing_fields)} for {phone.name} and not found in database"
                )
        else:
            completed_phones.append(phone)

    # Prepare the prompt with instruction for one-line response
    prompt = f"""Compare these smartphones and answer in one concise sentence: {request.user_question}

    Phones:
    """

    for phone in completed_phones:
        prompt += f"{phone.name} (${phone.price:.2f}, {phone.specs}); "

    prompt += "\nReply with just one clear comparison sentence, no explanations."

    try:
        response = chat_model.generate(
            model=MODEL_NAME,
            prompt=prompt,
            options={
                'temperature': 0.7,
                'num_predict': 300
            }
        )

        # Extract and clean the response
        one_liner = response['response'].strip().split('\n')[0]
        return {
            "comparison": one_liner,
            "phones_used": [phone.dict() for phone in completed_phones]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling LLM: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
