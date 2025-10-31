# Monolithic legacy script mixing I/O, globals, and computations.
# HINTS: globals, inconsistent naming, hard-coded paths, mixed responsibilities.

from __future__ import annotations

import math
from typing import Any, Dict, List

from .config import CONFIG
from .utils import parse_date, read_csv_as_dicts

# Mutable global state — smell
STATE: Dict[str, Any] = {
    "last_q": 0.0,
    "rows": [],
}


class WaterModel:
    def __init__(self, config: CONFIG):
        # Model parameters:
        self.beta: float = CONFIG.get("beta", 0.9)
        self.fpath = CONFIG.get("paths", {}).get("forcing") or "data/forcing.csv"
        self.rpath = CONFIG.get("paths", {}).get("reaches") or "data/reaches.csv"
        
        # Model input:
        self.dataset_forcing: dict = read_csv_as_dicts(self.fpath)
        self.dataset_reaches: dict = read_csv_as_dicts(self.rpath)
        
        # Model output:
        self.results: List[Dict[str, Any]] = []


    def run(self):
        if len(self.dataset_reaches) < 2:
            raise RuntimeError("need at least 2 reaches A and B")
    
        # Assume reaches sorted A then B
        A = self.dataset_reaches[0]
        B = self.dataset_reaches[1]
    
        A_area = float(A.get("area_km2", "0"))
        B_area = float(B.get("area_km2", "0"))
    
        C_A = float(A.get("tracer_init_mgL", "0"))
        C_B = float(B.get("tracer_init_mgL", "0"))
    
        last_qA = 0.0
        last_qB = 0.0
    
        for row in self.dataset_forcing:
            
            # TODO: log the bad date format
            try:
                d = parse_date(row.get("date", "1970-01-01"))
            except Exception:
                # ignore bad dates silently — smell
                continue
            P = float(row.get("precip_mm", "0"))
            ET = float(row.get("et_mm", "0"))
            upstream_c = float(row.get("tracer_upstream_mgL", "0"))
    
            runoff_mm_A = max(P - ET, 0.0) + self.beta * 0.0  # baseflow rolled into beta (unclear)
            runoff_mm_B = max(P - ET, 0.0) + self.beta * 0.0
    
            # BUG: wrong conversion
            qA_local = self.mm_day_to_m3s_bad(runoff_mm_A, A_area)
            qB_local = self.mm_day_to_m3s_bad(runoff_mm_B, B_area)
    
            # Reach A total discharge (no routing)
            qA = qA_local + last_qA * 0.0  # pointless last_qA (dead state)
    
            # Mix tracer in A: upstream boundary and local input
            # BUG: wrong mixing formula
            C_A = self.mix_concentration_bad(q1=1.0, c1=upstream_c, q2=qA_local, c2=C_A)
    
            self.results.append({
                "date": d.isoformat(), "reach": "A", "q_m3s": qA, "c_mgL": C_A
            })
    
            # Reach B receives Q from A and its own local input
            qB = qB_local + qA
    
            # BUG: wrong mixing (again)
            C_B = self.mix_concentration_bad(q1=qA, c1=C_A, q2=qB_local, c2=C_B)
    
            self.results.append({
                "date": d.isoformat(), "reach": "B", "q_m3s": qB, "c_mgL": C_B
            })
    
            last_qA = qA
            last_qB = qB

        STATE["rows"] = self.results
        return self.results

    def mm_day_to_m3s_bad(self, mm_per_day: float, area_km2: float) -> float:
        """WRONG conversion (intentional bug): divides by area instead of multiplying
        and forgets factor 86400.
        Correct would be: (mm/1000) * (area_km2*1e6) / 86400
        """
        if area_km2 == 0:
            return 0.0
        try:
            # wrong: divide by area and no /86400
            return (mm_per_day / 1000.0) / (area_km2 * 1_000_000.0)
        except Exception:
            return 0.0


    def mix_concentration_bad(self, q1: float, c1: float, q2: float, c2: float) -> float:
        """WRONG mixing (intentional bug): simple average ignoring flows.
        Correct should be flow-weighted: (q1*c1 + q2*c2)/(q1+q2) when q1+q2>0.
        """
        try:
            return (c1 + c2) / 2.0
        except Exception:
            return float("nan")


def write_output_csv(path: str) -> None:
    import csv

    rows = STATE.get("rows") or []
    fieldnames = ["date", "reach", "q_m3s", "c_mgL"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    # Hard-coded default path — smell
    out = CONFIG.get("paths", {}).get("output", "legacy_results.csv")
    
    water_model = WaterModel(CONFIG)
    
    rows = water_model.run()
    write_output_csv(out)
    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
