pragma solidity ^0.5.0;


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
        require(msg.value >= price, "You must pay an amount equal to or greater than the current price in ETH to purchase.");

        if (msg.value > price) {
            price = msg.value;
        }
        quantitySold += 1;

        return fileAddr;
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

}
