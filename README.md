# mtg-card-database

Creates/queries a database for storing an MTG collection. Stores set code, collector number, foil-ness, name, count, price, previous price, and price change since that card was last modified.

Operations include: adding cards, removing cards, updating card prices, searching cards, and exporting to csv

# Common usage examples

Add 4 foil of a card:\
mtgdb -af shm 211 4

Remove 2 non-foil of a card:\
mtgdb -r shm 211 2

Update prices for a foil card:\
mtgdb -uf shm 211

Update prices for all cards:\
mtgdb --update-all

Update prices for all cards and export to csv:\
mtgdb --update-all -c

Searching for a non-foil card:\
mtgdb -s shm 211
