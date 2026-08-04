#!/usr/bin/env python3
"""全自动 gh auth login — 从 CDP Chrome 输入设备验证码"""
import subprocess, json, time, sys, re, signal

CDP = "http://127.0.0.1:3456"

def cdp_open(url):
    r = subprocess.run(['curl', '-s', '--max-time', '10', f'{CDP}/new?url={url}'],
                       capture_output=True, text=True)
    return json.loads(r.stdout).get('targetId')

def cdp_eval(target, js, retries=3):
    for i in range(retries):
        try:
            r = subprocess.run(['curl', '-s', '--max-time', '12', '-X', 'POST',
                f'{CDP}/eval?target={target}', '-d', js],
                capture_output=True, text=True, timeout=15)
            val = json.loads(r.stdout).get('value', '')
            if val and val != 'null':
                return val
            time.sleep(1)
        except: time.sleep(1)
    return ''

def cdp_navigate(target, url):
    subprocess.run(['curl', '-s', '--max-time', '10',
        f'{CDP}/navigate?target={target}&url={url}'], capture_output=True)

def main():
    print("🔐 全自动 gh auth login")
    
    # 1. 启动 gh auth login
    proc = subprocess.Popen(
        ['gh', 'auth', 'login', '--git-protocol', 'ssh', '--hostname', 'github.com', '--web'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    
    # 2. 等它输出验证码
    code = None
    deadline = time.time() + 30
    output = ''
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line: break
        output += line
        m = re.search(r'one-time code:\s*([A-Z0-9-]+)', output)
        if m:
            code = m.group(1)
            break
    
    if not code:
        print(f"❌ 未检测到验证码\n输出: {output}")
        proc.terminate()
        return
    
    print(f"📟 验证码: {code}")
    
    # 3. 在 CDP Chrome 里打开设备激活页
    target = cdp_open("https://github.com/login/device")
    if not target:
        print("❌ CDP 无法打开页面")
        proc.terminate()
        return
    
    print(f"📄 页面已打开, 等待加载...")
    time.sleep(4)
    
    # 4. 尝试多种方式填入验证码
    strategies = [
        # GitHub 设备激活页可能使用各种不同的输入框
        "var i=document.querySelector('input[type=text],input:not([type=hidden]):not([type=submit]),#otp,input[name=code]');if(i){i.value='%s';i.dispatchEvent(new Event('input',{bubbles:true}));'found'}else{'no-input'}",
        # 有些页面把输入框藏在 shadow DOM 里
        "var inputs=document.querySelectorAll('input');var found=false;inputs.forEach(i=>{if(i.type!=='hidden'&&i.type!=='submit'){i.value='%s';i.dispatchEvent(new Event('input',{bubbles:true}));found=true}});found?'found-'+inputs.length:'no'",
        # 直接设表单值
        "var f=document.querySelector('form');if(f){var i=f.querySelector('input:not([type=hidden])');if(i){i.value='%s';i.dispatchEvent(new Event('change',{bubbles:true}));'form-ok'}else{'no-input-in-form'}}else{'no-form'}",
        # 查找 React 控制的输入
        "var r=document.querySelector('#__next input, [data-test-selector]');if(r){r.value='%s';r.dispatchEvent(new Event('input',{bubbles:true}));'react-ok'}else{'no-react'}"
    ]
    
    filled = False
    for strat in strategies:
        s = strat % code
        result = cdp_eval(target, s)
        print(f"  尝试: {result[:50]}")
        if 'found' in result.lower() or 'ok' in result.lower():
            filled = True
            break
    
    # 5. 尝试提交
    if filled:
        time.sleep(0.5)
        # 各种提交方式
        submits = [
            "document.querySelector('form')?.submit()",
            "document.querySelector('button[type=submit],input[type=submit]')?.click()",
            "document.querySelector('.btn-primary,button')?.click()",
        ]
        for s in submits:
            cdp_eval(target, s)
            time.sleep(1)
        
        print("✅ 已尝试提交")
    
    # 6. 截图看状态
    subprocess.run(['curl', '-s', '--max-time', '10', 
        f'{CDP}/screenshot?target={target}&file=/tmp/gh-device-result.png'],
        capture_output=True)
    
    # 7. 等待 gh 认证完成
    print("⏳ 等待认证...")
    try:
        proc.wait(timeout=30)
        print(f"✅ gh auth login 完成 (exit={proc.returncode})")
    except subprocess.TimeoutExpired:
        proc.terminate()
        print("⏰ 超时, 终止")
    
    # 8. 验证
    r = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
    print(r.stdout[:200])

if __name__ == '__main__':
    main()
