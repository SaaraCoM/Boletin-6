from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modelo.eleccion import EleccionCongreso2023
from servicios.analizador import AnalizadorElectoral
from servicios.graficos import GeneradorGraficos
from servicios.pactometro import Pactometro
from servicios.validador import ValidadorCoherencia
from ui.temas import TEMAS


class AplicacionElecciones(ctk.CTk):
    def __init__(self, eleccion: EleccionCongreso2023):
        super().__init__()
        self.eleccion = eleccion
        self.analizador = AnalizadorElectoral()
        self.graficos = GeneradorGraficos()
        self.pactometro = Pactometro()
        self.validador = ValidadorCoherencia()
        self.tema_actual = "oscuro"
        self.title("Congreso 2023 · Dashboard OO")
        self.geometry("1400x900")
        self.minsize(1100, 700)
        self._configurar_apariencia()
        self._construir_layout()

    def _configurar_apariencia(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self._aplicar_colores()

    def _aplicar_colores(self) -> None:
        paleta = TEMAS[self.tema_actual]
        self.configure(fg_color=paleta["fondo"])

    def _construir_layout(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        titulo = ctk.CTkLabel(self.sidebar, text="Congreso 2023", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.tema_switch = ctk.CTkSegmentedButton(self.sidebar, values=["oscuro", "claro"], command=self._cambiar_tema)
        self.tema_switch.set(self.tema_actual)
        self.tema_switch.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)
        for nombre in ["Dashboard", "Territorios", "Resultados", "D'Hondt", "Análisis", "Gráficos", "Pactómetro", "Validación"]:
            self.tabs.add(nombre)

        self._construir_dashboard()
        self._construir_territorios()
        self._construir_resultados()
        self._construir_dhondt()
        self._construir_analisis()
        self._construir_graficos()
        self._construir_pactometro()
        self._construir_validacion()

    def _crear_tarjeta(self, parent, titulo: str, valor: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(parent, corner_radius=16)
        ctk.CTkLabel(frame, text=titulo, anchor="w").pack(fill="x", padx=16, pady=(14, 4))
        ctk.CTkLabel(frame, text=valor, anchor="w", font=ctk.CTkFont(size=26, weight="bold")).pack(fill="x", padx=16, pady=(0, 14))
        return frame

    def _construir_dashboard(self) -> None:
        tab = self.tabs.tab("Dashboard")
        tab.grid_columnconfigure((0, 1, 2), weight=1)
        total_circ = len(self.eleccion.circunscripciones)
        total_partidos = len(self.eleccion.partidos)
        total_escanos = self.eleccion.nacion.total_diputados_oficiales() if self.eleccion.nacion else 0
        self._crear_tarjeta(tab, "Circunscripciones", str(total_circ)).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self._crear_tarjeta(tab, "Partidos detectados", str(total_partidos)).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self._crear_tarjeta(tab, "Escaños oficiales", str(total_escanos)).grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        if self.eleccion.nacion is not None:
            figura = self.graficos.grafico_barras_partidos(self.eleccion.nacion, "diputados")
            canvas = FigureCanvasTkAgg(figura, master=tab)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def _construir_territorios(self) -> None:
        tab = self.tabs.tab("Territorios")
        cuadro = tk.Text(tab, wrap="word", height=30)
        cuadro.pack(fill="both", expand=True, padx=12, pady=12)
        for comunidad in self.eleccion.comunidades.values():
            cuadro.insert("end", f"{comunidad.nombre}: {len(comunidad.circunscripciones)} circunscripciones\n")

    def _construir_resultados(self) -> None:
        tab = self.tabs.tab("Resultados")
        tree = ttk.Treeview(tab, columns=("territorio", "partido", "votos", "oficiales", "calculados"), show="headings")
        for columna in tree["columns"]:
            tree.heading(columna, text=columna.title())
            tree.column(columna, width=140)
        tree.pack(fill="both", expand=True, padx=12, pady=12)
        for circ in self.eleccion.circunscripciones.values():
            for resultado in circ.resultados.values():
                tree.insert("", "end", values=(circ.nombre, resultado.partido.siglas, resultado.votos, resultado.diputados_oficiales, resultado.diputados_calculados))

    def _construir_dhondt(self) -> None:
        tab = self.tabs.tab("D'Hondt")
        cuadro = tk.Text(tab, wrap="word")
        cuadro.pack(fill="both", expand=True, padx=12, pady=12)
        for fila in self.analizador.ultimo_escano_por_circunscripcion(self.eleccion):
            cuadro.insert(
                "end",
                f"{fila['circunscripcion']}: último={fila['ultimo_escano']} · cerca={fila['se_quedo_cerca']} · faltan={fila['votos_faltantes']}\n",
            )

    def _construir_analisis(self) -> None:
        tab = self.tabs.tab("Análisis")
        cuadro = tk.Text(tab, wrap="word")
        cuadro.pack(fill="both", expand=True, padx=12, pady=12)
        cuadro.insert("end", "Top circunscripciones por voto nulo:\n")
        for territorio in self.analizador.top_circunscripciones_nulos(self.eleccion):
            cuadro.insert("end", f"- {territorio.nombre}: {territorio.porcentaje_votos_nulos:.2f}%\n")

    def _construir_graficos(self) -> None:
        tab = self.tabs.tab("Gráficos")
        if self.eleccion.nacion is not None:
            figura = self.graficos.grafico_sectores_partidos(self.eleccion.nacion, "votos")
            canvas = FigureCanvasTkAgg(figura, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

    def _construir_pactometro(self) -> None:
        tab = self.tabs.tab("Pactómetro")
        cuadro = tk.Text(tab, wrap="word")
        cuadro.pack(fill="both", expand=True, padx=12, pady=12)
        for partidos, total in self.pactometro.generar(self.eleccion, 176)[:25]:
            cuadro.insert("end", f"{' + '.join(partidos)} = {total}\n")

    def _construir_validacion(self) -> None:
        tab = self.tabs.tab("Validación")
        cuadro = tk.Text(tab, wrap="word")
        cuadro.pack(fill="both", expand=True, padx=12, pady=12)
        incidencias = self.validador.validar(self.eleccion)
        if not incidencias:
            cuadro.insert("end", "Sin incidencias detectadas.\n")
            return
        for incidencia in incidencias[:200]:
            cuadro.insert("end", f"[{incidencia.severidad}] {incidencia.territorio}: {incidencia.mensaje}\n")

    def _cambiar_tema(self, valor: str) -> None:
        self.tema_actual = valor
        ctk.set_appearance_mode("dark" if valor == "oscuro" else "light")
        self._aplicar_colores()
