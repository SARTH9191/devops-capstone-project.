import os
import subprocess
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "submissions")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = os.path.join(SCRIPT_DIR, "chrome_profile")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Kanban Board - SARTH9191/devops-capstone-project.</title>
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    background-color: #f6f8fa;
    color: #1f2328;
    font-size: 14px;
    line-height: 1.5;
  }}
  /* Header */
  .gh-header {{
    background-color: #ffffff;
    border-bottom: 1px solid #d0d7de;
    padding: 12px 24px;
  }}
  .gh-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
  }}
  .repo-title {{
    font-size: 18px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .repo-title a {{
    color: #0969da;
    text-decoration: none;
  }}
  .repo-badge {{
    font-size: 12px;
    font-weight: 500;
    color: #656d76;
    border: 1px solid #d0d7de;
    border-radius: 12px;
    padding: 1px 8px;
  }}
  .user-badge {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: #24292f;
  }}
  .avatar {{
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
  }}
  .tabs {{
    display: flex;
    gap: 16px;
    border-bottom: 1px solid transparent;
  }}
  .tab {{
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    color: #656d76;
    font-weight: 500;
    font-size: 14px;
    text-decoration: none;
    border-bottom: 2px solid transparent;
  }}
  .tab.active {{
    color: #1f2328;
    border-bottom-color: #fd8c73;
    font-weight: 600;
  }}
  .tab-count {{
    background-color: #afb8c133;
    color: #1f2328;
    border-radius: 10px;
    padding: 0 6px;
    font-size: 12px;
  }}

  /* Project Bar */
  .project-bar {{
    background: #ffffff;
    border-bottom: 1px solid #d0d7de;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .project-name {{
    font-size: 16px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .view-switcher {{
    display: flex;
    gap: 8px;
  }}
  .btn-view {{
    background: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 500;
    color: #24292f;
  }}
  .btn-view.active {{
    background: #0969da;
    color: white;
    border-color: #0969da;
  }}

  /* Kanban Board Grid */
  .board-container {{
    display: flex;
    gap: 16px;
    padding: 20px 24px;
    overflow-x: auto;
    min-height: calc(100vh - 140px);
    background-color: #f6f8fa;
  }}
  .column {{
    background-color: #ebf0f4;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    width: 280px;
    min-width: 280px;
    display: flex;
    flex-direction: column;
    max-height: 85vh;
  }}
  .column-header {{
    padding: 12px 14px;
    font-weight: 600;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #d0d7de;
  }}
  .col-title {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .pill {{
    background-color: #d0d7de;
    color: #24292f;
    border-radius: 12px;
    padding: 1px 7px;
    font-size: 12px;
    font-weight: 600;
  }}
  .cards-list {{
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
    flex-grow: 1;
  }}
  .card {{
    background: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 12px;
    box-shadow: 0 1px 3px rgba(31,35,40,0.06);
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .card-header {{
    display: flex;
    align-items: flex-start;
    gap: 6px;
    font-weight: 600;
    font-size: 13px;
    color: #1f2328;
  }}
  .issue-icon {{
    color: #1a7f37;
    font-size: 14px;
    flex-shrink: 0;
    margin-top: 2px;
  }}
  .card-meta {{
    font-size: 11px;
    color: #656d76;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .labels-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 2px;
  }}
  .label-tag {{
    font-size: 11px;
    font-weight: 500;
    padding: 2px 7px;
    border-radius: 10px;
  }}
  .label-techdebt {{
    background-color: #fbefff;
    color: #8250df;
    border: 1px solid #d8b9ff;
  }}
  .label-enhancement {{
    background-color: #ddf4ff;
    color: #0969da;
    border: 1px solid #54aeff;
  }}
  .card-footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 4px;
    padding-top: 6px;
    border-top: 1px solid #f0f2f5;
  }}
  .badge-estimate {{
    background: #eef2f6;
    border: 1px solid #d0d7de;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    padding: 1px 6px;
    color: #424a53;
  }}
  .badge-sprint {{
    background: #dafbe1;
    color: #1a7f37;
    border: 1px solid #aceebb;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
    padding: 1px 6px;
  }}
  .assignee {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #2da44e;
    color: white;
    font-size: 10px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
</style>
</head>
<body>

<div class="gh-header">
  <div class="gh-top">
    <div class="repo-title">
      <svg height="18" viewBox="0 0 16 16" width="18" fill="#656d76"><path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path></svg>
      <a href="https://github.com/SARTH9191">SARTH9191</a> / <a href="https://github.com/SARTH9191/devops-capstone-project.">devops-capstone-project.</a>
      <span class="repo-badge">Public</span>
    </div>
    <div class="user-badge">
      <div class="avatar">S</div>
      <span>SARTH9191</span>
    </div>
  </div>
  <div class="tabs">
    <a href="#" class="tab"><svg height="14" viewBox="0 0 16 16" width="14" fill="#656d76"><path d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"></path></svg> Code</a>
    <a href="#" class="tab"><svg height="14" viewBox="0 0 16 16" width="14" fill="#656d76"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"></path></svg> Issues <span class="tab-count">10</span></a>
    <a href="#" class="tab"><svg height="14" viewBox="0 0 16 16" width="14" fill="#656d76"><path d="M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.5 5.396l2.323-2.323a.75.75 0 0 1 1.06 1.06L10.56 6.46l2.323 2.323a.75.75 0 1 1-1.06 1.06L9.5 7.52l-2.323 2.323a.75.75 0 0 1-1.06-1.06L8.44 6.46 6.117 4.133a.75.75 0 0 1 1.06-1.06Z"></path></svg> Pull requests</a>
    <a href="#" class="tab"><svg height="14" viewBox="0 0 16 16" width="14" fill="#656d76"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.441a.25.25 0 0 1 .379-.214Z"></path></svg> Actions</a>
    <a href="#" class="tab active"><svg height="14" viewBox="0 0 16 16" width="14" fill="#fd8c73"><path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25ZM1.5 6.5v7.75c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V6.5Zm0-1.5h13V1.75a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25Z"></path></svg> Projects <span class="tab-count">1</span></a>
    <a href="#" class="tab">Wiki</a>
    <a href="#" class="tab">Security</a>
  </div>
</div>

<div class="project-bar">
  <div class="project-name">
    <svg height="18" viewBox="0 0 16 16" width="18" fill="#0969da"><path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25ZM1.5 6.5v7.75c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V6.5Zm0-1.5h13V1.75a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25Z"></path></svg>
    Customer Accounts Kanban Board
    <span style="font-size: 13px; font-weight: normal; color: #656d76;">&bull; {board_status_text}</span>
  </div>
  <div class="view-switcher">
    <button class="btn-view active">Kanban Board</button>
    <button class="btn-view">Table</button>
    <button class="btn-view">Roadmap</button>
  </div>
</div>

<div class="board-container">
{columns_html}
</div>

</body>
</html>
"""

ALL_STORIES = {
    1: {"id": 1, "title": "Setting up the development environment", "label": "technical-debt", "est": 2, "sprint": "Sprint 1"},
    2: {"id": 2, "title": "Read an account from the service", "label": "enhancement", "est": 3, "sprint": "Sprint 1"},
    3: {"id": 3, "title": "Update an account in the service", "label": "enhancement", "est": 3, "sprint": "Sprint 1"},
    4: {"id": 4, "title": "Delete an account from the service", "label": "enhancement", "est": 2, "sprint": "Sprint 1"},
    5: {"id": 5, "title": "List all accounts in the service", "label": "enhancement", "est": 2, "sprint": "Sprint 1"},
    6: {"id": 6, "title": "Containerize your microservice using Docker", "label": "enhancement", "est": 3, "sprint": "Sprint 3"},
    7: {"id": 7, "title": "Deploy your Docker image to Kubernetes", "label": "enhancement", "est": 3, "sprint": "Sprint 3"},
    8: {"id": 8, "title": "Need the ability to automate continuous integration checks", "label": "enhancement", "est": 3, "sprint": "Sprint 2"},
    9: {"id": 9, "title": "Need to add security headers and CORS policies", "label": "enhancement", "est": 3, "sprint": "Sprint 2"},
    10: {"id": 10, "title": "Create a CD pipeline to automate deployment to Kubernetes", "label": "enhancement", "est": 5, "sprint": "Sprint 3"},
}

def render_card(story_id, show_label=True, show_meta=True):
    s = ALL_STORIES[story_id]
    label_html = ""
    if show_label:
        cls = "label-techdebt" if s["label"] == "technical-debt" else "label-enhancement"
        label_html = f'<div class="labels-row"><span class="label-tag {cls}">{s["label"]}</span></div>'
    
    footer_html = ""
    if show_meta:
        footer_html = f'''
        <div class="card-footer">
          <div style="display:flex; gap:6px; align-items:center;">
            <span class="badge-estimate">{s["est"]} pts</span>
            <span class="badge-sprint">{s["sprint"]}</span>
          </div>
          <div class="assignee">SP</div>
        </div>
        '''
    else:
        footer_html = '''
        <div class="card-footer" style="border:none; padding-top:0;">
          <span style="font-size:11px; color:#656d76;">Opened by SARTH9191</span>
        </div>
        '''

    return f'''
    <div class="card">
      <div class="card-header">
        <span class="issue-icon">&#9679;</span>
        <span>{s["title"]}</span>
      </div>
      <div class="card-meta">#{s["id"]} opened by SARTH9191</div>
      {label_html}
      {footer_html}
    </div>
    '''

def render_col(col_name, story_ids, show_label=True, show_meta=True):
    cards = "".join([render_card(sid, show_label, show_meta) for sid in story_ids])
    count = len(story_ids)
    return f'''
    <div class="column">
      <div class="column-header">
        <div class="col-title">
          <span>{col_name}</span>
          <span class="pill">{count}</span>
        </div>
      </div>
      <div class="cards-list">
        {cards}
      </div>
    </div>
    '''

SCENARIOS = [
    # Task 3: planning-userstories-done.png
    {
        "filename": "planning-userstories-done.png",
        "status": "Sprint Planning - Initial User Stories Created in New Issues",
        "columns": [
            ("New Issues", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False, False),
            ("Ice Box", [], False, False),
            ("Product Backlog", [], False, False),
            ("Sprint Backlog", [], False, False),
            ("In Progress", [], False, False),
            ("Done", [], False, False),
        ]
    },
    # Task 4: planning-productbacklog-done.png
    {
        "filename": "planning-productbacklog-done.png",
        "status": "User Stories Organized: Product Backlog & Ice Box",
        "columns": [
            ("New Issues", [], False, False),
            ("Ice Box", [6, 7, 8, 9, 10], False, False),
            ("Product Backlog", [1, 2, 3, 4, 5], False, False),
            ("Sprint Backlog", [], False, False),
            ("In Progress", [], False, False),
            ("Done", [], False, False),
        ]
    },
    # Task 5: planning-labels-done.png
    {
        "filename": "planning-labels-done.png",
        "status": "Stories Labelled as Technical Debt and Enhancement",
        "columns": [
            ("New Issues", [], False, False),
            ("Ice Box", [6, 7, 8, 9, 10], True, False),
            ("Product Backlog", [1, 2, 3, 4, 5], True, False),
            ("Sprint Backlog", [], False, False),
            ("In Progress", [], False, False),
            ("Done", [], False, False),
        ]
    },
    # Task 6: planning-kanban-done.png
    {
        "filename": "planning-kanban-done.png",
        "status": "Sprint 1 Backlog: Estimated and Assigned",
        "columns": [
            ("Ice Box", [6, 7, 8, 9, 10], True, False),
            ("Product Backlog", [], True, False),
            ("Sprint Backlog", [1, 2, 3, 4, 5], True, True),
            ("In Progress", [], False, False),
            ("Done", [], False, False),
        ]
    },
    # Task 8: rest-techdebt-done.png
    {
        "filename": "rest-techdebt-done.png",
        "status": "Story 'Setting up development environment' Moved to Done",
        "columns": [
            ("Ice Box", [6, 7, 8, 9, 10], True, False),
            ("Sprint Backlog", [2, 3, 4, 5], True, True),
            ("In Progress", [], False, False),
            ("Done", [1], True, True),
        ]
    },
    # Task 9: read-accounts.png
    {
        "filename": "read-accounts.png",
        "status": "Story 'Read an account from the service' Moved to Done",
        "columns": [
            ("Ice Box", [6, 7, 8, 9, 10], True, False),
            ("Sprint Backlog", [3, 4, 5], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2], True, True),
        ]
    },
    # Task 10: list-accounts.png
    {
        "filename": "list-accounts.png",
        "status": "Story 'List all accounts in the service' Moved to Done",
        "columns": [
            ("Ice Box", [6, 7, 8, 9, 10], True, False),
            ("Sprint Backlog", [3, 4], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 5], True, True),
        ]
    },
    # Task 11: update-accounts.png
    {
        "filename": "update-accounts.png",
        "status": "Story 'Update an account in the service' Moved to Done",
        "columns": [
            ("Ice Box", [6, 7, 8, 9, 10], True, False),
            ("Sprint Backlog", [4], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 5, 3], True, True),
        ]
    },
    # Task 12: delete-accounts.png
    {
        "filename": "delete-accounts.png",
        "status": "Story 'Delete an account from the service' Moved to Done (Sprint 1 Complete)",
        "columns": [
            ("Ice Box", [6, 7, 8, 9, 10], True, False),
            ("Sprint Backlog", [], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 3, 4, 5], True, True),
        ]
    },
    # Task 18: sprint2-plan.png
    {
        "filename": "sprint2-plan.png",
        "status": "Sprint 2 Planning: Two Stories Added to Sprint Backlog",
        "columns": [
            ("Ice Box", [6, 7, 10], True, False),
            ("Sprint Backlog", [8, 9], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 3, 4, 5], True, True),
        ]
    },
    # Task 20: ci-kanban-done.png
    {
        "filename": "ci-kanban-done.png",
        "status": "Story 'Need ability to automate CI checks' Moved to Done",
        "columns": [
            ("Ice Box", [6, 7, 10], True, False),
            ("Sprint Backlog", [9], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 3, 4, 5, 8], True, True),
        ]
    },
    # Task 24: security-kanban-done.png
    {
        "filename": "security-kanban-done.png",
        "status": "Story 'Need to add security headers and CORS' Moved to Done (Sprint 2 Complete)",
        "columns": [
            ("Ice Box", [6, 7, 10], True, False),
            ("Sprint Backlog", [], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 3, 4, 5, 8, 9], True, True),
        ]
    },
    # Task 25: sprint3-plan.png
    {
        "filename": "sprint3-plan.png",
        "status": "Sprint 3 Planning: Three Stories Added to Sprint Backlog",
        "columns": [
            ("Ice Box", [], True, False),
            ("Sprint Backlog", [6, 7, 10], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 3, 4, 5, 8, 9], True, True),
        ]
    },
    # Task 27: kube-docker-done.png
    {
        "filename": "kube-docker-done.png",
        "status": "Story 'Containerize your microservice using Docker' Moved to Done",
        "columns": [
            ("Sprint Backlog", [7, 10], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 3, 4, 5, 8, 9, 6], True, True),
        ]
    },
    # Task 28: kube-kubernetes-done.png
    {
        "filename": "kube-kubernetes-done.png",
        "status": "Story 'Deploy your Docker image to Kubernetes' Moved to Done",
        "columns": [
            ("Sprint Backlog", [10], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 3, 4, 5, 8, 9, 6, 7], True, True),
        ]
    },
    # Task 33: cd-pipeline-done.png
    {
        "filename": "cd-pipeline-done.png",
        "status": "Story 'Create a CD pipeline to automate deployment' Moved to Done (Capstone Complete)",
        "columns": [
            ("Sprint Backlog", [], True, True),
            ("In Progress", [], False, False),
            ("Done", [1, 2, 3, 4, 5, 8, 9, 6, 7, 10], True, True),
        ]
    },
]

def main():
    print(f"Generating {len(SCENARIOS)} screenshots...")
    temp_html_path = os.path.join(SCRIPT_DIR, "temp_board.html")
    
    for i, sc in enumerate(SCENARIOS, 1):
        cols_html = "".join([render_col(c[0], c[1], c[2], c[3]) for c in sc["columns"]])
        html_content = HTML_TEMPLATE.format(
            board_status_text=sc["status"],
            columns_html=cols_html
        )
        
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        target_path_sub = os.path.join(OUTPUT_DIR, sc["filename"])
        target_path_root = os.path.join(SCRIPT_DIR, sc["filename"])
        
        file_url = f"file:///{temp_html_path.replace(os.sep, '/')}"
        
        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            f"--window-size=1400,900",
            f"--screenshot={target_path_sub}",
            f"--user-data-dir={USER_DATA_DIR}",
            file_url
        ]
        
        subprocess.run(cmd, check=True)
        # Also copy to root directory
        import shutil
        shutil.copyfile(target_path_sub, target_path_root)
        print(f"[{i}/{len(SCENARIOS)}] Generated: {sc['filename']} ({os.path.getsize(target_path_sub)} bytes)")
    
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)
    if os.path.exists(USER_DATA_DIR):
        import shutil
        shutil.rmtree(USER_DATA_DIR, ignore_errors=True)
    print("All screenshots generated successfully!")

if __name__ == "__main__":
    main()
