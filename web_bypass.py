#!/usr/bin/env python3
from flask import Flask, request, render_template_string, jsonify
import requests
import subprocess
import os
import time
from datetime import datetime

app = Flask(__name__)

API_URL = "https://api-bypass-phi.vercel.app/api/bypass"
API_KEY = "fqzzdx-phuocdz"
HISTORY_FILE = "url_list.txt"

# HTML template với giao diện hiện đại (Dark mode, responsive, animation)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Delta Bypass | Key Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            font-family: 'Segoe UI', 'Poppins', system-ui, -apple-system, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            max-width: 700px;
            width: 100%;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(12px);
            border-radius: 2rem;
            padding: 2rem;
            box-shadow: 0 25px 45px rgba(0,0,0,0.2), 0 0 0 1px rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        h1 {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #c084fc, #60a5fa);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .sub {
            text-align: center;
            color: #94a3b8;
            margin-bottom: 2rem;
            font-size: 0.9rem;
        }
        .input-group {
            margin-bottom: 1.5rem;
        }
        label {
            display: block;
            margin-bottom: 0.5rem;
            color: #cbd5e1;
            font-weight: 500;
            letter-spacing: 0.5px;
        }
        textarea {
            width: 100%;
            padding: 1rem;
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 1rem;
            color: #f1f5f9;
            font-family: monospace;
            font-size: 0.85rem;
            resize: vertical;
            transition: 0.2s;
        }
        textarea:focus {
            outline: none;
            border-color: #8b5cf6;
            box-shadow: 0 0 0 3px rgba(139,92,246,0.3);
        }
        button {
            background: linear-gradient(135deg, #8b5cf6, #3b82f6);
            border: none;
            padding: 0.9rem 1.5rem;
            width: 100%;
            border-radius: 2rem;
            font-weight: bold;
            font-size: 1rem;
            color: white;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 0.5rem;
        }
        button:hover {
            transform: scale(0.98);
            box-shadow: 0 10px 20px -5px rgba(139,92,246,0.5);
        }
        .result {
            margin-top: 2rem;
            background: rgba(0,0,0,0.4);
            border-radius: 1.5rem;
            padding: 1.2rem;
            border-left: 4px solid #8b5cf6;
        }
        .key-box {
            background: #0f172a;
            border-radius: 1rem;
            padding: 1rem;
            font-family: monospace;
            font-size: 1rem;
            word-break: break-all;
            color: #a5f3c3;
            margin: 1rem 0;
        }
        .copy-btn {
            background: #2dd4bf;
            background: linear-gradient(135deg, #14b8a6, #0d9488);
            width: auto;
            padding: 0.5rem 1.2rem;
            font-size: 0.85rem;
            display: inline-block;
            margin-top: 0.5rem;
        }
        .status {
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        .error {
            color: #f87171;
        }
        .success {
            color: #4ade80;
        }
        footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.7rem;
            color: #475569;
        }
        @media (max-width: 500px) {
            .container { padding: 1.5rem; }
            h1 { font-size: 1.6rem; }
        }
    </style>
</head>
<body>
<div class="container">
    <h1>🔓 Delta Bypass</h1>
    <div class="sub">Nhập URL cần bypass · Nhận key ngay lập tức</div>

    <div class="input-group">
        <label>📎 Link Receive Key (dài)</label>
        <textarea id="bypassUrl" rows="3" placeholder="https://auth.platorelay.com/a?d=..."></textarea>
    </div>

    <button id="bypassBtn">⚡ Bypass Now ⚡</button>

    <div id="resultArea" class="result" style="display: none;">
        <div><strong>🔑 Key đã tạo:</strong></div>
        <div id="keyDisplay" class="key-box"></div>
        <button id="copyKeyBtn" class="copy-btn">📋 Copy vào clipboard</button>
        <div id="statusMsg" class="status"></div>
    </div>
    <footer>Delta Bypass · hoạt động 24/7 trên localhost</footer>
</div>

<script>
    const bypassBtn = document.getElementById('bypassBtn');
    const resultArea = document.getElementById('resultArea');
    const keyDisplay = document.getElementById('keyDisplay');
    const copyBtn = document.getElementById('copyKeyBtn');
    const statusMsg = document.getElementById('statusMsg');

    bypassBtn.addEventListener('click', async () => {
        const url = document.getElementById('bypassUrl').value.trim();
        if (!url) {
            statusMsg.innerText = '❌ Vui lòng nhập URL!';
            statusMsg.className = 'status error';
            resultArea.style.display = 'block';
            return;
        }

        bypassBtn.disabled = true;
        bypassBtn.innerText = '🔄 Đang xử lý...';
        statusMsg.innerText = '';
        resultArea.style.display = 'block';
        keyDisplay.innerText = '⏳ Đang gọi API...';

        try {
            const response = await fetch('/api/bypass', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            });
            const data = await response.json();
            if (data.success) {
                keyDisplay.innerText = data.key;
                statusMsg.innerText = '✅ Bypass thành công! Key đã sẵn sàng.';
                statusMsg.className = 'status success';
            } else {
                keyDisplay.innerText = '⚠️ Lỗi: ' + (data.error || 'Không lấy được key');
                statusMsg.innerText = 'Thử lại sau vài giây...';
                statusMsg.className = 'status error';
            }
        } catch (err) {
            keyDisplay.innerText = '❌ Kết nối server thất bại';
            statusMsg.innerText = 'Kiểm tra lại server Termux';
            statusMsg.className = 'status error';
        } finally {
            bypassBtn.disabled = false;
            bypassBtn.innerText = '⚡ Bypass Now ⚡';
        }
    });

    copyBtn.addEventListener('click', () => {
        const keyText = keyDisplay.innerText;
        if (!keyText || keyText.includes('⏳') || keyText.includes('Lỗi')) {
            statusMsg.innerText = '⚠️ Không có key hợp lệ để copy';
            return;
        }
        // Sử dụng Clipboard API
        navigator.clipboard.writeText(keyText).then(() => {
            statusMsg.innerText = '📋 Đã copy key vào clipboard!';
            statusMsg.className = 'status success';
            setTimeout(() => {
                statusMsg.innerText = '';
            }, 2000);
        }).catch(() => {
            statusMsg.innerText = '❌ Copy thất bại, hãy tự copy thủ công';
        });
    });
</script>
</body>
</html>
"""

def try_get_key(target_url):
    """Thử nhiều phương thức với API thật"""
    # POST JSON {"key": url}
    try:
        r = requests.post(API_URL, json={"key": target_url}, timeout=10)
        if r.status_code == 200:
            return extract_key(r)
    except: pass
    # POST JSON {"bypass": url}
    try:
        r = requests.post(API_URL, json={"bypass": target_url}, timeout=10)
        if r.status_code == 200:
            return extract_key(r)
    except: pass
    # GET query
    try:
        r = requests.get(API_URL, params={"bypass": target_url}, timeout=10)
        if r.status_code == 200:
            return extract_key(r)
    except: pass
    return None

def extract_key(resp):
    try:
        data = resp.json()
        key = data.get("key") or data.get("result") or data.get("data") or data.get("token")
        if key:
            return key
        return resp.text.strip()
    except:
        return resp.text.strip()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/bypass', methods=['POST'])
def api_bypass():
    data = request.get_json()
    url = data.get('url', '').strip()
    if not url:
        return jsonify({"success": False, "error": "Missing url"}), 400
    
    # Lưu lại url để tiện theo dõi
    with open(HISTORY_FILE, 'a') as f:
        f.write(f"{datetime.now()} - {url}\n")
    
    key = try_get_key(url)
    if key:
        # Copy vào clipboard hệ thống (Termux)
        try:
            subprocess.run(['termux-clipboard-set', key], check=False, timeout=2)
        except:
            pass
        return jsonify({"success": True, "key": key})
    else:
        return jsonify({"success": False, "error": "API không trả về key hoặc link sai"}), 502

if __name__ == '__main__':
    print("🔧 Delta Bypass Web Server đang chạy tại http://localhost:6767")
    app.run(host='0.0.0.0', port=6767, debug=False, threaded=True)
