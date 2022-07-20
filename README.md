# rAF2

Retrieve a set of phosphosite motifs (in graph format) based on a database of known phosphorylation sites and PDB codes. 

### Usage 

```
Usage: rprot [OPTIONS] PHOSPHOSITE STRUCTURES GRAPHS

Options:
  -r, --radius FLOAT            The threshold radius of the motif
  --rsa, --rsa-threshold FLOAT  The RSA threshold of the motif
  --help                        Show this message and exit.
```

### Example 

```
$ rprot ../datasets/human_known_serine.txt ../structures/human ../saved_graphs 
Downloading P35611 from AF2... DOWNLOADED.
Downloading P55212 from AF2... DOWNLOADED.
../structures/human/P18669.pdb already exists.
Downloading Q9Y237 from AF2... DOWNLOADED.
Downloading P10636-8 from AF2... FAILED.
Downloading P07900 from AF2... DOWNLOADED.
Downloading P21399 from AF2... DOWNLOADED.
Skipping non-uniprot ID 'ENSP00000357298'.
Downloading Q01954 from AF2... DOWNLOADED.
Downloading P46734 from AF2... DOWNLOADED.
Downloading P61224 from AF2... 

```


#### Some statistics are printed out at the end

```
$ rprot datasets/human_known_serine.txt structures/human/ saved_graphs/graphs-human-S-20A-0.2.txt\
--radius 20 --rsa 0.2
```

After loading ...

```
STATISTICS
----------
2155 phosphosites examined
52 graphs skipped
2101 graphs successfully constructed
2 graph constructions failed

Created 2103 graphs with threshold radius 20.0 A and RSA 0.2
Saving graphs to saved_graphs/graphs-human-S-known-all-20A-0.2.txt ... DONE.
$
```
