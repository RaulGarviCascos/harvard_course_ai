import os
import random
import re
import sys



DAMPING = 0.85
SAMPLES = 10000



def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
       


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    '''

--------CORPUS EXAMPLE---------

{'1.html': {'2.html'},
 '2.html': {'1.html', '3.html'},
 '3.html': {'4.html', '2.html'},
 '4.html': {'2.html'}}

'''
    transition_matrix = {}
    linked_pages = corpus[page]
    if linked_pages:
        for current_page in corpus:
            if current_page in corpus[page]:
                transition_matrix[current_page] = damping_factor/len(corpus[page]) + (1-damping_factor)/len(corpus)
            else:
                transition_matrix[current_page] = (1-damping_factor)/len(corpus)
    else:
        for current_page in corpus:
            transition_matrix[current_page] = 1/len(corpus)
    return transition_matrix

  

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_rank_result = {}

    
    page = random.choice(list(corpus.keys()))

    for i in range(n):

        transition_matrix = transition_model(corpus=corpus,page=page,damping_factor=damping_factor)

        next_page = random.choices(

            population=list(transition_matrix.keys()),
            weights=list(transition_matrix.values()),
            k=1
        )[0]

        if next_page in page_rank_result:
            page_rank_result[next_page] +=  1/n
        else:
            page_rank_result[next_page] =  1/n
        
        page = next_page
                

    return page_rank_result

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    def PR(p,page_rank):
        current_pr = 0
       
        for page in corpus:
            links = corpus[page] if corpus[page] else list(corpus)
            if p in links:
                current_pr+=damping_factor*page_rank[page]/len(links)
        current_pr+=(1-damping_factor)/len(corpus)
        return current_pr

    page_rank_result = {}

    for page in corpus:
        page_rank_result[page] = 1/len(corpus)

    min_diff = 0.001
    converged = False
    
    while not converged:
        converged=True
        for page in corpus:
            last_pr = page_rank_result[page]
            new_pr = PR(page,page_rank_result)
            page_rank_result[page]=new_pr
            diff = abs(last_pr-new_pr)
            if diff>min_diff:
                converged=False
        
    
    return page_rank_result

if __name__ == "__main__":
    main()
