import sys

blockchain = {'length': 1, 'chain': [{"blockID": 1, "transaction": "Genesis Block"}]}

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
    global blockchain
    incomplete = True
    while incomplete:
        print_green("\nplease enter new record")
        provider = input("\nenter provider: ")
        patient = input("\nenter patient name: ")
        reason = input("\nenter reason for visit: ")
        date = input("\nenter date: ")
        print_red("\nis this correct?\n")
        print_green("\nprovider: " + provider)
        print_green("\npatient: " + patient)
        print_green("\nreason: " + reason)
        print_green("\ndate: " + date)
        correct = input("\ny/n: ")
        if ( correct == "y"):
            incomplete = False
    blockchain['length'] += 1
    record = {"blockID": blockchain['length'], "transaction": {"provider": provider, "patient": patient, "reason": reason, "date": date}}
    blockchain['chain'].append(record)
    tid = str(blockchain['length'])
    print_blue("\nrecord has been added to the ledger\n")
    print_green("\nrecord and block ID: " + tid)


def getRecordsByName():
    global blockchain
    records=[]
    patient = input("\nenter the patient name: ")
    for block in blockchain['chain']:
        if block["blockID"] != 1:
            if block["transaction"]["patient"] == patient:
                records.append(block["transaction"])
    print_blue("\nrecords entered for " + patient + ":\n")
    print(records)

def getRecordsByProvider():
    global blockchain
    records=[]
    provider = input("\nenter the provider name: ")
    for block in blockchain['chain']:
        if block["blockID"] != 1:
            if block["transaction"]["provider"] == provider:
                records.append(block["transaction"])
    print_blue("\nrecords entered by " + provider + ":\n")
    print(records)

def getRecordByBlockID():
    global blockchain
    bid = 0
    while bid == 0:
        id = input("\nenter block or transaction ID number: ")
        try: 
            bid = int(id)
        except:
            print_red("\nplease enter an integer\n")
    if (bid > blockchain['length'] or bid <= 0):
        sid = str(bid)
        print_red("\n" + sid + " is not an existing block or transaction ID\n")
    else:
        print(blockchain['chain'][bid -1])

def printLedger():
    print_green("\ncurrent state of the ledger\n")
    print(blockchain)


def printHelp():
    print("""
    commands (case sensitive):

    help                    prints this menu
    addRecord               add a new record to the ledger
    getRecordsByName        prints records specific to a patient
    getRecordsByProvider    prints records made by a provider
    getRecordByBlockID      prints the record of a specific block
    printLedger             prints the entire ledger
    exit                    exits CLI
    """)

def main():

    switch = {  
                "addRecord":            addRecord,
                "getRecordsByName":     getRecordsByName,
                "getRecordsByProvider": getRecordsByProvider,
                "getRecordByBlockID":   getRecordByBlockID,
                "printLedger":          printLedger
            }
                
    print_blue("\n\n******DOMINOES MOCK CLI******\n")
    printHelp()
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
