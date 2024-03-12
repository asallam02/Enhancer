import gzip
import kipoiseq
from kipoiseq import Interval
import pyfaidx
import numpy as np

SEQUENCE_LENGTH = 393216

# this is to read from fasta files
class FastaStringExtractor:
  def __init__(self, fasta_file):
      self.fasta = pyfaidx.Fasta(fasta_file)
      self._chromosome_sizes = {k: len(v) for k, v in self.fasta.items()}

  def extract(self, interval: Interval, **kwargs) -> str:
      # Truncate interval if it extends beyond the chromosome lengths.
      print(interval.chrom)
      print(self._chromosome_sizes)
      chromosome_length = self._chromosome_sizes[interval.chrom]
      trimmed_interval = Interval(interval.chrom,
                                  max(interval.start, 0),
                                  min(interval.end, chromosome_length),
                                  )
      # pyfaidx wants a 1-based interval
      sequence = str(self.fasta.get_seq(trimmed_interval.chrom,
                                        trimmed_interval.start + 1,
                                        trimmed_interval.stop).seq).upper()
      # Fill truncated values with N's.
      pad_upstream = 'N' * max(-interval.start, 0)
      pad_downstream = 'N' * max(interval.end - chromosome_length, 0)
      return pad_upstream + sequence + pad_downstream

  def close(self):
      return self.fasta.close()


def variant_generator(vcf_file, gzipped=False):
  """Yields a kipoiseq.dataclasses.Variant for each row in VCF file."""
  def _open(file):
    return gzip.open(vcf_file, 'rt') if gzipped else open(vcf_file)
    
  with _open(vcf_file) as f:
    for line in f:
      if line.startswith('#'):
        continue
      chrom, pos, id, ref, alt_list = line.split('\t')[:5]
      # Split ALT alleles and return individual variants as output.
      for alt in alt_list.split(','):
        yield kipoiseq.dataclasses.Variant(chrom=chrom, pos=pos,
                                           ref=ref, alt=alt, id=id)


def one_hot_encode(sequence):
  return kipoiseq.transforms.functional.one_hot_dna(sequence).astype(np.float32)

def create_target_interval(chrom, start, end):
   return kipoiseq.Interval(chrom, start, end)

def create_fasta_file(fasta_seq: str, file_name):
   fasta_out = open(file_name, 'w')
   fasta_out.write(fasta_seq)
   fasta_out.close()

# preprocesses a fasta formatted sequence
def preprocess_seq(seq):
   filename = "fasta.txt"
   create_fasta_file(seq, filename)
   fasta_extractor = FastaStringExtractor(filename)
   target_interval = kipoiseq.Interval('4OO8_1|Chains', 1, 1372) # need to change this
   sequence_one_hot = one_hot_encode(fasta_extractor.extract(target_interval.resize(SEQUENCE_LENGTH)))
   return sequence_one_hot

# preprocesses a fasta file
def preprocess_file(filename):
   fasta_extractor = FastaStringExtractor(filename)
   target_interval = kipoiseq.Interval('4OO8_1|Chains', 1, 1372) # need to change this
   sequence_one_hot = one_hot_encode(fasta_extractor.extract(target_interval.resize(SEQUENCE_LENGTH)))
   return sequence_one_hot

if __name__ == "__main__":
   fasta_string = """>4OO8_1|Chains A, D|CRISPR-associated endonuclease Cas9/Csn1|Streptococcus pyogenes serotype M1 (301447)
GSGHMDKKYSIGLAIGTNSVGWAVITDEYKVPSKKFKVLGNTDRHSIKKNLIGALLFDSGETAEATRLKRTARRRYTRRKNRILYLQEIFSNEMAKVDDSFFHRLEESFLVEEDKKHERHPIFGNIVDEVAYHEKYPTIYHLRKKLVDSTDKADLRLIYLALAHMIKFRGHFLIEGDLNPDNSDVDKLFIQLVQTYNQLFEENPINASGVDAKAILSARLSKSRRLENLIAQLPGEKKNGLFGNLIALSLGLTPNFKSNFDLAEDAKLQLSKDTYDDDLDNLLAQIGDQYADLFLAAKNLSDAILLSDILRVNTEITKAPLSASMIKRYDEHHQDLTLLKALVRQQLPEKYKEIFFDQSKNGYAGYIDGGASQEEFYKFIKPILEKMDGTEELLVKLNREDLLRKQRTFDNGSIPHQIHLGELHAILRRQEDFYPFLKDNREKIEKILTFRIPYYVGPLARGNSRFAWMTRKSEETITPWNFEEVVDKGASAQSFIERMTNFDKNLPNEKVLPKHSLLYEYFTVYNELTKVKYVTEGMRKPAFLSGEQKKAIVDLLFKTNRKVTVKQLKEDYFKKIEEFDSVEISGVEDRFNASLGTYHDLLKIIKDKDFLDNEENEDILEDIVLTLTLFEDREMIEERLKTYAHLFDDKVMKQLKRRRYTGWGRLSRKLINGIRDKQSGKTILDFLKSDGFANRNFMQLIHDDSLTFKEDIQKAQVSGQGDSLHEHIANLAGSPAIKKGILQTVKVVDELVKVMGRHKPENIVIEMARENQTTQKGQKNSRERMKRIEEGIKELGSQILKEHPVENTQLQNEKLYLYYLQNGRDMYVDQELDINRLSDYDVDAIVPQSFLKDDSIDNKVLTRSDKNRGKSDNVPSEEVVKKMKNYWRQLLNAKLITQRKFDNLTKAERGGLSELDKAGFIKRQLVETRQITKHVAQILDSRMNTKYDENDKLIREVKVITLKSKLVSDFRKDFQFYKVREINNYHHAHDAYLNAVVGTALIKKYPKLESEFVYGDYKVYDVRKMIAKSEQEIGKATAKYFFYSNIMNFFKTEITLANGEIRKRPLIETNGETGEIVWDKGRDFATVRKVLSMPQVNIVKKTEVQTGGFSKESILPKRNSDKLIARKKDWDPKKYGGFDSPTVAYSVLVVAKVEKGKSKKLKSVKELLGITIMERSSFEKNPIDFLEAKGYKEVKKDLIIKLPKYSLFELENGRKRMLASAGELQKGNELALPSKYVNFLYLASHYEKLKGSPEDNEQKQLFVEQHKHYLDEIIEQISEFSKRVILADANLDKVLSAYNKHRDKPIREQAENIIHLFTLTNLGAPAAFKYFDTTIDRKRYTSTKEVLDATLIHQSITGLYETRIDLSQLGGD
"""
   sequence_one_hot = preprocess_seq(fasta_string)
   print(sequence_one_hot)
