'use client';

import React, { useState, useEffect } from 'react';
import { 
  Zap, 
  Activity, 
  CheckCircle, 
  AlertTriangle, 
  Layers, 
  RefreshCw, 
  Shield, 
  Radio, 
  ListFilter,
  RotateCcw,
  ArrowRight,
  Database
} from 'lucide-react';

interface EventEnvelope {
  id: string;
  eventId: string;
  eventType: string;
  eventVersion: string;
  organizationId: string;
  workspaceId?: string;
  source: string;
  subject: string;
  timestamp: string;
  correlationId: string;
  causationId?: string;
  producer: string;
  classification: string;
  payloadReference: any;
}

interface CatalogEntry {
  id: string;
  eventType: string;
  version: string;
  producer: string;
  description: string;
  classification: string;
  retentionDays: number;
}

interface EventSubscription {
  id: string;
  organizationId: string;
  workspaceId?: string;
  eventType: string;
  consumer: string;
  enabled: boolean;
  createdAt: string;
}

interface DeadLetter {
  id: string;
  eventId: string;
  eventType: string;
  producer: string;
  error: string;
  attemptCount: number;
  createdAt: string;
}

interface EventHealth {
  throughputEps: number;
  latencyP95: number;
  errorRate: number;
  consumerLag: number;
  deadLetterCount: number;
  updatedAt: string;
}

export const EventMeshWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'stream' | 'catalog' | 'subscriptions' | 'deadletters'>('stream');
  const [events, setEvents] = useState<EventEnvelope[]>([]);
  const [catalog, setCatalog] = useState<CatalogEntry[]>([]);
  const [subscriptions, setSubscriptions] = useState<EventSubscription[]>([]);
  const [deadLetters, setDeadLetters] = useState<DeadLetter[]>([]);
  const [health, setHealth] = useState<EventHealth | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [filterType, setFilterType] = useState('');

  const [pubEventType, setPubEventType] = useState('mission.created');
  const [pubSource, setPubSource] = useState('mission_engine');
  const [pubSubject, setPubSubject] = useState('mission_01');
  const [pubProducer, setPubProducer] = useState('executive_ai');

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [eventsRes, catalogRes, subsRes, dlRes, healthRes] = await Promise.all([
        fetch('/api/v1/events', { headers: { 'X-User-Id': 'usr_executive_01' } }),
        fetch('/api/v1/events/catalog'),
        fetch('/api/v1/events/subscriptions'),
        fetch('/api/v1/events/dead-letters'),
        fetch('/api/v1/events/health')
      ]);

      if (eventsRes.ok) setEvents(await eventsRes.json());
      if (catalogRes.ok) setCatalog(await catalogRes.json());
      if (subsRes.ok) setSubscriptions(await subsRes.json());
      if (dlRes.ok) setDeadLetters(await dlRes.json());
      if (healthRes.ok) setHealth(await healthRes.json());
    } catch (err) {
      console.error('Failed to fetch Event Mesh telemetry:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handlePublishTestEvent = async () => {
    try {
      const res = await fetch('/api/v1/events', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': 'usr_executive_01'
        },
        body: JSON.stringify({
          eventType: pubEventType,
          eventVersion: '1.0.0',
          organizationId: 'org_default_creator',
          workspaceId: 'ws_default_01',
          source: pubSource,
          subject: pubSubject,
          producer: pubProducer,
          payloadReference: { status: 'initiated', timestamp: new Date().toISOString() },
          classification: 'internal'
        })
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error('Failed to publish event:', err);
    }
  };

  const handleReplayEvent = async (eventId: string) => {
    try {
      const res = await fetch(`/api/v1/events/replay/${eventId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': 'usr_executive_01'
        },
        body: JSON.stringify({ reason: 'Admin manual re-drive request' })
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      console.error('Failed to replay event:', err);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 bg-slate-950 text-slate-100 min-h-screen">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <Zap className="w-8 h-8 text-cyan-400" />
            <h1 className="text-3xl font-bold tracking-tight text-white">Enterprise Event Mesh</h1>
          </div>
          <p className="text-slate-400 mt-1">
            Real-Time Intelligence Fabric & Policy-Governed Durable Event Routing
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={fetchData}
            className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-medium transition"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh Telemetry
          </button>
        </div>
      </div>

      {/* Telemetry Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-2 text-slate-400 text-sm font-medium">
            <Radio className="w-4 h-4 text-cyan-400" />
            Throughput (EPS)
          </div>
          <div className="text-2xl font-bold mt-2 text-white">
            {health?.throughputEps || 0} <span className="text-xs text-slate-400 font-normal">evt/s</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-2 text-slate-400 text-sm font-medium">
            <Activity className="w-4 h-4 text-emerald-400" />
            P95 Latency
          </div>
          <div className="text-2xl font-bold mt-2 text-white">
            {health?.latencyP95 || 0} <span className="text-xs text-slate-400 font-normal">ms</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-2 text-slate-400 text-sm font-medium">
            <Layers className="w-4 h-4 text-amber-400" />
            Consumer Lag
          </div>
          <div className="text-2xl font-bold mt-2 text-white">
            {health?.consumerLag || 0} <span className="text-xs text-slate-400 font-normal">msg</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-2 text-slate-400 text-sm font-medium">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            Dead Letters
          </div>
          <div className="text-2xl font-bold mt-2 text-rose-400">
            {health?.deadLetterCount || deadLetters.length}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-2 text-slate-400 text-sm font-medium">
            <Shield className="w-4 h-4 text-indigo-400" />
            Error Rate
          </div>
          <div className="text-2xl font-bold mt-2 text-white">
            {((health?.errorRate || 0) * 100).toFixed(2)}%
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-6">
        <button
          onClick={() => setActiveTab('stream')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'stream'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Event Stream ({events.length})
        </button>
        <button
          onClick={() => setActiveTab('catalog')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'catalog'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Schema Catalog ({catalog.length})
        </button>
        <button
          onClick={() => setActiveTab('subscriptions')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'subscriptions'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Subscriptions ({subscriptions.length})
        </button>
        <button
          onClick={() => setActiveTab('deadletters')}
          className={`pb-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'deadletters'
              ? 'border-cyan-400 text-cyan-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Dead Letter Queue ({deadLetters.length})
        </button>
      </div>

      {/* Tab Contents */}
      {activeTab === 'stream' && (
        <div className="space-y-6">
          {/* Quick Publish Test Widget */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-cyan-400" />
              Event Publisher & Test Dispatcher
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="text-xs font-medium text-slate-400">Event Type</label>
                <select
                  value={pubEventType}
                  onChange={(e) => setPubEventType(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-cyan-500"
                >
                  {catalog.map((c) => (
                    <option key={c.eventType} value={c.eventType}>{c.eventType}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400">Source</label>
                <input
                  type="text"
                  value={pubSource}
                  onChange={(e) => setPubSource(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400">Subject</label>
                <input
                  type="text"
                  value={pubSubject}
                  onChange={(e) => setPubSubject(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400">Producer</label>
                <input
                  type="text"
                  value={pubProducer}
                  onChange={(e) => setPubProducer(e.target.value)}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-cyan-500"
                />
              </div>
            </div>

            <button
              onClick={handlePublishTestEvent}
              className="mt-4 px-5 py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-medium transition flex items-center gap-2"
            >
              <Zap className="w-4 h-4" />
              Publish Event Envelope
            </button>
          </div>

          {/* Event Stream List */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <h3 className="font-semibold text-white">Live Event Feed</h3>
              <div className="flex items-center gap-2">
                <ListFilter className="w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  placeholder="Filter by event type..."
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="bg-slate-950 border border-slate-800 rounded-md px-3 py-1 text-xs text-white"
                />
              </div>
            </div>

            <div className="divide-y divide-slate-800">
              {events
                .filter((e) => !filterType || e.eventType.includes(filterType))
                .map((e) => (
                  <div key={e.id} className="p-4 hover:bg-slate-800/50 transition space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="font-mono text-xs text-cyan-400 bg-cyan-950 border border-cyan-800 px-2.5 py-0.5 rounded-full">
                          {e.eventType}
                        </span>
                        <span className="text-xs text-slate-400 font-mono">
                          ID: {e.eventId}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-slate-400">
                        <span>{new Date(e.timestamp).toLocaleTimeString()}</span>
                        <button
                          onClick={() => handleReplayEvent(e.eventId)}
                          className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs transition flex items-center gap-1"
                        >
                          <RotateCcw className="w-3 h-3" /> Replay
                        </button>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs text-slate-300 pt-1">
                      <div><span className="text-slate-500">Producer:</span> {e.producer}</div>
                      <div><span className="text-slate-500">Source:</span> {e.source}</div>
                      <div><span className="text-slate-500">Subject:</span> {e.subject}</div>
                      <div><span className="text-slate-500">Classification:</span> <span className="text-emerald-400">{e.classification}</span></div>
                    </div>

                    <div className="bg-slate-950 p-2.5 rounded border border-slate-800/80 font-mono text-xs text-slate-400 overflow-x-auto">
                      PayloadRef: {JSON.stringify(e.payloadReference)}
                    </div>
                  </div>
                ))}
              {events.length === 0 && (
                <div className="p-8 text-center text-slate-500">No events recorded in feed.</div>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'catalog' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {catalog.map((item) => (
            <div key={item.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-white font-mono text-sm">{item.eventType}</h3>
                <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
                  v{item.version}
                </span>
              </div>
              <p className="text-slate-400 text-sm">{item.description}</p>
              <div className="flex items-center justify-between text-xs text-slate-500 border-t border-slate-800/80 pt-3">
                <div>Producer: <span className="text-slate-300">{item.producer}</span></div>
                <div>Retention: <span className="text-cyan-400">{item.retentionDays} days</span></div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'subscriptions' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 font-semibold text-white">
            Active Subscriptions
          </div>
          <div className="divide-y divide-slate-800">
            {subscriptions.map((sub) => (
              <div key={sub.id} className="p-4 flex items-center justify-between">
                <div>
                  <div className="font-mono text-sm font-semibold text-white">{sub.eventType}</div>
                  <div className="text-xs text-slate-400 mt-0.5">Consumer: {sub.consumer}</div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="px-2.5 py-0.5 bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs rounded-full">
                    Enabled
                  </span>
                </div>
              </div>
            ))}
            {subscriptions.length === 0 && (
              <div className="p-8 text-center text-slate-500">No subscriptions configured.</div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'deadletters' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 font-semibold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-rose-400" />
            Dead Letter Queue Inspector
          </div>
          <div className="divide-y divide-slate-800">
            {deadLetters.map((dl) => (
              <div key={dl.id} className="p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="font-mono text-xs text-rose-400 font-semibold">{dl.eventType}</div>
                  <div className="text-xs text-slate-500">{new Date(dl.createdAt).toLocaleString()}</div>
                </div>
                <div className="text-xs text-rose-300 font-mono bg-rose-950/40 p-2.5 rounded border border-rose-900/50">
                  Error: {dl.error}
                </div>
              </div>
            ))}
            {deadLetters.length === 0 && (
              <div className="p-8 text-center text-slate-500">Dead Letter Queue is clear. Zero failed events.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
