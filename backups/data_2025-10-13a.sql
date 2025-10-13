SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict VGnNdwTeWXzSkEaci2J1UYTY8uznSuWEqfRB6f5LviRsUY7qd0h4gcvXoZH8Dgf

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."audit_log_entries" ("instance_id", "id", "payload", "created_at", "ip_address") FROM stdin;
\.


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."flow_state" ("id", "user_id", "auth_code", "code_challenge_method", "code_challenge", "provider_type", "provider_access_token", "provider_refresh_token", "created_at", "updated_at", "authentication_method", "auth_code_issued_at") FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at", "is_anonymous") FROM stdin;
\.


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."identities" ("provider_id", "user_id", "identity_data", "provider", "last_sign_in_at", "created_at", "updated_at", "id") FROM stdin;
\.


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."instances" ("id", "uuid", "raw_base_config", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sessions" ("id", "user_id", "created_at", "updated_at", "factor_id", "aal", "not_after", "refreshed_at", "user_agent", "ip", "tag") FROM stdin;
\.


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_amr_claims" ("session_id", "created_at", "updated_at", "authentication_method", "id") FROM stdin;
\.


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_factors" ("id", "user_id", "friendly_name", "factor_type", "status", "created_at", "updated_at", "secret", "phone", "last_challenged_at", "web_authn_credential", "web_authn_aaguid") FROM stdin;
\.


--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_challenges" ("id", "factor_id", "created_at", "verified_at", "ip_address", "otp_code", "web_authn_session_data") FROM stdin;
\.


--
-- Data for Name: oauth_clients; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."oauth_clients" ("id", "client_id", "client_secret_hash", "registration_type", "redirect_uris", "grant_types", "client_name", "client_uri", "logo_uri", "created_at", "updated_at", "deleted_at") FROM stdin;
\.


--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."one_time_tokens" ("id", "user_id", "token_type", "token_hash", "relates_to", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."refresh_tokens" ("instance_id", "id", "token", "user_id", "revoked", "created_at", "updated_at", "parent", "session_id") FROM stdin;
\.


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sso_providers" ("id", "resource_id", "created_at", "updated_at", "disabled") FROM stdin;
\.


--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."saml_providers" ("id", "sso_provider_id", "entity_id", "metadata_xml", "metadata_url", "attribute_mapping", "created_at", "updated_at", "name_id_format") FROM stdin;
\.


--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."saml_relay_states" ("id", "sso_provider_id", "request_id", "for_email", "redirect_to", "created_at", "updated_at", "flow_state_id") FROM stdin;
\.


--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sso_domains" ("id", "sso_provider_id", "domain", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: alumnos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."alumnos" ("id", "created_at", "NIA", "nombre", "apellido", "apellido 2", "telefono", "provincia", "localidad", "codigo_postal", "direccion", "email_alumno", "sexo", "preferencias_fp", "vehiculo", "ciclo_formativo", "estado", "motivo", "dni") FROM stdin;
38	2025-10-06 20:35:10.535306+00	NIA123	Carlos Antonio	Pisciolari	\N	35446656	\N	Santa Fe	2005	JP Lopez 332	cpiscio@gmail.com	\N	"Departamento Comercio Ext/aduanas"	No	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	12124155C
48	2025-10-08 14:23:07.388571+00	\N	Florencia	Blesio	\N	\N	\N	Xirivella	46006	Entre rios 2343	flor@gmail.com	\N	"Desarrollo software"	No	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	3589949
73	2025-10-10 07:39:10.816126+00	A324234	Diego 	Leuco	\N	342344	\N	Xirivella	46006	San Martin 1234	laura@gmail.com	\N	"Departamento de Marketing (estrategia/campañas)"	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	133442121
44	2025-10-08 08:59:56.953281+00	A2323A	Mica	Vazquez	\N	5496521545	\N	Buenos Aires	5002	Belgrano 123	mica@gmail.com	\N	"Gestión de eventos"	No	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	305545545
77	2025-10-10 08:47:59.929499+00	A2323	Julieta	Venturini	\N	352597979	\N	Colonia Caroya	5000	San Mateo 2332	juli@gmail.com	\N	"Gestión de almacén y stock"	No	"TRANSPORTE Y LOGÍSTICA"	Sin Empresa	\N	331545454
49	2025-10-08 14:23:47.086472+00	\N	Federico	Garcia	\N	\N	\N	Xirivella	03560	Entre rios 2343	fede@gmail.com	\N	"Soporte técnico y mantenimiento de apps"	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	365656
50	2025-10-08 14:24:32.74522+00	\N	Agustina	Pisciolari	\N	\N	\N	Xirivella	03580	Entre rios 2343	agus@gmail.com	\N	"Desarrollo aplicaciones móviles"	No	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	45212121
\.


--
-- Data for Name: alumno_estados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."alumno_estados" ("id", "created_at", "email_enviado", "match_fp", "fp_enprogreso", "fp_finalizada", "alumno", "form_completo", "documentacion_completa", "evaluacion_enviada", "evaluacion_completa", "fp_asignada") FROM stdin;
34	2025-10-08 14:23:07.56044+00	2025-10-09	2025-10-13	\N	\N	3589949	2025-10-08	\N	\N	\N	\N
66	2025-10-10 07:41:11.78508+00	\N	2025-10-13	\N	\N	133442121	\N	\N	\N	\N	2025-10-13
40	2025-10-08 16:18:08.277103+00	2025-10-09	2025-10-13	\N	\N	305545545	2025-10-09	\N	\N	\N	2025-10-13
67	2025-10-10 08:48:22.648285+00	\N	2025-10-13	\N	\N	331545454	\N	\N	\N	\N	2025-10-13
35	2025-10-08 14:23:47.678422+00	2025-10-09	2025-10-13	\N	\N	365656	2025-10-08	\N	\N	\N	2025-10-13
36	2025-10-08 14:24:32.992529+00	2025-10-08	2025-10-13	\N	\N	45212121	2025-10-08	\N	\N	\N	2025-10-13
29	2025-10-06 20:40:42.690065+00	2025-10-07	2025-10-13	\N	\N	12124155C	2025-10-06	\N	\N	\N	2025-10-13
\.


--
-- Data for Name: contacto_alumnos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."contacto_alumnos" ("id", "created_at", "email_alumno", "email_enviado") FROM stdin;
3	2025-10-08 09:12:09.732515+00	antopiscio@gmail.com	2025-10-08
\.


--
-- Data for Name: contacto_empresas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."contacto_empresas" ("id", "created_at", "email_empresa", "email_enviado") FROM stdin;
5	2025-09-30 09:27:29.768603+00	apisciolari@gmail.com	2025-09-30
7	2025-09-30 09:54:16.396855+00	antonela.pisciolari@embatconsultora.com	2025-09-30
8	2025-09-30 09:54:16.621753+00	antopiscio@gmail.com	2025-09-30
12	2025-10-03 09:15:44.001699+00	avicente@campuscamarafp.com	2025-10-03
13	2025-10-03 09:15:44.116178+00	msofia.aguirre@gmail.com	2025-10-03
\.


--
-- Data for Name: empresas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."empresas" ("id", "created_at", "CIF", "nombre", "direccion", "provincia", "localidad", "codigo_postal", "telefono", "fax", "tipo_empresa", "email_empresa", "responsable_legal", "nif_responsable_legal", "horario", "pagina_web", "nombre_rellena") FROM stdin;
4	2025-09-25 10:11:38.258311+00	C23233X	Luzu	Sueca 23	\N	Buenos aires	\N	549875441212	\N	\N	luzu@gmail.com	adasd	223432	wewe	asdasd	dsasda
12	2025-09-30 09:42:16.17365+00	Z233123V	Amazon	5th avenue	\N	New York	\N	1556844664	\N	\N	rick@amazon.com	\N	\N	\N	\N	\N
13	2025-09-30 10:58:32.212841+00	S4N0M4	Sanoma	Isabel la catolica 12, 4A	\N	L'hospitalet, Barcelona	08904	63454545	\N	\N	eugenia@sanoma.com	Mark Twain	Z2332323X	8 a 16	www.sanoma.com	Eugenia Orlanda
1	2025-09-24 13:46:38.500594+00	B22590715	Tuqui	Sueca 78	\N	Valencia	\N	634035788	\N	\N	tuqui.food@gmail.com	Antonela Pisciolari	\N	\N	\N	\N
15	2025-10-03 09:06:12.956718+00	B23423	Demo	montgoming 15	\N	Xirivella	46006	54654654	\N	\N	antopiscio@gmail.com	dasd	asdasd	8-18	\N	Antonela Pisciolari
16	2025-10-07 07:10:02.962326+00	B2332332	Google	Colon 1243, Xirivella	\N	Xirivella	46006	63564646	\N	\N	info@google.com	Mike Towers	Z213213S	08:00:00 - 20:00:00		Anto Piscio
22	2025-10-07 17:08:53.615364+00	COR2323	Microsoft	San Juan 123	\N	Cordoba	5000	5546546	\N	\N	micro@info.com	Tati Rouse	X2132131	9-18	www.microsoft.com	Ester
24	2025-10-08 11:22:22.82708+00	B232323	Iberostar	San calletano 323	\N	Valencia	46005	654654654	\N	\N	diego@iberostar.com	Martin	B232132	07:00:00 - 04:00:00		\N
25	2025-10-08 12:11:12.1541+00	B23232	Intel	Ituzaingo 123	\N	Cordoba	5000	423234	\N	\N	anto@intel.com	Martin Bert	34243434	09:00:00 - 14:13:00	www.intel.com	\N
27	2025-10-08 15:08:11.614332+00	ASD12312	ERSA	Colon 123	\N	Xirivella	46006	23434234	\N	\N	flor@ersa.com	Marcos Antonios Solis	2323123	17:05:00 - 17:05:00		\N
28	2025-10-08 15:09:21.665035+00	ASD232	FIAT	Colon 123	\N	Xirivella	46006	23434234	\N	\N	flor@ersa.com	Marcos Antonios Solis	2323123	17:05:00 - 17:05:00		\N
30	2025-10-09 11:14:21.842868+00	B2322323	Peugeot	San Martin 1220	\N	Valencia	45201	635977845	\N	\N	anto@peugeot.com	Yoyi Francella	N232344Z	08:00:00 - 20:00:00	www.peugeot.com	\N
\.


--
-- Data for Name: empresa_estados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."empresa_estados" ("id", "created_at", "email_enviado", "form_completo", "contrato_firmado", "fp_asignada", "fp_enprogreso", "fp_finalizada", "empresa", "documentacion_completa", "match_fp", "evaluacion_enviada", "evaluacion_completa") FROM stdin;
13	2025-09-30 10:58:32.356181+00	2025-09-30	2025-09-30	\N	\N	\N	\N	S4N0M4	\N	\N	\N	\N
7	2025-09-30 10:04:38.98733+00	2025-10-03	2025-10-03	\N	\N	\N	\N	B22590715	\N	\N	\N	\N
4	2025-09-30 09:27:29.610905+00	2025-10-03	2025-09-30	\N	\N	\N	\N	C23233X	\N	\N	\N	\N
34	2025-10-07 07:10:03.098841+00	2025-10-07	2025-10-07	\N	\N	\N	\N	B2332332	2025-10-08	\N	\N	\N
28	2025-10-03 09:06:13.097851+00	2025-10-08	2025-10-03	\N	\N	\N	\N	B23423	2025-10-03	\N	\N	\N
43	2025-10-08 11:22:22.980418+00	\N	2025-10-08	\N	\N	\N	\N	B232323	\N	\N	\N	\N
44	2025-10-08 12:11:12.387657+00	2025-10-08	2025-10-08	\N	\N	\N	\N	B23232	\N	\N	\N	\N
47	2025-10-08 15:08:11.848051+00	\N	2025-10-08	\N	\N	\N	\N	ASD12312	\N	\N	\N	\N
48	2025-10-08 15:09:21.823931+00	\N	2025-10-08	\N	\N	\N	\N	ASD232	\N	\N	\N	\N
50	2025-10-09 11:14:21.965966+00	\N	2025-10-09	\N	\N	\N	\N	B2322323	\N	\N	\N	\N
\.


--
-- Data for Name: forms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."forms" ("id", "created_at", "nombre", "tipo", "descripcion") FROM stdin;
1	2025-09-25 06:42:34.493665+00	Formación Empresas	empresa	Ficha 2025/2026
2	2025-09-25 06:43:22.636153+00	Alumnos Formación	alumnos	Este formulario tiene como objetivo conocer vuestras preferencias para la Formación en Empresa. \n⚠️ Importante: La información que facilitéis será tenida en cuenta en el proceso de asignación, pero la decisión final dependerá de:\nEl tipo de empresas solicitantes.\nLos requisitos que planteen.\nVuestro perfil, potencial y desempeño académico.\nPor tanto, aunque intentaremos ajustarnos en la medida de lo posible a vuestras preferencias, no podemos garantizar que se cumplan.
\.


--
-- Data for Name: form_fields; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."form_fields" ("id", "created_at", "form", "label", "type", "options", "required", "order_index", "category", "columnName") FROM stdin;
6	2025-09-25 07:02:40.99598+00	1	TELÉFONO DE CONTACTO DE LA EMPRESA	Texto	\N	f	6	Empresa	telefono
7	2025-09-25 07:02:47.639674+00	1	EMAIL DE CONTACTO DE LA EMPRESA 	Texto	\N	t	7	Empresa	email_empresa
5	2025-09-25 07:02:09.820032+00	1	NOMBRE DE LA PERSONA QUE RELLENA EL CUESTIONARIO	Texto	\N	f	5	Empresa	nombre_rellena
4	2025-09-25 07:01:59.303951+00	1	CIF	Texto	\N	t	4	Empresa	CIF
10	2025-09-25 07:03:10.654309+00	1	TUTOR (Persona responsable del alumno en la empresa)	Texto	\N	t	10	Empresa	nombre_tutor
11	2025-09-25 07:03:17.948714+00	1	NIF DEL TUTOR	Texto	\N	t	11	Empresa	NIF_tutor
12	2025-09-25 07:03:26.921987+00	1	E-MAIL DEL TUTOR	Texto	\N	t	12	Empresa	email_tutor
21	2025-09-25 07:05:18.754215+00	1	DESCRIBE EN QUÉ PROYECTO/S PODRÍA COLABORAR EL ALUMNO EN PRÁCTICAS.	Texto	\N	f	21	FP	proyectos
22	2025-09-25 07:05:26.571224+00	1	POR FAVOR, INDÍCANOS SI EL ALUMNO DEBE CUMPLIR ALGÚN REQUISITO ADICIONAL. (Ejemplo: B1 de inglés, que sepa trabajar en equipo, que sea tolerante a la presión, que viva en Valencia capital...)	Texto	\N	f	22	FP	requisitos
13	2025-09-25 07:03:32.584874+00	1	TELÉFONO DEL TUTOR	Texto	\N	t	13	Empresa	telefono_tutor
18	2025-09-25 07:04:29.413346+00	1	¿DE QUE CICLO/S FORMATIVO/S OS INTERESA INCORPORAR ALUMNOS EN PRÁCTICAS Y CANTIDAD DE ALUMNO POR CADA UNO?(Puedes seleccionar uno o varios)	OpcionesConCantidad	"[\\"COMERCIO INTERNACIONAL\\", \\"TRANSPORTE Y LOGÍSTICA\\", \\"MARKETING Y PUBLICIDAD\\", \\"DESARROLLO DE APLICACIONES MULTIPLATAFORMA\\", \\"DESARROLLO APLICACIONES WEB\\"]"	f	18	FP	ciclos_formativos
26	2025-09-25 08:10:00.166624+00	1	¿SE NECESITA VEHÍCULO PROPIO PARA PODER ACCEDER A VUESTRAS INSTALACIONES?	Si/No	\N	t	24	FP	vehiculo
28	2025-09-25 14:21:33.618297+00	2	NOMBRE	Texto	\N	t	1	Alumno	nombre
29	2025-09-25 14:21:38.814434+00	2	APELLIDOS	Texto	\N	t	2	Alumno	apellido
25	2025-09-25 08:09:29.124933+00	1	¿EN QUÉ PUESTOS/ÁREAS SE DESARROLLARÍA LA PRÁCTICA? 	Opciones	"{\\"COMERCIO INTERNACIONAL\\": [\\"Departamento Export/Import\\", \\"Departamento Comercio Exterior/Aduanas\\", \\"Compras internacionales/ Aprovisionamiento\\", \\"Atención a clientes internacionales\\", \\"Gestión documental/Almacén\\", \\"Preguntar más adelante...\\"], \\"TRANSPORTE Y LOGÍSTICA\\": [\\"Gestión de tráfico y transporte terrestres marítimo o aéreo\\", \\"Gestión de almacén y stock\\", \\"Operaciones logísticas y distribución\\", \\"Atención al cliente/logística inversa (devoluciones)\\", \\"Administración y documentación del transporte\\", \\"Preguntar más adelante...\\"], \\"MARKETING Y PUBLICIDAD\\": [\\"Departamento de Marketing (estrategia campañas)\\", \\"Publicidad y comunicación (redes sociales)\\", \\"Marketing Digital (SEO/SEM)\\", \\"Gestión de eventos\\", \\"Atención al cliente y fidelización\\", \\"Estudio de mercado e investigación comercial\\", \\"Preguntar más adelante...\\"], \\"DESARROLLO APPS MULTIPLATAFORMA\\": [\\"Desarrollo aplicaciones móviles\\", \\"Desarrollo Software\\", \\"Bases de datos y gestión de información\\", \\"Soporte técnico y mantenimiento de apps\\", \\"Integración de sistemas multiplataforma\\", \\"Preguntar más adelante...\\"], \\"DESARROLLO APPS WEB\\": [\\"Desarrollo Fronted\\", \\"Desarrollo Backend\\", \\"Bases de datos\\", \\"Soporte técnico en entornos web\\", \\"Administración de sistemas web/hosting\\", \\"Preguntar más adelante...\\"]}"	t	20	FP	areas
23	2025-09-25 07:05:35.922414+00	1	SI EL ALUMNO CUBRE VUESTRAS EXPECTATIVAS, ¿HABRÍA POSIBILIDAD DE HACERLE UN CONTRATO LABORAL?	Si/No	\N	t	18	FP	contrato
27	2025-09-25 13:22:47.253705+00	1	CP	Texto	\N	t	3	Empresa	codigo_postal
35	2025-09-25 14:26:57.495708+00	2	DNI/NIE	Texto	\N	t	3	Alumno	dni
32	2025-09-25 14:22:28.56535+00	2	LOCALIDAD	Texto	\N	t	5	Alumno	localidad
33	2025-09-25 14:22:36.049179+00	2	DISPONES DE VEHÍCULO PROPIO	Si/No	\N	t	6	Alumno	vehiculo
1	2025-09-25 07:01:11.35423+00	1	NOMBRE DE LA EMPRESA	Texto	\N	t	1	Empresa	nombre
2	2025-09-25 07:01:39.772774+00	1	DIRECCIÓN COMPLETA (Calle, número, CP)	Texto	\N	t	2	Empresa	direccion
3	2025-09-25 07:01:54.664717+00	1	LOCALIDAD	Texto	\N	f	3	Empresa	localidad
8	2025-09-25 07:02:56.008235+00	1	NOMBRE DEL RESPONSABLE LEGAL DE LA EMPRESA	Texto	\N	t	8	Empresa	responsable_legal
9	2025-09-25 07:03:03.122791+00	1	NIF DEL RESPONSABLE DE LA EMPRESA	Texto	\N	t	9	Empresa	nif_reponsable_legal
14	2025-09-25 07:03:42.725368+00	1	HORARIO DE LA EMPRESA	Texto	\N	t	14	Empresa	horario
15	2025-09-25 07:03:49.606937+00	1	PÁGINA WEB DE LA EMPRESA	Texto	\N	t	15	Empresa	pagina_web
16	2025-09-25 07:04:01.354965+00	1	DIRECCIÓN DEL CENTRO DE TRABAJO (Rellenar, en el caso de ser diferente al domicilio de la empresa)	Texto	\N	f	16	Empresa	direccion_centro_trabajo
17	2025-09-25 07:04:16.154784+00	1	LOCALIDAD DEL CENTRO DE TRABAJO (Rellenar, en el caso de ser diferente al domicilio de la empresa)	Texto	\N	f	17	Empresa	localidad_centro_trabajo
30	2025-09-25 14:22:10.364133+00	2	CICLO FORMATIVO	Opciones	"[\\"COMERCIO INTERNACIONAL\\", \\"TRANSPORTE Y LOGÍSTICA\\", \\"MARKETING Y PUBLICIDAD\\", \\"DESARROLLO APLICACIONES MULTIPLATAFORMA\\", \\"DESARROLLO APLICACIONES WEB\\"]"	t	7	Alumno	ciclo_formativo
31	2025-09-25 14:22:22.837033+00	2	INDÍCANOS TU DIRECCIÓN (calle, número, código postal)	Texto	\N	t	4	Alumno	direccion
34	2025-09-25 14:25:31.797029+00	2	PREFERENCIAS PROFESIONALES - MARCAR SOLAMENTE EL ÁREA DE VUESTRO CICLO FORMATIVO	Opciones	"{\\"COMERCIO INTERNACIONAL\\": [\\"Departamento Export/import\\", \\"Departamento Comercio Ext/aduanas\\", \\"Compras internacionales/ aprovisionamiento\\", \\"Atención a clientes internacionales\\", \\"Gestión documental/ almacén\\"], \\"TRANSPORTE Y LOGÍSTICA\\": [\\"Gestión de tráfico y transporte terrestre; marítimo o aéreo\\", \\"Gestión de almacén y stock\\", \\"Operaciones logísticas y distribución\\", \\"Atención al cliente/logística inversa (devoluciones)\\", \\"Administración y documentación de transporte\\"], \\"MARKETING Y PUBLICIDAD\\": [\\"Departamento de Marketing (estrategia/campañas)\\", \\"Publicidad y Comunicación (redes sociales)\\", \\"Marketing digital (SEO/SEM)\\", \\"Gestión de eventos\\", \\"Atención al cliente y fidelización\\", \\"Estudios de mercado e investigación comercial\\"], \\"DESARROLLO APLICACIONES MULTIPLATAFORMA\\": [\\"Desarrollo aplicaciones móviles\\", \\"Desarrollo software\\", \\"Bases de datos y gestión de información\\", \\"Soporte técnico y mantenimiento de apps\\", \\"Integración de sistemas multiplataforma\\"], \\"DESARROLLO APLICACIONES WEB\\": [\\"Desarrollo fronted\\", \\"Desarrollo backend\\", \\"Bases de datos\\", \\"Soporte técnico en entornos web\\", \\"Administración de sistemas web/hosting\\"]}"	t	8	Alumno	preferencias_fp
\.


--
-- Data for Name: form_answers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."form_answers" ("id", "created_at", "form", "field_id", "empresa", "value", "updated_at") FROM stdin;
1	2025-09-25 10:28:16.660308+00	1	1	\N	Luzu	\N
2	2025-09-25 10:28:16.756168+00	1	2	\N	asdadsa	\N
3	2025-09-25 10:28:16.861679+00	1	3	\N	adasd	\N
4	2025-09-25 10:28:16.95503+00	1	4	\N	C23233X	\N
5	2025-09-25 10:28:17.059579+00	1	5	\N	dsasda	\N
6	2025-09-25 10:28:17.16778+00	1	6	\N	123	\N
7	2025-09-25 10:28:17.264263+00	1	7	\N	123213	\N
8	2025-09-25 10:28:17.356617+00	1	8	\N	adasd	\N
9	2025-09-25 10:28:17.454803+00	1	9	\N	223432	\N
10	2025-09-25 10:28:17.560201+00	1	10	\N	adas	\N
11	2025-09-25 10:28:17.65239+00	1	11	\N	24324	\N
12	2025-09-25 10:28:17.740243+00	1	12	\N	23423	\N
13	2025-09-25 10:28:17.834598+00	1	13	\N	234234	\N
14	2025-09-25 10:28:17.933944+00	1	14	\N	wewe	\N
15	2025-09-25 10:28:18.040827+00	1	15	\N	asdasd	\N
16	2025-09-25 10:28:18.135697+00	1	16	\N	asdsad	\N
17	2025-09-25 10:28:18.23465+00	1	17	\N	asdsad	\N
18	2025-09-25 10:28:18.326841+00	1	18	\N	{"COMERCIO INTERNACIONAL": 2, "TRANSPORTE Y LOGÍSTICA": 1}	\N
19	2025-09-25 10:28:18.420207+00	1	25	\N	["Departamento Export/Import", "Gestión de tráfico y transporte terrestres marítimo o aéreo"]	\N
20	2025-09-25 10:28:18.518331+00	1	21	\N	sdsdas	\N
21	2025-09-25 10:28:18.634273+00	1	22	\N	sdasdasd	\N
22	2025-09-25 10:28:18.735702+00	1	23	\N	Sí	\N
23	2025-09-25 10:28:18.835337+00	1	26	\N	Sí	\N
24	2025-09-25 10:30:49.638779+00	1	1	\N	Luzu	\N
25	2025-09-25 10:30:49.744354+00	1	2	\N	asdadsa	\N
26	2025-09-25 10:30:49.854559+00	1	3	\N	adasd	\N
27	2025-09-25 10:30:49.956663+00	1	4	\N	C23233X	\N
28	2025-09-25 10:30:50.059184+00	1	5	\N	dsasda	\N
29	2025-09-25 10:30:50.16435+00	1	6	\N	123	\N
30	2025-09-25 10:30:50.267969+00	1	7	\N	123213	\N
31	2025-09-25 10:30:50.36923+00	1	8	\N	adasd	\N
32	2025-09-25 10:30:50.474939+00	1	9	\N	223432	\N
33	2025-09-25 10:30:50.574247+00	1	10	\N	adas	\N
34	2025-09-25 10:30:50.676053+00	1	11	\N	24324	\N
35	2025-09-25 10:30:50.875978+00	1	12	\N	23423	\N
36	2025-09-25 10:30:51.073232+00	1	13	\N	234234	\N
37	2025-09-25 10:30:51.287276+00	1	14	\N	wewe	\N
38	2025-09-25 10:30:51.38166+00	1	15	\N	asdasd	\N
39	2025-09-25 10:30:51.605161+00	1	16	\N	asdsad	\N
40	2025-09-25 10:30:51.729063+00	1	17	\N	asdsad	\N
41	2025-09-25 10:30:51.932793+00	1	18	\N	{"COMERCIO INTERNACIONAL": 2, "TRANSPORTE Y LOGÍSTICA": 1}	\N
42	2025-09-25 10:30:52.029236+00	1	25	\N	["Departamento Export/Import", "Gestión de tráfico y transporte terrestres marítimo o aéreo"]	\N
43	2025-09-25 10:30:52.125586+00	1	21	\N	sdsdas	\N
44	2025-09-25 10:30:52.226072+00	1	22	\N	sdasdasd	\N
45	2025-09-25 10:30:52.324504+00	1	23	\N	Sí	\N
46	2025-09-25 10:30:52.439705+00	1	26	\N	Sí	\N
47	2025-09-25 10:34:14.34777+00	1	1	\N	Luzu	\N
48	2025-09-25 10:34:14.45663+00	1	2	\N	asdadsa	\N
49	2025-09-25 10:34:14.553536+00	1	3	\N	adasd	\N
50	2025-09-25 10:34:14.650918+00	1	4	\N	C23233X	\N
51	2025-09-25 10:34:14.756882+00	1	5	\N	dsasda	\N
52	2025-09-25 10:34:14.885141+00	1	6	\N	123	\N
53	2025-09-25 10:34:14.9893+00	1	7	\N	123213	\N
54	2025-09-25 10:34:15.092105+00	1	8	\N	adasd	\N
55	2025-09-25 10:34:15.31738+00	1	9	\N	223432	\N
56	2025-09-25 10:34:15.427316+00	1	10	\N	adas	\N
57	2025-09-25 10:34:15.538457+00	1	11	\N	24324	\N
58	2025-09-25 10:34:15.643824+00	1	12	\N	23423	\N
59	2025-09-25 10:34:15.747828+00	1	13	\N	234234	\N
60	2025-09-25 10:34:15.855268+00	1	14	\N	wewe	\N
61	2025-09-25 10:34:15.946672+00	1	15	\N	asdasd	\N
62	2025-09-25 10:34:16.054195+00	1	16	\N	asdsad	\N
63	2025-09-25 10:34:16.168604+00	1	17	\N	asdsad	\N
64	2025-09-25 10:34:16.284724+00	1	18	\N	{"COMERCIO INTERNACIONAL": 2, "TRANSPORTE Y LOGÍSTICA": 1}	\N
65	2025-09-25 10:34:16.399588+00	1	25	\N	["Departamento Export/Import", "Gestión de tráfico y transporte terrestres marítimo o aéreo"]	\N
66	2025-09-25 10:34:16.501026+00	1	21	\N	sdsdas	\N
67	2025-09-25 10:34:16.599818+00	1	22	\N	sdasdasd	\N
68	2025-09-25 10:34:16.710864+00	1	23	\N	Sí	\N
69	2025-09-25 10:34:16.816196+00	1	26	\N	Sí	\N
70	2025-09-25 10:34:30.33095+00	1	1	\N	Luzu	\N
71	2025-09-25 10:34:30.442437+00	1	2	\N	asdadsa	\N
72	2025-09-25 10:34:30.546205+00	1	3	\N	adasd	\N
73	2025-09-25 10:34:30.661644+00	1	4	\N	C23233X	\N
74	2025-09-25 10:34:30.763659+00	1	5	\N	dsasda	\N
75	2025-09-25 10:34:30.873934+00	1	6	\N	123	\N
76	2025-09-25 10:34:30.990732+00	1	7	\N	123213	\N
77	2025-09-25 10:34:31.098476+00	1	8	\N	adasd	\N
78	2025-09-25 10:34:31.201058+00	1	9	\N	223432	\N
79	2025-09-25 10:34:31.349616+00	1	10	\N	adas	\N
80	2025-09-25 10:34:31.449949+00	1	11	\N	24324	\N
81	2025-09-25 10:34:31.564123+00	1	12	\N	23423	\N
82	2025-09-25 10:34:31.672391+00	1	13	\N	234234	\N
83	2025-09-25 10:34:31.784695+00	1	14	\N	wewe	\N
84	2025-09-25 10:34:31.883513+00	1	15	\N	asdasd	\N
85	2025-09-25 10:34:31.993615+00	1	16	\N	asdsad	\N
86	2025-09-25 10:34:32.094737+00	1	17	\N	asdsad	\N
87	2025-09-25 10:34:32.194749+00	1	18	\N	{"COMERCIO INTERNACIONAL": 2, "TRANSPORTE Y LOGÍSTICA": 1}	\N
88	2025-09-25 10:34:32.338382+00	1	25	\N	["Departamento Export/Import", "Gestión de tráfico y transporte terrestres marítimo o aéreo"]	\N
89	2025-09-25 10:34:32.444883+00	1	21	\N	sdsdas	\N
90	2025-09-25 10:34:32.563126+00	1	22	\N	nsfsdf	\N
91	2025-09-25 10:34:32.678237+00	1	23	\N	No	\N
92	2025-09-25 10:34:32.784241+00	1	26	\N	No	\N
\.


--
-- Data for Name: oferta_fp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."oferta_fp" ("id", "created_at", "empresa", "ciclos_formativos", "puestos", "requisitos", "contrato", "vehiculo", "estado", "motivo", "nombre_tutor", "nif_tutor", "email_tutor", "telefono_tutor", "direccion_empresa", "localidad_empresa", "cp_empresa", "nombre_rellena_form", "cupo_alumnos") FROM stdin;
17	2025-10-08 15:10:21.386314+00	ASD232	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": "Proyecto 1"}, {"area": "Compras internacionales/ aprovisionamiento", "proyecto": "Proyecto 12"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Proyecto3"}, {"area": "Gestión de eventos", "proyecto": "Proyecto 4"}]}	B1 de ingles	Sí	Sí	Completa	\N	Fran Piscio	2323223	fran@ersa.com	323423432	Colon 2423	Xirivella	46006	Florencia Blesio	3
14	2025-10-08 12:15:14.061926+00	B23232	{"COMERCIO INTERNACIONAL": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 2, "disponibles": 2}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Comercio Ext/aduanas", "proyecto": "Valencia"}, {"area": "Atención a clientes internacionales", "proyecto": "asdsad"}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo software", "proyecto": "sitio web"}]}	b1 de ingles	Sí	Sí	Nuevo	\N	Yoyi Vazquez	234234234	yoyi@intel.com	213223432				Anto	2
18	2025-10-09 11:14:22.088632+00	B2322323	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 0}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": "Nuevo Proyecto de cosas"}]}	Trabajo en equipi, b2 ingles, permiso de trabajo	Sí	Sí	Nuevo	\N	Diego Leuco	Z232323N	die@peugeot.com	635897979	San Martin 1220	Valencia	45201	Anto Pisciolari	1
\.


--
-- Data for Name: practicas_fp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."practicas_fp" ("id", "created_at", "empresa", "oferta", "alumno", "ciclo_formativo", "area", "proyecto") FROM stdin;
\.


--
-- Data for Name: practica_estados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."practica_estados" ("id", "created_at", "practicaId", "documentacion_pedida", "documentacion_firmada", "en_progreso", "cancelada", "finalizada") FROM stdin;
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."usuarios" ("id", "created_at", "email", "password") FROM stdin;
1	2025-09-24 13:08:28.062791+00	admin	admin
\.


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."buckets" ("id", "name", "owner", "created_at", "updated_at", "public", "avif_autodetection", "file_size_limit", "allowed_mime_types", "owner_id", "type") FROM stdin;
\.


--
-- Data for Name: buckets_analytics; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."buckets_analytics" ("id", "type", "format", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."objects" ("id", "bucket_id", "name", "owner", "created_at", "updated_at", "last_accessed_at", "metadata", "version", "owner_id", "user_metadata", "level") FROM stdin;
\.


--
-- Data for Name: prefixes; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."prefixes" ("bucket_id", "name", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."s3_multipart_uploads" ("id", "in_progress_size", "upload_signature", "bucket_id", "key", "version", "owner_id", "created_at", "user_metadata") FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."s3_multipart_uploads_parts" ("id", "upload_id", "size", "part_number", "bucket_id", "key", "etag", "owner_id", "version", "created_at") FROM stdin;
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 1, false);


--
-- Name: alumno_estados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."alumno_estados_id_seq"', 83, true);


--
-- Name: alumnos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."alumnos_id_seq"', 97, true);


--
-- Name: contacto_alumnos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."contacto_alumnos_id_seq"', 3, true);


--
-- Name: contacto_empresas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."contacto_empresas_id_seq"', 13, true);


--
-- Name: empresa_estados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."empresa_estados_id_seq"', 50, true);


--
-- Name: empresa_practica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."empresa_practica_id_seq"', 18, true);


--
-- Name: empresas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."empresas_id_seq"', 30, true);


--
-- Name: form_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."form_answers_id_seq"', 92, true);


--
-- Name: form_fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."form_fields_id_seq"', 36, true);


--
-- Name: forms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."forms_id_seq"', 2, true);


--
-- Name: practica_estados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."practica_estados_id_seq"', 1, true);


--
-- Name: practicas_fp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."practicas_fp_id_seq"', 51, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."usuarios_id_seq"', 1, true);


--
-- PostgreSQL database dump complete
--

-- \unrestrict VGnNdwTeWXzSkEaci2J1UYTY8uznSuWEqfRB6f5LviRsUY7qd0h4gcvXoZH8Dgf

RESET ALL;
