# Analysis

I made the analysis with the sentence "She drives the [MASK] on the road."

## Layer 1, Head 12

In this head, we can see that almost every word pays attention to the [MASK] token. Although it's not fully highlighted, this head shows the most focus on the masked word, suggesting that it plays a key role in contextual prediction.

## Layer 4, Head 10

In this head, the word "drives" pays attention to the determiner "the" and the [MASK] token. Since "drives" is the verb directly related to the masked word, this attention head may be focusing on verb-object relationships.

**Example Sentences:**
- She drives the [MASK] on the road.  
  -> She drives the **car** on the road.  
  -> She drives the **truck** on the road.  
  -> She drives the **van** on the road.

  This analysis shows how different attention heads focus on various grammatical relationships, such as verb-object or overall sentence context, when predicting masked words.

---

- John gave Mary a book, and she read the [MASK].  
  -> John gave Mary a book, and she read the **rest**.  
  -> John gave Mary a book, and she read the **words**.  
  -> John gave Mary a book, and she read the **title**.


    In this example, I tried to analyze the relation between the pronoun "she" and its antecedent "Mary", as well as the connection between the object "book" and the masked word.
