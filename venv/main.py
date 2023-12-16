
import requests
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmb
from PIL import Image, ImageTk
import threading

# import rightfram as r
# import leftfram as l





class Mainwindow:
    def __init__(self, window):
        self.window = window
        self.window.minsize(height=700,width=700)
        self.window.title('Fetch Movies Api')
        self.movie_widgets = []
        #self.window.state('zoomed')
        #######################  topframe   ####################################
        self.topfram = Frame(self.window, bg='#2E4374', height=100)
        self.topfram.pack(fill=X)
        self.titre = Label(self.topfram, text='Fetch Movies Api', bg='#2E4374', fg='#E5C3A6', font=('tachona', 35), pady=20)
        self.titre.pack()
        #######################  mainfarame = leftframe + rightframe   ####################################

        self.mainrfram = Frame(self.window, bg='#7C81AD')
        self.mainrfram.pack(fill=BOTH,expand=True)

        self.loading_label = Label(self.mainrfram, text='Loading...', font=('tachona', 20), pady=30)
        self.loading_label.pack()
        
        threading.Thread(target=self.fetch_movies).start()
        ##############################################################################
        
        #######################  leftframe= 6 entry boxes + 3 buttons  ####################################
    

    def fetch_movies(self):
        # Replace the URL with the actual API endpoint
        api_url = "https://run.mocky.io/v3/d9293f76-e064-4731-ba9f-dcef017cca1a"

        self.style = ttk.Style()
        self.style.configure("My.TFrame", background="#4B527E")

        
        try:
            
            response = requests.get(api_url)
            data = response.json()

            # Assuming the API response is a list of movie objects
            movies = data

            self.loading_label.destroy()

            # Clear existing data
            for widget in self.movie_widgets:
                widget.destroy()

            # Create and display movie information widgets
            for i, movie in enumerate(movies):
                frame = ttk.Frame(self.mainrfram, style="My.TFrame", padding="5")
                frame.grid(row=i // 3, column=i % 3, padx=7, pady=7)

                # Load and display movie image
                image_url = movie.get("image")
                if image_url:
                    
                    image = Image.open(requests.get(image_url, stream=True).raw)
                    image = image.resize((200, 250))
                    photo = ImageTk.PhotoImage(image)
                    label = ttk.Label(frame, image=photo)
                    label.image = photo
                    label.pack()

                ttk.Label(frame, text=f"{movie['name']}", font=('tachona', 17), background="#4B527E", foreground="white").pack()
                ttk.Label(frame, text=f"{movie['price']} $", font=('tachona', 17), background="#4B527E", foreground="white").pack()
                ttk.Label(frame, text=f"Translated: {movie['traduction']}", font=('tachona', 17), background="#4B527E", foreground="white").pack()

                self.movie_widgets.append(frame)

        except requests.RequestException as e:
            # Handle API request errors
            print(f"Error fetching data: {e}")
            self.loading_label.destroy()
            self.loading_label = Label(self.mainrfram, text=f"Error fetching data: {e}", fg = "red", font=('tachona', 20), pady=30)
            self.loading_label.pack()

    


        

        
def page():
    window = Tk()
    Mainwindow(window)
    window.mainloop()


if __name__ == '__main__':
    page()