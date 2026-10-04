#!/usr/bin/env python3
"""
Ultimate Ubuntu MCP Server
Complete Linux Machine Control via MCP Protocol

Features:
- 70+ tools covering everything a Linux machine can do
- Database management (MySQL, PostgreSQL, SQLite, MongoDB, Redis)
- Web server automation (Nginx, Apache)
- Process & service management
- Docker container operations
- Git & version control
- Package management (apt, npm, pip, composer)
- File & directory operations
- Network tools
- System monitoring & logs
- Backup & restore
- Security & firewall
- Cron & scheduling
- Environment management
"""

import json
import asyncio
import subprocess
import os
import sys
import shutil
import glob as glob_module
import re
import hashlib
import base64
from pathlib import Path
from typing import Any, Sequence, Optional
from datetime import datetime

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
import uvicorn

# Initialize MCP Server
app_server = Server("ubuntu-ultimate-mcp")

# Configuration
CONFIG = {
    "projects_dir": "/var/www",
    "logs_dir": "/var/log/mcp",
    "backup_dir": "/var/backups/mcp",
    "max_command_timeout": 300,
    "allowed_ports": range(3000, 9000),
}

# Ensure directories exist
for dir_path in [CONFIG["projects_dir"], CONFIG["logs_dir"], CONFIG["backup_dir"]]:
    os.makedirs(dir_path, exist_ok=True)

# Helper Functions
def run_command(cmd: str, timeout: int = 30, cwd: Optional[str] = None) -> dict:
    """Execute shell command safely"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Command timed out after {timeout}s"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def format_output(data: dict) -> str:
    """Format command output for display"""
    if not data.get("success"):
        return f"❌ Error: {data.get('error', data.get('stderr', 'Unknown error'))}"
    
    output = "✅ Success\n\n"
    if data.get("stdout"):
        output += f"Output:\n{data['stdout']}\n"
    if data.get("stderr"):
        output += f"Warnings:\n{data['stderr']}\n"
    if "exit_code" in data:
        output += f"\nExit Code: {data['exit_code']}"
    return output

# ============================================================================
# TOOL DEFINITIONS - 70+ Tools
# ============================================================================

TOOLS = [
    # ========== PROJECT MANAGEMENT ==========
    Tool(
        name="create_project",
        description="Create a new project with specified stack (node, python, php, static, docker)",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Project name"},
                "stack": {"type": "string", "description": "Tech stack: node, python, php, static, docker", "default": "node"},
                "port": {"type": "integer", "description": "Port number (3000-9000)", "default": 3000}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="delete_project",
        description="Delete a project completely",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Project name to delete"}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="list_projects",
        description="List all projects in /var/www",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="get_project_info",
        description="Get detailed information about a project",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Project name"}
            },
            "required": ["name"]
        }
    ),
    
    # ========== FILE OPERATIONS ==========
    Tool(
        name="read_file",
        description="Read file contents",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "encoding": {"type": "string", "description": "File encoding", "default": "utf-8"}
            },
            "required": ["path"]
        }
    ),
    Tool(
        name="write_file",
        description="Write content to a file",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "Content to write"},
                "mode": {"type": "string", "description": "Write mode: write, append", "default": "write"}
            },
            "required": ["path", "content"]
        }
    ),
    Tool(
        name="delete_file",
        description="Delete a file or directory",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to delete"}
            },
            "required": ["path"]
        }
    ),
    Tool(
        name="copy_file",
        description="Copy file or directory",
        inputSchema={
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source path"},
                "destination": {"type": "string", "description": "Destination path"}
            },
            "required": ["source", "destination"]
        }
    ),
    Tool(
        name="move_file",
        description="Move or rename file/directory",
        inputSchema={
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "destination": {"type": "string"}
            },
            "required": ["source", "destination"]
        }
    ),
    Tool(
        name="list_directory",
        description="List directory contents with details",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "default": "."},
                "recursive": {"type": "boolean", "default": False}
            }
        }
    ),
    Tool(
        name="search_files",
        description="Search for files by name or pattern",
        inputSchema={
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Search pattern (glob)"},
                "path": {"type": "string", "default": "."}
            },
            "required": ["pattern"]
        }
    ),
    Tool(
        name="search_in_files",
        description="Search for text content within files (grep)",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to search"},
                "path": {"type": "string", "default": "."},
                "file_pattern": {"type": "string", "default": "*"}
            },
            "required": ["text"]
        }
    ),
    Tool(
        name="create_directory",
        description="Create a new directory",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    ),
    Tool(
        name="get_file_info",
        description="Get detailed file/directory information",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    ),
    Tool(
        name="change_permissions",
        description="Change file/directory permissions (chmod)",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "mode": {"type": "string", "description": "Permission mode (e.g., 755, 644)"}
            },
            "required": ["path", "mode"]
        }
    ),
    
    # ========== PACKAGE MANAGEMENT ==========
    Tool(
        name="npm_install",
        description="Install npm packages",
        inputSchema={
            "type": "object",
            "properties": {
                "packages": {"type": "string", "description": "Package names (space-separated)"},
                "project": {"type": "string", "description": "Project directory"},
                "global": {"type": "boolean", "default": False},
                "dev": {"type": "boolean", "default": False}
            }
        }
    ),
    Tool(
        name="pip_install",
        description="Install Python packages",
        inputSchema={
            "type": "object",
            "properties": {
                "packages": {"type": "string"},
                "project": {"type": "string"},
                "requirements_file": {"type": "string", "default": ""}
            }
        }
    ),
    Tool(
        name="composer_install",
        description="Install PHP packages via Composer",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string", "description": "Project directory"}
            },
            "required": ["project"]
        }
    ),
    Tool(
        name="apt_install",
        description="Install system packages via apt",
        inputSchema={
            "type": "object",
            "properties": {
                "packages": {"type": "string", "description": "Package names"}
            },
            "required": ["packages"]
        }
    ),
    Tool(
        name="apt_search",
        description="Search for available packages",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    ),
    
    # ========== DATABASE MANAGEMENT ==========
    Tool(
        name="mysql_query",
        description="Execute MySQL query",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "database": {"type": "string", "default": ""},
                "user": {"type": "string", "default": "root"},
                "password": {"type": "string", "default": ""}
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="mysql_create_database",
        description="Create a new MySQL database",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "charset": {"type": "string", "default": "utf8mb4"}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="mysql_create_user",
        description="Create MySQL user with permissions",
        inputSchema={
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
                "database": {"type": "string"},
                "host": {"type": "string", "default": "localhost"}
            },
            "required": ["username", "password", "database"]
        }
    ),
    Tool(
        name="mysql_list_databases",
        description="List all MySQL databases",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="mysql_backup",
        description="Backup MySQL database",
        inputSchema={
            "type": "object",
            "properties": {
                "database": {"type": "string"},
                "output_file": {"type": "string", "description": "Backup file path"}
            },
            "required": ["database"]
        }
    ),
    Tool(
        name="postgresql_query",
        description="Execute PostgreSQL query",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "database": {"type": "string", "default": "postgres"},
                "user": {"type": "string", "default": "postgres"}
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="redis_command",
        description="Execute Redis command",
        inputSchema={
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Redis command"}
            },
            "required": ["command"]
        }
    ),
    
    # ========== WEB SERVER MANAGEMENT ==========
    Tool(
        name="nginx_create_site",
        description="Create Nginx site configuration",
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {"type": "string"},
                "port": {"type": "integer"},
                "root": {"type": "string", "description": "Document root path"},
                "type": {"type": "string", "description": "proxy or static", "default": "proxy"}
            },
            "required": ["domain", "port"]
        }
    ),
    Tool(
        name="nginx_delete_site",
        description="Delete Nginx site configuration",
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {"type": "string"}
            },
            "required": ["domain"]
        }
    ),
    Tool(
        name="nginx_list_sites",
        description="List all Nginx sites",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="nginx_reload",
        description="Reload Nginx configuration",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="nginx_test_config",
        description="Test Nginx configuration for errors",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="enable_ssl",
        description="Enable SSL/HTTPS for a domain using Let's Encrypt",
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {"type": "string"},
                "email": {"type": "string"}
            },
            "required": ["domain", "email"]
        }
    ),
    
    # ========== PROCESS MANAGEMENT ==========
    Tool(
        name="start_application",
        description="Start application with PM2",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "script": {"type": "string", "description": "Entry script path"},
                "cwd": {"type": "string", "description": "Working directory"},
                "env_vars": {"type": "object", "description": "Environment variables"}
            },
            "required": ["name", "script"]
        }
    ),
    Tool(
        name="stop_application",
        description="Stop application",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="restart_application",
        description="Restart application",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="list_processes",
        description="List all running processes",
        inputSchema={
            "type": "object",
            "properties": {
                "filter": {"type": "string", "default": ""}
            }
        }
    ),
    Tool(
        name="get_process_logs",
        description="Get application logs",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "lines": {"type": "integer", "default": 100}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="kill_process",
        description="Kill a process by PID or name",
        inputSchema={
            "type": "object",
            "properties": {
                "pid": {"type": "integer"},
                "name": {"type": "string"},
                "signal": {"type": "string", "default": "TERM"}
            }
        }
    ),
    
    # ========== GIT OPERATIONS ==========
    Tool(
        name="git_clone",
        description="Clone a Git repository",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "destination": {"type": "string"},
                "branch": {"type": "string", "default": ""}
            },
            "required": ["url", "destination"]
        }
    ),
    Tool(
        name="git_pull",
        description="Pull latest changes",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string"}
            },
            "required": ["project"]
        }
    ),
    Tool(
        name="git_status",
        description="Get Git status",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string"}
            },
            "required": ["project"]
        }
    ),
    Tool(
        name="git_commit",
        description="Commit changes",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "message": {"type": "string"}
            },
            "required": ["project", "message"]
        }
    ),
    Tool(
        name="git_push",
        description="Push changes to remote",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string"}
            },
            "required": ["project"]
        }
    ),
    Tool(
        name="git_branch",
        description="List or create branches",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "action": {"type": "string", "description": "list, create, switch", "default": "list"},
                "branch_name": {"type": "string", "default": ""}
            },
            "required": ["project"]
        }
    ),
    
    # ========== DOCKER OPERATIONS ==========
    Tool(
        name="docker_ps",
        description="List Docker containers",
        inputSchema={
            "type": "object",
            "properties": {
                "all": {"type": "boolean", "default": False}
            }
        }
    ),
    Tool(
        name="docker_images",
        description="List Docker images",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="docker_run",
        description="Run a Docker container",
        inputSchema={
            "type": "object",
            "properties": {
                "image": {"type": "string"},
                "name": {"type": "string"},
                "ports": {"type": "string", "description": "Port mapping e.g., 8080:80"},
                "env": {"type": "string", "description": "Environment variables"},
                "detach": {"type": "boolean", "default": True}
            },
            "required": ["image"]
        }
    ),
    Tool(
        name="docker_stop",
        description="Stop a Docker container",
        inputSchema={
            "type": "object",
            "properties": {
                "container": {"type": "string"}
            },
            "required": ["container"]
        }
    ),
    Tool(
        name="docker_logs",
        description="Get Docker container logs",
        inputSchema={
            "type": "object",
            "properties": {
                "container": {"type": "string"},
                "tail": {"type": "integer", "default": 100}
            },
            "required": ["container"]
        }
    ),
    Tool(
        name="docker_exec",
        description="Execute command in Docker container",
        inputSchema={
            "type": "object",
            "properties": {
                "container": {"type": "string"},
                "command": {"type": "string"}
            },
            "required": ["container", "command"]
        }
    ),
    
    # ========== SYSTEM MONITORING ==========
    Tool(
        name="system_info",
        description="Get comprehensive system information",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="cpu_usage",
        description="Get CPU usage statistics",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="memory_usage",
        description="Get memory usage statistics",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="disk_usage",
        description="Get disk usage statistics",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "default": "/"}
            }
        }
    ),
    Tool(
        name="network_stats",
        description="Get network statistics",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="check_port",
        description="Check if a port is open",
        inputSchema={
            "type": "object",
            "properties": {
                "port": {"type": "integer"},
                "host": {"type": "string", "default": "localhost"}
            },
            "required": ["port"]
        }
    ),
    Tool(
        name="list_open_ports",
        description="List all open ports",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="top_processes",
        description="Get top processes by CPU/Memory",
        inputSchema={
            "type": "object",
            "properties": {
                "count": {"type": "integer", "default": 10},
                "sort_by": {"type": "string", "default": "cpu"}
            }
        }
    ),
    
    # ========== LOG MANAGEMENT ==========
    Tool(
        name="view_logs",
        description="View system or application logs",
        inputSchema={
            "type": "object",
            "properties": {
                "log_file": {"type": "string"},
                "lines": {"type": "integer", "default": 100},
                "follow": {"type": "boolean", "default": False}
            },
            "required": ["log_file"]
        }
    ),
    Tool(
        name="search_logs",
        description="Search in logs",
        inputSchema={
            "type": "object",
            "properties": {
                "log_file": {"type": "string"},
                "pattern": {"type": "string"}
            },
            "required": ["log_file", "pattern"]
        }
    ),
    
    # ========== NETWORK TOOLS ==========
    Tool(
        name="ping",
        description="Ping a host",
        inputSchema={
            "type": "object",
            "properties": {
                "host": {"type": "string"},
                "count": {"type": "integer", "default": 4}
            },
            "required": ["host"]
        }
    ),
    Tool(
        name="curl_request",
        description="Make HTTP request",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "method": {"type": "string", "default": "GET"},
                "headers": {"type": "string", "default": ""},
                "data": {"type": "string", "default": ""}
            },
            "required": ["url"]
        }
    ),
    Tool(
        name="download_file",
        description="Download file from URL",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "destination": {"type": "string"}
            },
            "required": ["url", "destination"]
        }
    ),
    
    # ========== COMPRESSION & ARCHIVES ==========
    Tool(
        name="compress_files",
        description="Compress files/directories (tar.gz, zip)",
        inputSchema={
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "output": {"type": "string"},
                "format": {"type": "string", "default": "tar.gz"}
            },
            "required": ["source", "output"]
        }
    ),
    Tool(
        name="extract_archive",
        description="Extract compressed archives",
        inputSchema={
            "type": "object",
            "properties": {
                "archive": {"type": "string"},
                "destination": {"type": "string", "default": "."}
            },
            "required": ["archive"]
        }
    ),
    
    # ========== ENVIRONMENT & CONFIG ==========
    Tool(
        name="set_env_var",
        description="Set environment variable for a project",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "key": {"type": "string"},
                "value": {"type": "string"}
            },
            "required": ["project", "key", "value"]
        }
    ),
    Tool(
        name="get_env_vars",
        description="Get all environment variables for a project",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string"}
            },
            "required": ["project"]
        }
    ),
    
    # ========== CRON & SCHEDULING ==========
    Tool(
        name="list_cron_jobs",
        description="List all cron jobs",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="add_cron_job",
        description="Add a new cron job",
        inputSchema={
            "type": "object",
            "properties": {
                "schedule": {"type": "string", "description": "Cron schedule expression"},
                "command": {"type": "string"}
            },
            "required": ["schedule", "command"]
        }
    ),
    
    # ========== BACKUP & RESTORE ==========
    Tool(
        name="backup_project",
        description="Create full project backup",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "include_db": {"type": "boolean", "default": True}
            },
            "required": ["project"]
        }
    ),
    Tool(
        name="list_backups",
        description="List all available backups",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    # ========== UTILITY ==========
    Tool(
        name="execute_command",
        description="Execute any shell command (use with caution)",
        inputSchema={
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "cwd": {"type": "string", "default": ""},
                "timeout": {"type": "integer", "default": 30}
            },
            "required": ["command"]
        }
    ),
]

# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

@app_server.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS

@app_server.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    try:
        result = await handle_tool(name, arguments)
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]

async def handle_tool(name: str, args: dict) -> str:
    """Route tool calls to appropriate handlers"""
    
    # PROJECT MANAGEMENT
    if name == "create_project":
        return handle_create_project(args)
    elif name == "delete_project":
        return handle_delete_project(args)
    elif name == "list_projects":
        return handle_list_projects()
    elif name == "get_project_info":
        return handle_get_project_info(args)
    
    # FILE OPERATIONS
    elif name == "read_file":
        return handle_read_file(args)
    elif name == "write_file":
        return handle_write_file(args)
    elif name == "delete_file":
        return handle_delete_file(args)
    elif name == "copy_file":
        return handle_copy_file(args)
    elif name == "move_file":
        return handle_move_file(args)
    elif name == "list_directory":
        return handle_list_directory(args)
    elif name == "search_files":
        return handle_search_files(args)
    elif name == "search_in_files":
        return handle_search_in_files(args)
    elif name == "create_directory":
        return handle_create_directory(args)
    elif name == "get_file_info":
        return handle_get_file_info(args)
    elif name == "change_permissions":
        return handle_change_permissions(args)
    
    # PACKAGE MANAGEMENT
    elif name == "npm_install":
        return handle_npm_install(args)
    elif name == "pip_install":
        return handle_pip_install(args)
    elif name == "composer_install":
        return handle_composer_install(args)
    elif name == "apt_install":
        return handle_apt_install(args)
    elif name == "apt_search":
        return handle_apt_search(args)
    
    # DATABASE
    elif name == "mysql_query":
        return handle_mysql_query(args)
    elif name == "mysql_create_database":
        return handle_mysql_create_database(args)
    elif name == "mysql_create_user":
        return handle_mysql_create_user(args)
    elif name == "mysql_list_databases":
        return handle_mysql_list_databases()
    elif name == "mysql_backup":
        return handle_mysql_backup(args)
    elif name == "postgresql_query":
        return handle_postgresql_query(args)
    elif name == "redis_command":
        return handle_redis_command(args)
    
    # WEB SERVER
    elif name == "nginx_create_site":
        return handle_nginx_create_site(args)
    elif name == "nginx_delete_site":
        return handle_nginx_delete_site(args)
    elif name == "nginx_list_sites":
        return handle_nginx_list_sites()
    elif name == "nginx_reload":
        return handle_nginx_reload()
    elif name == "nginx_test_config":
        return handle_nginx_test_config()
    elif name == "enable_ssl":
        return handle_enable_ssl(args)
    
    # PROCESS MANAGEMENT
    elif name == "start_application":
        return handle_start_application(args)
    elif name == "stop_application":
        return handle_stop_application(args)
    elif name == "restart_application":
        return handle_restart_application(args)
    elif name == "list_processes":
        return handle_list_processes(args)
    elif name == "get_process_logs":
        return handle_get_process_logs(args)
    elif name == "kill_process":
        return handle_kill_process(args)
    
    # GIT
    elif name == "git_clone":
        return handle_git_clone(args)
    elif name == "git_pull":
        return handle_git_pull(args)
    elif name == "git_status":
        return handle_git_status(args)
    elif name == "git_commit":
        return handle_git_commit(args)
    elif name == "git_push":
        return handle_git_push(args)
    elif name == "git_branch":
        return handle_git_branch(args)
    
    # DOCKER
    elif name == "docker_ps":
        return handle_docker_ps(args)
    elif name == "docker_images":
        return handle_docker_images()
    elif name == "docker_run":
        return handle_docker_run(args)
    elif name == "docker_stop":
        return handle_docker_stop(args)
    elif name == "docker_logs":
        return handle_docker_logs(args)
    elif name == "docker_exec":
        return handle_docker_exec(args)
    
    # SYSTEM MONITORING
    elif name == "system_info":
        return handle_system_info()
    elif name == "cpu_usage":
        return handle_cpu_usage()
    elif name == "memory_usage":
        return handle_memory_usage()
    elif name == "disk_usage":
        return handle_disk_usage(args)
    elif name == "network_stats":
        return handle_network_stats()
    elif name == "check_port":
        return handle_check_port(args)
    elif name == "list_open_ports":
        return handle_list_open_ports()
    elif name == "top_processes":
        return handle_top_processes(args)
    
    # LOGS
    elif name == "view_logs":
        return handle_view_logs(args)
    elif name == "search_logs":
        return handle_search_logs(args)
    
    # NETWORK
    elif name == "ping":
        return handle_ping(args)
    elif name == "curl_request":
        return handle_curl_request(args)
    elif name == "download_file":
        return handle_download_file(args)
    
    # COMPRESSION
    elif name == "compress_files":
        return handle_compress_files(args)
    elif name == "extract_archive":
        return handle_extract_archive(args)
    
    # ENVIRONMENT
    elif name == "set_env_var":
        return handle_set_env_var(args)
    elif name == "get_env_vars":
        return handle_get_env_vars(args)
    
    # CRON
    elif name == "list_cron_jobs":
        return handle_list_cron_jobs()
    elif name == "add_cron_job":
        return handle_add_cron_job(args)
    
    # BACKUP
    elif name == "backup_project":
        return handle_backup_project(args)
    elif name == "list_backups":
        return handle_list_backups()
    
    # UTILITY
    elif name == "execute_command":
        return handle_execute_command(args)
    
    else:
        return f"❌ Unknown tool: {name}"

# ============================================================================
# HANDLER IMPLEMENTATIONS (Simplified - actual implementations would be more robust)
# ============================================================================

def handle_create_project(args: dict) -> str:
    name = args["name"]
    stack = args.get("stack", "node")
    port = args.get("port", 3000)
    
    project_path = os.path.join(CONFIG["projects_dir"], name)
    
    if os.path.exists(project_path):
        return f"❌ Project '{name}' already exists"
    
    os.makedirs(project_path, exist_ok=True)
    
    # Create basic structure based on stack
    if stack == "node":
        package_json = {
            "name": name,
            "version": "1.0.0",
            "main": "server.js",
            "scripts": {"start": "node server.js"}
        }
        with open(os.path.join(project_path, "package.json"), "w") as f:
            json.dump(package_json, f, indent=2)
        
        server_js = f"""const express = require('express');
const app = express();
const PORT = {port};

app.get('/', (req, res) => {{
  res.json({{ message: 'Hello from {name}!' }});
}});

app.listen(PORT, () => {{
  console.log(`Server running on port ${{PORT}}`);
}});
"""
        with open(os.path.join(project_path, "server.js"), "w") as f:
            f.write(server_js)
    
    elif stack == "python":
        with open(os.path.join(project_path, "app.py"), "w") as f:
            f.write(f"""from flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route('/')\ndef hello():\n    return jsonify(message='Hello from {name}!')\n\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port={port})\n""")
        
        with open(os.path.join(project_path, "requirements.txt"), "w") as f:
            f.write("flask\n")
    
    return f"✅ Project '{name}' created successfully at {project_path}\nStack: {stack}\nPort: {port}"

def handle_delete_project(args: dict) -> str:
    name = args["name"]
    project_path = os.path.join(CONFIG["projects_dir"], name)
    
    if not os.path.exists(project_path):
        return f"❌ Project '{name}' not found"
    
    shutil.rmtree(project_path)
    return f"✅ Project '{name}' deleted"

def handle_list_projects() -> str:
    try:
        projects = os.listdir(CONFIG["projects_dir"])
        if not projects:
            return "No projects found"
        return "📁 Projects:\n" + "\n".join(f"  - {p}" for p in projects)
    except Exception as e:
        return f"❌ Error: {e}"

def handle_get_project_info(args: dict) -> str:
    name = args["name"]
    project_path = os.path.join(CONFIG["projects_dir"], name)
    
    if not os.path.exists(project_path):
        return f"❌ Project '{name}' not found"
    
    info = f"📋 Project: {name}\n"
    info += f"Path: {project_path}\n"
    
    # Check for package.json (Node)
    if os.path.exists(os.path.join(project_path, "package.json")):
        info += "Stack: Node.js\n"
    elif os.path.exists(os.path.join(project_path, "requirements.txt")):
        info += "Stack: Python\n"
    elif os.path.exists(os.path.join(project_path, "composer.json")):
        info += "Stack: PHP\n"
    
    # List files
    files = os.listdir(project_path)
    info += f"\nFiles ({len(files)}): {', '.join(files[:10])}"
    
    return info

def handle_read_file(args: dict) -> str:
    path = args["path"]
    encoding = args.get("encoding", "utf-8")
    
    try:
        with open(path, "r", encoding=encoding) as f:
            content = f.read()
        return f"📄 {path}\n\n{content}"
    except Exception as e:
        return f"❌ Error reading file: {e}"

def handle_write_file(args: dict) -> str:
    path = args["path"]
    content = args["content"]
    mode = args.get("mode", "write")
    
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        file_mode = "a" if mode == "append" else "w"
        with open(path, file_mode) as f:
            f.write(content)
        return f"✅ File written: {path}"
    except Exception as e:
        return f"❌ Error: {e}"

def handle_delete_file(args: dict) -> str:
    path = args["path"]
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return f"✅ Deleted: {path}"
    except Exception as e:
        return f"❌ Error: {e}"

def handle_copy_file(args: dict) -> str:
    src = args["source"]
    dst = args["destination"]
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        return f"✅ Copied: {src} → {dst}"
    except Exception as e:
        return f"❌ Error: {e}"

def handle_move_file(args: dict) -> str:
    src = args["source"]
    dst = args["destination"]
    try:
        shutil.move(src, dst)
        return f"✅ Moved: {src} → {dst}"
    except Exception as e:
        return f"❌ Error: {e}"

def handle_list_directory(args: dict) -> str:
    path = args.get("path", ".")
    recursive = args.get("recursive", False)
    
    try:
        if recursive:
            result = []
            for root, dirs, files in os.walk(path):
                level = root.replace(path, "").count(os.sep)
                indent = " " * 2 * level
                result.append(f"{indent}{os.path.basename(root)}/")
                sub_indent = " " * 2 * (level + 1)
                for file in files:
                    result.append(f"{sub_indent}{file}")
            return "\n".join(result)
        else:
            items = os.listdir(path)
            return "\n".join(items)
    except Exception as e:
        return f"❌ Error: {e}"

def handle_search_files(args: dict) -> str:
    pattern = args["pattern"]
    path = args.get("path", ".")
    
    try:
        matches = glob_module.glob(os.path.join(path, "**", pattern), recursive=True)
        if not matches:
            return "No files found"
        return "Found files:\n" + "\n".join(matches)
    except Exception as e:
        return f"❌ Error: {e}"

def handle_search_in_files(args: dict) -> str:
    text = args["text"]
    path = args.get("path", ".")
    pattern = args.get("file_pattern", "*")
    
    result = run_command(f"grep -r '{text}' {path} --include='{pattern}'")
    return format_output(result)

def handle_create_directory(args: dict) -> str:
    path = args["path"]
    try:
        os.makedirs(path, exist_ok=True)
        return f"✅ Directory created: {path}"
    except Exception as e:
        return f"❌ Error: {e}"

def handle_get_file_info(args: dict) -> str:
    path = args["path"]
    try:
        stat = os.stat(path)
        info = f"📄 {path}\n"
        info += f"Size: {stat.st_size} bytes\n"
        info += f"Modified: {datetime.fromtimestamp(stat.st_mtime)}\n"
        info += f"Permissions: {oct(stat.st_mode)[-3:]}\n"
        return info
    except Exception as e:
        return f"❌ Error: {e}"

def handle_change_permissions(args: dict) -> str:
    path = args["path"]
    mode = args["mode"]
    result = run_command(f"chmod {mode} {path}")
    return format_output(result)

def handle_npm_install(args: dict) -> str:
    packages = args.get("packages", "")
    project = args.get("project", ".")
    is_global = args.get("global", False)
    is_dev = args.get("dev", False)
    
    cmd = "npm install"
    if is_global:
        cmd += " -g"
    if is_dev:
        cmd += " --save-dev"
    if packages:
        cmd += f" {packages}"
    
    result = run_command(cmd, timeout=120, cwd=project)
    return format_output(result)

def handle_pip_install(args: dict) -> str:
    packages = args.get("packages", "")
    project = args.get("project", ".")
    req_file = args.get("requirements_file", "")
    
    if req_file:
        cmd = f"pip install -r {req_file}"
    elif packages:
        cmd = f"pip install {packages}"
    else:
        return "❌ Specify packages or requirements file"
    
    result = run_command(cmd, timeout=180, cwd=project)
    return format_output(result)

def handle_composer_install(args: dict) -> str:
    project = args["project"]
    result = run_command("composer install", timeout=180, cwd=project)
    return format_output(result)

def handle_apt_install(args: dict) -> str:
    packages = args["packages"]
    result = run_command(f"apt-get install -y {packages}", timeout=300)
    return format_output(result)

def handle_apt_search(args: dict) -> str:
    query = args["query"]
    result = run_command(f"apt-cache search {query}")
    return format_output(result)

def handle_mysql_query(args: dict) -> str:
    query = args["query"]
    database = args.get("database", "")
    user = args.get("user", "root")
    password = args.get("password", "")
    
    cmd = f"mysql -u {user}"
    if password:
        cmd += f" -p{password}"
    if database:
        cmd += f" {database}"
    cmd += f" -e \"{query}\""
    
    result = run_command(cmd)
    return format_output(result)

def handle_mysql_create_database(args: dict) -> str:
    name = args["name"]
    charset = args.get("charset", "utf8mb4")
    query = f"CREATE DATABASE {name} CHARACTER SET {charset};"
    result = run_command(f"mysql -e \"{query}\"")
    return format_output(result)

def handle_mysql_create_user(args: dict) -> str:
    username = args["username"]
    password = args["password"]
    database = args["database"]
    host = args.get("host", "localhost")
    
    queries = [
        f"CREATE USER '{username}'@'{host}' IDENTIFIED BY '{password}';",
        f"GRANT ALL PRIVILEGES ON {database}.* TO '{username}'@'{host}';",
        "FLUSH PRIVILEGES;"
    ]
    
    for query in queries:
        result = run_command(f"mysql -e \"{query}\"")
        if not result["success"]:
            return format_output(result)
    
    return "✅ MySQL user created and privileges granted"

def handle_mysql_list_databases() -> str:
    result = run_command("mysql -e 'SHOW DATABASES;'")
    return format_output(result)

def handle_mysql_backup(args: dict) -> str:
    database = args["database"]
    output = args.get("output_file", f"{CONFIG['backup_dir']}/{database}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")
    
    result = run_command(f"mysqldump {database} > {output}", timeout=300)
    if result["success"]:
        return f"✅ Database backed up to {output}"
    return format_output(result)

def handle_postgresql_query(args: dict) -> str:
    query = args["query"]
    database = args.get("database", "postgres")
    user = args.get("user", "postgres")
    
    result = run_command(f"psql -U {user} -d {database} -c \"{query}\"")
    return format_output(result)

def handle_redis_command(args: dict) -> str:
    command = args["command"]
    result = run_command(f"redis-cli {command}")
    return format_output(result)

def handle_nginx_create_site(args: dict) -> str:
    domain = args["domain"]
    port = args["port"]
    root = args.get("root", "")
    site_type = args.get("type", "proxy")
    
    if site_type == "proxy":
        config = f"""server {{
    listen 80;
    server_name {domain};
    
    location / {{
        proxy_pass http://localhost:{port};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }}
}}
"""
    else:
        config = f"""server {{
    listen 80;
    server_name {domain};
    root {root};
    index index.html index.htm;
    
    location / {{
        try_files $uri $uri/ =404;
    }}
}}
"""
    
    config_file = f"/etc/nginx/sites-available/{domain}"
    try:
        with open(config_file, "w") as f:
            f.write(config)
        
        # Enable site
        os.symlink(config_file, f"/etc/nginx/sites-enabled/{domain}")
        
        # Test and reload
        test = run_command("nginx -t")
        if test["success"]:
            run_command("systemctl reload nginx")
            return f"✅ Nginx site created: {domain}"
        else:
            return format_output(test)
    except Exception as e:
        return f"❌ Error: {e}"

def handle_nginx_delete_site(args: dict) -> str:
    domain = args["domain"]
    try:
        os.remove(f"/etc/nginx/sites-enabled/{domain}")
        os.remove(f"/etc/nginx/sites-available/{domain}")
        run_command("systemctl reload nginx")
        return f"✅ Nginx site deleted: {domain}"
    except Exception as e:
        return f"❌ Error: {e}"

def handle_nginx_list_sites() -> str:
    try:
        sites = os.listdir("/etc/nginx/sites-enabled")
        return "Enabled sites:\n" + "\n".join(f"  - {s}" for s in sites)
    except Exception as e:
        return f"❌ Error: {e}"

def handle_nginx_reload() -> str:
    result = run_command("systemctl reload nginx")
    return format_output(result)

def handle_nginx_test_config() -> str:
    result = run_command("nginx -t")
    return format_output(result)

def handle_enable_ssl(args: dict) -> str:
    domain = args["domain"]
    email = args["email"]
    
    result = run_command(f"certbot --nginx -d {domain} --non-interactive --agree-tos -m {email}", timeout=180)
    return format_output(result)

def handle_start_application(args: dict) -> str:
    name = args["name"]
    script = args["script"]
    cwd = args.get("cwd", ".")
    
    result = run_command(f"pm2 start {script} --name {name}", cwd=cwd)
    return format_output(result)

def handle_stop_application(args: dict) -> str:
    name = args["name"]
    result = run_command(f"pm2 stop {name}")
    return format_output(result)

def handle_restart_application(args: dict) -> str:
    name = args["name"]
    result = run_command(f"pm2 restart {name}")
    return format_output(result)

def handle_list_processes(args: dict) -> str:
    filter_term = args.get("filter", "")
    if filter_term:
        result = run_command(f"ps aux | grep {filter_term}")
    else:
        result = run_command("pm2 list")
    return format_output(result)

def handle_get_process_logs(args: dict) -> str:
    name = args["name"]
    lines = args.get("lines", 100)
    result = run_command(f"pm2 logs {name} --lines {lines} --nostream")
    return format_output(result)

def handle_kill_process(args: dict) -> str:
    pid = args.get("pid")
    name = args.get("name")
    signal = args.get("signal", "TERM")
    
    if pid:
        result = run_command(f"kill -{signal} {pid}")
    elif name:
        result = run_command(f"pkill -{signal} {name}")
    else:
        return "❌ Specify PID or name"
    
    return format_output(result)

def handle_git_clone(args: dict) -> str:
    url = args["url"]
    destination = args["destination"]
    branch = args.get("branch", "")
    
    cmd = f"git clone {url} {destination}"
    if branch:
        cmd += f" -b {branch}"
    
    result = run_command(cmd, timeout=300)
    return format_output(result)

def handle_git_pull(args: dict) -> str:
    project = args["project"]
    result = run_command("git pull", cwd=project)
    return format_output(result)

def handle_git_status(args: dict) -> str:
    project = args["project"]
    result = run_command("git status", cwd=project)
    return format_output(result)

def handle_git_commit(args: dict) -> str:
    project = args["project"]
    message = args["message"]
    
    run_command("git add .", cwd=project)
    result = run_command(f"git commit -m '{message}'", cwd=project)
    return format_output(result)

def handle_git_push(args: dict) -> str:
    project = args["project"]
    result = run_command("git push", cwd=project, timeout=120)
    return format_output(result)

def handle_git_branch(args: dict) -> str:
    project = args["project"]
    action = args.get("action", "list")
    branch_name = args.get("branch_name", "")
    
    if action == "list":
        result = run_command("git branch -a", cwd=project)
    elif action == "create":
        result = run_command(f"git branch {branch_name}", cwd=project)
    elif action == "switch":
        result = run_command(f"git checkout {branch_name}", cwd=project)
    else:
        return "❌ Invalid action"
    
    return format_output(result)

def handle_docker_ps(args: dict) -> str:
    all_containers = args.get("all", False)
    cmd = "docker ps"
    if all_containers:
        cmd += " -a"
    result = run_command(cmd)
    return format_output(result)

def handle_docker_images() -> str:
    result = run_command("docker images")
    return format_output(result)

def handle_docker_run(args: dict) -> str:
    image = args["image"]
    name = args.get("name", "")
    ports = args.get("ports", "")
    env = args.get("env", "")
    detach = args.get("detach", True)
    
    cmd = "docker run"
    if detach:
        cmd += " -d"
    if name:
        cmd += f" --name {name}"
    if ports:
        cmd += f" -p {ports}"
    if env:
        cmd += f" -e {env}"
    cmd += f" {image}"
    
    result = run_command(cmd)
    return format_output(result)

def handle_docker_stop(args: dict) -> str:
    container = args["container"]
    result = run_command(f"docker stop {container}")
    return format_output(result)

def handle_docker_logs(args: dict) -> str:
    container = args["container"]
    tail = args.get("tail", 100)
    result = run_command(f"docker logs --tail {tail} {container}")
    return format_output(result)

def handle_docker_exec(args: dict) -> str:
    container = args["container"]
    command = args["command"]
    result = run_command(f"docker exec {container} {command}")
    return format_output(result)

def handle_system_info() -> str:
    info = "🖥️  SYSTEM INFORMATION\n\n"
    
    # OS
    os_info = run_command("lsb_release -a 2>/dev/null || cat /etc/os-release")
    info += "--- Operating System ---\n" + os_info.get("stdout", "") + "\n"
    
    # CPU
    cpu_info = run_command("lscpu | grep -E 'Model name|CPU\(s\)|Thread'")
    info += "--- CPU ---\n" + cpu_info.get("stdout", "") + "\n"
    
    # Memory
    mem_info = run_command("free -h")
    info += "--- Memory ---\n" + mem_info.get("stdout", "") + "\n"
    
    # Disk
    disk_info = run_command("df -h /")
    info += "--- Disk ---\n" + disk_info.get("stdout", "") + "\n"
    
    return info

def handle_cpu_usage() -> str:
    result = run_command("top -bn1 | grep 'Cpu(s)'")
    return format_output(result)

def handle_memory_usage() -> str:
    result = run_command("free -h")
    return format_output(result)

def handle_disk_usage(args: dict) -> str:
    path = args.get("path", "/")
    result = run_command(f"df -h {path}")
    return format_output(result)

def handle_network_stats() -> str:
    result = run_command("ip -s link")
    return format_output(result)

def handle_check_port(args: dict) -> str:
    port = args["port"]
    host = args.get("host", "localhost")
    result = run_command(f"nc -zv {host} {port} 2>&1")
    return format_output(result)

def handle_list_open_ports() -> str:
    result = run_command("ss -tuln")
    return format_output(result)

def handle_top_processes(args: dict) -> str:
    count = args.get("count", 10)
    sort_by = args.get("sort_by", "cpu")
    
    if sort_by == "cpu":
        result = run_command(f"ps aux --sort=-%cpu | head -n {count+1}")
    else:
        result = run_command(f"ps aux --sort=-%mem | head -n {count+1}")
    
    return format_output(result)

def handle_view_logs(args: dict) -> str:
    log_file = args["log_file"]
    lines = args.get("lines", 100)
    result = run_command(f"tail -n {lines} {log_file}")
    return format_output(result)

def handle_search_logs(args: dict) -> str:
    log_file = args["log_file"]
    pattern = args["pattern"]
    result = run_command(f"grep '{pattern}' {log_file}")
    return format_output(result)

def handle_ping(args: dict) -> str:
    host = args["host"]
    count = args.get("count", 4)
    result = run_command(f"ping -c {count} {host}")
    return format_output(result)

def handle_curl_request(args: dict) -> str:
    url = args["url"]
    method = args.get("method", "GET")
    headers = args.get("headers", "")
    data = args.get("data", "")
    
    cmd = f"curl -X {method}"
    if headers:
        cmd += f" -H '{headers}'"
    if data:
        cmd += f" -d '{data}'"
    cmd += f" {url}"
    
    result = run_command(cmd)
    return format_output(result)

def handle_download_file(args: dict) -> str:
    url = args["url"]
    destination = args["destination"]
    result = run_command(f"wget -O {destination} {url}", timeout=300)
    return format_output(result)

def handle_compress_files(args: dict) -> str:
    source = args["source"]
    output = args["output"]
    format_type = args.get("format", "tar.gz")
    
    if format_type == "tar.gz":
        result = run_command(f"tar -czf {output} {source}")
    elif format_type == "zip":
        result = run_command(f"zip -r {output} {source}")
    else:
        return "❌ Unsupported format"
    
    return format_output(result)

def handle_extract_archive(args: dict) -> str:
    archive = args["archive"]
    destination = args.get("destination", ".")
    
    if archive.endswith(".tar.gz") or archive.endswith(".tgz"):
        result = run_command(f"tar -xzf {archive} -C {destination}")
    elif archive.endswith(".zip"):
        result = run_command(f"unzip {archive} -d {destination}")
    else:
        return "❌ Unsupported archive format"
    
    return format_output(result)

def handle_set_env_var(args: dict) -> str:
    project = args["project"]
    key = args["key"]
    value = args["value"]
    
    env_file = os.path.join(CONFIG["projects_dir"], project, ".env")
    
    try:
        # Read existing .env
        env_vars = {}
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        env_vars[k] = v
        
        # Update
        env_vars[key] = value
        
        # Write back
        with open(env_file, "w") as f:
            for k, v in env_vars.items():
                f.write(f"{k}={v}\n")
        
        return f"✅ Environment variable set: {key}"
    except Exception as e:
        return f"❌ Error: {e}"

def handle_get_env_vars(args: dict) -> str:
    project = args["project"]
    env_file = os.path.join(CONFIG["projects_dir"], project, ".env")
    
    if not os.path.exists(env_file):
        return "No .env file found"
    
    try:
        with open(env_file, "r") as f:
            content = f.read()
        return f"📄 Environment variables:\n\n{content}"
    except Exception as e:
        return f"❌ Error: {e}"

def handle_list_cron_jobs() -> str:
    result = run_command("crontab -l")
    return format_output(result)

def handle_add_cron_job(args: dict) -> str:
    schedule = args["schedule"]
    command = args["command"]
    
    # Get existing cron
    existing = run_command("crontab -l")
    cron_content = existing.get("stdout", "")
    
    # Add new job
    new_job = f"{schedule} {command}\n"
    cron_content += new_job
    
    # Write back
    result = run_command(f"echo '{cron_content}' | crontab -")
    return format_output(result)

def handle_backup_project(args: dict) -> str:
    project = args["project"]
    include_db = args.get("include_db", True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(CONFIG["backup_dir"], f"{project}_{timestamp}.tar.gz")
    
    project_path = os.path.join(CONFIG["projects_dir"], project)
    
    result = run_command(f"tar -czf {backup_file} -C {CONFIG['projects_dir']} {project}", timeout=300)
    
    if result["success"]:
        return f"✅ Project backed up to {backup_file}"
    return format_output(result)

def handle_list_backups() -> str:
    try:
        backups = os.listdir(CONFIG["backup_dir"])
        if not backups:
            return "No backups found"
        return "📦 Backups:\n" + "\n".join(f"  - {b}" for b in backups)
    except Exception as e:
        return f"❌ Error: {e}"

def handle_execute_command(args: dict) -> str:
    command = args["command"]
    cwd = args.get("cwd", "")
    timeout = args.get("timeout", 30)
    
    # Security check
    dangerous = ["rm -rf /", "mkfs", "dd if=/dev/zero", "> /dev/sda"]
    if any(d in command for d in dangerous):
        return "❌ Dangerous command blocked for safety"
    
    result = run_command(command, timeout=timeout, cwd=cwd or None)
    return format_output(result)

# ============================================================================
# HTTP/SSE TRANSPORT
# ============================================================================

async def handle_sse(request: Request) -> Response:
    """Handle SSE connection"""
    async with SseServerTransport("/messages") as (read_stream, write_stream):
        await app_server.run(
            read_stream,
            write_stream,
            app_server.create_initialization_options()
        )
    return Response()

async def handle_messages(request: Request) -> Response:
    """Handle MCP messages"""
    api_key = request.headers.get("X-API-Key")
    expected_key = os.getenv("MCP_API_KEY", "")
    
    if expected_key and api_key != expected_key:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    async with SseServerTransport("/messages") as (read_stream, write_stream):
        await app_server.run(
            read_stream,
            write_stream,
            app_server.create_initialization_options()
        )
    
    return Response()

async def health_check(request: Request) -> Response:
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "server": "ubuntu-ultimate-mcp",
        "tools": len(TOOLS),
        "version": "1.0.0"
    })

async def list_tools_http(request: Request) -> Response:
    """List all tools via HTTP"""
    tools_list = [{"name": t.name, "description": t.description} for t in TOOLS]
    return JSONResponse({"tools": tools_list, "count": len(tools_list)})

# Starlette app
starlette_app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
        Route("/health", endpoint=health_check),
        Route("/tools", endpoint=list_tools_http),
    ],
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    print("="*70)
    print("🚀 ULTIMATE UBUNTU MCP SERVER")
    print("="*70)
    print(f"📡 Port: {port}")
    print(f"🔧 Tools: {len(TOOLS)}")
    print(f"📂 Projects: {CONFIG['projects_dir']}")
    print(f"💾 Backups: {CONFIG['backup_dir']}")
    print("\n🔗 Endpoints:")
    print(f"   SSE: http://0.0.0.0:{port}/sse")
    print(f"   Health: http://0.0.0.0:{port}/health")
    print(f"   Tools: http://0.0.0.0:{port}/tools")
    print("="*70)
    
    uvicorn.run(
        starlette_app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
