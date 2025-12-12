#!/usr/bin/env python3
"""
====================================================================================
 HEXT Text to ASCII Banner Generator
 Title: HEXT Editor - Text To ASCII Banner Script
 Version: 1.3.0
 Author: Rob Seaverns (K0NxT3D)
====================================================================================

 Description:
    HEXT is a lightweight Python3 Flask application that converts plain text
    into ASCII banners using the pyfiglet font library. It provides a local
    web interface with a dark "Sith hacker" aesthetic, live preview,
    selectable fonts, clipboard copy support, and downloadable output.

 Purpose:
    • Create large ASCII banner text for terminals, project headers, scripts,
      or branding.
    • Provide an easy UI for previewing hundreds of pyfiglet fonts instantly.
    • Offer a simple API endpoint for automation or programmatic use.

 Features:
    • Web UI powered by Flask (default port: 22800)
    • Live ASCII preview with instant font switching
    • Copy-to-clipboard and downloadable .txt banners
    • Over 400 pyfiglet fonts available
    • Automatic browser launch on start

------------------------------------------------------------------------------------
 Usage:
    Run the script:
        python3 hext.py

    Then open:
        http://127.0.0.1:22800/

    Render API endpoint:
        POST /render
        JSON: {"text": "<your text>", "font": "<font name>"}

------------------------------------------------------------------------------------
 Requirements:
    Python: 3.8+
    System: Linux / macOS / Windows
    Base Packages:
        • Flask
        • pyfiglet

 Install requirements:
        pip3 install flask pyfiglet

 Optional:
        • A modern web browser for UI access
        • Network port 22800 available

------------------------------------------------------------------------------------
 File Behavior:
    • On execution, HEXT starts a Flask server and opens a browser tab.
    • All fonts are discovered on startup for faster UI performance.
    • The terminal displays an ASCII "HEXT" header using the doom font.

------------------------------------------------------------------------------------
 Flask Application:
    Host: 0.0.0.0
    Port: 22800
    Main Endpoint: /
    Render Endpoint: /render

  Compile Binary (Linux - Python3)
    If pyinstaller does not attach pyfiglet the app will not work as a binary.

pyinstaller --onefile \ --add-data "$(python3 -c 'import pyfiglet, os; print(os.path.dirname(pyfiglet.__file__))')/fonts:pyfiglet/fonts" \ hext.py
====================================================================================
"""


import threading
import webbrowser
import time
from flask import Flask, request, jsonify, render_template_string, make_response
import pyfiglet

# App defaults
APP_PORT = 22800
APP_HOST = "0.0.0.0"

app = Flask(__name__)

# Gather fonts once at startup
FONTS = sorted(pyfiglet.FigletFont.getFonts())

# Generate HTML Template
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>HEXT Text to ASCII Banner Generator</title>
<style>
/* =========================
   Dark 'Sith hacker' aesthetic
   Block-format CSS
========================= */
:root {
    --bg: #070708;
    --panel: #0d0d0f;
    --muted: #8a8a8a;
    --accent: #990000;
    --gold: #c9a600;
    --mono: "Courier New", Courier, monospace;
}

html, body {
    height: 100%;
    margin: 0;
    background: radial-gradient(circle at 10% 10%, #08080a 0%, #000000 60%);
    color: #ddd;
    font-family: Inter, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
}

.wrap {
    max-width: 1200px;
    margin: 28px auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 18px;
}

header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.title {
    display: flex;
    flex-direction: column;
}

h1 {
    margin: 0;
    font-size: 20px;
    letter-spacing: 2px;
    color: var(--gold);
}

.sub {
    font-size: 12px;
    color: var(--muted);
    margin-top: 6px;
}

.card {
    background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));
    border: 1px solid rgba(153,0,0,0.12);
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.6);
}

.controls {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 10px;
}

label {
    font-size: 13px;
    color: var(--muted);
    margin-right: 6px;
}

input[type="text"] {
    min-width: 260px;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.04);
    background: #060606;
    color: #eee;
    font-family: var(--mono);
}

select {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.04);
    background: #070707;
    color: #eee;
    font-family: var(--mono);
    cursor: pointer;
    max-height: 200px;
    overflow-y: auto;
}

/* Option highlight */
option:hover,
option:checked {
    background: var(--bg);
    color: var(--gold);
}

button {
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid var(--accent);
    background: transparent;
    color: var(--gold);
    cursor: pointer;
    font-weight: 600;
}

.layout {
    display: flex;
    gap: 16px;
    align-items: flex-start;
}

.left {
    flex: 0 0 360px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.right {
    flex: 1;
    min-width: 0;
}

.preview {
    height: 420px;
    overflow: auto;
    background: #000000;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.02);
    font-family: var(--mono);
    white-space: pre;
    line-height: 1;
}

.footer {
    font-size: 12px;
    color: var(--muted);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 6px;
}

@media (max-width: 900px) {
    .layout {
        flex-direction: column;
    }

    .left {
        flex: unset;
        width: 100%;
    }

    .preview {
        height: 320px;
    }
}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="title">
      <h1>HEXT Text to ASCII Banner Generator</h1>
      <div class="sub">Version 1.3.0 — By: K0NxT3D</div>
    </div>
    <div style="text-align:right;color:var(--muted);font-size:13px;">
      Port: {{port}} &nbsp; • &nbsp; Python/Flask &nbsp; • &nbsp; pyfiglet fonts: {{fonts_count}}
    </div>
  </header>

  <div class="card">
    <div class="controls">
      <label for="text">Text</label>
      <input id="text" type="text" value="HEXT" placeholder="Enter text to convert" />
      <label for="font">Font</label>
      <select id="font">
        {% for f in fonts %}
          <option value="{{f}}">{{f}}</option>
        {% endfor %}
      </select>
      <button id="renderBtn">Render</button>
      <button id="copyBtn" title="Copy banner to clipboard">Copy</button>
      <button id="downloadBtn" title="Download banner as .txt">Download</button>
    </div>

    <div class="layout">
      <div class="right">
        <div class="preview card" id="preview" role="region" aria-live="polite">
          Loading preview...
        </div>
      </div>
    </div>

    <div class="footer">
      <div>HexT Editor • Text To ASCII Banner Script</div>
      <div style="color:var(--muted)">Tip: select a font to preview it instantly.</div>
    </div>
  </div>
</div>

<script>
const previewEl = document.getElementById('preview');
const textEl = document.getElementById('text');
const fontSelect = document.getElementById('font');
const renderBtn = document.getElementById('renderBtn');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');

async function renderBanner() {
  const text = textEl.value || 'HEXT';
  const font = fontSelect.value;
  try {
    const res = await fetch('/render', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({text, font})
    });
    if (!res.ok) {
      const t = await res.text();
      previewEl.textContent = 'Error rendering: ' + t;
      return;
    }
    const data = await res.json();
    previewEl.textContent = data.banner;
  } catch (err) {
    previewEl.textContent = 'Error: ' + err;
  }
}

renderBtn.addEventListener('click', e => { e.preventDefault(); renderBanner(); });
textEl.addEventListener('keydown', e => { if(e.key==='Enter') renderBanner(); });

copyBtn.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(previewEl.textContent);
    copyBtn.textContent = 'Copied';
    setTimeout(()=>copyBtn.textContent='Copy',1200);
  } catch(e) {
    copyBtn.textContent = 'Failed';
    setTimeout(()=>copyBtn.textContent='Copy',1200);
  }
});

downloadBtn.addEventListener('click', () => {
  const blob = new Blob([previewEl.textContent], {type:'text/plain;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = (textEl.value || 'hext') + '.txt';
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

fontSelect.addEventListener('change', renderBanner);
window.addEventListener('load', () => setTimeout(renderBanner, 150));
</script>
</body>
</html>
"""

# Generate main HTML document (Front End UI)
@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, fonts=FONTS, fonts_count=len(FONTS), port=APP_PORT)

# Render ASCII Output
@app.route("/render", methods=["POST"])
def render_banner():
    try:
        data = request.get_json(force=True)
        text = data.get("text", "") or ""
        font = data.get("font", "") or "standard"
        if len(text) > 300:
            return make_response("Text too long (max 300 chars)", 400)
        if font not in FONTS:
            return make_response("Font not available", 400)
        banner = pyfiglet.figlet_format(text, font=font)
        return jsonify({"banner": banner})
    except Exception as e:
        return make_response(str(e), 500)

# Open default browser
def open_browser_when_ready():
    time.sleep(1.1)
    url = f"http://127.0.0.1:{APP_PORT}/"
    try:
        webbrowser.open_new_tab(url)
    except Exception:
        pass

# Main
if __name__ == "__main__":
    threading.Thread(target=open_browser_when_ready, daemon=True).start()
    try:
        header = pyfiglet.figlet_format("HEXT", font="doom")
    except Exception:
        header = "HEXT\n"
    print(header)
    print(f"Starting HEXT on port {APP_PORT} — opening browser (if available)...")
    app.run(host=APP_HOST, port=APP_PORT, debug=False)

