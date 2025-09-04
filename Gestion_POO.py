# fitness_oop.py (optimizado)
from typing import List, Optional, Dict

# Parámetros de estimación (ajustables)
SEC_POR_REP = 5  # segundos por repetición
DESCANSO_ENTRE_SERIES = 30  # segundos entre series


def minutos_a_texto(mins: float) -> str:
    total = int(round(mins * 60))
    m, s = divmod(total, 60)
    return f"{m} min {s} s"


def _norm(s: str) -> str:
    return s.strip().lower()


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
    def __init__(self, nombre: str, descripcion: str, ejercicios: List[Ejercicio]):
        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        self.ejercicios: List[Ejercicio] = list(ejercicios)
        self._validar()

    def _validar(self):
        if not self.nombre:
            raise ValueError("El nombre de la rutina no puede estar vacío.")
        if not self.descripcion:
            raise ValueError("La descripción de la rutina no puede estar vacía.")
        if not self.ejercicios:
            raise ValueError("Una rutina debe tener al menos un ejercicio.")
        nombres = [_norm(ej.nombre) for ej in self.ejercicios]
        if len(nombres) != len(set(nombres)):
            raise ValueError(
                "Hay ejercicios duplicados por nombre dentro de la rutina."
            )

    def agregar_ejercicio(self, ejercicio: Ejercicio):
        if any(_norm(ej.nombre) == _norm(ejercicio.nombre) for ej in self.ejercicios):
            raise ValueError(
                f"Ya existe un ejercicio '{ejercicio.nombre}' en la rutina."
            )
        self.ejercicios.append(ejercicio)

    def eliminar_ejercicio(self, nombre_ejercicio: str):
        key = _norm(nombre_ejercicio)
        nueva = [ej for ej in self.ejercicios if _norm(ej.nombre) != key]
        if len(nueva) == len(self.ejercicios):
            raise ValueError("No se encontró el ejercicio para eliminar.")
        if not nueva:
            raise ValueError(
                "La rutina no puede quedarse vacía; agrega otro ejercicio o cancela la eliminación."
            )
        self.ejercicios = nueva

    def actualizar_datos(
        self, nombre: Optional[str] = None, descripcion: Optional[str] = None
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

    def actualizar_ejercicio(
        self,
        nombre_ejercicio: str,
        repeticiones: Optional[int] = None,
        series: Optional[int] = None,
    ):
        ej = self._buscar(nombre_ejercicio)
        ej.actualizar(repeticiones, series)

    def _buscar(self, nombre_ejercicio: str) -> Ejercicio:
        key = _norm(nombre_ejercicio)
        for ej in self.ejercicios:
            if _norm(ej.nombre) == key:
                return ej
        raise ValueError("Ejercicio no encontrado en la rutina.")

    def duracion_total_min(self) -> float:
        return sum(ej.duracion_minutos() for ej in self.ejercicios)

    def __str__(self) -> str:
        return (
            f"Rutina: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
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
        if self.edad < 16:
            raise ValueError("La edad debe ser un número mayor o igual a 16 años.")

    def asignar_rutina(self, rutina: Rutina):
        if any(_norm(r.nombre) == _norm(rutina.nombre) for r in self.rutinas):
            raise ValueError(
                f"El usuario ya tiene una rutina llamada '{rutina.nombre}'."
            )
        self.rutinas.append(rutina)

    def __str__(self) -> str:
        return (
            f"Usuario: {self.nombre} | Edad: {self.edad} | Rutinas: {len(self.rutinas)}"
        )


class SistemaGestion:
    """
    Optimizado con índices O(1):
      - self.idx_usuarios: Dict[str, Usuario]      (clave = nombre normalizado)
      - self.idx_ejercicios: Dict[str, Ejercicio]
      - self.idx_rutinas: Dict[str, Rutina]
    Se mantienen listas para listar en pantalla conservando el orden de alta.
    """

    def __init__(self):
        self.usuarios: List[Usuario] = []
        self.ejercicios_catalogo: List[Ejercicio] = []
        self.rutinas: List[Rutina] = []

        self.idx_usuarios: Dict[str, Usuario] = {}
        self.idx_ejercicios: Dict[str, Ejercicio] = {}
        self.idx_rutinas: Dict[str, Rutina] = {}

    # --------- Helpers I/O ---------
    @staticmethod
    def _input_no_vacio(msg: str) -> str:
        while True:
            txt = input(msg).strip()
            if txt:
                return txt
            print("El valor no puede estar vacío.")

    @staticmethod
    def _input_int(msg: str, minimo: Optional[int] = None) -> int:
        while True:
            try:
                val = int(input(msg).strip())
                if minimo is not None and val < minimo:
                    print(f"El valor debe ser mayor o igual a {minimo}.")
                    continue
                return val
            except ValueError:
                print("Ingresa un número entero válido.")

    # -------- Usuarios --------
    def _buscar_usuario(self, nombre: str) -> Optional[Usuario]:
        return self.idx_usuarios.get(_norm(nombre))

    def agregar_usuario(self, nombre: str, edad: int):
        key = _norm(nombre)
        if key in self.idx_usuarios:
            raise ValueError("Ya existe un usuario con ese nombre.")
        u = Usuario(nombre, edad)
        self.idx_usuarios[key] = u
        self.usuarios.append(u)

    def listar_usuarios(self):
        if not self.usuarios:
            print("No hay usuarios.")
            return
        for u in self.usuarios:
            print(u)

    def mostrar_rutinas_de_usuario(self, nombre_usuario: str):
        u = self._buscar_usuario(nombre_usuario)
        if not u:
            print("Usuario no encontrado.")
        elif not u.rutinas:
            print(f"{u.nombre} no tiene rutinas asignadas.")
        else:
            print(f"Rutinas de {u.nombre}:")
            for r in u.rutinas:
                print(f"  - {r.nombre}: {minutos_a_texto(r.duracion_total_min())}")

    # -------- Ejercicios (catálogo) --------
    def _buscar_ejercicio_catalogo(self, nombre: str) -> Optional[Ejercicio]:
        return self.idx_ejercicios.get(_norm(nombre))

    def crear_ejercicio(self, nombre: str, repeticiones: int, series: int):
        key = _norm(nombre)
        if key in self.idx_ejercicios:
            raise ValueError("Ya existe un ejercicio en el catálogo con ese nombre.")
        ej = Ejercicio(nombre, repeticiones, series)
        self.idx_ejercicios[key] = ej
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
        key = _norm(nombre)
        ej = self.idx_ejercicios.pop(key, None)
        if ej is None:
            raise ValueError("No se encontró el ejercicio para eliminar.")
        # quitar de la lista manteniendo orden
        self.ejercicios_catalogo = [e for e in self.ejercicios_catalogo if e is not ej]
        # también eliminarlo de las rutinas donde esté (sin dejar vacías)
        for r in self.rutinas:
            try:
                r.eliminar_ejercicio(ej.nombre)
            except ValueError:
                # si no estaba o la eliminación lo dejaría vacío, ignoramos:
                # (política: no romper rutinas al borrar del catálogo si quedaría vacía)
                pass

    def obtener_ejercicios_por_nombres(self, nombres: List[str]) -> List[Ejercicio]:
        res: List[Ejercicio] = []
        vistos = set()
        for n in nombres:
            key = _norm(n)
            if key in vistos:
                raise ValueError(
                    f"Nombre de ejercicio repetido en la selección: '{n}'."
                )
            vistos.add(key)
            ej = self.idx_ejercicios.get(key)
            if ej is None:
                raise ValueError(f"Ejercicio '{n}' no existe en el catálogo.")
            res.append(ej)
        return res

    # -------- Rutinas --------
    def _buscar_rutina(self, nombre: str) -> Optional[Rutina]:
        return self.idx_rutinas.get(_norm(nombre))

    def crear_rutina(
        self, nombre: str, descripcion: str, nombres_ejercicios: List[str]
    ):
        if not self.ejercicios_catalogo:
            raise ValueError("Primero crea ejercicios en el catálogo.")
        if not nombres_ejercicios:
            raise ValueError("Debes seleccionar al menos un ejercicio para la rutina.")
        key = _norm(nombre)
        if key in self.idx_rutinas:
            raise ValueError("Ya existe una rutina con ese nombre.")
        ejercicios = self.obtener_ejercicios_por_nombres(nombres_ejercicios)
        r = Rutina(nombre, descripcion, ejercicios)
        self.idx_rutinas[key] = r
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

    def editar_rutina(
        self,
        nombre: str,
        nuevo_nombre: Optional[str] = None,
        nueva_desc: Optional[str] = None,
    ):
        r = self._buscar_rutina(nombre)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        old_key = _norm(r.nombre)
        r.actualizar_datos(nuevo_nombre, nueva_desc)
        # si cambió el nombre, actualizamos índice
        new_key = _norm(r.nombre)
        if new_key != old_key:
            if new_key in self.idx_rutinas:
                raise ValueError("Ya existe otra rutina con ese nombre.")
            self.idx_rutinas.pop(old_key, None)
            self.idx_rutinas[new_key] = r

    def rutina_agregar_ejercicio(self, nombre_rutina: str, nombre_ejercicio: str):
        r = self._buscar_rutina(nombre_rutina)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        ej = self._buscar_ejercicio_catalogo(nombre_ejercicio)
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

    # -------- Asignación y Reporte --------
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

    # -------- Menús de terminal (mismos textos) --------
    def menu(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1) Usuarios")
            print("2) Ejercicios (catálogo)")
            print("3) Rutinas")
            print("4) Asignar rutina a usuario")
            print("5) Mostrar rutinas de un usuario")
            print("6) Reporte por usuario")
            print("7) Salir")
            op = input("Opción: ").strip()
            try:
                if op == "1":
                    self.menu_usuarios()
                elif op == "2":
                    self.menu_ejercicios()
                elif op == "3":
                    self.menu_rutinas()
                elif op == "4":
                    while True:
                        u = input("Usuario: ").strip()
                        if not u:
                            print("El nombre de usuario no puede estar vacío.")
                            continue
                        break
                    while True:
                        r = input("Rutina: ").strip()
                        if not r:
                            print("El nombre de la rutina no puede estar vacío.")
                            continue
                        break
                    self.asignar_rutina_a_usuario(u, r)
                    print("Rutina asignada.")
                elif op == "5":
                    nombre = input("Usuario: ").strip()
                    self.mostrar_rutinas_de_usuario(nombre)
                elif op == "6":
                    self.reporte_por_usuario()
                elif op == "7":
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
            print("3) Editar usuario")
            print("4) Volver")
            op = input("Opción: ").strip()
            if op == "1":
                while True:
                    nombre = self._input_no_vacio("Nombre: ")
                    if self._buscar_usuario(nombre):
                        print("Ya existe un usuario con ese nombre. Intenta otro.")
                    else:
                        break
                edad = self._input_int("Edad: ", minimo=16)
                try:
                    self.agregar_usuario(nombre, edad)
                    print("Usuario agregado.")
                except ValueError as e:
                    print(f"[Error] {e}")
            elif op == "2":
                self.listar_usuarios()
            elif op == "3":
                nombre = self._input_no_vacio("Nombre del usuario a editar: ")
                usuario = self._buscar_usuario(nombre)
                if usuario is None:
                    print("No existe ese usuario.")
                    continue
                while True:
                    print(f"\nEditando usuario: {usuario.nombre}")
                    print("1) Cambiar nombre")
                    print("2) Cambiar edad")
                    print("3) Volver")
                    subop = input("Opción: ").strip()
                    if subop == "1":
                        nuevo = self._input_no_vacio("Nuevo nombre: ")
                        if self._buscar_usuario(nuevo):
                            print("Ya existe un usuario con ese nombre.")
                            continue
                        # actualizar índice
                        old_key = _norm(usuario.nombre)
                        usuario.nombre = nuevo.strip()
                        self.idx_usuarios.pop(old_key, None)
                        self.idx_usuarios[_norm(usuario.nombre)] = usuario
                        print("Nombre actualizado.")
                    elif subop == "2":
                        usuario.edad = self._input_int("Nueva edad: ", minimo=16)
                        print("Edad actualizada.")
                    elif subop == "3":
                        break
                    else:
                        print("Opción no válida.")
            elif op == "4":
                return
            else:
                print("Opción no válida.")

    def menu_ejercicios(self):
        while True:
            print("\n--- Ejercicios (catálogo) ---")
            print("1) Crear ejercicio")
            print("2) Listar ejercicios")
            print("3) Editar ejercicio")
            print("4) Eliminar ejercicio")
            print("5) Volver")
            op = input("Opción: ").strip()
            if op == "1":
                while True:
                    nombre = self._input_no_vacio("Nombre: ")
                    if self._buscar_ejercicio_catalogo(nombre):
                        print("Ya existe un ejercicio con ese nombre. Intenta otro.")
                    else:
                        break
                reps = self._input_int("Repeticiones: ", minimo=1)
                series = self._input_int("Series: ", minimo=1)
                try:
                    self.crear_ejercicio(nombre, reps, series)
                except ValueError as e:
                    print(f"[Error] {e}")
            elif op == "2":
                self.listar_ejercicios()
            elif op == "3":
                nombre = self._input_no_vacio("Nombre del ejercicio a editar: ")
                ejercicio = self._buscar_ejercicio_catalogo(nombre)
                if ejercicio is None:
                    print("No existe ese ejercicio.")
                    continue
                while True:
                    print(f"\nEditando ejercicio: {ejercicio.nombre}")
                    print("1) Cambiar nombre")
                    print("2) Cambiar repeticiones")
                    print("3) Cambiar series")
                    print("4) Volver")
                    subop = input("Opción: ").strip()
                    if subop == "1":
                        nuevo = self._input_no_vacio("Nuevo nombre: ")
                        if self._buscar_ejercicio_catalogo(nuevo):
                            print("Ya existe un ejercicio con ese nombre.")
                            continue
                        old_key = _norm(ejercicio.nombre)
                        ejercicio.nombre = nuevo.strip()
                        # actualizar índice
                        self.idx_ejercicios.pop(old_key, None)
                        self.idx_ejercicios[_norm(ejercicio.nombre)] = ejercicio
                        print("Nombre actualizado.")
                    elif subop == "2":
                        ejercicio.repeticiones = self._input_int(
                            "Nuevas repeticiones: ", minimo=1
                        )
                        print("Repeticiones actualizadas.")
                    elif subop == "3":
                        ejercicio.series = self._input_int("Nuevas series: ", minimo=1)
                        print("Series actualizadas.")
                    elif subop == "4":
                        break
                    else:
                        print("Opción no válida.")
            elif op == "4":
                nombre = self._input_no_vacio("Nombre a eliminar: ")
                try:
                    self.eliminar_ejercicio(nombre)
                    print("Ejercicio eliminado del catálogo.")
                except ValueError as e:
                    print(f"[Error] {e}")
            elif op == "5":
                return
            else:
                print("Opción no válida.")

    def menu_rutinas(self):
        while True:
            print("\n--- Rutinas ---")
            print("1) Crear rutina (seleccionando ejercicios del catálogo)")
            print("2) Listar rutinas")
            print("3) Editar rutina")
            print("4) Volver")
            op = input("Opción: ").strip()
            if op == "1":
                if not self.ejercicios_catalogo:
                    print("Primero crea ejercicios en el catálogo.")
                    continue
                while True:
                    nombre = self._input_no_vacio("Nombre de la rutina: ")
                    if self._buscar_rutina(nombre):
                        print("Ya existe una rutina con ese nombre. Intenta otro.")
                    else:
                        break
                desc = self._input_no_vacio("Descripción: ")
                print("\nEjercicios disponibles (separa por coma):")
                self.listar_ejercicios()
                while True:
                    sel = input("Nombres a incluir (separados por coma): ").strip()
                    nombres = [n.strip() for n in sel.split(",") if n.strip()]
                    if not nombres:
                        print("Debes seleccionar al menos un ejercicio.")
                        continue
                    try:
                        self.crear_rutina(nombre, desc, nombres)
                        print("Rutina creada.")
                        break
                    except ValueError as e:
                        print(f"[Error] {e}")
            elif op == "2":
                self.listar_rutinas()
            elif op == "3":
                nombre = self._input_no_vacio("Nombre de la rutina a editar: ")
                r = self._buscar_rutina(nombre)
                if r is None:
                    print("No existe esa rutina.")
                    continue
                self.submenu_editar_rutina(r)
            elif op == "4":
                return
            else:
                print("Opción no válida.")

    def submenu_editar_rutina(self, r: Rutina):
        while True:
            print(f"\n>>> Editando: {r.nombre}")
            print("1) Agregar ejercicio (del catálogo)")
            print("2) Eliminar ejercicio")
            print("3) Actualizar reps/series de un ejercicio")
            print("4) Modificar nombre/descr.")
            print("5) Ver duración total")
            print("6) Listar ejercicios")
            print("7) Volver")
            op = input("Opción: ").strip()
            if op == "1":
                if not self.ejercicios_catalogo:
                    print("Catálogo vacío. Crea ejercicios primero.")
                    continue
                self.listar_ejercicios()
                nombre = self._input_no_vacio("Nombre del ejercicio a agregar: ")
                try:
                    self.rutina_agregar_ejercicio(r.nombre, nombre)
                    print("Ejercicio agregado a la rutina.")
                except ValueError as e:
                    print(f"[Error] {e}")
            elif op == "2":
                nombre = self._input_no_vacio("Nombre del ejercicio a eliminar: ")
                try:
                    self.rutina_eliminar_ejercicio(r.nombre, nombre)
                    print("Ejercicio eliminado de la rutina.")
                except ValueError as e:
                    print(f"[Error] {e}")
            elif op == "3":
                nombre = self._input_no_vacio("Ejercicio a actualizar: ")
                rep_txt = input("Nuevas repeticiones (enter para mantener): ").strip()
                ser_txt = input("Nuevas series (enter para mantener): ").strip()
                rep = None if rep_txt == "" else int(rep_txt)
                ser = None if ser_txt == "" else int(ser_txt)
                try:
                    self.rutina_actualizar_ejercicio(
                        r.nombre, nombre, repeticiones=rep, series=ser
                    )
                    print("Ejercicio actualizado.")
                except ValueError as e:
                    print(f"[Error] {e}")
            elif op == "4":
                nuevo = input("Nuevo nombre (enter=mantener): ").strip()
                desc = input("Nueva descripción (enter=mantener): ").strip()
                try:
                    self.editar_rutina(
                        r.nombre,
                        nuevo_nombre=(None if not nuevo else nuevo),
                        nueva_desc=(None if not desc else desc),
                    )
                    print("Datos actualizados.")
                except ValueError as e:
                    print(f"[Error] {e}")
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


if __name__ == "__main__":
    sistema = SistemaGestion()
    sistema.menu()
