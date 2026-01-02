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
forms =["feedback_inicial", "feedback_adaptacion", "feedback_seguimiento", "feedback_cierre"]
#fases
fasesEmpresa = ["Form Enviado", "Form Completo", "Match en progreso", "Alumnos asignados",  "Documentación Completa","Pasantía en progreso", "Finalizada", "Evaluación Enviada"] 
fasesAlumno = ["Form Enviado", "Form Completo",  "Match en progreso","Alumnos asignados","Documentación Completa", "Pasantía en progreso", "Finalizada", "Evaluación Enviada"] 
fasesPractica = ["Documentación Pedida", "Documentación Firmada", "Pasantía en progreso", "Finalizada", "Cancelada"]
faseColPractica = {
    "Documentación Pedida": "documentacion_pedida",
    "Documentación Firmada": "documentacion_firmada",
    "Pasantía en progreso": "en_progreso",
    "Finalizada": "finalizada",
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
feedbackFormsTabla="feedback_forms"
feedbackResponseTabla="feedback_respuestas"
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
                    "Práctica asignada por el centro"
                ]
sectorEmpresa = [
  "Comercio minorista y mayorista",
  "Turismo y hostelería",
  "Servicios profesionales y empresariales",
  "Transporte, logística y actividades portuarias",
  "Industria manufacturera",
  "Automoción, maquinaria y bienes de equipo",
  "Industria cerámica",
  "Metalurgia y productos metálicos",
  "Químico y materias plásticas",
  "Agroalimentario y transformación de alimentos",
  "Agricultura y ganadería",
  "Tecnología, innovación y startups",
  "Energías renovables y sostenibilidad",
  "Construcción e infraestructuras",
  "Educación, salud y servicios sociales",
  "Otros"
]

localidades = [
  "ADEMUZ",
  "ADOR",
  "AGULLENT",
  "AIELO DE MALFERIT",
  "AIELO DE RUGAT",
  "ALAQUAS",
  "ALBAIDA",
  "ALBAL",
  "ALBALAT DE LA RIBERA",
  "ALBALAT DELS SORELLS",
  "ALBALAT DELS TARONGERS",
  "ALBERIC",
  "ALBORACHE",
  "ALBORAYA",
  "ALBUIXECH",
  "ALCANTERA DE XUQUER",
  "ALCASSER",
  "ALCUBLAS",
  "ALDAIA",
  "ALFAFAR",
  "ALFARA DE ALGIMIA",
  "ALFARA DEL PATRIARCA",
  "ALFARP",
  "ALFARRASI",
  "ALFAUIR",
  "ALGAR DE PALANCIA",
  "ALGEMESI",
  "ALGIMIA DE ALFARA",
  "ALGINET",
  "ALMASSERA",
  "ALMISERA",
  "ALMOINES",
  "ALMUSSAFES",
  "ALPUENTE",
  "ALZIRA",
  "ANDILLA",
  "ANNA",
  "ANTELLA",
  "ARAS DE ALPUENTE",
  "ATZENETA D'ALBAIDA",
  "AYORA",
  "BARX",
  "BARXETA",
  "BELGIDA",
  "BELLREGUARD",
  "BELLUS",
  "BENAGEBER",
  "BENAGUASIL",
  "BENAVITES",
  "BENEIXIDA",
  "BENETUSSER",
  "BENIARJO",
  "BENIATJAR",
  "BENICOLET",
  "BENIFAIO",
  "BENIFAIRO DE LES VALLS",
  "BENIFAIRO DE LA VALLDIGNA",
  "BENIFLA",
  "BENIGANIM",
  "BENIMODO",
  "BENIMUSLEM",
  "BENIPARRELL",
  "BENIRREDRA",
  "BENISANO",
  "BENISODA",
  "BENISUERA",
  "BETERA",
  "BICORP",
  "BOCAIRENT",
  "BOLBAITE",
  "BONREPOS I MIRAMBELL",
  "BUFALI",
  "BUGARRA",
  "BUÑOL",
  "BURJASSOT",
  "CALLES",
  "CAMPORROBLES",
  "CANALS",
  "CANET D'EN BERENGUER",
  "CARCAIXENT",
  "CARCER",
  "CARLET",
  "CARRICOLA",
  "CASAS ALTAS",
  "CASAS BAJAS",
  "CASINOS",
  "CASTELLO DE RUGAT",
  "CASTELLONET DE LA CONQUESTA",
  "CASTIELFABIB",
  "CATADAU",
  "CATARROJA",
  "CAUDETE DE LAS FUENTES",
  "CERDA",
  "CHELLA",
  "CHELVA",
  "CHERA",
  "CHESTE",
  "CHIVA",
  "CHULILLA",
  "COFRENTES",
  "CORBERA",
  "CORTES DE PALLAS",
  "COTES",
  "CULLERA",
  "DAIMUS",
  "DOMEÑO",
  "DOS AGUAS",
  "EMPERADOR",
  "ENGUERA",
  "ESTIVELLA",
  "ESTUBENY",
  "FAURA",
  "FAVARA",
  "FOIOS",
  "FONTANARS DELS ALFORINS",
  "FORTALENY",
  "FUENTERROBLES",
  "GANDIA",
  "GATOVA",
  "GAVARDA",
  "GENOVES",
  "GESTALGAR",
  "GILET",
  "GODELLA",
  "GODELLETA",
  "GUADASEQUIES",
  "GUADASSUAR",
  "GUARDAMAR",
  "HIGUERUELAS",
  "JALANCE",
  "JARAFUEL",
  "LA FONT DE LA FIGUERA",
  "LA FONT D'EN CARROS",
  "LA GRANJA DE LA COSTERA",
  "LA POBLA DE FARNALS",
  "LA POBLA DE VALLBONA",
  "LA POBLA DEL DUC",
  "LA POBLA LLARGA",
  "LA YESA",
  "L'ALCUDIA",
  "L'ALCUDIA DE CRESPINS",
  "L'ALQUERIA DE LA COMTESSA",
  "L'ELIANA",
  "L'ENOVA",
  "LLANERA DE RANES",
  "LLAURI",
  "LLIRIA",
  "LLOCNOU DE SANT JERONI",
  "LLOMBAI",
  "LLOSA DE RANES",
  "LLUTXENT",
  "L'OLLERIA",
  "LORIGUILLA",
  "LOSA DEL OBISPO",
  "LUGAR NUEVO DE FENOLLET",
  "LUGAR NUEVO DE LA CORONA",
  "MACASTRE",
  "MANISES",
  "MANUEL",
  "MARINES",
  "MASALAVES",
  "MASSALFASSAR",
  "MASSAMAGRELL",
  "MASSANASSA",
  "MELIANA",
  "MILLARES",
  "MIRAMAR",
  "MISLATA",
  "MOIXENT",
  "MONCADA",
  "MONTSERRAT",
  "MONTAVERNER",
  "MONTESA",
  "MONTICHELVO",
  "MONTROY",
  "MUSEROS",
  "NAQUERA",
  "NAVARRES",
  "NOVELE",
  "OLIVA",
  "OLOCAU",
  "ONTINYENT",
  "OTOS",
  "PAIPORTA",
  "PALMA DE GANDIA",
  "PALMERA",
  "PALOMAR",
  "PATERNA",
  "PEDRALBA",
  "PETRES",
  "PICANYA",
  "PICASSENT",
  "PILES",
  "PINET",
  "POLINYA DE XUQUER",
  "POTRIES",
  "PUÇOL",
  "PUEBLA DE SAN MIGUEL",
  "PUIG",
  "QUART DE LES VALLS",
  "QUART DE POBLET",
  "QUARTELL",
  "QUATRETONDA",
  "QUESA",
  "RAFELBUNYOL",
  "RAFELCOFER",
  "RAFELGUARAF",
  "RAFOL DE SALEM",
  "REAL DE GANDIA",
  "REAL DE MONTROI",
  "REQUENA",
  "RIBA-ROJA DE TURIA",
  "RIOLA",
  "ROCAFORT",
  "ROTGLA I CORBERA",
  "ROTOVA",
  "RUGAT",
  "SAGUNTO",
  "SALEM",
  "SAN ANTONIO DE BENAGEBER",
  "SAN JUAN DE ENOVA",
  "SEDAVI",
  "SEGART",
  "SELLENT",
  "SEMPERE",
  "SENYERA",
  "SERRA",
  "SIETE AGUAS",
  "SILLA",
  "SIMAT DE LA VALLDIGNA",
  "SINARCAS",
  "SOLLANA",
  "SOT DE CHERA",
  "SUECA",
  "SUMACARCER",
  "TAVERNES BLANQUES",
  "TAVERNES DE LA VALLDIGNA",
  "TERESA DE COFRENTES",
  "TERRATEIG",
  "TITAGUAS",
  "TORREBAJA",
  "TORRELLA",
  "TORRENT",
  "TORRES TORRES",
  "TOUS",
  "TUEJAR",
  "TURIS",
  "UTIEL",
  "VALENCIA",
  "VALLADA",
  "VALLANCA",
  "VALLES",
  "VENTA DEL MORO",
  "VILAMARXANT",
  "VILLALONGA",
  "VILLANUEVA DE CASTELLON",
  "VILLAR DEL ARZOBISPO",
  "VILLARGORDO DEL CABRIEL",
  "VINALESA",
  "XATIVA",
  "XERACO",
  "XERESA",
  "XIRIVELLA",
  "YATOVA",
  "ZARRA"
]
