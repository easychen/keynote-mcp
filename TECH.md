# Keynote-MCP Technical Documentation

## Architecture Design

### Core Components

```
keynote-mcp/
├── src/
│   ├── server.py              # MCP server main program
│   ├── tools/                 # MCP tool definitions
│   │   ├── __init__.py
│   │   ├── presentation.py    # Presentation management tools
│   │   ├── slide.py          # Slide operation tools
│   │   ├── content.py        # Content management tools
│   │   ├── export.py         # Export and screenshot tools
│   │   └── unsplash.py       # Unsplash image tools
│   ├── applescript/           # AppleScript script library
│   │   ├── keynote_base.scpt  # Basic Keynote operations
│   │   ├── presentation.scpt  # Presentation operations
│   │   ├── slide.scpt        # Slide operations
│   │   ├── content.scpt      # Content operations
│   │   └── export.scpt       # Export operations
│   └── utils/
│       ├── __init__.py
│       ├── applescript_runner.py  # AppleScript executor
│       └── error_handler.py       # Error handling
├── tests/                     # Test files
├── examples/                  # Usage examples
├── requirements.txt          # Python dependencies
└── package.json             # Node.js dependencies (if needed)
```

## Functional Modules

### 1. Presentation Management

#### Tool List
- `create_presentation` - Create new presentation
- `open_presentation` - Open existing presentation
- `save_presentation` - Save presentation
- `close_presentation` - Close presentation
- `list_presentations` - List all open presentations
- `set_presentation_theme` - Set presentation theme

#### Detailed Functions
```python
# Create presentation
{
    "name": "create_presentation",
    "description": "Create new Keynote presentation",
    "parameters": {
        "title": "Presentation title",
        "theme": "Theme name (optional)",
        "template": "Template path (optional)"
    }
}

# Open presentation
{
    "name": "open_presentation", 
    "description": "Open existing Keynote presentation",
    "parameters": {
        "file_path": "File path"
    }
}
```

### 2. Slide Operations

#### Tool List
- `add_slide` - Add new slide
- `delete_slide` - Delete slide
- `duplicate_slide` - Duplicate slide
- `move_slide` - Move slide position
- `get_slide_count` - Get slide count
- `select_slide` - Select specific slide
- `set_slide_layout` - Set slide layout

#### Detailed Functions
```python
# Add slide
{
    "name": "add_slide",
    "description": "Add new slide at specified position",
    "parameters": {
        "position": "Insert position (number, optional)",
        "layout": "Layout type (optional)",
        "master_slide": "Master slide (optional)"
    }
}

# Delete slide
{
    "name": "delete_slide",
    "description": "Delete specified slide",
    "parameters": {
        "slide_number": "Slide number"
    }
}
```

### 3. Content Management

#### Tool List
- `add_text_box` - Add text box
- `edit_text_box` - Edit text box content
- `add_image` - Add image
- `add_shape` - Add shape
- `add_table` - Add table
- `add_chart` - Add chart
- `set_text_style` - Set text style
- `position_object` - Set object position
- `resize_object` - Resize object

#### Detailed Functions
```python
# Add text box
{
    "name": "add_text_box",
    "description": "Add text box to current slide",
    "parameters": {
        "text": "Text content",
        "x": "X coordinate (optional)",
        "y": "Y coordinate (optional)",
        "width": "Width (optional)",
        "height": "Height (optional)",
        "slide_number": "Slide number (optional, default current)"
    }
}

# Add image
{
    "name": "add_image",
    "description": "Add image to slide",
    "parameters": {
        "image_path": "Image file path",
        "x": "X coordinate (optional)",
        "y": "Y coordinate (optional)",
        "width": "Width (optional)",
        "height": "Height (optional)",
        "slide_number": "Slide number (optional)"
    }
}
```

### 4. Export and Screenshot

#### Tool List
- `export_presentation` - Export presentation
- `screenshot_slide` - Screenshot single slide
- `screenshot_all_slides` - Screenshot all slides
- `export_pdf` - Export as PDF
- `export_images` - Export as image sequence

#### Detailed Functions
```python
# Screenshot slide
{
    "name": "screenshot_slide",
    "description": "Screenshot specified slide",
    "parameters": {
        "slide_number": "Slide number",
        "output_path": "Output file path",
        "format": "Image format (png/jpg, default png)",
        "quality": "Image quality (1-100, default 100)"
    }
}

# Export PDF
{
    "name": "export_pdf",
    "description": "Export presentation as PDF",
    "parameters": {
        "output_path": "Output file path",
        "slide_range": "Slide range (optional, e.g. '1-5')"
    }
}
```

### 5. Unsplash Integration

#### Tool List
- `search_unsplash_images` - Search Unsplash images
- `add_unsplash_image_to_slide` - Search and add Unsplash image to slide
- `get_random_unsplash_image` - Get random Unsplash image and add to slide

#### Detailed Functions
```python
# Search images
{
    "name": "search_unsplash_images",
    "description": "Search Unsplash images",
    "parameters": {
        "query": "Search keywords",
        "per_page": "Images per page (1-30, default 10)",
        "orientation": "Image orientation (landscape/portrait/squarish, optional)",
        "order_by": "Sort order (relevant/latest/popular, default relevant)"
    }
}

# Add image to slide
{
    "name": "add_unsplash_image_to_slide",
    "description": "Search Unsplash image and add to slide",
    "parameters": {
        "slide_number": "Slide number",
        "query": "Search keywords",
        "image_index": "Select which image (0-9, default 0)",
        "orientation": "Image orientation (optional)",
        "x": "X coordinate (optional)",
        "y": "Y coordinate (optional)",
        "width": "Image width (optional)",
        "height": "Image height (optional)"
    }
}
```

## AppleScript Core Scripts

### Basic Operation Script Example

```applescript
-- keynote_base.scpt
-- Check if Keynote is running
on checkKeynoteRunning()
    tell application "System Events"
        return (name of processes) contains "Keynote"
    end tell
end checkKeynoteRunning

-- Launch Keynote
on launchKeynote()
    tell application "Keynote"
        activate
    end tell
end launchKeynote

-- Create new presentation
on createNewPresentation(presentationName, themeName)
    tell application "Keynote"
        set newDoc to make new document with properties {name:presentationName}
        if themeName is not "" then
            set theme of newDoc to theme themeName
        end if
        return newDoc
    end tell
end createNewPresentation
```

### Slide Operation Script Example

```applescript
-- slide.scpt
-- Add new slide
on addSlide(slidePosition, layoutType)
    tell application "Keynote"
        tell front document
            if slidePosition is not 0 then
                set newSlide to make new slide at slide slidePosition
            else
                set newSlide to make new slide at end of slides
            end if
            
            if layoutType is not "" then
                set master slide of newSlide to master slide layoutType
            end if
            
            return index of newSlide
        end tell
    end tell
end addSlide

-- Delete slide
on deleteSlide(slideNumber)
    tell application "Keynote"
        tell front document
            delete slide slideNumber
        end tell
    end tell
end deleteSlide
```

## Error Handling Strategy

### Error Types
1. **Keynote Application Errors** - Keynote not running or crashed
2. **AppleScript Execution Errors** - Script syntax or permission issues
3. **File Operation Errors** - File not found or insufficient permissions
4. **Parameter Validation Errors** - Invalid input parameters

### Error Handling Mechanism
```python
class KeynoteError(Exception):
    """Keynote operation base exception"""
    pass

class AppleScriptError(KeynoteError):
    """AppleScript execution exception"""
    pass

class FileOperationError(KeynoteError):
    """File operation exception"""
    pass

def handle_applescript_error(error_output):
    """Handle AppleScript error output"""
    if "Keynote got an error" in error_output:
        raise AppleScriptError(f"Keynote error: {error_output}")
    elif "Can't get" in error_output:
        raise AppleScriptError(f"Object not found: {error_output}")
    else:
        raise AppleScriptError(f"Unknown AppleScript error: {error_output}")
```

## Advanced Usage Examples

### Batch Create Slides
```python
slides_data = [
    {"title": "Chapter 1", "content": "Introduction", "image_query": "introduction"},
    {"title": "Chapter 2", "content": "Details", "image_query": "analysis"},
    {"title": "Chapter 3", "content": "Summary", "image_query": "conclusion"}
]

for i, slide_data in enumerate(slides_data, 1):
    await mcp_client.call_tool("add_slide", {"layout": "Title & Content"})
    await mcp_client.call_tool("add_text_box", {
        "text": slide_data["title"],
        "slide_number": i + 1
    })
    await mcp_client.call_tool("add_text_box", {
        "text": slide_data["content"],
        "y": 300,
        "slide_number": i + 1
    })
    # Auto add related images
    await mcp_client.call_tool("add_unsplash_image_to_slide", {
        "slide_number": i + 1,
        "query": slide_data["image_query"],
        "orientation": "landscape"
    })
```

### Themed Presentation with Unsplash
```python
async def create_themed_presentation():
    # Create themed presentation
    await mcp_client.call_tool("create_presentation", {
        "title": "Nature Theme Presentation",
        "theme": "White"
    })
    
    themes = ["mountain", "ocean", "forest", "sunset"]
    
    for i, theme in enumerate(themes, 1):
        await mcp_client.call_tool("add_slide", {"layout": "Title & Content"})
        await mcp_client.call_tool("add_text_box", {
            "text": f"{theme.title()} Theme",
            "slide_number": i
        })
        # Add theme-related high-quality images
        await mcp_client.call_tool("add_unsplash_image_to_slide", {
            "slide_number": i,
            "query": theme,
            "orientation": "landscape",
            "image_index": 0  # Select most relevant image
        })
```

## Technical Requirements

### System Requirements
- macOS 10.14 or higher
- Keynote application
- Python 3.8+
- AppleScript permissions

### Dependencies
```txt
# requirements.txt
mcp>=1.0.0
asyncio-mqtt>=0.16.0
pathlib>=1.0.1
typing-extensions>=4.0.0
aiohttp>=3.8.0
aiofiles>=0.8.0
Pillow>=9.0.0
```

### Permission Configuration
The application requires the following macOS permissions:
- **Accessibility Permission** - Control Keynote application
- **File System Permission** - Read/write presentation files
- **AppleScript Permission** - Execute automation scripts

## Development Roadmap

### Phase 1 (Basic Features)
- [x] Project architecture design
- [ ] Basic MCP server framework
- [ ] Core AppleScript script library
- [ ] Presentation management tools
- [ ] Basic slide operations

### Phase 2 (Content Management)
- [ ] Text content operations
- [ ] Image and media management
- [ ] Shape and chart support
- [ ] Style and formatting

### Phase 3 (Advanced Features)
- [ ] Batch operation support
- [ ] Template system
- [ ] Animation and transition effects
- [ ] Collaboration and sharing features

### Phase 4 (Optimization and Extension)
- [ ] Performance optimization
- [ ] Error handling improvement
- [ ] Test coverage
- [ ] Documentation improvement 