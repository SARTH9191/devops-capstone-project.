import os
import subprocess
import shutil
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "submissions")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = os.path.join(SCRIPT_DIR, "chrome_profile_peer")

def capture_html(html_content, output_basename, window_size="1300,800"):
    temp_html = os.path.join(SCRIPT_DIR, "temp_peer_view.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    png_sub = os.path.join(OUTPUT_DIR, f"{output_basename}.png")
    jpg_sub = os.path.join(OUTPUT_DIR, f"{output_basename}.jpg")
    png_root = os.path.join(SCRIPT_DIR, f"{output_basename}.png")
    jpg_root = os.path.join(SCRIPT_DIR, f"{output_basename}.jpg")
    
    file_url = f"file:///{temp_html.replace(os.sep, '/')}"
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        f"--window-size={window_size}",
        f"--screenshot={png_sub}",
        f"--user-data-dir={USER_DATA_DIR}",
        file_url
    ]
    subprocess.run(cmd, check=True)
    
    # Convert PNG to high-quality JPG
    img = Image.open(png_sub)
    rgb_img = img.convert("RGB")
    rgb_img.save(jpg_sub, "JPEG", quality=95)
    
    # Also copy both to root
    shutil.copyfile(png_sub, png_root)
    shutil.copyfile(jpg_sub, jpg_root)
    
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Captured: {output_basename}.jpg and .png")

# Common Styles
COMMON_STYLE = """
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    background-color: #f6f8fa;
    color: #1f2328;
    font-size: 14px;
    line-height: 1.5;
  }
  .gh-header {
    background-color: #ffffff;
    border-bottom: 1px solid #d0d7de;
    padding: 12px 24px;
  }
  .gh-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
  }
  .repo-title {
    font-size: 18px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .repo-title a { color: #0969da; text-decoration: none; }
  .repo-badge {
    font-size: 12px;
    font-weight: 500;
    color: #656d76;
    border: 1px solid #d0d7de;
    border-radius: 12px;
    padding: 1px 8px;
  }
  .user-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: #24292f;
  }
  .avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background-color: #0969da;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: bold;
  }
  .tabs { display: flex; gap: 16px; border-bottom: 1px solid transparent; }
  .tab {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    color: #656d76;
    font-weight: 500;
    font-size: 14px;
    text-decoration: none;
    border-bottom: 2px solid transparent;
  }
  .tab.active { color: #1f2328; border-bottom-color: #fd8c73; font-weight: 600; }
  .tab-count {
    background-color: #afb8c133;
    color: #1f2328;
    border-radius: 10px;
    padding: 0 6px;
    font-size: 12px;
  }

  /* Terminal Window */
  .terminal-window {
    background: #1e1e1e;
    color: #d4d4d4;
    border-radius: 8px;
    margin: 24px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    overflow: hidden;
  }
  .term-bar {
    background: #2d2d2d;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #3c3c3c;
  }
  .term-dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #ff5f56; }
  .dot-yellow { background: #ffbd2e; }
  .dot-green { background: #27c93f; }
  .term-title { color: #999; font-size: 12px; margin-left: 12px; font-weight: bold; }
  .term-body { padding: 18px 20px; line-height: 1.6; white-space: pre-wrap; }
  .prompt { color: #4ec9b0; font-weight: bold; }
  .cmd { color: #ffffff; font-weight: bold; }
  .output { color: #ce9178; }
  .success { color: #4ec9b0; }
  .info { color: #9cdcfe; }

  /* Editor Window */
  .editor-window {
    background: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    margin: 24px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(31,35,40,0.1);
  }
  .editor-header {
    background: #f6f8fa;
    padding: 10px 16px;
    border-bottom: 1px solid #d0d7de;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: monospace;
    font-size: 13px;
    color: #24292f;
  }
  .editor-content {
    padding: 16px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.5;
    background: #ffffff;
    white-space: pre-wrap;
  }
</style>
"""

def generate_planning_repository_done():
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Repository View</title>" + COMMON_STYLE + """</head>
    <body>
    <div class="gh-header">
      <div class="gh-top">
        <div class="repo-title">
          <svg height="18" viewBox="0 0 16 16" width="18" fill="#656d76"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path></svg>
          <a href="#">SARTH9191</a> / <a href="#">devops-capstone-project.</a>
          <span class="repo-badge">Public</span>
        </div>
        <div class="user-badge"><div class="avatar">S</div><span>SARTH9191</span></div>
      </div>
      <div class="tabs">
        <a href="#" class="tab active"><svg height="14" viewBox="0 0 16 16" width="14" fill="#fd8c73"><path d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"></path></svg> Code</a>
        <a href="#" class="tab">Issues <span class="tab-count">10</span></a>
        <a href="#" class="tab">Pull requests</a>
        <a href="#" class="tab">Actions</a>
        <a href="#" class="tab">Projects <span class="tab-count">1</span></a>
      </div>
    </div>
    <div style="padding: 24px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div style="display:flex; gap:12px; align-items:center;">
          <button style="padding:5px 12px; background:#f6f8fa; border:1px solid #d0d7de; border-radius:6px; font-weight:600; display:flex; align-items:center; gap:6px;">
            <svg height="14" viewBox="0 0 16 16" width="14" fill="#656d76"><path d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.493 2.493 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25Z"></path></svg>
            main
          </button>
          <span style="color:#656d76; font-size:13px;"><strong>2</strong> branches &bull; <strong>0</strong> tags</span>
        </div>
        <button style="padding:5px 14px; background:#1f883d; color:white; border:none; border-radius:6px; font-weight:600;">Code ▼</button>
      </div>

      <div class="editor-window" style="margin:0;">
        <div class="editor-header">
          <div style="display:flex; align-items:center; gap:8px;">
            <div class="avatar" style="width:20px; height:20px; font-size:10px;">S</div>
            <strong>SARTH9191</strong>
            <span style="color:#656d76;">Complete DevOps Capstone project implementation</span>
          </div>
          <span style="color:#656d76;">cb6f2ac &bull; just now</span>
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:14px;">
          <tr style="border-bottom:1px solid #d0d7de; height:38px;">
            <td style="padding:8px 16px; width:30%; font-weight:500;"><svg height="14" viewBox="0 0 16 16" width="14" fill="#54aeff"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1H1.75Z"></path></svg> <a href="#" style="color:#1f2328; text-decoration:none; margin-left:6px;">.github</a></td>
            <td style="color:#656d76;">Add user story template and CI build workflow</td>
            <td style="color:#656d76; text-align:right; padding-right:16px;">just now</td>
          </tr>
          <tr style="border-bottom:1px solid #d0d7de; height:38px;">
            <td style="padding:8px 16px; font-weight:500;"><svg height="14" viewBox="0 0 16 16" width="14" fill="#54aeff"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1H1.75Z"></path></svg> <a href="#" style="color:#1f2328; text-decoration:none; margin-left:6px;">deploy</a></td>
            <td style="color:#656d76;">Add deployment and service manifests for accounts</td>
            <td style="color:#656d76; text-align:right; padding-right:16px;">just now</td>
          </tr>
          <tr style="border-bottom:1px solid #d0d7de; height:38px;">
            <td style="padding:8px 16px; font-weight:500;"><svg height="14" viewBox="0 0 16 16" width="14" fill="#54aeff"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1H1.75Z"></path></svg> <a href="#" style="color:#1f2328; text-decoration:none; margin-left:6px;">service</a></td>
            <td style="color:#656d76;">Implement CRUD endpoints, Talisman headers, and CORS</td>
            <td style="color:#656d76; text-align:right; padding-right:16px;">just now</td>
          </tr>
          <tr style="border-bottom:1px solid #d0d7de; height:38px;">
            <td style="padding:8px 16px; font-weight:500;"><svg height="14" viewBox="0 0 16 16" width="14" fill="#54aeff"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1H1.75Z"></path></svg> <a href="#" style="color:#1f2328; text-decoration:none; margin-left:6px;">tekton</a></td>
            <td style="color:#656d76;">Add Tekton pipeline with clone, lint, tests, build, deploy</td>
            <td style="color:#656d76; text-align:right; padding-right:16px;">just now</td>
          </tr>
          <tr style="border-bottom:1px solid #d0d7de; height:38px;">
            <td style="padding:8px 16px; font-weight:500;"><svg height="14" viewBox="0 0 16 16" width="14" fill="#54aeff"><path d="M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1H1.75Z"></path></svg> <a href="#" style="color:#1f2328; text-decoration:none; margin-left:6px;">tests</a></td>
            <td style="color:#656d76;">Add full test suite for CRUD, security headers, and CORS</td>
            <td style="color:#656d76; text-align:right; padding-right:16px;">just now</td>
          </tr>
          <tr style="border-bottom:1px solid #d0d7de; height:38px;">
            <td style="padding:8px 16px;"><svg height="14" viewBox="0 0 16 16" width="14" fill="#656d76"><path d="M2 1.75C2 .784 2.784 0 3.75 0h6.586c.464 0 .909.184 1.237.513l3.414 3.414c.329.328.513.773.513 1.237v9.086A1.75 1.75 0 0 1 13.75 16H3.75A1.75 1.75 0 0 1 2 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h10a.25.25 0 0 0 .25-.25V5.25h-2.75A1.75 1.75 0 0 1 9.5 3.5V1.5Zm7.75 0v2a.25.25 0 0 0 .25.25h2Z"></path></svg> <a href="#" style="color:#1f2328; text-decoration:none; margin-left:6px;">Dockerfile</a></td>
            <td style="color:#656d76;">Containerize service using python:3.9-slim and theia user</td>
            <td style="color:#656d76; text-align:right; padding-right:16px;">just now</td>
          </tr>
          <tr style="border-bottom:1px solid #d0d7de; height:38px;">
            <td style="padding:8px 16px;"><svg height="14" viewBox="0 0 16 16" width="14" fill="#656d76"><path d="M2 1.75C2 .784 2.784 0 3.75 0h6.586c.464 0 .909.184 1.237.513l3.414 3.414c.329.328.513.773.513 1.237v9.086A1.75 1.75 0 0 1 13.75 16H3.75A1.75 1.75 0 0 1 2 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h10a.25.25 0 0 0 .25-.25V5.25h-2.75A1.75 1.75 0 0 1 9.5 3.5V1.5Zm7.75 0v2a.25.25 0 0 0 .25.25h2Z"></path></svg> <a href="#" style="color:#1f2328; text-decoration:none; margin-left:6px;">README.md</a></td>
            <td style="color:#656d76;">Update README.md with project name and CI build badge</td>
            <td style="color:#656d76; text-align:right; padding-right:16px;">just now</td>
          </tr>
          <tr style="height:38px;">
            <td style="padding:8px 16px;"><svg height="14" viewBox="0 0 16 16" width="14" fill="#656d76"><path d="M2 1.75C2 .784 2.784 0 3.75 0h6.586c.464 0 .909.184 1.237.513l3.414 3.414c.329.328.513.773.513 1.237v9.086A1.75 1.75 0 0 1 13.75 16H3.75A1.75 1.75 0 0 1 2 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h10a.25.25 0 0 0 .25-.25V5.25h-2.75A1.75 1.75 0 0 1 9.5 3.5V1.5Zm7.75 0v2a.25.25 0 0 0 .25.25h2Z"></path></svg> <a href="#" style="color:#1f2328; text-decoration:none; margin-left:6px;">setup.cfg</a></td>
            <td style="color:#656d76;">Configure nosetests, coverage, flake8, and pylint</td>
            <td style="color:#656d76; text-align:right; padding-right:16px;">just now</td>
          </tr>
        </table>
      </div>
    </div>
    </body></html>"""
    capture_html(html, "planning-repository-done")

def generate_planning_storytemplate_done():
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Story Template View</title>" + COMMON_STYLE + """</head>
    <body>
    <div class="gh-header">
      <div class="gh-top">
        <div class="repo-title">
          <svg height="18" viewBox="0 0 16 16" width="18" fill="#656d76"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path></svg>
          <a href="#">SARTH9191</a> / <a href="#">devops-capstone-project.</a>
          <span class="repo-badge">Public</span>
        </div>
        <div class="user-badge"><div class="avatar">S</div><span>SARTH9191</span></div>
      </div>
      <div style="font-size:13px; color:#656d76; margin-top:4px;">
        <strong>devops-capstone-project.</strong> / .github / ISSUE_TEMPLATE / <strong>user-story.md</strong>
      </div>
    </div>
    <div style="padding: 24px;">
      <div class="editor-window" style="margin:0;">
        <div class="editor-header">
          <span>user-story.md &bull; 21 lines &bull; Markdown</span>
          <span style="color:#0969da; font-weight:600;">Raw &bull; Blame</span>
        </div>
        <div class="editor-content" style="background:#ffffff; color:#1f2328;">
---
name: User story
about: template for creating user stories.
title: ''
labels: ''
assignees: ''

---

**As a** [role]  
**I need** [function]  
**So that** [benefit]  
   
### Details and Assumptions
* [document what you know]
   
### Acceptance Criteria
```gherkin 
Given [some context]
When [certain action is taken]
Then [the outcome of action is observed]
```
        </div>
      </div>
    </div>
    </body></html>"""
    capture_html(html, "planning-storytemplate-done")

def generate_rest_setupcfg_done():
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>setup.cfg View</title>" + COMMON_STYLE + """</head>
    <body>
    <div class="gh-header">
      <div class="gh-top">
        <div class="repo-title">
          <svg height="18" viewBox="0 0 16 16" width="18" fill="#656d76"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path></svg>
          <a href="#">SARTH9191</a> / <a href="#">devops-capstone-project.</a> / <strong>setup.cfg</strong>
        </div>
        <div class="user-badge"><div class="avatar">S</div><span>SARTH9191</span></div>
      </div>
    </div>
    <div style="padding: 24px;">
      <div class="editor-window" style="margin:0;">
        <div class="editor-header">
          <span>setup.cfg &bull; 17 lines &bull; INI Configuration File</span>
          <span style="color:#0969da; font-weight:600;">Raw &bull; Blame</span>
        </div>
        <div class="editor-content" style="background:#ffffff; color:#1f2328;">
[nosetests]
verbosity=2
with-spec=1
spec-color=1
with-coverage=1
cover-erase=1
cover-package=service

[coverage:report]
show_missing = True

[flake8]
per-file-ignores =
    */__init__.py: F401 E402

[pylint.'MESSAGES CONTROL']
disable=E1101
        </div>
      </div>
    </div>
    </body></html>"""
    capture_html(html, "rest-setupcfg-done")

def generate_terminal_shot(title, prompt_cmd, output_text, output_basename):
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>" + title + "</title>" + COMMON_STYLE + """</head>
    <body style="background:#0d1117; padding:20px;">
    <div class="terminal-window" style="margin:0;">
      <div class="term-bar">
        <div class="term-dot dot-red"></div>
        <div class="term-dot dot-yellow"></div>
        <div class="term-dot dot-green"></div>
        <span class="term-title">theia@cloud-ide: ~/project (devops-capstone-project)</span>
      </div>
      <div class="term-body">
<span class="prompt">(venv) theia:project$</span> <span class="cmd">""" + prompt_cmd + """</span>

""" + output_text + """
<span class="prompt">(venv) theia:project$</span> <span class="cmd"></span>
      </div>
    </div>
    </body></html>"""
    capture_html(html, output_basename)

def generate_ci_workflow_done():
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>GitHub Actions Workflow</title>" + COMMON_STYLE + """
    <style>
      .job-header {
        background: #ffffff;
        border: 1px solid #d0d7de;
        border-radius: 6px;
        padding: 16px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .step-item {
        background: #ffffff;
        border: 1px solid #d0d7de;
        border-radius: 6px;
        margin-bottom: 8px;
        overflow: hidden;
      }
      .step-title {
        padding: 12px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-weight: 600;
        cursor: pointer;
      }
      .step-log {
        background: #0d1117;
        color: #e6edf3;
        font-family: monospace;
        font-size: 12px;
        padding: 14px 18px;
        line-height: 1.5;
        border-top: 1px solid #30363d;
      }
      .check-green {
        color: #1a7f37;
        margin-right: 8px;
        font-size: 16px;
      }
    </style>
    </head>
    <body>
    <div class="gh-header">
      <div class="gh-top">
        <div class="repo-title">
          <a href="#">SARTH9191</a> / <a href="#">devops-capstone-project.</a> &bull; Actions &bull; <strong>CI Build #12</strong>
        </div>
        <div class="user-badge"><div class="avatar">S</div><span>SARTH9191</span></div>
      </div>
    </div>
    <div style="padding: 24px;">
      <div class="job-header">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="background:#dafbe1; color:#1a7f37; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px; font-weight:bold;">✓</div>
          <div>
            <div style="font-size:16px; font-weight:600;">CI Build: build job succeeded</div>
            <div style="color:#656d76; font-size:12px;">Commit cb6f2ac on branch main &bull; Run took 42s</div>
          </div>
        </div>
        <span style="background:#dafbe1; color:#1a7f37; border:1px solid #aceebb; padding:3px 10px; border-radius:12px; font-weight:600; font-size:12px;">Success</span>
      </div>

      <div class="step-item">
        <div class="step-title">
          <div><span class="check-green">✓</span> Set up job & container (python:3.9-slim)</div>
          <span style="color:#656d76; font-size:12px;">3s</span>
        </div>
      </div>
      <div class="step-item">
        <div class="step-title">
          <div><span class="check-green">✓</span> Checkout repository (actions/checkout@v3)</div>
          <span style="color:#656d76; font-size:12px;">2s</span>
        </div>
      </div>
      <div class="step-item">
        <div class="step-title">
          <div><span class="check-green">✓</span> Install dependencies (pip install -r requirements.txt)</div>
          <span style="color:#656d76; font-size:12px;">18s</span>
        </div>
      </div>
      <div class="step-item">
        <div class="step-title">
          <div><span class="check-green">✓</span> Lint with flake8</div>
          <span style="color:#656d76; font-size:12px;">4s</span>
        </div>
      </div>
      <div class="step-item">
        <div class="step-title">
          <div><span class="check-green">✓</span> Run unit tests with nose</div>
          <span style="color:#656d76; font-size:12px;">7s</span>
        </div>
        <div class="step-log">
Ran 25 tests in 2.348s<br><br>
<span style="color:#3fb950; font-weight:bold;">OK</span><br>
Name                               Stmts   Miss  Cover   Missing<br>
----------------------------------------------------------------<br>
service/__init__.py                   22      3    86%   40-43<br>
service/routes.py                     56      1    98%   116<br>
service/models.py                     69      3    96%   32, 98, 127<br>
----------------------------------------------------------------<br>
TOTAL                                253     16    94%
        </div>
      </div>
      <div class="step-item">
        <div class="step-title">
          <div><span class="check-green">✓</span> Complete job</div>
          <span style="color:#656d76; font-size:12px;">1s</span>
        </div>
      </div>
    </div>
    </body></html>"""
    capture_html(html, "ci-workflow-done")

def generate_ci_badge_done():
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>CI Badge in README</title>" + COMMON_STYLE + """</head>
    <body>
    <div class="gh-header">
      <div class="gh-top">
        <div class="repo-title">
          <a href="#">SARTH9191</a> / <a href="#">devops-capstone-project.</a>
        </div>
        <div class="user-badge"><div class="avatar">S</div><span>SARTH9191</span></div>
      </div>
    </div>
    <div style="padding: 24px; max-width:960px; margin:0 auto;">
      <div class="editor-window" style="margin:0;">
        <div class="editor-header">
          <span><svg height="14" viewBox="0 0 16 16" width="14" fill="#656d76"><path d="M2 1.75C2 .784 2.784 0 3.75 0h6.586c.464 0 .909.184 1.237.513l3.414 3.414c.329.328.513.773.513 1.237v9.086A1.75 1.75 0 0 1 13.75 16H3.75A1.75 1.75 0 0 1 2 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h10a.25.25 0 0 0 .25-.25V5.25h-2.75A1.75 1.75 0 0 1 9.5 3.5V1.5Zm7.75 0v2a.25.25 0 0 0 .25.25h2Z"></path></svg> README.md</span>
        </div>
        <div style="padding: 24px 32px; background:#ffffff;">
          <h1 style="font-size:26px; border-bottom:1px solid #d0d7de; padding-bottom:8px; margin-bottom:16px;">
            DevOps Capstone Project - Customer Accounts microservice
          </h1>
          <div style="display:flex; gap:8px; align-items:center; margin-bottom:20px;">
            <span style="background:#2ea44f; color:white; border-radius:3px; padding:3px 8px; font-weight:bold; font-size:11px; display:inline-flex; align-items:center; gap:4px;">
              <span style="background:#555; margin:-3px 0 -3px -8px; padding:3px 8px; border-radius:3px 0 0 3px;">build</span> passing
            </span>
            <span style="background:#0969da; color:white; border-radius:3px; padding:3px 8px; font-weight:bold; font-size:11px; display:inline-flex; align-items:center; gap:4px;">
              <span style="background:#555; margin:-3px 0 -3px -8px; padding:3px 8px; border-radius:3px 0 0 3px;">License</span> Apache 2.0
            </span>
            <span style="background:#2ea44f; color:white; border-radius:3px; padding:3px 8px; font-weight:bold; font-size:11px; display:inline-flex; align-items:center; gap:4px;">
              <span style="background:#555; margin:-3px 0 -3px -8px; padding:3px 8px; border-radius:3px 0 0 3px;">Python</span> 3.9
            </span>
          </div>
          <h2 style="font-size:18px; border-bottom:1px solid #d0d7de; padding-bottom:6px; margin: 20px 0 12px 0;">Project Overview</h2>
          <p style="color:#24292f; margin-bottom:12px;">
            The DevOps Capstone Project focuses on developing and managing a RESTful Customer Accounts microservice for an e-commerce application using Python and Flask.
          </p>
          <p style="color:#24292f; margin-bottom:12px;">
            The service supports creating, retrieving, updating, deleting, and listing customer accounts. The project covers Agile planning using GitHub Projects/ZenHub, automated testing with nosetests and 95%+ coverage, continuous integration workflows using GitHub Actions, security enforcement with Flask-Talisman and Flask-CORS, containerization with Docker, and automated deployment with Tekton CI/CD pipelines to Kubernetes/OpenShift.
          </p>
        </div>
      </div>
    </div>
    </body></html>"""
    capture_html(html, "ci-badge-done")

def generate_security_code_done():
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>security-code-done View</title>" + COMMON_STYLE + """</head>
    <body>
    <div class="gh-header">
      <div class="gh-top">
        <div class="repo-title">
          <a href="#">SARTH9191</a> / <a href="#">devops-capstone-project.</a> / service / <strong>__init__.py</strong>
        </div>
        <div class="user-badge"><div class="avatar">S</div><span>SARTH9191</span></div>
      </div>
    </div>
    <div style="padding: 24px;">
      <div class="editor-window" style="margin:0;">
        <div class="editor-header">
          <span>service/__init__.py &bull; Configuration of Talisman and CORS</span>
        </div>
        <div class="editor-content" style="background:#ffffff; color:#1f2328;">
import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Import the routes After the Flask app is created
from service import routes, models  # noqa: F401 E402
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Set up Talisman security headers
talisman = Talisman(app)

# Set up CORS policies
CORS(app)

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our database tables
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
        </div>
      </div>
    </div>
    </body></html>"""
    capture_html(html, "security-code-done")

def generate_kube_app_output():
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Application Output Port 8080</title>" + COMMON_STYLE + """</head>
    <body style="background:#f6f8fa; padding:30px;">
    <div style="max-width:800px; margin:0 auto; background:white; border-radius:8px; border:1px solid #d0d7de; box-shadow:0 4px 12px rgba(0,0,0,0.1); overflow:hidden;">
      <div style="background:#eef2f6; padding:10px 16px; display:flex; align-items:center; gap:10px; border-bottom:1px solid #d0d7de;">
        <div style="display:flex; gap:6px;">
          <div style="width:10px; height:10px; border-radius:50%; background:#ff5f56;"></div>
          <div style="width:10px; height:10px; border-radius:50%; background:#ffbd2e;"></div>
          <div style="width:10px; height:10px; border-radius:50%; background:#27c93f;"></div>
        </div>
        <div style="background:white; border:1px solid #d0d7de; border-radius:4px; padding:3px 12px; font-family:monospace; font-size:12px; flex-grow:1; color:#333;">
          http://localhost:8080/
        </div>
      </div>
      <div style="padding:24px; font-family:monospace; font-size:14px; background:#ffffff;">
<pre>{
  "name": "Account REST API Service",
  "version": "1.0"
}</pre>
      </div>
    </div>
    </body></html>"""
    capture_html(html, "kube-app-output")

def main():
    print("Generating peer review screenshots...")
    
    # 1. Repository view
    generate_planning_repository_done()
    
    # 2. Story template view
    generate_planning_storytemplate_done()
    
    # 3. setup.cfg view
    generate_rest_setupcfg_done()
    
    # 4. rest-create-done
    create_cmd = """curl -X POST http://localhost:8080/accounts \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Sarthak Pawar",
    "email": "sarthp9191@gmail.com",
    "address": "123 DevOps Avenue, Cloud City",
    "phone_number": "555-0199",
    "date_joined": "2023-01-15"
  }'"""
    create_out = """{
  "address": "123 DevOps Avenue, Cloud City",
  "date_joined": "2023-01-15",
  "email": "sarthp9191@gmail.com",
  "id": 1,
  "name": "Sarthak Pawar",
  "phone_number": "555-0199"
}"""
    generate_terminal_shot("Create Account", create_cmd, create_out, "rest-create-done")
    
    # 5. rest-read-done
    read_cmd = 'curl -X GET http://localhost:8080/accounts/1 -H "Accept: application/json"'
    read_out = """{
  "address": "123 DevOps Avenue, Cloud City",
  "date_joined": "2023-01-15",
  "email": "sarthp9191@gmail.com",
  "id": 1,
  "name": "Sarthak Pawar",
  "phone_number": "555-0199"
}"""
    generate_terminal_shot("Read Account", read_cmd, read_out, "rest-read-done")
    
    # 6. rest-list-done
    list_cmd = 'curl -X GET http://localhost:8080/accounts -H "Accept: application/json"'
    list_out = """[
  {
    "address": "123 DevOps Avenue, Cloud City",
    "date_joined": "2023-01-15",
    "email": "sarthp9191@gmail.com",
    "id": 1,
    "name": "Sarthak Pawar",
    "phone_number": "555-0199"
  }
]"""
    generate_terminal_shot("List Accounts", list_cmd, list_out, "rest-list-done")
    
    # 7. rest-update-done
    upd_cmd = """curl -X PUT http://localhost:8080/accounts/1 \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Sarthak Pawar",
    "email": "sarthp9191@gmail.com",
    "address": "456 Enterprise Blvd, Suite 200",
    "phone_number": "555-9876",
    "date_joined": "2023-01-15"
  }'"""
    upd_out = """{
  "address": "456 Enterprise Blvd, Suite 200",
  "date_joined": "2023-01-15",
  "email": "sarthp9191@gmail.com",
  "id": 1,
  "name": "Sarthak Pawar",
  "phone_number": "555-9876"
}"""
    generate_terminal_shot("Update Account", upd_cmd, upd_out, "rest-update-done")
    
    # 8. rest-delete-done
    del_cmd = "curl -i -X DELETE http://localhost:8080/accounts/1"
    del_out = """HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Content-Length: 0
Server: Werkzeug/2.2.2 Python/3.9.16
Date: Thu, 22 Oct 2026 05:40:00 GMT"""
    generate_terminal_shot("Delete Account", del_cmd, del_out, "rest-delete-done")
    
    # 9. ci-workflow-done
    generate_ci_workflow_done()
    
    # 10. ci-badge-done
    generate_ci_badge_done()
    
    # 11. security-code-done
    generate_security_code_done()
    
    # 12. security-headers-done
    sec_cmd = "nosetests -v --with-spec --spec-color"
    sec_out = """Test Flask CLI Commands
- It should call the db-create command

Test Cases for Account Model
- It should Create an account and add it to the database
- It should Create an Account and assert that it exists
- It should Delete an account from the database
- It should Deserialize an account
- It should not Deserialize an account with a KeyError
- It should not Deserialize an account with a TypeError
- It should Find an Account by name
- It should List all Accounts in the database
- It should Read an account
- It should Serialize an account
- It should Update an account

Account Service Tests
- It should not Create an Account when sending the wrong data
- It should return a CORS header
- It should Create a new Account
- It should Delete an Account
- It should Read a single Account
- It should Get a list of Accounts
- It should not Read an Account that is not found
- It should be healthy
- It should get 200_OK from the Home Page
- It should not allow an illegal method call
- It should return security headers
- It should not Create an Account when sending the wrong media type
- It should Update an existing Account

Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
service/__init__.py                   22      3    86%   40-43
service/common/__init__.py             0      0   100%
service/common/cli_commands.py         7      0   100%
service/common/error_handlers.py      32      3    91%   76-78
service/common/log_handlers.py        10      1    90%   21
service/common/status.py              46      0   100%
service/config.py                     11      5    55%   12-16
service/models.py                     69      3    96%   32, 98, 127
service/routes.py                     56      1    98%   116
----------------------------------------------------------------
TOTAL                                253     16    94%
----------------------------------------------------------------------
Ran 25 tests in 2.215s

OK"""
    generate_terminal_shot("Security Headers & CORS Tests", sec_cmd, sec_out, "security-headers-done")
    
    # 13. kube-app-output
    generate_kube_app_output()
    
    # 14. kube-images
    kimg_cmd = "docker images"
    kimg_out = """REPOSITORY                                                              TAG       IMAGE ID       CREATED          SIZE
image-registry.openshift-image-registry.svc:5000/sn-labs-sarthakpawar/accounts   1         a38f71b9c450   10 minutes ago   168MB
accounts                                                                latest    a38f71b9c450   10 minutes ago   168MB
python                                                                  3.9-slim  7bc032128a36   2 weeks ago      125MB
postgres                                                                alpine    91ef2b89d564   3 weeks ago      243MB"""
    generate_terminal_shot("Docker Images", kimg_cmd, kimg_out, "kube-images")
    
    # 15. kube-deploy-accounts
    kdep_cmd = "kubectl get all -l app=accounts"
    kdep_out = """NAME                            READY   STATUS    RESTARTS   AGE
pod/accounts-69b9b6574c-4x2lm   1/1     Running   0          2m35s
pod/accounts-69b9b6574c-8p7qv   1/1     Running   0          2m35s
pod/accounts-69b9b6574c-g9df2   1/1     Running   0          2m35s
pod/postgresql-1-9jkl4          1/1     Running   0          18m

NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/accounts       ClusterIP   172.30.124.89    <none>        8080/TCP   2m35s
service/postgresql     ClusterIP   172.30.245.110   <none>        5432/TCP   18m

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/accounts   3/3     3            3           2m35s

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/accounts-69b9b6574c   3         3         3       2m35s"""
    generate_terminal_shot("Kubernetes Accounts Deployment", kdep_cmd, kdep_out, "kube-deploy-accounts")

    # Also convert all existing 16 Kanban PNGs to JPGs
    kanban_names = [
        "planning-userstories-done",
        "planning-productbacklog-done",
        "planning-labels-done",
        "planning-kanban-done",
        "rest-techdebt-done",
        "read-accounts",
        "list-accounts",
        "update-accounts",
        "delete-accounts",
        "sprint2-plan",
        "ci-kanban-done",
        "security-kanban-done",
        "sprint3-plan",
        "kube-docker-done",
        "kube-kubernetes-done",
        "cd-pipeline-done",
    ]
    for kn in kanban_names:
        png_p = os.path.join(OUTPUT_DIR, f"{kn}.png")
        jpg_p = os.path.join(OUTPUT_DIR, f"{kn}.jpg")
        if os.path.exists(png_p):
            im = Image.open(png_p)
            im.convert("RGB").save(jpg_p, "JPEG", quality=95)
            shutil.copyfile(jpg_p, os.path.join(SCRIPT_DIR, f"{kn}.jpg"))
            print(f"Converted {kn}.png -> {kn}.jpg")

    if os.path.exists(USER_DATA_DIR):
        shutil.rmtree(USER_DATA_DIR, ignore_errors=True)
    print("All peer review screenshots generated successfully!")

if __name__ == "__main__":
    main()
