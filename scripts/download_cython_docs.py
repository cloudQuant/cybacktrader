import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
import markdownify

def create_directory(path):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(path, exist_ok=True)
        return path
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        return None

def sanitize_filename(filename):
    """Sanitize filename for Windows"""
    # Remove or replace invalid characters for Windows filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_safe_path(base_path, url_path, extension='.md'):
    """Convert URL path to safe Windows file path with .md extension"""
    # Split the path and sanitize each component
    path_parts = url_path.strip('/').split('/')
    sanitized_parts = []

    for part in path_parts:
        if part and part != '.':
            # Sanitize the part
            safe_part = sanitize_filename(part)
            if safe_part:
                sanitized_parts.append(safe_part)

    # If no valid parts, use index.md
    if not sanitized_parts:
        return os.path.join(base_path, 'index.md')

    # The last part is the filename (replace .html with .md if present)
    last_part = sanitized_parts[-1]
    # Remove .html extension if present and add .md
    if last_part.endswith('.html'):
        last_part = last_part[:-5]  # Remove .html
    if '.' not in last_part:
        last_part = last_part + extension

    sanitized_parts[-1] = last_part

    # Join with OS separator
    relative_path = os.path.join(*sanitized_parts)
    return os.path.join(base_path, relative_path)

def clean_html_for_markdown(html_content, url):
    """Clean HTML content to improve markdown conversion"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Remove navigation elements that aren't useful in markdown
    for nav in soup.find_all(['nav', 'header', 'footer']):
        if nav.get('class') and any(cls in nav.get('class') for cls in ['navbar', 'navigation', 'footer']):
            nav.decompose()

    # Convert to string for markdownify
    return str(soup)

def html_to_markdown_with_code_blocks(html_content, url):
    """Convert HTML to markdown, preserving code blocks"""
    # First clean the HTML
    cleaned_html = clean_html_for_markdown(html_content, url)

    # Configure markdownify to preserve code blocks well
    md = markdownify.markdownify(
        cleaned_html,
        heading_style="ATX",  # Use # for headings
        convert=['div', 'span', 'p', 'pre', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a', 'img'],
        default_title=True  # Preserve titles
    )

    # Post-process to ensure code blocks are properly formatted
    lines = md.split('\n')
    processed_lines = []

    for line in lines:
        # Ensure code blocks with language hints are preserved
        if line.strip().startswith('```') and ('python' in line or 'cython' in line or 'py' in line):
            processed_lines.append(line)
        else:
            processed_lines.append(line)

    return '\n'.join(processed_lines)

def download_cython_docs(base_url, output_dir):
    """Download Cython documentation recursively as markdown"""
    visited = set()
    to_visit = {base_url}

    # Ensure output directory exists
    output_dir = os.path.abspath(output_dir)
    if not create_directory(output_dir):
        print("Failed to create output directory")
        return

    # Get base domain for URL filtering
    base_domain = urlparse(base_url).netloc

    # Configure session with SSL verification disabled for problematic certificates
    session = requests.Session()
    session.verify = False  # Disable SSL verification for problematic sites

    print(f"Starting markdown download to: {output_dir}")

    while to_visit:
        try:
            current_url = to_visit.pop()

            if current_url in visited:
                continue

            print(f"Processing: {current_url}")
            visited.add(current_url)

            # Remove URL fragment if present
            if '#' in current_url:
                current_url = current_url.split('#')[0]
                if not current_url:
                    continue

            # Download with timeout and error handling
            try:
                response = session.get(current_url, timeout=30, allow_redirects=True)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error downloading {current_url}: {e}")
                continue

            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Determine save path (as .md file)
            parsed_url = urlparse(current_url)
            url_path = parsed_url.path

            # Handle root URL
            if not url_path or url_path == '/':
                save_path = os.path.join(output_dir, 'index.md')
            else:
                save_path = get_safe_path(output_dir, url_path, '.md')

            # Ensure parent directory exists
            parent_dir = os.path.dirname(save_path)
            if parent_dir and not os.path.exists(parent_dir):
                create_directory(parent_dir)

            # Convert HTML to markdown
            try:
                markdown_content = html_to_markdown_with_code_blocks(response.text, current_url)

                # Save the markdown content
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                print(f"Saved: {save_path}")

            except Exception as e:
                print(f"Error converting to markdown {save_path}: {e}")
                continue

            # Find and process all links on the page
            for link in soup.find_all(['a', 'link']):
                href = link.get('href')
                if not href:
                    continue

                # Convert to absolute URL and remove fragment
                absolute_url = urljoin(current_url, href).split('#')[0]

                # Only process links from the same domain
                if urlparse(absolute_url).netloc != base_domain:
                    continue

                # Skip non-HTML resources and empty URLs
                if (not absolute_url or
                    any(absolute_url.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.css', '.js']) or
                    absolute_url.endswith('/#')):
                    continue

                # Add to queue if not visited
                if absolute_url not in visited and absolute_url not in to_visit:
                    to_visit.add(absolute_url)

            # Be nice to the server - reduced delay
            time.sleep(0.3)

        except KeyboardInterrupt:
            print("\nDownload interrupted by user")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

    print("Markdown download completed!")

def main():
    base_url = "https://cython.readthedocs.io/en/latest/"
    output_dir = os.path.join("docs", "cython_docs")

    print(f"Starting download of Cython documentation to {output_dir}")
    download_cython_docs(base_url, output_dir)

if __name__ == "__main__":
    main()
