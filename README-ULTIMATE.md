# 🚀 Ultimate Ubuntu MCP Server

> **Complete Linux Development Environment via MCP Protocol**

[![MCP](https://img.shields.io/badge/MCP-Protocol-blue)](https://modelcontextprotocol.io/)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🎯 What is This?

একটা **সম্পূর্ণ Ubuntu Linux machine** যা তুমি **Claude (বা যেকোনো MCP client)** দিয়ে control করতে পারবে। 

### তুমি Claude কে বলবে:
```
"আমার জন্য একটা e-commerce website বানাও 
React frontend + Node.js backend + MySQL database সহ"
```

### Claude automatically করবে:
- ✅ Project structure তৈরি করবে
- ✅ Database setup করবে  
- ✅ Frontend + Backend code লিখবে
- ✅ Dependencies install করবে
- ✅ Nginx configure করবে
- ✅ SSL enable করবে
- ✅ Deploy করে live URL দেবে

**সব কিছু automatic!** ⚡

---

## ✨ Features

### 🛠️ **70+ Powerful Tools**

#### 📁 Project Management (4 tools)
- Create, delete, list, manage projects
- Support: Node.js, Python, PHP, Static HTML, Docker

#### 📝 File Operations (11 tools)  
- Read, write, delete, copy, move files
- Search files and content
- Permissions management

#### 📦 Package Management (5 tools)
- npm, pip, composer, apt
- Install, update, search packages

#### 🗄️ Database Management (7 tools)
- **MySQL**: Create DB, users, queries, backups
- **PostgreSQL**: Queries and management  
- **Redis**: Commands and caching
- **SQLite**: Built-in support

#### 🌐 Web Server (6 tools)
- **Nginx**: Auto-configuration, virtual hosts
- **SSL/HTTPS**: Let's Encrypt integration
- Domain management

#### ⚙️ Process Management (6 tools)
- **PM2**: Start, stop, restart apps
- Process monitoring
- Real-time logs

#### 🔄 Git Operations (6 tools)
- Clone, pull, push, commit
- Branch management
- Full version control

#### 🐳 Docker Operations (6 tools)
- Containers: run, stop, logs
- Images management
- Docker exec

#### 📊 System Monitoring (8 tools)
- CPU, Memory, Disk usage
- Network stats
- Port checking
- Top processes

#### 🌍 Network Tools (3 tools)
- Ping, HTTP requests
- File downloads

#### 🗜️ Compression (2 tools)
- Create/extract archives (tar.gz, zip)

#### 🔐 Security & Config (4 tools)
- Environment variables
- Cron jobs
- Firewall (UFW)

#### 💾 Backup & Restore (2 tools)
- Full project backups
- Database backups

---

## 🚀 Quick Start

### Option 1: Docker (Fastest - 5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/ubuntu-mcp-server.git
cd ubuntu-mcp-server

# 2. Create .env file
echo "MCP_API_KEY=$(openssl rand -hex 32)" > .env

# 3. Start with Docker Compose
docker-compose -f docker-compose.ultimate.yml up -d

# 4. Check health
curl http://localhost:8000/health

# 5. View logs
docker-compose -f docker-compose.ultimate.yml logs -f
```

**Done!** Server running at `http://localhost:8000` 🎉

---

### Option 2: Cloud VPS (Production - 15 minutes)

#### Step 1: Get a server
- **Hetzner Cloud** (Best value): €12/month for 4 CPU + 8GB RAM
- **DigitalOcean**: $24/month for 4GB RAM
- **AWS EC2**: t3.medium ~$30/month

#### Step 2: SSH into server
```bash
ssh root@your-server-ip
```

#### Step 3: Clone and install
```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/ubuntu-mcp-server.git
cd ubuntu-mcp-server

# Make installer executable
chmod +x install-ultimate.sh

# Run installation (takes ~10 minutes)
./install-ultimate.sh
```

This installs:
- ✅ Node.js 20.x, Python 3.11, PHP 8.2
- ✅ MySQL, PostgreSQL, Redis
- ✅ Nginx, Certbot (SSL)
- ✅ Docker, PM2
- ✅ All MCP server dependencies

#### Step 4: Configure and start
```bash
# Set your API key
nano /etc/systemd/system/mcp-server.service
# Change: Environment="MCP_API_KEY=your-secret-key-here"

# Reload and start
systemctl daemon-reload
systemctl start mcp-server
systemctl status mcp-server

# Check health
curl http://localhost:8000/health
```

#### Step 5: Configure firewall
```bash
# Firewall is auto-configured, but verify:
ufw status

# Should show:
# 22/tcp (SSH)
# 80/tcp (HTTP)  
# 443/tcp (HTTPS)
# 8000/tcp (MCP Server)
# 3000:9000/tcp (Apps)
```

**Production ready!** 🚀

---

## 🔌 Client Setup

### Claude Desktop

**1. Find config file:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**2. Edit config:**
```json
{
  "mcpServers": {
    "ubuntu-dev": {
      "url": "http://YOUR_SERVER_IP:8000/sse",
      "transport": "sse",
      "headers": {
        "X-API-Key": "your-secret-key"
      }
    }
  }
}
```

**3. Restart Claude Desktop**

**4. Test connection:**
```
"List all available tools on the ubuntu-dev server"
```

Claude should show 70+ tools! ✅

---

## 💡 Usage Examples

### Example 1: Simple Blog

**Tell Claude:**
```
Create a blog website with:
- Node.js + Express backend
- MySQL database  
- EJS templates for frontend
- CRUD for posts
- Deploy on port 3001
- Domain: blog.example.com
```

**Claude will execute ~15 tools automatically:**
1. `create_project` → Project structure
2. `mysql_create_database` → Database
3. `mysql_create_user` → DB user
4. `write_file` (multiple) → All code files
5. `npm_install` → Dependencies
6. `set_env_var` → Environment vars
7. `nginx_create_site` → Web server
8. `start_application` → Launch app
9. `enable_ssl` → HTTPS (if domain configured)

**Result:** Live blog at `https://blog.example.com` in 2-3 minutes! 🎉

---

### Example 2: REST API

**Tell Claude:**
```
Build a REST API with Python Flask and PostgreSQL for a todo app.
Features:
- User authentication (JWT)
- CRUD for todos
- Categories and tags
- Search and filtering
Port: 5000
```

**Claude handles everything** including:
- Flask app structure
- PostgreSQL setup
- SQLAlchemy models
- JWT authentication
- API endpoints
- Gunicorn deployment

---

### Example 3: Full Stack App

**Tell Claude:**
```
Create a full-stack e-commerce application:

Frontend:
- React 18 with Vite
- TailwindCSS
- Product catalog
- Shopping cart
- Checkout flow

Backend:
- Node.js + Express
- MySQL database
- REST API
- Stripe payment integration
- Admin dashboard

Deploy both on the same domain with proper routing
```

**Claude will:**
1. Create separate frontend/backend projects
2. Setup databases and tables
3. Write all React components
4. Write all API endpoints
5. Configure Nginx for SPA routing
6. Build frontend and serve static files
7. Deploy everything

**Completely autonomous development!** 🤯

---

## 📊 Server Requirements

### By Use Case

| Use Case | CPU | RAM | Disk | Cost/Month | Platform |
|----------|-----|-----|------|------------|----------|
| **Testing/Personal** | 2 cores | 2GB | 20GB | $5-12 | Hetzner CPX11 |
| **Small Projects (1-5)** | 2 cores | 4GB | 40GB | $12-15 | Hetzner CPX21 |
| **Medium (5-15 sites)** | 4 cores | 8GB | 80GB | $12-25 | Hetzner CPX31 ⭐ |
| **Production (20+ sites)** | 8 cores | 16GB | 160GB | $25-50 | Hetzner CPX41 |

**Recommended:** Hetzner CPX31 (4 CPU, 8GB RAM, €12/month) - Best value! 🏆

---

## 🔐 Security Features

- ✅ **API Key Authentication**: All requests require valid key
- ✅ **Command Blacklist**: Dangerous commands blocked
- ✅ **Firewall (UFW)**: Auto-configured
- ✅ **SSL/HTTPS**: Let's Encrypt integration
- ✅ **Isolated Projects**: Separate directories per project
- ✅ **Database Security**: User permissions properly set
- ✅ **Regular Updates**: Easy update mechanism

---

## 📚 Documentation

- **[ULTIMATE-GUIDE.md](./ULTIMATE-GUIDE.md)** - Complete documentation (150+ pages)
- **[API-REFERENCE.md](./API-REFERENCE.md)** - All 70+ tools documented
- **[DEPLOYMENT-GUIDE.md](./DEPLOYMENT-GUIDE.md)** - Step-by-step deployment
- **[WORKFLOW-EXAMPLES.md](./WORKFLOW-EXAMPLES.md)** - Real-world examples

---

## 🛠️ Technical Stack

### Server Side
- **MCP Protocol**: Communication layer
- **Python 3.11+**: Server implementation
- **Starlette + Uvicorn**: HTTP/SSE transport
- **Ubuntu 22.04**: Base OS

### Pre-installed Tools
- **Languages**: Node.js 20, Python 3.11, PHP 8.2
- **Databases**: MySQL 8, PostgreSQL 14, Redis, SQLite
- **Web Servers**: Nginx, Apache (optional)
- **Process Manager**: PM2
- **Containerization**: Docker + Docker Compose
- **SSL**: Certbot (Let's Encrypt)
- **Version Control**: Git

---

## 📁 Project Structure

```
ubuntu-mcp-server/
├── mcp-server-ultimate.py       # Main server (60KB, 70+ tools)
├── requirements-ultimate.txt    # Python dependencies
├── Dockerfile.ultimate          # Docker image
├── docker-compose.ultimate.yml  # Docker Compose
├── docker-entrypoint.sh         # Container startup
├── install-ultimate.sh          # VPS installation script
├── client-ultimate-example.py   # Client example (blog demo)
├── ULTIMATE-GUIDE.md            # Complete guide
└── README-ULTIMATE.md           # This file
```

---

## 🔧 Troubleshooting

### Server won't start
```bash
# Check logs
journalctl -u mcp-server -n 50

# Or for Docker
docker logs mcp-server

# Check port
netstat -tuln | grep 8000
```

### Can't connect from client
```bash
# Test health endpoint
curl http://YOUR_SERVER:8000/health

# Check firewall
ufw status

# Verify API key matches
echo $MCP_API_KEY
```

### Database issues
```bash
# MySQL
systemctl status mysql
mysql -u root -p

# PostgreSQL  
systemctl status postgresql
sudo -u postgres psql
```

### Out of memory
```bash
# Check usage
free -h

# Add swap
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add new tools
- Improve documentation
- Report bugs
- Suggest features

---

## 📄 License

MIT License - Free to use, modify, and distribute

---

## 🌟 Star History

If you find this useful, please ⭐ star the repository!

---

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) - Amazing protocol
- [Anthropic Claude](https://claude.ai/) - Best AI assistant
- Open Source Community - For all the great tools

---

## 📞 Support

**Issues?** Open a GitHub issue

**Questions?** Check [ULTIMATE-GUIDE.md](./ULTIMATE-GUIDE.md)

**Updates?** Watch this repo for new features

---

<div align="center">

### 🚀 Ready to build something amazing?

**Deploy now and let Claude build your next project!**

[Get Started](#-quick-start) • [Read Docs](./ULTIMATE-GUIDE.md) • [View Examples](./client-ultimate-example.py)

---

Made with ❤️ for developers who want to move fast

**Happy Building! 🎉**

</div>
