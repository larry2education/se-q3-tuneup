#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Larry Scott with help from John and Peter"

import cProfile
import pstats
import functools
import timeit


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    def inner(*args, **kwargs):
        my_profiler = cProfile.Profile()
        my_profiler.enable()
        results = func(*args, **kwargs)
        my_profiler.disable()
        stat = pstats.Stats(my_profiler).sort_stats("cumulative")
        stat.print_stats(10)
        return results
    return inner    


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates

def optimized_find_duplicate_movies(src):
    """Returns an optimized list of duplicate movies from a src list."""
    movies = read_movies(src)
    all_movies = {}
    duplicates = []
    for movie in movies:
        if movie not in all_movies:
            all_movies[movie] = 1
        else:
            all_movies[movie] += 1
            duplicates.append(movie)
    return duplicates


def timeit_helper(func_name, func_param):
    """Part A: Obtain some profiling measurements using timeit"""
    assert isinstance(func_name, str)
    stmt = f"{func_name}('{func_param}')"
    setup = f"from {__name__} import {func_name}"
    t = timeit.Timer(stmt=stmt, setup=setup)
    runs_per_repeat = 3
    num_repeats = 5
    result = t.repeat(repeat=num_repeats, number=runs_per_repeat)
    time_cost = min(result)/num_repeats
    print(f"""func={func_name} num_repeats={num_repeats} 
    runs_per_repeat={runs_per_repeat} time_cost={time_cost:.3f} sec""")
    return t


def main():
    """Computes a list of duplicate movie entries."""

    filename = 'movies.txt'

    print("--- Before optimization ---")
    result = find_duplicate_movies(filename)
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))

    print("\n--- Timeit results, before optimization ---")
    timeit_helper('find_duplicate_movies', filename)

    print("--- After optimization ---")
    result = optimized_find_duplicate_movies(filename)
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))

    print("\n--- Timeit results, after optimization ---")
    timeit_helper('optimized_find_duplicate_movies', filename)

    print("\n--- cProfile results, before optimization ---")
    profile(find_duplicate_movies)(filename)
    
    print("\n--- cProfile results, after optimization ---")
    profile(optimized_find_duplicate_movies)(filename)

if __name__ == '__main__':
    main()
    print("Completed.")
