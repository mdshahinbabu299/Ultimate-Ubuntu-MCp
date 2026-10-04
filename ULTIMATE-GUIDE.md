# 🚀 Ultimate Ubuntu MCP Server - Complete Guide

## 🎯 What is This?

একটা **complete Linux development environment** যা MCP protocol এর মাধ্যমে control করা যায়। এটা দিয়ে তুমি:

- ✅ **যেকোনো ওয়েবসাইট তৈরি** করতে পারবে (Node, Python, PHP)
- ✅ **Database setup** করতে পারবে (MySQL, PostgreSQL, MongoDB, Redis)
- ✅ **Backend + Frontend** একসাথে host করতে পারবে
- ✅ **SSL সহ production-ready** deployment
- ✅ **Docker containers** চালাতে পারবে
- ✅ **Git operations**, package management, সবকিছু

## 🛠️ Features (70+ Tools)

### 📁 Project Management
- `create_project` - নতুন project তৈরি (Node/Python/PHP/Static)
- `delete_project` - Project মুছে ফেলা
- `list_projects` - সব projects দেখা
- `get_project_info` - Project details

### 📝 File Operations (11 tools)
- `read_file`, `write_file`, `delete_file`
- `copy_file`, `move_file`
- `list_directory`, `create_directory`
- `search_files`, `search_in_files`
- `get_file_info`, `change_permissions`

### 📦 Package Management (5 tools)
- `npm_install` - Node packages
- `pip_install` - Python packages
- `composer_install` - PHP packages
- `apt_install` - System packages
- `apt_search` - Package search

### 🗄️ Database Management (7 tools)
- `mysql_query`, `mysql_create_database`, `mysql_create_user`
- `mysql_list_databases`, `mysql_backup`
- `postgresql_query`
- `redis_command`

### 🌐 Web Server (6 tools)
- `nginx_create_site` - Nginx site setup
- `nginx_delete_site` - Site remove
- `nginx_list_sites` - Active sites
- `nginx_reload`, `nginx_test_config`
- `enable_ssl` - Let's Encrypt SSL

### ⚙️ Process Management (6 tools)
- `start_application` - PM2 দিয়ে app start
- `stop_application`, `restart_application`
- `list_processes`, `get_process_logs`
- `kill_process`

### 🔄 Git Operations (6 tools)
- `git_clone`, `git_pull`, `git_status`
- `git_commit`, `git_push`
- `git_branch` - Branch management

### 🐳 Docker Operations (6 tools)
- `docker_ps`, `docker_images`
- `docker_run`, `docker_stop`
- `docker_logs`, `docker_exec`

### 📊 System Monitoring (8 tools)
- `system_info` - Complete system info
- `cpu_usage`, `memory_usage`, `disk_usage`
- `network_stats`, `check_port`, `list_open_ports`
- `top_processes`

### 📜 Log Management (2 tools)
- `view_logs` - Log viewing
- `search_logs` - Log search

### 🌍 Network Tools (3 tools)
- `ping` - Network connectivity
- `curl_request` - HTTP requests
- `download_file` - File download

### 🗜️ Compression (2 tools)
- `compress_files` - tar.gz, zip
- `extract_archive` - Extract archives

### 🔐 Environment & Config (2 tools)
- `set_env_var` - Environment variables
- `get_env_vars` - View env vars

### ⏰ Cron & Scheduling (2 tools)
- `list_cron_jobs` - View cron jobs
- `add_cron_job` - Add scheduled tasks

### 💾 Backup & Restore (2 tools)
- `backup_project` - Full project backup
- `list_backups` - Available backups

### 🛠️ Utility (1 tool)
- `execute_command` - Any shell command

---

## 🚀 Deployment Options

### Option 1: Docker (Local Testing - Recommended)

#### Prerequisites
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

#### Quick Start
```bash
# 1. Clone/copy files
cd /path/to/project

# 2. Build image
docker build -f Dockerfile.ultimate -t ubuntu-mcp-ultimate .

# 3. Run container
docker run -d \
  --name mcp-server \
  --privileged \
  -p 8000:8000 \
  -p 80:80 \
  -p 443:443 \
  -p 3000-3010:3000-3010 \
  -e MCP_API_KEY=your-secret-key \
  -v $(pwd)/projects:/var/www \
  -v $(pwd)/backups:/var/backups/mcp \
  ubuntu-mcp-ultimate

# 4. Check health
curl http://localhost:8000/health

# 5. View logs
docker logs -f mcp-server
```

#### Docker Compose (Even Easier)
```bash
# 1. Set environment variables
echo "MCP_API_KEY=your-secret-key-here" > .env

# 2. Start everything
docker-compose -f docker-compose.ultimate.yml up -d

# 3. Check status
docker-compose -f docker-compose.ultimate.yml ps

# 4. View logs
docker-compose -f docker-compose.ultimate.yml logs -f

# 5. Stop
docker-compose -f docker-compose.ultimate.yml down
```

---

### Option 2: Cloud VPS (Hetzner/DigitalOcean)

#### Server Requirements
```
Minimum:
- CPU: 2 cores
- RAM: 4 GB
- Disk: 40 GB SSD
- Cost: ~$12/month

Recommended:
- CPU: 4 cores
- RAM: 8 GB
- Disk: 80 GB SSD
- Cost: ~$25/month (Hetzner CPX31: €12/month!)
```

#### Setup Steps

**1. Create VPS**
```bash
# Hetzner Cloud Console
# - Select Ubuntu 22.04
# - Choose CPX21 or CPX31
# - Add SSH key
# - Create server
```

**2. SSH into server**
```bash
ssh root@your-server-ip
```

**3. Run installation script**
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ubuntu-mcp-server.git
cd ubuntu-mcp-server

# Make scripts executable
chmod +x install-ultimate.sh

# Run installation
./install-ultimate.sh

# This will:
# - Install all dependencies (Node, Python, PHP, databases)
# - Setup Nginx
# - Configure firewall
# - Install SSL tools
# - Setup MCP server
```

**4. Configure environment**
```bash
# Set API key
echo "MCP_API_KEY=your-super-secret-key" >> /etc/environment
source /etc/environment
```

**5. Start server**
```bash
# Using systemd (auto-start on boot)
sudo systemctl enable mcp-server
sudo systemctl start mcp-server

# Or using PM2
pm2 start mcp-server-ultimate.py --name mcp-server --interpreter python3
pm2 save
pm2 startup
```

**6. Configure firewall**
```bash
# Allow necessary ports
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw allow 8000/tcp # MCP Server
ufw allow 3000:9000/tcp # Application ports
ufw enable
```

**7. Setup domain (optional)**
```bash
# Point your domain to server IP
# Then configure Nginx
nginx_create_site domain=mcp.yourdomain.com port=8000 type=proxy

# Enable SSL
enable_ssl domain=mcp.yourdomain.com email=you@email.com
```

---

### Option 3: Railway/Render (Simplified Cloud)

⚠️ **Limitation**: Full features (Docker, databases) won't work on free tier

Best for: Testing MCP protocol only

```bash
# Use simplified version
cp mcp-server.py railway-server.py
# Remove Docker/database features
# Deploy to Railway
```

---

## 🔌 Client Configuration

### Claude Desktop

**Config file location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "ubuntu-dev": {
      "url": "http://your-server-ip:8000/sse",
      "transport": "sse",
      "headers": {
        "X-API-Key": "your-secret-key"
      }
    }
  }
}
```

**For domain with SSL:**
```json
{
  "mcpServers": {
    "ubuntu-dev": {
      "url": "https://mcp.yourdomain.com/sse",
      "transport": "sse",
      "headers": {
        "X-API-Key": "your-secret-key"
      }
    }
  }
}
```

---

## 💡 Usage Examples

### Example 1: Create a Node.js Blog

**Tell Claude:**
```
"Create a blog website with Node.js, Express, and MySQL.
The blog should have:
- Posts with title, content, author
- Comments system
- REST API
- Admin panel

Domain: blog.example.com
Port: 3001"
```

**Claude will automatically:**
1. `create_project(name="blog", stack="node", port=3001)`
2. `mysql_create_database(name="blog_db")`
3. `mysql_create_user(username="blog_user", password="...", database="blog_db")`
4. Write all code files (server.js, models, routes, views)
5. `npm_install(project="blog", packages="express mysql2 ejs")`
6. `set_env_var(project="blog", key="DB_HOST", value="localhost")`
7. `nginx_create_site(domain="blog.example.com", port=3001)`
8. `enable_ssl(domain="blog.example.com", email="you@email.com")`
9. `start_application(name="blog", script="server.js", cwd="/var/www/blog")`

**Result:** Live at `https://blog.example.com` ✨

---

### Example 2: Deploy Python Flask API

**Tell Claude:**
```
"Build a REST API with Flask and PostgreSQL for a task manager.
Features:
- User authentication
- CRUD for tasks
- Task assignment
- Due dates

Domain: api.tasks.com
Port: 5000"
```

**Claude will:**
1. Create Flask project
2. Setup PostgreSQL database
3. Write API endpoints
4. Install dependencies
5. Configure Nginx
6. Deploy with Gunicorn

---

### Example 3: E-commerce Site

**Tell Claude:**
```
"Create a full e-commerce website with:
- React frontend
- Node.js backend
- MySQL database
- Payment integration (Stripe)
- Admin dashboard
- Product catalog
- Shopping cart
- Order management

Domain: shop.example.com"
```

**Claude will handle everything end-to-end!**

---

## 🔐 Security Best Practices

### 1. Strong API Key
```bash
# Generate secure key
openssl rand -hex 32

# Set it
export MCP_API_KEY="generated-key-here"
```

### 2. Firewall Configuration
```bash
# Only allow necessary ports
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp
ufw enable
```

### 3. Database Security
```bash
# MySQL
mysql_secure_installation

# PostgreSQL
# Edit /etc/postgresql/*/main/pg_hba.conf
# Set authentication to md5
```

### 4. Regular Updates
```bash
# System updates
apt update && apt upgrade -y

# Package updates
npm update -g
pip install --upgrade pip
```

### 5. SSL Certificates
```bash
# Always use HTTPS in production
enable_ssl domain=yourdomain.com email=you@email.com

# Auto-renewal (certbot does this automatically)
certbot renew --dry-run
```

---

## 📊 Monitoring & Maintenance

### Check Server Health
```bash
curl http://localhost:8000/health
```

### View System Stats
```bash
# CPU & Memory
top
htop

# Disk usage
df -h

# Network
netstat -tuln
```

### Application Logs
```bash
# PM2 logs
pm2 logs

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# System logs
journalctl -u mcp-server -f
```

### Backup
```bash
# Backup all projects
for project in /var/www/*; do
  backup_project(project=$(basename $project), include_db=true)
done

# Or via MCP
# Tell Claude: "Backup all projects"
```

---

## 🆘 Troubleshooting

### Server won't start
```bash
# Check logs
journalctl -u mcp-server -n 50

# Check port availability
netstat -tuln | grep 8000

# Kill conflicting process
kill $(lsof -t -i:8000)
```

### Database connection failed
```bash
# Check MySQL
systemctl status mysql
systemctl restart mysql

# Check PostgreSQL
systemctl status postgresql
systemctl restart postgresql
```

### Nginx errors
```bash
# Test configuration
nginx -t

# Check error log
tail -f /var/log/nginx/error.log

# Restart
systemctl restart nginx
```

### Out of memory
```bash
# Check memory
free -h

# Add swap
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

---

## 💰 Cost Breakdown

### Hetzner Cloud (Best Value)
```
CPX21 (2 vCPU, 4GB RAM): €5.83/month
CPX31 (4 vCPU, 8GB RAM): €11.90/month  ⭐ Recommended
CPX41 (8 vCPU, 16GB RAM): €23.90/month
```

### DigitalOcean
```
2GB RAM: $12/month
4GB RAM: $24/month
8GB RAM: $48/month
```

### AWS EC2
```
t3.medium (2 vCPU, 4GB): ~$30/month
t3.large (2 vCPU, 8GB): ~$60/month
```

**Recommendation:** Hetzner CPX31 (€12/month) - best performance per dollar

---

## 🎓 Next Steps

1. ✅ Deploy server (Docker or VPS)
2. ✅ Configure Claude Desktop
3. ✅ Test with simple project
4. ✅ Build your first full website
5. 🚀 Scale and optimize

---

## 📚 Additional Resources

- MCP Protocol: https://modelcontextprotocol.io/
- Hetzner Cloud: https://www.hetzner.com/cloud
- PM2 Docs: https://pm2.keymetrics.io/
- Nginx Docs: https://nginx.org/en/docs/
- Let's Encrypt: https://letsencrypt.org/

---

## 🤝 Support

Issues? Questions?
- Check troubleshooting section
- Review logs
- Test individual tools

Enjoy building! 🎉
