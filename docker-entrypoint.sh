#!/bin/bash
set -e

echo "🚀 Starting Ultimate Ubuntu MCP Server..."

# Start MySQL
echo "📦 Starting MySQL..."
service mysql start

# Start PostgreSQL
echo "📦 Starting PostgreSQL..."
service postgresql start

# Start Redis
echo "📦 Starting Redis..."
service redis-server start

# Start Nginx
echo "🌐 Starting Nginx..."
service nginx start

# Start Docker daemon (if not running in privileged mode, this might fail)
if [ -S /var/run/docker.sock ]; then
    echo "🐳 Docker socket found"
else
    echo "⚠️  Docker socket not found (run with --privileged for Docker support)"
fi

echo "✅ All services started"
echo ""

# Execute the main command
exec "$@"
