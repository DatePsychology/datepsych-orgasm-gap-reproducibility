"""Independent arithmetic/unit sanity checks using packaged published aggregate inputs.

Run: python -m unittest test_reconstruction.py -v
"""
import csv
import math
import unittest
from pathlib import Path
from scipy.stats import chi2_contingency

ROOT = Path(__file__).resolve().parent


def load(name):
    with (ROOT/name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class AggregateArithmeticTests(unittest.TestCase):
    def test_oral_sex_contingency_and_yates(self):
        rows=load("oral_sex_counts.csv")
        table=[[int(r["ever_orgasm_yes"]),int(r["ever_orgasm_no"])] for r in rows]
        self.assertEqual(table, [[38,13],[8,11]])
        self.assertEqual(sum(map(sum, table)),70)
        self.assertAlmostEqual(38/51, .7450980392156863, places=10)
        self.assertAlmostEqual(8/19, .42105263157894735, places=10)
        chi, p, _, _ = chi2_contingency(table, correction=True)
        self.assertAlmostEqual(chi, 5.093468165298155, places=9)
        self.assertAlmostEqual(p, 0.024016116467245507, places=9)

    def test_initial_orgasm_followup(self):
        rows=load("encounter_followup_counts.csv")
        n1,d1=int(rows[0]["five_or_more_encounters_yes"]),int(rows[0]["five_or_more_encounters_no"])
        n0,d0=int(rows[1]["five_or_more_encounters_yes"]),int(rows[1]["five_or_more_encounters_no"])
        self.assertEqual((n1,d1,n0,d0),(22,11,13,24))
        rr=(n1/(n1+d1))/(n0/(n0+d0))
        odds=(n1*d0)/(n0*d1)
        self.assertAlmostEqual(rr,1.8974358974358971,places=10)
        self.assertAlmostEqual(odds,3.6923076923076925,places=10)

    def test_welch_audit(self):
        rows=load("welch_reported_inputs.csv")
        cases={"Sexual satisfaction":(3.6574050688126345,29.0872444646884),
               "Sexual regret":(4.492492796321228,36.2597664042022)}
        for row in rows:
            with self.subTest(row=row["outcome"]):
                n1,n2=int(row["assumed_n_oral_yes"]),int(row["assumed_n_oral_no"])
                s1,s2=float(row["sd_oral_yes"]),float(row["sd_oral_no"])
                m1,m2=float(row["mean_oral_yes"]),float(row["mean_oral_no"])
                x=s1*s1/n1;y=s2*s2/n2
                welch=abs(m1-m2)/math.sqrt(x+y)
                dof=(x+y)**2/((x*x)/(n1-1)+(y*y)/(n2-1))
                exp_t,exp_df=cases[row["outcome"]]
                self.assertAlmostEqual(welch,exp_t,places=9)
                self.assertAlmostEqual(dof,exp_df,places=9)

    def test_literature_r2_values(self):
        rows=load("dasilva_reported_r2.csv")
        self.assertEqual([float(r["r_squared_percent"]) for r in rows],[3.4,2.6,1.6,1.4,1.0])

    def test_hypothetical_exposure_example(self):
        self.assertAlmostEqual((1-.6**5)*100,92.224,places=9)

if __name__ == "__main__":
    unittest.main()
