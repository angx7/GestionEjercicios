from __future__ import annotations
from typing import Optional, Dict, List, Tuple
from functools import reduce

# -------------------- Constantes y utilidades --------------------

SEC_POR_REP = 5
DESCANSO_ENTRE_SERIES = 30


def minutos_a_texto(mins: float) -> str:
    total = int(round(mins * 60))
    m, s = divmod(total, 60)
    return f"{m} min {s} s"


def _norm(s: str) -> str:
    return s.strip().lower()


# -------------------- Tipos de datos inmutables (dicts) --------------------
# Usamos dicts (estilo récord inmutable por convención: no mutar en sitio)


# Ejercicio: {nombre, repeticiones, series, sec_por_rep, descanso_entre_series}
def mk_ejercicio(
    nombre: str,
    repeticiones: int,
    series: int,
    sec_por_rep: int = SEC_POR_REP,
    descanso_entre_series: int = DESCANSO_ENTRE_SERIES,
) -> Dict:
    e = {
        "nombre": nombre.strip(),
        "repeticiones": int(repeticiones),
        "series": int(series),
        "sec_por_rep": int(sec_por_rep),
        "descanso_entre_series": int(descanso_entre_series),
    }
    validar_ejercicio(e)
    return e


def validar_ejercicio(e: Dict) -> None:
    if not e["nombre"]:
        raise ValueError("El nombre del ejercicio no puede estar vacío.")
    if e["repeticiones"] <= 0:
        raise ValueError("Las repeticiones deben ser mayores a 0.")
    if e["repeticiones"] > 100:
        raise ValueError("Las repeticiones no pueden ser mayores a 100.")
    if e["series"] <= 0:
        raise ValueError("Las series deben ser mayores a 0.")
    if e["series"] > 100:
        raise ValueError("Las series no pueden ser mayores a 100.")
    if e["sec_por_rep"] <= 0 or e["descanso_entre_series"] < 0:
        raise ValueError("Tiempos inválidos para el ejercicio.")


def duracion_ejercicio_min(e: Dict) -> float:
    movimiento = e["repeticiones"] * e["sec_por_rep"] * e["series"]
    descanso = e["descanso_entre_series"] * max(0, e["series"] - 1)
    return (movimiento + descanso) / 60.0


def str_ejercicio(e: Dict) -> str:
    return (
        f'{e["nombre"]} | reps: {e["repeticiones"]} | series: {e["series"]} '
        f"| estimado: {minutos_a_texto(duracion_ejercicio_min(e))}"
    )


def actualizar_ejercicio(
    e: Dict, rep: Optional[int] = None, ser: Optional[int] = None
) -> Dict:
    nuevo = dict(e)
    if rep is not None:
        if rep <= 0:
            raise ValueError("Las repeticiones deben ser mayores a 0.")
        nuevo["repeticiones"] = rep
    if ser is not None:
        if ser <= 0:
            raise ValueError("Las series deben ser mayores a 0.")
        nuevo["series"] = ser
    validar_ejercicio(nuevo)
    return nuevo


# Rutina: {nombre, descripcion, ejercicios: List[Ejercicio]}
def mk_rutina(nombre: str, descripcion: str, ejercicios: List[Dict]) -> Dict:
    r = {
        "nombre": nombre.strip(),
        "descripcion": descripcion.strip(),
        "ejercicios": list(ejercicios),
    }
    validar_rutina(r)
    return r


def validar_rutina(r: Dict) -> None:
    if not r["nombre"]:
        raise ValueError("El nombre de la rutina no puede estar vacío.")
    if not r["descripcion"]:
        raise ValueError("La descripción de la rutina no puede estar vacía.")
    if not r["ejercicios"]:
        raise ValueError("Una rutina debe tener al menos un ejercicio.")
    nombres = list(map(lambda ej: _norm(ej["nombre"]), r["ejercicios"]))

    # verificar duplicados con reduce
    def acum_dups(acc: Tuple[set, bool], nom: str) -> Tuple[set, bool]:
        vistos, dup = acc
        return (vistos | {nom}, dup or (nom in vistos))

    _, hay_dup = reduce(acum_dups, nombres, (set(), False))
    if hay_dup:
        raise ValueError("Hay ejercicios duplicados por nombre dentro de la rutina.")


def rutina_agregar_ejercicio(r: Dict, e: Dict) -> Dict:
    key = _norm(e["nombre"])
    existe = reduce(
        lambda acc, ej: acc or (_norm(ej["nombre"]) == key),
        r["ejercicios"],
        False,
    )
    if existe:
        raise ValueError(f"Ya existe un ejercicio '{e['nombre']}' en la rutina.")
    nueva_lista = r["ejercicios"] + [e]
    return mk_rutina(r["nombre"], r["descripcion"], nueva_lista)


def rutina_eliminar_ejercicio(r: Dict, nombre_ejercicio: str) -> Dict:
    key = _norm(nombre_ejercicio)
    # filtrar sin comprensiones
    nueva = list(filter(lambda ej: _norm(ej["nombre"]) != key, r["ejercicios"]))
    if len(nueva) == len(r["ejercicios"]):
        raise ValueError("No se encontró el ejercicio para eliminar.")
    if not nueva:
        raise ValueError(
            "La rutina no puede quedarse vacía; agrega otro ejercicio o cancela la eliminación."
        )
    return mk_rutina(r["nombre"], r["descripcion"], nueva)


def rutina_buscar_ejercicio(r: Dict, nombre_ejercicio: str) -> Dict:
    key = _norm(nombre_ejercicio)

    # búsqueda recursiva
    def go(lst: List[Dict]) -> Dict:
        if not lst:
            raise ValueError("Ejercicio no encontrado en la rutina.")
        cabeza, *resto = lst[0:1], lst[1:]
        ej = cabeza[0]
        return ej if _norm(ej["nombre"]) == key else go(resto)

    return go(r["ejercicios"])


def rutina_actualizar_ejercicio(
    r: Dict, nombre_ejercicio: str, rep: Optional[int] = None, ser: Optional[int] = None
) -> Dict:
    key = _norm(nombre_ejercicio)

    # map para reemplazar el ejercicio objetivo
    def rep_o_mismo(ej: Dict) -> Dict:
        return actualizar_ejercicio(ej, rep, ser) if _norm(ej["nombre"]) == key else ej

    nueva = list(map(rep_o_mismo, r["ejercicios"]))
    # verificar que sí existía
    igual = reduce(
        lambda acc, ej: acc and (_norm(ej["nombre"]) != key), r["ejercicios"], True
    )
    if igual:
        # ninguna coincidencia en la lista original
        raise ValueError("Ejercicio no encontrado en la rutina.")
    return mk_rutina(r["nombre"], r["descripcion"], nueva)


def rutina_duracion_total_min(r: Dict) -> float:
    return reduce(
        lambda acc, ej: acc + duracion_ejercicio_min(ej), r["ejercicios"], 0.0
    )


def str_rutina(r: Dict) -> str:
    return (
        f"Rutina: {r['nombre']}\n"
        f"Descripción: {r['descripcion']}\n"
        f"Total: {minutos_a_texto(rutina_duracion_total_min(r))}\n"
        f"Ejercicios: {len(r['ejercicios'])}"
    )


def rutina_actualizar_datos(
    r: Dict, nombre: Optional[str] = None, descripcion: Optional[str] = None
) -> Dict:
    nuevo_nombre = r["nombre"] if nombre is None else nombre.strip()
    nueva_desc = r["descripcion"] if descripcion is None else descripcion.strip()
    if nombre is not None and not nuevo_nombre:
        raise ValueError("El nombre de la rutina no puede quedar vacío.")
    if descripcion is not None and not nueva_desc:
        raise ValueError("La descripción de la rutina no puede quedar vacía.")
    return mk_rutina(nuevo_nombre, nueva_desc, r["ejercicios"])


# Usuario: {nombre, edad, rutinas: List[Rutina]}
def mk_usuario(nombre: str, edad: int) -> Dict:
    u = {"nombre": nombre.strip(), "edad": int(edad), "rutinas": []}  # type: ignore
    validar_usuario(u)
    return u


def validar_usuario(u: Dict) -> None:
    if not u["nombre"]:
        raise ValueError("El nombre del usuario no puede estar vacío.")
    if u["edad"] < 16:
        raise ValueError("La edad debe ser un número mayor o igual a 16 años.")
    if u["edad"] > 100:
        raise ValueError("La edad debe ser menor o igual a 100 años.")


def usuario_asignar_rutina(u: Dict, r: Dict) -> Dict:
    key = _norm(r["nombre"])
    ya = reduce(
        lambda acc, rr: acc or (_norm(rr["nombre"]) == key), u["rutinas"], False
    )
    if ya:
        raise ValueError(f"El usuario ya tiene una rutina llamada '{r['nombre']}'.")
    return {"nombre": u["nombre"], "edad": u["edad"], "rutinas": u["rutinas"] + [r]}


def str_usuario(u: Dict) -> str:
    return f"Usuario: {u['nombre']} | Edad: {u['edad']} | Rutinas: {len(u['rutinas'])}"


# -------------------- Estado del sistema (funcional) --------------------
# Estado: {
#   usuarios: List[Usuario],
#   ejercicios_catalogo: List[Ejercicio],
#   rutinas: List[Rutina],
#   idx_usuarios: Dict[str, Usuario],
#   idx_ejercicios: Dict[str, Ejercicio],
#   idx_rutinas: Dict[str, Rutina],
# }


def estado_vacio() -> Dict:
    return {
        "usuarios": [],
        "ejercicios_catalogo": [],
        "rutinas": [],
        "idx_usuarios": {},
        "idx_ejercicios": {},
        "idx_rutinas": {},
    }


# --------- Helpers I/O (recursivos, sin while) ---------


def _input_no_vacio(msg: str) -> str:
    txt = input(msg).strip()
    return (
        txt
        if txt
        else (_print("El valor no puede estar vacío.") or _input_no_vacio(msg))
    )


def _input_int(
    msg: str, minimo: Optional[int] = None, maximo: Optional[int] = None
) -> int:
    raw = input(msg).strip()
    try:
        val = int(raw)
        if minimo is not None and val < minimo:
            _print(f"El valor debe ser mayor o igual a {minimo}.")
            return _input_int(msg, minimo, maximo)
        if maximo is not None and val > maximo:
            _print(f"El valor debe ser menor o igual a {maximo}.")
            return _input_int(msg, minimo, maximo)
        return val
    except ValueError:
        _print("Ingresa un número entero válido.")
        return _input_int(msg, minimo, maximo)


def _print(msg: str) -> None:
    print(msg)


# NUEVO: pedir nombres válidos de ejercicios (reintenta hasta que existan)
def _pedir_nombres_validos_ejercicios(st: Dict) -> List[str]:
    """
    Pide 'Nombres a incluir (separados por coma)' y valida que todos existan en el catálogo.
    Si hay error (no existen o nombres repetidos), muestra el error y vuelve a pedir.
    """
    sel = _input_no_vacio("Nombres a incluir (separados por coma): ")
    nombres = list(filter(lambda x: x != "", map(lambda s: s.strip(), sel.split(","))))
    try:
        # Solo para validar; no usamos el resultado aquí.
        _ = obtener_ejercicios_por_nombres(st, nombres)
        return nombres
    except ValueError as e:
        _print(f"[Error] {e}")
        return _pedir_nombres_validos_ejercicios(st)


# -------------------- Búsquedas en índices --------------------


def buscar_usuario(st: Dict, nombre: str) -> Optional[Dict]:
    return st["idx_usuarios"].get(_norm(nombre))


def buscar_ejercicio(st: Dict, nombre: str) -> Optional[Dict]:
    return st["idx_ejercicios"].get(_norm(nombre))


def buscar_rutina(st: Dict, nombre: str) -> Optional[Dict]:
    return st["idx_rutinas"].get(_norm(nombre))


# -------------------- Operaciones de dominio (devuelven nuevo estado) --------------------


def agregar_usuario(st: Dict, nombre: str, edad: int) -> Dict:
    key = _norm(nombre)
    if key in st["idx_usuarios"]:
        raise ValueError("Ya existe un usuario con ese nombre.")
    u = mk_usuario(nombre, edad)
    nuevos_idx = dict(st["idx_usuarios"])
    nuevos_idx[key] = u
    return {**st, "usuarios": st["usuarios"] + [u], "idx_usuarios": nuevos_idx}


def listar_usuarios(st: Dict) -> None:
    if not st["usuarios"]:
        _print("No hay usuarios.")
        return

    # imprimir por recursión
    def go(lst: List[Dict]) -> None:
        if not lst:
            return
        cabeza, resto = lst[0], lst[1:]
        _print(str_usuario(cabeza))
        go(resto)

    go(st["usuarios"])


def mostrar_rutinas_de_usuario(st: Dict, nombre_usuario: str) -> None:
    u = buscar_usuario(st, nombre_usuario)
    if not u:
        _print("Usuario no encontrado.")
    elif not u["rutinas"]:
        _print(f"{u['nombre']} no tiene rutinas asignadas.")
    else:
        _print(f"Rutinas de {u['nombre']}:")

        def go(lst: List[Dict]) -> None:
            if not lst:
                return
            cabeza, resto = lst[0], lst[1:]
            _print(
                f"  - {cabeza['nombre']}: {minutos_a_texto(rutina_duracion_total_min(cabeza))}"
            )
            go(resto)

        go(u["rutinas"])


def crear_ejercicio(st: Dict, nombre: str, rep: int, ser: int) -> Dict:
    key = _norm(nombre)
    if key in st["idx_ejercicios"]:
        raise ValueError("Ya existe un ejercicio en el catálogo con ese nombre.")
    ej = mk_ejercicio(nombre, rep, ser)
    idx = dict(st["idx_ejercicios"])
    idx[key] = ej
    _print(
        f"Ejercicio creado. Duración estimada: {minutos_a_texto(duracion_ejercicio_min(ej))}"
    )
    return {
        **st,
        "ejercicios_catalogo": st["ejercicios_catalogo"] + [ej],
        "idx_ejercicios": idx,
    }


def listar_ejercicios(st: Dict) -> None:
    if not st["ejercicios_catalogo"]:
        _print("(Catálogo vacío)")
        return

    def go(lst: List[Dict]) -> None:
        if not lst:
            return
        cabeza, resto = lst[0], lst[1:]
        _print(f"- {str_ejercicio(cabeza)}")
        go(resto)

    go(st["ejercicios_catalogo"])


def eliminar_ejercicio(st: Dict, nombre: str) -> Dict:
    key = _norm(nombre)
    ej = st["idx_ejercicios"].get(key)
    if ej is None:
        raise ValueError("No se encontró el ejercicio para eliminar.")
    # quitar de lista manteniendo orden (filter)
    nueva_lista = list(filter(lambda e: e is not ej, st["ejercicios_catalogo"]))

    # eliminar de rutinas sin romperlas (intentar recursivamente)
    def quitar_en_rutina(r: Dict) -> Dict:
        try:
            return rutina_eliminar_ejercicio(r, ej["nombre"])
        except ValueError:
            return r

    nuevas_rutinas = list(map(quitar_en_rutina, st["rutinas"]))
    # actualizar índices
    nuevo_idx = dict(st["idx_ejercicios"])
    nuevo_idx.pop(key, None)
    return {
        **st,
        "ejercicios_catalogo": nueva_lista,
        "rutinas": nuevas_rutinas,
        "idx_ejercicios": nuevo_idx,
    }


def obtener_ejercicios_por_nombres(st: Dict, nombres: List[str]) -> List[Dict]:
    # Recursivo con control de duplicados
    def go(pend: List[str], vistos: set, acc: List[Dict]) -> List[Dict]:
        if not pend:
            return acc
        n = pend[0]
        key = _norm(n)
        if key in vistos:
            raise ValueError(f"Nombre de ejercicio repetido en la selección: '{n}'.")
        ej = st["idx_ejercicios"].get(key)
        if ej is None:
            raise ValueError(f"Ejercicio '{n}' no existe en el catálogo.")
        return go(pend[1:], vistos | {key}, acc + [ej])

    return go(nombres, set(), [])


def crear_rutina(
    st: Dict, nombre: str, descripcion: str, nombres_ejercicios: List[str]
) -> Dict:
    if not st["ejercicios_catalogo"]:
        raise ValueError("Primero crea ejercicios en el catálogo.")
    if not nombres_ejercicios:
        raise ValueError("Debes seleccionar al menos un ejercicio para la rutina.")
    key = _norm(nombre)
    if key in st["idx_rutinas"]:
        raise ValueError("Ya existe una rutina con ese nombre.")
    ejercicios = obtener_ejercicios_por_nombres(st, nombres_ejercicios)
    r = mk_rutina(nombre, descripcion, ejercicios)
    idx = dict(st["idx_rutinas"])
    idx[key] = r
    return {**st, "rutinas": st["rutinas"] + [r], "idx_rutinas": idx}


def listar_rutinas(st: Dict) -> None:
    if not st["rutinas"]:
        _print("No hay rutinas.")
        return

    def imprimir_rutina(r: Dict) -> None:
        _print("-" * 60)
        _print(str_rutina(r))

        def go(lst: List[Dict]) -> None:
            if not lst:
                return
            cabeza, resto = lst[0], lst[1:]
            _print(f"  • {str_ejercicio(cabeza)}")
            go(resto)

        go(r["ejercicios"])

    def go(lst: List[Dict]) -> None:
        if not lst:
            _print("-" * 60)
            return
        cabeza, resto = lst[0], lst[1:]
        imprimir_rutina(cabeza)
        go(resto)

    go(st["rutinas"])


def editar_rutina(
    st: Dict,
    nombre: str,
    nuevo_nombre: Optional[str] = None,
    nueva_desc: Optional[str] = None,
) -> Dict:
    r = buscar_rutina(st, nombre)
    if r is None:
        raise ValueError("Rutina no encontrada.")
    old_key = _norm(r["nombre"])
    r2 = rutina_actualizar_datos(r, nuevo_nombre, nueva_desc)
    new_key = _norm(r2["nombre"])
    if new_key != old_key and new_key in st["idx_rutinas"]:
        raise ValueError("Ya existe otra rutina con ese nombre.")
    # reemplazar en lista (map)
    nuevas_rutinas = list(map(lambda x: r2 if x is r else x, st["rutinas"]))
    # actualizar índices
    idx = dict(st["idx_rutinas"])
    if new_key != old_key:
        idx.pop(old_key, None)
    idx[new_key] = r2
    return {**st, "rutinas": nuevas_rutinas, "idx_rutinas": idx}


def rutina_agregar_ejercicio_st(
    st: Dict, nombre_rutina: str, nombre_ejercicio: str
) -> Dict:
    r = buscar_rutina(st, nombre_rutina)
    if r is None:
        raise ValueError("Rutina no encontrada.")
    ej = buscar_ejercicio(st, nombre_ejercicio)
    if ej is None:
        raise ValueError("Ese ejercicio no existe en el catálogo.")
    r2 = rutina_agregar_ejercicio(r, ej)
    nuevas = list(map(lambda x: r2 if x is r else x, st["rutinas"]))
    idx = dict(st["idx_rutinas"])
    idx[_norm(r2["nombre"])] = r2
    return {**st, "rutinas": nuevas, "idx_rutinas": idx}


def rutina_eliminar_ejercicio_st(
    st: Dict, nombre_rutina: str, nombre_ejercicio: str
) -> Dict:
    r = buscar_rutina(st, nombre_rutina)
    if r is None:
        raise ValueError("Rutina no encontrada.")
    r2 = rutina_eliminar_ejercicio(r, nombre_ejercicio)
    nuevas = list(map(lambda x: r2 if x is r else x, st["rutinas"]))
    idx = dict(st["idx_rutinas"])
    idx[_norm(r2["nombre"])] = r2
    return {**st, "rutinas": nuevas, "idx_rutinas": idx}


def rutina_actualizar_ejercicio_st(
    st: Dict,
    nombre_rutina: str,
    nombre_ejercicio: str,
    rep: Optional[int] = None,
    ser: Optional[int] = None,
) -> Dict:
    r = buscar_rutina(st, nombre_rutina)
    if r is None:
        raise ValueError("Rutina no encontrada.")
    r2 = rutina_actualizar_ejercicio(r, nombre_ejercicio, rep, ser)
    nuevas = list(map(lambda x: r2 if x is r else x, st["rutinas"]))
    idx = dict(st["idx_rutinas"])
    idx[_norm(r2["nombre"])] = r2
    return {**st, "rutinas": nuevas, "idx_rutinas": idx}


def asignar_rutina_a_usuario(st: Dict, nombre_usuario: str, nombre_rutina: str) -> Dict:
    u = buscar_usuario(st, nombre_usuario)
    if u is None:
        raise ValueError("Usuario no encontrado.")
    r = buscar_rutina(st, nombre_rutina)
    if r is None:
        raise ValueError("Rutina no encontrada.")
    u2 = usuario_asignar_rutina(u, r)
    # reemplazar en lista y actualizar índice
    nuevos_usuarios = list(map(lambda x: u2 if x is u else x, st["usuarios"]))
    idx = dict(st["idx_usuarios"])
    idx[_norm(u2["nombre"])] = u2
    return {**st, "usuarios": nuevos_usuarios, "idx_usuarios": idx}


def reporte_por_usuario(st: Dict) -> None:
    if not st["usuarios"]:
        _print("No hay usuarios.")
        return

    def imprimir_u(u: Dict) -> None:
        _print("=" * 60)
        _print(f"Usuario: {u['nombre']} | Edad: {u['edad']}")
        if not u["rutinas"]:
            _print("  (Sin rutinas asignadas)")
        else:

            def go(lst: List[Dict]) -> None:
                if not lst:
                    return
                cabeza, resto = lst[0], lst[1:]
                _print(
                    f"  - {cabeza['nombre']}: {minutos_a_texto(rutina_duracion_total_min(cabeza))}"
                )
                go(resto)

            go(u["rutinas"])

    def go(lst: List[Dict]) -> None:
        if not lst:
            _print("=" * 60)
            return
        cabeza, resto = lst[0], lst[1:]
        imprimir_u(cabeza)
        go(resto)

    go(st["usuarios"])


# -------------------- Menús (recursivos) --------------------


def menu_principal(st: Dict) -> None:
    _print("\n=== MENÚ PRINCIPAL ===")
    _print("1) Usuarios")
    _print("2) Ejercicios (catálogo)")
    _print("3) Rutinas")
    _print("4) Asignar rutina a usuario")
    _print("5) Mostrar rutinas de un usuario")
    _print("6) Reporte por usuario")
    _print("7) Salir")
    op = input("Opción: ").strip()
    try:
        if op == "1":
            return menu_usuarios(st)
        elif op == "2":
            return menu_ejercicios(st)
        elif op == "3":
            return menu_rutinas(st)
        elif op == "4":
            u = _pedir_usuario_nombre()
            _print("\nRutinas disponibles:")
            listar_rutinas(st)
            r_line = _pedir_no_vacio("Rutinas (separadas por coma): ")
            nombres_rutinas = list(
                filter(lambda x: x != "", map(lambda s: s.strip(), r_line.split(",")))
            )
            errores: List[str] = []

            def asignar_fold(
                state_and_errs: Tuple[Dict, List[str]], nombre_r: str
            ) -> Tuple[Dict, List[str]]:
                state, errs = state_and_errs
                try:
                    nuevo = asignar_rutina_a_usuario(state, u, nombre_r)
                    return (nuevo, errs)
                except ValueError as e:
                    return (state, errs + [f"{nombre_r}: {e}"])

            st2, errores = reduce(asignar_fold, nombres_rutinas, (st, errores))
            if errores:
                _print("Algunos errores al asignar rutinas:")

                def go_msgs(xs: List[str]) -> None:
                    if not xs:
                        return
                    cabeza, resto = xs[0], xs[1:]
                    _print(f"  [Error] {cabeza}")
                    go_msgs(resto)

                go_msgs(errores)
                return menu_principal(st2)
            else:
                _print("Rutinas asignadas.")
                return menu_principal(st2)
        elif op == "5":
            nombre = input("Usuario: ").strip()
            mostrar_rutinas_de_usuario(st, nombre)
            return menu_principal(st)
        elif op == "6":
            reporte_por_usuario(st)
            return menu_principal(st)
        elif op == "7":
            _print("Hasta luego.")
            return None
        else:
            _print("Opción no válida.")
            return menu_principal(st)
    except ValueError as e:
        _print(f"[Error] {e}")
        return menu_principal(st)


def _pedir_no_vacio(msg: str) -> str:
    return _input_no_vacio(msg)


def _pedir_usuario_nombre() -> str:
    nombre = input("Usuario: ").strip()
    return (
        nombre
        if nombre
        else (
            _print("El nombre de usuario no puede estar vacío.")
            or _pedir_usuario_nombre()
        )
    )


# ---- Submenú Usuarios ----


def menu_usuarios(st: Dict) -> None:
    _print("\n--- Usuarios ---")
    _print("1) Agregar")
    _print("2) Listar")
    _print("3) Editar usuario")
    _print("4) Volver")
    op = input("Opción: ").strip()
    if op == "1":
        nombre = _repetir_hasta(
            lambda n: buscar_usuario(st, n) is None,
            "Nombre: ",
            "Ya existe un usuario con ese nombre. Intenta otro.",
        )
        edad = _input_int("Edad: ", minimo=16, maximo=100)
        try:
            st2 = agregar_usuario(st, nombre, edad)
            _print("Usuario agregado.")
            return menu_usuarios(st2)
        except ValueError as e:
            _print(f"[Error] {e}")
            return menu_usuarios(st)
    elif op == "2":
        listar_usuarios(st)
        return menu_usuarios(st)
    elif op == "3":
        nombre = _input_no_vacio("Nombre del usuario a editar: ")
        u = buscar_usuario(st, nombre)
        if u is None:
            _print("No existe ese usuario.")
            return menu_usuarios(st)
        return submenu_editar_usuario(st, u)
    elif op == "4":
        return menu_principal(st)
    else:
        _print("Opción no válida.")
        return menu_usuarios(st)


def _repetir_hasta(pred_ok, prompt: str, msg_dup: str) -> str:
    val = _input_no_vacio(prompt)
    return (
        val
        if pred_ok(val)
        else (_print(msg_dup) or _repetir_hasta(pred_ok, prompt, msg_dup))
    )


def submenu_editar_usuario(st: Dict, u: Dict) -> None:
    _print(f"\nEditando usuario: {u['nombre']}")
    _print("1) Cambiar nombre")
    _print("2) Cambiar edad")
    _print("3) Volver")
    subop = input("Opción: ").strip()
    if subop == "1":
        nuevo = _repetir_hasta(
            lambda n: buscar_usuario(st, n) is None,
            "Nuevo nombre: ",
            "Ya existe un usuario con ese nombre.",
        )
        old_key = _norm(u["nombre"])
        u2 = {"nombre": nuevo.strip(), "edad": u["edad"], "rutinas": u["rutinas"]}
        # actualizar índice + lista
        nuevos_idx = dict(st["idx_usuarios"])
        nuevos_idx.pop(old_key, None)
        nuevos_idx[_norm(u2["nombre"])] = u2
        nuevos_usuarios = list(map(lambda x: u2 if x is u else x, st["usuarios"]))
        _print("Nombre actualizado.")
        return submenu_editar_usuario(
            {**st, "usuarios": nuevos_usuarios, "idx_usuarios": nuevos_idx}, u2
        )
    elif subop == "2":
        u2 = {
            "nombre": u["nombre"],
            "edad": _input_int("Nueva edad: ", minimo=16, maximo=100),
            "rutinas": u["rutinas"],
        }
        nuevos_idx = dict(st["idx_usuarios"])
        nuevos_idx[_norm(u2["nombre"])] = u2
        nuevos_usuarios = list(map(lambda x: u2 if x is u else x, st["usuarios"]))
        _print("Edad actualizada.")
        return submenu_editar_usuario(
            {**st, "usuarios": nuevos_usuarios, "idx_usuarios": nuevos_idx}, u2
        )
    elif subop == "3":
        return menu_usuarios(st)
    else:
        _print("Opción no válida.")
        return submenu_editar_usuario(st, u)


# ---- Submenú Ejercicios ----


def menu_ejercicios(st: Dict) -> None:
    _print("\n--- Ejercicios (catálogo) ---")
    _print("1) Crear ejercicio")
    _print("2) Listar ejercicios")
    _print("3) Editar ejercicio")
    _print("4) Eliminar ejercicio")
    _print("5) Volver")
    op = input("Opción: ").strip()
    if op == "1":
        nombre = _repetir_hasta(
            lambda n: buscar_ejercicio(st, n) is None,
            "Nombre: ",
            "Ya existe un ejercicio con ese nombre. Intenta otro.",
        )
        reps = _input_int("Repeticiones: ", minimo=1, maximo=100)
        series = _input_int("Series: ", minimo=1, maximo=100)
        try:
            st2 = crear_ejercicio(st, nombre, reps, series)
            return menu_ejercicios(st2)
        except ValueError as e:
            _print(f"[Error] {e}")
            return menu_ejercicios(st)
    elif op == "2":
        listar_ejercicios(st)
        return menu_ejercicios(st)
    elif op == "3":
        nombre = _input_no_vacio("Nombre del ejercicio a editar: ")
        ejercicio = buscar_ejercicio(st, nombre)
        if ejercicio is None:
            _print("No existe ese ejercicio.")
            return menu_ejercicios(st)
        return submenu_editar_ejercicio(st, ejercicio)
    elif op == "4":
        nombre = _input_no_vacio("Nombre a eliminar: ")
        try:
            st2 = eliminar_ejercicio(st, nombre)
            _print("Ejercicio eliminado del catálogo.")
            return menu_ejercicios(st2)
        except ValueError as e:
            _print(f"[Error] {e}")
            return menu_ejercicios(st)
    elif op == "5":
        return menu_principal(st)
    else:
        _print("Opción no válida.")
        return menu_ejercicios(st)


def submenu_editar_ejercicio(st: Dict, ej: Dict) -> None:
    _print(f"\nEditando ejercicio: {ej['nombre']}")
    _print("1) Cambiar nombre")
    _print("2) Cambiar repeticiones")
    _print("3) Cambiar series")
    _print("4) Volver")
    subop = input("Opción: ").strip()
    if subop == "1":
        nuevo = _repetir_hasta(
            lambda n: buscar_ejercicio(st, n) is None,
            "Nuevo nombre: ",
            "Ya existe un ejercicio con ese nombre.",
        )
        old_key = _norm(ej["nombre"])
        ej2 = dict(ej)
        ej2["nombre"] = nuevo.strip()
        idx = dict(st["idx_ejercicios"])
        idx.pop(old_key, None)
        idx[_norm(ej2["nombre"])] = ej2
        catalogo = list(map(lambda x: ej2 if x is ej else x, st["ejercicios_catalogo"]))
        _print("Nombre actualizado.")
        return submenu_editar_ejercicio(
            {**st, "idx_ejercicios": idx, "ejercicios_catalogo": catalogo}, ej2
        )
    elif subop == "2":
        ej2 = actualizar_ejercicio(
            ej, rep=_input_int("Nuevas repeticiones: ", minimo=1, maximo=100)
        )
        idx = dict(st["idx_ejercicios"])
        idx[_norm(ej2["nombre"])] = ej2
        catalogo = list(map(lambda x: ej2 if x is ej else x, st["ejercicios_catalogo"]))
        _print("Repeticiones actualizadas.")
        return submenu_editar_ejercicio(
            {**st, "idx_ejercicios": idx, "ejercicios_catalogo": catalogo}, ej2
        )
    elif subop == "3":
        ej2 = actualizar_ejercicio(
            ej, ser=_input_int("Nuevas series: ", minimo=1, maximo=100)
        )
        idx = dict(st["idx_ejercicios"])
        idx[_norm(ej2["nombre"])] = ej2
        catalogo = list(map(lambda x: ej2 if x is ej else x, st["ejercicios_catalogo"]))
        _print("Series actualizadas.")
        return submenu_editar_ejercicio(
            {**st, "idx_ejercicios": idx, "ejercicios_catalogo": catalogo}, ej2
        )
    elif subop == "4":
        return menu_ejercicios(st)
    else:
        _print("Opción no válida.")
        return submenu_editar_ejercicio(st, ej)


# ---- Submenú Rutinas ----


def menu_rutinas(st: Dict) -> None:
    _print("\n--- Rutinas ---")
    _print("1) Crear rutina (seleccionando ejercicios del catálogo)")
    _print("2) Listar rutinas")
    _print("3) Editar rutina")
    _print("4) Volver")
    op = input("Opción: ").strip()
    if op == "1":
        if not st["ejercicios_catalogo"]:
            _print("Primero crea ejercicios en el catálogo.")
            return menu_rutinas(st)
        nombre = _repetir_hasta(
            lambda n: buscar_rutina(st, n) is None,
            "Nombre de la rutina: ",
            "Ya existe una rutina con ese nombre. Intenta otro.",
        )
        desc = _input_no_vacio("Descripción: ")
        _print("\nEjercicios disponibles (separa por coma):")
        listar_ejercicios(st)
        # Aquí reintentamos hasta que todos los nombres existan
        nombres = _pedir_nombres_validos_ejercicios(st)
        try:
            st2 = crear_rutina(st, nombre, desc, nombres)
            _print("Rutina creada.")
            return menu_rutinas(st2)
        except ValueError as e:
            _print(f"[Error] {e}")
            return menu_rutinas(st)
    elif op == "2":
        listar_rutinas(st)
        return menu_rutinas(st)
    elif op == "3":
        nombre = _input_no_vacio("Nombre de la rutina a editar: ")
        r = buscar_rutina(st, nombre)
        if r is None:
            _print("No existe esa rutina.")
            return menu_rutinas(st)
        return submenu_editar_rutina(st, r)
    elif op == "4":
        return menu_principal(st)
    else:
        _print("Opción no válida.")
        return menu_rutinas(st)


def submenu_editar_rutina(st: Dict, r: Dict) -> None:
    _print(f"\n>>> Editando: {r['nombre']}")
    _print("1) Agregar ejercicio (del catálogo)")
    _print("2) Eliminar ejercicio")
    _print("3) Actualizar reps/series de un ejercicio")
    _print("4) Modificar nombre/descr.")
    _print("5) Ver duración total")
    _print("6) Listar ejercicios")
    _print("7) Volver")
    op = input("Opción: ").strip()
    if op == "1":
        if not st["ejercicios_catalogo"]:
            _print("Catálogo vacío. Crea ejercicios primero.")
            return submenu_editar_rutina(st, r)
        listar_ejercicios(st)

        # Reintenta hasta que el ejercicio exista
        def _pedir_ej_valido() -> str:
            nombre_ej = _input_no_vacio("Nombre del ejercicio a agregar: ")
            if buscar_ejercicio(st, nombre_ej) is None:
                _print("Ese ejercicio no existe en el catálogo.")
                return _pedir_ej_valido()
            return nombre_ej

        nombre = _pedir_ej_valido()
        try:
            st2 = rutina_agregar_ejercicio_st(st, r["nombre"], nombre)
            _print("Ejercicio agregado a la rutina.")
            r2 = buscar_rutina(st2, r["nombre"]) or r
            return submenu_editar_rutina(st2, r2)
        except ValueError as e:
            _print(f"[Error] {e}")
            return submenu_editar_rutina(st, r)
    elif op == "2":
        nombre = _input_no_vacio("Nombre del ejercicio a eliminar: ")
        try:
            st2 = rutina_eliminar_ejercicio_st(st, r["nombre"], nombre)
            _print("Ejercicio eliminado de la rutina.")
            r2 = buscar_rutina(st2, r["nombre"]) or r
            return submenu_editar_rutina(st2, r2)
        except ValueError as e:
            _print(f"[Error] {e}")
            return submenu_editar_rutina(st, r)
    elif op == "3":
        nombre = _input_no_vacio("Ejercicio a actualizar: ")
        rep_txt = input("Nuevas repeticiones (enter para mantener): ").strip()
        ser_txt = input("Nuevas series (enter para mantener): ").strip()
        rep = None if rep_txt == "" else int(rep_txt)
        ser = None if ser_txt == "" else int(ser_txt)
        try:
            st2 = rutina_actualizar_ejercicio_st(st, r["nombre"], nombre, rep, ser)
            _print("Ejercicio actualizado.")
            r2 = buscar_rutina(st2, r["nombre"]) or r
            return submenu_editar_rutina(st2, r2)
        except ValueError as e:
            _print(f"[Error] {e}")
            return submenu_editar_rutina(st, r)
    elif op == "4":
        nuevo = input("Nuevo nombre (enter=mantener): ").strip()
        desc = input("Nueva descripción (enter=mantener): ").strip()
        try:
            st2 = editar_rutina(
                st,
                r["nombre"],
                nuevo_nombre=(None if not nuevo else nuevo),
                nueva_desc=(None if not desc else desc),
            )
            _print("Datos actualizados.")
            r2 = buscar_rutina(st2, (nuevo if nuevo else r["nombre"])) or r
            return submenu_editar_rutina(st2, r2)
        except ValueError as e:
            _print(f"[Error] {e}")
            return submenu_editar_rutina(st, r)
    elif op == "5":
        _print(f"Duración total: {minutos_a_texto(rutina_duracion_total_min(r))}")
        return submenu_editar_rutina(st, r)
    elif op == "6":
        if not r["ejercicios"]:
            _print("(Sin ejercicios)")
        else:

            def go(lst: List[Dict]) -> None:
                if not lst:
                    return
                cabeza, resto = lst[0], lst[1:]
                _print(f"  • {str_ejercicio(cabeza)}")
                go(resto)

            go(r["ejercicios"])
        return submenu_editar_rutina(st, r)
    elif op == "7":
        return menu_rutinas(st)
    else:
        _print("Opción no válida.")
        return submenu_editar_rutina(st, r)


# -------------------- Main --------------------

if __name__ == "__main__":
    st = estado_vacio()
    try:
        menu_principal(st)
    except KeyboardInterrupt:
        print("\n¡Hasta luego!")
