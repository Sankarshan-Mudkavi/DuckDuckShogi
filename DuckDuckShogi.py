"""This code works for single word queries and multi-word queries, however it does not rank multiword queries, yet"""

#Returns urls for multi-word queries
def multi_lookup(index, query):
    urls = []
    if (len(query) != 0):
        decision = lookup(index, query[0])
        if(decision == None):
            return []
        for i in range(1, len(query)):
            descrip = lookup(index, query[i])
            if(descrip == None):
                return []
            decision = check_same(decision, descrip)
        for i in range(len(decision)):
            if decision[i][0] not in urls:
                urls.append(decision[i][0])
    return urls

#Used to see if words are beside each other in the URL
def check_same(s, t):
    exist = []
    for descrip1 in s:
        for descrip2 in t:
            if (descrip1[0] == descrip2[0]) and ((descrip2[1] - descrip1[1]) == 1):
                exist.append(descrip2)
    return exist

#Returns ranked urls
def ordered_search(index, ranks, keyword):
    if keyword in index:
        return sort_quick(index[keyword], ranks)
    return None

#Quick sort impelementation
def sort_quick(url_list, p_rank):
    if len(url_list) <= 1:
        return url_list
    else:
        piv = url_list[0]
        less = []
        great = []
        for url in range(1, len(url_list)):
            if p_rank[url_list[url]] <= p_rank[piv]:
                less.append(url_list[url])
            else:
                great.append(url_list[url])
        return combine(sort_quick(great, p_rank), piv, sort_quick(less, p_rank))

def combine(a,b, c):
    a.append(b)
    for e in c:
        a.append(e)
    return a

#webcrawler
def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = set([seed])
    crawled = set()
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            tocrawl.update(outlinks)
            crawled.update(page)
    return index, graph

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

#Used sets(update) to perform unions instead
"""def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)"""

def add_page_to_index(index, url, content):
    words = content.split()
    for i in range(len(words)):
        add_to_index(index, words[i], i, url)

def add_to_index(index, keyword, pos, url):
    if keyword in index:
        index[keyword].append([url, pos])
    else:
        index[keyword] = [[url, pos]]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

#Implementation of page-rank
def compute_ranks(graph):    
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

"""Cache provided by Udacity"""
cache = {
   'http://www.udacity.com/cs101x/final/multi.html': """<html>
<body>

<a href="http://www.udacity.com/cs101x/final/a.html">A</a><br>
<a href="http://www.udacity.com/cs101x/final/b.html">B</a><br>

</body>
""", 
   'http://www.udacity.com/cs101x/final/b.html': """<html>
<body>

Monty likes the Python programming language
Thomas Jefferson founded the University of Virginia
When Mandela was in London, he visited Nelson's Column.

</body>
</html>
""", 
   'http://www.udacity.com/cs101x/final/a.html': """<html>
<body>

Monty Python is not about a programming language
Udacity was not founded by Thomas Jefferson
Nelson Mandela said "Education is the most powerful weapon which you can
use to change the world."
</body>
</html>
""", 
}

def get_page(url):
    if url in cache:
        return cache[url]
    else:
        print "Page not in cache: " + url
        return None