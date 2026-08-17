/**
 * Vapor OS - Failure-State Truthfulness Verification Script
 */
const { apiClient, ApiError, ApiConnectionError } = require('./src/lib/api/client');

async function testFailureTruthfulness() {
  console.log('Testing Failure-State Truthfulness...');

  // 1. Test against non-existent port (simulating backend down)
  process.env.NEXT_PUBLIC_API_URL = 'http://127.0.0.1:59999/api/v1';
  let failureCaught = false;
  try {
    await apiClient('/home/brief');
  } catch (err) {
    failureCaught = true;
    console.log(`  ✓ Unreachable backend correctly threw error: [${err.name}] ${err.message}`);
    if (err instanceof ApiError && err.status === 503) {
      console.log('  ✓ Error classified as 503 CONNECTION_REFUSED (truthful error state)');
    }
  }

  if (!failureCaught) {
    console.error('  ✗ Failure was silently swallowed!');
    process.exit(1);
  }

  // 2. Restore healthy backend URL
  process.env.NEXT_PUBLIC_API_URL = 'http://localhost:3000/api/v1';
  try {
    const data = await apiClient('/home/brief?user_name=Alex');
    console.log(`  ✓ Restored backend successfully returned: greeting="${data.greeting}"`);
    console.log('  ✓ Retry -> Success verified cleanly!');
  } catch (err) {
    console.error(`  ✗ Restored connection failed: ${err.message}`);
    process.exit(1);
  }

  console.log('Failure-State Truthfulness: PASSED');
}

testFailureTruthfulness();
