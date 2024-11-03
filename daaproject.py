# import heapq
# from collections import defaultdict

# # Graph representation using adjacency list
# class Graph:
#     def __init__(self):
#         # Use a dictionary where each key is a city (vertex) and the value is a list of tuples (neighboring city, road distance)
#         self.graph = defaultdict(list)

#     def add_edge(self, city1, city2, road_distance):
#         # Since it's an undirected graph, add roads in both directions (city1 -> city2 and city2 -> city1)
#         self.graph[city1].append((city2, road_distance))
#         self.graph[city2].append((city1, road_distance))

#     def prim_mst(self):
#         # Prim's algorithm to find the Minimum Spanning Tree (MST)
#         mst = []  # To store the MST result
#         visited = set()  # To track the visited cities
#         min_heap = [(0, 0)]  # Start with city 0 and road distance 0 in the priority queue (min-heap)

#         print("\nOptimizing City Road Network using Prim's Algorithm for MST:")
#         print("================================================================")
        
#         total_road_length = 0  # To keep track of the total road distance in the MST
        
#         while min_heap:
#             # Get the city with the minimum road distance
#             road_distance, city = heapq.heappop(min_heap)
            
#             # If the city is already visited, skip it
#             if city in visited:
#                 continue
            
#             # Mark this city as visited
#             visited.add(city)
#             # Append the city and its road distance to the MST result
#             mst.append((city, road_distance))
#             total_road_length += road_distance

#             print(f"Connecting city {city} with road length {road_distance} to the network")

#             # Explore its neighboring cities
#             for neighbor, distance in self.graph[city]:
#                 if neighbor not in visited:
#                     # Push the neighboring city and its road distance into the min-heap
#                     heapq.heappush(min_heap, (distance, neighbor))
#                     print(f"Evaluating road between city {city} and city {neighbor} with length {distance}")
        
#         print("\nRoad Network Optimization complete!")
#         print(f"Total road length to connect all cities: {total_road_length}")
#         return mst

#     def dijkstra(self, start):
#         # Dijkstra's algorithm to find the shortest paths from a starting city
#         distances = {city: float('inf') for city in self.graph}  # Initialize distances to infinity
#         distances[start] = 0  # Distance to the start city is 0
#         pq = [(0, start)]  # Priority queue (min-heap) initialized with start city
        
#         print(f"\nFinding Shortest Routes from City {start} using Dijkstra's Algorithm:")
#         print("===================================================================")
        
#         while pq:
#             # Pop the city with the smallest distance
#             current_distance, current_city = heapq.heappop(pq)

#             # Skip if we've already found a shorter path
#             if current_distance > distances[current_city]:
#                 continue

#             print(f"Exploring city {current_city} with current shortest distance {current_distance}")

#             # Check all neighboring cities
#             for neighbor, road_distance in self.graph[current_city]:
#                 # Calculate the new distance
#                 new_distance = current_distance + road_distance

#                 # If the new distance is smaller, update the shortest path
#                 if new_distance < distances[neighbor]:
#                     distances[neighbor] = new_distance
#                     heapq.heappush(pq, (new_distance, neighbor))
#                     print(f"Updated shortest distance to city {neighbor}: {new_distance}")
        
#         print("\nShortest route calculation complete!")
#         return distances

# # Example to test
# g = Graph()
# # Adding roads between cities (city1, city2, road_distance)
# g.add_edge(0, 1, 4)
# g.add_edge(0, 7, 8)
# g.add_edge(1, 2, 8)
# g.add_edge(1, 7, 11)
# g.add_edge(2, 3, 7)

# # Print the road network structure for better understanding
# print("City Road Network Structure (Adjacency List):")
# for city, roads in g.graph.items():
#     print(f"City {city}: Roads {roads}")

# # Minimum Spanning Tree (MST) for road network optimization using Prim’s Algorithm
# mst_result = g.prim_mst()
# print("\nOptimized Road Network (MST):")
# for city, road_length in mst_result:
#     print(f"City {city} connected with road length {road_length}")

# # Shortest path from city 0 using Dijkstra's Algorithm
# dijkstra_result = g.dijkstra(0)
# print("\nShortest Routes from City 0:")
# for city, distance in dijkstra_result.items():
#     print(f"City {city}: Shortest distance {distance}")

# from flask import Flask, render_template, request

# app = Flask(__name__)

# # ... (rest of your code from the previous response)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/find_shortest_path", methods=["POST"])
# def find_shortest_path():
#     start_city = request.form["start_city"]
#     # ... (rest of your code to find the shortest path using Dijkstra's algorithm)
#     return render_template("result.html", shortest_paths=mst_result)

# if __name__ == "__main__":
#     app.run(debug=True)

import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import heapq
from collections import defaultdict
import random
from PIL import Image, ImageTk
import threading

# Graph representation using adjacency list
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, city1, city2, road_distance):
        self.graph[city1].append((city2, road_distance))
        self.graph[city2].append((city1, road_distance))

    def dijkstra(self, start):
        distances = {city: float('inf') for city in self.graph}
        distances[start] = 0
        pq = [(0, start)]
        predecessors = {start: None}

        while pq:
            current_distance, current_city = heapq.heappop(pq)
            if current_distance > distances[current_city]:
                continue

            for neighbor, road_distance in self.graph[current_city]:
                new_distance = current_distance + road_distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_city
                    heapq.heappush(pq, (new_distance, neighbor))

        return distances, predecessors

# GUI Application
class CityRoadNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart City Paths: Visual Pathfinding")
        self.graph = Graph()
        self.city_coordinates = {}

        # Load images for both themes
        self.light_map_image = Image.open("D://DAA Experiments//Project//World.PNG")
        self.dark_map_image = Image.open("D://DAA Experiments//Project//68624446_sl_070722_51460_26.jpg")
        self.background_image = None
        self.marker_image = ImageTk.PhotoImage(Image.open("D://DAA Experiments//Project//Location.png").resize((20, 30)))
        self.start_marker_image = ImageTk.PhotoImage(Image.open("D://DAA Experiments//Project//—Pngtree—red location icon vector design_18250455.png").resize((65, 65)))

        # Initialize theme
        self.dark_theme = False
        self.create_widgets()
        self.update_theme()

    def create_widgets(self):
        # Create a frame for the left-side inputs and buttons
        self.left_frame = ctk.CTkFrame(self.root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Input fields for adding edges
        ctk.CTkLabel(self.left_frame, text="City 1:").place(x=10, y=10)
        self.city1_entry = ctk.CTkEntry(self.left_frame)
        self.city1_entry.place(x=120, y=10)

        ctk.CTkLabel(self.left_frame, text="City 2:").place(x=10, y=40)
        self.city2_entry = ctk.CTkEntry(self.left_frame)
        self.city2_entry.place(x=120, y=40)

        ctk.CTkLabel(self.left_frame, text="Distance:").place(x=10, y=70)
        self.distance_entry = ctk.CTkEntry(self.left_frame)
        self.distance_entry.place(x=120, y=70)

        # Add Edge button
        ctk.CTkButton(self.left_frame, text="Add Edge", command=self.add_edge).place(x=90, y=110)

        ctk.CTkLabel(self.left_frame, text="Run Dijkstra's:").place(x=10, y=150)

        # Dropdown for Dijkstra's options
        self.dijkstra_option = ctk.CTkOptionMenu(
            self.left_frame,
            values=["To All Cities", "City to City"],
            command=self.update_entry_state
        )
        self.dijkstra_option.place(x=120, y=150)

        # Entry for the starting city
        ctk.CTkLabel(self.left_frame, text="Start City:").place(x=10, y=180)
        self.start_city_entry = ctk.CTkEntry(self.left_frame)
        self.start_city_entry.place(x=120, y=180)

        # Entry for the destination city
        ctk.CTkLabel(self.left_frame, text="End City:").place(x=10, y=210)
        self.end_city_entry = ctk.CTkEntry(self.left_frame)
        self.end_city_entry.place(x=120, y=210)

        # Dijkstra's button
        dijkstra_button = ctk.CTkButton(
            self.left_frame,
            text="Run Dijkstra's",
            command=self.run_dijkstra_thread,
            fg_color="purple",
            hover_color="lightgreen",
            text_color="white",
            font=("Arial", 12, "bold")
        )
        dijkstra_button.place(x=90, y=250)

        # Other buttons
        ctk.CTkButton(self.left_frame, text="Reset", command=self.reset).place(x=20, y=290)
        ctk.CTkButton(self.left_frame, text="Theme", command=self.toggle_theme).place(x=170, y=290)

        # Output Text Area (right side)
        self.output_text = scrolledtext.ScrolledText(self.root, width=40, height=25)
        self.output_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Canvas for drawing with background image
        self.canvas = ctk.CTkCanvas(self.root, width=1000, height=600)
        self.canvas.grid(row=1, columnspan=2, sticky="nsew")
        self.canvas.create_image(0, 0, anchor=ctk.NW, image=self.background_image)

    def update_theme(self):
        if self.dark_theme:
            ctk.set_appearance_mode("dark")
            self.background_image = ImageTk.PhotoImage(self.dark_map_image.resize((1000, 550)))
            self.left_frame.configure(fg_color="black")
            self.output_text.configure(bg="black", fg="white")
            self.canvas.configure(bg="black")
        else:
            ctk.set_appearance_mode("light")
            self.background_image = ImageTk.PhotoImage(self.light_map_image.resize((1000, 550)))
            self.left_frame.configure(fg_color="white")
            self.output_text.configure(bg="white", fg="black")
            self.canvas.configure(bg="white")

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=ctk.NW, image=self.background_image)

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.update_theme()

    def update_entry_state(self, option):
        if option == "City to City":
            self.start_city_entry.configure(state="normal")
            self.end_city_entry.configure(state="normal")
        else:
            self.start_city_entry.configure(state="normal")
            self.end_city_entry.configure(state="disabled")

    def add_edge(self):
        try:
            city1 = self.city1_entry.get().strip()
            city2 = self.city2_entry.get().strip()
            distance = int(self.distance_entry.get().strip())

            if city1 not in self.city_coordinates:
                self.city_coordinates[city1] = (random.randint(50, 550), random.randint(50, 350))
            if city2 not in self.city_coordinates:
                self.city_coordinates[city2] = (random.randint(50, 550), random.randint(50, 350))

            self.graph.add_edge(city1, city2, distance)
            self.draw_edge(city1, city2, distance)
            self.output_text.insert(ctk.END, f"Added distance between {city1} and {city2} with distance {distance}\n")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid characters for distance.")

    def draw_edge(self, city1, city2, distance):
        x1, y1 = self.city_coordinates[city1]
        x2, y2 = self.city_coordinates[city2]

        # Draw line between cities
        self.canvas.create_line(x1, y1, x2, y2, fill='Grey', arrow=ctk.LAST)

        # Draw location markers and city names
        self.canvas.create_image(x1, y1, anchor=ctk.CENTER, image=self.marker_image)
        self.canvas.create_text(x1, y1 - 10, text=city1, fill='black', font=('Arial', 12, 'bold'))

        self.canvas.create_image(x2, y2, anchor=ctk.CENTER, image=self.marker_image)
        self.canvas.create_text(x2, y2 - 10, text=city2, fill='black', font=('Arial', 12, 'bold'))

    def run_dijkstra_thread(self):
        self.output_text.delete(1.0, ctk.END)
        start_city = self.start_city_entry.get().strip()
        end_city = self.end_city_entry.get().strip() if self.dijkstra_option.get() == "City to City" else None

        if self.dijkstra_option.get() == "City to City":
            if start_city not in self.city_coordinates or end_city not in self.city_coordinates:
                messagebox.showerror("Input Error", "Please enter valid cities.")
                return
        else:
            if start_city not in self.city_coordinates:
                messagebox.showerror("Input Error", f"City '{start_city}' not found in the graph.")
                return

        # Highlight the starting city immediately when Dijkstra's is run
        self.highlight_starting_city(start_city)

        # Run Dijkstra's in a separate thread
        thread = threading.Thread(target=self.run_dijkstra, args=(start_city, end_city))
        thread.start()

    def highlight_starting_city(self, start_city):
        x_start, y_start = self.city_coordinates[start_city]
        self.canvas.create_image(x_start, y_start, anchor=ctk.CENTER, image=self.start_marker_image)
        self.canvas.create_text(x_start, y_start - 10, text=start_city, fill='black', font=('Arial', 10, 'bold'))

    def run_dijkstra(self, start_city, end_city=None):
        distances, predecessors = self.graph.dijkstra(start_city)

        if end_city:
            output = f"Shortest distance from city {start_city} to city {end_city}: {distances[end_city]}\n"
            self.output_text.insert(ctk.END, output)
            self.draw_shortest_path(start_city, {end_city: distances[end_city]}, predecessors, [end_city])
        else:
            output = f"Shortest distances from city {start_city}:\n"
            for city, distance in distances.items():
                output += f"To city {city} : {distance}\n"
            self.output_text.insert(ctk.END, output)
            self.draw_shortest_path(start_city, distances, predecessors)

    def draw_shortest_path(self, start_city, distances, predecessors, end_cities=None):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=ctk.NW, image=self.background_image)

        for city in self.graph.graph:
            for neighbor, distance in self.graph.graph[city]:
                if city < neighbor:
                    self.draw_edge(city, neighbor, distance)

        self.highlight_starting_city(start_city)

        if end_cities:
            for end_city in end_cities:
                if distances[end_city] < float('inf'):
                    path = self.get_path(start_city, end_city, predecessors)
                    self.highlight_path(path)
        else:
            for city, distance in distances.items():
                if distance < float('inf'):
                    path = self.get_path(start_city, city, predecessors)
                    self.highlight_path(path)

    def get_path(self, start_city, end_city, predecessors):
        path = []
        while end_city is not None:
            path.append(end_city)
            end_city = predecessors.get(end_city)
        path.reverse()
        return path

    def highlight_path(self, path):
        if len(path) < 2:
            return
        
        for i in range(len(path) - 1):
            city1, city2 = path[i], path[i + 1]
            x1, y1 = self.city_coordinates[city1]
            x2, y2 = self.city_coordinates[city2]
            self.canvas.create_line(x1, y1, x2, y2, fill='green', width=3)
            self.canvas.create_image(x1, y1, anchor=ctk.CENTER, image=self.marker_image)
            self.canvas.create_text(x1, y1 - 10, text=city1, fill='black', font=('Arial', 10, 'bold'))
            
            self.canvas.create_image(x2, y2, anchor=ctk.CENTER, image=self.marker_image)
            self.canvas.create_text(x2, y2 - 10, text=city2, fill='black', font=('Arial', 10, 'bold'))

    def reset(self):
        self.graph = Graph()
        self.city_coordinates = {}
        self.canvas.delete("all")
        self.output_text.delete(1.0, ctk.END)
        self.city1_entry.delete(0, ctk.END)
        self.city2_entry.delete(0, ctk.END)
        self.distance_entry.delete(0, ctk.END)
        self.start_city_entry.delete(0, ctk.END)
        self.end_city_entry.delete(0, ctk.END)
        self.canvas.create_image(0, 0, anchor=ctk.NW, image=self.background_image)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    app = CityRoadNetworkApp(root)
    root.mainloop()
