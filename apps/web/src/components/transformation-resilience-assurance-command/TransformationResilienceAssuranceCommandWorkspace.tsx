'use client';

import React, { useState, useEffect } from 'react';

export function TransformationResilienceAssuranceCommandWorkspace() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [bottomTab, setBottomTab] = useState<
    'timeline' | 'dependencies' | 'interventions' | 'warnings' | 'snapshots' | 'handoffs' | 'scenes' | 'query'
  >('timeline');
  const [queryText, setQueryText] = useState<string>('What is happening right now and what decisions are blocked?');
  const [queryResult, setQueryResult] = useState<any>(null);
  const [queryLoading, setQueryLoading] = useState<boolean>(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/transformation-resilience-assurance-command');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      } else {
        // Fallback seed data
        setData({
          domainsCount: 1,
          criticalObjectsCount: 1,
          decisionQueueCount: 1,
          decisionBottlenecksCount: 1,
          approvalBottlenecksCount: 1,
          interventionBottlenecksCount: 1,
          dependencyHotspotsCount: 1,
          scenesCount: 1,
          snapshotsCount: 2,
          escalationsCount: 1,
          handoffsCount: 1,
          domains: [
            { id: 'cdom_01', name: 'Global Enterprise Resilience Assurance Operations Center 2.0', owner: 'Principal Enterprise Assurance Command & Control Architect', status: 'active', version: 'v2.0' }
          ],
          operationalPictures: [
            { id: 'opic_01', status: 'elevated', active_risks_count: 4, active_warnings_count: 3, active_conflicts_count: 2, active_interventions_count: 2, blocked_actions_count: 1, critical_dependencies_count: 5, capacity_pressure: 'elevated compute load', decision_backlog_count: 2, approval_backlog_count: 1, residual_exposure: 0.12 }
          ],
          criticalObjects: [
            { id: 'crobj_01', object_type: 'intervention', object_id: 'icase_01', title: 'Q3 Wave 4 Simulation Compute Deficit Risk', severity: 'high', owner: 'Transformation Resilience Preventive Operations Engineer', deadline: '2026-08-25', status: 'active' }
          ],
          executiveDecisionQueues: [
            { id: 'edq_01', decision_id: 'dpack_01', title: 'Approval of Preemptive Resequencing for HR Cloud Wave 4 Batch', impact: 'Eliminates predicted compute deficit with zero budget impact.', deadline: '2026-08-20', authority_required: 'Governance Board Authorization', status: 'pending', blocking_objects_json: ['aplan_hr_cloud_02'] }
          ],
          decisionBottlenecks: [
            { id: 'dbott_01', decision_id: 'dpack_01', bottleneck_type: 'approval_delay', description: 'Governance Board review meeting postponed by 48 hours.', impact: 'Delays execution authorization for preemptive resequencing plan.' }
          ],
          approvalBottlenecks: [
            { id: 'abott_01', approval_id: 'appr_01', required_authority: 'Governance Board', age_days: 3.5, impact: 'Blocks ActionGateway execution of action iact_01.', blocking_actions_json: ['iact_01'] }
          ],
          interventionBottlenecks: [
            { id: 'ibott_01', intervention_id: 'icase_01', bottleneck_cause: 'approval', description: 'Intervention action iact_01 is waiting on Governance Board sign-off.' }
          ],
          dependencyHotspots: [
            { id: 'dhot_01', dependency_id: 'dep_compute_cluster_01', name: 'Simulation Compute Cluster 01', affected_plans_count: 5, affected_risks_count: 3, affected_conflicts_count: 2, affected_interventions_count: 2, severity: 'critical' }
          ],
          resourcePressures: [
            { id: 'rpress_01', resource_category: 'compute_capacity', pressure_level: 'elevated', affected_plans_json: ['aplan_01', 'aplan_hr_cloud_02'], affected_interventions_json: ['icase_01'], trend: 'increasing', confidence: 0.95 }
          ],
          knowledgeHealthProjections: [
            { id: 'khealth_01', evidence_freshness: 0.95, coverage: 0.92, validation_rate: 0.90, review_backlog_count: 2, staleness_pct: 0.05, uncertainty_score: 0.10 }
          ],
          planHealthProjections: [
            { id: 'phealth_01', plan_id: 'aplan_01', plan_health: 'watch', staleness: 'fresh', dependency_health: 'elevated_risk', risk_exposure: 0.15, execution_status: 'on_track' }
          ],
          transformationHealthProjections: [
            { id: 'thealth_01', transformation_name: 'Cloud Transformation Wave 3', risk_score: 0.15, coverage_score: 0.90, execution_health: 'stable', dependency_health: 'elevated_risk', active_interventions_count: 1, residual_exposure: 0.08 }
          ],
          crossDomainHeatmaps: [
            { id: 'cdheat_01', domain_name: 'Cloud Transformation Wave 3', risk_level: 0.35, knowledge_level: 0.92, capacity_level: 0.85, dependency_level: 0.75, deadline_level: 0.40, conflict_level: 0.30, intervention_level: 0.60, decision_level: 0.50 }
          ],
          operationalScenes: [
            { id: 'oscene_01', title: 'ERP Transformation & Simulation Cluster Compute Load Compression', description: 'Shared dependency Simulation Cluster 01 queue depth compression affecting Wave 3 and HR Cloud Wave 4.', status: 'active', contained_objects_json: ['icase_01', 'dhot_01', 'dpack_01', 'ewarn_01'] }
          ],
          sceneTimelines: [
            { id: 'stim_01', scene_id: 'oscene_01', stage: 'detection', event_description: 'Early warning trigger detected gradual 15% increase in compute cluster queue depth.' }
          ],
          snapshots: [
            { id: 'csnap_01', label: 'Initial Baseline Snapshot - 2026-08-13', created_at: '2026-08-13T00:00:00Z' },
            { id: 'csnap_02', label: 'Current Operational State Snapshot - 2026-08-14', created_at: '2026-08-14T00:00:00Z' }
          ],
          snapshotDiffs: [
            { id: 'cdiff_01', previous_snapshot_id: 'csnap_01', current_snapshot_id: 'csnap_02', new_risks_json: ['emrisk_02'], new_warnings_json: ['ewarn_02'], new_conflicts_json: ['iconf_01'], new_interventions_json: ['icase_01'], decision_changes_json: ['dpack_01 submitted for approval'] }
          ],
          escalations: [
            { id: 'cesc_01', trigger_reason: 'Decision deadline breach risk on decision packet dpack_01.', status: 'detected', owner: 'Executive Governance Lead' }
          ],
          handoffs: [
            { id: 'ohand_01', outgoing_owner: 'Day Shift Assurance Controller', incoming_owner: 'Night Shift Assurance Controller', current_state_summary: 'Operational status is elevated due to pending Governance Board decision on dpack_01. Action iact_01 ready upon approval.', next_review: '2026-08-14 00:00 UTC' }
          ],
          projectionHealths: [
            { id: 'phealth_01', lag_seconds: 0.12, errors_count: 0, last_processed_event_id: 'cevt_01', rebuild_status: 'idle' }
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
      const res = await fetch(`/api/v1/transformation-resilience-assurance-command/query?query=${encodeURIComponent(queryText)}`, {
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

  const opic = data?.operationalPictures?.[0] || {};
  const kh = data?.knowledgeHealthProjections?.[0] || {};
  const phealth = data?.projectionHealths?.[0] || {};

  return (
    <div className="p-6 space-y-6 max-w-[1700px] mx-auto text-slate-100 font-sans">
      {/* 25. TOP: Enterprise Assurance Status Bar */}
      <div className="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 backdrop-blur-md space-y-4">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-400 via-rose-400 to-indigo-400">
                Assurance Operations Center 2.0
              </h1>
              <span className={`px-3 py-1 text-xs font-bold uppercase rounded-full border ${
                opic.status === 'stable' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' : 'bg-amber-500/20 text-amber-300 border-amber-500/40 animate-pulse'
              }`}>
                Operational State: {opic.status || 'ELEVATED'}
              </span>
              {phealth.lag_seconds > 1.0 && (
                <span className="px-2.5 py-0.5 text-xs rounded bg-yellow-500/20 text-yellow-300 border border-yellow-500/30">
                  Degraded Projection (Lag: {phealth.lag_seconds}s)
                </span>
              )}
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Unified operational command layer over Sprints 97-102: real-time assurance visibility, executive response control, and bottleneck intelligence.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={fetchData}
              className="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
            >
              Refresh Command Center
            </button>
          </div>
        </div>

        {/* Status Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3 text-xs">
          <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
            <p className="text-slate-400 font-medium">Active Risks</p>
            <p className="text-lg font-bold text-rose-400 mt-0.5">{opic.active_risks_count ?? 4}</p>
          </div>
          <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
            <p className="text-slate-400 font-medium">Active Warnings</p>
            <p className="text-lg font-bold text-amber-400 mt-0.5">{opic.active_warnings_count ?? 3}</p>
          </div>
          <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
            <p className="text-slate-400 font-medium">Active Conflicts</p>
            <p className="text-lg font-bold text-yellow-400 mt-0.5">{opic.active_conflicts_count ?? 2}</p>
          </div>
          <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
            <p className="text-slate-400 font-medium">Interventions</p>
            <p className="text-lg font-bold text-cyan-400 mt-0.5">{opic.active_interventions_count ?? 2}</p>
          </div>
          <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
            <p className="text-slate-400 font-medium">Blocked Actions</p>
            <p className="text-lg font-bold text-rose-300 mt-0.5">{opic.blocked_actions_count ?? 1}</p>
          </div>
          <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
            <p className="text-slate-400 font-medium">Decision Backlog</p>
            <p className="text-lg font-bold text-indigo-400 mt-0.5">{opic.decision_backlog_count ?? 2}</p>
          </div>
          <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
            <p className="text-slate-400 font-medium">Approval Backlog</p>
            <p className="text-lg font-bold text-purple-400 mt-0.5">{opic.approval_backlog_count ?? 1}</p>
          </div>
          <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
            <p className="text-slate-400 font-medium">Residual Exposure</p>
            <p className="text-lg font-bold text-teal-400 mt-0.5">{((opic.residual_exposure ?? 0.12) * 100).toFixed(0)}%</p>
          </div>
        </div>
      </div>

      {/* 3-COLUMN MAIN LAYOUT (26. LEFT: Critical Queue | 27. CENTER: Operational Picture | 28. RIGHT: Leadership Decisions) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT PANEL: Critical Queue (3 Cols) */}
        <div className="lg:col-span-3 bg-slate-900/70 p-5 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
            <h2 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              Critical Queue
            </h2>
            <span className="text-xs text-slate-400">{data?.criticalObjects?.length ?? 1} objects</span>
          </div>

          <div className="space-y-3 max-h-[480px] overflow-y-auto pr-1 scrollbar-thin">
            {data?.criticalObjects?.map((obj: any) => (
              <div key={obj.id} className="p-3.5 rounded-xl bg-slate-950/80 border border-rose-500/30 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-rose-300 uppercase">{obj.object_type}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-semibold">{obj.severity}</span>
                </div>
                <p className="text-xs font-semibold text-slate-200 leading-snug">{obj.title}</p>
                <div className="flex justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800">
                  <span>Owner: {obj.owner}</span>
                  <span>Deadline: {obj.deadline || 'N/A'}</span>
                </div>
              </div>
            ))}

            {data?.priorities?.map((p: any) => (
              <div key={p.id} className="p-3 rounded-xl bg-slate-950/50 border border-slate-800 space-y-1.5 text-xs">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-amber-400">Rank Score: {p.rank_score}</span>
                  <span className="text-slate-400">Urgency: {p.urgency}</span>
                </div>
                <p className="text-slate-300">Object ID: <strong>{p.object_id}</strong> | Window: <strong>{p.intervention_window}</strong></p>
                <p className="text-[11px] text-slate-400">Dependency: {p.decision_dependency}</p>
              </div>
            ))}
          </div>
        </div>

        {/* CENTER PANEL: Operational Picture & Health Projections (6 Cols) */}
        <div className="lg:col-span-6 bg-slate-900/70 p-5 rounded-2xl border border-slate-800 space-y-5">
          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
            <h2 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
              Operational Picture & Health Projections
            </h2>
            <span className="text-xs text-cyan-400 font-semibold">Real-Time Event Projections</span>
          </div>

          {/* Health Projections Grid */}
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800 space-y-1">
              <p className="font-semibold text-cyan-400">Transformation Health</p>
              <p className="text-slate-300">Risk Score: <strong className="text-rose-400">0.15</strong> | Coverage: <strong className="text-emerald-400">90%</strong></p>
              <p className="text-[11px] text-slate-400">Execution: Stable | Exposure: 8%</p>
            </div>
            <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800 space-y-1">
              <p className="font-semibold text-teal-400">Knowledge Health</p>
              <p className="text-slate-300">Freshness: <strong className="text-emerald-400">{(kh.evidence_freshness * 100 || 95).toFixed(0)}%</strong> | Coverage: <strong>{(kh.coverage * 100 || 92).toFixed(0)}%</strong></p>
              <p className="text-[11px] text-slate-400">Staleness: {(kh.staleness_pct * 100 || 5).toFixed(0)}% | Backlog: {kh.review_backlog_count || 2} items</p>
            </div>
            <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800 space-y-1">
              <p className="font-semibold text-amber-400">Capacity & Resource Pressure</p>
              <p className="text-slate-300">Compute Load: <strong className="text-amber-400 font-semibold">Elevated (Increasing)</strong></p>
              <p className="text-[11px] text-slate-400">Affected: Wave 3, HR Cloud Wave 4</p>
            </div>
            <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800 space-y-1">
              <p className="font-semibold text-indigo-400">Dependency Hotspot</p>
              <p className="text-slate-300">Hotspot: <strong className="text-indigo-300 font-semibold">Simulation Cluster 01</strong></p>
              <p className="text-[11px] text-slate-400">Affects 5 plans, 3 risks, 2 conflicts</p>
            </div>
          </div>

          {/* Operational Scene Section */}
          <div className="p-4 rounded-xl bg-slate-950/90 border border-cyan-500/30 space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">Active Operational Scene</span>
              <span className="text-[10px] px-2.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-semibold uppercase">Status: Active</span>
            </div>
            {data?.operationalScenes?.map((sc: any) => (
              <div key={sc.id} className="space-y-1">
                <p className="text-xs font-bold text-slate-200">{sc.title}</p>
                <p className="text-[11px] text-slate-300">{sc.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT PANEL: Leadership Decisions & Bottlenecks (3 Cols) */}
        <div className="lg:col-span-3 bg-slate-900/70 p-5 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
            <h2 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-400"></span>
              Leadership Decisions
            </h2>
            <span className="text-xs text-indigo-400 font-semibold">{data?.executiveDecisionQueues?.length ?? 1} pending</span>
          </div>

          <div className="space-y-3 max-h-[480px] overflow-y-auto pr-1 scrollbar-thin">
            {data?.executiveDecisionQueues?.map((dq: any) => (
              <div key={dq.id} className="p-3.5 rounded-xl bg-slate-950/80 border border-indigo-500/30 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-indigo-300">Decision ID: {dq.decision_id}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-semibold">{dq.status}</span>
                </div>
                <p className="text-xs font-semibold text-slate-200 leading-snug">{dq.title}</p>
                <p className="text-[11px] text-slate-300">{dq.impact}</p>
                <p className="text-[11px] text-indigo-400 font-semibold">Authority: {dq.authority_required}</p>
              </div>
            ))}

            {data?.decisionBottlenecks?.map((db: any) => (
              <div key={db.id} className="p-3 rounded-xl bg-slate-950/60 border border-rose-500/20 space-y-1 text-xs">
                <span className="font-bold text-rose-400">Decision Bottleneck: {db.bottleneck_type}</span>
                <p className="text-slate-300">{db.description}</p>
              </div>
            ))}

            {data?.approvalBottlenecks?.map((ab: any) => (
              <div key={ab.id} className="p-3 rounded-xl bg-slate-950/60 border border-purple-500/20 space-y-1 text-xs">
                <span className="font-bold text-purple-400">Approval Bottleneck (Age: {ab.age_days} days)</span>
                <p className="text-slate-300">{ab.impact}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* BOTTOM PANELS & TABS */}
      <div className="space-y-4">
        <div className="flex border-b border-slate-800 overflow-x-auto space-x-2 scrollbar-none">
          {[
            { id: 'timeline', label: 'Scene Timelines' },
            { id: 'dependencies', label: 'Dependency Hotspots' },
            { id: 'interventions', label: 'Intervention Bottlenecks' },
            { id: 'warnings', label: 'Command Events' },
            { id: 'snapshots', label: 'Command Snapshots & Diffs' },
            { id: 'handoffs', label: 'Operations Handoffs' },
            { id: 'query', label: 'Command Natural Language Query' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setBottomTab(tab.id as any)}
              className={`px-4 py-2.5 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
                bottomTab === tab.id
                  ? 'border-amber-400 text-amber-400 bg-amber-500/5'
                  : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 min-h-[300px]">
          {loading ? (
            <div className="flex items-center justify-center h-48 text-slate-400 text-sm">
              Loading operational command center streams and checking projection health...
            </div>
          ) : (
            <>
              {bottomTab === 'timeline' && (
                <div className="space-y-3">
                  <h3 className="text-sm font-semibold text-slate-200">Scene Timeline Events</h3>
                  {data?.sceneTimelines?.map((st: any) => (
                    <div key={st.id} className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                      <div>
                        <span className="text-xs px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-bold uppercase mr-3">{st.stage}</span>
                        <span className="text-xs text-slate-200">{st.event_description}</span>
                      </div>
                      <span className="text-xs text-slate-400">{st.timestamp}</span>
                    </div>
                  ))}
                </div>
              )}

              {bottomTab === 'dependencies' && (
                <div className="space-y-3">
                  <h3 className="text-sm font-semibold text-slate-200">Critical Dependency Hotspots</h3>
                  {data?.dependencyHotspots?.map((dh: any) => (
                    <div key={dh.id} className="p-4 rounded-xl bg-slate-950/60 border border-indigo-500/30 space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-bold text-indigo-300">{dh.name}</span>
                        <span className="text-xs px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 font-semibold uppercase">{dh.severity}</span>
                      </div>
                      <p className="text-xs text-slate-300">
                        Affected Plans: <strong className="text-amber-400">{dh.affected_plans_count}</strong> | Risks: <strong>{dh.affected_risks_count}</strong> | Interventions: <strong>{dh.affected_interventions_count}</strong>
                      </p>
                    </div>
                  ))}
                </div>
              )}

              {bottomTab === 'snapshots' && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-200">Operational Point-in-Time Snapshots & Diffs</h3>
                  <div className="grid grid-cols-2 gap-4">
                    {data?.snapshots?.map((sn: any) => (
                      <div key={sn.id} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                        <span className="text-xs font-bold text-teal-400">{sn.label}</span>
                        <p className="text-xs text-slate-400">Created At: {sn.created_at}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {bottomTab === 'handoffs' && (
                <div className="space-y-3">
                  <h3 className="text-sm font-semibold text-slate-200">Shift Ownership Handoffs</h3>
                  {data?.handoffs?.map((ho: any) => (
                    <div key={ho.id} className="p-4 rounded-xl bg-slate-950/60 border border-purple-500/30 space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-xs font-bold text-purple-300">{ho.outgoing_owner} → {ho.incoming_owner}</span>
                        <span className="text-xs text-slate-400">Next Review: {ho.next_review}</span>
                      </div>
                      <p className="text-xs text-slate-300">{ho.current_state_summary}</p>
                    </div>
                  ))}
                </div>
              )}

              {bottomTab === 'query' && (
                <div className="space-y-6">
                  <h3 className="text-sm font-semibold text-slate-200">Command Center Natural Language Query</h3>
                  <div className="flex gap-3">
                    <input
                      type="text"
                      value={queryText}
                      onChange={(e) => setQueryText(e.target.value)}
                      placeholder="Ask about active operational state, blocked decisions, dependency hotspots, or snapshot diffs..."
                      className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-amber-500/50"
                    />
                    <button
                      onClick={handleQuery}
                      disabled={queryLoading}
                      className="px-5 py-2.5 bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-slate-950 text-xs font-bold rounded-xl transition"
                    >
                      {queryLoading ? 'Processing...' : 'Run Query'}
                    </button>
                  </div>

                  {queryResult && (
                    <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-xs font-semibold text-amber-400">Command Operations Result</span>
                        <span className="text-xs text-slate-400">Confidence: {queryResult.confidencePct}%</span>
                      </div>
                      {queryResult.evidenceJson?.error ? (
                        <div className="text-xs text-rose-400 font-semibold">{queryResult.evidenceJson.error}</div>
                      ) : (
                        <div className="space-y-2 text-xs text-slate-300">
                          {queryResult.results?.map((r: any, idx: number) => (
                            <div key={idx} className="p-3 bg-slate-900 rounded-lg space-y-1">
                              <p><strong className="text-amber-400">What Is Happening:</strong> {r.what_is_happening}</p>
                              <p><strong className="text-cyan-400">What Is About To Happen:</strong> {r.what_is_about_to_happen}</p>
                              <p><strong className="text-teal-400">What Are We Doing:</strong> {r.what_are_we_doing}</p>
                              <p><strong className="text-rose-400">What Is Blocked:</strong> {r.what_is_blocked}</p>
                              <p><strong className="text-indigo-400">What Needs A Decision:</strong> {r.what_needs_decision}</p>
                              <p><strong className="text-purple-400">What Needs Leadership Attention:</strong> {r.what_needs_leadership_attention}</p>
                              <p><strong className="text-yellow-400">What Could Cascade:</strong> {r.what_could_cascade}</p>
                              <p><strong className="text-emerald-400">What Has Recovered:</strong> {r.what_has_recovered}</p>
                              <p><strong className="text-rose-300">What Remains Exposed:</strong> {r.what_remains_exposed}</p>
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
    </div>
  );
}
