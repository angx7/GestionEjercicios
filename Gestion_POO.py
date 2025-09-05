# fitness_oop_puro.py
from typing import List, Optional, Dict


class Parametros:
    """Parámetros globales de estimación (orientado a objetos)."""

    SEC_POR_REP: int = 5  # segundos por repetición
    DESCANSO_ENTRE_SERIES: int = 30  # segundos entre series


class Utilidades:
    """Utilidades estáticas (sin funciones sueltas en módulo)."""

    @staticmethod
    def minutos_a_texto(mins: float) -> str:
        total = int(round(mins * 60))
        m = total // 60
        s = total - (m * 60)
        return f"{m} min {s} s"

    @staticmethod
    def normalizar(s: str) -> str:
        return s.strip().lower()


class Ejercicio:
    def __init__(
        self,
        nombre: str,
        repeticiones: int,
        series: int,
        sec_por_rep: int = Parametros.SEC_POR_REP,
        descanso_entre_series: int = Parametros.DESCANSO_ENTRE_SERIES,
    ):
        self.nombre: str = nombre.strip()
        self.repeticiones: int = int(repeticiones)
        self.series: int = int(series)
        self.sec_por_rep: int = int(sec_por_rep)
        self.descanso_entre_series: int = int(descanso_entre_series)
        self._validar()

    def _validar(self) -> None:
        if self.nombre == "":
            raise ValueError("El nombre del ejercicio no puede estar vacío.")
        if self.repeticiones <= 0:
            raise ValueError("Las repeticiones deben ser mayores a 0.")
        if self.repeticiones > 100:
            raise ValueError("Las repeticiones no pueden ser mayores a 100.")
        if self.series <= 0:
            raise ValueError("Las series deben ser mayores a 0.")
        if self.series > 100:
            raise ValueError("Las series no pueden ser mayores a 100.")
        if self.sec_por_rep <= 0:
            raise ValueError("Los segundos por repetición deben ser mayores a 0.")
        if self.descanso_entre_series < 0:
            raise ValueError("El descanso entre series no puede ser negativo.")

    def cambiar_nombre(self, nuevo_nombre: str) -> None:
        nuevo = nuevo_nombre.strip()
        if nuevo == "":
            raise ValueError("El nombre del ejercicio no puede quedar vacío.")
        self.nombre = nuevo

    def actualizar(
        self, repeticiones: Optional[int] = None, series: Optional[int] = None
    ) -> None:
        if repeticiones is not None:
            if repeticiones <= 0:
                raise ValueError("Las repeticiones deben ser mayores a 0.")
            if repeticiones > 100:
                raise ValueError("Las repeticiones no pueden ser mayores a 100.")
            self.repeticiones = int(repeticiones)

        if series is not None:
            if series <= 0:
                raise ValueError("Las series deben ser mayores a 0.")
            if series > 100:
                raise ValueError("Las series no pueden ser mayores a 100.")
            self.series = int(series)

    def duracion_minutos(self) -> float:
        movimiento = self.repeticiones * self.sec_por_rep * self.series
        descanso_series = self.series - 1
        if descanso_series < 0:
            descanso_series = 0
        descanso = self.descanso_entre_series * descanso_series
        return (movimiento + descanso) / 60.0

    def __str__(self) -> str:
        return (
            f"{self.nombre} | reps: {self.repeticiones} | series: {self.series} "
            f"| estimado: {Utilidades.minutos_a_texto(self.duracion_minutos())}"
        )


class Rutina:
    def __init__(self, nombre: str, descripcion: str, ejercicios: List[Ejercicio]):
        self.nombre: str = nombre.strip()
        self.descripcion: str = descripcion.strip()
        self.ejercicios: List[Ejercicio] = []
        # Copia explícita evitando list(...) y comprensiones
        i = 0
        while i < len(ejercicios):
            self.ejercicios.append(ejercicios[i])
            i += 1
        self._validar()

    def _validar(self) -> None:
        if self.nombre == "":
            raise ValueError("El nombre de la rutina no puede estar vacío.")
        if self.descripcion == "":
            raise ValueError("La descripción de la rutina no puede estar vacía.")
        if len(self.ejercicios) == 0:
            raise ValueError("Una rutina debe tener al menos un ejercicio.")

        # Detección de duplicados sin sets ni comprensiones
        vistos: List[str] = []
        i = 0
        while i < len(self.ejercicios):
            key = Utilidades.normalizar(self.ejercicios[i].nombre)
            j = 0
            repetido = False
            while j < len(vistos):
                if key == vistos[j]:
                    repetido = True
                    break
                j += 1
            if repetido:
                raise ValueError(
                    "Hay ejercicios duplicados por nombre dentro de la rutina."
                )
            vistos.append(key)
            i += 1

    def agregar_ejercicio(self, ejercicio: Ejercicio) -> None:
        key_nuevo = Utilidades.normalizar(ejercicio.nombre)
        i = 0
        while i < len(self.ejercicios):
            if Utilidades.normalizar(self.ejercicios[i].nombre) == key_nuevo:
                raise ValueError(
                    f"Ya existe un ejercicio '{ejercicio.nombre}' en la rutina."
                )
            i += 1
        self.ejercicios.append(ejercicio)

    def eliminar_ejercicio(self, nombre_ejercicio: str) -> None:
        key = Utilidades.normalizar(nombre_ejercicio)
        nueva: List[Ejercicio] = []
        encontrado = False

        i = 0
        while i < len(self.ejercicios):
            ej = self.ejercicios[i]
            if Utilidades.normalizar(ej.nombre) == key:
                encontrado = True
            else:
                nueva.append(ej)
            i += 1

        if not encontrado:
            raise ValueError("No se encontró el ejercicio para eliminar.")
        if len(nueva) == 0:
            raise ValueError(
                "La rutina no puede quedarse vacía; agrega otro ejercicio o cancela la eliminación."
            )

        self.ejercicios = nueva

    def actualizar_datos(
        self, nombre: Optional[str] = None, descripcion: Optional[str] = None
    ) -> None:
        if nombre is not None:
            nuevo = nombre.strip()
            if nuevo == "":
                raise ValueError("El nombre de la rutina no puede quedar vacío.")
            self.nombre = nuevo
        if descripcion is not None:
            nueva = descripcion.strip()
            if nueva == "":
                raise ValueError("La descripción de la rutina no puede quedar vacía.")
            self.descripcion = nueva

    def actualizar_ejercicio(
        self,
        nombre_ejercicio: str,
        repeticiones: Optional[int] = None,
        series: Optional[int] = None,
    ) -> None:
        ej = self._buscar(nombre_ejercicio)
        ej.actualizar(repeticiones, series)

    def _buscar(self, nombre_ejercicio: str) -> Ejercicio:
        key = Utilidades.normalizar(nombre_ejercicio)
        i = 0
        while i < len(self.ejercicios):
            if Utilidades.normalizar(self.ejercicios[i].nombre) == key:
                return self.ejercicios[i]
            i += 1
        raise ValueError("Ejercicio no encontrado en la rutina.")

    def duracion_total_min(self) -> float:
        total = 0.0
        i = 0
        while i < len(self.ejercicios):
            total = total + self.ejercicios[i].duracion_minutos()
            i += 1
        return total

    def __str__(self) -> str:
        return (
            f"Rutina: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Total: {Utilidades.minutos_a_texto(self.duracion_total_min())}\n"
            f"Ejercicios: {len(self.ejercicios)}"
        )


class Usuario:
    def __init__(self, nombre: str, edad: int):
        self.nombre: str = nombre.strip()
        self.edad: int = int(edad)
        self.rutinas: List[Rutina] = []
        self._validar()

    def _validar(self) -> None:
        if self.nombre == "":
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if self.edad < 16:
            raise ValueError("La edad debe ser un número mayor o igual a 16 años.")
        if self.edad > 100:
            raise ValueError("La edad debe ser menor o igual a 100 años.")

    def cambiar_nombre(self, nuevo_nombre: str) -> None:
        nuevo = nuevo_nombre.strip()
        if nuevo == "":
            raise ValueError("El nombre del usuario no puede quedar vacío.")
        self.nombre = nuevo

    def cambiar_edad(self, nueva_edad: int) -> None:
        if nueva_edad < 16:
            raise ValueError("La edad debe ser un número mayor o igual a 16 años.")
        if nueva_edad > 100:
            raise ValueError("La edad debe ser menor o igual a 100 años.")
        self.edad = int(nueva_edad)

    def asignar_rutina(self, rutina: Rutina) -> None:
        # Evita duplicados por nombre de rutina
        key_rutina = Utilidades.normalizar(rutina.nombre)
        i = 0
        while i < len(self.rutinas):
            if Utilidades.normalizar(self.rutinas[i].nombre) == key_rutina:
                raise ValueError(
                    f"El usuario ya tiene una rutina llamada '{rutina.nombre}'."
                )
            i += 1
        self.rutinas.append(rutina)

    def __str__(self) -> str:
        return (
            f"Usuario: {self.nombre} | Edad: {self.edad} | Rutinas: {len(self.rutinas)}"
        )


class SistemaGestion:
    """
    Implementación 100% POO sin atajos “pythonicos”.
    - Índices O(1) (diccionarios) para búsquedas por nombre normalizado.
    - Listas para preservar orden de alta.
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
            if txt != "":
                return txt
            print("El valor no puede estar vacío.")

    @staticmethod
    def _input_int(
        msg: str, minimo: Optional[int] = None, maximo: Optional[int] = None
    ) -> int:
        while True:
            texto = input(msg).strip()
            try:
                val = int(texto)
                if (minimo is not None) and (val < minimo):
                    print(f"El valor debe ser mayor o igual a {minimo}.")
                elif (maximo is not None) and (val > maximo):
                    print(f"El valor debe ser menor o igual a {maximo}.")
                else:
                    return val
            except ValueError:
                print("Ingresa un número entero válido.")

    # -------- Usuarios --------
    def _buscar_usuario(self, nombre: str) -> Optional[Usuario]:
        return self.idx_usuarios.get(Utilidades.normalizar(nombre))

    def agregar_usuario(self, nombre: str, edad: int) -> None:
        key = Utilidades.normalizar(nombre)
        if key in self.idx_usuarios:
            raise ValueError("Ya existe un usuario con ese nombre.")
        u = Usuario(nombre, edad)
        self.idx_usuarios[key] = u
        self.usuarios.append(u)

    def listar_usuarios(self) -> None:
        if len(self.usuarios) == 0:
            print("No hay usuarios.")
            return
        i = 0
        while i < len(self.usuarios):
            print(self.usuarios[i])
            i += 1

    def mostrar_rutinas_de_usuario(self, nombre_usuario: str) -> None:
        u = self._buscar_usuario(nombre_usuario)
        if u is None:
            print("Usuario no encontrado.")
            return
        if len(u.rutinas) == 0:
            print(f"{u.nombre} no tiene rutinas asignadas.")
            return
        print(f"Rutinas de {u.nombre}:")
        i = 0
        while i < len(u.rutinas):
            r = u.rutinas[i]
            print(
                "  - "
                + r.nombre
                + ": "
                + Utilidades.minutos_a_texto(r.duracion_total_min())
            )
            i += 1

    # -------- Ejercicios (catálogo) --------
    def _buscar_ejercicio_catalogo(self, nombre: str) -> Optional[Ejercicio]:
        return self.idx_ejercicios.get(Utilidades.normalizar(nombre))

    def crear_ejercicio(self, nombre: str, repeticiones: int, series: int) -> None:
        key = Utilidades.normalizar(nombre)
        if key in self.idx_ejercicios:
            raise ValueError("Ya existe un ejercicio en el catálogo con ese nombre.")
        ej = Ejercicio(nombre, repeticiones, series)
        self.idx_ejercicios[key] = ej
        self.ejercicios_catalogo.append(ej)
        print(
            "Ejercicio creado. Duración estimada: "
            + Utilidades.minutos_a_texto(ej.duracion_minutos())
        )

    def listar_ejercicios(self) -> None:
        if len(self.ejercicios_catalogo) == 0:
            print("(Catálogo vacío)")
            return
        i = 0
        while i < len(self.ejercicios_catalogo):
            print("- " + str(self.ejercicios_catalogo[i]))
            i += 1

    def eliminar_ejercicio(self, nombre: str) -> None:
        key = Utilidades.normalizar(nombre)
        ej = self.idx_ejercicios.pop(key, None)
        if ej is None:
            raise ValueError("No se encontró el ejercicio para eliminar.")

        # Quitar de la lista manteniendo orden (sin comprensiones)
        nueva: List[Ejercicio] = []
        i = 0
        while i < len(self.ejercicios_catalogo):
            if self.ejercicios_catalogo[i] is not ej:
                nueva.append(self.ejercicios_catalogo[i])
            i += 1
        self.ejercicios_catalogo = nueva

        # Intentar eliminar de las rutinas donde esté (sin romper rutinas si quedan vacías)
        i = 0
        while i < len(self.rutinas):
            try:
                self.rutinas[i].eliminar_ejercicio(ej.nombre)
            except ValueError:
                # Ignorar si no estaba o si la rutina quedaría vacía (política: no romper rutinas)
                pass
            i += 1

    def obtener_ejercicios_por_nombres(self, nombres: List[str]) -> List[Ejercicio]:
        res: List[Ejercicio] = []
        vistos: List[str] = []
        i = 0
        while i < len(nombres):
            n = nombres[i]
            key = Utilidades.normalizar(n)

            # Detectar repetidos en selección
            j = 0
            repetido = False
            while j < len(vistos):
                if key == vistos[j]:
                    repetido = True
                    break
                j += 1
            if repetido:
                raise ValueError(
                    "Nombre de ejercicio repetido en la selección: '" + n + "'."
                )

            ej = self.idx_ejercicios.get(key)
            if ej is None:
                raise ValueError("Ejercicio '" + n + "' no existe en el catálogo.")

            res.append(ej)
            vistos.append(key)
            i += 1
        return res

    # -------- Rutinas --------
    def _buscar_rutina(self, nombre: str) -> Optional[Rutina]:
        return self.idx_rutinas.get(Utilidades.normalizar(nombre))

    def crear_rutina(
        self, nombre: str, descripcion: str, nombres_ejercicios: List[str]
    ) -> None:
        if len(self.ejercicios_catalogo) == 0:
            raise ValueError("Primero crea ejercicios en el catálogo.")
        if len(nombres_ejercicios) == 0:
            raise ValueError("Debes seleccionar al menos un ejercicio para la rutina.")

        key = Utilidades.normalizar(nombre)
        if key in self.idx_rutinas:
            raise ValueError("Ya existe una rutina con ese nombre.")

        ejercicios = self.obtener_ejercicios_por_nombres(nombres_ejercicios)
        r = Rutina(nombre, descripcion, ejercicios)
        self.idx_rutinas[key] = r
        self.rutinas.append(r)

    def listar_rutinas(self) -> None:
        if len(self.rutinas) == 0:
            print("No hay rutinas.")
            return
        print("-" * 60)
        i = 0
        while i < len(self.rutinas):
            r = self.rutinas[i]
            print(r)
            k = 0
            while k < len(r.ejercicios):
                print("  • " + str(r.ejercicios[k]))
                k += 1
            print("-" * 60)
            i += 1

    def editar_rutina(
        self,
        nombre: str,
        nuevo_nombre: Optional[str] = None,
        nueva_desc: Optional[str] = None,
    ) -> None:
        r = self._buscar_rutina(nombre)
        if r is None:
            raise ValueError("Rutina no encontrada.")

        old_key = Utilidades.normalizar(r.nombre)

        # Verifica nombre duplicado ANTES de cambiar (para no dejar estado inconsistente)
        if nuevo_nombre is not None:
            propuesto_key = Utilidades.normalizar(nuevo_nombre)
            if (propuesto_key != old_key) and (propuesto_key in self.idx_rutinas):
                raise ValueError("Ya existe otra rutina con ese nombre.")

        r.actualizar_datos(nuevo_nombre, nueva_desc)

        new_key = Utilidades.normalizar(r.nombre)
        if new_key != old_key:
            self.idx_rutinas.pop(old_key, None)
            self.idx_rutinas[new_key] = r

    def rutina_agregar_ejercicio(
        self, nombre_rutina: str, nombre_ejercicio: str
    ) -> None:
        r = self._buscar_rutina(nombre_rutina)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        ej = self._buscar_ejercicio_catalogo(nombre_ejercicio)
        if ej is None:
            raise ValueError("Ese ejercicio no existe en el catálogo.")
        r.agregar_ejercicio(ej)

    def rutina_eliminar_ejercicio(
        self, nombre_rutina: str, nombre_ejercicio: str
    ) -> None:
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
    ) -> None:
        r = self._buscar_rutina(nombre_rutina)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        r.actualizar_ejercicio(nombre_ejercicio, repeticiones, series)

    # -------- Asignación y Reporte --------
    def asignar_rutina_a_usuario(self, nombre_usuario: str, nombre_rutina: str) -> None:
        u = self._buscar_usuario(nombre_usuario)
        if u is None:
            raise ValueError("Usuario no encontrado.")
        r = self._buscar_rutina(nombre_rutina)
        if r is None:
            raise ValueError("Rutina no encontrada.")
        u.asignar_rutina(r)

    def reporte_por_usuario(self) -> None:
        if len(self.usuarios) == 0:
            print("No hay usuarios.")
            return
        print("=" * 60)
        i = 0
        while i < len(self.usuarios):
            u = self.usuarios[i]
            print("Usuario: " + u.nombre + " | Edad: " + str(u.edad))
            if len(u.rutinas) == 0:
                print("  (Sin rutinas asignadas)")
            else:
                j = 0
                while j < len(u.rutinas):
                    r = u.rutinas[j]
                    print(
                        "  - "
                        + r.nombre
                        + ": "
                        + Utilidades.minutos_a_texto(r.duracion_total_min())
                    )
                    j += 1
            print("=" * 60)
            i += 1

    # -------- Menús de terminal --------
    def menu(self) -> None:
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
                    u = self._input_no_vacio("Usuario: ")
                    print("\nRutinas disponibles:")
                    self.listar_rutinas()
                    r = self._input_no_vacio("Rutinas (separadas por coma): ")
                    # Parseo explícito
                    nombres_rutinas: List[str] = []
                    tmp = r.split(",")
                    i = 0
                    while i < len(tmp):
                        n = tmp[i].strip()
                        if n != "":
                            nombres_rutinas.append(n)
                        i += 1
                    errores: List[str] = []
                    i = 0
                    while i < len(nombres_rutinas):
                        nombre_r = nombres_rutinas[i]
                        try:
                            self.asignar_rutina_a_usuario(u, nombre_r)
                        except ValueError as e:
                            errores.append(nombre_r + ": " + str(e))
                        i += 1
                    if len(errores) > 0:
                        print("Algunos errores al asignar rutinas:")
                        j = 0
                        while j < len(errores):
                            print("  [Error] " + errores[j])
                            j += 1
                    else:
                        print("Rutinas asignadas.")
                elif op == "5":
                    nombre = self._input_no_vacio("Usuario: ")
                    self.mostrar_rutinas_de_usuario(nombre)
                elif op == "6":
                    self.reporte_por_usuario()
                elif op == "7":
                    print("Hasta luego.")
                    break
                else:
                    print("Opción no válida.")
            except ValueError as e:
                print("[Error] " + str(e))

    def menu_usuarios(self) -> None:
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
                    if self._buscar_usuario(nombre) is not None:
                        print("Ya existe un usuario con ese nombre. Intenta otro.")
                    else:
                        break
                edad = self._input_int("Edad: ", minimo=16, maximo=100)
                try:
                    self.agregar_usuario(nombre, edad)
                    print("Usuario agregado.")
                except ValueError as e:
                    print("[Error] " + str(e))
            elif op == "2":
                self.listar_usuarios()
            elif op == "3":
                nombre = self._input_no_vacio("Nombre del usuario a editar: ")
                usuario = self._buscar_usuario(nombre)
                if usuario is None:
                    print("No existe ese usuario.")
                    continue
                while True:
                    print("\nEditando usuario: " + usuario.nombre)
                    print("1) Cambiar nombre")
                    print("2) Cambiar edad")
                    print("3) Volver")
                    subop = input("Opción: ").strip()
                    if subop == "1":
                        nuevo = self._input_no_vacio("Nuevo nombre: ")
                        if self._buscar_usuario(nuevo) is not None:
                            print("Ya existe un usuario con ese nombre.")
                            continue
                        old_key = Utilidades.normalizar(usuario.nombre)
                        try:
                            usuario.cambiar_nombre(nuevo)
                        except ValueError as e:
                            print("[Error] " + str(e))
                            continue
                        self.idx_usuarios.pop(old_key, None)
                        self.idx_usuarios[Utilidades.normalizar(usuario.nombre)] = (
                            usuario
                        )
                        print("Nombre actualizado.")
                    elif subop == "2":
                        try:
                            nueva_edad = self._input_int(
                                "Nueva edad: ", minimo=16, maximo=100
                            )
                            usuario.cambiar_edad(nueva_edad)
                            print("Edad actualizada.")
                        except ValueError as e:
                            print("[Error] " + str(e))
                    elif subop == "3":
                        break
                    else:
                        print("Opción no válida.")
            elif op == "4":
                return
            else:
                print("Opción no válida.")

    def menu_ejercicios(self) -> None:
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
                    if self._buscar_ejercicio_catalogo(nombre) is not None:
                        print("Ya existe un ejercicio con ese nombre. Intenta otro.")
                    else:
                        break
                reps = self._input_int("Repeticiones: ", minimo=1, maximo=100)
                series = self._input_int("Series: ", minimo=1, maximo=100)
                try:
                    self.crear_ejercicio(nombre, reps, series)
                except ValueError as e:
                    print("[Error] " + str(e))
            elif op == "2":
                self.listar_ejercicios()
            elif op == "3":
                nombre = self._input_no_vacio("Nombre del ejercicio a editar: ")
                ejercicio = self._buscar_ejercicio_catalogo(nombre)
                if ejercicio is None:
                    print("No existe ese ejercicio.")
                    continue
                while True:
                    print("\nEditando ejercicio: " + ejercicio.nombre)
                    print("1) Cambiar nombre")
                    print("2) Cambiar repeticiones")
                    print("3) Cambiar series")
                    print("4) Volver")
                    subop = input("Opción: ").strip()
                    if subop == "1":
                        nuevo = self._input_no_vacio("Nuevo nombre: ")
                        if self._buscar_ejercicio_catalogo(nuevo) is not None:
                            print("Ya existe un ejercicio con ese nombre.")
                            continue
                        old_key = Utilidades.normalizar(ejercicio.nombre)
                        try:
                            ejercicio.cambiar_nombre(nuevo)
                        except ValueError as e:
                            print("[Error] " + str(e))
                            continue
                        self.idx_ejercicios.pop(old_key, None)
                        self.idx_ejercicios[Utilidades.normalizar(ejercicio.nombre)] = (
                            ejercicio
                        )
                        print("Nombre actualizado.")
                    elif subop == "2":
                        try:
                            nuevas_reps = self._input_int(
                                "Nuevas repeticiones: ", minimo=1, maximo=100
                            )
                            ejercicio.actualizar(repeticiones=nuevas_reps)
                            print("Repeticiones actualizadas.")
                        except ValueError as e:
                            print("[Error] " + str(e))
                    elif subop == "3":
                        try:
                            nuevas_series = self._input_int(
                                "Nuevas series: ", minimo=1, maximo=100
                            )
                            ejercicio.actualizar(series=nuevas_series)
                            print("Series actualizadas.")
                        except ValueError as e:
                            print("[Error] " + str(e))
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
                    print("[Error] " + str(e))
            elif op == "5":
                return
            else:
                print("Opción no válida.")

    def menu_rutinas(self) -> None:
        while True:
            print("\n--- Rutinas ---")
            print("1) Crear rutina (seleccionando ejercicios del catálogo)")
            print("2) Listar rutinas")
            print("3) Editar rutina")
            print("4) Volver")
            op = input("Opción: ").strip()
            if op == "1":
                if len(self.ejercicios_catalogo) == 0:
                    print("Primero crea ejercicios en el catálogo.")
                    continue
                while True:
                    nombre = self._input_no_vacio("Nombre de la rutina: ")
                    if self._buscar_rutina(nombre) is not None:
                        print("Ya existe una rutina con ese nombre. Intenta otro.")
                    else:
                        break
                desc = self._input_no_vacio("Descripción: ")
                print("\nEjercicios disponibles (separa por coma):")
                self.listar_ejercicios()
                while True:
                    sel = input("Nombres a incluir (separados por coma): ").strip()
                    tmp = sel.split(",")
                    nombres: List[str] = []
                    i = 0
                    while i < len(tmp):
                        n = tmp[i].strip()
                        if n != "":
                            nombres.append(n)
                        i += 1
                    if len(nombres) == 0:
                        print("Debes seleccionar al menos un ejercicio.")
                        continue
                    try:
                        self.crear_rutina(nombre, desc, nombres)
                        print("Rutina creada.")
                        break
                    except ValueError as e:
                        print("[Error] " + str(e))
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

    def submenu_editar_rutina(self, r: Rutina) -> None:
        while True:
            print("\n>>> Editando: " + r.nombre)
            print("1) Agregar ejercicio (del catálogo)")
            print("2) Eliminar ejercicio")
            print("3) Actualizar reps/series de un ejercicio")
            print("4) Modificar nombre/descr.")
            print("5) Ver duración total")
            print("6) Listar ejercicios")
            print("7) Volver")
            op = input("Opción: ").strip()
            if op == "1":
                if len(self.ejercicios_catalogo) == 0:
                    print("Catálogo vacío. Crea ejercicios primero.")
                    continue
                self.listar_ejercicios()
                nombre = self._input_no_vacio("Nombre del ejercicio a agregar: ")
                try:
                    self.rutina_agregar_ejercicio(r.nombre, nombre)
                    print("Ejercicio agregado a la rutina.")
                except ValueError as e:
                    print("[Error] " + str(e))
            elif op == "2":
                nombre = self._input_no_vacio("Nombre del ejercicio a eliminar: ")
                try:
                    self.rutina_eliminar_ejercicio(r.nombre, nombre)
                    print("Ejercicio eliminado de la rutina.")
                except ValueError as e:
                    print("[Error] " + str(e))
            elif op == "3":
                nombre = self._input_no_vacio("Ejercicio a actualizar: ")
                rep_txt = input("Nuevas repeticiones (enter para mantener): ").strip()
                ser_txt = input("Nuevas series (enter para mantener): ").strip()
                rep = None
                ser = None
                if rep_txt != "":
                    rep = int(rep_txt)
                if ser_txt != "":
                    ser = int(ser_txt)
                try:
                    self.rutina_actualizar_ejercicio(
                        r.nombre, nombre, repeticiones=rep, series=ser
                    )
                    print("Ejercicio actualizado.")
                except ValueError as e:
                    print("[Error] " + str(e))
            elif op == "4":
                nuevo = input("Nuevo nombre (enter=mantener): ").strip()
                desc = input("Nueva descripción (enter=mantener): ").strip()
                try:
                    self.editar_rutina(
                        r.nombre,
                        nuevo_nombre=(None if nuevo == "" else nuevo),
                        nueva_desc=(None if desc == "" else desc),
                    )
                    print("Datos actualizados.")
                except ValueError as e:
                    print("[Error] " + str(e))
            elif op == "5":
                print(
                    "Duración total: "
                    + Utilidades.minutos_a_texto(r.duracion_total_min())
                )
            elif op == "6":
                if len(r.ejercicios) == 0:
                    print("(Sin ejercicios)")
                else:
                    i = 0
                    while i < len(r.ejercicios):
                        print("  • " + str(r.ejercicios[i]))
                        i += 1
            elif op == "7":
                return
            else:
                print("Opción no válida.")


if __name__ == "__main__":
    sistema = SistemaGestion()
    try:
        sistema.menu()
    except KeyboardInterrupt:
        print("\n¡Hasta luego!")
