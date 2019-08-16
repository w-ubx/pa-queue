pragma solidity ^0.4.24;

contract Queue {

    address public issuer;
    bool public valid;

    string public user;
    uint public queue_id;
    uint public number;

    constructor(address _issuer, string _user, uint _queue_id,
        uint _number) public {
        issuer = _issuer;
        user = _user;
        queue_id = _queue_id;
        number = _number;
        valid = true;
    }

    modifier isIssuer() {
        require (msg.sender == issuer);
        _;
    }

    function revoke() external isIssuer {
        valid = false;
    }

    function user() public view returns (string) {
        return user;
    }

    function queue_id() public view returns (uint) {
        return queue_id;
    }

    function number() public view returns (uint) {
        return number;
    }

    function valid() public view returns (bool) {
        return valid;
    }
}