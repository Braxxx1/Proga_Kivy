
import sqlite3 as sq
import json as js


#копирование информации из Airport.db в Application.db
def copying_information(airport_id):
    connection = sq.connect('BD\\Airport.db')
    cursor = connection.cursor()

    #чтение информации: связки аэропорт-город-страна
    cursor.execute('SELECT id_airport, name_airport, name_city, name_country\
                    FROM Countries \
                    join Cities on Countries.id_country = Cities.country_id \
                    join Airports on Cities.id_city = Airports.city_id')
    airports = cursor.fetchall()
    #чтение информации: выходы
    cursor.execute('SELECT id_num_gate, num_floor FROM Gates')
    gates = cursor.fetchall()
    #чтение информации: связка рейс-посадочный-пассажир
    cursor.execute('SELECT id_num_flight, airport_from_id, airport_to_id, time_from, time_to, num_gate_id, id_num_boarding, num_passport, surname, given_names, date_birth, num_seat\
                    FROM Flights\
                    JOIN Boarding_passes on Flights.id_num_flight = Boarding_passes.num_flight_id\
                    JOIN Passengers on Boarding_passes.passenger_id = Passengers.id_passenger ')
    passengers_on_flights = cursor.fetchall()
    
    #обработка при чтении: связки аэропорт-город-страна при чтении
    airports_list = []
    for airport in airports:
        airport_dict = {
            'id_airport': airport[0],
            'name_airport': airport[1],
            'name_city': airport[2],
            'name_country': airport[3]
        }
        airports_list.append(airport_dict)
    #обработка при чтении: выходы
    gates_list = []
    for gate in gates:
        gate_dict = {
            'id_num_gate': gate[0],
            'num_floor': gate[1]
        }
        gates_list.append(gate_dict)
    #обработка при чтении: связка рейс-посадочный-пассажир
    passengers_on_flights_list = []
    for passenger in  passengers_on_flights:
        passenger_dict = {
            'id_num_flight': passenger[0],
            'airport_from_id': passenger[1],
            'airport_to_id': passenger[2],
            'time_from': passenger[3],
            'time_to': passenger[4],
            'num_gate_id': passenger[5],
            'id_num_boarding': passenger[6],
            'num_passport': passenger[7],
            'surname': passenger[8],
            'given_names': passenger[9],
            'date_birth': passenger[10],
            'num_seat': passenger[11]
        }
        passengers_on_flights_list.append(passenger_dict)

    connection.close()


    connection = sq.connect('BD\\Application.db')
    cursor = connection.cursor()

    #чтение информации при записи: связка аэропорт-город-страна
    cursor.execute('SELECT id_airport FROM Airports')
    airports = cursor.fetchall()
    cursor.execute('SELECT id_city, name_city FROM Cities')
    cities = cursor.fetchall()
    cursor.execute('SELECT id_country, name_country FROM Countries')
    countries = cursor.fetchall()
    cursor.execute('SELECT MAX(id_city) FROM Cities')
    max_id_city = cursor.fetchone()[0] + 1
    cursor.execute('SELECT MAX(id_country) FROM Countries')
    max_id_country = cursor.fetchone()[0] + 1
    #чтение информации при записи: выходы
    cursor.execute('SELECT name_point FROM Points_routes WHERE airport_id = (?)', [airport_id])
    points_routes = cursor.fetchall()
    cursor.execute('SELECT MAX(id_point) FROM Points_routes')
    max_id_point = cursor.fetchone()[0] + 1

    #обработка при записи: связка аэропорт-город-страна
    id_airports_app_list = []
    for airport in airports:
        id_airports_app_list.append(airport[0])
    cities_dict ={}
    for city in cities:
        cities_dict[city[1]] = city[0]
    countries_dict ={}
    for country in countries:
        countries_dict[country[1]] = country[0]
    #обработка при записи: выходы
    points_list = []
    for point in points_routes:
        points_list.append(point[0])

    #запись: связки аэропорт-город-страна
    for airport in airports_list:
        if airport.get('id_airport') not in id_airports_app_list:
            if cities_dict.get(airport.get('name_city'), 0) == 0:
                if countries_dict.get(airport.get('name_country'), 0) == 0:
                    #записать в бд аэропорт, город, страну
                    cursor.execute('INSERT INTO Countries(id_country, name_country) VALUES(?, ?)',\
                                    (max_id_country, airport.get('name_country')))
                    cursor.execute('INSERT INTO Cities(id_city, name_city, country_id) VALUES(?, ?, ?)',\
                                    (max_id_city, airport.get('name_city'), max_id_country))
                    cursor.execute('INSERT INTO Airports(id_airport, name_airport, city_id) VALUES(?, ?, ?)',\
                                    (airport.get('id_airport'), airport.get('name_airport'), max_id_city))
                    max_id_city += 1
                    max_id_country += 1
                else:
                    #записать в бд аэропорт и город
                    cursor.execute('INSERT INTO Cities(id_city, name_city, country_id) VALUES(?, ?, ?)',\
                                    (max_id_city, airport.get('name_city'), countries_dict.get(airport.get('name_country'))))
                    cursor.execute('INSERT INTO Airports(id_airport, name_airport, city_id) VALUES(?, ?, ?)',\
                                    (airport.get('id_airport'), airport.get('name_airport'), max_id_city))
                    max_id_city += 1
            else:
                #записать в бд аэропорт
                cursor.execute('INSERT INTO Airports(id_airport, name_airport, city_id) VALUES(?, ?, ?)',\
                                (airport.get('id_airport'), airport.get('name_airport'), cities_dict.get(airport.get('name_city'))))   
    #запись: выходы
    for gate in gates_list:
        if gate.get('id_num_gate') not in points_list:
            #записать в бд новый выход
            cursor.execute('INSERT INTO Points_routes(id_point, name_point, num_floor, if_gate, airport_id) VALUES(?, ?, ?, ?, ?)',\
                            (max_id_point, gate.get('id_num_gate'), gate.get('num_floor'), int(1), airport_id))
            max_id_point += 1
    
    connection.commit()

    #чтение информации при записи: связка рейс-посадочный-пассажир
    cursor.execute('SELECT id_num_flight FROM Flights')
    nums_flights = cursor.fetchall()
    cursor.execute('SELECT id_num_boarding FROM Boarding_passes')
    nums_boarding = cursor.fetchall()
    cursor.execute('SELECT num_passport FROM Passengers')
    nums_passports = cursor.fetchall()
    cursor.execute('SELECT id_point, name_point FROM Points_routes WHERE (if_gate = 1) and (airport_id = (?))', [airport_id])
    gates = cursor.fetchall()
    cursor.execute('SELECT id_passenger, num_passport FROM Passengers')
    passengers = cursor.fetchall()
    cursor.execute('SELECT MAX(id_passenger) FROM Passengers')
    max_id_passenger = cursor.fetchone()[0] + 1

    #обработка при записи: связка рейс-посадочный-пассажир
    nums_flights_list = []
    for num_flight in nums_flights:
        nums_flights_list.append(num_flight[0])
    nums_boarding_list = []
    for num_boarding in nums_boarding:
        nums_boarding_list.append(num_boarding[0])
    nums_passports_list = []
    for num_passport in nums_passports:
        nums_passports_list.append(num_passport[0])
    gates_dict = {}
    for gate in gates:
        gates_dict[gate[1]] = gate[0]
    passengers_dict = {}
    for passenger in passengers:
        passengers_dict[passenger[1]] = passenger[0]

    #запись: связка рейс-посадочный-пассажир
    for passenger in passengers_on_flights_list:
        if passenger.get('id_num_flight') not in nums_flights_list:
            #записать в бд новый рейс
            cursor.execute('INSERT INTO Flights(id_num_flight, airport_from_id, airport_to_id, time_from, time_to, point_gate_id) VALUES(?, ?, ?, ?, ?, ?)', \
                           (passenger.get('id_num_flight'), passenger.get('airport_from_id'), passenger.get('airport_to_id'), passenger.get('time_from'), passenger.get('time_to'), gates_dict.get(passenger.get('num_gate_id'))))
        if passenger.get('id_num_boarding') not in nums_boarding_list:
            if passenger.get('num_passport') not in nums_passports_list:
                #записать в бд пассажира и его посадочный
                cursor.execute('INSERT INTO Passengers(id_passenger, num_passport, surname, given_names, date_birth) VALUES(?, ?, ?, ?, ?)', \
                            (max_id_passenger, passenger.get('num_passport'), passenger.get('surname'), passenger.get('given_names'), passenger.get('date_birth')))
                cursor.execute('INSERT INTO Boarding_passes(id_num_boarding, num_flight_id, passenger_id, current_point_id, num_seat) VALUES(?, ?, ?, ?, ?)', \
                            (passenger.get('id_num_boarding'), passenger.get('id_num_flight'), max_id_passenger, 0, passenger.get('num_seat')))
                max_id_passenger += 1
            else:
                #записать в бд посадочный талон
                cursor.execute('INSERT INTO Boarding_passes(id_num_boarding, num_flight_id, passenger_id, current_point_id, num_seat) VALUES(?, ?, ?, ?, ?)', \
                            (passenger.get('id_num_boarding'), passenger.get('id_num_flight'), passengers_dict.get(passenger.get('num_passport')), 0, passenger.get('num_seat')))
    
    connection.commit()
    connection.close()   
    print('Сopy has been completed') 


def get_info_about_boarding_pass(id_num_boarding):
    connection = sq.connect('BD\\Application.db')
    cursor = connection.cursor()

    cursor.execute('''
                    SELECT id_num_boarding, num_seat,
                           num_passport, surname, given_names, date_birth, 
                           id_num_flight, airport_from_id, airport_to_id, time_from, time_to,
                           (SELECT name_airport
                            FROM Airports
                            JOIN Flights ON Airports.id_airport = Flights.airport_from_id
                            JOIN Boarding_passes ON Flights.id_num_flight = Boarding_passes.num_flight_id
                            WHERE id_num_boarding = ?) as airport_from,
                           (SELECT name_city
                            FROM Cities
                            JOIN Airports ON Cities.id_city = Airports.city_id
                            JOIN Flights ON Airports.id_airport = Flights.airport_from_id
                            JOIN Boarding_passes ON Flights.id_num_flight = Boarding_passes.num_flight_id
                            WHERE id_num_boarding = ?) as cities_from,
                           (SELECT name_country
                            FROM Countries
                            JOIN Cities ON Countries.id_country = Cities.country_id
                            JOIN Airports ON Cities.id_city = Airports.city_id
                            JOIN Flights ON Airports.id_airport = Flights.airport_from_id
                            JOIN Boarding_passes ON Flights.id_num_flight = Boarding_passes.num_flight_id
                            WHERE id_num_boarding = ?) as country_from,
                           (SELECT name_airport
                            FROM Airports
                            JOIN Flights ON Airports.id_airport = Flights.airport_to_id
                            JOIN Boarding_passes ON Flights.id_num_flight = Boarding_passes.num_flight_id
                            WHERE id_num_boarding = ?) as airport_to,
                           (SELECT name_city
                            FROM Cities
                            JOIN Airports ON Cities.id_city = Airports.city_id
                            JOIN Flights ON Airports.id_airport = Flights.airport_to_id
                            JOIN Boarding_passes ON Flights.id_num_flight = Boarding_passes.num_flight_id
                            WHERE id_num_boarding = ?) as cities_to,
                           (SELECT name_country
                            FROM Countries
                            JOIN Cities ON Countries.id_country = Cities.country_id
                            JOIN Airports ON Cities.id_city = Airports.city_id
                            JOIN Flights ON Airports.id_airport = Flights.airport_to_id
                            JOIN Boarding_passes ON Flights.id_num_flight = Boarding_passes.num_flight_id
                            WHERE id_num_boarding = ?) as country_to,
                           (SELECT name_point
                            FROM Points_routes
                            JOIN Flights ON Points_routes.id_point = Flights.point_gate_id
                            JOIN Boarding_passes ON Flights.id_num_flight = Boarding_passes.num_flight_id
                            WHERE id_num_boarding = ?) as gate_boarding
                    FROM Passengers
                    JOIN Boarding_passes ON Passengers.id_passenger = Boarding_passes.passenger_id
                    JOIN Flights ON Boarding_passes.num_flight_id = Flights.id_num_flight
                    WHERE id_num_boarding = ?
                   ''', (id_num_boarding, id_num_boarding, id_num_boarding, id_num_boarding, id_num_boarding, id_num_boarding, id_num_boarding, id_num_boarding))
    boarding_info = cursor.fetchone()
    
    boarding_info_dict = {
        'num_boarding': boarding_info[0],
        str(boarding_info[0]): {
            'num_passport': boarding_info[2],
            'surname': boarding_info[3],
            'given_names': boarding_info[4],
            'date_birth': boarding_info[5],
            'num_flight': boarding_info[6],
            'num_seat': boarding_info[1],
            'airport_from': boarding_info[7],
            'name_airport_from': boarding_info[11],
            'name_city_from': boarding_info[12],
            'name_country_from': boarding_info[13],
            'time_from': boarding_info[9],
            'airport_to': boarding_info[8],
            'name_airport_to': boarding_info[14],
            'name_city_to': boarding_info[15],
            'name_country_to': boarding_info[16],
            'time_to': boarding_info[10],
            'gate': boarding_info[17]
        }
    }

    with open ('BD\\Files\\boarding.json', 'w') as f:
        f.write(js.dumps(boarding_info_dict, indent=4))
    connection.close()
    return boarding_info_dict
    


def get_all_points():
    connection = sq.connect('BD\\Application.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id_airport, name_airport, name_city\
                    FROM Airports JOIN Cities ON Airports.city_id = Cities.id_city')
    airports = cursor.fetchall()

    airports_list = []
    for airport in airports:
        airports_list.append(airport[0]) 
    
    points_dict = {}
    for airport in airports_list:
        cursor.execute('SELECT distinct num_floor\
                        FROM Points_routes\
                        WHERE airport_id = ? and id_point != 0', [airport])
        gates_dict = {}
        other_points_dict = {}
        nums_floors = cursor.fetchall()
        for num_floor in nums_floors:
            cursor.execute('SELECT id_point, name_point, if_gate\
                            FROM Points_routes\
                            WHERE airport_id = ? and id_point != 0 and num_floor = ?', [airport, num_floor[0]])
            points = cursor.fetchall()
            gates_list = []
            other_points_list = []
            if len(points) != 0:
                for point in points:
                    if point[2] == 1:
                        gate_dict = {
                            'id_point': point[0],
                            'name_point': point[1],
                        }
                        gates_list.append(gate_dict)
                    elif point[2] == 0:
                        other_point_dict = {
                            'id_point': point[0],
                            'name_point': point[1],

                        }
                        other_points_list.append(other_point_dict)
            gates_dict[num_floor[0]] = gates_list
            other_points_dict[num_floor[0]] = other_points_list
        points_dict[airport] = {
            'gates': gates_dict,
            'other_points': other_points_dict
        }
    
    with open ('BD\\Files\\all_points.json', 'w') as f:
        f.write(js.dumps(points_dict, indent=4))
    
    connection.close()


def get_points_airport(airport_id):
    connection = sq.connect('BD\\Application.db')
    cursor = connection.cursor()

    cursor.execute('SELECT distinct num_floor\
                        FROM Points_routes\
                        WHERE airport_id = ? and id_point != 0', [airport_id])
    nums_floors = cursor.fetchall()
    
    gates_dict = {}
    other_points_dict = {}
    for num_floor in nums_floors:
        cursor.execute('SELECT id_point, coordinates, if_gate\
                            FROM Points_routes\
                            WHERE airport_id = ? and id_point != 0 and num_floor = ?', [airport_id, num_floor[0]])
        points = cursor.fetchall()
        gates_list = []
        other_points_list = []
        if len(points) != 0:
            for point in points:
                if point[2] == 1:
                    x, y = point[1].split()
                    gate_dict = {
                        'id_point': point[0],
                        'x': x,
                        'y': y
                    }
                    gates_list.append(gate_dict)
                elif point[2] == 0:
                    x, y = point[1].split()
                    other_point_dict = {
                        'id_point': point[0],
                        'x': x,
                        'y': y,
                    }
                    other_points_list.append(other_point_dict)
        gates_dict[num_floor[0]] = gates_list
        other_points_dict[num_floor[0]] = other_points_list
    points_dict = {
        'gates': gates_dict,
        'other_points': other_points_dict
    }
    
    with open ('BD\\Files\\points.json', 'w') as f:
        f.write(js.dumps(points_dict, indent=4))
    
    connection.close()


copying_information('DME')
get_info_about_boarding_pass('1111111111')
# get_all_points()
get_points_airport('SVO')