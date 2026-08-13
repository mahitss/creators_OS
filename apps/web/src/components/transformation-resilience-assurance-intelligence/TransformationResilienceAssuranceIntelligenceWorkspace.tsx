'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceAssuranceIntelligenceWorkspace() {
  const [activeTab, setActiveTab] = useState<
    | 'overview'
    | 'outcomes'
    | 'expected_vs_actual'
    | 'variances'
    | 'evidences'
    | 'causal'
    | 'rec_qualities'
    | 'dec_qualities'
    | 'patterns'
    | 'analogues'
    | 'calibrations'
    | 'signals'
    | 'priorities'
    | 'proposals'
    | 'versions'
    | 'shadow'
    | 'regressions'
    | 'drifts'
    | 'lessons'
    | 'query'
  >('overview');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [queryText, setQueryText] = useState<string>('Show expected vs actual outcomes and recommendation calibration.');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-assurance-intelligence');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          outcomesCount: 1,
          comparisonsCount: 1,
          variancesCount: 1,
          evidencesCount: 1,
          causalsCount: 1,
          recQualitiesCount: 1,
          decQualitiesCount: 1,
          patternsCount: 1,
          analoguesCount: 1,
          signalsCount: 1,
          proposalsCount: 2,
          versionsCount: 1,
          regressionsCount: 1,
          lessonsCount: 1,
          domains: [
            { id: 'adom_01', name: 'Global Enterprise Assurance Decision Intelligence & Closed-Loop Resolution Learning 2.0', owner: 'Principal Enterprise Assurance Decision Intelligence Architect', status: 'active', version: 'v2.0' }
          ],
          outcomes: [
            { id: 'dout_01', decision_id: 'dec_seq_01', conflict_id: 'ccase_01', selected_option: 'sequence', execution_status: 'completed', verification_status: 'verified', outcome_status: 'positive' }
          ],
          comparisons: [
            { id: 'eac_01', decision_outcome_id: 'dout_01', expected_risk: 0.08, actual_risk: 0.07, expected_coverage: 0.92, actual_coverage: 0.94, expected_timeline_days: 14, actual_timeline_days: 13 }
          ],
          variances: [
            { id: 'ovar_01', dimension: 'coverage', expected_val: 0.92, actual_val: 0.94, delta: 0.02, explanation_status: 'explained' }
          ],
          evidences: [
            { id: 'oev_01', source: 'resilience_sensing', evidence_type: 'telemetry_verification', quality: 0.95, relationship: 'verified_telemetry' }
          ],
          causals: [
            { id: 'causal_01', causal_relationship: 'contributed_to', description: 'Sequencing simulation compute directly relieved 20% over-subscription without delaying critical deployment milestones.', confidence: 0.92 }
          ],
          recommendationQualities: [
            { id: 'rq_01', recommendation_id: 'crec_01', evidence_quality: 0.94, scenario_quality: 0.92, risk_calibration: 0.95, coverage_accuracy: 0.96 }
          ],
          decisionQualities: [
            { id: 'dq_01', decision_id: 'dec_seq_01', information_sufficiency: 0.95, option_completeness: 0.92, tradeoff_visibility: 0.94, governance_alignment: 0.98 }
          ],
          patternPerformances: [
            { id: 'ppperf_01', pattern_id: 'rpatt_01', usage_count: 12, success_count: 11, failure_count: 1, coverage_preservation_avg: 0.92 }
          ],
          historicalAnalogues: [
            { id: 'analog_01', current_case_id: 'ccase_01', historical_case_id: 'ccase_hist_99', historical_outcome: 'positive', relevance_score: 0.90, confidence: 0.92 }
          ],
          calibrations: [
            { id: 'rcal_01', predicted_confidence_avg: 0.95, observed_accuracy_avg: 0.94, calibration_error: 0.01, status: 'well_calibrated' }
          ],
          learningSignals: [
            { id: 'lsig_01', signal_type: 'recurring_pattern', description: 'Sequencing simulation compute workloads across adjacent weeks consistently preserves >90% coverage.', priority: 'high' }
          ],
          knowledgeUpdateProposals: [
            { id: 'kup_01', proposal_type: 'new_validation_requirement', description: 'Require simulation cluster capacity validation prior to final Q3 wave authorization.', status: 'pending_review' }
          ],
          recommendationUpdateProposals: [
            { id: 'rup_01', current_behavior: 'Default to parallel execution until compute failure detected.', proposed_improvement: 'Proactively recommend sequenced execution when cluster utilization exceeds 85%.', status: 'pending_review' }
          ],
          learningVersions: [
            { id: 'lver_01', version_number: 'v2.0', parent_version: 'v1.0', changes_summary: 'Integrated closed-loop resolution learning and recommendation optimization 2.0.', approval_state: 'approved' }
          ],
          regressions: [
            { id: 'reg_01', previous_version: 'v1.0', new_version: 'v2.0', affected_dimension: 'risk_calibration', severity: 'low', description: 'Minor 0.5% variance increase in secondary timeline prediction window.' }
          ],
          drifts: [
            { id: 'rdrift_01', drift_type: 'confidence_drift', description: 'Confidence drift detected: vendor operations plans show higher variance in timeline predictions.' }
          ],
          lessons: [
            { id: 'less_01', lesson_type: 'success', title: 'Sequenced Simulation Workload Optimization Lesson', description: 'Staggering compute-intensive simulation workloads by 7 days resolves capacity shortages without compromising risk coverage.' }
          ]
        });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async () => {
    if (!queryText.trim()) return;
    setQueryLoading(true);
    try {
      const res = await fetch(`/api/v1/transformation-resilience-assurance-intelligence/query?query=${encodeURIComponent(queryText)}`, {
        method: 'POST'
      });
      if (res.ok) {
        const json = await res.json();
        setQueryResult(json);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setQueryLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 via-teal-400 to-indigo-400">
              Assurance Decision Intelligence & Closed-Loop Resolution Learning 2.0
            </h1>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Governed Recommendation Optimization
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Observe, measure, compare, learn, and improve recommendation quality across decisions, execution, verification, and outcome evidence without autonomous governance changes.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Refresh Learning Engine
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Domain Status</p>
          <p className="text-xl font-bold text-emerald-400 mt-1">Active</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Outcomes Tracked</p>
          <p className="text-xl font-bold text-teal-400 mt-1">{data?.outcomesCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Rec Quality</p>
          <p className="text-xl font-bold text-indigo-400 mt-1">94.0%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Calibration Error</p>
          <p className="text-xl font-bold text-cyan-400 mt-1">1.0%</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Learning Signals</p>
          <p className="text-xl font-bold text-amber-400 mt-1">{data?.signalsCount ?? 1}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Update Proposals</p>
          <p className="text-xl font-bold text-rose-400 mt-1">{data?.proposalsCount ?? 2}</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Active Version</p>
          <p className="text-xl font-bold text-purple-400 mt-1">v2.0</p>
        </div>
        <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400 font-medium">Verified Lessons</p>
          <p className="text-xl font-bold text-blue-400 mt-1">{data?.lessonsCount ?? 1}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
        {[
          { id: 'overview', label: 'Domain Overview' },
          { id: 'outcomes', label: 'Decision Outcomes' },
          { id: 'expected_vs_actual', label: 'Expected vs Actual' },
          { id: 'variances', label: 'Outcome Variances' },
          { id: 'evidences', label: 'Evidence Provenance' },
          { id: 'causal', label: 'Causal Analysis' },
          { id: 'rec_qualities', label: 'Recommendation Quality' },
          { id: 'dec_qualities', label: 'Decision Quality' },
          { id: 'patterns', label: 'Pattern Performance' },
          { id: 'analogues', label: 'Historical Analogues' },
          { id: 'calibrations', label: 'Recommendation Calibration' },
          { id: 'signals', label: 'Learning Signals' },
          { id: 'priorities', label: 'Learning Priorities' },
          { id: 'proposals', label: 'Update Proposals' },
          { id: 'versions', label: 'Learning Versions' },
          { id: 'shadow', label: 'Shadow Evaluation' },
          { id: 'regressions', label: 'Regression Detection' },
          { id: 'drifts', label: 'Behavioral Drift' },
          { id: 'lessons', label: 'Lessons & Reuse' },
          { id: 'query', label: 'Assurance Intelligence Query' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
              activeTab === tab.id
                ? 'border-emerald-400 text-emerald-400 bg-emerald-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 min-h-[400px]">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-slate-400 text-sm">
            Measuring expected vs actual outcomes, computing recommendation calibration, and extracting verified lessons...
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Assurance Decision Intelligence Domain</h3>
                {data?.domains?.map((dom: any) => (
                  <div key={dom.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-emerald-400">{dom.name}</span>
                      <p className="text-xs text-slate-400 mt-1">Owner: {dom.owner} | Version: {dom.version}</p>
                    </div>
                    <span className="text-xs px-3 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">{dom.status}</span>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'outcomes' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Decision Outcome Records</h3>
                {data?.outcomes?.map((doc: any) => (
                  <div key={doc.id} className="p-4 rounded-xl bg-slate-950/60 border border-emerald-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-emerald-400">Outcome ID: {doc.id}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-300 font-semibold uppercase">{doc.outcome_status}</span>
                    </div>
                    <p className="text-xs text-slate-300">Decision ID: {doc.decision_id} | Conflict ID: {doc.conflict_id} | Selected Option: {doc.selected_option}</p>
                    <p className="text-xs text-slate-400">Execution: {doc.execution_status} | Verification: {doc.verification_status}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'expected_vs_actual' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Expected vs Actual Outcome Comparisons</h3>
                {data?.comparisons?.map((eac: any) => (
                  <div key={eac.id} className="p-4 rounded-xl bg-slate-950/60 border border-teal-500/30 space-y-3">
                    <span className="text-sm font-semibold text-teal-400">Comparison {eac.id} (Decision Outcome: {eac.decision_outcome_id})</span>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs text-slate-300">
                      <div className="p-2.5 bg-slate-900 rounded-lg">
                        <p className="text-slate-400">Risk Exposure</p>
                        <p>Expected: <strong>{(eac.expected_risk * 100).toFixed(0)}%</strong> vs Actual: <strong>{(eac.actual_risk * 100).toFixed(0)}%</strong></p>
                      </div>
                      <div className="p-2.5 bg-slate-900 rounded-lg">
                        <p className="text-slate-400">Assurance Coverage</p>
                        <p>Expected: <strong>{(eac.expected_coverage * 100).toFixed(0)}%</strong> vs Actual: <strong>{(eac.actual_coverage * 100).toFixed(0)}%</strong></p>
                      </div>
                      <div className="p-2.5 bg-slate-900 rounded-lg">
                        <p className="text-slate-400">Timeline Shift</p>
                        <p>Expected: <strong>{eac.expected_timeline_days} days</strong> vs Actual: <strong>{eac.actual_timeline_days} days</strong></p>
                      </div>
                      <div className="p-2.5 bg-slate-900 rounded-lg">
                        <p className="text-slate-400">Residual Risk</p>
                        <p>Expected: <strong>{(eac.expected_residual_risk * 100).toFixed(0)}%</strong> vs Actual: <strong>{(eac.actual_residual_risk * 100).toFixed(0)}%</strong></p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'calibrations' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Recommendation Calibration & Error Analysis</h3>
                {data?.calibrations?.map((rcal: any) => (
                  <div key={rcal.id} className="p-4 rounded-xl bg-slate-950/60 border border-cyan-500/30 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-cyan-400">Calibration Status: {rcal.status}</span>
                      <span className="text-xs px-2.5 py-1 rounded bg-cyan-500/20 text-cyan-300 font-semibold">Error: {(rcal.calibration_error * 100).toFixed(1)}%</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs text-slate-300 mt-2">
                      <p>Predicted Confidence Avg: <strong>{(rcal.predicted_confidence_avg * 100).toFixed(0)}%</strong></p>
                      <p>Observed Accuracy Avg: <strong>{(rcal.observed_accuracy_avg * 100).toFixed(0)}%</strong></p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'proposals' && (
              <div className="space-y-4">
                <h3 className="text-base font-semibold text-slate-200">Governed Update Proposals (Pending Approval Routing)</h3>
                {data?.knowledgeUpdateProposals?.map((kup: any) => (
                  <div key={kup.id} className="p-4 rounded-xl bg-amber-950/30 border border-amber-500/40 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-amber-400">Knowledge Update Proposal {kup.id}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-semibold">{kup.status}</span>
                    </div>
                    <p className="text-xs text-slate-300">{kup.description}</p>
                  </div>
                ))}
                {data?.recommendationUpdateProposals?.map((rup: any) => (
                  <div key={rup.id} className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-500/40 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-semibold text-indigo-400">Recommendation Update Proposal {rup.id}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-semibold">{rup.status}</span>
                    </div>
                    <p className="text-xs text-slate-300">Proposed Improvement: {rup.proposed_improvement}</p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'query' && (
              <div className="space-y-6">
                <h3 className="text-base font-semibold text-slate-200">Natural Language Assurance Intelligence Query</h3>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    placeholder="Ask about expected vs actual outcomes, recommendation quality, calibration, or lessons..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500/50"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryLoading}
                    className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-slate-950 text-xs font-semibold rounded-xl transition"
                  >
                    {queryLoading ? 'Processing...' : 'Run Query'}
                  </button>
                </div>

                {queryResult && (
                  <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-emerald-400">Assurance Intelligence Result</span>
                      <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                    </div>
                    {queryResult.evidenceJson?.error ? (
                      <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                    ) : (
                      <div className="space-y-2 text-xs text-slate-300">
                        {queryResult.results?.map((r: any, idx: number) => (
                          <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                            <p><strong className="text-emerald-400">5 Core Distinctions:</strong> {r.five_core_distinctions}</p>
                            <p><strong className="text-teal-400">Expected vs Actual:</strong> {r.expected_vs_actual_variance}</p>
                            <p><strong className="text-indigo-400">Causal Analysis:</strong> {r.causal_analysis}</p>
                            <p><strong className="text-cyan-400">Recommendation Quality:</strong> {r.recommendation_quality}</p>
                            <p><strong className="text-amber-400">Pattern Performance:</strong> {r.pattern_performance}</p>
                            <p><strong className="text-blue-400">Calibration Status:</strong> {r.calibration}</p>
                            <p><strong className="text-emerald-300 font-semibold">Verified Lesson:</strong> {r.lessons}</p>
                            <p><strong className="text-rose-400">Governance Update Proposal:</strong> {r.learning_proposal}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
