from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Hackathon mock logic if no API key is set
API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_MOCK = len(API_KEY) < 5

if not USE_MOCK:
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=API_KEY)

class WasteInfo(BaseModel):
    waste_type: str = Field(description="The primary type of waste")
    quantity: float = Field(description="The numeric amount of waste")
    unit: str = Field(description="The unit of measurement (e.g. tons, kg, liters)")
    clean_description: str = Field(description="A clean, concise 1-sentence description of the waste")

def run_interpreter_agent(raw_text: str) -> dict:
    if USE_MOCK:
        return {"waste_type": "Simulated Organic Waste", "quantity": 5, "unit": "Tons", "clean_description": raw_text}
    
    parser = JsonOutputParser(pydantic_object=WasteInfo)
    prompt = PromptTemplate(
        template="Extract the waste information from the following unstructured text.\n{format_instructions}\nText: {text}",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    return chain.invoke({"text": raw_text})

def run_negotiator_agent(producer_name: str, consumer_name: str, waste_data: dict, consumer_demand: str) -> dict:
    if USE_MOCK:
        return {
            "agreement_summary": f"Transport {waste_data.get('quantity')} {waste_data.get('unit')} to {consumer_name}",
            "estimated_transport_cost": "$250",
            "timeline": "Weekly pickups starting next Monday"
        }
    
    prompt = PromptTemplate.from_template(
        """You are an autonomous AI negotiating a resource exchange.
Producer: {producer} 
Provider Offers: {quantity} {unit} of {waste_type}
Consumer: {consumer}
Consumer Demands: {demand}

Draft a realistic agreement. Output ONLY valid JSON in this exact format, with no markdown code blocks:
{{
  "agreement_summary": "A 1 sentence summary",
  "estimated_transport_cost": "A dollar amount like $500",
  "timeline": "A short timeline phrase"
}}
"""
    )
    response = llm.invoke(prompt.format(
        producer=producer_name,
        consumer=consumer_name,
        quantity=waste_data.get("quantity"),
        unit=waste_data.get("unit"),
        waste_type=waste_data.get("waste_type"),
        demand=consumer_demand
    ))
    try:
        return json.loads(response.content.replace("```json", "").replace("```", "").strip())
    except Exception:
        return {"agreement_summary": "Agreement formulation failed.", "estimated_transport_cost": "N/A", "timeline": "N/A"}

def run_evaluator_agent(producer_name: str, consumer_name: str, waste_type: str) -> str:
    if USE_MOCK:
        return f"By redirecting {waste_type} from {producer_name} to {consumer_name}, this match prevents landfill dumping and reduces heavy industrial carbon output."
        
    prompt = PromptTemplate.from_template(
        """Write a 2-sentence sustainability pitch explaining why {producer} giving their {waste_type} to {consumer} is a big win for the circular economy and reduces carbon emissions."""
    )
    response = llm.invoke(prompt.format(
        producer=producer_name, 
        consumer=consumer_name, 
        waste_type=waste_type
    ))
    return response.content
