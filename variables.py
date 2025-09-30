title="Cámara Valencia - FP"
logoutButton="Desloguearse"
page_icon="./images/cv-fp.ico"
companyIcon="./images/cv-fp.png"



#forms
tipoCampo=["Texto", "Si/No", "Opciones", "Cantidad","OpcionesConCantidad"]
categoria=["Empresa", "FP", "Alumno"]
estados=["Activo", "Cerrado", "Cancelado"]
estadosAlumno=["Activo", "Finalizado", "En progreso", "Cancelado"]

#fases
fasesEmpresa = ["Form Enviado", "Form Completo", "Documentación Completa", "Match en progreso", "Alumnos asignados","Pasantía en progreso", "Finalizada", "Evaluación Enviada"] 
fasesAlumno = ["Form Enviado", "Form Completo", "Documentación Completa", "Match en progreso", "Pasantía en progreso", "Finalizada", "Evaluación Enviada"] 


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


#

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