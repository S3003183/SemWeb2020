from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff
import SPARQL

"""
g1 = Graph().parse(format='n3', data='''
         @prefix : <http://example.org/ns#> .
         <http://example.org> :rel
             <http://example.org/same>,
             [ :label "Same" ],
             <http://example.org/a>,
             [ :label "A" ] .
     ''')
g2 = Graph().parse(format='n3', data='''
         @prefix : <http://example.org/ns#> .
         <http://example.org> :rel
             <http://example.org/same>,
             [ :label "Same" ],
             <http://example.org/b>,
             [ :label "B" ] .
     ''')
 """
g1 = SPARQL.RDF_parser("http://purl.org/ontology/mo/MusicGroup", False)
g2 = SPARQL.RDF_parser("http://purl.org/ontology/mo/MusicGroup", False)

iso1 = to_isomorphic(g1)
iso2 = to_isomorphic(g2)

print(iso1 == iso2)

in_both, in_first, in_second = graph_diff(iso1, iso2)


def dump_nt_sorted(g):
    for l in sorted(g.serialize(format='nt').splitlines()):
        if l:
            print(l.decode('ascii'))


dump_nt_sorted(in_both)  # doctest: +SKIP

dump_nt_sorted(in_first)  # doctest: +SKIP

dump_nt_sorted(in_second)  # doctest: +SKIP

print("\n____________________________IN BOTH______________________________\n")
print(in_both.serialize(format="n3"))
print("\n____________________________IN FIRST______________________________\n")
print(in_first.serialize(format="n3"))
print("\n____________________________IN "
      "SECOND______________________________\n")
print(in_second.serialize(format="n3"))
