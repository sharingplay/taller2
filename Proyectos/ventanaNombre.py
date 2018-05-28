import tkinter as tk

import juegoSublimeEditar as game

def un_jugador():
    print ("nombre del jugador 1: " + entry1.get())
    master.withdraw()
    game.juegoPrincipal(entry1.get(),"")
    master.destroy()

def dos_jugadores():
    print ("nombre del jugador 1: " + entry1.get() + "\t nombre del jugador 2: " + entry2.get())
    master.withdraw()
    game.juegoPrincipal(entry1.get(), entry2.get())
    master.destroy()

master = tk.Tk()

master.geometry("300x200")

tk.Label(master, text="Jugador uno: ").place(x=30,y=10)
tk.Label(master, text="Jugador dos: ").place(x=30,y=60)

entry1 = tk.Entry(master)
entry2 = tk.Entry(master)

entry1.place(x=110,y=10)
entry2.place(x=110,y=60)

uno = tk.Button(master, text="Un jugador", command=un_jugador).place(x=50,y=110)

dos = tk.Button(master, text="Dos jugadores", command=dos_jugadores).place(x=150,y=110)

tk.mainloop( )
