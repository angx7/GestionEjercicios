# fitness_oop.py
from typing import List, Optional

# Parámetros de estimación (ajustables)
SEC_POR_REP = 5  # segundos por repetición
DESCANSO_ENTRE_SERIES = 30  # segundos entre series


def minutos_a_texto(mins: float) -> str:
    total = int(round(mins * 60))
    m, s = divmod(total, 60)
    return f"{m} min {s} s"


class Ejercicio:
    def __init__(
        self,
        nombre: str,
        repeticiones: int,
        series: int,
        sec_por_rep: int = SEC_POR_REP,
        descanso_entre_series: int = DESCANSO_ENTRE_SERIES,
    ):
        self.nombre = nombre.strip()
        self.repeticiones = int(repeticiones)
        self.series = int(series)
        self.sec_por_rep = int(sec_por_rep)
        self.descanso_entre_series = int(descanso_entre_series)
        self._validar()

    def _validar(self):
        if not self.nombre:
            raise ValueError("El nombre del ejercicio no puede estar vacío.")
        if self.repeticiones <= 0:
            raise ValueError("Las repeticiones deben ser mayores a 0.")
        if self.series <= 0:
            raise ValueError("Las series deben ser mayores a 0.")
        if self.sec_por_rep <= 0 or self.descanso_entre_series < 0:
            raise ValueError("Tiempos inválidos para el ejercicio.")

    def duracion_minutos(self) -> float:
        movimiento = self.repeticiones * self.sec_por_rep * self.series
        descanso = self.descanso_entre_series * max(0, self.series - 1)
        return (movimiento + descanso) / 60.0

    def actualizar(
        self, repeticiones: Optional[int] = None, series: Optional[int] = None
    ):
        if repeticiones is not None:
            if repeticiones <= 0:
                raise ValueError("Las repeticiones deben ser mayores a 0.")
            self.repeticiones = repeticiones
        if series is not None:
            if series <= 0:
                raise ValueError("Las series deben ser mayores a 0.")
            self.series = series

    def __str__(self) -> str:
        return (
            f"{self.nombre} | reps: {self.repeticiones} | series: {self.series} "
            f"| estimado: {minutos_a_texto(self.duracion_minutos())}"
        )


class Rutina:
    def __init__(
        self,
        nombre: str,
        descripcion: str,
        ejercicios: List[Ejercicio],
        duracion_base_min: float = 0.0,
    ):
        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        self.duracion_base_min = max(0.0, float(duracion_base_min))
        self.ejercicios: List[Ejercicio] = list(ejercicios)
        self._validar()

    def _validar(self):
        if not self.nombre:
            raise ValueError("El nombre de la rutina no puede estar vacío.")
        if not self.descripcion:
            raise ValueError("La descripción de la rutina no puede estar vacía.")
        if len(self.ejercicios) == 0:
            raise ValueError("Una rutina debe tener al menos un ejercicio.")
        nombres = [ej.nombre.lower() for ej in self.ejercicios]
        if len(nombres) != len(set(nombres)):
            raise ValueError(
                "Hay ejercicios duplicados por nombre dentro de la rutina."
            )

    def agregar_ejercicio(self, ejercicio: Ejercicio):
        if any(ej.nombre.lower() == ejercicio.nombre.lower() for ej in self.ejercicios):
            raise ValueError(
                f"Ya existe un ejercicio '{ejercicio.nombre}' en la rutina."
            )
        self.ejercicios.append(ejercicio)

    def eliminar_ejercicio(self, nombre_ejercicio: str):
        base = len(self.ejercicios)
        self.ejercicios = [
            ej
            for ej in self.ejercicios
            if ej.nombre.lower() != nombre_ejercicio.strip().lower()
        ]
        if len(self.ejercicios) == base:
            raise ValueError("No se encontró el ejercicio a eliminar.")
        if len(self.ejercicios) == 0:
            raise ValueError(
                "La rutina no puede quedarse vacía; agrega otro ejercicio o cancela la eliminación."
            )

    def actualizar_datos(
        self,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        duracion_base_min: Optional[float] = None,
    ):
        if nombre is not None:
            nombre = nombre.strip()
            if not nombre:
                raise ValueError("El nombre de la rutina no puede quedar vacío.")
            self.nombre = nombre
        if descripcion is not None:
            descripcion = descripcion.strip()
            if not descripcion:
                raise ValueError("La descripción de la rutina no puede quedar vacía.")
            self.descripcion = descripcion
        if duracion_base_min is not None:
            if duracion_base_min < 0:
                raise ValueError("La duración base no puede ser negativa.")
            self.duracion_base_min = float(duracion_base_min)

    def actualizar_ejercicio(
        self,
        nombre_ejercicio: str,
        repeticiones: Optional[int] = None,
        series: Optional[int] = None,
    ):
        ej = self._buscar(nombre_ejercicio)
        ej.actualizar(repeticiones, series)

    def _buscar(self, nombre_ejercicio: str) -> Ejercicio:
        for ej in self.ejercicios:
            if ej.nombre.lower() == nombre_ejercicio.strip().lower():
                return ej
        raise ValueError("Ejercicio no encontrado en la rutina.")

    def duracion_total_min(self) -> float:
        return self.duracion_base_min + sum(
            ej.duracion_minutos() for ej in self.ejercicios
        )

    def __str__(self) -> str:
        return (
            f"Rutina: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Base: {minutos_a_texto(self.duracion_base_min)} | "
            f"Total: {minutos_a_texto(self.duracion_total_min())}\n"
            f"Ejercicios: {len(self.ejercicios)}"
        )


class Usuario:
    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre.strip()
        self.edad = int(edad)
        self.rutinas: List[Rutina] = []
        self._validar()

    def _validar(self):
        if not self.nombre:
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if self.edad is None or self.edad < 16:
            raise ValueError("La edad debe ser un número mayor o igual a 16 años.")

    def asignar_rutina(self, rutina: Rutina):
        if any(r.nombre.lower() == rutina.nombre.lower() for r in self.rutinas):
            raise ValueError(
                f"El usuario ya tiene una rutina llamada '{rutina.nombre}'."
            )
        self.rutinas.append(rutina)

    def __str__(self) -> str:
        return (
            f"Usuario: {self.nombre} | Edad: {self.edad} | Rutinas: {len(self.rutinas)}"
        )


class SistemaGestion:
    def __init__(self):
        self.usuarios: List[Usuario] = []
        self.ejercicios_catalogo: List[Ejercicio] = []  # catálogo global
        self.rutinas: List[Rutina] = []

    # Usuarios
    def agregar_usuario(self, nombre: str, edad: int):
        if self._buscar_usuario(nombre) is not None:
            raise ValueError("Ya existe un usuario con ese nombre.")
        self.usuarios.append(Usuario(nombre, edad))

    def listar_usuarios(self):
        if not self.usuarios:
            print("No hay usuarios.")
        for u in self.usuarios:
            print(u)

    def _buscar_usuario(self, nombre: str) -> Optional[Usuario]:
        for u in self.usuarios:
            if u.nombre.lower() == nombre.strip().lower():
                return u
        return None

    # Ejercicios (catálogo global)
    def crear_ejercicio(self, nombre: str, repeticiones: int, series: int):
        if any(
            ej.nombre.lower() == nombre.strip().lower()
            for ej in self.ejercicios_catalogo
        ):
            raise ValueError("Ya existe un ejercicio en el catálogo con ese nombre.")
        ej = Ejercicio(nombre, repeticiones, series)
        self.ejercicios_catalogo.append(ej)
        print(
            f"Ejercicio creado. Duración estimada: {minutos_a_texto(ej.duracion_minutos())}"
        )

    def listar_ejercicios(self):
        if not self.ejercicios_catalogo:
            print("(Catálogo vacío)")
            return
        for ej in self.ejercicios_catalogo:
            print(f"- {ej}")

    def eliminar_ejercicio(self, nombre: str):
        base = len(self.ejercicios_catalogo)
        self.ejercicios_catalogo = [
            ej
            for ej in self.ejercicios_catalogo
            if ej.nombre.lower() != nombre.strip().lower()
        ]
        if len(self.ejercicios_catalogo) == base:
            raise ValueError("No se encontró el ejercicio para eliminar.")

    def obtener_ejercicios_por_nombres(self, nombres: List[str]) -> List[Ejercicio]:
        result = []
        for nombre in nombres:
            ej = next(
                (
                    e
                    for e in self.ejercicios_catalogo
                    if e.nombre.lower() == nombre.strip().lower()
                ),
                None,
            )
            if ej is None:
                raise ValueError(f"Ejercicio '{nombre}' no existe en el catálogo.")
            result.append(ej)
        return result

    # Rutinas (siempre con ≥1 ejercicio del catálogo)
    def crear_rutina(
        self,
        nombre: str,
        descripcion: str,
        nombres_ejercicios: List[str],
        duracion_base_min: float = 0.0,
    ):
        if self._buscar_rutina(nombre) is not None:
            raise ValueError("Ya existe una rutina con ese nombre.")
        if not self.ejercicios_catalogo:
            raise ValueError("Primero crea ejercicios en el catálogo.")
        if not nombres_ejercicios:
            raise ValueError("Debes seleccionar al menos un ejercicio para la rutina.")
        ejercicios = self.obtener_ejercicios_por_nombres(nombres_ejercicios)
        r = Rutina(nombre, descripcion, ejercicios, duracion_base_min)
        self.rutinas.append(r)

    def listar_rutinas(self):
        if not self.rutinas:
            print("No hay rutinas.")
            return
        for r in self.rutinas:
            print("-" * 60)
            print(r)
            for ej in r.ejercicios:
                print(f"  • {ej}")
        print("-" * 60)

    def _buscar_rutina(self, nombre: str) -> Optional[Rutina]:
        for r in self.rutinas:
            if r.nombre.lower() == nombre.strip().lower():
                return r
        return None

    def editar_rutina(
        self,
        nombre: str,
        nuevo_nombre: Optional[str] = None,
        nueva_desc: Optional[str] = None,
        nueva_base: Optional[float] = None,
    ):
        r = self._buscar_rutina(nombre)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        r.actualizar_datos(nuevo_nombre, nueva_desc, nueva_base)

    def rutina_agregar_ejercicio(self, nombre_rutina: str, nombre_ejercicio: str):
        r = self._buscar_rutina(nombre_rutina)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        ej = next(
            (
                e
                for e in self.ejercicios_catalogo
                if e.nombre.lower() == nombre_ejercicio.strip().lower()
            ),
            None,
        )
        if ej is None:
            raise ValueError("Ese ejercicio no existe en el catálogo.")
        r.agregar_ejercicio(ej)

    def rutina_eliminar_ejercicio(self, nombre_rutina: str, nombre_ejercicio: str):
        r = self._buscar_rutina(nombre_rutina)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        r.eliminar_ejercicio(nombre_ejercicio)

    def rutina_actualizar_ejercicio(
        self,
        nombre_rutina: str,
        nombre_ejercicio: str,
        repeticiones: Optional[int] = None,
        series: Optional[int] = None,
    ):
        r = self._buscar_rutina(nombre_rutina)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        r.actualizar_ejercicio(nombre_ejercicio, repeticiones, series)

    # Asignación y Reporte
    def asignar_rutina_a_usuario(self, nombre_usuario: str, nombre_rutina: str):
        u = self._buscar_usuario(nombre_usuario)
        if u is None:
            raise ValueError("Usuario no encontrado.")
        r = self._buscar_rutina(nombre_rutina)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        u.asignar_rutina(r)

    def reporte_por_usuario(self):
        if not self.usuarios:
            print("No hay usuarios.")
            return
        for u in self.usuarios:
            print("=" * 60)
            print(f"Usuario: {u.nombre} | Edad: {u.edad}")
            if not u.rutinas:
                print("  (Sin rutinas asignadas)")
            else:
                for r in u.rutinas:
                    print(f"  - {r.nombre}: {minutos_a_texto(r.duracion_total_min())}")
        print("=" * 60)

    # Menús de terminal
    def menu(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1) Usuarios")
            print("2) Ejercicios (catálogo)")
            print("3) Rutinas")
            print("4) Asignar rutina a usuario")
            print("5) Reporte por usuario")
            print("6) Salir")
            op = input("Opción: ").strip()
            try:
                if op == "1":
                    self.menu_usuarios()
                elif op == "2":
                    self.menu_ejercicios()
                elif op == "3":
                    self.menu_rutinas()
                elif op == "4":
                    u = input("Usuario: ")
                    r = input("Rutina: ")
                    self.asignar_rutina_a_usuario(u, r)
                    print("Rutina asignada.")
                elif op == "5":
                    self.reporte_por_usuario()
                elif op == "6":
                    print("Hasta luego.")
                    break
                else:
                    print("Opción no válida.")
            except ValueError as e:
                print(f"[Error] {e}")

    def menu_usuarios(self):
        while True:
            print("\n--- Usuarios ---")
            print("1) Agregar")
            print("2) Listar")
            print("3) Volver")
            op = input("Opción: ").strip()
            try:
                if op == "1":
                    nombre = input("Nombre: ").strip()
                    edad = int(input("Edad: ").strip())
                    self.agregar_usuario(nombre, edad)
                    print("Usuario agregado.")
                elif op == "2":
                    self.listar_usuarios()
                elif op == "3":
                    return
                else:
                    print("Opción no válida.")
            except ValueError as e:
                print(f"[Error] {e}")

    def menu_ejercicios(self):
        while True:
            print("\n--- Ejercicios (catálogo) ---")
            print("1) Crear ejercicio")
            print("2) Listar ejercicios")
            print("3) Eliminar ejercicio")
            print("4) Volver")
            op = input("Opción: ").strip()
            # try/except dentro de cada opción:
            try:
                if op == "1":
                    nombre = input("Nombre: ").strip()
                    reps = int(input("Repeticiones: ").strip())
                    series = int(input("Series: ").strip())
                    self.crear_ejercicio(nombre, reps, series)
                elif op == "2":
                    self.listar_ejercicios()
                elif op == "3":
                    nombre = input("Nombre a eliminar: ").strip()
                    self.eliminar_ejercicio(nombre)
                    print("Ejercicio eliminado del catálogo.")
                elif op == "4":
                    return
                else:
                    print("Opción no válida.")
            except ValueError as e:
                print(f"[Error] {e}")

    def menu_rutinas(self):
        while True:
            print("\n--- Rutinas ---")
            print("1) Crear rutina (seleccionando ejercicios del catálogo)")
            print("2) Listar rutinas")
            print("3) Editar rutina")
            print("4) Volver")
            op = input("Opción: ").strip()
            try:
                if op == "1":
                    if not self.ejercicios_catalogo:
                        print("Primero crea ejercicios en el catálogo.")
                        continue
                    nombre = input("Nombre de la rutina: ").strip()
                    desc = input("Descripción: ").strip()
                    base_txt = input(
                        "Duración base en min (opcional, enter=0): "
                    ).strip()
                    base = float(base_txt) if base_txt else 0.0
                    print("\nEjercicios disponibles (separa por coma):")
                    self.listar_ejercicios()
                    sel = input("Nombres a incluir: ").strip()
                    nombres = [n.strip() for n in sel.split(",") if n.strip()]
                    self.crear_rutina(nombre, desc, nombres, base)
                    print("Rutina creada.")
                elif op == "2":
                    self.listar_rutinas()
                elif op == "3":
                    nombre = input("Nombre de la rutina a editar: ").strip()
                    r = self._buscar_rutina(nombre)
                    if r is None:
                        print("No existe esa rutina.")
                        continue
                    self.submenu_editar_rutina(r)
                elif op == "4":
                    return
                else:
                    print("Opción no válida.")
            except ValueError as e:
                print(f"[Error] {e}")

    def submenu_editar_rutina(self, r: Rutina):
        while True:
            print(f"\n>>> Editando: {r.nombre}")
            print("1) Agregar ejercicio (del catálogo)")
            print("2) Eliminar ejercicio")
            print("3) Actualizar reps/series de un ejercicio")
            print("4) Modificar nombre/descr./base")
            print("5) Ver duración total")
            print("6) Listar ejercicios")
            print("7) Volver")
            op = input("Opción: ").strip()
            try:
                if op == "1":
                    if not self.ejercicios_catalogo:
                        print("Catálogo vacío. Crea ejercicios primero.")
                        continue
                    self.listar_ejercicios()
                    nombre = input("Nombre del ejercicio a agregar: ").strip()
                    self.rutina_agregar_ejercicio(r.nombre, nombre)
                    print("Ejercicio agregado a la rutina.")
                elif op == "2":
                    nombre = input("Nombre del ejercicio a eliminar: ").strip()
                    self.rutina_eliminar_ejercicio(r.nombre, nombre)
                    print("Ejercicio eliminado de la rutina.")
                elif op == "3":
                    nombre = input("Ejercicio a actualizar: ").strip()
                    rep_txt = input(
                        "Nuevas repeticiones (enter para mantener): "
                    ).strip()
                    ser_txt = input("Nuevas series (enter para mantener): ").strip()
                    rep = None if rep_txt == "" else int(rep_txt)
                    ser = None if ser_txt == "" else int(ser_txt)
                    self.rutina_actualizar_ejercicio(
                        r.nombre, nombre, repeticiones=rep, series=ser
                    )
                    print("Ejercicio actualizado.")
                elif op == "4":
                    nuevo = input("Nuevo nombre (enter=mantener): ")
                    desc = input("Nueva descripción (enter=mantener): ")
                    base_txt = input("Nueva base en min (enter=mantener): ").strip()
                    base = None if base_txt == "" else float(base_txt)
                    self.editar_rutina(
                        r.nombre,
                        nuevo_nombre=(None if not nuevo.strip() else nuevo),
                        nueva_desc=(None if not desc.strip() else desc),
                        nueva_base=base,
                    )
                    print("Datos actualizados.")
                elif op == "5":
                    print(f"Duración total: {minutos_a_texto(r.duracion_total_min())}")
                elif op == "6":
                    if not r.ejercicios:
                        print("(Sin ejercicios)")
                    else:
                        for ej in r.ejercicios:
                            print(f"  • {ej}")
                elif op == "7":
                    return
                else:
                    print("Opción no válida.")
            except ValueError as e:
                print(f"[Error] {e}")


if __name__ == "__main__":
    sistema = SistemaGestion()
    sistema.menu()
