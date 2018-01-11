import argparse
import yaml
import json
import requests
import sys

parser = argparse.ArgumentParser(description="========== CI Client Tool ==========")

parser.add_argument('-y', '--yaml', help='Enter the name of the workflow file under the "conf" folder.')

args = parser.parse_args()

def printFailedMsg():
    print("\n=========== Task Failed ============")
    print("========= Please Check Log =========\n")
    return

def executeTask(payload):
    f = open(sys.path[0] + "/config.yml")
    x = yaml.load(f)
    urlAddress = "http://" + x['host'] + ":" + str(x['port'])
    headers = {"Content-Type": "application/json"}
    r = requests.post(urlAddress + "/trigger", headers=headers, data=payload)
    if r.status_code == 200:
        print("\n========== Server Connected ==========\n")
        authorization = r.text
        headers = {"Content-Type": "application/json", "Authorization": authorization}
        # init
        print("\n[    Loading......  ]\n")
        r = requests.post(urlAddress + "/steps/init", headers=headers, data=payload)
        print(r.text)
        if r.status_code == 200 and r.text[-1] == '0':
            # git_clone
            print("\n[    Loading......  ]\n")
            r = requests.post(urlAddress + "/steps/git_clone", headers=headers, data=payload)
            print(r.text)
            if r.status_code == 200 and r.text[-1] == '0':
                # install
                print("\n[    Loading......  ]\n")
                r = requests.post(urlAddress + "/steps/install", headers=headers, data=payload)
                print(r.text)
                if r.status_code == 200 and r.text[-1] == '0':
                    # unit_test
                    print("\n[    Loading......  ]\n")
                    r = requests.post(urlAddress + "/steps/unit_test", headers=headers, data=payload)
                    print(r.text)
                    if r.status_code == 200 and r.text[-1] == '0':
                        # assemble
                        print("\n[    Loading......  ]\n")
                        r = requests.post(urlAddress + "/steps/assemble", headers=headers, data=payload)
                        print(r.text)
                        if r.status_code == 200 and r.text[-1] == '0':
                            # upload
                            print("\n[    Loading......  ]\n")
                            r = requests.post(urlAddress + "/steps/upload", headers=headers, data=payload)
                            print(r.text)
                            if r.status_code == 200 and r.text[-1] == '0':
                                # send_email
                                print("\n[    Loading......  ]\n")
                                r = requests.post(urlAddress + "/finalize/send_email", headers=headers, data=payload)
                                print(r.text)
                                if r.status_code == 200 and r.text[-1] == '0':
                                    print("\n========== Task Complete ==========\n")
                                else:
                                    printFailedMsg()
                            else:
                                printFailedMsg()
                        else:
                            printFailedMsg()
                    else:
                        printFailedMsg()
                else:
                    printFailedMsg()
            else:
                printFailedMsg()
        else:
            printFailedMsg()
    else:
        print("\n========== Connect Failed ==========\n")
        print(r.status_code)
    return

if args.yaml is not None:
    f = open(args.yaml)
    x = yaml.load(f)
    payload = json.dumps(x)
    executeTask(payload)
    # print(payload)
else:
    tempDict = {}
    tempDict['projectType'] = raw_input("Input your [project type] \t: ")
    tempDict['repositoryName'] = raw_input("Input your [repository name] \t: ")
    tempDict['repositoryUrl'] = raw_input("Input your [repository url] \t: ")
    tempDict['targetBranch'] = raw_input("Input your [target branch] \t: ")
    tempDict['bundleId'] = raw_input("Input your [bundle id] \t\t: ")
    tempDict['firToken'] = raw_input("Input your [FIR token] \t\t: ")
    tempDict['changeLog'] = raw_input("Input your [change log] \t: ")
    tempDict['emailAddress'] = raw_input("Input your [email address] \t: ")
    payload = json.dumps(tempDict)
    executeTask(payload)
    # print(payload)
