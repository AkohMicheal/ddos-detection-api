from fastapi import APIRouter, Query, HTTPException
from app.services.simulator import TrafficSimulator
from app.services.preprocessing import TrafficPreprocessor
from app.models.gru_model import RNNModel
from app.api.endpoints.inference import predict_traffic_sequence
from app.schemas.traffic import SequenceInferenceRequest
from typing import Dict, Any, Optional

router = APIRouter()

# Global state for simulation (in-memory for demo purposes)
CURRENT_SIMULATION_STATE = "BENIGN"

@router.get("/stream")
def get_live_traffic_stream(
    state: Optional[str] = Query(None, description="BENIGN, SYN_FLOOD, DNS_REFLECTION, UDP_FLOOD"),
    model_type: str = Query("GRU", description="GRU or LSTM")
):
    """
    Returns a simulated live network traffic sequence, preprocessed and evaluated
    by the active machine learning model.
    """
    global CURRENT_SIMULATION_STATE
    
    # If state is provided in query, override. Otherwise, use global state.
    active_state = state or CURRENT_SIMULATION_STATE
    
    if active_state not in ["BENIGN", "SYN_FLOOD", "DNS_REFLECTION", "UDP_FLOOD"]:
        raise HTTPException(status_code=400, detail="Invalid simulation state")
        
    try:
        # 1. Generate simulated raw flows
        raw_sequence = TrafficSimulator.generate_sequence(state=active_state, length=15)
        
        # 2. Format request payload for model inference
        inference_request = SequenceInferenceRequest(
            sequence=raw_sequence,
            model_type=model_type
        )
        
        # 3. Call predict routine directly to run RNN inference
        prediction_result = predict_traffic_sequence(inference_request)
        
        # 4. Return combined payload
        # Convert Pydantic schemas to standard dictionaries for JSON serialization
        flows_serialized = []
        for flow in raw_sequence:
            flows_serialized.append(flow.dict(by_alias=True))
            
        return {
            "simulation_state": active_state,
            "flows": flows_serialized,
            "inference": prediction_result.dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation streaming error: {str(e)}")

@router.post("/state")
def update_simulation_state(state: str = Query(..., description="BENIGN, SYN_FLOOD, DNS_REFLECTION, UDP_FLOOD")):
    """Updates the global simulation state."""
    global CURRENT_SIMULATION_STATE
    
    if state not in ["BENIGN", "SYN_FLOOD", "DNS_REFLECTION", "UDP_FLOOD"]:
        raise HTTPException(status_code=400, detail="Invalid simulation state")
        
    CURRENT_SIMULATION_STATE = state
    return {"status": "success", "message": f"Simulation state updated to {state}"}
