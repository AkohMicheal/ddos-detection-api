from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class NetworkFlowFeature(BaseModel):
    flow_duration: float = Field(..., alias="Flow Duration", description="Duration of the flow in microseconds")
    tot_fwd_pkts: float = Field(..., alias="Tot Fwd Pkts", description="Total packets in the forward direction")
    tot_bwd_pkts: float = Field(..., alias="Tot Bwd Pkts", description="Total packets in the backward direction")
    tot_len_fwd_pkts: float = Field(..., alias="TotLen Fwd Pkts", description="Total size of packets in forward direction")
    flow_byts_s: float = Field(..., alias="Flow Byts/s", description="Flow bytes per second")
    flow_pkts_s: float = Field(..., alias="Flow Pkts/s", description="Flow packets per second")
    fwd_pkt_len_max: float = Field(..., alias="Fwd Pkt Len Max", description="Maximum size of packet in forward direction")
    bwd_pkt_len_max: float = Field(..., alias="Bwd Pkt Len Max", description="Maximum size of packet in backward direction")
    protocol: int = Field(..., alias="Protocol", description="Transmission protocol (e.g. 6 for TCP, 17 for UDP)")
    fwd_header_len: float = Field(..., alias="Fwd Header Len", description="Total header length in forward direction")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "Flow Duration": 120530,
                "Tot Fwd Pkts": 4,
                "Tot Bwd Pkts": 2,
                "TotLen Fwd Pkts": 180,
                "Flow Byts/s": 1493.40,
                "Flow Pkts/s": 49.78,
                "Fwd Pkt Len Max": 45,
                "Bwd Pkt Len Max": 90,
                "Protocol": 6,
                "Fwd Header Len": 80
            }
        }

class SequenceInferenceRequest(BaseModel):
    sequence: List[NetworkFlowFeature] = Field(..., description="Sequence of network packet flows of length T")
    model_type: Optional[str] = Field("GRU", description="Model architecture to use: GRU or LSTM")

class InferenceResponse(BaseModel):
    is_anomaly: bool = Field(..., description="Boolean indicating if DDoS attack is detected")
    probability: float = Field(..., description="DDoS probability score between 0 and 1")
    confidence_level: str = Field(..., description="Text description of confidence: High, Medium, Low")
    model_used: str = Field(..., description="GRU or LSTM")
    gate_history: List[Dict[str, Any]] = Field(..., description="Internal gate state history for step-by-step visualizers")
    attack_type: Optional[str] = Field(None, description="Detailed DDoS vector type if malicious (e.g. DNS, SYN, UDP)")
