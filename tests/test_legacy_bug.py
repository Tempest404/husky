from __future__ import annotations

# Failing regression tests that capture real defects in legacy_code.
# Candidates should fix the bugs during refactor and make these pass (or replace with equivalent tests on src/).

import unittest
import math

# AI-ASSIST: Example marker to illustrate how to annotate AI-influenced code or tests.
import water_model.water_model as water_model
import water_model.config as config


class TestMixing(unittest.TestCase):
    def setUp(self):        
       self.model = water_model.WaterModel(config.CONFIG)
       
    def test_tracer_mixing_should_be_flow_weighted(self):
        # Flow-weighted mixing expected value
        q1, c1 = 1.0, 10.0
        q2, c2 = 3.0, 0.0
        expected = (q1 * c1 + q2 * c2) / (q1 + q2)  # 2.5 mg/L
    
        got = self.model.mix_concentration(q1, c1, q2, c2)
    
        # Intentional failing assertion: legacy uses simple average (5.0) which is wrong.
        assert math.isclose(got, expected, rel_tol=1e-9), (
            "Legacy tracer mixing is incorrect; should be flow-weighted mass balance"
        )


class TestUnitConversion(unittest.TestCase):
    def setUp(self):        
       self.model = water_model.WaterModel(config.CONFIG)
       
    def test_mm_day_to_m3s_conversion_on_1km2_should_be_1_m3s(self):
        # 86.4 mm/day over 1 km^2 should yield exactly 1 m^3/s
        mm_per_day = 86.4
        area_km2 = 1.0
        expected = 1.0
    
        got = self.model.mm_day_to_m3s(mm_per_day, area_km2)
    
        # Intentional failing assertion: legacy divides by area and misses /86400
        assert math.isclose(got, expected, rel_tol=1e-12), (
            "Legacy unit conversion mm/day -> m^3/s is incorrect"
        )
    
if __name__ == "__main__":
    unittest.main()
