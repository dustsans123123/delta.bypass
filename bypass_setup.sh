#!/bin/bash
# Delta Bypass Web - Tự động khởi động cùng Termux

set -e

echo "====================================="
echo "  Delta Bypass Web - Cài đặt tự động"
echo "====================================="

# Cập nhật và cài gói cần thiết
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install python termux-clipboard-set wget -y
pip install flask requests

# Tạo thư mục làm việc
mkdir -p ~/delta_web
cd ~/delta_web

# Tải web server (nội dung bên dưới)
cat > web_bypass.py << 'EOF'
#!/usr/bin/env python3
from flask import Flask, request, render_template_string, jsonify
import requests
import subprocess
import os
from datetime import datetime

app = Flask(__name__)

API_URL = "https://api-bypass-phi.vercel.app/api/bypass"
API_KEY = "fqzzdx-phuocdz"

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delta Bypass | Key Generator</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:linear-gradient(135deg,#0f172a,#1e293b);font-family:system-ui;min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}
        .container{max-width:700px;width:100%;background:rgba(255,255,255,0.05);backdrop-filter:blur(12px);border-radius:2rem;padding:2rem;box-shadow:0 25px 45px rgba(0,0,0,0.2)}
        h1{font-size:2rem;background:linear-gradient(135deg,#c084fc,#60a5fa);-webkit-background-clip:text;background-clip:text;color:transparent;text-align:center}
        .sub{text-align:center;color:#94a3b8;margin-bottom:2rem}
        textarea{width:100%;padding:1rem;background:#0f172a;border:1px solid #334155;border-radius:1rem;color:#f1f5f9;font-family:monospace;margin:1rem 0}
        button{background:linear-gradient(135deg,#8b5cf6,#3b82f6);border:none;padding:0.9rem;width:100%;border-radius:2rem;font-weight:bold;color:white;cursor:pointer}
        .result{margin-top:2rem;background:rgba(0,0,0,0.4);border-radius:1.5rem;padding:1.2rem}
        .key-box{background:#0f172a;border-radius:1rem;padding:1rem;word-break:break-all;color:#a5f3c3;margin:1rem 0}
        .copy-btn{background:#2dd4bf;width:auto;padding:0.5rem 1.2rem;display:inline-block}
        .error{color:#f87171}
        .success{color:#4ade80}
    </style>
</head>
<body>
<div class="container">
    <h1>🔓 Delta Bypass</h1>
    <div class="sub">Nhập URL cần bypass → nhận key ngay</div>
    <textarea id="url" rows="3" placeholder="https://auth.xxx.com/a?d=..."></textarea>
    <button id="bypassBtn">⚡ Bypass Now</button>
    <div id="result" class="result" style="display:none">
        <strong>🔑 Key:</strong>
        <div id="key" class="key-box"></div>
        <button id="copyBtn" class="copy-btn">📋 Copy clipboard</button>
        <div id="msg" class="status"></div>
    </div>
</div>
<script>
    const btn=document.getElementById('bypassBtn');
    const resultDiv=document.getElementById('result');
    const keyDiv=document.getElementById('key');
    const msgDiv=document.getElementById('msg');
    btn.onclick=async()=>{
        const url=document.getElementById('url').value.trim();
        if(!url){msgDiv.innerText='❌ Nhập URL';msgDiv.className='error';resultDiv.style.display='block';return;}
        btn.disabled=true;btn.innerText='⏳ Đang xử lý...';
        resultDiv.style.display='block';keyDiv.innerText='⏳ Đang gọi API...';msgDiv.innerText='';
        try{
            const res=await fetch('/api/bypass',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url})});
            const data=await res.json();
            if(data.success){
                keyDiv.innerText=data.key;
                msgDiv.innerText='✅ Bypass thành công! Key đã sẵn sàng.';
                msgDiv.className='success';
            }else{
                keyDiv.innerText='⚠️ Lỗi: '+data.error;
                msgDiv.innerText='Thử lại sau.';
                msgDiv.className='error';
            }
        }catch(e){
            keyDiv.innerText='❌ Lỗi kết nối server';
            msgDiv.innerText='Kiểm tra lại Termux';
        }finally{
            btn.disabled=false;btn.innerText='⚡ Bypass Now';
        }
    };
    document.getElementById('copyBtn').onclick=async()=>{
        const k=keyDiv.innerText;
        if(!k||k.includes('⏳')||k.includes('Lỗi')){msgDiv.innerText='⚠️ Không có key hợp lệ';return;}
        try{await navigator.clipboard.writeText(k);msgDiv.innerText='📋 Đã copy key!';setTimeout(()=>msgDiv.innerText='',2000);}
        catch{msgDiv.innerText='❌ Copy thất bại, hãy copy thủ công';}
    };
</script>
</body>
</html>
'''

def try_get_key(url):
    for payload in [{"key":url},{"bypass":url}]:
        try:
            r = requests.post(API_URL, json=payload, timeout=10)
            if r.status_code==200:
                return extract(r)
        except: pass
    try:
        r = requests.get(API_URL, params={"bypass":url}, timeout=10)
        if r.status_code==200:
            return extract(r)
    except: pass
    return None

def extract(resp):
    try:
        data=resp.json()
        return data.get("key") or data.get("result") or data.get("data") or resp.text.strip()
    except:
        return resp.text.strip()

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/bypass', methods=['POST'])
def api_bypass():
    url = request.json.get('url','').strip()
    if not url:
        return jsonify({"success":False,"error":"Missing url"}),400
    key = try_get_key(url)
    if key:
        try:
            subprocess.run(['termux-clipboard-set', key], check=False, timeout=2)
        except: pass
        return jsonify({"success":True,"key":key})
    return jsonify({"success":False,"error":"API không trả về key"}),502

if __name__ == '__main__':
    print("✅ Delta Bypass Web Server đang chạy tại http://localhost:6767")
    app.run(host='0.0.0.0', port=6767, debug=False, threaded=True)
EOF

# Tạo script khởi động ngầm trong ~/.bashrc
if ! grep -q "delta_web_auto" ~/.bashrc; then
    cat >> ~/.bashrc << 'BASHRC'

# Delta Bypass tự động (chạy ngầm, đợi 2s)
if ! pgrep -f "web_bypass.py" > /dev/null; then
    (cd ~/delta_web && nohup python web_bypass.py > server.log 2>&1 &)
    sleep 2
    echo "✅ Delta Bypass Web đã khởi động tại http://localhost:6767"
fi
BASHRC
fi

echo "====================================="
echo "✅ Cài đặt hoàn tất!"
echo "🔁 Từ bây giờ, mỗi khi mở Termux:"
echo "   - Đợi 2-3 giây (server tự chạy)"
echo "   - Mở trình duyệt, vào http://localhost:6767"
echo "====================================="
