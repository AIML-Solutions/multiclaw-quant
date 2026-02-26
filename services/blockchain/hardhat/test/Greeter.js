const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Greeter", function () {
  it("stores and updates greeting", async function () {
    const Greeter = await ethers.getContractFactory("Greeter");
    const greeter = await Greeter.deploy("hello quant");
    await greeter.waitForDeployment();

    expect(await greeter.greet()).to.equal("hello quant");

    const tx = await greeter.setGreeting("new alpha");
    await tx.wait();

    expect(await greeter.greet()).to.equal("new alpha");
  });
});
