#!/usr/bin/env python3

import sys, re

class Net:
    """
    Class for Bayesian Network.

    Data structures:
        list of variable names
        dictionary that maps variable names to a dictonary {
                parents -> list of parents
                children -> list of children
                prob -> probability of the variable if it's independent, else None
                condprob -> dictionary for the conditionary probability table {
                        tuple of values for parents -> probability
                    }
            }

        e.g. for ex2.bn
        ('A', B', 'C', 'D', 'E')
        {
            'A': {
                'parents': [],
                'children': ['C', 'D'],
                'prob': 0.3,
                'condprob': {}
            },
            
            ...

            'D': {
                'parents': ['A', 'B'],
                'children': [],
                'prob': -1,
                'condprob': {
                    (True, True): 0.7,
                    (True, False): 0.8,
                    ...
                }
            }
        }
    """
    def __init__(self, fname):
        self.vars = set()
        self.net = {}
        with open(fname) as f:
            lines = []
            for line in f:
                if line == '\n':
                    self._parse(lines)
                    lines = []
                else:
                    lines.append(line)


    def _parse(self, lines):
        if len(lines) == 1:
            #  single line
            match = re.match(r'P\((.*)\) = (.*)\n', lines[0])
            var, prob = match.group(1).strip(), float(match.group(2).strip())
            self.vars.add(var)
            self.net[var] = {
                'parents': [], 
                'children': [],
                'prob': prob,
                'condprob': {}
            }
        else:
            # table header
            match = re.match(r'(.*) \| (.*)', lines[0])
            parents, var = match.group(1).split(), match.group(2).strip()
            self.vars.add(var)
            for p in parents:
                self.net[p]['children'].append(var)
            self.net[var] = {
                'parents': parents,
                'children': [],
                'prob': -1,
                'condprob': {}
            }

            # table entries
            for probline in lines[2:]:
                match = re.match(r'(.*) \| (.*)', probline)
                truth, prob = match.group(1).split(), float(match.group(2).strip())
                truth = tuple(True if x == 't' else False for x in truth)
                self.net[var]['condprob'][truth] = prob

def enum_ask(X, e, bn):
    """
    Calculate the distribution over the query variable X using enumeration.

    Args:
        X:  The query variable.
        e:  Dictionary of evidence variables and observed values.
        bn: Bayes net.

    Returns:
        Distribution over X as a tuple (t, f).
    """
    pass

def elim_ask(X, e, bn):
    """
    Calculate the distribution over the query variable X using elimination.

    Args:
        X:  The query variable.
        e:  Dictionary of evidence variables and observed values.
        bn: Bayes net.

    Returns:
        Distribution over X as a tuple (t, f).
    """

def query(net, alg, q):
    pass

def main():
    try:
        net = Net(sys.argv[1])

        alg = sys.argv[2]
        assert(alg == 'enum' or alg == 'elim')

        q = sys.argv[3]

        query(net, alg, q)
    except SyntaxError:
        print('Invalid syntax for bayes net file %s' % sys.argv[1])
    except IndexError:
        print('Not enough argument.')
        print('Usage: %s <bayesnet> <enum|elim> <query>' % sys.argv[0])

if __name__=='__main__':
    main()