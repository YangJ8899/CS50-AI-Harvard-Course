import os
import random
import re
import sys
from collections import defaultdict

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
    
    pages = defaultdict(int)

    # base case: no outgoing links, choose at random from all pages in corpus
    if len(corpus[page]) == 0:
        for n in corpus:
            pages[n] = 1 / len(corpus)
        
        return pages

    # Now we look at damping_factor and 1 - damping_factor
    random = (1 - damping_factor) / len(corpus)
    random_link = damping_factor / len(corpus[page])

    # for all pages we add the "1 - damping_factor" probability
    for n in corpus:
        pages[n] += random
        # if that page is linked to our current, we add the damping_factor probability
        if n in corpus[page]:
            pages[n] += random_link

    return pages


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = defaultdict(int)

    # To start, choose a random page from the corpus
    page = random.choice(list(corpus.keys()))

    for _ in range(n):
        # run the transition model on our chosen page
        new_page = transition_model(corpus, page, damping_factor)

        # choose the next page based on the previous transition model
        page = random.choices(list(new_page.keys()), list(new_page.values()), k=1)[0]

        # Now we increment the probability that it was chosen by 1/n (chosen out of n options in the sample)
        samples[page] += 1/n
    
    return samples


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = defaultdict(lambda: 1/len(corpus))
    prev = defaultdict(int)

    # populate our first dict
    for page in corpus:
        prev[page] = 1/len(corpus)

    while True:
        for page in corpus:
            sum = 0
            for other in corpus:
                # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                if len(corpus[other]) == 0:
                    sum += page_rank[other] / len(corpus)
                
                # check to see if page is linked, if it is, update our sum value accordingly
                if other != page and page in corpus[other]:
                    sum += page_rank[other] / len(corpus[other])

            # Calculate the iterative function
            pr = ((1 - damping_factor) / len(corpus)) + damping_factor * sum

            page_rank[page] = pr
        
        if max([abs(page_rank[i] - prev[i]) for i in prev.keys()]) < 0.001:
            break

        prev = page_rank.copy()
    
    return page_rank
            

if __name__ == "__main__":
    main()
