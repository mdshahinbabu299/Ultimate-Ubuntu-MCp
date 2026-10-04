# Ultimate Ubuntu MCP Server - Complete Development Environment
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install system packages
RUN apt-get update && apt-get install -y \
    # Build essentials
    build-essential \
    curl \
    wget \
    git \
    vim \
    nano \
    unzip \
    zip \
    tar \
    gzip \
    # System tools
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    # Network tools
    net-tools \
    iputils-ping \
    netcat \
    dnsutils \
    # Process tools
    htop \
    ps misc \
    procps \
    # Node.js (via NodeSource)
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    # Python 3.11
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y python3.11 python3.11-venv python3-pip \
    # PHP 8.2
    && add-apt-repository ppa:ondrej/php -y \
    && apt-get update \
    && apt-get install -y php8.2 php8.2-cli php8.2-common php8.2-mysql php8.2-zip php8.2-gd php8.2-mbstring php8.2-curl php8.2-xml \
    # Databases
    && apt-get install -y \
    mysql-server \
    mysql-client \
    postgresql \
    postgresql-contrib \
    redis-server \
    sqlite3 \
    # Web servers
    nginx \
    # Docker
    && curl -fsSL https://get.docker.com -o get-docker.sh \
    && sh get-docker.sh \
    && rm get-docker.sh \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Composer (PHP)
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Install PM2 (Process Manager)
RUN npm install -g pm2 yarn pnpm

# Install Python packages
RUN pip3 install --no-cache-dir \
    pip --upgrade \
    setuptools \
    wheel

# Install Certbot for SSL
RUN apt-get update && apt-get install -y certbot python3-certbot-nginx && apt-get clean

# Create application directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY mcp-server-ultimate.py .

# Create necessary directories
RUN mkdir -p /var/www /var/log/mcp /var/backups/mcp \
    && chmod 755 /var/www /var/log/mcp /var/backups/mcp

# Configure MySQL
RUN service mysql start && \
    mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';" && \
    mysql -e "FLUSH PRIVILEGES;" && \
    service mysql stop

# Configure PostgreSQL
RUN service postgresql start && \
    su - postgres -c "psql -c \"ALTER USER postgres PASSWORD 'postgres';\"" && \
    service postgresql stop

# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default

# Expose ports
EXPOSE 8000 80 443 3000-9000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Startup script
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python3", "mcp-server-ultimate.py"]
