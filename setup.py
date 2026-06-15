#!/usr/bin/env python3
"""
Skills Python 环境安装脚本
用于创建统一的虚拟环境并安装依赖
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

# 配置
VENV_DIR = Path(__file__).parent / "venv"
REQUIREMENTS_FILE = Path(__file__).parent / "requirements.txt"


def run_command(cmd, cwd=None):
    """运行shell命令并返回结果"""
    print(f"[执行] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"[错误] {result.stderr}")
        return False, result.stderr
    print(f"[成功] {result.stdout}")
    return True, result.stdout


def setup_pip_config():
    """配置pip信任源（解决SSL证书问题）"""
    pip_dir = Path.home() / ".pip"
    pip_conf = pip_dir / "pip.conf"
    
    config_content = """[global]
trusted-host = pypi.org
               files.pythonhosted.org
               pypi.python.org
               pypi.tuna.tsinghua.edu.cn
               mirrors.aliyun.com
               pypi.douban.com
               mirrors.cloud.tencent.com
index-url = https://pypi.org/simple
"""
    
    # 检查是否已配置
    if pip_conf.exists():
        content = pip_conf.read_text()
        if "trusted-host" in content:
            print("[信息] pip信任源已配置")
            return True
    
    try:
        pip_dir.mkdir(exist_ok=True)
        pip_conf.write_text(config_content)
        print(f"[成功] pip信任源配置完成: {pip_conf}")
        return True
    except Exception as e:
        print(f"[警告] 配置pip信任源失败: {e}")
        return False


def create_venv():
    """创建虚拟环境"""
    if VENV_DIR.exists():
        print(f"[信息] 删除已存在的虚拟环境: {VENV_DIR}")
        import shutil
        shutil.rmtree(VENV_DIR)
    
    print(f"[信息] 创建虚拟环境: {VENV_DIR}")
    try:
        venv.create(VENV_DIR, with_pip=True)
        print("[成功] 虚拟环境创建完成")
        return True
    except Exception as e:
        print(f"[错误] 创建虚拟环境失败: {e}")
        return False


def get_python_executable():
    """获取虚拟环境中的Python可执行文件路径"""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    else:
        return VENV_DIR / "bin" / "python"


def get_pip_executable():
    """获取虚拟环境中的pip可执行文件路径"""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "pip.exe"
    else:
        return VENV_DIR / "bin" / "pip"


def install_requirements():
    """安装requirements.txt中的依赖"""
    if not REQUIREMENTS_FILE.exists():
        print(f"[错误] 找不到 {REQUIREMENTS_FILE}")
        return False
    
    pip = get_pip_executable()
    
    # 先升级pip
    print("[信息] 升级pip...")
    run_command([str(pip), "install", "--upgrade", 
                 "--index-url", "https://pypi.org/simple",
                 "--trusted-host", "pypi.org", 
                 "--trusted-host", "files.pythonhosted.org", "pip"])
    
    # 安装依赖
    print("[信息] 安装依赖包...")
    success, output = run_command([
        str(pip), "install", "-r", str(REQUIREMENTS_FILE),
        "--index-url", "https://pypi.org/simple",
        "--trusted-host", "pypi.org",
        "--trusted-host", "files.pythonhosted.org"
    ])
    
    if success:
        print("[成功] 所有依赖安装完成")
    else:
        print("[错误] 依赖安装失败")
    
    return success


def show_activation_command():
    """显示激活虚拟环境的命令"""
    print("\n" + "="*50)
    print("环境安装完成！")
    print("="*50)
    print("\n[macOS/Linux 激活命令]")
    print("  source venv/bin/activate")
    print("\n[Windows 激活命令]")
    print("  venv\\Scripts\\activate")
    print("\n[Python 路径]")
    print("  macOS/Linux: venv/bin/python")
    print("  Windows:     venv\\Scripts\\python.exe")
    print("="*50)


def main():
    """主函数"""
    print("="*50)
    print("Skills Python 环境安装工具")
    print("="*50)
    
    # 0. 配置pip信任源
    setup_pip_config()
    
    # 1. 创建虚拟环境
    if not create_venv():
        sys.exit(1)
    
    # 2. 安装依赖
    if not install_requirements():
        sys.exit(1)
    
    # 3. 显示激活命令
    show_activation_command()


if __name__ == "__main__":
    main()
