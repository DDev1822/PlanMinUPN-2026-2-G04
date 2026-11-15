"""Controles independientes de balances y manifiestos para el producto del grupo."""
from collections import Counter
import csv
import json
import math
from pathlib import Path
import unittest

from src.missions.products import product_status

ROOT = Path(__file__).resolve().parents[1]
GROUP = json.loads((ROOT / "kai/config_teoria_v2.json").read_text(encoding="utf-8"))["grupo"]


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def num(row, key):
    return float(row[key]) if row[key] != "" else None


class GroupProductTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        status = product_status(ROOT)
        if any(status[s]["status"] != "VALIDATED" for s in ("S11", "S12")):
            raise AssertionError(f"Generaciones no vigentes: {status}")
        pointer = json.loads((ROOT / "outputs" / f"{GROUP.lower()}_products.json").read_text())
        cls.folders = {s: (ROOT / pointer[s]["manifest"]).parent for s in ("S11", "S12")}
        cls.s11 = rows(cls.folders["S11"] / "block_model_s11.csv")
        cls.s12 = rows(cls.folders["S12"] / "block_model_s12.csv")
        cls.links = rows(cls.folders["S12"] / "block_scenario_s12.csv")
        cls.summary11 = json.loads((cls.folders["S11"] / "s11_summary.json").read_text())
        cls.summary12 = json.loads((cls.folders["S12"] / "s12_summary.json").read_text())

    def test_identity_and_lineage(self):
        self.assertEqual(self.summary12["s11_run_id"], self.summary11["run_id"])
        self.assertEqual(self.summary11["total_blocks"], len(self.s11))
        self.assertEqual(self.summary12["total_blocks"], len(self.s12))
        ids11 = [r["block_id"] for r in self.s11]
        ids12 = [r["block_id"] for r in self.s12]
        self.assertEqual(ids11, ids12)
        self.assertEqual(len(ids11), len(set(ids11)))
        self.assertTrue(all(i.startswith(GROUP + "-") for i in ids11))

    def test_volume_density_tonnage_balance(self):
        for row in self.s11:
            volume = num(row, "rock_volume_m3")
            density = num(row, "density_t_m3_est")
            tonnage = num(row, "tonnage_t")
            full = num(row, "cell_volume_m3")
            self.assertIsNotNone(full)
            if volume is not None:
                self.assertGreaterEqual(volume, 0)
                self.assertLessEqual(volume, full + 1e-5)
            if tonnage is not None:
                self.assertIsNotNone(volume)
                self.assertIsNotNone(density)
                self.assertTrue(math.isclose(tonnage, volume * density, rel_tol=1e-10, abs_tol=1e-5))
            if row["topo_status"] == "AIR":
                self.assertIsNone(tonnage)
        reported = self.summary11["quantified_tonnage_t"]
        self.assertTrue(math.isclose(reported, math.fsum(num(r,"tonnage_t") or 0 for r in self.s11), rel_tol=1e-10))

    def test_candidate_inventory(self):
        counts = Counter(r["candidate_class"] for r in self.s12)
        self.assertEqual(counts, self.summary12["candidate_counts"])
        for category, key in (("ORE_CANDIDATE", "ore_inventory_t"), ("WASTE_CANDIDATE", "waste_inventory_t")):
            actual = math.fsum(num(r,"tonnage_t") or 0 for r in self.s12 if r["candidate_class"] == category)
            self.assertTrue(math.isclose(actual, self.summary12[key], rel_tol=1e-10, abs_tol=1e-5))
        self.assertTrue(all(r["reserve_classification"] == "NOT_ASSIGNED" for r in self.s12))

    def test_scenarios_and_links(self):
        self.assertEqual(len(self.links), 2 * len(self.s12))
        self.assertEqual({r["scenario"] for r in self.links}, {"A", "B"})
        for scenario in ("A", "B"):
            data = self.summary12["scenario_" + scenario]
            links = [r for r in self.links if r["scenario"] == scenario]
            moved = math.fsum(num(r,"allocated_moved_t") or 0 for r in links)
            processed = math.fsum(num(r,"allocated_processed_t") or 0 for r in links)
            opex = math.fsum(num(r,"total_opex_usd") or 0 for r in links)
            self.assertTrue(math.isclose(moved, data["moved_t_period"], rel_tol=1e-9, abs_tol=1e-4))
            self.assertTrue(math.isclose(processed, data["ore_allocated_t_period"], rel_tol=1e-9, abs_tol=1e-4))
            self.assertTrue(math.isclose(opex, data["opex_usd_period"], rel_tol=1e-9, abs_tol=1e-3))
            self.assertGreater(data["trucks_for_target"], 0)


if __name__ == "__main__":
    unittest.main()
