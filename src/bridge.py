import sys, os
sys.path.append((os.path.dirname(__file__)))
from utils.config import *
from utils.consts import *
from utils.funcs import *

def main():
    tusBalance = checkSwimmerBalance(MAIN_ADDRESS)
    fee = getCrosschainFee()
    bridgeAmount = tusBalance - fee - AMOUNT_LEFT_IN_SWIMMER_ACCOUNTS
    if bridgeAmount <= 0:
        raise Exception("insufficient balance")
    dataInput = getDataInput(int(bridgeAmount))
    value = int(bridgeAmount + fee)
    print("bridging...", f"value: {value}", f"bridge amount: {bridgeAmount}", sep="\n")
    sendSwimmerTx(address=MAIN_ADDRESS, to=LAYERZERO_BRIDGE_CONTRACT_ADDRESS, dataInput=dataInput, value=value)
    return bridgeAmount

if __name__ == "__main__":
    main()
    # print(getCrosschainFee())
