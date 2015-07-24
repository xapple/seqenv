# seqenv version 1.0.3
Assign environment ontology (EnvO) terms to short DNA sequences. More information at: http://environments.hcmr.gr/seqenv.html

### Installing
To install `seqenv` onto your machine, use the python package manager:

    $ pip install seqenv

You might be installing this onto a computer server which you don't own and thus don't have sufficient privileges. In that case you can install everything in your home directory like this:

    $ pip install --user seqenv

If this still doesn't work, you might be missing the `pip` program on your system or the correct version of Python (any version `2.7.x`). You can get both of these things by using using this little project: https://github.com/yyuu/pyenv

### Dependencies
* You need to have a copy of the NCBI nucleotide data base (called `nt`) installed locally as well as the `blastn` executable in your `$PATH`. So that BLAST finds the NT database, you can edit your `~/.ncbirc` file.
* The project also depends on some other python modules such as `biopython`. Happily, these will be installed automatically when calling the `pip` command above.

### Optional dependencies
* To compile parts of the software you might need a copy of the BOOST libraries as well as the SWIG libraries.

### Usage
Once that is done, you can start processing FASTA files from the command line. For using the default parameters you can just type:

    $ seqenv sequences.fasta

We will then assume that you have inputed 16S sequences. To modify the database or input a different type of sequences:

    $ seqenv sequences.fasta --seqtype prot --db nr

To modify the minimum identity in the similarity search, use the following:

    $ seqenv sequences.fasta --min_identity 0.97

If you have abundance data you would like to add to your analysis you can specify it like this in a TSV file:

    $ seqenv sequences.fasta --abundances counts.tsv

### All parameters
Several other options are possible. Here is a list describing them all:

   * `--seq_type`: Sequence type `nucl` or `prot`, for nucleotides or amino acids respectively (Default: `nucl`).
   * `--search_algo`: Search algorithm. Either `blast` or `vsearch` (Default: `blast`).
   * `--search_db`: The database to search against (Default: `nt`). You can specify the full path or make a `~/.ncbirc` file.
   * `--backtracking`: For every term identified by the tagger, we will propagate frequency counts up the acyclic directed graph described by the ontology. Defaults to `False`.
   * `--normalization`: Should we divide the counts of every input sequence by the number of text entries that were associated to it. Defaults to `True`.
   * `--num_threads`: Number of cores to use (Defaults to the total number of cores). Use `1` for non-parallel processing.
   * `--out_dir`: The output directory in which to store the result and intermediary files. Defaults to the same directory as the input file.
   * `--min_identity`: Minimum identity in similarity search (Default: `0.97`). Note: not available when using `blastp`.
   * `--e_value`: Minimum e-value in similarity search (Default: 0.0001`).
   * `--max_targets`: Maximum number of reference matches in the similarity search (Default: `10`).
   * `--min_coverage`: Minimum query coverage in similarity search (Default: `0.97`).
   * `--abundances`: Abundances file as TSV with OTUs as rows and sample names as columns (Default: None).
   * `--N`: If abundances are given, pick only the top N sequences (Default: `1000`).

### Introduction
The continuous drop in the associated costs combined with the increased efficiency of the latest high-throughput sequencing technologies has resulted in an unprecedented growth in sequencing projects. Ongoing endeavours such as the [Earth Microbiome Project](http://www.earthmicrobiome.org) and the [Ocean Sampling Day](http://www.microb3.eu/osd) are transcending national boundaries and are attempting to characterise the global microbial taxonomic and functional diversity for the benefit of mankind. The collection of sequencing information generated by such efforts is vital to shed light on the ecological features and the processes characterising different ecosystems, yet, the full knowledge discovery potential can only be unleashed if the associated meta data is also exploited to extract hidden patterns. For example, with the majority of genomes submitted to NCBI, there is an associated PubMed publication and in some cases there is a GenBank field called "isolation sources" that contains rich environmental information.
With the advances in community-generated standards and the adherence to recommended annotation guidelines such as those of [MIxS](http://gensc.org/gc_wiki/index.php/MIxS) of the Genomics Standards Consortium, it is now feasible to support intelligent queries and automated inference on such text resources.

The [Environmental Ontology](http://environmentontology.org/) will be a critical part of this approach as it gives the ontology for the concise, controlled description of environments. It thus provides structured and controlled vocabulary for the unified meta data annotation, and also serves as a source for naming environmental information. Thus, we have developed the `seqenv` pipeline capable of annotating sequences with environment descriptive terms occurring within their records and/or in relevant literature. Given a set of sequences, `seqenv` retrieves highly similar sequences from public repositories (NCBI GenBank). Subsequently, from each of these records, text fields carrying environmental context information (such as the reference title and the **isolation source**) are extracted. Once the relevant pieces of text for each matching sequence have been gathered, they are then processed by a text mining module capable of identifying EnvO terms mentioned in them terms such as glacier, pelagic, forest, lagoon). The identified EnvO terms along with their frequencies of occurrence are then subjected to clustering analysis and multivariate statistics. As a result, tagclouds and heatmaps of environment descriptive terms characterizing different sequences/samples are generated. The `seqenv` pipeline can be applied to any set of nucleotide and protein sequences. Annotation of metagenomic samples, in particular 16S rRNA sequences is also supported.

The pipeline has already been applied to a range of datasets (e.g Greek lagoon, Swedish lake/river, African and Asian pitlatrine datasets, Black Sea sediment sample datasets have been processed).

### Pipeline overview
#### This is an old version of the diagram.. the current version of seqenv doesn't exactly do this.
![seqenv](/biohackers/seqenv/raw/master/documentation/frequencies.png "seqenv")

### Tutorial
We will first run `seqenv` on a 16S rRNA dataset using ***isolation sources*** as a text source. Here, `abundance.tsv` is a species abundance file (97% OTUs) processed through [`illumitag`](https://github.com/limno/illumitag) software and `centers.fasta` contains the corresponding sequences for the OTUs.

~~~
$ ls
abundance.tsv
centers.fasta

$ seqenv centers.fasta --abundances abundance.tsv --seq_type nucl --out_dir output --N 1000 --min_identity 0.99
~~~

The output you will receive should look something like this:

~~~
seqenv version 1.0.3 (pid 20539)
Start at: 2015-07-24 03:50:37.982581
--> STEP 1: Parse the input FASTA file.
Elapsed time: 0:00:02.345551
Using: output/renamed.fasta
--> STEP 1B: Get the top 1000 sequences (in terms of their abundances).
Elapsed time: 0:00:00.504347
Using: output/top_seqs.fasta
--> STEP 2: Similarity search against the 'nt' database with 24 processes
Elapsed time: 0:38:30.489685
--> STEP 3: Filter out bad hits from the search results
Elapsed time: 0:00:00.022893
--> STEP 4: Parsing the search results
Elapsed time: 0:00:00.069423
--> STEP 5: Loading all NCBI isolation sources in RAM
Elapsed time: 0:02:18.169891
Got 5654 GIs from search results
--> STEP 6: Run the text mining tagger on all blobs.
Elapsed time: 0:00:00.269561
Using 853 different isolation sources
--> STEP 7: Parsing the tagger results and counting terms.
Elapsed time: 0:00:00.014824
------------
Success. Outputs are in 'output/'
End at: 2015-07-24 04:31:42.324913
Total elapsed time: 0:41:04.342529
~~~

Once the pipeline has finished processing, you will have the following contents in the output folder:

~~~
$ ls output/
list_concepts_found.tsv  seq_to_concepts.tsv    text_to_matches.pickle
renamed.fasta            seq_to_gis.pickle      top_seqs.blastout
samples.biom             seq_to_names.tsv       top_seqs.fasta
samples_to_names.tsv     text_to_counts.pickle  top_seqs.fasta.parts
~~~

The most interesting files are probably:

* `list_concepts_found.tsv` links every OTU to all its relevent BLAST hits and linked ENVO terms.
* `seq_to_names.tsv` a matrix linking every OTU to its "composition" in terms of ENVO identifiers translated to readable names.
* `samples_to_names.tsv` if an abundance file was provided, this is a a matrix linking every one of your samples to its "composition" in terms of ENVO identifiers translated to readable names.

### Acknowledgments
`seqenv` was conceived and developed in the following hackathons supported by European Union's Earth System Science and Environmental Management ES1103 COST Action ("[Microbial ecology & the earth system: collaborating for insight and success with the new generation of sequencing tools](http://www.cost.eu/domains_actions/essem/Actions/ES1103)"):

- **From Signals to Environmentally Tagged Sequences** (Ref: ECOST-MEETING-ES1103-050912-018418), September 27th-29th 2012, Hellenic Centre for Marine Research, Crete, Greece.
- **From Signals to Environmentally Tagged Sequences II** (Ref: ECOST-MEETING-ES1103-100613-031037), June 10th-13th 2013, Hellenic Centre for Marine Research, Crete, Greece.
- **From Signals to Environmentally Tagged Sequences III** (Ref: ECOST-MEETING-ES1103-220914-047036), September 22nd-25th 2014, Hellenic Centre for Marine Research, Crete, Greece.

This work would not have been possible without the advice and support of many people who attended the hackathons:

- [Umer Zeeshan Ijaz](http://userweb.eng.gla.ac.uk/umer.ijaz) (Umer.Ijaz@glasgow.ac.uk) [1,2]
- [Evangelos Pafilis](http://epafilis.info/) (pafilis@hcmr.gr) [1,2]
- [Chris Quince](http://www.gla.ac.uk/schools/engineering/staff/christopherquince/) (cq8u@udcf.gla.ac.uk) [2]
- Christina Pavloudi (cpavloud@hcmr.gr)
- Anastasis Oulas (oulas@hcmr.gr)
- Julia Schnetzer (jschnetz@mpi-bremen.de)
- Aaron Weimann (aaron.weimann@uni-duesseldorf.de)
- Alica Chronakova (alicach@upb.cas.cz)
- Ali Zeeshan Ijaz (alizeeshanijaz@gmail.com)
- Simon Berger (simon.berger@h-its.org)
- Lucas Sinclair (lucas.sinclair@me.com) [1]

[1] Main developers
[2] Contact for correspondence

### News
* **August 2013**: Chris Quince presented a talk on `seqenv` at [STAMPS2013](https://stamps.mbl.edu/index.php/Main_Page). You can download the PDF of the presentation: [C Quince et. al., SeqEnv: Annotating sequences with environments (STAMPS 2013)](https://stamps.mbl.edu/images/4/44/Quince_SeqEnvSTAMPS2013.pdf)

### Manual installation
This chapter will be removed once the simple `pip install seqenv` is fully operational. In the meantime, no automated installation has been developed for the `seqenv` package. But following this document and typing these commands on your bash prompt should get you started. If you cannot get a functional installation set up, contact the authors.

##### Step 1: Cloning the repository
Here you will download a copy of the code from bitbucket and place it somewhere in your home directory.

    $ cd ~
    $ mkdir repos
    $ cd repos
    $ git clone git@bitbucket.org:biohackers/seqenv.git

##### Step 2: Modify your search paths
Here you will edit your ``~/.bashrc`` or ``~/.bash_profile`` to add a reference to the code you just downloaded.

    $ vim ~/.bash_profile
    export PYTHONPATH="$HOME/repos/seqenv/":$PYTHONPATH

    $ vim ~/.bash_profile
    export PATH="$HOME/repos/seqenv/seqenv":$PATH

##### Step 3 (optional): Install your own version of python
Your system probably comes with a version of python installed. But the variations from system to system are too great to rely on any available python. We strongly suggest to just install our own version in your home directory. Otherwise make sure that you are using version 2.7.x of python.

##### Step 4: Install all required python packages
`seqenv` uses several third party python libraries. You can get them by running these commands:

    $ pip install biopython
    $ pip install sh
    $ pip install pandas
    $ pip install tqdm
    $ pip install biom-format

If you are using a python manager such as pyenv, don't forget to rehash the binary links at the end:

    $ pyenv rehash

You can check that it all works like this:

    $ python -c "import seqenv"

##### Step 5: Check you have all the required executables
`seqenv` will search for several different binaries as it processes your data. Please check all of these are available in your `$PATH`:

    $ which blastn

##### Step 6: Compile the tagger if on OS X
Having to compile code is a liability to installation unfortunately, but we don't have any other solution for the moment. I remember that there were some complicated tricks to compile it on OS X, so you will have to figure that out if you are using a Mac. But with Linux hopefully it shouldn't be too difficult because we have a precompiled binary bundled now so you can skip this step ! Unless it's a 32-bit processor, than again it's going to be difficult.

    $ cd ~/repos/seqenv/tagger
    $ make

##### Step 7: Get a local copy of the NT database
You can choose the database you want to BLAST against. By default we will search against `nt. So check your `~/.ncbirc` file for the adequate references.