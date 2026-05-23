#!/bin/bash
# Delta Bypass Web Installer - Chạy 1 lần

set -e

echo "========================================="
echo "   Delta Key Bypass - Web Installer"
echo "========================================="

# Cập nhật & cài gói
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install python termux-clipboard-set git wget -y
pip install flask requests

# Tạo thư mục
mkdir -p ~/delta_web
cd ~/delta_web

# Tải web server (flask app)
wget -q -O web_bypass.py https://raw.githubusercontent.com/NXMC-samehwid/Public/refs/heads/main/web_bypass.py

# Tạo file lưu link (nếu chưa có)
[ -f url_list.txt ] || touch url_list.txt

# Tạo script khởi động nhanh
cat <<'EOF' > $PREFIX/bin/delta-bypass
#!/data/data/com.termux/files/usr/bin/bash
cd ~/delta_web
nohup python web_bypass.py > server.log 2>&1 &
sleep 2
termux-open-url http://localhost:6767
echo "✅ Delta Bypass Web đã chạy tại http://localhost:6767"
echo "📋 Nhấn Ctrl+C để xem log, dùng 'pkill -f web_bypass' để dừng"
EOF

chmod +x $PREFIX/bin/delta-bypass

# Tự động khởi động khi mở Termux (không bắt buộc)
if ! grep -q "delta-bypass" ~/.bashrc; then
    echo "delta-bypass" >> ~/.bashrc
fi

echo "========================================="
echo "✅ Cài đặt thành công!"
echo "🔧 Cách dùng:"
echo "   - Gõ 'delta-bypass' để chạy web server"
echo "   - Mở trình duyệt: http://localhost:6767"
echo "   - Dán link cần bypass, nhấn 'Bypass'"
echo "========================================="
