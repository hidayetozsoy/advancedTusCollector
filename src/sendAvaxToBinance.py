import sys, os
sys.path.append((os.path.dirname(__file__)))
from utils.config import *
from utils.funcs import *

def main(transferAmount):
    if BINANCE_AVAX_C_ADDRESS == "":
        raise Exception("Destination Binance address is empty. Process is stopped.")
    sendAvaxTx(address=MAIN_ADDRESS, to=BINANCE_AVAX_C_ADDRESS, value=transferAmount)

if __name__ == "__main__":
    main()