import base64
import json
import os
import requests

env = json.loads(open("constants/env.json").read())

url = env["url"]
apiKey = env["X-API-Key"]
parentFolder = env["parentFolder"]


def upload(folder):
    """
    This uploads folder items to ipfs moralis
    """
    if not os.path.exists(parentFolder + "/" + folder):
        print("images folder does not exits, please make a folder 'images' and paste all images in that folder")
        print("creating file structure for you, paste files in the directories")
        os.system("mkdir " + parentFolder + "/" + folder)
    final_array = []
    print("Preparing to upload")
    file_list = os.listdir(parentFolder + "/" + folder)
    if len(file_list) == 0:
        return
    for i in file_list:
        with open(parentFolder + "/" + folder + "/" + str(i), "rb") as file:
            b64 = base64.b64encode(file.read())
            body = {"path": "NFT/" + str(i), "content": str(b64, "utf-8")}
            final_array.append(body)

    header = {"X-API-Key": apiKey,
              "Content-Type": "application/json; charset=utf-8", "Host": "deep-index.moralis.io",
              "Content-Length": str(len(json.dumps(body)))}

    print("Uploading: " + str(len(file_list)) + " " + folder)
    response_data = requests.post(url=url, headers=header, data=json.dumps(final_array))
    base_url = ""
    try:
        base_url = "/".join(response_data.json()[0]["path"].split("/")[:-1])
        print("BASE URL of " + folder + ": " + base_url, end="\n*******************************\n")
        print("Uploaded")
    except:
        print(response_data.json())
        exit()
    return base_url


def add_path_in_json(base_url):
    """
    This adds path in images meta-data json or create json if it does not eixts
    """
    print("Preparing meta data")
    file_list = os.listdir("data/images")
    for i in file_list:
        json_path = parentFolder + "/jsons/" + str(i.split(".")[0]) + ".json"
        temp_json = {}
        try:
            json_file = open(json_path, "r")
            temp_json = json.loads(json_file.read())
        except Exception as exc:
            print(exc)
        temp_json["image"] = base_url + "/" + i
        json_file = open(json_path, "w")
        json_file.write(json.dumps(temp_json))
        json_file.close()
    print("Meta data prepared", end="\n*******************************\n")


add_path_in_json(upload("images"))
upload("jsons")
