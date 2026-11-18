import streamlit as st
import pandas as pd
import extra_streamlit_components as stx
from modules.data_base import get
from modules.emailSender import send_welcome_email
from page_utils import apply_page_config
from navigation import make_sidebar
from modules.session_manager import load_user
from variables import (
    usuariosTabla, alumnosTabla, empresasTabla, tutoresTabla,
    tutoresCentroTabla, gestoresTabla, nombres_roles,
)

# Hidden page: not linked from the menu (navigation.py), only reachable by URL.
st.set_page_config(page_title="Superadmin", page_icon="🔐", layout="wide")
apply_page_config()

# Opening this page by URL starts a new session (empty session_state), and make_sidebar()
# would send it to the login page. Restore the session from the login cookie first,
# the same way streamlit_app.py does.
if not st.session_state.get("logged_in"):
    saved_email = stx.CookieManager(key="superadmin_cookie_manager").get("saved_user_email")
    if saved_email and load_user(saved_email):
        st.rerun()
    # The cookie component returns nothing on its first render and reruns the page once
    # it has loaded, so this message only stays if there is no saved session.
    st.info("Inicia sesión para acceder a esta página.")
    st.markdown("[Ir al inicio de sesión](/)")
    st.stop()

make_sidebar()

# --- Access: logged-in admin whose username is listed in secrets.toml ---
#   [superadmin]
#   usuarios = ["usuario1", "usuario2"]
superadmins = [str(u).strip().lower() for u in st.secrets.get("superadmin", {}).get("usuarios", [])]
usuario_actual = str(st.session_state.get("username") or "").strip().lower()
if not (
    st.session_state.get("logged_in")
    and st.session_state.get("rol") == "admin"
    and usuario_actual in superadmins
):
    st.error("No tienes permisos para acceder a esta página.")
    st.stop()

st.markdown("<h2 style='text-align: center;'>Usuarios de la plataforma</h2>", unsafe_allow_html=True)


def _txt(valor):
    return str(valor or "").strip()


def cargar_usuarios():
    """Every user plus the name and email address the welcome email goes to."""
    alumnos = {_txt(a.get("dni")).upper(): a for a in get(alumnosTabla) or []}
    empresas = {_txt(e.get("CIF")).upper(): e for e in get(empresasTabla) or []}
    tutores = get(tutoresTabla) or []
    tutores_nif = {_txt(t.get("nif")).upper(): t for t in tutores if t.get("nif")}
    tutores_email = {_txt(t.get("email")).lower(): t for t in tutores if t.get("email")}
    tutores_centro = {_txt(t.get("email")).lower(): t for t in get(tutoresCentroTabla) or []}
    gestores = {_txt(g.get("email")).lower(): g for g in get(gestoresTabla) or []}

    filas = []
    for u in get(usuariosTabla) or []:
        usuario = _txt(u.get("email"))
        rol = _txt(u.get("rol"))
        nombre, destino = "", ""
        if rol == "alumno":
            a = alumnos.get(usuario.upper(), {})
            nombre = f"{_txt(a.get('nombre'))} {_txt(a.get('apellido'))}".strip()
            destino = _txt(a.get("email_alumno"))
        elif rol == "empresa":
            e = empresas.get(usuario.upper(), {})
            nombre, destino = _txt(e.get("nombre")), _txt(e.get("email_empresa"))
        elif rol == "tutor":
            # Tutor users are created with the NIF or with the email as username
            t = tutores_nif.get(usuario.upper()) or tutores_email.get(usuario.lower()) or {}
            nombre, destino = _txt(t.get("nombre")), _txt(t.get("email"))
        elif rol == "tutorCentro":
            t = tutores_centro.get(usuario.lower(), {})
            nombre, destino = _txt(t.get("nombre")), _txt(t.get("email"))
        elif rol == "gestor":
            g = gestores.get(usuario.lower(), {})
            nombre, destino = _txt(g.get("nombre")), _txt(g.get("email"))
        if not destino and "@" in usuario:
            destino = usuario
        filas.append({
            "Usuario": usuario,
            "Rol": nombres_roles.get(rol, rol),
            "Nombre": nombre,
            "Email": destino,
            "Contraseña": _txt(u.get("password")),
        })
    return pd.DataFrame(filas, columns=["Usuario", "Rol", "Nombre", "Email", "Contraseña"])


if "superadmin_usuarios" not in st.session_state or st.button("🔄 Actualizar"):
    with st.spinner("Cargando usuarios..."):
        st.session_state.superadmin_usuarios = cargar_usuarios()
df = st.session_state.superadmin_usuarios

# --- Filters ---
col_buscar, col_rol, col_pass = st.columns([3, 2, 1])
with col_buscar:
    buscar = st.text_input("Buscar", placeholder="Usuario, nombre o email").strip().lower()
with col_rol:
    roles = st.multiselect("Rol", sorted(df["Rol"].dropna().unique()), placeholder="Todos")
with col_pass:
    st.write("")
    mostrar_pass = st.toggle("Ver contraseñas")

vista = df
if buscar:
    vista = vista[
        vista[["Usuario", "Nombre", "Email"]].apply(
            lambda col: col.str.lower().str.contains(buscar, regex=False, na=False)
        ).any(axis=1)
    ]
if roles:
    vista = vista[vista["Rol"].isin(roles)]
vista = vista.reset_index(drop=True)

st.caption(f"{len(vista)} de {len(df)} usuarios. Selecciona una fila para reenviar el email de acceso.")
seleccion = st.dataframe(
    vista if mostrar_pass else vista.drop(columns=["Contraseña"]),
    hide_index=True,
    width="stretch",
    on_select="rerun",
    selection_mode="single-row",
    key="tabla_superadmin",
)

# --- Resend welcome email ---
filas_sel = seleccion.selection.rows if seleccion else []
if filas_sel and filas_sel[0] < len(vista):
    u = vista.iloc[filas_sel[0]]
    with st.container(border=True):
        st.markdown(f"**{u['Nombre'] or u['Usuario']}** · {u['Rol']}")
        st.write(f"**Usuario:** {u['Usuario']}")
        destino = st.text_input(
            "Enviar a", value=u["Email"], key=f"destino_{u['Usuario']}",
            help="Email registrado del usuario. Puedes cambiarlo solo para este envío.",
        ).strip()
        if not u["Contraseña"]:
            st.warning("Este usuario no tiene contraseña en la base de datos.")
        if st.button(
            "📧 Reenviar usuario y contraseña", type="primary",
            disabled=not destino or "@" not in destino or not u["Contraseña"],
            key=f"reenviar_{u['Usuario']}",
        ):
            try:
                send_welcome_email(destino, u["Usuario"], u["Contraseña"], u["Nombre"] or u["Usuario"])
                st.success(f"✅ Email enviado a {destino}")
            except Exception as e:
                st.error(f"❌ No se pudo enviar el email: {e}")
