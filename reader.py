'''
Module for helping with reading files.
'''


def read_data(path: str, starting_index=0):
    r'''
    Read lines from file starting from starting_index.

    >>> next(read_data('locations.list', 14))
    '"#1 Single" (2006)\t\t\t\t\tLos Angeles, California, USA'
    >>> next(read_data('locations.list', 1061298))
    'Star Wars: Episode V - The Empire Strikes Back (1980)\tHardangerj�kulen Glacier, Finse, Norway'
    '''
    with open(path, 'r', errors='replace') as lines:
        for i, line in enumerate(lines):
            if i < starting_index:
                continue

            yield line.strip()


def split_line(line: str, sep='\t') -> list:
    '''
    Split line and remove empty strings from splitted list.

    >>> split_line('"Gossip Girl" (2007)					Brooklyn, New York City, New York, USA', sep='\t')
    ['"Gossip Girl" (2007)', 'Brooklyn, New York City, New York, USA']
    '''
    splitted_line = [i for i in line.split(sep) if i != '']
    return splitted_line


def read_movies_without_duplicates(path: str):
    '''
    Read movies from file with unique names and filming locations.

    >>> next(read_movies_without_duplicates('locations.list'))
    ['"#1 Single" (2006)', 'Los Angeles, California, USA']
    '''
    titles = []
    locations = []
    for movie in read_data(path, 14):
        movie = split_line(movie)
        title = movie[0].split(' {')[0]
        location = movie[1]

        if title in titles or location in locations:
            continue

        titles.append(title)
        locations.append(location)
        yield [movie[0], location]


def get_movies_by_year(path: str, year: int, number_of_movies: int) -> list:
    '''
    Get movies filmed in a certain year from file.

    >>> get_movies_by_year('locations.list', 2020, 2)
    [['"2020 Summer Olympics" (2020)', 'Tokyo, Japan'],\
 ['"2020 Summer Paralympics" (2020)', 'Tokyo, Japan']]
    >>> get_movies_by_year('locations.list', 2010, 2)
    [['"$#*! My Dad Says" (2010)',\
 'Warner Brothers Burbank Studios - 4000 Warner Boulevard, Burbank, California, USA'],\
 ['"1 Non Blonde" (2010)', 'New Zealand']]
    '''
    movies = []
    if year not in range(1950, 2019):
        for movie in read_data(path, 14):
            if f'({year})' in movie:
                movies.append(split_line(movie))
            if len(movies) == number_of_movies:
                break
    else:
        for movie in read_movies_without_duplicates(path):
            if f'({year})' in movie[0]:
                movies.append(movie)
            if len(movies) == number_of_movies:
                break

    return movies
