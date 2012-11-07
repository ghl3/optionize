
import optionize

class ExistingThing(optionize.OptionizedClass):
    ontology = 'irrational'
    permanence = 'little'


class LivingThing(ExistingThing):
    kill = ('decay', None, 'kill the thing')
    born = ('eggs', None, 'how the thing is born')


class AnimalThing(LivingThing):
    born = ('live birth', None, 'how the thing is born')
    mass = 42.0


class OutputConfiguation(optionize.OptionizedClass):
    infile = ("input.dat", 'i', 'input file to read from')
    outfile = ("output.dat", 'o', 'file to output to result')
    parallel = False
    format = ('ascii', 'f', 'output file format')


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    animal = AnimalThing()
    outcfg = OutputConfiguation()

    animal.add_options(parser)
    outcfg.add_options(parser)

    opts, args = parser.parse_args()

    animal.report()
    outcfg.report()
