import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import heapq
from collections import defaultdict
import random
from PIL import Image, ImageTk
import threading
import mysql.connector

# Database connection setup (make sure to configure your database settings)
con = mysql.connector.connect(
    host="localhost", user="root", password="Eswar", database="o_b_s"
)


# Graph representation using adjacency list
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, city1, city2, road_distance):
        self.graph[city1].append((city2, road_distance))
        self.graph[city2].append((city1, road_distance))

    def dijkstra(self, start):
        distances = {city: float("inf") for city in self.graph}
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
        self.dark_map_image = Image.open(
            "D://DAA Experiments//Project//68624446_sl_070722_51460_26.jpg"
        )
        self.background_image = None
        self.marker_image = ImageTk.PhotoImage(
            Image.open("D://DAA Experiments//Project//Location.png").resize((20, 30))
        )
        self.start_marker_image = ImageTk.PhotoImage(
            Image.open(
                "D://DAA Experiments//Project//—Pngtree—red location icon vector design_18250455.png"
            ).resize((65, 65))
        )

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
        ctk.CTkButton(self.left_frame, text="Add Edge", command=self.add_edge).place(
            x=90, y=110
        )

        ctk.CTkLabel(self.left_frame, text="Run Dijkstra's:").place(x=10, y=150)

        # Dropdown for Dijkstra's options
        self.dijkstra_option = ctk.CTkOptionMenu(
            self.left_frame,
            values=["To All Cities", "City to City"],
            command=self.update_entry_state,
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
            font=("Arial", 12, "bold"),
        )
        dijkstra_button.place(x=90, y=250)

        # Other buttons
        ctk.CTkButton(self.left_frame, text="Reset", command=self.reset).place(
            x=20, y=290
        )
        ctk.CTkButton(self.left_frame, text="Theme", command=self.toggle_theme).place(
            x=170, y=290
        )

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
            self.background_image = ImageTk.PhotoImage(
                self.dark_map_image.resize((1000, 550))
            )
            self.left_frame.configure(fg_color="black")
            self.output_text.configure(bg="black", fg="white")
            self.canvas.configure(bg="black")
        else:
            ctk.set_appearance_mode("light")
            self.background_image = ImageTk.PhotoImage(
                self.light_map_image.resize((1000, 550))
            )
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
                self.city_coordinates[city1] = (
                    random.randint(50, 550),
                    random.randint(50, 350),
                )
            if city2 not in self.city_coordinates:
                self.city_coordinates[city2] = (
                    random.randint(50, 550),
                    random.randint(50, 350),
                )

            self.graph.add_edge(city1, city2, distance)
            self.draw_edge(city1, city2, distance)
            self.output_text.insert(
                ctk.END,
                f"Added distance between {city1} and {city2} with distance {distance}\n",
            )
        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter valid characters for distance."
            )

    def draw_edge(self, city1, city2, distance):
        x1, y1 = self.city_coordinates[city1]
        x2, y2 = self.city_coordinates[city2]

        # Draw line between cities
        self.canvas.create_line(x1, y1, x2, y2, fill="Grey", arrow=ctk.LAST)

        # Draw location markers and city names
        self.canvas.create_image(x1, y1, anchor=ctk.CENTER, image=self.marker_image)
        self.canvas.create_text(
            x1, y1 - 10, text=city1, fill="black", font=("Arial", 12, "bold")
        )

        self.canvas.create_image(x2, y2, anchor=ctk.CENTER, image=self.marker_image)
        self.canvas.create_text(
            x2, y2 - 10, text=city2, fill="black", font=("Arial", 12, "bold")
        )

    def run_dijkstra_thread(self):
        self.output_text.delete(1.0, ctk.END)
        start_city = self.start_city_entry.get().strip()
        end_city = (
            self.end_city_entry.get().strip()
            if self.dijkstra_option.get() == "City to City"
            else None
        )

        if self.dijkstra_option.get() == "City to City":
            if (
                start_city not in self.city_coordinates
                or end_city not in self.city_coordinates
            ):
                messagebox.showerror("Input Error", "Please enter valid cities.")
                return
        else:
            if start_city not in self.city_coordinates:
                messagebox.showerror(
                    "Input Error", f"City '{start_city}' not found in the graph."
                )
                return

        # Highlight the starting city immediately when Dijkstra's is run
        self.highlight_starting_city(start_city)

        # Run Dijkstra's in a separate thread
        thread = threading.Thread(target=self.run_dijkstra, args=(start_city, end_city))
        thread.start()

    def highlight_starting_city(self, start_city):
        x_start, y_start = self.city_coordinates[start_city]
        self.canvas.create_image(
            x_start, y_start, anchor=ctk.CENTER, image=self.start_marker_image
        )
        self.canvas.create_text(
            x_start,
            y_start - 10,
            text=start_city,
            fill="black",
            font=("Arial", 10, "bold"),
        )

    def run_dijkstra(self, start_city, end_city=None):
        distances, predecessors = self.graph.dijkstra(start_city)

        if end_city:
            output = f"Shortest distance from city {start_city} to city {end_city}: {distances[end_city]}\n"
            self.output_text.insert(ctk.END, output)
            self.draw_shortest_path(
                start_city, {end_city: distances[end_city]}, predecessors, [end_city]
            )
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
                if distances[end_city] < float("inf"):
                    path = self.get_path(start_city, end_city, predecessors)
                    self.highlight_path(path)
        else:
            for city, distance in distances.items():
                if distance < float("inf"):
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
            self.canvas.create_line(x1, y1, x2, y2, fill="green", width=3)
            self.canvas.create_image(x1, y1, anchor=ctk.CENTER, image=self.marker_image)
            self.canvas.create_text(
                x1, y1 - 10, text=city1, fill="black", font=("Arial", 10, "bold")
            )

            self.canvas.create_image(x2, y2, anchor=ctk.CENTER, image=self.marker_image)
            self.canvas.create_text(
                x2, y2 - 10, text=city2, fill="black", font=("Arial", 10, "bold")
            )

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


class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Authentication")
        self.root.geometry("800x800")  # Adjusted size for login form
        self.root.resizable(True, True)  # Prevent resizing for better centering
        self.create_widgets()

    def create_widgets(self):
        # Create a frame that will be centered
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(expand=True)  # Allow frame to expand and center

        # Configure the grid for better alignment
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(self.login_frame, text="Email:").grid(
            row=0, column=0, padx=10, pady=5, sticky="e"
        )
        self.email_entry = ctk.CTkEntry(self.login_frame)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.login_frame, text="Password:").grid(
            row=1, column=0, padx=10, pady=5, sticky="e"
        )
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = ctk.CTkButton(
            self.login_frame, text="Login", command=self.login
        )
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.register_button = ctk.CTkButton(
            self.login_frame, text="Register", command=self.redirect_to_registration
        )
        self.register_button.grid(row=3, column=0, columnspan=2, pady=5)

    def update_login_button_state(self, event=None):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if email and password and len(password) >= 8:
            self.login_button.configure(state="normal")
        else:
            self.login_button.configure(state="disabled")

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if len(password) < 8:
            messagebox.showerror(
                "Input Error", "Password must be at least 8 characters long."
            )
            return

        cursor = con.cursor()
        cursor.execute(
            "SELECT * FROM registration WHERE email = %s AND password = %s",
            (email, password),
        )
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Success", "Welcome to the City Road Network!")
            self.login_frame.destroy()
            CityRoadNetworkApp(self.root)
        else:
            messagebox.showerror("Login Failed", "Incorrect email or password.")

    def redirect_to_registration(self):
        self.login_frame.destroy()
        self.create_registration_form()

    def create_registration_form(self):
        # Create a frame for the registration form
        self.registration_frame = ctk.CTkFrame(self.root)
        self.registration_frame.pack(padx=30, pady=30, fill="both", expand=True)

        # Configure the grid for better alignment
        self.registration_frame.grid_columnconfigure(0, weight=1)  # Label column
        self.registration_frame.grid_columnconfigure(1, weight=2)  # Entry column

        # Add labels and entries to the frame
        ctk.CTkLabel(self.registration_frame, text="Name:").grid(
            row=0, column=0, padx=10, pady=5, sticky="e"
        )
        self.name_entry = ctk.CTkEntry(self.registration_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.registration_frame, text="Email:").grid(
            row=1, column=0, padx=10, pady=5, sticky="e"
        )
        self.email_entry = ctk.CTkEntry(self.registration_frame)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.registration_frame, text="Password:").grid(
            row=2, column=0, padx=10, pady=5, sticky="e"
        )
        self.reg_password_entry = ctk.CTkEntry(self.registration_frame, show="*")
        self.reg_password_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.registration_frame, text="Confirm Password:").grid(
            row=3, column=0, padx=10, pady=5, sticky="e"
        )
        self.confirm_password_entry = ctk.CTkEntry(self.registration_frame, show="*")
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=5)

        # Center buttons in the grid
        self.register_button = ctk.CTkButton(
            self.registration_frame, text="Register", command=self.register_user
        )
        self.register_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.back_to_login_button = ctk.CTkButton(
            self.registration_frame, text="Back to Login", command=self.back_to_login
        )
        self.back_to_login_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Center the registration frame within the root window
        self.registration_frame.pack_propagate(False)  # Prevent frame from shrinking
        self.registration_frame.update_idletasks()  # Update the frame's size
        width = self.registration_frame.winfo_width()
        height = self.registration_frame.winfo_height()
        self.registration_frame.place(relx=0.5, rely=0.5, anchor="center")

    def back_to_login(self):
        self.registration_frame.destroy()
        self.__init__(self.root)  # Reinitialize AuthApp to show the login form again

    def register_user(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not name or not email or len(password) < 8:
            messagebox.showerror(
                "Input Error",
                "Please fill all fields and ensure the password is at least 8 characters long.",
            )
            return

        if password != confirm_password:
            messagebox.showerror("Input Error", "Passwords do not match.")
            return

        cursor = con.cursor()
        try:
            cursor.execute(
                "INSERT INTO registration (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password),
            )
            con.commit()
            messagebox.showinfo("Registration Successful", "You can now log in.")
            self.back_to_login()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Registration Error", "Email already registered.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()


if __name__ == "__main__":
    root = ctk.CTk()
    AuthApp(root)
    root.mainloop()
