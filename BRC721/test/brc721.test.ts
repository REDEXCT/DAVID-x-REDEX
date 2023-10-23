/* eslint-disable no-unused-expressions */
// eslint-disable-next-line import/no-extraneous-dependencies
import { expect } from 'chai'
import { Computer } from '@bitcoin-computer/lib'
import { NFT } from '../src/nft'
import { BRC721 } from '../src/brc721'

/**
 * To run the tests with the Bitcoin Computer testnet node remove the opts argument.
 */
const computer = new Computer({
  url: 'http://127.0.0.1:1031',
  network: 'regtest' as any,
})

before(async () => {
  // @ts-ignore
  await computer.faucet(1e7)
})

describe('BRC721', () => {
  describe('Constructor', () => {
    it('Should create a new BRC721 object', async () => {
      const nft = new NFT('to', 'name', 'symbol')
      expect(nft).not.to.be.undefined
      expect(nft).to.deep.eq({
        name: 'name',
        symbol: 'symbol',
        _owners: ['to'],
      })
    })
  })

  describe('mint', () => {
    it('Should mint tokens', async () => {
      const brc721 = new BRC721(computer)
      const publicKey = brc721.computer.getPublicKey()
      const rev = await brc721.mint(publicKey, 'name', 'symbol')
      expect(rev).not.to.be.undefined
      expect(typeof rev).to.eq('object')
    })
  })

  describe('balanceOf', () => {
    it('Should compute the balance', async () => {
      const brc721 = new BRC721(computer)
      const publicKey = computer.getPublicKey()
      brc721.mint(publicKey, 'name', 'symbol')
      expect(brc721).not.to.be.undefined
      const balance = await brc721.balanceOf(publicKey)
      expect(balance).to.be.greaterThanOrEqual(1)
    })
  })

  describe('transfer', () => {
    it('Should transfer a token', async () => {
      const computer2 = new Computer()
      const brc721 = new BRC721(computer)
      const publicKey = brc721.computer.getPublicKey()
      const token = await brc721.mint(publicKey, 'name', 'symbol')
      const publicKey2 = computer2.getPublicKey()
      await brc721.transfer(publicKey2, token._id)
      const res = await brc721.balanceOf(publicKey)
      expect(res).to.be.greaterThanOrEqual(1)
    })
  })
})
