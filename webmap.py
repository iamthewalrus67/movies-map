'''
Module for working with HTML maps
'''

import folium


def place_markers(folium_map, locations: tuple, color='blue'):
    '''
    Place multiple markers on map.
    '''
    for location in locations:
        create_mark(folium_map, location[0], location[1], color=color)


def create_mark(folium_map, name, location: tuple, color='blue'):
    '''
    Place one mark on map.
    '''
    if location == (0, 0):
        return
    folium_map.add_child(folium.Marker(
        location=location, popup=name, icon=folium.Icon(color=color)))


def create_map(location: tuple) -> folium.Map:
    '''
    Create new folium map.
    '''
    folium_map = folium.Map(location=location, zoom_start=4)
    return folium_map


def create_group(name: str, show=True):
    '''
    Create new feature group.
    '''
    feature_group = folium.FeatureGroup(name=name, show=show)
    return feature_group


def save_map(folium_map, path: str):
    '''
    Save map to file.
    '''
    folium_map.save(path)
