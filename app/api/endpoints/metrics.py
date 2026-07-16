from fastapi import APIRouter

router = APIRouter()

@router.get("/comparison")
def get_model_comparison_metrics():
    """
    Returns benchmark performance comparison metrics between GRU and LSTM
    architectures as documented in the research chapters.
    """
    return {
        "metrics": [
            {
                "name": "Accuracy",
                "GRU": 91.00,
                "LSTM": 90.00,
                "unit": "%",
                "description": "Overall ratio of correctly classified traffic flow sequences"
            },
            {
                "name": "Precision",
                "GRU": 96.00,
                "LSTM": 95.00,
                "unit": "%",
                "description": "Ratio of correctly identified DDoS attacks to all flagged sequences"
            },
            {
                "name": "Recall (Sensitivity)",
                "GRU": 90.00,
                "LSTM": 90.00,
                "unit": "%",
                "description": "Ratio of identified attacks to actual total attacks (crucial for cybersecurity)"
            },
            {
                "name": "Specificity",
                "GRU": 92.00,
                "LSTM": 91.00,
                "unit": "%",
                "description": "Ratio of correctly identified benign traffic"
            },
            {
                "name": "F1-Score",
                "GRU": 92.90,
                "LSTM": 92.43,
                "unit": "%",
                "description": "Harmonic mean of Precision and Recall"
            },
            {
                "name": "Training Time",
                "GRU": 2.8,
                "LSTM": 4.1,
                "unit": "s/epoch",
                "description": "Average computation time per training cycle on standard hardware"
            },
            {
                "name": "Inference Latency",
                "GRU": 1.8,
                "LSTM": 2.7,
                "unit": "ms",
                "description": "Average response time per network packet sequence classification"
            }
        ],
        "summary": {
            "title": "Why Gated Recurrent Unit (GRU) was Selected",
            "content": "While the standard LSTM gets matching recall (90.00%), the Gated Recurrent Unit (GRU) achieves a slightly higher overall accuracy (91.00% vs 90.00%) and contains a simplified 2-gate architecture. This yields a 31.7% reduction in training time and a 33.3% reduction in inference latency, making the GRU optimal for real-time traffic filtering in high-speed, resource-constrained network routing environments (such as SDN controllers and IoT edge nodes)."
        }
    }
