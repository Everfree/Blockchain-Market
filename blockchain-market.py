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
START_BAL = 50      # amount to start accounts off with


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
        encrypted = usr_acct.encrypt(password=str(usernames[usr] + 'pass'))
        fn = 'Blockchain/keystore/' + usernames[usr] + '-keyfile'
        with open(fn, 'w') as kf:
            kf.write(json.dumps(encrypted))


# sets the default account to use for chain transactions
# Input:
#   - acct_index: the index of the account in X.eth.accounts to use
def set_default_account(acct_index):
    gNode.eth.defaultAccount = gNode.eth.accounts[acct_index]


# simulates activity on the blockchain
def simulate():
    gNode.geth.miner.start(4)

    seed_accounts = False
    for account in gNode.eth.accounts:
        if Web3.fromWei(gNode.eth.getBalance(account), 'ether') < START_BAL:
            seed_accounts = True
            break
    if seed_accounts:
        while(Web3.fromWei(gNode.eth.getBalance(gNode.eth.accounts[0]),
              'ether') < (len(gNode.eth.accounts) * START_BAL)):
            # do nothing until default account has enough to seed others
            continue

    gNode.geth.miner.stop()

    gNode.geth.personal.unlock_account(gNode.eth.accounts[0], 'user0pass', 0)

    # seed other accounts
    for i in range(1, len(gNode.eth.accounts)):
        gNode.eth.sendTransaction({'to': gNode.eth.accounts[i],
                                  'value': START_BAL})

    # with open('commands.txt', 'r') as fin:
    #     for command in fin:
    #         command = command.split()


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

    # get the bytecode for the compiled Solidity code
    bytecode = comp_sol['contracts']['SaleListing.sol']['SaleListing']['evm']['bytecode']['object']

    # get the bytecode for the compiled Solidity code
    abi = json.loads(comp_sol['contracts']['SaleListing.sol']['SaleListing']['metadata'])['output']['abi']

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


# IPC Provider
gNode = Web3(Web3.IPCProvider('/Users/tkrull/Library/Ethereum/geth.ipc'))

if (len(gNode.eth.accounts) < MIN_ACCTS):
    populate_users(len(gNode.eth.accounts), MIN_ACCTS)

# set the first account as the default account
set_default_account(0)

# get the compiled contract
SaleListing = compile_contract('contract.json')

# # Submit the transaction that deploys the contract
# trans_hash = SaleListing.constructor("testaddress", 5,
#                                      "Test Description").transact()
simulate()
print_info()
