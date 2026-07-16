from fastapi import APIRouter, HTTPException
from app.schemas.traffic import SequenceInferenceRequest, InferenceResponse
from app.services.preprocessing import TrafficPreprocessor
from app.models.gru_model import RNNModel
from typing import Optional

router = APIRouter()

@router.post("/predict", response_model=InferenceResponse)
def predict_traffic_sequence(request: SequenceInferenceRequest):
    """
    Analyzes a sequence of network flows to detect volumetric DDoS anomalies.
    Expects a sequence of length T (usually 10-20 flows).
    """
    sequence = request.sequence
    model_type = request.model_type or "GRU"
    
    if len(sequence) == 0:
        raise HTTPException(status_code=400, detail="Sequence cannot be empty")
        
    if model_type not in ["GRU", "LSTM"]:
        raise HTTPException(status_code=400, detail="Invalid model type. Choose 'GRU' or 'LSTM'")
        
    try:
        # 1. Preprocess & Scale features to [0, 1] range
        scaled_matrix = TrafficPreprocessor.preprocess_sequence(sequence)
        
        # 2. Instantiate and execute the RNN forward pass
        model = RNNModel(model_type=model_type, input_dim=10, hidden_dim=32)
        probability, detail_dict = model.forward(scaled_matrix)
        
        # 3. Determine classification threshold (0.5)
        is_anomaly = probability >= 0.5
        
        # 4. Determine confidence level text
        if probability >= 0.85 or probability <= 0.15:
            confidence = "High"
        elif probability >= 0.65 or probability <= 0.35:
            confidence = "Medium"
        else:
            confidence = "Low"
            
        # 5. Extract attack vector type if malicious
        attack_type = None
        if is_anomaly:
            # Check protocol and length to classify the simulated vector
            mean_protocol = sum(p.protocol for p in sequence) / len(sequence)
            mean_bytes = sum(p.flow_byts_s for p in sequence) / len(sequence)
            mean_fwd_pkts = sum(p.tot_fwd_pkts for p in sequence) / len(sequence)
            
            if mean_protocol > 15 and mean_bytes > 20000000:
                attack_type = "UDP Flood"
            elif mean_protocol > 15:
                attack_type = "DNS Reflection"
            elif mean_protocol < 10 and mean_fwd_pkts > 50:
                attack_type = "SYN Flood"
            else:
                attack_type = "Generic volumetric DDoS"

        return InferenceResponse(
            is_anomaly=is_anomaly,
            probability=probability,
            confidence_level=confidence,
            model_used=model_type,
            gate_history=detail_dict["gate_history"],
            attack_type=attack_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
