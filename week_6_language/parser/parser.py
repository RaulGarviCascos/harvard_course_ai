import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
AdjP -> Adj | Adj AdjP
AdvP -> Adv | Adv AdvP | Adv AdjP
NP -> N | Det NP | AdjP NP | N PP | AdvP NP | NP Conj NP 
PP -> P NP
VP -> V | V NP | NP V | V NP PP |VP Conj VP | VP PP | AdvP VP | VP AdvP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")
    
    # Convert input into list of words
    s = preprocess(s)
    
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return
    
    
    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
        
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))
        
       
   
def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence_list = nltk.word_tokenize(sentence)
    sentence_list = [word.lower() for word in sentence_list if word.isalpha()]
    return sentence_list



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunk_list = []
    for element in tree:
        for sub in element.subtrees():
            if sub.label() == "NP":
                has_inner_np = any(
                    subtree for subtree in sub.subtrees(filter=lambda t: t != sub and t.label() == "NP")
                )
                if not has_inner_np:
                    np_chunk_list.append(sub)

                    
    return np_chunk_list

if __name__ == "__main__":

    main()

    