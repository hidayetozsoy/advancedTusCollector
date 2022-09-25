import sys, os
sys.path.append((os.path.dirname(__file__)))
from utils.config import *
from utils.consts import *
from utils.funcs import *

def main():
    global account
    try:
        for address in SIDE_ADDRESSES:
            balance = checkSwimmerBalance(address)
            if balance > FLOOR_TRANSFER_LIMIT_IN_SWIMMER_ACCOUNTS:
                transferAmount = balance - AMOUNT_LEFT_IN_SWIMMER_ACCOUNTS - SWIMMER_TRANSFER_PRICE
                printn(f"{int(transferAmount/pow(10,18))} TUS sent from {address} to {MAIN_ADDRESS}")
                sendSwimmerTx(address=address, to=MAIN_ADDRESS, value=int(transferAmount), sleepTime=0)

    except Exception as e:
        printn(e)
        
if __name__ == "__main__":
    main()