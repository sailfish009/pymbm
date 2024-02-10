"""
additional information
"""

from duckduckgo_search import DDGS

def search(keyword):
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(f'{keyword}', max_results=5)]
        return results