import json
import unittest
from pathlib import Path
from analyzer import sanitize, compare
ROOT = Path(__file__).resolve().parent.parent

class BidMirrorTests(unittest.TestCase):
    def get_fixtures(self):
        d = json.loads((ROOT/'fixtures/demo_extracts.json').read_text())
        return sanitize(d['a'], (ROOT/'fixtures/quote_a.txt').read_text()), sanitize(d['b'], (ROOT/'fixtures/quote_b.txt').read_text())

    def test_demo_evidence_grounded(self):
        a,b=self.get_fixtures()
        self.assertEqual(len(a['items']), 4)
        self.assertEqual(len(b['items']), 4)
        self.assertEqual(len(b['exclusions']),2)

    def test_comparison_reports_warranty_missing_not_excluded(self):
        a,b=self.get_fixtures()
        z=compare(a,b)
        self.assertEqual(len(z['matched']),4)
        self.assertTrue(any('warranty' in q.lower() for q in z['questions']))
        self.assertFalse(any('warranty' in e['text'] for e in b['exclusions']))

    def test_hallucinated_evidence_filtered(self):
        z=sanitize({'items':[{'name':'Imaginary work','amount':5000,'evidence':'This never appears.'}],
                    'exclusions':[{'text':'secret item','evidence':'not in quote'}]},'A normal contractor quote with dated amounts')
        self.assertEqual(z['items'],[])
        self.assertEqual(z['exclusions'],[])

    def test_currency_mismatch_disables_deltas(self):
        a,b=self.get_fixtures()
        b['currency']='EUR'
        z=compare(a,b)
        self.assertFalse(z['currencies_comparable'])
        self.assertTrue(all(x['delta_b_minus_a'] is None for x in z['matched']))

    def test_no_false_missing_as_excluded(self):
        a,b=self.get_fixtures()
        z=compare(a,b)
        self.assertIn('NOT proof of exclusion',z['caution'])

if __name__=='__main__': unittest.main()
