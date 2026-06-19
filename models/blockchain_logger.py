import hashlib
import json
import pandas as pd
from datetime import datetime


class Block:
    """A single record in the allocation audit chain."""

    def __init__(self, index, data, previous_hash):
        self.index         = index
        self.timestamp     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data          = data
        self.previous_hash = previous_hash
        self.hash          = self._hash()

    def _hash(self):
        content = json.dumps({
            "index"        : self.index,
            "timestamp"    : self.timestamp,
            "data"         : self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def __repr__(self):
        return (f"Block({self.index}) | "
                f"Hash: {self.hash[:12]}... | "
                f"Prev: {self.previous_hash[:12]}...")


class AllocationChain:
    """
    Blockchain that logs every cloud allocation decision.
    
    Why blockchain here?
    - Cloud providers bill based on allocation logs
    - Tamper-proof logs = dispute resolution between 
      provider and customer
    - Auditors can verify every scaling decision made
    """

    def __init__(self):
        genesis = Block(0, {
            "event"  : "CloudSim IQ Genesis Block",
            "system" : "Initialized"
        }, "0" * 64)
        self.chain = [genesis]
        print("[Blockchain] Chain initialized with genesis block")

    def add(self, hour, actual, predicted, allocation):
        """Log one hour's allocation decision as a new block."""
        data = {
            "simulation_hour"  : int(hour),
            "actual_demand"    : int(actual),
            "predicted_demand" : round(float(predicted), 2),
            "prediction_error" : round(abs(float(actual)
                                   - float(predicted)), 2),
            "cpu_allocated"    : allocation["cpu"],
            "ram_allocated_gb" : allocation["ram"],
            "throughput"       : allocation["throughput"],
            "cost_usd"         : allocation["cost_usd"],
            "efficiency_score" : allocation["efficiency"]
        }
        block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=self.chain[-1].hash
        )
        self.chain.append(block)
        return block

    def is_valid(self):
        """Verify entire chain hasn't been tampered with."""
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr._hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

    def audit_report(self):
        """Export full audit trail as DataFrame."""
        rows = []
        for block in self.chain[1:]:
            rows.append({
                **block.data,
                "block_hash": block.hash[:16] + "..."
            })
        df = pd.DataFrame(rows)
        df.to_csv("data/blockchain_audit.csv", index=False)
        return df

    def tamper_demo(self):
        """
        Demonstrates blockchain security.
        Tries to alter block 2 and shows chain breaks.
        """
        print("\n[Blockchain] ⚠️  Tampering simulation...")
        print(f"  Chain valid BEFORE tamper: {self.is_valid()}")
        original = self.chain[2].data.copy()
        self.chain[2].data["cost_usd"] = 0.0001  # fake cheap cost
        print(f"  Chain valid AFTER tamper : {self.is_valid()}")
        self.chain[2].data = original             # restore
        print(f"  Chain valid AFTER restore: {self.is_valid()}")