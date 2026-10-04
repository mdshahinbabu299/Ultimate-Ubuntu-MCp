#!/bin/bash

# Ultimate Ubuntu MCP Server Installation Script
# For Ubuntu 22.04 LTS

set -e

echo "="*70
echo "🚀 Ultimate Ubuntu MCP Server Installation"
echo "="*70
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root or with sudo"
    exit 1
fi

echo "📋 System: $(lsb_release -ds)"
echo ""

# Update system
echo "📦 Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq

# Install basic tools
echo "🔧 Installing basic tools..."
apt-get install -y -qq \
    curl \
    wget \
    git \
    vim \
    nano \
    unzip \
    zip \
    tar \
    gzip \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    net-tools \
    iputils-ping \
    netcat \
    htop \
    python3-pip

echo "✅ Basic tools installed"

# Install Node.js 20.x
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash - > /dev/null 2>&1
apt-get install -y -qq nodejs
echo "✅ Node.js $(node --version) installed"

# Install Python 3.11
echo "📦 Installing Python 3.11..."
add-apt-repository ppa:deadsnakes/ppa -y > /dev/null 2>&1
apt-get update -qq
apt-get install -y -qq python3.11 python3.11-venv python3.11-dev
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
echo "✅ Python $(python3 --version) installed"

# Install PHP 8.2
echo "📦 Installing PHP 8.2..."
add-apt-repository ppa:ondrej/php -y > /dev/null 2>&1
apt-get update -qq
apt-get install -y -qq \
    php8.2 \
    php8.2-cli \
    php8.2-fpm \
    php8.2-mysql \
    php8.2-pgsql \
    php8.2-sqlite3 \
    php8.2-redis \
    php8.2-zip \
    php8.2-gd \
    php8.2-mbstring \
    php8.2-curl \
    php8.2-xml
echo "✅ PHP $(php --version | head -n1) installed"

# Install Composer
echo "📦 Installing Composer..."
curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer > /dev/null 2>&1
echo "✅ Composer installed"

# Install MySQL
echo "📦 Installing MySQL..."
export DEBIAN_FRONTEND=noninteractive
apt-get install -y -qq mysql-server mysql-client
systemctl start mysql
systemctl enable mysql
echo "✅ MySQL installed"

# Secure MySQL (basic)
echo "🔐 Configuring MySQL..."
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';"
mysql -e "DELETE FROM mysql.user WHERE User='';"
mysql -e "DROP DATABASE IF EXISTS test;"
mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
mysql -e "FLUSH PRIVILEGES;"
echo "✅ MySQL configured"

# Install PostgreSQL
echo "📦 Installing PostgreSQL..."
apt-get install -y -qq postgresql postgresql-contrib
systemctl start postgresql
systemctl enable postgresql
echo "✅ PostgreSQL installed"

# Configure PostgreSQL
echo "🔐 Configuring PostgreSQL..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" > /dev/null 2>&1
echo "✅ PostgreSQL configured"

# Install Redis
echo "📦 Installing Redis..."
apt-get install -y -qq redis-server
systemctl start redis-server
systemctl enable redis-server
echo "✅ Redis installed"

# Install MongoDB (optional, commented out for faster install)
# echo "📦 Installing MongoDB..."
# curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
# echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
# apt-get update -qq
# apt-get install -y -qq mongodb-org
# systemctl start mongod
# systemctl enable mongod
# echo "✅ MongoDB installed"

# Install Nginx
echo "📦 Installing Nginx..."
apt-get install -y -qq nginx
systemctl start nginx
systemctl enable nginx
rm -f /etc/nginx/sites-enabled/default
echo "✅ Nginx installed"

# Install Certbot for SSL
echo "📦 Installing Certbot..."
apt-get install -y -qq certbot python3-certbot-nginx
echo "✅ Certbot installed"

# Install Docker
echo "📦 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh > /dev/null 2>&1
rm get-docker.sh
systemctl start docker
systemctl enable docker
echo "✅ Docker installed"

# Install Docker Compose
echo "📦 Installing Docker Compose..."
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
echo "✅ Docker Compose installed"

# Install PM2
echo "📦 Installing PM2..."
npm install -g pm2 yarn pnpm --silent
echo "✅ PM2 installed"

# Install Python packages
echo "📦 Installing Python packages..."
pip3 install --quiet --no-cache-dir -r requirements-ultimate.txt
echo "✅ Python packages installed"

# Create directories
echo "📁 Creating directories..."
mkdir -p /var/www
mkdir -p /var/log/mcp
mkdir -p /var/backups/mcp
chmod 755 /var/www /var/log/mcp /var/backups/mcp
echo "✅ Directories created"

# Configure firewall
echo "🔥 Configuring firewall..."
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw allow 8000/tcp comment 'MCP Server'
ufw allow 3000:9000/tcp comment 'Application ports'
echo "✅ Firewall configured"

# Create systemd service
echo "⚙️  Creating systemd service..."
cat > /etc/systemd/system/mcp-server.service << 'EOF'
[Unit]
Description=Ultimate Ubuntu MCP Server
After=network.target mysql.service postgresql.service redis-server.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/mcp-server
Environment="MCP_API_KEY=change-this-secret-key"
Environment="PORT=8000"
ExecStart=/usr/bin/python3 /opt/mcp-server/mcp-server-ultimate.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Copy server file
mkdir -p /opt/mcp-server
cp mcp-server-ultimate.py /opt/mcp-server/
chmod +x /opt/mcp-server/mcp-server-ultimate.py

# Enable service
systemctl daemon-reload
systemctl enable mcp-server

echo "✅ Systemd service created"

echo ""
echo "="*70
echo "✅ Installation Complete!"
echo "="*70
echo ""
echo "📋 Installed Components:"
echo "   - Node.js $(node --version)"
echo "   - Python $(python3 --version | cut -d' ' -f2)"
echo "   - PHP $(php -v | head -n1 | cut -d' ' -f2)"
echo "   - MySQL $(mysql --version | cut -d' ' -f6 | cut -d',' -f1)"
echo "   - PostgreSQL $(psql --version | cut -d' ' -f3)"
echo "   - Redis $(redis-server --version | cut -d' ' -f3 | cut -d'=' -f2)"
echo "   - Nginx $(nginx -v 2>&1 | cut -d'/' -f2)"
echo "   - Docker $(docker --version | cut -d' ' -f3 | tr -d ',')"
echo "   - PM2 $(pm2 --version)"
echo ""
echo "🔧 Next Steps:"
echo ""
echo "1. Set your API key:"
echo "   nano /etc/systemd/system/mcp-server.service"
echo "   (Change MCP_API_KEY value)"
echo ""
echo "2. Start the MCP server:"
echo "   systemctl start mcp-server"
echo ""
echo "3. Check status:"
echo "   systemctl status mcp-server"
echo ""
echo "4. View logs:"
echo "   journalctl -u mcp-server -f"
echo ""
echo "5. Test the server:"
echo "   curl http://localhost:8000/health"
echo ""
echo "6. Configure your client with:"
echo "   URL: http://$(curl -s ifconfig.me):8000/sse"
echo "   API Key: (your secret key)"
echo ""
echo "📚 Read ULTIMATE-GUIDE.md for complete documentation"
echo ""
echo "🎉 Happy building!"
echo "="*70
