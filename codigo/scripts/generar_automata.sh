#!/bin/sh
[ -f parser.out ] || echo "Tenés que generar el parser.out con la info de debug"
awk -f scripts/generar_graphviz.awk < parser.out | dot -Tpdf > automata.pdf
