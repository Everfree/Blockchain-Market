/* blockchain-market is an experiment in creating a private blockchain and
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

# This file contains the contract's Solidity code
*/

pragma solidity 0.5.0;


contract SaleListing {


    address public owner;
    string private fileAddr;
    uint public price;
    uint public quantitySold;
    string public description;

    constructor(string memory _fileAddr, uint _price, string memory _description) public {
        owner = msg.sender;
        fileAddr = _fileAddr;
        price = _price;
        description = _description;
        quantitySold = 0;
    }

    function purchase() public payable returns (string memory) {
        require(msg.value >= price,
        "You must pay an amount equal to or greater than the current price in ETH to purchase.");

        if (msg.value > price) {
            price = msg.value;
        }
        quantitySold += 1;

        return fileAddr;
    }

    function getPrice() public view returns (uint) {
        return price;
    }

    function describe() public view returns (string memory) {
        return description;
    }

    function timesBought() public view returns (uint) {
        return quantitySold;
    }

    function getBalance() public view returns (uint) {
        require(msg.sender == owner, "Only the owner may check this contract's balance.");
        return address(this).balance;
    }

    function transferETH(uint amount) public {
        require(msg.sender == owner, "Only the owner may transfer funds.");
        require(amount <= address(this).balance, "The requested amount exceeds available funds.");
        address(msg.sender).transfer(amount);
    }

    function updatePrice(uint newPrice) public {
        require(msg.sender == owner, "Only the owner may update the price.");
        require(quantitySold == 0, "Can only change price if there are 0 sales");
        price = newPrice;
    }

    function takeOffMarket() public {
        require(msg.sender == owner, "Only the owner may take the listing off the market.");
        selfdestruct(address(uint160(owner)));
    }

}
