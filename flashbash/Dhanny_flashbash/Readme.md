# CHOICE FLASH LOAN

A flash loan script that swaps from an asset to another

## Setup and Installation

- Install the required dependencies

```sh
$ pip install -r requirements.txt
```

- Rename `env_copy` to `.env`. Don't forget to add the dot

```sh
$ mv .env_copy .env
```

- Add your Mnemonic phrase into the `mnemonic` key
  for example

```
mnemonic=add chef phrase
```

## Run the code

> On Mainnet: `IS_MAINET` in the script must be `True`

```sh
$ python run.py

Running...
Got your address as: UJUKMRPUJ2M44HRRDYYCZ6J2UN4XAZGNERY5BMWYOWYUYR3AZMJ7IQTM24
Checking if user is opted into asset: Algorand
User is opted into asset
Checking if user is opted into asset: Choice Coin
User is opted into asset
Querying balance on assets
#######################################################
You have a balance of 13885028 on asset: Algorand
You have a balance of 10466957 on asset: Choice Coin
#######################################################
Creating poool...
Created pool successfully
Swapping 2 Algorand to Choice Coin
Signing flash
Signed! Waiting for confirmation
Waiting for confirmation
Transaction ECBBPSUEPYTLL6JHFDZKPT77CFTTBV6TBMHFLB2PEAJLGJQSS3MA confirmed in round 20506181.
{'asset_id': 1,
 'creator': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ',
 'decimals': 6,
 'default_frozen': False,
 'freeze': None,
 'manager': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ',
 'name': 'Algorand',
 'reserve': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ',
 'total': 10000000000,
 'unit_name': 'ALGO',
 'url': 'https://www.algorand.com/'} 5
Flash loan completed successfully



Check transaction at https://algoexplorer.io/tx/ECBBPSUEPYTLL6JHFDZKPT77CFTTBV6TBMHFLB2PEAJLGJQSS3MA

```

> On testNet: `IS_MAINNET` in the script must be `False`

```sh
$ python run.py

Running...
Got your address as: UJUKMRPUJ2M44HRRDYYCZ6J2UN4XAZGNERY5BMWYOWYUYR3AZMJ7IQTM24
Checking if user is opted into asset: Algorand
User is opted into asset
Checking if user is opted into asset: USDC
User is opted into asset
Querying balance on assets
#######################################################
You have a balance of 8856911 on asset: Algorand
You have a balance of 9815201 on asset: USDC
#######################################################
Creating poool...
Created pool successfully
Swapping 0.2 Algorand to USDC
Signing flash
Signed! Waiting for confirmation
Waiting for confirmation
Transaction 2NMU4ZPCUV6VPS6Z45KWH2RJCF7KNNY5BUNA2J64SH66ORV2CQDQ confirmed in round 21076463.
{'asset_id': 1,
 'creator': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ',
 'decimals': 6,
 'default_frozen': False,
 'freeze': None,
 'manager': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ',
 'name': 'Algorand',
 'reserve': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ',
 'total': 10000000000,
 'unit_name': 'ALGO',
 'url': 'https://www.algorand.com/'} 5
Flash loan completed successfully



Check transaction at https://testnet.algoexplorer.io/tx/2NMU4ZPCUV6VPS6Z45KWH2RJCF7KNNY5BUNA2J64SH66ORV2CQDQ

```

- Here is the link to my transaction on [Algoexplorer](https://algoexplorer.io/tx/ECBBPSUEPYTLL6JHFDZKPT77CFTTBV6TBMHFLB2PEAJLGJQSS3MA)

- Here is the lint to my transactio on [Tesnet](https://testnet.algoexplorer.io/tx/2NMU4ZPCUV6VPS6Z45KWH2RJCF7KNNY5BUNA2J64SH66ORV2CQDQ)
