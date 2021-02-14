'''
Main module
'''

import folium
import geo_helper
import webmap
import reader


def get_movies(path: str, year: int, user_location: tuple, number_of_movies: int) -> list:
    '''
    Get movies filmed in certain year.
    >>> get_movies('locations.list', 2001, (0, 0), 2)
    [['"7 Lives Xposed" (2001) {(#1.2)}', (34.0896518, -118.2693735), 12575.416857244845],\
 ['"24" (2001)', (34.2595715, -118.6023247), 12599.222546846191]]
    '''
    movies = []
    movies = reader.get_movies_by_year(path, year, number_of_movies)

    movies_coordinates = geo_helper.get_movies_coordinates(movies)
    movies_coordinates_with_distance = sorted(geo_helper.get_movies_coordinates_with_distance(
        movies_coordinates, user_location), key=lambda a: a[-1])
    return movies_coordinates_with_distance


def set_up_map(movies_coordinates_with_distance: list, year: int, user_location: tuple):
    '''
    Set up HTML map.
    '''
    folium_map = webmap.create_map(user_location)
    closest_markers = webmap.create_group('Closest markers')
    all_markers = webmap.create_group('Other markers', show=False)
    user_location_marker = webmap.create_group('Your location')

    webmap.place_markers(
        closest_markers, movies_coordinates_with_distance[:10], color='darkpurple')
    webmap.place_markers(
        all_markers, movies_coordinates_with_distance[10:])
    webmap.create_mark(user_location_marker, 'You are here',
                       user_location, color='green')

    folium_map.add_child(all_markers)
    folium_map.add_child(closest_markers)
    folium_map.add_child(user_location_marker)
    folium_map.add_child(folium.LayerControl())

    webmap.save_map(folium_map, f'{year}_movies_map.html')


def main():
    '''
    Execute program.
    '''
    year = ''
    user_location = ''

    # Get user input
    while True:
        try:
            if year == '':
                year = int(input(
                    'Please enter a year you would like to have a map for: '))
                if int(year) not in range(1900, 2021):
                    year = ''
                    raise ValueError

            user_location = input(
                'Please enter your location (format: lat, long): ')
            user_location = [float(i) for i in user_location.split(',')]
            if len(user_location) != 2:
                raise ValueError

            break
        except ValueError:
            print('Wrong input. Try again.')
            continue

    # Find movies locations and generate map
    print('Finding locations...\nPlease wait...')
    movies = get_movies('locations.list', year, user_location, 100)
    print('Generating map...')
    set_up_map(movies, year, user_location)
    print(f'Finished. Open {year}_movies_map.html to see the results')


if __name__ == '__main__':
    main()
