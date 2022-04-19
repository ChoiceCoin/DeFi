# CHOICE COIN FLASH LOAN ON ALGOFI

On the processes implementing this script i encountered a lot of errors because the initial pool used had no liquidity so i hahde to change 
```
CONSTANT_PRODUCT_25BP_FEE
```
TO
```
CONSTANT_PRODUCT_75BP_FEE

```

## OUTPUT
```
AHAMUEFULEs-MacBook-Pro-2:DeFi-main ahamuefuleterence$  cd /Users/ahamuefuleterence/Downloads/DeFi-main ; /usr/bin/env /usr/local/bin/python /Users/ahamuefuleterence/.vscode/extensions/ms-python.python-2022.4.1/pythonFiles/lib/python/debugpy/launcher 59163 -- /Users/ahamuefuleterence/Downloads/DeFi-main/Tutorial/flash_loan.py 
Waiting for confirmation
Transaction M2NCLYP4YFGU2BQRX3N7HIJBD5SH7SKRLQNWNOIIRVIYXMFHMUQA confirmed in round 20492033.
{'asset_id': 297995609,
 'creator': 'FG7NNTZU2LMMD2RD3Q5P2T77MESNEU2XXSZKYXKE5TWMXIHTMPJTSCILTA',
 'decimals': 2,
 'default_frozen': False,
 'freeze': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ',
 'manager': 'FG7NNTZU2LMMD2RD3Q5P2T77MESNEU2XXSZKYXKE5TWMXIHTMPJTSCILTA',
 'name': 'Choice Coin',
 'reserve': 'FG7NNTZU2LMMD2RD3Q5P2T77MESNEU2XXSZKYXKE5TWMXIHTMPJTSCILTA',
 'total': 100000000000,
 'unit_name': 'Choice',
 'url': 'https://choice-coin.com/'} 2
Choice Flash Successful
```
THE TRANSACTION ID IS M2NCLYP4YFGU2BQRX3N7HIJBD5SH7SKRLQNWNOIIRVIYXMFHMUQA
On the algo explorer you would see that i made 100 choice from this trade all on my IDE and terminal.




## ACKNOLEDGEMENT
Thanks to my research and some help from the algofi dev discord I was able to complete this bash
Now we can exploit this arbitrage oppourtunity for our development .
Lets build great things
**THANK YOU**
