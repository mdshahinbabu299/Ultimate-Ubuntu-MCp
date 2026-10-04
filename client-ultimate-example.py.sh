#!/usr/bin/env python3
"""
Ultimate MCP Client Example
Demonstrates building a complete website using the MCP server
"""

import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client

# Configuration
SERVER_URL = "http://your-server-ip:8000/sse"  # Change this
API_KEY = "your-secret-key"  # Change this


async def create_blog_website():
    """
    Complete example: Create a Node.js blog with MySQL
    """
    print("🚀 Creating a complete blog website...\n")
    
    async with sse_client(url=SERVER_URL, headers={"X-API-Key": API_KEY}) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Create project
            print("📁 Step 1: Creating project structure...")
            result = await session.call_tool(
                "create_project",
                arguments={"name": "myblog", "stack": "node", "port": 3001}
            )
            print(result.content[0].text)
            print()
            
            # 2. Create database
            print("🗄️  Step 2: Creating MySQL database...")
            result = await session.call_tool(
                "mysql_create_database",
                arguments={"name": "myblog_db", "charset": "utf8mb4"}
            )
            print(result.content[0].text)
            print()
            
            # 3. Create database user
            print("👤 Step 3: Creating database user...")
            result = await session.call_tool(
                "mysql_create_user",
                arguments={
                    "username": "blog_user",
                    "password": "secure_password_123",
                    "database": "myblog_db"
                }
            )
            print(result.content[0].text)
            print()
            
            # 4. Write package.json
            print("📦 Step 4: Writing package.json...")
            package_json = json.dumps({
                "name": "myblog",
                "version": "1.0.0",
                "description": "A simple blog application",
                "main": "server.js",
                "scripts": {
                    "start": "node server.js",
                    "dev": "nodemon server.js"
                },
                "dependencies": {
                    "express": "^4.18.2",
                    "mysql2": "^3.6.0",
                    "dotenv": "^16.3.1",
                    "ejs": "^3.1.9",
                    "body-parser": "^1.20.2"
                }
            }, indent=2)
            
            result = await session.call_tool(
                "write_file",
                arguments={
                    "path": "/var/www/myblog/package.json",
                    "content": package_json
                }
            )
            print(result.content[0].text)
            print()
            
            # 5. Write server.js
            print("💻 Step 5: Writing server code...")
            server_code = '''const express = require('express');
const mysql = require('mysql2/promise');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Database connection
const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'blog_user',
  password: process.env.DB_PASSWORD || 'secure_password_123',
  database: process.env.DB_NAME || 'myblog_db',
  waitForConnections: true,
  connectionLimit: 10
});

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));
app.set('view engine', 'ejs');

// Routes
app.get('/', async (req, res) => {
  try {
    const [posts] = await pool.query('SELECT * FROM posts ORDER BY created_at DESC LIMIT 10');
    res.render('index', { posts });
  } catch (error) {
    res.status(500).json({ error: 'Database error' });
  }
});

app.get('/api/posts', async (req, res) => {
  try {
    const [posts] = await pool.query('SELECT * FROM posts ORDER BY created_at DESC');
    res.json({ posts });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/posts', async (req, res) => {
  const { title, content, author } = req.body;
  try {
    const [result] = await pool.query(
      'INSERT INTO posts (title, content, author, created_at) VALUES (?, ?, ?, NOW())',
      [title, content, author]
    );
    res.json({ success: true, id: result.insertId });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Initialize database
async function initDatabase() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        author VARCHAR(100) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
      )
    `);
    console.log('✅ Database initialized');
  } catch (error) {
    console.error('❌ Database initialization failed:', error);
  }
}

// Start server
initDatabase().then(() => {
  app.listen(PORT, () => {
    console.log(`🚀 Blog server running on port ${PORT}`);
  });
});
'''
            
            result = await session.call_tool(
                "write_file",
                arguments={
                    "path": "/var/www/myblog/server.js",
                    "content": server_code
                }
            )
            print(result.content[0].text)
            print()
            
            # 6. Write .env file
            print("🔐 Step 6: Writing environment variables...")
            env_content = """PORT=3001
DB_HOST=localhost
DB_USER=blog_user
DB_PASSWORD=secure_password_123
DB_NAME=myblog_db
"""
            result = await session.call_tool(
                "write_file",
                arguments={
                    "path": "/var/www/myblog/.env",
                    "content": env_content
                }
            )
            print(result.content[0].text)
            print()
            
            # 7. Create views directory and index.ejs
            print("🎨 Step 7: Creating views...")
            result = await session.call_tool(
                "create_directory",
                arguments={"path": "/var/www/myblog/views"}
            )
            print(result.content[0].text)
            
            index_ejs = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Blog</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        .post { border: 1px solid #ddd; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .post h2 { margin-top: 0; }
        .meta { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>📝 My Blog</h1>
    <% if (posts.length === 0) { %>
        <p>No posts yet. Create your first post!</p>
    <% } else { %>
        <% posts.forEach(post => { %>
            <div class="post">
                <h2><%= post.title %></h2>
                <p><%= post.content %></p>
                <div class="meta">
                    By <%= post.author %> on <%= post.created_at %>
                </div>
            </div>
        <% }) %>
    <% } %>
</body>
</html>
'''
            result = await session.call_tool(
                "write_file",
                arguments={
                    "path": "/var/www/myblog/views/index.ejs",
                    "content": index_ejs
                }
            )
            print(result.content[0].text)
            print()
            
            # 8. Install npm packages
            print("📦 Step 8: Installing npm packages (this may take a while)...")
            result = await session.call_tool(
                "npm_install",
                arguments={"project": "/var/www/myblog"}
            )
            print(result.content[0].text)
            print()
            
            # 9. Configure Nginx
            print("🌐 Step 9: Configuring Nginx...")
            result = await session.call_tool(
                "nginx_create_site",
                arguments={
                    "domain": "blog.example.com",
                    "port": 3001,
                    "type": "proxy"
                }
            )
            print(result.content[0].text)
            print()
            
            # 10. Start application with PM2
            print("🚀 Step 10: Starting application...")
            result = await session.call_tool(
                "start_application",
                arguments={
                    "name": "myblog",
                    "script": "server.js",
                    "cwd": "/var/www/myblog"
                }
            )
            print(result.content[0].text)
            print()
            
            # 11. Check process status
            print("✅ Step 11: Checking application status...")
            result = await session.call_tool(
                "list_processes",
                arguments={"filter": "myblog"}
            )
            print(result.content[0].text)
            print()
            
            print("="*70)
            print("🎉 BLOG WEBSITE CREATED SUCCESSFULLY!")
            print("="*70)
            print("\n📋 Summary:")
            print("   ✅ Project created: /var/www/myblog")
            print("   ✅ Database created: myblog_db")
            print("   ✅ User created: blog_user")
            print("   ✅ Code written: server.js, views, etc.")
            print("   ✅ Dependencies installed")
            print("   ✅ Nginx configured")
            print("   ✅ Application started with PM2")
            print("\n🔗 Access your blog:")
            print("   Local: http://localhost:3001")
            print("   Domain: http://blog.example.com (after DNS setup)")
            print("\n💡 Next steps:")
            print("   1. Point blog.example.com to your server IP")
            print("   2. Enable SSL: enable_ssl(domain='blog.example.com', email='you@email.com')")
            print("   3. Create your first post via API:")
            print("      curl -X POST http://localhost:3001/api/posts \\")
            print("        -H 'Content-Type: application/json' \\")
            print("        -d '{\"title\":\"Hello World\",\"content\":\"My first post!\",\"author\":\"Admin\"}'")
            print("="*70)


async def main():
    """
    Main demo function
    """
    print("="*70)
    print("🌐 Ultimate Ubuntu MCP Client - Complete Website Demo")
    print("="*70)
    print()
    
    try:
        await create_blog_website()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
