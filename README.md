# Apprecio.Finance - Measuring Inflation Decentrally

## Quick setup

**Node address**: 0x141bf09f27B1d274ff18bbbbD00eAfd3828C0E0A (more info in the [Job's TOML](https://github.com/omarespejel/apprecio_decentralized_inflation/blob/main/chainlink/node_jobs/july_2021_mexico_inflation_rate.toml)).

**externalJobID**: 8bc862a3f7734550948a824ed4307769 (more info in the [Job's TOML](https://github.com/omarespejel/apprecio_decentralized_inflation/blob/main/chainlink/node_jobs/july_2021_mexico_inflation_rate.toml)).

To get the lastest inflation estimate using Apprecio.Finance please create a contract instance of [ChainlinkClient.sol](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/ChainlinkClient.sol) and add a request-fulfill pipeline (please review [Chainlink documentation](https://docs.chain.link/docs/architecture-request-model/)).

A good example on how to get the latest inflation rate can be found in the [ClientInflationCall.sol](https://github.com/omarespejel/apprecio_decentralized_inflation/blob/main/contracts/ClientInflationAsk.sol).


## Inspiration

Inspiration for [Apprecio.Finance](apprecio.finance) (AF) came from August 5, 2021, [1729 Newsletter](https://1729.com/inflation), sponsored by Bajali Srinivasan (@[balajis](https://twitter.com/balajis)):

> “Inflation is a [monetary phenomenon](https://onlinelibrary.wiley.com/doi/pdf/10.1002/9781119205814.app2), a function of money printing. But it is also in part a social phenomenon, a function of mass psychology. If enough of the right people believe that inflation is going to happen, it will. As such, when inflation is happening, there is often a push to _censor_ discussion of inflation itself, under the grounds that discussing the problem actually causes it in the first place. That is exactly what happened in [Argentina](https://qz.com/84838/argentines-are-now-allowed-to-know-the-real-rate-of-inflation-thanks-to-their-courts/) and [Venezuela](https://www.economist.com/the-americas/2015/04/04/maduros-muzzle) over the last decade […] And that is why the world needs a global, decentralized, censorship-resistant inflation dashboard.
> 
> Why do we need an inflation dashboard? Because trillions of dollars have been [printed](https://www.marketwatch.com/story/why-the-feds-balance-sheet-is-expected-to-top-9-trillion-after-it-starts-reducing-its-monthly-asset-purchases-11626135642) over the last year – and it's not just dollars. Many countries besides the US have been printing fiat like mad to fund the response to COVID. Figures that shocked and stunned ten years ago ([$787B](https://www.politico.com/story/2009/02/senate-passes-787-billion-stimulus-bill-018837) for the bailout!) no longer warrant a headline today, though they may well result in headlines tomorrow.
> 
> If inflation is a government-caused problem, we can't necessarily rely on government statistics like the [CPI](https://www.bls.gov/cpi/) to diagnose it or remediate it. Indeed, in places with high inflation, censorship and denial is the rule rather than the exception.”




## What it does
**AF is a decentralized inflation dashboard: it estimates inflation from various price sources and makes it available through a front-end and on-chain trough Chainlink.** 

Its main objective is to resist censorship and provide an alternative to centralized measures such as those that come from Central Banks and national statistical agencies. AF implements decentralization at three different times in its design. (1) The price data are obtained from more than 1,000 different sources (in the Mexican case), independent of the government, which prevents the failure or manipulation of any source from significantly affecting the inflation calculation. (2) Data is automatically stored off-chain using the Interplanetary File System (IPFS), for data to be distributed across multiple off-chain nodes, and Filecoin, for data permanence and availability at any moment. (3) Aggregate prices and inflation rate are stored on-chain, Kovan testnet for AF v0.2, using Chainlink. The last two steps would also allow the data to be cryptographically signed twice.

## How we built it

### AF Design

To achieve the highest possible resistance to censorship, AF implements decentralization at three different times in its design. The following figure captures them.

![Decentralization at three stages.](https://images.mirror-media.xyz/publication-images/OqhU4tdR0D8jkqIGYAIvk.png?height=3295&width=1428)

### Data Recollection

This step is crucial to maintain decentralization. If manipulation of the data source by a third party can significantly alter AF's inflation rate measurement, then the objective of censorship resistance would be compromised.

Thus, for the Mexican case, our first measure, the data are obtained from two different types of sources.

1.  **Small sellers.** Through the [Apprecio](https://apprecio.mx) web and mobile applications.
    
2.  **Medium and large sellers**. Through web scrapping of online stores.
    

### Data Recollection: Small vendors (tienditas, in Spanish)

AF is unique in that it takes advantage of a data source such as that from small vendors.

In Latin America, these sellers are frequent. **Around** [700](https://www.elfinanciero.com.mx/mundo-empresa/2021/11/18/hablemos-del-valor-de-las-tienditas-en-mexico-y-que-podemos-hacer-por-ellas/) **thousand _tienditas_ exist in Mexico and generate 1% of GDP**. **Not taking this data source into account would greatly skew the inflation estimate.** However, obtaining data from these sources is a grassroots activity. There is no database that tracks prices in these relevant units.

**We take advantage of the work of the Mexican [Apprecio](https://apprecio.mx) fintech with more than 8 thousand small vendors as clients** throughout the Mexican Republic. Among other financial and strategic services, Apprecio helps small suppliers to calculate the ideal prices for their products. To do this, they require units to charge the prices at which they offer their products. AF then uses these data to calculate inflation.

![Apprecio.mx homepage](https://images.mirror-media.xyz/publication-images/uOeqO6vxKHhDs_fHvFMlc.png?height=803&width=1666)

**This source is decentralized**. **The data, for November 2021, comes from at least 1,000 different units and the number is growing**. The fact that a unit does not report accurate data would not affect the general median price of the good and therefore any calculations made with the prices.

### Data Recollection: Medium to Big Vendors

**Prices from [Walmart](https://www.walmart.com.mx/), [La Comer](https://www.lacomer.com.mx/lacomer/), and [Soriana](https://www.soriana.com/supermercado.html) are included to further decentralize data sources**. AF scrapes their online stores. For Mexico, it is planned to include at least two additional sources: Costco and Sam's Club.

**These sources provide the assurance of the constant presence of at least one price during any period**. The main challenge comes from maintaining scrappers that can repeatedly beat the web pages. The [1729 Newsletter](https://1729.com/inflation) mentions **several issues related to reliance on scrappers for pricing data,** including dealing with automated countermeasures, maintaining the web crawler, and analyzing hard-to-determine units. AF met these problems successfully.



### Decentralized storage off-chain

For AF to be a successful tool for openly measuring inflation, it must be **available for audit (1) at any time and (2) as cheaply as possible**.

Storage has at least two requirements for AF:

1.  **Raw price data must be auditable**. Currently, raw data storage is done off-chain due to gas prices. Possibly, the next step would be for AF to move to an Ethereum L2 and be able to store raw data on the chain.
    
2.  **The data must be stored in a decentralized way**. A central server means the consolidation of control over the data. Even off the chain, due to point 1, this should be achieved.
    

**AF achieves both requirements by storing raw price data off-chain using** [IFPS](https://ipfs.io/)**.** The entire price data set is divided into smaller chunks, cryptographic hashed, and assigned a unique fingerprint called a [Content Identifier](https://proto.school/anatomy-of-a-cid) **(CID)**. The dataset would be stored on at least one node, a local server anywhere in the world. By using the CID, other nodes can request the data and will cache the data themselves locally. This would increase the decentralization of the data set off the chain.

**The data must always be online and available for direct request.**

> “While IPFS guarantees that any content on the network is discoverable, it doesn't guarantee that any content is persistently available. This is where [Filecoin](https://filecoin.io/) comes in […] a decentralized storage network in which storage providers rent their storage space to clients.” ([IPFS documentation](https://docs.ipfs.io/concepts/persistence/#pinning-services)).

AF uses **Filecoin so that price data is always available while maintaining its decentralization**. The dataset would be anchored in at least one node.

The [Web3.Storage](https://web3.storage/) solution enables AF **(1)** to automatically store the dataset in IPFS and back it up with Filecoin; and **(2)** replicate pricing data across a network of storage providers and verify its integrity.

This solution allows data to be persistent, available, and decentralized even off-chain. The next layer of decentralization will come from making the data available on-chain.

### On-Chain Storage and Availability

Raw off-chain **data of available sources are aggregated to obtain the median value of the prices for a determined period of time**, leading to a single price per item that must be taken into account in the inflation calculation. **AF calculates inflation off-chain** using the [CalculateInflation.py](http://CalculateInflation.py) function in AF's GitHub repository. The calculation is done off-chain to save gas. However, **the next step is to allow any user to request an on-chain calculation**.

**AF v0.2 uses [Chainlink](https://chain.link/) to bring off-chain data to the Kovan testnet.** The next step would be to run a node directly on the Ethereum Mainnet to add an additional layer of decentralization. Chainlink is a decentralized Oracle network that cryptographically signs and delivers data on-chain. **Currently, any user can request (1) the current inflation rate; and (2) the aggregate prices of each of the items in the inflation calculation.**



## What's next for Apprecio.Finance

Three main points appear on the AF roadmap:

1.  **Coverage extended to new countries.** The next would be the United States and Brazil. Requests from other economies are appreciated.
    
2.  **Possible migration to full on-chain storage.** With the development of new Ethereum L2 rollups like Starknet, it's cheaper than ever to chain data. This would allow users to request and integrate AF data into their smart contracts inexpensively.
    
3.  **Adding new data sources**. The more good quality data sources AF uses, the more decentralized and secure the inflation rate will be. In Mexico, AF is already implementing data from small suppliers (_tienditas_) and retailers.
