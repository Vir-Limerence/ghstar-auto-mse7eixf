#!/usr/bin/env python3
"""
CDP 反向代理 — 用已登录的 CDP Chrome 渲染需要登录的网站
启动后，访问 http://localhost:8800/?url=小红书帖子链接 即可无登录查看

用法:
  python3 cdp_proxy.py
  # 然后浏览器访问 http://localhost:8800/?url=https://www.xiaohongshu.com/explore/xxx
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess, json, urllib.parse, re

CDP = "http://127.0.0.1:3456"

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        url = params.get('url', [None])[0]
        
        if not url:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing ?url= parameter')
            return
        
        try:
            # 在 CDP Chrome 中打开
            r = subprocess.run(['curl', '-s', '--max-time', '10',
                f'{CDP}/new?url={url}'], capture_output=True, text=True, timeout=15)
            tab = json.loads(r.stdout).get('targetId')
            
            # 等待加载
            import time
            time.sleep(2)
            
            # 获取页面内容
            r2 = subprocess.run(['curl', '-s', '--max-time', '10', '-X', 'POST',
                f'{CDP}/eval?target={tab}', '-d', 'document.documentElement.outerHTML'],
                capture_output=True, text=True, timeout=15)
            html = json.loads(r2.stdout).get('value', '')
            
            # 渲染到 iframe
            proxy_html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
            <style>body{{margin:0;background:#fff}}iframe{{width:100%;height:100vh;border:none}}</style>
            </head><body><iframe srcdoc="{html.replace(chr(34), '&quot;').replace(chr(38)+'gt;', '&gt;').replace(chr(38)+'lt;', '&lt;')}"></iframe></body></html>'''
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(proxy_html.encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {e}'.encode())

if __name__ == '__main__':
    print('🔐 CDP 代理启动: http://localhost:8800')
    HTTPServer(('127.0.0.1', 8800), ProxyHandler).serve_forever()
