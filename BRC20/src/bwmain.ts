import { BRC20 } from './brc-20';
import bitcoin from 'bitcoinjs-lib';

// Initialize your connection to the blockchain here
let network = bitcoin.networks.bitcoin; // for mainnet

// Create an instance of the BRC20 token
let BothWorldsToken = new BRC20('BothWorlds', 'BWT', network);