/**
 * Vapor OS - Real-Application Full Route & API E2E Acceptance Test Suite
 */
const http = require('http');

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000';

const NAVIGATION_ROUTES = [
  // Command & Briefing (11)
  { label: 'Executive Brief', path: '/' },
  { label: 'Attention Inbox', path: '/attention' },
  { label: 'Autonomous Missions', path: '/missions' },
  { label: 'Work Queue', path: '/work' },
  { label: 'Strategic Intelligence', path: '/strategy' },
  { label: 'Strategic Foresight', path: '/foresight' },
  { label: 'Portfolio Intelligence', path: '/portfolio' },
  { label: 'Execution Governance', path: '/execution' },
  { label: 'Operating Model', path: '/operating-model' },
  { label: 'Collaboration Center', path: '/collaboration' },
  { label: 'Operating Map', path: '/organization' },
  
  // Intelligence & Context (9)
  { label: 'Content Studio', path: '/content' },
  { label: 'Gmail Triage', path: '/gmail' },
  { label: 'Drive Browser', path: '/drive' },
  { label: 'Memory Vault', path: '/memory' },
  { label: 'Enterprise Knowledge', path: '/knowledge' },
  { label: 'Semantic Graph', path: '/knowledge/graph' },
  { label: 'Intelligence Governance', path: '/knowledge/governance' },
  { label: 'AI Evaluation', path: '/ai/evaluation' },
  { label: 'AI Models', path: '/ai/models' },

  // Automation & Agents (12)
  { label: 'Automations', path: '/automations' },
  { label: 'Workflows', path: '/workflows' },
  { label: 'Workflow Optimization', path: '/workflows/optimization' },
  { label: 'AI Agent Mesh', path: '/agents/mesh' },
  { label: 'Agent Skill Fabric', path: '/agents/skills' },
  { label: 'Capability Registry', path: '/capabilities' },
  { label: 'Agent Executions 2.0', path: '/agents/executions/exec_demo_01' },
  { label: 'Decision Engine 2.0', path: '/decisions' },
  { label: 'Decision Intelligence', path: '/intelligence' },
  { label: 'Decision Learning 2.0', path: '/transformation-decision-learning' },
  { label: 'Prescriptive Intelligence', path: '/optimization' },
  { label: 'Predictive Operations', path: '/predictions' },

  // Resilience & Operations (23)
  { label: 'Resilience Command Center', path: '/transformation-resilience-command-center' },
  { label: 'Transformation Control', path: '/transformation-control' },
  { label: 'Transformation Intelligence', path: '/transformation-intelligence' },
  { label: 'Transformation Foresight', path: '/transformation-foresight' },
  { label: 'Transformation Decisions', path: '/transformation-decisions' },
  { label: 'Transformation Portfolio', path: '/transformation-portfolio' },
  { label: 'Digital Twin Simulation', path: '/transformation-simulation' },
  { label: 'Transformation War Room', path: '/transformation-war-room' },
  { label: 'Transformation Recovery', path: '/transformation-recovery' },
  { label: 'Resilience Engineering', path: '/transformation-resilience-engineering' },
  { label: 'Adaptive Governance', path: '/transformation-governance' },
  { label: 'Crisis Operations', path: '/crisis' },
  { label: 'Threat Intelligence', path: '/threats' },
  { label: 'Global Operations', path: '/operations' },
  { label: 'FinOps & Cloud Infra', path: '/finops' },
  { label: 'Enterprise Governance', path: '/admin/governance' },
  { label: 'Enterprise Identity & SSO', path: '/admin/identity' },
  { label: 'Enterprise Data Security', path: '/admin/data' },
  { label: 'SecOps Operations Center', path: '/security/operations' },
  { label: 'Agent Security Fabric', path: '/security' },
  { label: 'Integrations Hub', path: '/integrations' },
  { label: 'Event Mesh', path: '/admin/events' },
  { label: 'Settings Console', path: '/settings' },
];

const HISTORICAL_REDIRECTS = [
  { from: '/queue', expectedTo: '/work' },
  { from: '/strategic-intelligence', expectedTo: '/strategy' },
  { from: '/strategic-foresight', expectedTo: '/foresight' },
  { from: '/portfolio-intelligence', expectedTo: '/portfolio' },
  { from: '/execution-governance', expectedTo: '/execution' },
  { from: '/operating-map', expectedTo: '/organization' },
  { from: '/graph', expectedTo: '/knowledge/graph' },
  { from: '/intelligence-governance', expectedTo: '/knowledge/governance' },
  { from: '/evals', expectedTo: '/ai/evaluation' },
  { from: '/models', expectedTo: '/ai/models' },
];

const API_ENDPOINTS = [
  { path: '/api/v1/health', expectedStatus: 200 },
  { path: '/api/v1/home/brief?user_name=Alex', expectedStatus: 200 },
  { path: '/api/v1/attention/count', expectedStatus: 200 },
  { path: '/api/v1/attention', expectedStatus: 200 },
  { path: '/api/v1/missions', expectedStatus: 200 },
  { path: '/api/v1/memories', expectedStatus: 200 },
  { path: '/api/v1/content', expectedStatus: 200 },
  { path: '/api/v1/gmail/status', expectedStatus: 200 },
  { path: '/api/v1/drive/status', expectedStatus: 200 },
  { path: '/api/v1/integrations', expectedStatus: 200 },
  { path: '/api/v1/search?q=test', expectedStatus: 200 },
];

function fetchUrl(url, options = {}) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const req = http.request(
      {
        hostname: parsed.hostname,
        port: parsed.port,
        path: parsed.pathname + parsed.search,
        method: options.method || 'GET',
        headers: {
          'X-Workspace-Id': 'ws_default_01',
          'X-User-Id': 'usr_alex',
          ...(options.headers || {}),
        },
      },
      (res) => {
        let body = '';
        res.on('data', (chunk) => (body += chunk));
        res.on('end', () => {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body,
          });
        });
      }
    );
    req.on('error', reject);
    req.setTimeout(35000, () => {
      req.destroy();
      reject(new Error(`Timeout (35s) fetching ${url}`));
    });
    if (options.body) {
      req.write(options.body);
    }
    req.end();
  });
}

async function runE2EAcceptance() {
  console.log('===============================================================');
  console.log('  VAPOR OS — FULL REAL-APPLICATION E2E ACCEPTANCE SUITE');
  console.log('===============================================================\n');

  let passed = 0;
  let failed = 0;

  // 1. Stack Health Check
  console.log('[1/5] Checking Stack Connectivity...');
  try {
    const fe = await fetchUrl(BASE_URL);
    console.log(`  ✓ Frontend listening at ${BASE_URL} (HTTP ${fe.statusCode})`);
    passed++;
  } catch (err) {
    console.error(`  ✗ Frontend unreachable: ${err.message}`);
    failed++;
  }

  try {
    const be = await fetchUrl(`${BACKEND_URL}/api/v1/health`);
    console.log(`  ✓ Backend listening at ${BACKEND_URL} (HTTP ${be.statusCode})`);
    passed++;
  } catch (err) {
    console.error(`  ✗ Backend unreachable: ${err.message}`);
    failed++;
  }

  // 2. Navigation Routes Check (55/55)
  console.log('\n[2/5] Testing All 55 Navigation Routes from AppShell...');
  for (const route of NAVIGATION_ROUTES) {
    try {
      const res = await fetchUrl(`${BASE_URL}${route.path}`);
      if (res.statusCode === 200) {
        console.log(`  ✓ [${route.label}] ${route.path} -> 200 OK (${res.body.length} bytes)`);
        passed++;
      } else {
        console.error(`  ✗ [${route.label}] ${route.path} -> Unexpected HTTP ${res.statusCode}`);
        failed++;
      }
    } catch (err) {
      console.error(`  ✗ [${route.label}] ${route.path} -> ${err.message}`);
      failed++;
    }
  }

  // 3. Historical Redirects Check (10/10)
  console.log('\n[3/5] Testing 10 Historical Route Redirects...');
  for (const redir of HISTORICAL_REDIRECTS) {
    try {
      const res = await fetchUrl(`${BASE_URL}${redir.from}`);
      const loc = res.headers['location'];
      if (res.statusCode === 307 && loc === redir.expectedTo) {
        console.log(`  ✓ ${redir.from} -> 307 Redirect to ${loc}`);
        passed++;
      } else {
        console.error(`  ✗ ${redir.from} -> HTTP ${res.statusCode}, Location: ${loc} (expected ${redir.expectedTo})`);
        failed++;
      }
    } catch (err) {
      console.error(`  ✗ ${redir.from} -> ${err.message}`);
      failed++;
    }
  }

  // 4. Nonexistent Route 404 Check
  console.log('\n[4/5] Testing 404 Experience for Nonexistent Route...');
  try {
    const res = await fetchUrl(`${BASE_URL}/route-that-genuinely-does-not-exist-998877`);
    if (res.statusCode === 404 && res.body.includes('Resource Not Found')) {
      console.log(`  ✓ Nonexistent route returns HTTP 404 with custom 404 UI (${res.body.length} bytes)`);
      passed++;
    } else {
      console.error(`  ✗ Nonexistent route returned HTTP ${res.statusCode}`);
      failed++;
    }
  } catch (err) {
    console.error(`  ✗ 404 test failed: ${err.message}`);
    failed++;
  }

  // 5. API Proxy & Backend Endpoints Check
  console.log('\n[5/5] Testing API Proxying via Next.js (/api/v1/*)...');
  for (const api of API_ENDPOINTS) {
    try {
      const res = await fetchUrl(`${BASE_URL}${api.path}`);
      if (res.statusCode === api.expectedStatus) {
        console.log(`  ✓ [Proxy] ${api.path} -> HTTP ${res.statusCode}`);
        passed++;
      } else {
        console.error(`  ✗ [Proxy] ${api.path} -> HTTP ${res.statusCode} (expected ${api.expectedStatus})`);
        failed++;
      }
    } catch (err) {
      console.error(`  ✗ [Proxy] ${api.path} -> ${err.message}`);
      failed++;
    }
  }

  console.log('\n===============================================================');
  console.log(`  E2E ACCEPTANCE SUMMARY: ${passed} PASSED, ${failed} FAILED`);
  console.log('===============================================================');

  if (failed > 0) {
    process.exit(1);
  }
}

runE2EAcceptance();
