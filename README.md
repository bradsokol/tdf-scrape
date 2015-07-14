TDF Scrape
==========

Since 1994, Erik T has run an [Internet Tour de France Game](http://ifarm.nl/tdf/)
where players put together
hypothetical cycling teams that are scored on the performance of real riders
in the Tour de France. Some friends and I have run a small, friendly pool 
for many years, using this game for scoring.

This small script makes it fast and easy to pull the results from the game site
for a list of players participating in your pool.

Requirements
------------

This script requires Python v3.4 and the `pip` utility to install additional
libraries.

Usage
-----

The list of players is read from a text file with each player's name on a separate
line. For example:

```
Erik TKS
```

With this file, all player's teams can be listed:

```
$ ./tdfscrape.py teams --year=2015

Name:    Erik TKS
Date:    20150705 23:51:28
Country: The Netherlands
E-mail:  erixxxxx@xxxxxxxx.nl
                            tot  3  4  5  6  7  8
 1. N. Quintana              15 15  .  .  .  .  .
 2. V. Nibali                14 14  .  .  .  .  .
 3. A. Contador               0  .  .  .  .  .  .
 4. T. van Garderen          24 12  .  .  .  . 12
 5. C. Froome                22 11  .  .  .  . 11
 6. A. Valverde              10  .  .  .  .  . 10
 7. R. Gesink                 0  .  .  .  .  .  .
 8. B. Mollema               16  8  .  .  .  .  8
 9. J. Rodriguez              7  7  .  .  .  .  .
10. L. ten Dam                0  .  .  .  .  .  .
11. T. Pinot                  0  .  .  .  .  .  .
12. R. Bardet                 0  .  .  .  .  .  .
13. J. Peraud                 0  .  .  .  .  .  .
14. R. Majka                  0  .  .  .  .  .  .
15. D. Teklehaimanot          0  .  .  .  .  .  .
Ranking: 303        Points: 108 67  0  0  0  0 41
               Percentiles:   6100  0  0  0  0 87

Found 1 participant.
```
Use the `stage` command to list results for a given stage:
```
$ ./tdfscrape.py stage --date=20150711
Name        Stage Rank    Stage Points    Pool Rank    Pool Behind
--------  ------------  --------------  -----------  -------------
Erik TKS            35              41            1              0
```

The 'Pool Rank' and 'Pool Behind' columns show the standing for your local pool i.e. 
all the players listed in the input file.

Similarly, use the `overall` command to see overall standings up to a given date:
```
$ ./tdfscrape.py overall --date=20150711
Name        Rank    Prev. Rank    Points    Behind    Pool Rank    Pool Behind
--------  ------  ------------  --------  --------  -----------  -------------
Erik TKS     303           311       108      -195            1              0
```

Run `tdfscrape.py --help` to see a list of all options.
