from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio import AlignIO
def createTree(file):
    aln = AlignIO.read(file, 'phylip')
    # Calculate the distance matrix
    calculator = DistanceCalculator('identity')
    dm = calculator.get_distance(aln)

    # Construct the phylogenetic tree using UPGMA algorithm
    constructor = DistanceTreeConstructor()
    tree = constructor.upgma(dm)
    Phylo.write(tree, 'new.xml' , 'phyloxml')
    