/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@vapor/ui', '@vapor/types', '@vapor/ai', '@vapor/utils'],
};

module.exports = nextConfig;
