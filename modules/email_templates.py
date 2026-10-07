from html import escape


LOGO_URL = "https://github.com/user-attachments/assets/f1d559fc-def7-4907-b3ae-4a89e73ed00d"


def render_welcome_email(
    nombre: str,
    usuario: str,
    password: str,
    url: str,
) -> str:
    nombre_html = escape(nombre)
    usuario_html = escape(usuario)
    password_html = escape(password)
    url_html = escape(url, quote=True)

    return f"""
    <!DOCTYPE html>
    <html lang="es">
      <body style="margin:0; padding:0; background-color:#f4f8fa; color:#013d5f;
                   font-family:Calibri, Arial, sans-serif; line-height:1.6;">
        <div style="width:100%; padding:32px 12px; box-sizing:border-box;">
          <div style="max-width:620px; margin:0 auto; background:#ffffff;
                      border-radius:16px; overflow:hidden;
                      box-shadow:0 4px 18px rgba(1,61,95,.12);">
            <div style="padding:28px 24px; text-align:center; background:#ffffff;">
              <img src="{LOGO_URL}" alt="MCC logo"
                   style="display:block; width:280px; max-width:100%; height:auto;
                          margin:0 auto;">
            </div>
            <div style="padding:34px 38px;">
              <h1 style="margin:0 0 18px; color:#172b47; font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
                         font-size:32px; font-weight:normal; letter-spacing:.4px;">
                ¡Bienvenido/a, {nombre_html}!
              </h1>
              <p style="margin:0 0 18px; font-size:17px;">
                Te damos la bienvenida a la plataforma de
                <strong style="color:#013d5f;">MCC</strong>.
                Desde aquí podrás gestionar tu participación en los proyectos de
                Formación Profesional.
              </p>
              <p style="margin:0 0 10px; font-size:16px;">
                Estos son tus datos de acceso:
              </p>
              <div style="margin:0 0 26px; padding:18px 20px; background:#eefafa;
                          border-left:5px solid #2AD2C9; border-radius:8px;
                          font-size:16px;">
                <p style="margin:0 0 8px;"><strong>Usuario:</strong> {usuario_html}</p>
                <p style="margin:0;"><strong>Contraseña:</strong> {password_html}</p>
              </div>
              <div style="text-align:center; margin:28px 0 24px;">
                <a href="{url_html}" target="_blank" rel="noopener noreferrer"
                   style="display:inline-block; padding:14px 28px; border-radius:8px;
                          background:#2AD2C9; color:#013d5f; font-size:17px;
                          font-weight:bold; text-decoration:none;">
                  Acceder a la plataforma
                </a>
              </div>
            </div>
            <div style="padding:18px 24px; text-align:center; background:#172b47;
                        color:#ffffff; font-size:14px;">
              <strong style="font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
                             font-size:18px; font-weight:normal;">Cámara FP Valencia - MCC</strong>
            </div>
          </div>
        </div>
      </body>
    </html>
    """


def render_feedback_tutor_email(
    alumno: str,
    fecha_fin_real: str,
    link: str,
) -> str:
    alumno_html = escape(alumno)
    fecha_fin_html = escape(fecha_fin_real)
    link_html = escape(link, quote=True)

    return f"""
    <!DOCTYPE html>
    <html lang="es">
      <body style="margin:0; padding:0; background-color:#f4f8fa; color:#013d5f;
                   font-family:Calibri, Arial, sans-serif; line-height:1.6;">
        <div style="width:100%; padding:32px 12px; box-sizing:border-box;">
          <div style="max-width:620px; margin:0 auto; background:#ffffff;
                      border-radius:16px; overflow:hidden;
                      box-shadow:0 4px 18px rgba(1,61,95,.12);">
            <div style="padding:28px 24px; text-align:center; background:#ffffff;">
              <img src="{LOGO_URL}" alt="Cámara FP Valencia"
                   style="display:block; width:280px; max-width:100%; height:auto;
                          margin:0 auto;">
            </div>
            <div style="padding:34px 38px;">
              <h1 style="margin:0 0 18px; color:#013d5f; font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
                         font-size:32px; font-weight:normal; letter-spacing:.4px;">
                ¡Formulario de Cierre!
              </h1>
              <p style="margin:0 0 18px; font-size:17px;">
                La formación en empresa de <strong>{alumno_html}</strong>
                ha finalizado el <strong>{fecha_fin_html}</strong>.
              </p>
              <p style="margin:0 0 10px; font-size:16px;">
                Aquí te enviamos el
                <a href="{link_html}" target="_blank" rel="noopener noreferrer">
                  formulario de cierre
                </a>.
                Por favor, rellénalo.
              </p>
            </div>
            <div style="padding:18px 24px; text-align:center; background:#013d5f;
                        color:#ffffff; font-size:14px;">
              <strong style="font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
                             font-size:18px; font-weight:normal;">Cámara FP Valencia</strong>
            </div>
          </div>
        </div>
      </body>
    </html>
    """
