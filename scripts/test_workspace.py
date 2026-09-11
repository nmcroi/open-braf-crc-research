import copy,unittest
import workspace,sync_tasks
class WorkspaceTests(unittest.TestCase):
    def test_same_cohort_not_independent(self):
        r=workspace.records();a=copy.deepcopy(r[0]);a["id"]="SOURCE-COPY"
        groups=workspace.cohorts(r+[a]);self.assertIn("SOURCE-COPY",groups[r[0]["cohort_id"]]);self.assertEqual(len(groups),2)
    def test_real_records(self):workspace.validate(workspace.records())
    def test_duplicate_rejected(self):
        r=workspace.records()
        with self.assertRaises(ValueError):workspace.validate(r+[r[0]])
    def test_unknown_rejected(self):
        r=copy.deepcopy(workspace.records());r[0]['depends_on']=['missing']
        with self.assertRaises(ValueError):workspace.validate(r)
    def test_cycle_rejected(self):
        r=copy.deepcopy(workspace.records());r[0]['depends_on']=[r[0]['id']]
        with self.assertRaises(ValueError):workspace.validate(r)
    def test_source_change_propagates(self):
        r=workspace.records();b=workspace.baseline(r);r[0]['version']='changed'
        self.assertIn('CLAIM-SCP-PAIRS',workspace.impact(r,b)['requires_review'])
    def test_unchanged_no_flags(self):
        r=workspace.records();self.assertEqual(workspace.impact(r,workspace.baseline(r))['requires_review'],[])
    def test_no_false_completion(self):
        x=dict(number=1,title='t',url='https://example.org',state='CLOSED',updatedAt='today',labels=[{'name':'status:submitted'}])
        self.assertEqual(sync_tasks.normalize([x])[0]['status'],'closed-without-accepted-status')
    def test_status_conflicts(self):
        x=dict(number=1,title='t',url='https://example.org',state='OPEN',updatedAt='today',labels=[{'name':'status:open'},{'name':'status:done'}])
        self.assertEqual(sync_tasks.normalize([x])[0]['status'],'status-conflict')
    def test_stale_visible(self):self.assertIn('verouderd',sync_tasks.render({},stale=True))
    def test_search(self):self.assertTrue(workspace.search('chemokine'))
if __name__=='__main__':unittest.main()
