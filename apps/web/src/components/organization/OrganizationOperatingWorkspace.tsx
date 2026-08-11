"use client";

import React, { useState, useEffect } from "react";
import {
  Building2,
  Users,
  Box,
  Target,
  AlertTriangle,
  GitBranch,
  Search,
  Play,
  RefreshCw,
  TrendingUp,
  Layers,
  ShieldCheck,
  Zap,
  HelpCircle
} from "lucide-react";

export function OrganizationOperatingWorkspace() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "teams" | "capabilities" | "outcomes" | "risks" | "scenarios" | "query"
  >("overview");

  const [overview, setOverview] = useState<any>(null);
  const [queryInput, setQueryInput] = useState("Which missions depend on Salesforce?");
  const [queryResult, setQueryResult] = useState<any>(null);
  const [scenarioName, setScenarioName] = useState("Simulated Salesforce API Outage");
  const [scenarioResult, setScenarioResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchOverview = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/organization");
      if (res.ok) {
        const data = await res.json();
        setOverview(data);
      }
    } catch (err) {
      console.error("Failed to load organization operating graph data:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  const handleQuery = async () => {
    if (!queryInput) return;
    try {
      const res = await fetch("/api/v1/organization/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryInput })
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResult(data);
      }
    } catch (err) {
      console.error("NL Query failed:", err);
    }
  };

  const handleSimulateScenario = async () => {
    try {
      const res = await fetch("/api/v1/organization/scenarios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: scenarioName, assumptionsJson: { target: "integration_sf_01" } })
      });
      if (res.ok) {
        const data = await res.json();
        setScenarioResult(data);
      }
    } catch (err) {
      console.error("Scenario simulation failed:", err);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-[1600px] mx-auto text-slate-100 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
              <Building2 className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
                Enterprise Operating Graph 2.0
                <span className="text-xs px-2.5 py-1 bg-emerald-500/20 text-emerald-300 font-mono font-medium rounded-full border border-emerald-500/30">
                  Business Outcome Intelligence
                </span>
              </h1>
              <p className="text-xs text-slate-400 font-medium">
                Living organizational operating graph connecting teams, capabilities, missions, work, decisions, and outcomes
              </p>
            </div>
          </div>
        </div>

        <button
          onClick={fetchOverview}
          className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold flex items-center gap-2 transition border border-slate-700/50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} />
          Refresh Graph
        </button>
      </div>

      {/* Top Telemetry Header */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Active Outcomes</span>
            <Target className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">{overview?.activeOutcomesCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Dependencies Monitored</span>
            <GitBranch className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-cyan-400">{overview?.dependenciesMonitoredCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>System Bottlenecks</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">{overview?.systemBottlenecksCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Capability Gaps</span>
            <Box className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-2xl font-bold text-purple-400">{overview?.capabilityGapsCount || 0}</p>
        </div>

        <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>Concentration Risks</span>
            <ShieldCheck className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-bold text-rose-400">{overview?.concentrationRisksCount || 0}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: "overview", label: "Operating Overview", icon: Building2 },
          { id: "capabilities", label: "Capabilities & Gaps", icon: Box },
          { id: "outcomes", label: "Business Outcomes", icon: Target },
          { id: "risks", label: "Risks & Concentration", icon: AlertTriangle },
          { id: "scenarios", label: "Scenario Simulator", icon: Play },
          { id: "query", label: "Natural Language Graph Query", icon: Search }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 whitespace-nowrap transition ${
                isActive
                  ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT: Overview */}
      {activeTab === "overview" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Building2 className="w-4 h-4 text-emerald-400" />
            Operating Graph Status &amp; Bottleneck Evidence
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.bottlenecks?.map((b: any) => (
              <div key={b.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-amber-300">Bottleneck: {b.blocker_type}</span>
                  <span className="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded font-bold uppercase">{b.status}</span>
                </div>
                <p className="text-slate-300">Root Dependency: {b.root_dependency_ref}</p>
                <p className="text-slate-500">Duration: {b.duration_hours} hours | Affected Work: {JSON.stringify(b.affected_work_json)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Capabilities & Gaps */}
      {activeTab === "capabilities" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Box className="w-4 h-4 text-purple-400" />
            Capability &amp; Skill Gap Matrix
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.gaps?.map((g: any) => (
              <div key={g.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-purple-300">Capability: {g.capability_id}</span>
                  <span className="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-bold uppercase">{g.gap_classification}</span>
                </div>
                <p className="text-slate-300">{g.impact_summary}</p>
                <p className="text-slate-500">Required By: {g.required_by_ref}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Business Outcomes */}
      {activeTab === "outcomes" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Target className="w-4 h-4 text-emerald-400" />
            Business Outcomes &amp; Traceability
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.outcomes?.map((o: any) => (
              <div key={o.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-emerald-300">{o.name}</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold uppercase">{o.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{o.description}</p>
                <p className="text-slate-400">Target: {o.target} | Current: {o.current_state}</p>
                <p className="text-slate-500">Owner: {o.owner}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Risks & Concentration */}
      {activeTab === "risks" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-rose-400" />
            Concentration Risks &amp; Organizational Hazards
          </h2>

          <div className="space-y-3 font-mono text-xs">
            {overview?.risks?.map((r: any) => (
              <div key={r.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-300">{r.title} ({r.dimension})</span>
                  <span className="text-[10px] bg-rose-500/20 text-rose-300 px-2 py-0.5 rounded font-bold uppercase">{r.status}</span>
                </div>
                <p className="text-slate-300 font-sans">{r.description}</p>
                <p className="text-slate-500">Source: {r.source_ref}</p>
                <p className="text-slate-400">Mitigation Recommendations: {JSON.stringify(r.mitigation_recommendations_json)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Scenario Simulator */}
      {activeTab === "scenarios" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Play className="w-4 h-4 text-cyan-400" />
            Production-Safe Scenario Analysis Lab
          </h2>

          <div className="space-y-3 font-mono text-xs">
            <div className="flex gap-2">
              <input
                type="text"
                value={scenarioName}
                onChange={(e) => setScenarioName(e.target.value)}
                className="flex-1 bg-slate-800 border border-slate-700 text-slate-200 px-3 py-2 rounded-xl text-xs"
                placeholder="Enter scenario assumption..."
              />
              <button
                onClick={handleSimulateScenario}
                className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-semibold flex items-center gap-2"
              >
                <Play className="w-4 h-4" />
                Run Simulation
              </button>
            </div>

            {scenarioResult && (
              <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <span className="font-bold text-cyan-300">Simulation Output: {scenarioResult.name}</span>
                <p className="text-slate-300">Affected Nodes: {JSON.stringify(scenarioResult.affectedNodesJson)}</p>
                <p className="text-slate-400">Expected Impact: {JSON.stringify(scenarioResult.expectedImpactJson)}</p>
                <span className="text-[10px] text-emerald-400 font-bold">Production State Preserved Unchanged</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB CONTENT: Natural Language Graph Query */}
      {activeTab === "query" && (
        <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Search className="w-4 h-4 text-emerald-400" />
            Natural Language Operating Graph Queries
          </h2>

          <div className="space-y-3 font-mono text-xs">
            <div className="flex gap-2">
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                className="flex-1 bg-slate-800 border border-slate-700 text-slate-200 px-3 py-2 rounded-xl text-xs"
                placeholder="Ask an organizational graph question..."
              />
              <button
                onClick={handleQuery}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold flex items-center gap-2"
              >
                <Search className="w-4 h-4" />
                Execute Query
              </button>
            </div>

            {queryResult && (
              <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 space-y-2">
                <span className="font-bold text-emerald-300">Query: {queryResult.query} ({queryResult.confidencePct}% confidence)</span>
                <p className="text-slate-300">Results: {JSON.stringify(queryResult.results)}</p>
                <p className="text-slate-500">Evidence: {JSON.stringify(queryResult.evidenceJson)}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
