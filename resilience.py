import argparse
import random
import os
import sys
import time
import tkinter as tk
from tkinter import ttk

def clrscr() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def gen_addition() -> list:
    num1 = random.randint(1, 999)
    num2 = random.randint(1, 1000 - num1)
    res = num1 + num2
    return [num1, num2, res, "+"]

def gen_subtraction() -> list:
    num1 = random.randint(1, 1000)
    num2 = random.randint(1, num1)
    res = num1 - num2
    return [num1, num2, res, "-"]

def gen_multiplication() -> list:
    num1 = random.randint(2, 100)
    num2 = random.randint(2, 1000 // num1)
    res = num1 * num2
    return [num1, num2, res, "*"]

def gen_division() -> list:
    num2 = random.randint(2, 50)
    num1 = random.choice(list(range(num2, 1000, num2)))
    res = int(num1 / num2)
    return [num1, num2, res, "/"]

def gen_recomms(cor: int) -> str:
    ret = [cor]
    for i in range(4):
        rand = random.randint(cor - 100 if cor > 100 else 1, cor + 100 if cor < 901 else 1000)
        while rand in ret:
            rand = random.randint(cor - 100 if cor > 100 else 1, cor + 100 if cor < 901 else 1000)
        ret.append(rand)
    random.shuffle(ret)
    return ret

class Gui(tk.Tk):
    def __init__(self, easymode):
        tk.Tk.__init__(self)
        self.gamevars = {
            "easymode": easymode,
            "round": 0,
            "correct": 0,
            "points": 0,
            "total": 0
        }
        self.call("source", "Azure-ttk-theme/azure.tcl")
        self.call("set_theme", "dark")
        self.geometry(f"800x600+{(self.winfo_screenwidth() // 2) - (800 // 2)}+{(self.winfo_screenheight() // 2) - (600 // 2) - 50}")
        self.resizable(False, False)
        self.title("Resilience")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._frame = None
        self.switch_frame(StartFrame)
    
    def switch_frame(self, frame_class):
        self.unbind("<Return>")
        self._frame.destroy() if self._frame != None else None
        self._frame = frame_class(self)
        self._frame.pack()

    def on_close(self):
        print("Fenster wird geschlossen und Programm beendet.")
        self.destroy()
        sys.exit(0)

class StartFrame(ttk.Frame):
    def __init__(self, window):
        ttk.Frame.__init__(self, window, width=800, height=600)
        self.window = window
        self.pack_propagate(False)

        self.title = ttk.Label(self, text="Willkommen bei Resilience", font=("Arial", 44))
        self.subtitle = ttk.Label(self, text="Resilience ist ein Kopfrechentrainer.\n\nWenn du startest bekommst du 10 zufällig ausgewählte Rechnungen mit den vier Grundrechenarten im Bereich von 1 - 1000.", justify="center", wraplength=750, font=("Arial", 24))
        self.optionsframe = ttk.Frame(self)
        self.easycheck = ttk.Checkbutton(self.optionsframe, text="Easymode (Du bekommst 5 Antworten zur Auswahl)", command=self.toggle_easymode, style="Switch.TCheckbutton")
        self.themeswitch = ttk.Checkbutton(self.optionsframe, text="Dark Mode", command=self.change_theme, style="Switch.TCheckbutton")
        self.start = ttk.Button(self, text="Starten", command=lambda: window.switch_frame(CalcFrame))

        self.title.pack(pady=50)
        self.subtitle.pack()
        self.optionsframe.pack(padx=30, pady=30, side=tk.LEFT, anchor="s")
        self.themeswitch.pack(side=tk.TOP, anchor="w")
        self.easycheck.pack(side=tk.TOP, anchor="w")
        self.start.pack(padx=30, pady=30, ipadx=10, ipady=10, side=tk.RIGHT, anchor="s")

        self.easycheck.state(["selected"]) if window.gamevars["easymode"] else None
        self.themeswitch.state(["selected"])
        window.bind("<Return>", lambda _: window.switch_frame(CalcFrame))

    def toggle_easymode(self):
        self.window.gamevars["easymode"] = not self.window.gamevars["easymode"]
    
    def change_theme(self):
        if self.window.call("ttk::style", "theme", "use") == "azure-dark":
            self.window.call("set_theme", "light")
            self.themeswitch["text"] = "Light Mode"
        else:
            self.window.call("set_theme", "dark")
            self.themeswitch["text"] = "Dark Mode"

class CalcFrame(ttk.Frame):
    def __init__(self, window):
        ttk.Frame.__init__(self, window, width=800, height=600)
        self.window = window
        self.pack_propagate(False)
        self.timer = 0.0
        self.calculation = random.choice([gen_addition, gen_subtraction, gen_multiplication, gen_division])()
        self.recomms = gen_recomms(self.calculation[2]) if window.gamevars["easymode"] else False
        window.gamevars["round"] += 1

        self.topframe = ttk.Frame(self)
        self.title = ttk.Label(self.topframe, text=f"{window.gamevars['round']}. Rechnung:", font=("Arial", 22))
        self.timer_label = ttk.Label(self.topframe, text="0.0 Sekunden", font=("Arial", 22))
        self.middleframe = ttk.Frame(self)
        self.calculation_label = ttk.Label(self.middleframe, text=f"{self.calculation[0]} {self.calculation[3]} {self.calculation[1]}", font=("Arial", 30))
        self.answer = ttk.Entry(self.middleframe, justify="center", validate="key", validatecommand=(self.register(self.input_validation), "%S"))
        self.result = ttk.Label(self.middleframe, text="", wraplength=700, font=("Arial", 20), justify="center")
        self.bottomframe = ttk.Frame(self)
        self.finish = ttk.Button(self.bottomframe, text="Fertig", command=self.on_finish)
        self.quit = ttk.Button(self.bottomframe, text="Frühzeitig\nBeenden", command=self.on_quit)
        
        self.topframe.pack(side=tk.TOP, fill=tk.BOTH)
        self.title.pack(padx=10, pady=10, side=tk.LEFT, anchor="w")
        self.timer_label.pack(padx=10, pady=10, side=tk.RIGHT, anchor="e")
        self.middleframe.place(anchor="c", relx=.5, rely=.5)
        self.calculation_label.pack()
        self.answer.pack()
        self.result.pack()
        self.bottomframe.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.quit.pack(padx=30, pady=30, ipadx=10, ipady=2, side=tk.LEFT, anchor="w")
        self.finish.pack(padx=30, pady=30, ipadx=10, ipady=10, side=tk.RIGHT, anchor="e")

        self.answer.focus()
        window.bind("<Return>", self.on_finish)
        self.tk_timer = self.after(100, self.update_timer)

    def input_validation(self, S):
        if S.isdigit():
            return True
        else:
            self.bell()
            return False

    def on_finish(self, event = 0):
        if not self.window.gamevars["easymode"]:
            self.window.unbind("<Return>")
            self.answer.state(["disabled"])
        else:
            pass
        if not self.answer.get() == "" and int(self.answer.get()) == self.calculation[2]: # or the easymode answer
            points = 3 if round(self.timer, 1) < 10.0 else 2 if round(self.timer, 1) < 20.0 else 1
            self.window.gamevars["correct"] += 1
            self.window.gamevars["points"] += points
            self.result["text"] = f"Toll gemacht! Du hast die Rechnung in {int(round(self.timer, 1)) if round(self.timer, 1) == int(round(self.timer, 1)) else round(self.timer, 1)} Sekunde{'' if round(self.timer, 1) == 1.0 else 'n'} gelöst.\n\nDas gibt {points} Punkt{'e' if points != 1 else ''}"
        else:
            self.result["text"] = f"Wie schade! Du hast {int(round(self.timer, 1)) if round(self.timer, 1) == int(round(self.timer, 1)) else round(self.timer, 1)} Sekunde{'' if round(self.timer, 1) == 1.0 else 'n'} gebraucht und trotzdem falsch gerechnet.\nDas richtige Ergebnis wäre {self.calculation[2]} gewesen."
        self.timer_label["text"] = f"Gesamtpunkte: {self.window.gamevars['points']}"
        self.result.pack_configure(ipady=30)
        self.after_cancel(self.tk_timer)
        if self.window.gamevars["round"] < 10:
            self.finish.pack_configure(ipady=2)
            self.finish.configure(text="Nächste\nRechnung", command=self.on_next)
        else:
            self.quit.pack_forget()
            self.finish.pack_configure(ipady=10)
            self.finish.configure(text="Beenden", command=self.on_next)
        self.window.bind("<Return>", self.on_next)

    def on_next(self, event = 0):
        self.window.switch_frame(CalcFrame if self.window.gamevars["round"] < 10 else EndFrame)

    def on_quit(self):
        self.window.unbind("<Return>") if not self.window.gamevars["easymode"] else None
        self.after_cancel(self.tk_timer)
        self.window.switch_frame(EndFrame)

    def update_timer(self):
        self.timer += 0.1
        self.timer_label["text"] = f"{round(self.timer, 1)} Sekunde{'n' if round(self.timer, 1) != 1.0 else '  '}"
        self.tk_timer = self.after(100, self.update_timer)

class EndFrame(ttk.Frame):
    def __init__(self, window):
        ttk.Frame.__init__(self, window, width=800, height=600)
        self.pack_propagate(False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Resilience", description="Python Kopfrechentrainer")
    parser.add_argument("-g", "--gui", action="store_true", default=False, dest="use_gui", help="Öffnet das Programm mit einer grafischen Benutzeroberfläche")
    parser.add_argument("-e", "--easy", action="store_true", default=False, dest="use_easy", help="Aktiviert den Easy-Modus bei dem dir fünf potenziell richtige Ergebnisse vorgeschlagen werden")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, dest="use_verbose", help="Aktiviert den verbosen Modus")
    parser._actions[0].help = "Zeigt diese Hilfenachricht"
    args = parser.parse_args()
    easymode = args.use_easy
    verbose = args.use_verbose
    if args.use_gui:
        print("GUI Version wird gestartet...")
        gui = Gui(easymode)
        gui.mainloop()
    clrscr()
    print("Willkommen bei Resilience!")
    print("Resilience ist ein Kopfrechentrainer.")
    print("Wenn du startest bekommst du 10 zufällig ausgewählte Rechnungen mit den vier Grundrechenarten im Bereich von 1 - 1000.\n")
    if easymode:
        print("Der Easy Mode ist aktiviert, dir werden bei jeder Rechnung 5 Vorschläge gegeben von denen einer richtig ist.")
    if input("Starten? (q für beenden): ")[:1].lower() == "q":
        sys.exit(0)
    count = 1
    correct = 0
    total = 0
    while True:
        clrscr()
        print(f"{count}. Rechnung:")
        calc = random.choice([gen_addition, gen_subtraction, gen_multiplication, gen_division])()
        if easymode:
            print(f"Vorschläge: {' | '.join(str(i) for i in gen_recomms(calc[2]))}")
        timer = time.time()
        res = input(f"{calc[0]} {calc[3]} {calc[1]}: ")
        while not res.isdigit():
            print("Bitte gib eine Zahl ein!")
            res = input(f"{calc[0]} {calc[3]} {calc[1]}: ")
        res = int(res)
        timer = round(time.time() - timer, 1)
        if res == calc[2]:
            print(f"Toll gemacht! Du hast die Rechnung in {int(timer) if timer == int(timer) else timer} Sekunde{'' if timer == 1.0 else 'n'} gelöst.")
            points = 3 if timer < 10 else (2 if timer < 20 else 1)
            total += points
            correct += 1
            print(f"Das gibt {points} Punkt{'' if points == 1 else 'e'} und somit hast du jetzt {total} Punkt{'' if total == 1 else 'e'}.")
        else:
            print(f"Wie schade! Du hast {int(timer) if timer == int(timer) else timer} Sekunde{'' if timer == 1.0 else 'n'} gebraucht und trotzdem falsch gerechnet.")
            print(f"Das richtige Ergebnis wäre {calc[2]} gewesen.")
        count += 1
        if count == 11 and str(input("Beenden?: ")) + "x" or input("Nächste Rechnung? (q für beenden): ")[:1].lower() == "q":
            clrscr()
            print(f"Du hast insgesamt {correct} / {count - 1} Rechnung{'en' if count - 1 != 1 else ''} gelöst und dabei {total} / {(count - 1) * 3} Punkten erreicht.")
            break
