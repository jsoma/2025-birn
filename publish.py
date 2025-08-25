#!/usr/bin/env python3
"""
Simple notebook publishing script for BIRN workshop.
Processes notebooks with metadata and solution-tagged cells.
"""

import json
from pathlib import Path
import zipfile
from glob import glob
import yaml
import re
try:
    import markdown
except ImportError:
    print("Warning: 'markdown' package not installed. Install with: pip install markdown")
    markdown = None

def get_notebook_metadata(notebook):
    """Extract workshop metadata from notebook."""
    return notebook.get('metadata', {}).get('workshop', {})

def extract_markdown_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        yaml_content = match.group(1)
        markdown_content = match.group(2)
        try:
            frontmatter = yaml.safe_load(yaml_content)
            return frontmatter, markdown_content
        except:
            print(f"Warning: Invalid YAML frontmatter")
            return {}, content
    return {}, content

def markdown_to_html(content, title=""):
    """Convert markdown to HTML with basic styling."""
    if markdown:
        html_content = markdown.markdown(content, extensions=['extra', 'codehilite'])
    else:
        # Fallback: just wrap in pre tags if markdown not available
        html_content = f"<pre>{content}</pre>"
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>
        body {{
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        h1, h2, h3, h4 {{ margin-top: 2em; }}
        h3 a {{
            text-decoration: none;
        }}
        h3 a:hover {{
            text-decoration: underline;
        }}
        p {{
            margin: 0.5em 0;
        }}
        code {{ 
            background: #f4f4f4; 
            padding: 2px 4px; 
            border-radius: 3px;
            font-family: Consolas, Monaco, monospace;
        }}
        pre {{ 
            background: #f4f4f4; 
            padding: 1em; 
            border-radius: 5px; 
            overflow-x: auto;
        }}
        pre code {{ background: none; padding: 0; }}
        a {{ color: #0066cc; }}
        .download-box {{
            background: #e8f4f8;
            padding: 1em;
            border-radius: 5px;
            margin: 1em 0;
        }}
        ul {{
            list-style-type: disc;
            padding-left: 2em;
            margin: 0.5em 0;
        }}
        li {{
            margin: 0.3em 0;
        }}
        .section-header {{
            margin-top: 2em;
            margin-bottom: 1em;
            padding-bottom: 0.5em;
            border-bottom: 2px solid #eee;
        }}
        .resource-buttons {{
            margin: 1em 0;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5em;
        }}
        .resource-button {{
            display: inline-block;
            padding: 0.4em 0.8em;
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 4px;
            text-decoration: none;
            color: #333;
            font-size: 0.9em;
            transition: all 0.2s;
        }}
        .resource-button:hover {{
            background: #e0e0e0;
            border-color: #ccc;
        }}
        .resource-button.primary {{
            background: #e3f2fd;
            color: #1565c0;
            border-color: #90caf9;
        }}
        .resource-button.primary:hover {{
            background: #bbdefb;
            border-color: #64b5f6;
        }}
        .resource-button.completed {{
            background: #e8f5e9;
            color: #2e7d32;
            border-color: #a5d6a7;
        }}
        .resource-button.completed:hover {{
            background: #c8e6c9;
            border-color: #81c784;
        }}
        .data-download {{
            margin: 0.5em 0;
            font-size: 0.9em;
        }}
        .download-links {{
            margin: 0.5em 0;
            line-height: 1.8;
        }}
        .download-links a {{
            color: #1976d2;
            text-decoration: none;
        }}
        .download-links a:hover {{
            text-decoration: underline;
        }}
        p:last {{
            margin-bottom: 0;
            margin-top: 5em;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

def load_config():
    """Load workshop configuration from YAML file."""
    config_path = Path('workshop-config.yaml')
    if not config_path.exists():
        print("Warning: workshop-config.yaml not found, using defaults")
        return {
            'github_repo': 'yourusername/birn-workshop',
            'github_branch': 'main',
            'title': 'Workshop',
            'description': '',
            'output_dir': 'docs'
        }
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_setup_cell(zip_name, github_repo, install_packages="pandas natural_pdf tqdm", links=None):
    """Create setup cell that works in Colab, Jupyter, etc."""
    source_lines = [
        "# Run this cell first to set up the environment\n",
        "import os\n",
        "import urllib.request\n",
        "import zipfile\n",
        "\n",
        "# Install required packages\n",
        f"!pip install -q {install_packages}\n",
        "\n",
        "# Download and extract data files\n",
        f"url = 'https://github.com/{github_repo}/releases/latest/download/{zip_name}'\n",
        "print(f'Downloading data from {{url}}...')\n",
        f"urllib.request.urlretrieve(url, '{zip_name}')\n",
        "\n",
        f"print('Extracting {zip_name}...')\n",
        f"with zipfile.ZipFile('{zip_name}', 'r') as zip_ref:\n",
        "    zip_ref.extractall('.')\n",
        "\n",
        f"os.remove('{zip_name}')\n",
        "print('✓ Data files extracted!')"
    ]
    
    # Add links section if provided
    if links:
        source_lines.extend([
            "\n",
            "# Useful links:\n"
        ])
        for link in links:
            name = link.get('name', 'Link')
            url = link.get('url', '#')
            desc = link.get('description', '')
            if desc:
                source_lines.append(f"# - {name}: {url} ({desc})\n")
            else:
                source_lines.append(f"# - {name}: {url}\n")
    
    return {
        "cell_type": "code",
        "metadata": {},
        "source": source_lines,
        "execution_count": None,
        "outputs": []
    }

def process_notebook(notebook_path, output_dir, config):
    """Process a single notebook and return info for index."""
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    metadata = get_notebook_metadata(notebook)
    if not metadata:
        print(f"Skipping {notebook_path} - no workshop metadata")
        return None
    
    base_name = notebook_path.stem
    notebook_dir = notebook_path.parent
    
    # Create complete version (ANSWERS)
    complete_nb = notebook.copy()
    
    # Create exercise version
    exercise_nb = json.loads(json.dumps(notebook))  # Deep copy
    
    # Process cells for exercise version - replace solution-tagged cells
    for i, cell in enumerate(exercise_nb['cells']):
        if cell.get('metadata', {}).get('tags') and 'solution' in cell['metadata']['tags']:
            # Replace with empty cell
            exercise_nb['cells'][i] = {
                "cell_type": "code",
                "metadata": {},
                "source": [],
                "execution_count": None,
                "outputs": []
            }
    
    # Add setup cell if data files are specified
    if metadata.get('data_files'):
        zip_name = f"{base_name}-data.zip"
        install_packages = metadata.get('install', 'pandas natural_pdf tqdm')
        links = metadata.get('links', None)
        setup_cell = create_setup_cell(zip_name, config['github_repo'], install_packages, links)
        
        # Find first non-metadata cell position
        insert_pos = 0
        for i, cell in enumerate(complete_nb['cells']):
            if cell['cell_type'] == 'markdown':
                insert_pos = i + 1
                break
        
        complete_nb['cells'].insert(insert_pos, setup_cell)
        exercise_nb['cells'].insert(insert_pos, setup_cell)
        
        # Create data zip with paths relative to notebook directory
        create_data_zip(metadata['data_files'], output_dir / zip_name, notebook_dir)
    
    # Write output files
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Exercise version keeps original name
    with open(output_dir / f"{base_name}.ipynb", 'w') as f:
        json.dump(exercise_nb, f, indent=1)
    print(f"✓ Created {output_dir / base_name}.ipynb")
    
    # Complete version gets -ANSWERS suffix
    with open(output_dir / f"{base_name}-ANSWERS.ipynb", 'w') as f:
        json.dump(complete_nb, f, indent=1)
    print(f"✓ Created {output_dir / base_name}-ANSWERS.ipynb")
    
    # Return info for index
    return {
        'name': base_name,
        'title': metadata.get('title', base_name),
        'description': metadata.get('description', ''),
        'exercise_file': f"{base_name}.ipynb",
        'answers_file': f"{base_name}-ANSWERS.ipynb",
        'data_file': f"{base_name}-data.zip" if metadata.get('data_files') else None,
        'section': notebook_dir.name,
        'order': metadata.get('order', None),
        'links': metadata.get('links', None)
    }

def create_data_zip(data_patterns, zip_path, base_dir):
    """Create a zip file with files matching the patterns, relative to base_dir."""
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        added_files = set()
        
        for pattern in data_patterns:
            # Resolve pattern relative to notebook directory
            full_pattern = str(base_dir / pattern)
            matches = glob(full_pattern, recursive=True)
            
            if not matches:
                print(f"  Warning: No files match pattern '{pattern}' in {base_dir}")
            
            for file_path in matches:
                file_path = Path(file_path)
                # Calculate the archive name relative to the notebook's directory
                try:
                    arcname = file_path.relative_to(base_dir)
                except ValueError:
                    # If file is outside notebook dir, use full relative path
                    arcname = file_path
                
                if str(file_path) not in added_files:
                    zipf.write(file_path, str(arcname))
                    added_files.add(str(file_path))
        
        print(f"✓ Created {zip_path.name} with {len(added_files)} files")

def process_markdown(markdown_path, output_dir, config):
    """Process a markdown file with frontmatter and return info for index."""
    with open(markdown_path, 'r') as f:
        content = f.read()
    
    frontmatter, markdown_content = extract_markdown_frontmatter(content)
    if not frontmatter:
        print(f"Skipping {markdown_path} - no frontmatter")
        return None
    
    base_name = markdown_path.stem
    markdown_dir = markdown_path.parent
    title = frontmatter.get('title', base_name)
    
    # Create data zip if data files are specified
    if frontmatter.get('data_files'):
        zip_name = f"{base_name}-data.zip"
        create_data_zip(frontmatter['data_files'], output_dir / zip_name, markdown_dir)
    
    # Build the full content with title and download link
    full_content = f"# {title}\n\n"
    if frontmatter.get('data_files'):
        zip_name = f"{base_name}-data.zip"
        full_content += f'<div class="download-box">\n<strong>Download files:</strong> <a href="./{zip_name}">📦 {zip_name}</a>\n</div>\n\n'
    
    # Add links section if present
    if frontmatter.get('links'):
        full_content += "## Useful Links\n\n"
        for link in frontmatter['links']:
            name = link.get('name', 'Link')
            url = link.get('url', '#')
            desc = link.get('description', '')
            if desc:
                full_content += f"- [{name}]({url}) - {desc}\n"
            else:
                full_content += f"- [{name}]({url})\n"
        full_content += "\n"
    
    full_content += markdown_content
    
    # Convert to HTML and save
    html_content = markdown_to_html(full_content, title)
    output_html = output_dir / f"{base_name}.html"
    with open(output_html, 'w') as f:
        f.write(html_content)
    
    print(f"✓ Created {output_html}")
    
    # Return info for index
    return {
        'name': base_name,
        'title': title,
        'description': frontmatter.get('description', ''),
        'html_file': f"{base_name}.html",
        'data_file': f"{base_name}-data.zip" if frontmatter.get('data_files') else None,
        'section': markdown_dir.name,
        'type': 'markdown',
        'order': frontmatter.get('order', None),
        'links': frontmatter.get('links', None)
    }

def create_index(notebooks, config, output_dir):
    """Create index.html with links to all notebooks."""
    github_repo = config['github_repo']
    github_branch = config.get('github_branch', 'main')
    
    # Group notebooks by section
    sections = {}
    for nb in notebooks:
        section = nb['section']
        if section not in sections:
            sections[section] = []
        sections[section].append(nb)
    
    # Build notebooks markdown
    notebooks_md = []
    
    for section, section_items in sorted(sections.items()):
        notebooks_md.append(f'\n## {section}\n')
        
        # Sort items: first by those with order (ascending), then by filename (descending)
        def sort_key(item):
            if item['order'] is not None:
                return (0, item['order'], '')  # Items with order come first
            else:
                return (1, 0, item['name'])  # Then items without order
        
        sorted_items = sorted(section_items, key=sort_key)
        # For items without order, we want descending by name
        items_with_order = [item for item in sorted_items if item['order'] is not None]
        items_without_order = sorted([item for item in sorted_items if item['order'] is None], 
                                   key=lambda x: x['name'], reverse=True)
        sorted_items = items_with_order + items_without_order
        
        for item in sorted_items:
            # Make title a link
            if item.get('type') == 'markdown':
                notebooks_md.append(f"### [{item['title']}](./{item['html_file']})\n")
            else:
                colab_url = f"https://colab.research.google.com/github/{github_repo}/blob/{github_branch}/publish/{item['exercise_file']}"
                notebooks_md.append(f"### [{item['title']}]({colab_url})\n")
            
            if item['description']:
                notebooks_md.append(f"{item['description']}\n")
            
            if item.get('type') == 'markdown':
                # Handle markdown files
                notebooks_md.append('<div>\n')
                # notebooks_md.append(f'📄 View: <a href="./{item["html_file"]}">content</a><br>\n')
                if item['data_file']:
                    notebooks_md.append(f'📦 Data: <a href="./{item["data_file"]}">{item["data_file"]}</a><br>\n')
                notebooks_md.append('</div>\n')
            else:
                # Handle notebooks
                colab_url = f"https://colab.research.google.com/github/{github_repo}/blob/{github_branch}/publish/{item['exercise_file']}"
                answers_colab_url = f"https://colab.research.google.com/github/{github_repo}/blob/{github_branch}/publish/{item['answers_file']}"
                
                notebooks_md.append('<div class="resource-buttons">\n')
                notebooks_md.append(f'<a href="{colab_url}" class="resource-button primary">🚀 Live coding worksheet</a>\n')
                notebooks_md.append(f'<a href="{answers_colab_url}" class="resource-button completed">✓ Completed version</a>\n')
                notebooks_md.append('</div>\n')
                
                notebooks_md.append('<div class="download-links">\n')
                notebooks_md.append(f'📓 Download: <a href="./{item["exercise_file"]}">worksheet</a> | ')
                notebooks_md.append(f'<a href="./{item["answers_file"]}">completed</a><br>\n')
                if item['data_file']:
                    notebooks_md.append(f'📦 Data: <a href="./{item["data_file"]}">{item["data_file"]}</a>\n')
                notebooks_md.append('</div>\n')
            
            # Add links if present
            if item.get('links'):
                notebooks_md.append('\n**Links:**\n\n')
                notebooks_md.append("<ul>")
                for link in item['links']:
                    name = link.get('name', 'Link')
                    url = link.get('url', '#')
                    desc = link.get('description', '')
                    if desc:
                        notebooks_md.append(f'<li><a href="{url}">{name}</a> {desc}</li>\n')
                    else:
                        notebooks_md.append(f'<li><a href="{url}">{name}</a></li>\n')
            notebooks_md.append("</ul>")
            notebooks_md.append("\n\n")
            notebooks_md.append("")  # Empty line between items
    
    # Use template from config or default
    template = config.get('index_template', '''# {{ title }}

{{ description }}

## Materials

{{ notebooks }}
''')
    
    # Replace template variables
    index_content = template
    index_content = index_content.replace('{{ title }}', config.get('title', 'Workshop'))
    index_content = index_content.replace('{{ description }}', config.get('description', ''))
    index_content = index_content.replace('{{ notebooks }}', '\n'.join(notebooks_md))
    index_content = index_content.replace('{{ author }}', config.get('author', ''))
    index_content = index_content.replace('{{ organization }}', config.get('organization', ''))
    
    # Convert to HTML and write
    html_content = markdown_to_html(index_content, config.get('title', 'Workshop'))
    with open(output_dir / 'index.html', 'w') as f:
        f.write(html_content)
    
    print(f"✓ Created {output_dir / 'index.html'}")

def main():
    """Process all notebooks and create data packages."""
    config = load_config()
    output_dir = Path(config.get('output_dir', 'publish'))
    
    # Clean up old publish directory
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
        print(f"✓ Cleaned up old {output_dir}/ directory")
    
    output_dir.mkdir(exist_ok=True)
    
    # Look for notebooks and markdown files in configured sections
    sections = config.get('sections', [])
    if not sections:
        print("Warning: No sections defined in workshop-config.yaml")
        return
    
    processed_items = []
    
    for section in sections:
        if isinstance(section, dict):
            folder = section.get('folder')
            title = section.get('title', folder)
        else:
            # Handle if sections is a list of strings
            folder = section
            title = section
            
        if not folder or not Path(folder).exists():
            print(f"Warning: Section folder '{folder}' not found")
            continue
            
        # Process notebooks
        for notebook_path in Path(folder).glob('*.ipynb'):
            # Skip checkpoints
            if '.ipynb_checkpoints' in str(notebook_path):
                continue
            
            print(f"\nProcessing {notebook_path}")
            notebook_info = process_notebook(notebook_path, output_dir, config)
            if notebook_info:
                # Override section with configured title
                notebook_info['section'] = title
                notebook_info['section_folder'] = folder
                processed_items.append(notebook_info)
        
        # Process markdown files
        for markdown_path in Path(folder).glob('*.md'):
            print(f"\nProcessing {markdown_path}")
            markdown_info = process_markdown(markdown_path, output_dir, config)
            if markdown_info:
                # Override section with configured title
                markdown_info['section'] = title
                markdown_info['section_folder'] = folder
                processed_items.append(markdown_info)
    
    # Create index.html
    if processed_items:
        print("\nCreating index.html...")
        create_index(processed_items, config, output_dir)
    
    print(f"\n✓ Published {len(processed_items)} items to {output_dir}/")

if __name__ == '__main__':
    main()