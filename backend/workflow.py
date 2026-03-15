import json
import asyncio
from geopy.distance import geodesic
from vector_db import search_demands
from agents import run_interpreter_agent, run_negotiator_agent, run_evaluator_agent
from pydantic import BaseModel

class WorkflowOrchestrator:
    def __init__(self):
        # Stream events via Memory Queue for local fast Websockets
        self.message_queue = asyncio.Queue()
        
        with open("industries.json", "r") as f:
            self.industries = {ind["id"]: ind for ind in json.load(f)}

    async def log_thought(self, agent: str, message: str, match_data: dict = None):
        payload = {"agent": agent, "message": message}
        if match_data:
            payload["match_data"] = match_data
        await self.message_queue.put(payload)
        await asyncio.sleep(1.5) # Artificial pause so judges can read the UI log streams

    async def process_waste_event(self, producer_id: str, raw_text: str):
        producer = self.industries.get(producer_id)
        if not producer:
            await self.log_thought("System", f"Producer {producer_id} not found.")
            return

        # 1. Interpreter
        await self.log_thought("Interpreter", f"Parsing raw text: '{raw_text[:50]}...'")
        waste_data = run_interpreter_agent(raw_text)
        await self.log_thought("Interpreter", f"Extracted: {waste_data.get('quantity')} {waste_data.get('unit')} of {waste_data.get('waste_type')}")

        # 2. Matcher
        clean_desc = waste_data.get("clean_description", raw_text)
        await self.log_thought("Matcher", f"Querying Vector DB for demands matching '{clean_desc}'")
        search_res = search_demands(clean_desc, k=3)
        
        if not search_res['ids'] or len(search_res['ids'][0]) == 0:
            await self.log_thought("System", "No matches found.")
            return
            
        candidate_ids = search_res['ids'][0]
        candidate_metas = search_res['metadatas'][0]
        
        # 3. Logistics
        best_consumer = None
        best_distance = float('inf')
        
        await self.log_thought("Logistics", f"Evaluating {len(candidate_ids)} candidates geographically...")
        
        prod_coords = (producer["lat"], producer["lon"])
        for i, c_id in enumerate(candidate_ids):
            meta = candidate_metas[i]
            cons_coords = (meta["lat"], meta["lon"])
            dist = geodesic(prod_coords, cons_coords).kilometers
            
            if dist < 200 and dist < best_distance: # Max distance 200km
                best_distance = dist
                best_consumer = {"id": c_id, "name": meta["name"], "demand": meta.get("demand", ""), "lat": meta["lat"], "lon": meta["lon"]}
                
        if not best_consumer:
            await self.log_thought("Logistics", "All candidates are too far away (>200km).")
            return
            
        await self.log_thought("Logistics", f"Selected {best_consumer['name']} at {best_distance:.1f} km away.")

        # 4. Negotiator
        await self.log_thought("Negotiator", "Drafting autonomous mutual resource agreement...")
        agreement = run_negotiator_agent(producer["name"], best_consumer["name"], waste_data, best_consumer["demand"])
        await self.log_thought("Negotiator", f"Agreement drafted. Transport: {agreement.get('estimated_transport_cost', 'TBD')}")

        # 5. Evaluator
        await self.log_thought("Evaluator", "Calculating environmental impact and ESG pitch...")
        pitch = run_evaluator_agent(producer["name"], best_consumer["name"], waste_data.get("waste_type"))
        
        # 6. Save & Emit
        match_payload = {
            "producer": producer,
            "consumer": best_consumer,
            "waste": waste_data,
            "distance_km": round(best_distance, 1),
            "agreement": agreement,
            "sustainability_pitch": pitch
        }
        
        from database import SessionLocal
        from models import MatchRecord
        import json
        
        db_session = SessionLocal()
        try:
            db_match = MatchRecord(
                producer_id=producer["id"],
                producer_name=producer["name"],
                consumer_id=best_consumer["id"],
                consumer_name=best_consumer["name"],
                waste_type=waste_data.get("waste_type"),
                quantity=waste_data.get("quantity"),
                unit=waste_data.get("unit"),
                distance_km=round(best_distance, 1),
                agreement_json=json.dumps(agreement),
                sustainability_pitch=pitch
            )
            db_session.add(db_match)
            db_session.commit()
            db_session.refresh(db_match)
            await self.log_thought("System", "Match finalized.", match_data=match_payload)
        finally:
            db_session.close()
        
orchestrator = WorkflowOrchestrator()
