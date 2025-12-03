title="Cámara Valencia - FP"
logoutButton="Desloguearse"
page_icon="./images/cv-fp.ico"
companyIcon="./images/cv-fp.png"

azul="#013d5f"
celeste="2AD2C9"
amarillo=""
#forms
tipoCampo=["Texto", "Si/No", "Opciones", "Cantidad","OpcionesConCantidad"]
categoria=["Empresa", "FP", "Alumno"]
estados=["Nuevo","Completa", "Activo", "Finalizada", "Cancelado"]
estadosAlumno=["Sin Empresa","Asignado", "Finalizado", "En progreso", "Cancelado"]

#fases
fasesEmpresa = ["Form Enviado", "Form Completo", "Match en progreso", "Alumnos asignados",  "Documentación Completa","Pasantía en progreso", "Finalizada", "Evaluación Enviada"] 
fasesAlumno = ["Form Enviado", "Form Completo",  "Match en progreso","Alumnos asignados","Documentación Completa", "Pasantía en progreso", "Finalizada", "Evaluación Enviada"] 
fasesPractica = ["Documentación Pedida", "Documentación Firmada", "Pasantía en progreso", "Finalizada", "Cancelada"]
faseColPractica = {
    "Documentación Pedida": "documentacion_pedida",
    "Documentación Firmada": "documentacion_firmada",
    "Pasantía en progreso": "en_progreso",
    "Finalizada": "fp_finalizada",
    "Cancelada": "cancelada"
}
fase2colEmpresa = {
    "Form Enviado": "email_enviado",
    "Form Completo": "form_completo",
    "Documentación Completa": "documentacion_completa",
    "Match en progreso": "match_fp",
    "Alumnos asignados": "fp_asignada",
    "Pasantía en progreso": "fp_enprogreso",
    "Finalizada": "fp_finalizada",
    "Evaluación Enviada": "evaluacion_enviada"
}
#colores
verdeOk="#D8E4BC"
celeste="#P3252C"
azul="P3025C"
gris="P431C"
#Tablas
usuariosTabla="usuarios"
formTabla="forms"
formFieldsTabla="form_fields"
empresasTabla="empresas"
alumnosTabla="alumnos"
answersTabla="form_answers"
necesidadFP="oferta_fp"
empresaEstadosTabla="empresa_estados"
contactoEmpresaTabla="contacto_empresas"
alumnoEstadosTabla="alumno_estados"
contactoAlumnoTabla="contacto_alumnos"
practicaTabla="practicas_fp"
practicaEstadosTabla="practica_estados"
tutoresTabla="tutores"

max_file_size = 20 * 1024 * 1024  # 20MB

#drive
carpetaAlumnos="1Q6YVWNLi2Jm5V7E9dnT454Me_INBvU3Z"
carpetaEmpresas="1S4WOBuY_Yn_7eiFqJ3BJrRSWu_QLhg4_"
carpetaPractica="1a-s8ycno4rXBnennRUdodvJbrt-KgRHT"
#emails
bodyEmailsEmpresa= f"""Hola,

Nos ponemos en contacto desde la Cámara de Comercio de Valencia en relación a la Formación Profesional.
Estamos próximos a lanzar los nuevos proyectos de FP y nos gustaría contar con tu colaboración. 
Llena esta formulario si tiene alguna pasantia u oferta: {"{{form_link}}"}

Saludos,
Andrea
"""
bodyEmailsAlumno= f"""Hola,

Nos ponemos en contacto desde la Cámara de Comercio de Valencia en relación a la Formación Profesional.
Estamos próximos a lanzar los nuevos proyectos de FP y nos gustaría contar con tu colaboración. 
Llena esta formulario si te interesaría participar en alguna pasantía: {"{{form_link}}"}

Saludos,
Andrea
"""

#forms
ciclos = [
    "COMERCIO INTERNACIONAL",
    "TRANSPORTE Y LOGÍSTICA",
    "MARKETING Y PUBLICIDAD",
    "DESARROLLO APLICACIONES MULTIPLATAFORMA",
    "DESARROLLO APLICACIONES WEB",
]

preferencias = "{\"COMERCIO INTERNACIONAL\": [\"Departamento Export/import\", \"Departamento Comercio Ext/aduanas\", \"Compras internacionales/ aprovisionamiento\", \"Atención a clientes internacionales\", \"Gestión documental/ almacén\"], \"TRANSPORTE Y LOGÍSTICA\": [\"Gestión de tráfico y transporte terrestre; marítimo o aéreo\", \"Gestión de almacén y stock\", \"Operaciones logísticas y distribución\", \"Atención al cliente/logística inversa (devoluciones)\", \"Administración y documentación de transporte\"], \"MARKETING Y PUBLICIDAD\": [\"Departamento de Marketing (estrategia/campañas)\", \"Publicidad y Comunicación (redes sociales)\", \"Marketing digital (SEO/SEM)\", \"Gestión de eventos\", \"Atención al cliente y fidelización\", \"Estudios de mercado e investigación comercial\"], \"DESARROLLO APLICACIONES MULTIPLATAFORMA\": [\"Desarrollo aplicaciones móviles\", \"Desarrollo software\", \"Bases de datos y gestión de información\", \"Soporte técnico y mantenimiento de apps\", \"Integración de sistemas multiplataforma\"], \"DESARROLLO APLICACIONES WEB\": [\"Desarrollo fronted\", \"Desarrollo backend\", \"Bases de datos\", \"Soporte técnico en entornos web\", \"Administración de sistemas web/hosting\"]}"

opciones_motivo = [
        "Ya no tienen necesidad de acoger becarios",
        "El alumno/a no ha pasado la entrevista",
        "El alumno/a ha decidido no continuar con el proceso",
        "Otros"
    ]

tipoPracticas= [
                    "Práctica Autogestionada",
                    "Práctica Asignada por el Centro"
                ]