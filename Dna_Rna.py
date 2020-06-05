class NucleicAcids:
    def __init__(self, seq):
        self.seq = seq

    def gc_content(self):
        return len([i for i in self.seq if i in "GC"]) * 100 / len(self.seq)

    def __eq__(self, other):
        return self.seq == other.seq

    def __iter__(self):
        return iter(self.seq)

    def __hash__(self):
        return hash(self.seq)


class Dna(NucleicAcids):
    def reverse_complement(self):
        complement = {'G': 'C', 'C': 'G', 'A': 'T', 'T': 'A'}
        return ''.join([complement[i] for i in self.seq][::-1])

    def transcribe(self):
        return Rna(''.join([i if i in 'GCA' else 'U' for i in self.seq]))


class Rna(NucleicAcids):
    def reverse_complement(self):
        complement = {'G': 'C', 'C': 'G', 'A': 'U', 'U': 'A'}
        return ''.join([complement[i] for i in self.seq][::-1])
