import numpy as np
from typing import List, Dict, Any
from app.schemas.traffic import NetworkFlowFeature

class TrafficPreprocessor:
    """
    Service to handle data cleaning, normalization (Min-Max Scaling), 
    and time-series window preparation for the RNN models.
    """
    # Standard Min-Max parameters based on training statistics of the CIC-DDoS2019 dataset
    FEATURE_LIMITS = {
        "flow_duration": {"min": 0.0, "max": 10000000.0},
        "tot_fwd_pkts": {"min": 0.0, "max": 2000.0},
        "tot_bwd_pkts": {"min": 0.0, "max": 2000.0},
        "tot_len_fwd_pkts": {"min": 0.0, "max": 150000.0},
        "flow_byts_s": {"min": 0.0, "max": 50000000.0}, # 50 MB/s
        "flow_pkts_s": {"min": 0.0, "max": 250000.0},
        "fwd_pkt_len_max": {"min": 0.0, "max": 1500.0},
        "bwd_pkt_len_max": {"min": 0.0, "max": 1500.0},
        "protocol": {"min": 0.0, "max": 255.0},
        "fwd_header_len": {"min": 0.0, "max": 100000.0}
    }

    @classmethod
    def scale_value(cls, val: float, feature_name: str) -> float:
        """Applies Min-Max scaling to a single feature value."""
        limits = cls.FEATURE_LIMITS.get(feature_name, {"min": 0.0, "max": 1.0})
        f_min = limits["min"]
        f_max = limits["max"]
        
        # Avoid division by zero
        if f_max == f_min:
            return 0.0
            
        scaled = (val - f_min) / (f_max - f_min)
        return float(np.clip(scaled, 0.0, 1.0))

    @classmethod
    def preprocess_record(cls, flow: NetworkFlowFeature) -> np.ndarray:
        """Converts a single NetworkFlowFeature into a scaled 1D numpy array of length 10."""
        scaled_features = [
            cls.scale_value(flow.flow_duration, "flow_duration"),
            cls.scale_value(flow.tot_fwd_pkts, "tot_fwd_pkts"),
            cls.scale_value(flow.tot_bwd_pkts, "tot_bwd_pkts"),
            cls.scale_value(flow.tot_len_fwd_pkts, "tot_len_fwd_pkts"),
            cls.scale_value(flow.flow_byts_s, "flow_byts_s"),
            cls.scale_value(flow.flow_pkts_s, "flow_pkts_s"),
            cls.scale_value(flow.fwd_pkt_len_max, "fwd_pkt_len_max"),
            cls.scale_value(flow.bwd_pkt_len_max, "bwd_pkt_len_max"),
            cls.scale_value(flow.protocol, "protocol"),
            cls.scale_value(flow.fwd_header_len, "fwd_header_len")
        ]
        return np.array(scaled_features)

    @classmethod
    def preprocess_sequence(cls, flow_sequence: List[NetworkFlowFeature]) -> np.ndarray:
        """
        Converts a list of NetworkFlowFeatures (sequence of packets) 
        into a scaled 2D numpy matrix of shape (time_steps, 10).
        """
        matrix = []
        for flow in flow_sequence:
            matrix.append(cls.preprocess_record(flow))
        return np.array(matrix)
