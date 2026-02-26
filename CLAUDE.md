# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

XulDebugTool is a PyQt5-based desktop application for debugging XUL (XML User Interface Language) applications on Android devices. It connects to devices via ADB and communicates with a debug server to inspect and modify UI elements, user objects, and data providers.

## Key Architecture

### Entry Point
- `XulDebugTool/App.py` - Application entry point that launches `ConnectWindow`

### Window Flow
1. **ConnectWindow** (`ui/ConnectWindow.py`) - Initial connection dialog
   - Connects to device via ADB (`adb connect`, `adb devices`)
   - Forwards XUL debug port (`adb forward tcp:55550 tcp:55550`)
   - Device format: `ip[:adb_port][:xul_port]` (defaults: adb=5555, xul=55550)
   - Launches `MainWindow` on successful connection

2. **MainWindow** (`ui/MainWindow.py`) - Main debug interface
   - Left: Tree view of pages, user objects, providers
   - Center: WebEngine view displaying XUL layout (XML rendered as HTML)
   - Right: Property editor and favorites/history
   - Bottom: Console log output

### Core Communication

**XulDebugServerHelper** (`utils/XulDebugServerHelper.py`)
- Static helper for HTTP API calls to XUL debug server
- Base URL format: `http://localhost:55550/api/`
- Key APIs:
  - `listPages()` - List all pages
  - `getLayout(pageId, skipProp, withBindingData, withPosition, withSelector)` - Get page layout
  - `listUserObject()` - List user objects (BitmapCache, DataService, PluginManager)
  - `getUserObject(objectId)` - Get user object details
  - `updateUrl(type, id, key, value)` - Update element attributes/styles
  - `clearAllCaches()` - Clear caches

**CmdExecutor** (`utils/CmdExecutor.py`)
- QThread-based ADB command executor
- Executes shell commands asynchronously
- 20-second timeout for commands

### Data Layer

**DBManager** (`ui/widget/model/database/DBManager.py`)
- SQLite database manager (`XulDebugTool.db`)
- Tables: `device`, `login`, `history_query`, `favorites`, `configuration`

**Data Models**
- `PropertyModel` - Tree model for element properties
- `Property` - Property data structure

### UI Components

**Widgets** (`ui/widget/`)
- `DataQueryDialog` - Dialog for querying provider data
- `FavoriteTreeView` - Tree view for favorites and history
- `UpdateProperty` - Property editor widget
- `ButtomConsoleWindow` - Bottom console log window

**Web Integration**
- `WebShareObject` (`webprocess/WebShareObject.py`) - Bridge between Python and JavaScript
- `WebDataHandler` (`webprocess/WebDataHandler.py`) - Handles web data
- JavaScript injection via QWebChannel for element interaction

### Logging

**STCLogger** (`logcatapi/Logcat.py`)
- Custom logger with file output
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Outputs to both file and console window

## Running the Application

```bash
# Activate virtual environment (if using venv)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run the application
python XulDebugTool/App.py
```

## Key Dependencies
- PyQt5 - UI framework
- urllib3 - HTTP requests
- pyperclip - Clipboard operations
- xmltodict - XML to JSON conversion (via Utils.xml2json)

## Important Constants

From `MainWindow.py`:
```python
SKIP_PROP = 'skip-prop'
WITH_CHILDREN = 'with-children'
WITH_BINDING_DATA = 'with-binding-data'
WITH_POSITION = 'with-position'
WITH_SELECTOR = 'with-selector'
```

## Tree Item Types
- `ITEM_TYPE_PAGE_ROOT` - Page root node
- `ITEM_TYPE_USER_OBJECT_ROOT` - User object root node
- `ITEM_TYPE_PROVIDER_REQUESTS_ROOT` - Provider requests root
- `ITEM_TYPE_PLUGIN_ROOT` - Plugin root
- `ITEM_TYPE_PAGE` - Individual page
- `ITEM_TYPE_USER_OBJECT` - Individual user object
- `ITEM_TYPE_PROVIDER` - Data provider

## Database Location
- Database file: `XulDebugTool.db` (created in working directory)
- Log path: Configurable via File -> LogPath menu
