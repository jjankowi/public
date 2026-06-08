"""
Panel desktopowy - tkinter + ttkbootstrap
Sidebar: zakładki 1-4 + rozwijane "Testy" (10 testów), tabela z wyszukiwaniem.

Instalacja:
    pip install ttkbootstrap
Uruchomienie:
    python panel_tk.py
"""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


# ----- DANE (podmień na własne źródło / zapytanie do bazy) -----
COLUMNS = ["id", "namespace", "routine", "linesexecuted",
           "globalreferences", "state", "pidexternal",
           "username", "clientipaddress"]


def get_test_data(test_id):
    """Zwraca wiersze dla danego testu. Tu statyczne dane przykładowe."""
    base = [
        (615, "%SYS", "%SYS.WorkQueueMgr", 150092, 10634, "SEMW", 615, "", ""),
        (616, "%SYS", "%SYS.WorkQueueMgr", 7070, 23, "SEMW", 616, "", ""),
        (617, "%SYS", "%SYS.WorkQueueMgr", 98827, 10143, "EVTW", 617, "", ""),
        (625, "USER", "Ens.Queue.1", 288330, 24058, "EVTW", 625, "_Ensemble", ""),
        (626, "USER", "Ens.Queue.1", 1117, 131, "EVTW", 626, "_Ensemble", ""),
        (627, "USER", "Ens.Queue.1", 1112, 134, "EVTW", 627, "_Ensemble", ""),
        (628, "USER", "Ens.Queue.1", 1025, 138, "EVTW", 628, "_Ensemble", ""),
        (629, "USER", "Ens.Queue.1", 394861, 56374, "EVTW", 629, "_Ensemble", ""),
        (630, "USER", "Ens.Queue.1", 124506, 12273, "EVTW", 630, "_Ensemble", ""),
        (631, "USER", "Ens.Queue.1", 596381, 31908, "EVTW", 631, "_Ensemble", ""),
    ]
    # lekka modyfikacja, by dane różniły się per test
    return [(r[0] + test_id, *r[1:]) for r in base]


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="cosmo")  # jasny motyw; np. "darkly" dla ciemnego
        self.title("Panel")
        self.geometry("1200x680")
        self.minsize(900, 560)

        self._all_rows = []          # bufor do filtrowania
        self.current_test = None

        self._build_sidebar()
        self._build_content()
        self.show_placeholder("Zakładka 1")

    # ---------------- SIDEBAR ----------------
    def _build_sidebar(self):
        sidebar = ttk.Frame(self, width=240, bootstyle=DARK)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="  Panel", bootstyle=(INVERSE, DARK),
                  font=("-size 13 -weight bold")).pack(fill=X, pady=(16, 8), padx=4)
        ttk.Separator(sidebar).pack(fill=X, pady=(0, 6))

        # Zakładki 1-4
        for i in range(1, 5):
            ttk.Button(sidebar, text=f"  Zakładka {i}", bootstyle=(DARK, LINK),
                       command=lambda n=i: self.show_placeholder(f"Zakładka {n}")
                       ).pack(fill=X, padx=6, pady=1, anchor=W)

        # Punkt 5: Testy (rozwijane)
        self.tests_open = tk.BooleanVar(value=False)
        self.toggle_btn = ttk.Button(sidebar, text="  ▸ Testy", bootstyle=(DARK, LINK),
                                     command=self._toggle_tests)
        self.toggle_btn.pack(fill=X, padx=6, pady=(8, 1), anchor=W)

        # kontener na podpunkty testów
        self.tests_frame = ttk.Frame(sidebar, bootstyle=DARK)
        for t in range(1, 11):
            ttk.Button(self.tests_frame, text=f"      Test {t}",
                       bootstyle=(DARK, LINK),
                       command=lambda n=t: self.show_test(n)
                       ).pack(fill=X, padx=6, pady=0, anchor=W)

    def _toggle_tests(self):
        if self.tests_open.get():
            self.tests_frame.pack_forget()
            self.toggle_btn.config(text="  ▸ Testy")
            self.tests_open.set(False)
        else:
            self.tests_frame.pack(fill=X, after=self.toggle_btn)
            self.toggle_btn.config(text="  ▾ Testy")
            self.tests_open.set(True)

    # ---------------- CONTENT ----------------
    def _build_content(self):
        self.content = ttk.Frame(self, padding=20)
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

        self.title_lbl = ttk.Label(self.content, text="", font="-size 15 -weight bold")
        self.title_lbl.pack(anchor=W, pady=(0, 14))

        # --- pasek wyszukiwania ---
        self.search_bar = ttk.Frame(self.content)
        ttk.Label(self.search_bar, text="Szukaj:").pack(side=LEFT, padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._apply_filter())
        ttk.Entry(self.search_bar, textvariable=self.search_var, width=30).pack(side=LEFT)

        # --- tabela (Treeview) ---
        self.table_wrap = ttk.Frame(self.content)
        self.tree = ttk.Treeview(self.table_wrap, columns=COLUMNS,
                                 show="headings", bootstyle=PRIMARY, height=15)
        widths = {"routine": 150, "linesexecuted": 110, "globalreferences": 120,
                  "username": 100, "clientipaddress": 110}
        for c in COLUMNS:
            self.tree.heading(c, text=c,
                              command=lambda col=c: self._sort_by(col, False))
            self.tree.column(c, width=widths.get(c, 90), anchor=W)

        vsb = ttk.Scrollbar(self.table_wrap, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        vsb.pack(side=RIGHT, fill=Y)

        self.info_lbl = ttk.Label(self.content, text="", bootstyle=SECONDARY)

    # ---------------- WIDOKI ----------------
    def show_placeholder(self, name):
        self.current_test = None
        self.title_lbl.config(text=name)
        self.search_bar.pack_forget()
        self.table_wrap.pack_forget()
        self.info_lbl.config(text=f'Zawartość: „{name}". Wybierz Testy → konkretny test, '
                                  f'aby zobaczyć tabelę z wynikami.')
        self.info_lbl.pack(anchor=W)

    def show_test(self, test_id):
        self.current_test = test_id
        self.title_lbl.config(text=f"Wyniki: Test {test_id}")
        self.search_var.set("")
        self.info_lbl.pack_forget()

        self.search_bar.pack(anchor=E, pady=(0, 10))
        self.table_wrap.pack(fill=BOTH, expand=True)
        self.info_lbl.pack(anchor=W, pady=(8, 0))

        self._all_rows = get_test_data(test_id)
        self._populate(self._all_rows)

    def _populate(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", END, values=r)
        self.info_lbl.config(text=f"Wyświetlam {len(rows)} z {len(self._all_rows)} wpisów")

    def _apply_filter(self):
        q = self.search_var.get().lower().strip()
        if not q:
            self._populate(self._all_rows)
            return
        filtered = [r for r in self._all_rows
                    if any(q in str(v).lower() for v in r)]
        self._populate(filtered)

    def _sort_by(self, col, descending):
        idx = COLUMNS.index(col)
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        # sortuj numerycznie jeśli się da
        try:
            data.sort(key=lambda t: float(t[0]), reverse=descending)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=descending)
        for pos, (_, k) in enumerate(data):
            self.tree.move(k, "", pos)
        self.tree.heading(col, command=lambda: self._sort_by(col, not descending))


if __name__ == "__main__":
    App().mainloop()
