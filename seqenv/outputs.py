# Built-in modules #
import warnings

# Internal modules #
import seqenv
from seqenv.common import flatter
from seqenv.common.cache import property_cached

# Third party modules #
import pandas

# We don't want the annoying h5py warning #
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import biom

################################################################################
class OutputGenerator(object):
    """Once the Analysis is run and all the data is in memory in the
    form of python objects, this class will take care of generating
    all the output files the user could possibly want. You pass it the Analysis
    object obviously."""

    sep = '\t'
    float_format = '%.5g'

    def __init__(self, analysis):
        self.analysis = analysis
        self.a        = analysis

    def make_all(self):
        """Let's generate all the files"""
        # General matrices #
        self.tsv_seq_to_concepts()
        self.tsv_seq_to_names()
        self.list_sequence_concept()
        # Only in the with 'samples' case #
        if self.a.abundances: self.tsv_samples_to_names()
        if self.a.abundances: self.biom_output()

    @property_cached
    def df_seqs_concepts(self):
        """A normalized dataframe with sequences as columns and concepts (envo terms) as rows."""
        # Get the data #
        df = pandas.DataFrame(self.a.seq_to_counts)
        df = df.fillna(0)
        # Rename to original names #
        df = df.rename(columns=self.a.renamed_to_orig)
        # Return
        return df

    def tsv_seq_to_concepts(self):
        """A TSV matrix file containing the df_seqs_concepts matrix"""
        with open(self.a.out_dir + 'seq_to_concepts.tsv', 'w') as handle:
            content = self.df_seqs_concepts.to_csv(None, sep=self.sep, float_format=self.float_format)
            handle.writelines(content)

    def tsv_seq_to_names(self, sep='\t'):
        """A TSV matrix file where we translate the concept to human readable names"""
        with open(self.a.out_dir + 'seq_to_names.tsv', 'w') as handle:
            df = self.df_seqs_concepts.rename(index=self.a.concept_to_name)
            content = df.to_csv(None, sep=self.sep, float_format=self.float_format)
            handle.writelines(content)

    @property_cached
    def df_sample_names(self):
        """A dataframe where we operate a matrix multiplication with the abundances file
        provided to link samples to concept human readable names"""
        # Get results #
        df1 = self.df_seqs_concepts.rename(index=self.a.concept_to_name)
        # Remove those that were discarded #
        df2 = self.a.df_abundances
        df2 = df2.loc[df1.columns]
        # Multiply them #
        df = df1.dot(df2)
        # Return
        return df

    def tsv_samples_to_names(self, sep='\t'):
        """A TSV matrix file where operate a matrix multiplication with the abundances file
        provided to link samples to concept human readable names"""
        with open(self.a.out_dir + 'samples_to_names.tsv', 'w') as handle:
            content = self.df_sample_names.to_csv(sep=self.sep, float_format=self.float_format)
            handle.writelines(content)

    def list_sequence_concept(self):
        """A flat TSV file listing every concept found for every sequence.
        It has one concept per line and looks something like this:
        - OTU1, ENVO:00001, ocean, 4, GIs : [56, 123, 345]
        - OTU1, ENVO:00002, soil, 7, GIs : [22, 44]
        """
        with open(self.a.out_dir + 'list_concepts_found.tsv', 'w') as handle:
            for seq, gis in self.a.seq_to_gis.items():
                gis = [gi for gi in gis if gi in self.a.gi_to_text and self.a.gi_to_text[gi] in self.a.text_to_counts]
                texts = set(self.a.gi_to_text[gi] for gi in gis)
                concepts = set(flatter(self.a.text_to_counts[t].keys() for t in texts))
                for concept in concepts:
                    seq_name     = self.a.renamed_to_orig[seq]
                    concept_name = self.a.concept_to_name.get(concept, concept)
                    concept_gis  = [gi for gi in gis if concept in self.a.text_to_counts[self.a.gi_to_text[gi]]]
                    count_gis    = len(concept_gis)
                    line         = (seq_name, concept, concept_name, str(count_gis), str(concept_gis))
                    handle.write('\t'.join(line) + '\n')

    def biom_output(self):
        """The same matrix as the user gave in the abundance file, but with source
        information attached for every sequence.
        See http://biom-format.org"""
        data = self.a.df_abundances
        with open(self.a.out_dir + 'samples.biom', 'w') as handle:
            # Basic #
            sample_ids = data.columns
            sample_md = None
            observation_ids = data.index
            # Observation metadata #
            observation_md = []
            for seq in data.index:
                seq_name = self.a.orig_names_to_renamed[seq]
                counts = self.a.seq_to_counts.get(seq_name)
                if not counts: observation_md.append({})
                else: observation_md.append({'source': counts})
            # Output #
            t = biom.table.Table(data.transpose().as_matrix(), sample_ids, observation_ids, sample_md, observation_md)
            handle.write(t.to_json('seqenv version %s') % seqenv.__version__)

    def output_3(self):
        """Possible output #3: the number of terms per OTU
        OTU1: 0
        OTU2: 2
        OTU3: 1"""
        pass
