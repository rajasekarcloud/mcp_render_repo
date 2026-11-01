from typing import Any, Dict, List, Optional
from mcp.server.mcpserver import MCPServer as FastMCP
import sqlite3
from datetime import datetime, timezone
import json
mcp = FastMCP("Food Server")
