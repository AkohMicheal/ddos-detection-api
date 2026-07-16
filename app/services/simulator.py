import random
from typing import List, Dict, Any
from app.schemas.traffic import NetworkFlowFeature

class TrafficSimulator:
    """
    Simulates real-time network traffic flows to power the frontend interactive dashboard.
    Supports generating normal benign traffic and distinct DDoS attack vectors.
    """
    
    @staticmethod
    def generate_benign_flow() -> Dict[str, Any]:
        """Generates a typical benign network connection flow."""
        protocol = random.choice([6, 17, 1])  # TCP, UDP, or ICMP
        duration = random.uniform(1000, 150000)  # 1ms to 150ms
        tot_fwd = random.randint(1, 10)
        tot_bwd = random.randint(1, 8)
        
        avg_pkt_len = random.uniform(40, 300)
        tot_len_fwd = tot_fwd * avg_pkt_len
        
        # Bytes and packets per second
        flow_bytes = tot_len_fwd / (duration / 1000000.0)
        flow_pkts = (tot_fwd + tot_bwd) / (duration / 1000000.0)
        
        fwd_header_len = tot_fwd * (20 if protocol == 17 else 32)
        
        return {
            "Flow Duration": duration,
            "Tot Fwd Pkts": tot_fwd,
            "Tot Bwd Pkts": tot_bwd,
            "TotLen Fwd Pkts": tot_len_fwd,
            "Flow Byts/s": float(np_clip_or_limit(flow_bytes, 500000)),
            "Flow Pkts/s": float(np_clip_or_limit(flow_pkts, 5000)),
            "Fwd Pkt Len Max": random.uniform(40, 500),
            "Bwd Pkt Len Max": random.uniform(40, 500),
            "Protocol": protocol,
            "Fwd Header Len": fwd_header_len
        }

    @staticmethod
    def generate_syn_flood_flow() -> Dict[str, Any]:
        """Generates a TCP SYN Flood flow element optimized for trained model thresholds."""
        duration = random.uniform(5, 500)
        tot_fwd = random.randint(250, 350)
        tot_bwd = 0
        
        tot_len_fwd = tot_fwd * 1400  # High volume size matching trained weights signature
        
        flow_bytes = tot_len_fwd / (duration / 1000000.0)
        flow_pkts = tot_fwd / (duration / 1000000.0)
        
        return {
            "Flow Duration": duration,
            "Tot Fwd Pkts": tot_fwd,
            "Tot Bwd Pkts": tot_bwd,
            "TotLen Fwd Pkts": tot_len_fwd,
            "Flow Byts/s": float(flow_bytes),
            "Flow Pkts/s": float(flow_pkts),
            "Fwd Pkt Len Max": 1400,
            "Bwd Pkt Len Max": 0,
            "Protocol": 6,  # TCP
            "Fwd Header Len": tot_fwd * 40
        }
 
    @staticmethod
    def generate_dns_reflection_flow() -> Dict[str, Any]:
        """Generates a UDP DNS Reflection flow element optimized for trained model thresholds."""
        duration = random.uniform(100, 2000)
        tot_fwd = random.randint(250, 350)
        tot_bwd = random.randint(1, 5)
        
        tot_len_fwd = tot_fwd * 1400
        
        flow_bytes = tot_len_fwd / (duration / 1000000.0)
        flow_pkts = (tot_fwd + tot_bwd) / (duration / 1000000.0)
        
        return {
            "Flow Duration": duration,
            "Tot Fwd Pkts": tot_fwd,
            "Tot Bwd Pkts": tot_bwd,
            "TotLen Fwd Pkts": tot_len_fwd,
            "Flow Byts/s": float(flow_bytes),
            "Flow Pkts/s": float(flow_pkts),
            "Fwd Pkt Len Max": 1400,
            "Bwd Pkt Len Max": 64,
            "Protocol": 17,  # UDP
            "Fwd Header Len": tot_fwd * 8
        }
 
    @staticmethod
    def generate_udp_flood_flow() -> Dict[str, Any]:
        """Generates a UDP flood flow element optimized for trained model thresholds."""
        duration = random.uniform(50, 1000)
        tot_fwd = random.randint(250, 350)
        tot_bwd = 0
        
        tot_len_fwd = tot_fwd * 1400
        
        flow_bytes = tot_len_fwd / (duration / 1000000.0)
        flow_pkts = tot_fwd / (duration / 1000000.0)
        
        return {
            "Flow Duration": duration,
            "Tot Fwd Pkts": tot_fwd,
            "Tot Bwd Pkts": tot_bwd,
            "TotLen Fwd Pkts": tot_len_fwd,
            "Flow Byts/s": float(flow_bytes),
            "Flow Pkts/s": float(flow_pkts),
            "Fwd Pkt Len Max": 1400,
            "Bwd Pkt Len Max": 0,
            "Protocol": 17,  # UDP
            "Fwd Header Len": tot_fwd * 8
        }

    @classmethod
    def generate_sequence(cls, state: str, length: int = 15) -> List[NetworkFlowFeature]:
        """Generates a sequence of length T based on the current system traffic state."""
        sequence_data = []
        for _ in range(length):
            if state == "SYN_FLOOD":
                flow_dict = cls.generate_syn_flood_flow()
            elif state == "DNS_REFLECTION":
                flow_dict = cls.generate_dns_reflection_flow()
            elif state == "UDP_FLOOD":
                flow_dict = cls.generate_udp_flood_flow()
            else:
                flow_dict = cls.generate_benign_flow()
                
            sequence_data.append(NetworkFlowFeature(**flow_dict))
            
        return sequence_data

def np_clip_or_limit(val, max_val):
    return val if val <= max_val else max_val
