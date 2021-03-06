# blockchain-market is an experiment in creating a private blockchain and
# building a market on top of it.
# Copyright (C) 2021  Tim Krull tkrull@purdue.edu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This is the prject's main .py file

# imports
import secrets
import json
from os import getcwd
from web3 import Web3
from eth_account import Account
from solc import compile_standard

# constants
HEX_DIGITS = 32     # number of digits for random hex nums
MIN_ACCTS = 16      # minimum number of accounts to have active
START_BAL = 150     # amount to start accounts off with
THREADS = 8         # number of threads for miner to use

# global variables
commands = {}   # list of functions for commands
gNode = Web3(Web3.IPCProvider('~/Library/Ethereum/geth.ipc'))  # IPC Provider
sale_listing = None  # eventual holder for contract


# function to populate commands through use of decorator @command
# this will be used to access command functions
def command(c):
    commands[c.__name__] = c


# function for purchase commands.
# Inputs:
#   - the sender account
#   - the amount being sent to purchase
# Returns: The transaction receipt address
@command
def purchase(*args):
    print('Executing purchase transaction\n')
    set_default_account(int(args[0]))
    return sale_listing.functions.purchase.value(int(args[1]))().transact()


# function for get price commands.
# Inputs:
#   - the sender account
# Returns: The transaction receipt address
@command
def get_price(*args):
    print('Executing getPrice transaction\n')
    set_default_account(int(args[0]))
    return sale_listing.functions.getPrice().transact()


# function for describe commands.
# Inputs:
#   - the sender account
# Returns: The transaction receipt address
@command
def describe(*args):
    print('Executing describe transaction\n')
    set_default_account(int(args[0]))
    return sale_listing.functions.describe().transact()


# function for times bought commands.
# Inputs:
#   - the sender account
# Returns: The transaction receipt address
@command
def times_bought(*args):
    print('Executing timesBought transaction\n')
    set_default_account(int(args[0]))
    return sale_listing.functions.timesBought().transact()


# function for get balance commands.
# Inputs:
#   - the sender account
# Returns: The transaction receipt address
@command
def get_balance(*args):
    print('Executing getBalance transaction\n')
    set_default_account(int(args[0]))
    return sale_listing.functions.getBalance().transact()


# function for transfer ETH commands.
# Inputs:
#   - the sender account
#   - the amount being requested
# Returns: The transaction receipt address
@command
def transfer_eth(*args):
    print('Executing transferETH transaction\n')
    set_default_account(int(args[0]))
    return sale_listing.functions.transferETH(int(args[1])).transact()


# function for update price commands.
# Inputs:
#   - the sender account
#   - the new price
# Returns: The transaction receipt address
@command
def update_price(*args):
    print('Executing updatePrice transaction\n')
    set_default_account(int(args[0]))
    return sale_listing.functions.updatePrice(int(args[1])).transact()


# function for take off market commands.
# Inputs:
#   - the sender account
# Returns: The transaction receipt address
@command
def take_off_market(*args):
    print('Executing takeOffMarket transaction\n')
    set_default_account(int(args[0]))
    return sale_listing.functions.takeOffMarket().transact()


# function for take send ETH commands.
# Inputs:
#   - the sender account
#   - the reciever account
#   - the amount being sent
# Returns: The transaction receipt address
@command
def send(*args):
    print('Executing send transaction\n')
    return gNode.eth.sendTransaction({'to': int(args[1]),
                                      'from': int(args[0]),
                                      'value': int(args[2])})


# sets the default account to use for chain transactions
# Input:
#   - acct_index: the index of the account in X.eth.accounts to use
def set_default_account(acct_index):
    gNode.eth.defaultAccount = gNode.eth.accounts[acct_index]


# distribute ETH among accounts for transactions
def distribute_eth():
    # start the miner with preset number of threads
    gNode.geth.miner.start(THREADS)

    # while the default account's balance is less than START_BAL times
    # the number of accounts, mine ETH
    while(Web3.fromWei(gNode.eth.getBalance(gNode.eth.accounts[0]),
          'ether') < (len(gNode.eth.accounts) * START_BAL)):
        # do nothing until default account has enough to seed others
        continue

    # distribute ETH to other accounts
    for i in range(1, len(gNode.eth.accounts)):
        # initiaite send transaction
        th = gNode.eth.sendTransaction({'to': gNode.eth.accounts[i],
                                        'value': START_BAL})
        # wait for the transaction to complete
        gNode.eth.waitForTransactionReceipt(th)

    # stop the miner
    gNode.geth.miner.stop()


# simulates activity on the blockchain
def simulate():
    print('Entering simulate()\n')

    # distribute at least the minimum START_BAL to each account
    distribute_eth()

    # start miner with preset number of threads
    gNode.geth.miner.start(THREADS)

    # read in commands and execute them
    with open('commands.txt', 'r') as fin:
        for command in fin:
            command = command.strip().split(sep=',')
            print('current command line:')
            print(command)

            th = commands[command[0]](command[1:])
            tr = gNode.eth.waitForTransactionReceipt(th)
            print(gNode.eth.getTransactionReceipt(tr))

    # stop miner
    gNode.geth.miner.stop()


# creates dummy users and adds their accounts to the blockchain
# Inputs:
#   - start: int to start indexing users at
#   - num: number of accounts to generate
# Outputs: user keyfiles
def populate_users(start, num):
    # create some hex values to use to generate account keys/addresses
    ex_entropy = [str(secrets.token_hex(HEX_DIGITS)) for
                  i in range(start, num)]

    # create some identifiers for users' keyfiles
    usernames = ['user' + str(x) for x in range(start, num)]

    # generate [num] user accounts, encrypt them, then write them to a keyfile
    # to add them to the blockchain
    for usr in range(num):
        usr_acct = Account.create(ex_entropy[usr])
        encrypted = usr_acct.encrypt(password='password')
        fn = 'Blockchain/keystore/' + usernames[usr] + '-keyfile'
        with open(fn, 'w') as kf:
            kf.write(json.dumps(encrypted))


# compile the contract defined using Solidity
# Input:
#   - fn: the name of the json file containing the contract definition
# Returns: a contract object
def compile_contract(fn):
    code = ""

    # open the json file and read it in
    with open(fn, 'r') as file:
        code = json.load(file)

    # compile the Solidity code
    comp_sol = compile_standard(code,
                                allow_paths=getcwd())

    # get the SaleListing data
    sale_listing = comp_sol['contracts']['SaleListing.sol']['SaleListing']

    # get the bytecode for the compiled Solidity code
    bytecode = sale_listing['evm']['bytecode']['object']

    # get the bytecode for the compiled Solidity code
    abi = json.loads(sale_listing['metadata'])['output']['abi']

    # return the contract data
    return gNode.eth.contract(abi=abi, bytecode=bytecode)


# prints info about the current state of the chain
def print_info():
    # output if connected to the geth node
    print("Node Connected: " + str(gNode.isConnected()) + "\n")

    # print info on latest block
    print("Details of latest block:")
    print(json.dumps(json.loads(Web3.toJSON(gNode.eth.get_block('latest'))),
                     indent=4, sort_keys=True) + '\n')

    # print user addresses
    print("Current Account Addresses:")
    for acct in gNode.eth.accounts:
        output = 'address: ' + acct + '\tbalance:' + str(Web3.fromWei(
                                                        gNode.eth.getBalance(
                                                         gNode.eth.accounts[0]
                                                         ), 'ether'))
        print(output)
    # print a blank line
    print()


def main(*args, **kwargs):
    if (len(gNode.eth.accounts) < MIN_ACCTS):
        populate_users(len(gNode.eth.accounts), MIN_ACCTS)

    # set the first account as the default account
    set_default_account(0)

    for i in range(len(gNode.eth.accounts)):
        gNode.geth.personal.unlock_account(gNode.eth.accounts[i],
                                           'password', 0)

    # get the compiled contract
    contract = compile_contract('contract.json')

    # Submit the transaction that deploys the contract
    trans_hash = contract.constructor("testaddress", 5,
                                      "Test Description").transact()
    # start up miner with preset number of threads
    gNode.geth.miner.start(THREADS)

    # Wait for the transaction to be mined, and get the transaction receipt
    trans_receipt = gNode.eth.waitForTransactionReceipt(trans_hash)

    sale_listing = gNode.eth.contract(address=trans_receipt.contractAddress,
                                      abi=contract.abi)

    # call a contract function
    sale_listing.functions.describe().call()

    # stop the miner
    gNode.geth.miner.stop()

    simulate()
    print_info()


if __name__ == "__main__":
    main()
