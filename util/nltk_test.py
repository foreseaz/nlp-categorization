from nltk.corpus import wordnet

synsets = wordnet.synsets('cake')

for synset in synsets:
  print '-' * 10
  print "Name:", synset.name
  print "Lexical Type:", synset.lexname
  print "Definition:", synset.definition
  # for example in synset.examples:
  #   print "Example:", example
