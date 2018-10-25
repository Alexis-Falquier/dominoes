import sys
import json
import requests

chain = []

def print_green(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

def print_red(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\x1b[91m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

def print_blue(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\x1b[94m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))

def addRecord():
    incomplete = True
    while incomplete:
        print_green("\nplease enter new record")
        provider = input("\nenter provider: ")
        providerID = input("\nenter provider ID: ")
        patient = input("\nenter patient full name: ")
        patientID = input("\nenter patient ID: ")
        reason = input("\nenter description of record event: ")
        date = input("\nenter date: ")
        print_red("\nis this correct?\n")
        print_green("\nprovider: " + provider)
        print_green("\nprovider ID: " + providerID)
        print_green("\npatient: " + patient)
        print_green("\npatient ID: " + patientID)
        print_green("\nreason: " + reason)
        print_green("\ndate: " + date)
        correct = input("\ny/n: ")
        if ( correct == "y"):
            incomplete = False
    
    url = 'http://18.218.143.83:5000/newrecord'
    payload = {
        "provider": provider,
        "providerID": providerID,
        "patient": patient,
        "patientID": patientID,
        "description": reason,
        "date": date
    }
    headers = {'content-type': 'application/json'}
    
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    updateChain()

    print_blue("\nrecord has been added to the ledger")
    print_green("\nrecord and block ID: " + str(len(chain) - 1))
    
def updateChain():
    global chain
    get_chain = requests.get("http://18.218.143.83:5000/verifiedchain").content.decode('utf-8')
    get_chain = json.loads(get_chain)
    updated_chain = get_chain["dominoes_chain"]
    if (len(chain) < len(updated_chain)):
        chain = updated_chain

def getRecordsByPatientName():
    updateChain()
    records=[]
    patient = input("\nenter the patient name: ")
    for block in chain:
        if block["blockID"] != 0:
            if block["data"]["patient"] == patient:
                records.append(block["data"])
    print_blue("\nrecords entered for " + patient + ":\n")
    for record in records:
        print(record)

def getRecordsByPatientID():
    updateChain()
    records=[]
    patient = input("\nenter the patient ID: ")
    for block in chain:
        if block["blockID"] != 0:
            if block["data"]["patientID"] == patient:
                records.append(block["data"])
    print_blue("\nrecords entered for patient of ID " + patient + ":\n")
    for record in records:
        print(record)

def getRecordsByProvider():
    updateChain()
    records=[]
    provider = input("\nenter the provider name: ")
    for block in chain:
        if block["blockID"] != 0:
            if block["data"]["provider"] == provider:
                records.append(block["data"])
    print_blue("\nrecords entered by " + provider + ":\n")
    for record in records:
        print(record)

def getRecordsByProviderID():
    updateChain()
    records=[]
    provider = input("\nenter the provider ID: ")
    for block in chain:
        if block["blockID"] != 0:
            if block["data"]["providerID"] == provider:
                records.append(block["data"])
    print_blue("\nrecords entered by privder of ID " + provider + ":\n")
    for record in records:
        print(record)

def getRecordByBlockID():
    updateChain()
    bid = -1
    while bid < 0:
        id = input("\nenter block or transaction ID number (int > 0): ")
        try: 
            bid = int(id)
        except:
            print_red("\nplease enter an integer larger than 0\n")
    if (bid >= len(chain)):
        sid = str(bid)
        print_red("\n" + sid + " is not an existing block or transaction ID\n")
    elif (bid == 0):
        print_green("\nblock ID 0 belongd to the genesis block")
    else:
        print_blue("\nrecord ID " + str(bid) + ":\n")
        print(chain[bid]["data"])

def printLedger():
    updateChain()
    print_green("\ncurrent state of the ledger\n")
    for block in chain:
        print("\n" + str(block))


def printHelp():
    print("""
    commands (case sensitive):

    help                        prints this menu
    addRecord                   add a new record to the ledger
    getRecordsByPatientName     prints records specific to a patient
    getRecordsByPatientID       prints records specific to a patient ID
    getRecordsByProvider        prints records made by a provider
    getRecordsByProviderID      prints records made by a provider ID
    getRecordByBlockID          prints the record of a specific block
    printLedger                 prints the entire ledger
    exit                        exits CLI
    """)

def main():

    switch = {  
                "addRecord":                addRecord,
                "getRecordsByPatientName":  getRecordsByPatientName,
                "getRecordsByPatientID":    getRecordsByPatientID,
                "getRecordsByProvider":     getRecordsByProvider,
                "getRecordsByProviderID":   getRecordsByProviderID,
                "getRecordByBlockID":       getRecordByBlockID,
                "printLedger":              printLedger
            }
                
    print_blue("\n\n******DOMINOES PATIENT RECORD CLI******\n")
    printHelp()
    updateChain()
    print("\nenter command:\n")

    for cmd in sys.stdin:
        cmd = cmd.rstrip( '\n' )
        if (cmd == "exit"):
            print_green("\nexiting\n")
            break
        elif (cmd == "help"):
            printHelp()
        else:
            try: 
                switch[cmd]()
            except KeyError:
                print_red("\n'%s' is not a valid command\n" % cmd)
                printHelp()
        print("\nenter command:\n")

if __name__ == '__main__':
    main()