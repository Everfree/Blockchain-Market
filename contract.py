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

# This file contains the contract's Solidity code and code to add it
# to the private blockchain

# imports
import json
from web3 import Web3
from solc import compile_standard


# compile the contract defined using Solidity
# Input:
#   - fn: the name of the json file containing the contract definition
# Returns: compiled Solidity code
def compile_contract(fn):

    code = ""

    with open(fn) as file:
        code = json.load(file)

        print(code)

    return compile_standard(code, allow_paths=
                            "/Users/tkrull/Documents/SourceTree/BoilerMakeVIII"
                            )


print(compile_contract("contract.json"))
