/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@vapor/ui', '@vapor/types', '@vapor/ai', '@vapor/utils'],
  env: {
    NEXT_PUBLIC_GOOGLE_CLIENT_ID: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '381940932694-o2q57f2bhp8sjbt9r6fgm240q4jknmfa.apps.googleusercontent.com',
  },
  async redirects() {
    return [
      { source: '/queue', destination: '/work', permanent: false },
      { source: '/strategic-intelligence', destination: '/strategy', permanent: false },
      { source: '/strategic-foresight', destination: '/foresight', permanent: false },
      { source: '/portfolio-intelligence', destination: '/portfolio', permanent: false },
      { source: '/execution-governance', destination: '/execution', permanent: false },
      { source: '/operating-map', destination: '/organization', permanent: false },
      { source: '/graph', destination: '/knowledge/graph', permanent: false },
      { source: '/intelligence-governance', destination: '/knowledge/governance', permanent: false },
      { source: '/evals', destination: '/ai/evaluation', permanent: false },
      { source: '/models', destination: '/ai/models', permanent: false },
    ];
  },
  async rewrites() {
    // Development default is 127.0.0.1:8000; Production & Staging targets are configured via API_PROXY_TARGET or API_INTERNAL_URL
    const backendOrigin = process.env.API_PROXY_TARGET || process.env.API_INTERNAL_URL || 'http://127.0.0.1:8000';
    
    return [
      {
        source: '/api/v1/:path*',
        destination: `${backendOrigin}/api/v1/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
