#!/usr/bin/env bash
set -e

echo "=== Initializing Vapor OS Platform Foundation ==="

echo "1. Installing Node dependencies..."
npm install

echo "2. Building shared packages..."
npm run build

echo "3. Starting Docker services (PostgreSQL & Redis)..."
docker-compose up -d postgres redis

echo "=== System Ready. Run 'npm run dev' to boot Vapor OS ==="
