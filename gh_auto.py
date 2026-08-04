#!/usr/bin/env python3
"""
GitHub 全自动操作库 — 基于 Chrome Cookie SQLite
零人工，无需 Token，利用已登录 Chrome 的 Session Cookie

用法:
    from gh_auto import GitHub
    gh = GitHub()
    gh.create_repo("my-repo", desc="描述")
    gh.enable_pages("my-repo")
    token = gh.create_token("my-token", scopes=["repo"])
    user = gh.whoami()
"""
import sqlite3
import shutil
import urllib.request
import urllib.parse
import urllib.error
import json
import re
import os
import time
from pathlib import Path

# ─── Cookie 管理 ───────────────────────────────────────────

class ChromeCookies:
    """从 Chrome 的 SQLite Cookie 数据库提取 cookie（含 httpOnly）"""
    
    COOKIE_DB = Path.home() / "Library/Application Support/Google/Chrome/Default/Cookies"
    
    @classmethod
    def extract(cls, domains=('.github.com', 'github.com')):
        """提取指定域名的所有 cookie，返回 cookie header string"""
        if not cls.COOKIE_DB.exists():
            raise FileNotFoundError(f"Chrome Cookie DB 不存在: {cls.COOKIE_DB}")
        
        tmp = Path("/tmp/chrome-cookies-snapshot.db")
        shutil.copy2(cls.COOKIE_DB, tmp)
        
        try:
            conn = sqlite3.connect(str(tmp))
            conn.row_factory = sqlite3.Row
            
            placeholders = ','.join('?' * len(domains))
            rows = conn.execute(
                f"SELECT name, value FROM cookies WHERE host_key IN ({placeholders})",
                domains
            ).fetchall()
            
            cookie_str = "; ".join(f"{r['name']}={r['value']}" for r in rows)
            conn.close()
            return cookie_str
        finally:
            tmp.unlink(missing_ok=True)
    
    @classmethod
    def list_cookies(cls, domain='.github.com'):
        """列出某个域名的所有 cookie 名称"""
        tmp = Path("/tmp/chrome-cookies-snapshot.db")
        shutil.copy2(cls.COOKIE_DB, tmp)
        try:
            conn = sqlite3.connect(str(tmp))
            rows = conn.execute(
                "SELECT name, is_httponly FROM cookies WHERE host_key=?",
                (domain,)
            ).fetchall()
            conn.close()
            return [(r[0], bool(r[1])) for r in rows]
        finally:
            tmp.unlink(missing_ok=True)


# ─── GitHub 操作类 ──────────────────────────────────────────

class GitHub:
    """基于 Chrome Session Cookie 的 GitHub 全自动操作"""
    
    BASE = "https://github.com"
    API = "https://api.github.com"
    
    def __init__(self):
        self._cookie = None
        self._csrf = None
        self._session = None
    
    @property
    def cookie(self):
        if not self._cookie:
            self._cookie = ChromeCookies.extract()
        return self._cookie
    
    @property
    def session(self):
        """带 cookie 的 urllib opener"""
        if not self._session:
            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('Cookie', self.cookie),
                ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'),
                ('Accept', 'text/html,application/xhtml+xml'),
            ]
            self._session = opener
        return self._session
    
    @property
    def csrf(self):
        """获取 CSRF token（从 /new 页面抓取）"""
        if not self._csrf:
            resp = self.session.open(f"{self.BASE}/new", timeout=15)
            html = resp.read().decode()
            m = re.search(r'name="authenticity_token" value="([^"]+)"', html)
            if not m:
                raise RuntimeError("无法获取 CSRF token — 可能未登录")
            self._csrf = m.group(1)
        return self._csrf
    
    def _post_form(self, path, data, referer=None):
        """POST 表单到 GitHub（带 CSRF 和 cookie）"""
        data['authenticity_token'] = self.csrf
        encoded = urllib.parse.urlencode(data).encode()
        
        req = urllib.request.Request(
            f"{self.BASE}{path}",
            data=encoded,
            headers={
                'Cookie': self.cookie,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': self.BASE,
                'Referer': referer or f"{self.BASE}{path}",
                'Accept': 'text/html',
            }
        )
        return urllib.request.urlopen(req, timeout=20)
    
    # ── 仓库操作 ─────────────────────────────────────────
    
    def create_repo(self, name, description="", private=False, auto_init=True):
        """创建 GitHub 仓库"""
        print(f"📦 创建仓库: {name}")
        
        try:
            resp = self._post_form('/repositories', {
                'repository[name]': name,
                'repository[description]': description,
                'repository[visibility]': 'private' if private else 'public',
                'repository[auto_init]': '1' if auto_init else '0',
            }, referer=f"{self.BASE}/new")
            
            final_url = resp.geturl()
            if '/new' in final_url:
                # 检查错误
                body = resp.read().decode()
                err = re.search(r'<div[^>]*class="[^"]*error[^"]*"[^>]*>(.*?)</div>', body, re.DOTALL)
                if err:
                    msg = re.sub('<[^>]+>', '', err.group(1)).strip()
                    raise RuntimeError(f"创建失败: {msg[:200]}")
                raise RuntimeError("创建失败，可能名称已存在")
            
            repo_url = final_url.rstrip('/')
            print(f"  ✅ {repo_url}")
            self._csrf = None
            return repo_url
            
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode()[:500]
            except:
                body = "无法读取错误详情"
            raise RuntimeError(f"HTTP {e.code}: {body}")
        except Exception as e:
            raise RuntimeError(f"网络错误: {e}")
    
    def enable_pages(self, repo_name, branch="main", path="/"):
        """开启 GitHub Pages"""
        print(f"🌐 开启 Pages: {repo_name}")
        
        resp = self._post_form(
            f"/Vir-Limerence/{repo_name}/settings/pages",
            {
                'page[source][branch]': branch,
                'page[source][path]': path,
            },
            referer=f"{self.BASE}/Vir-Limerence/{repo_name}/settings/pages"
        )
        
        page_url = resp.geturl()
        if 'pages' in page_url:
            print(f"  ✅ Pages 已配置")
            print(f"  🔗 https://vir-limerence.github.io/{repo_name}/")
            return f"https://vir-limerence.github.io/{repo_name}/"
        raise RuntimeError("Pages 配置失败")
    
    def repo_exists(self, name):
        """检查仓库是否存在"""
        try:
            resp = self.session.open(f"{self.BASE}/Vir-Limerence/{name}", timeout=10)
            return resp.getcode() == 200
        except urllib.error.HTTPError:
            return False
    
    # ── Token 操作 ────────────────────────────────────────
    
    def create_token(self, note="hermes-auto", scopes=None, expiration=None):
        """创建 Personal Access Token（classic）"""
        if scopes is None:
            scopes = ["repo", "workflow"]
        
        print(f"🔑 创建 Token: {note}")
        print(f"   权限: {', '.join(scopes)}")
        
        # 先访问 token 创建页获取 CSRF
        resp = self.session.open(f"{self.BASE}/settings/tokens/new", timeout=15)
        html = resp.read().decode()
        m = re.search(r'name="authenticity_token" value="([^"]+)"', html)
        if not m:
            raise RuntimeError("无法获取 token 页面的 CSRF")
        token_csrf = m.group(1)
        
        # 构造请求
        data = {
            'authenticity_token': token_csrf,
            'oauth_application[description]': note,
        }
        for scope in scopes:
            data[f'oauth_application[scopes][]'] = scope
        
        encoded = urllib.parse.urlencode(data, doseq=True).encode()
        
        req = urllib.request.Request(
            f"{self.BASE}/settings/tokens",
            data=encoded,
            headers={
                'Cookie': self.cookie,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': self.BASE,
                'Referer': f"{self.BASE}/settings/tokens/new",
            }
        )
        
        try:
            resp = urllib.request.urlopen(req, timeout=20)
            html = resp.read().decode()
            
            # 提取生成的 token
            m = re.search(r'id="new-oauth-token"[^>]*value="([^"]+)"', html)
            if m:
                token = m.group(1)
                print(f"  ✅ Token: {token[:10]}...{token[-4:]}")
                return token
            
            # 可能到了 sudo 页面
            if 'sudo' in resp.geturl():
                raise RuntimeError("需要密码确认 — 请在浏览器中手动操作 github.com/settings/tokens/new")
            
            raise RuntimeError("未能提取 token")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP {e.code}")
    
    # ── 用户操作 ─────────────────────────────────────────
    
    def whoami(self):
        """获取当前登录用户"""
        resp = self.session.open(f"{self.BASE}/settings/profile", timeout=10)
        html = resp.read().decode()
        m = re.search(r'<title>([^<]+)</title>', html)
        if m:
            title = m.group(1)
            user = title.replace(' · GitHub', '').replace('Your profile', '').strip()
            return user
        return None
    
    # ── 一键部署 ─────────────────────────────────────────
    
    def deploy_static(self, repo_name, local_dir, entry_file="index.html"):
        """一键部署静态网站：创建仓库 → 推送 → 开 Pages"""
        import subprocess
        
        # 1. 创建仓库
        if not self.repo_exists(repo_name):
            url = self.create_repo(repo_name, description="自动部署")
        else:
            print(f"📦 仓库已存在: {repo_name}")
            url = f"{self.BASE}/Vir-Limerence/{repo_name}"
        
        # 2. Git push
        print(f"📤 推送代码...")
        cwd = Path(local_dir)
        subprocess.run(['git', '-C', str(cwd), 'remote', 'remove', 'origin'], 
                       capture_output=True)
        subprocess.run(['git', '-C', str(cwd), 'remote', 'add', 'origin',
                       f'git@github.com:Vir-Limerence/{repo_name}.git'],
                       capture_output=True)
        
        result = subprocess.run(['git', '-C', str(cwd), 'push', '-u', 'origin', 'main'],
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ⚠️ push 警告: {result.stderr[:200]}")
            # 尝试 force push
            subprocess.run(['git', '-C', str(cwd), 'push', '-f', 'origin', 'main'],
                         capture_output=True)
        
        # 3. 开 Pages
        site_url = self.enable_pages(repo_name)
        
        print(f"\n🎉 部署完成!")
        print(f"   📂 仓库: {url}")
        print(f"   🌐 网站: {site_url}{entry_file}")
        return site_url


# ─── CLI ────────────────────────────────────────────────────

if __name__ == '__main__':
    import sys
    
    gh = GitHub()
    
    if len(sys.argv) < 2:
        print("""用法:
  python3 gh_auto.py whoami              # 查看登录用户
  python3 gh_auto.py create <name>       # 创建仓库
  python3 gh_auto.py pages <name>        # 开启 Pages
  python3 gh_auto.py token [note]        # 生成 PAT
  python3 gh_auto.py deploy <name> <dir> # 一键部署静态站
""")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == 'whoami':
        user = gh.whoami()
        print(f"👤 {user}")
    
    elif cmd == 'create':
        name = sys.argv[2] if len(sys.argv) > 2 else input("仓库名: ")
        gh.create_repo(name)
    
    elif cmd == 'pages':
        name = sys.argv[2] if len(sys.argv) > 2 else input("仓库名: ")
        gh.enable_pages(name)
    
    elif cmd == 'token':
        note = sys.argv[2] if len(sys.argv) > 2 else "hermes-auto"
        token = gh.create_token(note)
        print(f"\n📋 GITHUB_TOKEN={token}")
    
    elif cmd == 'deploy':
        name = sys.argv[2] if len(sys.argv) > 2 else input("仓库名: ")
        d = sys.argv[3] if len(sys.argv) > 3 else '.'
        gh.deploy_static(name, d)
    
    else:
        print(f"未知命令: {cmd}")
