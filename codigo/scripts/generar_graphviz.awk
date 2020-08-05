BEGIN {
  print "digraph G {"
  print "node [shape=rectangle]"
  started = 0
}

/^state 0$/ { started = 1 }

/^state [0-9]+/ {
  current_state = "state"$2
  printf current_state" [label=\""$2"\\l----\\l"
  parsing_state=0
}

/^$/ {
  if (started && parsing_state == 1)
    print "\"]"
  parsing_state++
}

{
  if (started && parsing_state == 1 && $0 != "")
    printf $0"\\l"
}

/[$A-Za-z_]+ +shift and go to state/ {
  print current_state" -> state"$7" [label=\""$1"\"]"
}

END { print "}" }
