MAIN_ADDRESS = "0xf6463F3C5E2DCe879eE61E005A0Ad15601838A84" #main address, all the TUS will be sent to this address

SIDE_ADDRESSES = [ # side addresses that TUS will be sent from, !!! do not include your main address !!!
	"0x82A323000D50CABaEd045A71FDE88e01a8b082d8",
	"0x4043D2508C591f57C1C0d36CF227be5a3ace83d4",
]

PRIVATE_KEYS = { # address : private key (private keys of all addresses, including main address.)
    "0x82A323000D50CABaEd045A71FDE88e01a8b082d8":"58995c0f29e038d54d94868b8592edc1cbe88f076e24aa91b1a54b5d463317df",
    "0x4043D2508C591f57C1C0d36CF227be5a3ace83d4":"686e075ee398432d1ea14f9acabd93e695f77404bc51d800dab3c0c1aa02fe14",
}

SLIPPAGE = 1 # TUS to AVAX slippage

BINANCE_AVAX_C_ADDRESS = "" # binance avax c chain address that AVAX will be sent 

AMOUNT_LEFT_IN_SWIMMER_ACCOUNTS = 150 * pow(10,18) #amount of TUS that will be left at the address to maintain the game.
FLOOR_TRANSFER_LIMIT_IN_SWIMMER_ACCOUNTS = 300 * pow(10,18) #floor limit for transfer. if the amount is less than floor limit, transfer will not be executed.
SWIMMER_TRANSFER_PRICE = 0.21 * pow(10,18)

AMOUNT_LEFT_IN_AVAX_NETWORK = 0.1 * pow(10,18) #amount of AVAX that will be left at main address in AVAX NETWORK.
