# `seqenv` version 1.0.4
* Assign environment ontology (EnvO) terms to short DNA sequences.
* More information at: http://environments.hcmr.gr/seqenv.html
* Code written by [Lucas Sinclair](http://envonautics.com/#lucas).

### Installing (doesn't work yet, go to manual install)
To install `seqenv` onto your machine, use the python package manager:

    $ pip install seqenv

You might be installing this onto a computer server which you don't own and thus don't have sufficient privileges. In that case you can install everything in your home directory like this:

    $ pip install --user seqenv

If this still doesn't work, you might be missing the `pip` program on your system or the correct version of Python (any version `2.7.x`). You can get both of these things by using using this little project: https://github.com/yyuu/pyenv

### Dependencies
* You need to have a copy of the NCBI nucleotide data base (called `nt`) installed locally as well as the `blastn` executable in your `$PATH`. So that BLAST finds the NT database, you can edit your `~/.ncbirc` file.
* The project also depends on some other python modules such as `biopython`. Happily, these will be installed automatically when calling the `pip` command above.

### Optional dependencies
* To compile parts of the software you might need a working installation of the BOOST libraries as well as the SWIG libraries.

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
   * `--normalization`: Can be either of `flat`, `ui` or `upui`. This option defaults to `ui`.
                      > If you choose `flat`, we will count every isolation source once,
                          even if the same text entry appears several time for the same input
                          sequence.
                      > If you choose `ui`, standing for unique isolation, we will uniquify
                          every frequency count depending on the text entry of its isolation
                          source.
                      > If you choose `upui`, standing for unique isolation and unique pubmed-ID,
                          we will uniquify the frequency counts based on the text entry of its
                          isolation source and the pubmed-ID from which the isolation text was
                          obtained.
   * `--proportional`: Should we divide the counts of every input sequence by the number of text entries that were associated to it. Defaults to `True`.
   * `--backtracking`: For every term identified by the tagger, we will propagate frequency counts up the acyclic directed graph described by the ontology. Defaults to `False`.
   * `--num_threads`: Number of cores to use (Defaults to the total number of cores). Use `1` for non-parallel processing.
   * `--out_dir`: The output directory in which to store the result and intermediary files. Defaults to the same directory as the input file.
   * `--min_identity`: Minimum identity in similarity search (Default: `0.97`). Note: not available when using `blastp`.
   * `--e_value`: Minimum e-value in similarity search (Default: `0.0001`).
   * `--max_targets`: Maximum number of reference matches in the similarity search (Default: `10`).
   * `--min_coverage`: Minimum query coverage in similarity search (Default: `0.97`).
   * `--abundances`: Abundances file as TSV with OTUs as rows and sample names as columns (Default: None).
   * `--N`: If abundances are given, pick only the top N sequences (Default: `1000`).

### Why make this ?
The continuous drop in the associated costs combined with the increased efficiency of the latest high-throughput sequencing technologies has resulted in an unprecedented growth in sequencing projects. Ongoing endeavours such as the [Earth Microbiome Project](http://www.earthmicrobiome.org) and the [Ocean Sampling Day](http://www.microb3.eu/osd) are transcending national boundaries and are attempting to characterise the global microbial taxonomic and functional diversity for the benefit of mankind. The collection of sequencing information generated by such efforts is vital to shed light on the ecological features and the processes characterizing different ecosystems, yet, the full knowledge discovery potential can only be unleashed if the associated meta data is also exploited to extract hidden patterns. For example, with the majority of genomes submitted to NCBI, there is an associated PubMed publication and in some cases there is a GenBank field called "isolation sources" that contains rich environmental information.

With the advances in community-generated standards and the adherence to recommended annotation guidelines such as those of [MIxS](http://gensc.org/gc_wiki/index.php/MIxS) of the Genomics Standards Consortium, it is now feasible to support intelligent queries and automated inference on such text resources.

The [Environmental Ontology](http://environmentontology.org/) (or EnvO) will be a critical part of this approach as it gives the ontology for the concise, controlled description of environments. It thus provides structured and controlled vocabulary for the unified meta data annotation, and also serves as a source for naming environmental information. Thus, we have developed the `seqenv` pipeline capable of annotating sequences with environment descriptive terms occurring within their records and/or in relevant literature.

The `seqenv` pipeline can be applied to any set of nucleotide or protein sequences. Annotation of metagenomic samples, in particular 16S rRNA sequences is also supported.

The pipeline has already been applied to a range of datasets (e.g Greek lagoon, Swedish lake/river, African and Asian pitlatrine datasets, Black Sea sediment sample datasets have been processed).

### What does it do exactly ?
 Given a set of DNA sequences, `seqenv` first retrieves highly similar sequences from public repositories (e.g. NCBI GenBank) using BLAST or similar algorithm. Subsequently, from each of these homologous records, text fields carrying environmental context information such as the reference title and the **isolation source** field found in the metadata are extracted. Once the relevant pieces of text from each matching sequence have been gathered, they are processed by a text mining module capable of identifying any EnvO terms they contain (e.g. the word "glacier", or "pelagic", "forest", etc.). The identified EnvO terms along with their frequencies of occurrence are then subjected to multivariate statistics, producing matrices XXXXXX as well as other useful outputs.

### Pipeline overview
[![seqenv](documentation/frequencies.png)](documentation/frequencies.png)

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
seqenv version 1.0.4 (pid 52169)
Start at: 2016-03-02 00:22:09.727377
--> STEP 1: Parse the input FASTA file.
Elapsed time: 0:00:00.005811
Using: output/renamed.fasta
--> STEP 2: Similarity search against the 'nt' database with 5 processes
Elapsed time: 0:02:11.215829
--> STEP 3: Filter out bad hits from the search results
Elapsed time: 0:00:00.002071
--> STEP 4: Parsing the search results
Elapsed time: 0:00:00.002099
Elapsed time: 0:00:00.000156
--> STEP 5: Loading database with all NCBI isolation sources
Got 60 unique GIs from search results
Got 56 unique GIs with an isolation source
Got 24 unique isolation source texts
Elapsed time: 0:00:01.496406
--> STEP 6: Run the text mining tagger on all blobs.
Elapsed time: 0:00:00.025384
Got 28 environmental term matches
--> STEP 7: Parsing the tagger results and counting terms.
Elapsed time: 0:00:00.001027
------------
Success. Outputs are in 'output/'
End at: 2016-03-02 00:24:22.504485
Total elapsed time: 0:02:12.777297
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

* `list_concepts_found.tsv` links every OTU to all its relevant BLAST hits and linked ENVO terms.
* `seq_to_names.tsv` a matrix linking every OTU to its "composition" in terms of ENVO identifiers translated to readable names.
* `samples_to_names.tsv` if an abundance file was provided, this is a a matrix linking every one of your samples to its "composition" in terms of ENVO identifiers translated to readable names.

### Acknowledgments
`seqenv` was conceived and developed in the following hackathons supported by European Union's Earth System Science and Environmental Management ES1103 COST Action ("[Microbial ecology & the earth system: collaborating for insight and success with the new generation of sequencing tools](http://www.cost.eu/domains_actions/essem/Actions/ES1103)"):

- **From Signals to Environmentally Tagged Sequences** (Ref: ECOST-MEETING-ES1103-050912-018418), September 27th-29th 2012, Hellenic Centre for Marine Research, Crete, Greece.
- **From Signals to Environmentally Tagged Sequences II** (Ref: ECOST-MEETING-ES1103-100613-031037), June 10th-13th 2013, Hellenic Centre for Marine Research, Crete, Greece.
- **From Signals to Environmentally Tagged Sequences III** (Ref: ECOST-MEETING-ES1103-220914-047036), September 22nd-25th 2014, Hellenic Centre for Marine Research, Crete, Greece.

This work would not have been possible without the advice and support of many people who attended the hackathons, in alphabetical order:

- Simon Berger (simon.berger@h-its.org)
- Alica Chronakova (alicach@upb.cas.cz)
- Anastasis Oulas (oulas@hcmr.gr)
- [Evangelos Pafilis](http://epafilis.info/) (pafilis@hcmr.gr) [2]
- Christina Pavloudi (cpavloud@hcmr.gr)
- [Chris Quince](http://www2.warwick.ac.uk/fac/med/staff/cquince/) (c.quince@warwick.ac.uk) [3]
- Julia Schnetzer (jschnetz@mpi-bremen.de)
- [Lucas Sinclair](http://envonautics.com/#lucas) (lucas.sinclair@me.com) [1]
- Aaron Weimann (aaron.weimann@uni-duesseldorf.de)
- Ali Zeeshan Ijaz (alizeeshanijaz@gmail.com)
- [Umer Zeeshan Ijaz](http://userweb.eng.gla.ac.uk/umer.ijaz/) (umer.ijaz@glasgow.ac.uk) [3]

[1] Main developer
[2] Contact for correspondence
[3] Original idea

### News
* **August 2013**: Chris Quince presented a talk on `seqenv` at [STAMPS2013](https://stamps.mbl.edu/index.php/Main_Page). You can download the PDF of the presentation: [C Quince et. al., SeqEnv: Annotating sequences with environments (STAMPS 2013)](https://stamps.mbl.edu/images/4/44/Quince_SeqEnvSTAMPS2013.pdf)

### Publications that have used seqenv
* Bacterial diversity along a 2600 km river continuum. `doi:10.1111/1462-2920.12886`
* Can marine bacteria be recruited from freshwater sources and the air? `doi:10.1038/ismej.2014.89`

### Manual installation
This chapter will be removed once the simple `pip install seqenv` is fully operational. In the meantime, no automated installation has been developed for the `seqenv` package. But following this document and typing these commands on your bash prompt should get you started. If you cannot get a functional installation set up, contact the authors.

##### Step 1: Cloning the repository
Here you will download a copy of the code and place it somewhere in your home directory.

    $ cd ~
    $ mkdir repos
    $ cd repos
    $ git clone https://github.com/xapple/seqenv.git

##### Step 2: Modify your search paths
Here you will edit your ``~/.bashrc`` or ``~/.bash_profile`` to add a reference to the code you just downloaded.

    $ vim ~/.bash_profile
    export PYTHONPATH="$HOME/repos/seqenv/":$PYTHONPATH

    $ vim ~/.bash_profile
    export PATH="$HOME/repos/seqenv/seqenv":$PATH

And finally source your `.bash_profile` file if you haven't already.

##### Step 3 (optional): Install your own version of python
Your system probably comes with a version of python installed. But the variations from system to system are too great to rely on any available python. We strongly suggest to just install our own version in your home directory. Otherwise make sure that you are using version 2.7.x of python.

##### Step 4: Check you have all the required executables
`seqenv` will search for several different binaries as it processes your data. Please check all of these are available in your `$PATH`:

    $ which blastn

##### Step 5: Get a local copy of the NT database
You can choose the database you want to BLAST against. By default we will search against `nt`. So check your `~/.ncbirc` file for the adequate references. If you don't have a copy of such a database, you need to download one to your machine.

##### Step 6: Install all required python packages
`seqenv` uses several third party python libraries. You can get them by running these commands:

    $ pip install biopython
    $ pip install sh
    $ pip install pandas
    $ pip install tqdm
    $ pip install biom-format
    $ pip install requests

If you are on a machine that does not authorize you to install packages like that you can try to install them only for your user:

    $ pip install --user biopython
    $ pip install --user sh
    $ pip install --user pandas
    $ pip install --user tqdm
    $ pip install --user biom-format
    $ pip install --user requests

If you are using a python manager such as pyenv, don't forget to rehash the binary links at the end:

    $ pyenv rehash

Now, you can check that it all works like this, if it doesn't, go to the "Troubleshooting" section:

    $ python -c "import seqenv"

### Troubleshooting
##### Compiling the tagger
Having to compile code is a liability to installation unfortunately, but we don't have any other solution for the moment. I remember that there were some complicated tricks to compile it on OS X, so you will have to figure that out if you are using a Mac. But with Linux hopefully it shouldn't be too difficult because we have a precompiled binary bundled now so you can skip this step ! Unless it's a 32-bit processor, than again it's going to be difficult.

In the case you get an error such as `ImportError: libboost_regex.so.5: cannot open shared object file` it means that `seqenv` tried using the precompiled version of the tagger but it didn't find the needed libraries installed on your system. In such a case you need to compile the tagger:

    $ cd ~/repos/seqenv/tagger
    $ make

In the case you get an error such as `/usr/bin/ld: cannot find -lpython` it means you are missing some libraries. You can try changing the following line in the makefile:

    LFLAGS = -fpic -shared -lboost_regex -lpython2.7

You might also need to install the boost libraries. For CentOS and RedHat the following yum command works, otherwise try with `apt-get`.

    $ sudo yum install boost-devel

If you are trying to compile on OS X you might need to change another line in the makefile (assuming you have python installed via homebrew):

    PYTHON = -I/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/include/python2.7

Then you might run into other problems on OS X and need to add other includes such as:

    -I/usr/local/Cellar/boost/1.57.0/include/boost/tr1

