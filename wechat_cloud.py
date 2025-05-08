import itchat
import schedule
import time
from datetime import datetime
import os
import json
import sys
import requests

# 配置文件路径
CONFIG_FILE = 'wechat_config.json'

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_config(friend_name, send_time):
    """保存配置"""
    config = {
        'friend_name': friend_name,
        'send_time': send_time
    }
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def send_message(friend_name, message):
    """发送微信消息给指定好友"""
    try:
        friend = itchat.search_friends(name=friend_name)
        if friend:
            itchat.send(message, toUserName=friend[0]['UserName'])
            print(f"[{datetime.now()}] 消息已发送给 {friend_name}: {message}")
        else:
            print(f"[{datetime.now()}] 未找到好友: {friend_name}")
    except Exception as e:
        print(f"[{datetime.now()}] 发送消息失败: {str(e)}")

def format_time(time_str):
    """格式化时间字符串为HH:MM格式"""
    time_str = ''.join(c for c in time_str if c.isdigit() or c == ':' or c == '.')
    
    if '.' in time_str:
        hour, minute = time_str.split('.')
    elif ':' in time_str:
        hour, minute = time_str.split(':')
    else:
        hour, minute = time_str, '00'
    
    hour = hour.zfill(2)
    minute = str(minute).zfill(2)
    
    return f"{hour}:{minute}"

def main():
    # 登录微信
    print("正在登录微信，请扫描二维码...")
    # 禁用代理
    os.environ['no_proxy'] = '*'
    # 设置请求超时
    itchat.auto_login(
        hotReload=True,
        enableCmdQR=2,
        statusStorageDir='itchat.pkl',
        loginCallback=lambda: print("登录成功！"),
        exitCallback=lambda: print("已退出登录。")
    )
    
    # 加载或创建配置
    config = load_config()
    if config:
        friend_name = config['friend_name']
        send_time = config['send_time']
        print(f"已加载配置：好友 {friend_name}，发送时间 {send_time}")
    else:
        friend_name = input("请输入要发送消息的好友名称: ")
        time_input = input("请输入发送时间 (例如: 5.20 或 05:20): ")
        send_time = format_time(time_input)
        save_config(friend_name, send_time)
    
    # 设置定时任务
    schedule.every().day.at(send_time).do(send_message, friend_name, "I miss you")
    
    print(f"程序已启动，将在每天 {send_time} 发送消息给 {friend_name}")
    print("按 Ctrl+C 可以退出程序")
    
    # 保持程序运行
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 