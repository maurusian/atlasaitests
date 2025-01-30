from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json, requests, time

def read_token():
    with open("token.txt", "r") as tok:
        return tok.read().strip()

token_access = read_token()
headers = {"Authorization": f"Bearer {token_access}"}

API_URL = "https://api-inference.huggingface.co/models/atlasia/Terjman-Large-v2"

def query(payload, max_retries=5):
    start_time = time.time()
    retries = 0
    
    while retries < max_retries:
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        result = json.loads(response.content.decode("utf-8"))
        
        if "error" in result:
            error_message = result["error"]
            if "estimated_time" in result:
                wait_time = result["estimated_time"]
                print(f"Error encountered: {error_message}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
            else:
                print(f"Fatal error encountered: {error_message}. Exiting.")
                return result
        else:
            execution_time = time.time() - start_time
            print(f"Execution completed in {execution_time:.2f} seconds.")
            return result
    
    print("Max retries reached. Exiting.")
    return result


data = query(
    {
        #"inputs": "The neutron is a subatomic particle, symbol n, that has no electric charge, and a mass slightly greater than that of a proton.",
        #"inputs": "Artemisia absinthium, otherwise known as common wormwood, is a species of Artemisia native to North Africa and temperate regions of Eurasia, and widely naturalized in Canada and the northern United States.",
        #"inputs": "Association football, more commonly known as football or soccer,[a] is a team sport played between two teams of 11 players each, who almost exclusively use their feet to propel a ball around a rectangular field called a pitch.", 
        #"inputs": "Franklin Delano Roosevelt (January 30, 1882 – April 12, 1945), also known as FDR, was the 32nd president of the United States, serving from 1933 until his death in 1945.",
        #"inputs": "Gukesh Dommaraju (born 29 May 2006) is an Indian chess grandmaster and the reigning World Chess Champion. A chess prodigy, Gukesh is the youngest undisputed world champion, the youngest player to have surpassed a FIDE rating of 2750, doing so at the age of 17, and the third-youngest to have surpassed 2700 Elo at the age of 16. He earned the title of grandmaster at the age of 12 and is the third-youngest grandmaster in chess history.",
        "inputs": "Russian invasion of Ukraine",
    } 
)

print(data)
