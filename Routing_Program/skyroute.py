from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices

stations_under_construction = []

landmark_string = ""
for letter, landmark in landmark_choices.items():
    landmark_string += f"{letter} - {landmark}\n"

def greet():
    print("Hi there and welcome to SkyRoute!")
    print("We'll help you find the shortest route between the following Vancouver landmarks:\n" + landmark_string)

def get_active_stations():
    updated_metro = vc_metro.copy()
    for station_under_construction in stations_under_construction:
        for current_station, neighboring_stations in vc_metro.items():
            if current_station != station_under_construction:
                updated_metro[current_station] -= set(stations_under_construction)
            else:
                updated_metro[current_station] = set([])
    return updated_metro

def get_route(start_point, end_point):
    start_stations = vc_landmarks[start_point]
    end_stations = vc_landmarks[end_point]
    routes = []

    for start_station in start_stations:
        for end_station in end_stations:
            metro_system = get_active_stations() if stations_under_construction else vc_metro

            if stations_under_construction:
                possible_route = dfs(metro_system, start_station, end_station)
                if not possible_route:
                    continue

            route = bfs(metro_system, start_station, end_station)
            if route:
                routes.append(route)

    if routes:
        shortest_route = min(routes, key=len)
        return shortest_route
    return None

def set_start_and_end(start_point, end_point):
    if start_point:
        change_point = input("What would you like to change? Enter 'o' for origin, 'd' for destination, or 'b' for both: ")
        if change_point == "b":
            start_point = get_start()
            end_point = get_end()
        elif change_point == "o":
            start_point = get_start()
        elif change_point == "d":
            end_point = get_end()
        else:
            print("Oops, that isn't 'o', 'd', or 'b'...")
            return set_start_and_end(start_point, end_point)
    else:
        start_point = get_start()
        end_point = get_end()
    return start_point, end_point

def get_start():
    start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
    if start_point_letter in landmark_choices:
        return landmark_choices[start_point_letter]
    else:
        print("Sorry, that's not a landmark we have data on. Let's try again...")
        return get_start()

def get_end():
    end_point_letter = input("Where are you headed? Type in the corresponding letter: ")
    if end_point_letter in landmark_choices:
        return landmark_choices[end_point_letter]
    else:
        print("Sorry, that's not a landmark we have data on. Let's try again...")
        return get_end()

def new_route(start_point=None, end_point=None):
    start_point, end_point = set_start_and_end(start_point, end_point)
    shortest_route = get_route(start_point, end_point)
    if shortest_route:
        shortest_route_string = "\n".join(shortest_route)
        print("The shortest metro route from {0} to {1} is:\n{2}".format(start_point, end_point, shortest_route_string))
    else:
        print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))
    again = input("Would you like to see another route? Enter y/n: ")
    if again == "y":
        show_landmarks()
        new_route(start_point, end_point)

def show_landmarks():
    see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n: ")
    if see_landmarks == "y":
        print(landmark_string)

def goodbye():
    print("Thanks for using SkyRoute!")

def skyroute():
    greet()
    new_route()
    goodbye()

skyroute()
