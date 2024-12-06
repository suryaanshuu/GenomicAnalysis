# MedLedger Analytix


## Introduction

## Installation Pre-requisites
The basic requirements to run the projects are node.js and npm. 

### Node modules

1. Open the project repo.
2. Run `npm i` to install all the dependencies.

### Ganache

1. [Ganache homepage](https://truffleframework.com/ganache) Download and install Ganache. 

### IPFS

1. [github page](https://github.com/ipfs/ipfs-desktop) of Download and install IPFS Desktop
2. For Reference - (https://docs.ipfs.eth.link/install/command-line/#official-distributions)

### Local server

1. Install Node lite-server by running the following command on your terminal `npm install -g lite-server`

### Metamask

1. Download Metamask as a browser extension.

## Running the App

### Configuration

#### 1. Ganache
  - Open Ganache and click on settings in the top right corner.
  - Under **Server** tab:
    - Set Hostname to 127.0.0.1
    - Set Port Number to 8545
    - Enable Automine
  - Under **Accounts & Keys** tab:
    - Enable Autogenerate HD Mnemonic

#### 2. IPFS
  - Open your terminal and run `ipfs init`
  - Then run 
    ```
    ipfs config --json API.HTTPHeaders.Access-Control-Allow-Origin "['*']"
    ipfs config --json API.HTTPHeaders.Access-Control-Allow-Credentials "['true']"
    ipfs config --json API.HTTPHeaders.Access-Control-Allow-Methods "['PUT', 'POST', 'GET']"
    ```

#### 3. Metamask
  - After installing Metamask, click on the metamask icon on your browser.
  - Click on __TRY IT NOW__ and set it up
  - Stop when Metamask asks you to create a new password.
  
### Smart Contract

1. Install Truffle using `npm install truffle -g`
2. Compile Contracts using `truffle compile`

#### 1. Starting your local development blockchain
  - Open Ganache.
  - Make sure to configure it the way mentioned above.
  
1. Open new Terminal and deploy contracts using `truffle migrate`
2. Copy deployed contract address to src/app.js 


```js
var agentContractAddress = '0x75E115394aacC7c6063E593B9292CB9417E4cbeC';
```

### Running the App

#### 1. Connecting Metamask to our local blockchain
  - Connect metamask to localhost:8485
  - Click on import account
  - Select any account from ganache and copy the private key to import account into metaMask

#### 2. Starting IPFS 
  - Start the IPFS Desktop Application
  
#### 3. Start a local server
  - Open a new terminal window and navigate to `/PROJECT_DIRECTORY/app/`.
  - Run `npm start`.
  - Open `localhost:3000` on your browser.
  - The dApp is up and running locally.

#### 4. Start the WEB APP Separately
  - Open the sub-dir named as WEB APP
  - Go to the app.py
  - Run `python app.py`
  - Open `localhost:5000` on your browser.
  - The web app is up and running locally.
  - It can also be directly accessed via the medledger as it is linked to it
