import requests
import json
import concurrent.futures

API_KEY = "a6a1b29d57ec42ad96504aab0375c0a5"  # Get from Tianqi console. 从控制台获取
API_SECRET = "cdb98e3698584fbababfccffb6790a3f"  # Get from Tianqi console. 从控制台获取
PROMPT = "import (\n    \"math\"\n)\n\nfunc has_close_elements(numbers []float64, threshold float64) bool {\n        for i := 0; i < len(numbers); i++ {\n        for j := i + 1; j < len(numbers); j++ {\n            var distance float64 = math.Abs(numbers[i] - numbers[j])\n            if distance < threshold {\n                return true\n            }\n        }\n    }\n    return false\n}"
SRC_LANG = "Go"
DST_LANG = "Python"
REQUEST_URL = "https://tianqi.aminer.cn/api/v2/"
API_ENDPOINT = "multilingual_code_translate"

headers = {'Content-Type': 'application/json'}
data = {
    "apikey": API_KEY,
    "apisecret": API_SECRET,
    "prompt": PROMPT,
    "src_lang": SRC_LANG,
    "dst_lang": DST_LANG
}

def send_request(url, request_data):
    response = requests.post(url, headers=headers, data=json.dumps(request_data))
    if response:
        return response.json()
    else:
        return None

def main():
    request_urls = [REQUEST_URL + API_ENDPOINT] * 5  # Specify the number of parallel requests
    request_data = [data] * 5  # Specify the request data for each request

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit requests
        futures = [executor.submit(send_request, url, req_data) for url, req_data in zip(request_urls, request_data)]

        # Process results as they become available
        for future in concurrent.futures.as_completed(futures):
            response = future.result()
            if response:
                print(response)
            else:
                print("Error occurred during the request")

if __name__ == '__main__':
    main()
