// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract ATestnetConsumer is ChainlinkClient, ConfirmedOwner {
  using Chainlink for Chainlink.Request;
    
 
  uint256 constant private ORACLE_PAYMENT = 1000000000000000000;
  uint256 public currentInflation;

  
  event RequestInflationFulfilled(
    bytes32 indexed requestId,
    uint256 indexed inflation
  );
  

  constructor() ConfirmedOwner(msg.sender){
    setPublicChainlinkToken();
  }
  
  
  function requestInflationMexico(address _oracle, string memory _jobId)
    public
    onlyOwner
  {
    Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(_jobId), address(this), this.fulfillInflation.selector);
    req.add("get", "https://bafybeiae7rqgeyd7w4todhplzjuvq5plch6w4lljwniacvikleztps3j2y.ipfs.dweb.link/inflation_cpi_prices_data.json");
    req.add("path", "inflation");
    req.addInt("times", 100);
    sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
  }
  
  function fulfillInflation(bytes32 _requestId, uint256 _inflation)
    public
    recordChainlinkFulfillment(_requestId)
  {
    emit RequestInflationFulfilled(_requestId, _inflation);
    currentInflation = _inflation;
  }
  

  function getChainlinkToken() public view returns (address) {
    return chainlinkTokenAddress();
  }

  function withdrawLink() public onlyOwner {
    LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
    require(link.transfer(msg.sender, link.balanceOf(address(this))), "Unable to transfer");
  }

  function cancelRequest(
    bytes32 _requestId,
    uint256 _payment,
    bytes4 _callbackFunctionId,
    uint256 _expiration
  )
    public
    onlyOwner
  {
    cancelChainlinkRequest(_requestId, _payment, _callbackFunctionId, _expiration);
  }

  function stringToBytes32(string memory source) private pure returns (bytes32 result) {
    bytes memory tempEmptyStringTest = bytes(source);
    if (tempEmptyStringTest.length == 0) {
      return 0x0;
    }

    assembly { // solhint-disable-line no-inline-assembly
      result := mload(add(source, 32))
    }
  }
}