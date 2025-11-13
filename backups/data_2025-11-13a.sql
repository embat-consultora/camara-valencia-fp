SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict FR9Yo5jrcOaHzzTI7NoojvQ9QfGVbK5dkNaFtmfpO4DgYoI05m4pcCJSk3SkunI

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
-- Data for Name: oauth_clients; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."oauth_clients" ("id", "client_secret_hash", "registration_type", "redirect_uris", "grant_types", "client_name", "client_uri", "logo_uri", "created_at", "updated_at", "deleted_at", "client_type") FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sessions" ("id", "user_id", "created_at", "updated_at", "factor_id", "aal", "not_after", "refreshed_at", "user_agent", "ip", "tag", "oauth_client_id", "refresh_token_hmac_key", "refresh_token_counter") FROM stdin;
\.


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_amr_claims" ("session_id", "created_at", "updated_at", "authentication_method", "id") FROM stdin;
\.


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_factors" ("id", "user_id", "friendly_name", "factor_type", "status", "created_at", "updated_at", "secret", "phone", "last_challenged_at", "web_authn_credential", "web_authn_aaguid", "last_webauthn_challenge_data") FROM stdin;
\.


--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_challenges" ("id", "factor_id", "created_at", "verified_at", "ip_address", "otp_code", "web_authn_session_data") FROM stdin;
\.


--
-- Data for Name: oauth_authorizations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."oauth_authorizations" ("id", "authorization_id", "client_id", "user_id", "redirect_uri", "scope", "state", "resource", "code_challenge", "code_challenge_method", "response_type", "status", "authorization_code", "created_at", "expires_at", "approved_at") FROM stdin;
\.


--
-- Data for Name: oauth_consents; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."oauth_consents" ("id", "user_id", "client_id", "scopes", "granted_at", "revoked_at") FROM stdin;
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

COPY "public"."alumnos" ("id", "created_at", "NIA", "nombre", "apellido", "apellido 2", "telefono", "provincia", "localidad", "codigo_postal", "direccion", "email_alumno", "sexo", "preferencias_fp", "vehiculo", "ciclo_formativo", "estado", "motivo", "dni", "requisitos", "tipoPractica") FROM stdin;
139	2025-11-03 12:52:58.45846+00	\N	Marina	Baldovi Santiago	\N	\N	\N	Godella	46110	Calle Montgó 2D	marinabalw@gmail.com	\N	["Publicidad y Comunicación (redes sociales)"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	23873689B	\N	Práctica asignada por el centro
140	2025-11-03 12:55:30.908007+00	\N	Paula	Veses Navarro	\N	\N	\N	Lliria	46160	Marc Cornelli Nigrí	paulavesesnavarro@gmail.com	\N	["Publicidad y Comunicación (redes sociales)", "Gestión de eventos"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	73666906E	\N	Práctica asignada por el centro
141	2025-11-03 12:55:47.704964+00	\N	Alvaro	Martínez Perez	\N	\N	\N	Torrent	46900	Calle Lope de Rueda, 9	alvaromartinezperez2006@gmail.com	\N	["Publicidad y Comunicación (redes sociales)", "Gestión de eventos", "Departamento de Marketing (estrategia/campañas)"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	53885085H	\N	Práctica asignada por el centro
142	2025-11-03 12:58:19.150382+00	\N	Rafa	Artesero Bueno	\N	\N	\N	L'Eliana	46183	AV ALCALDE ENRIQUE DARIES 12	rartesero@campuscamarafp.com	\N	["Departamento Comercio Ext/aduanas", "Atención a clientes internacionales", "Compras internacionales/ aprovisionamiento"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	23937154L	\N	Práctica asignada por el centro
143	2025-11-03 12:59:56.60404+00	\N	Carlos	Carbonell Álvarez	\N	\N	\N	Lliria	46160	C/Molí del Bailón 2, 7	carloscarbonellalvarez@gmail.com	\N	["Desarrollo aplicaciones móviles", "Soporte técnico y mantenimiento de apps", "Desarrollo software"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	03162491Z	\N	Práctica asignada por el centro
144	2025-11-03 17:27:59.94601+00	\N	Luis	López Martinez	\N	\N	\N	Godella	46110	Ermita nova 26	llopez@campuscamarafp.com	\N	["Bases de datos y gestión de información"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	49180951M	\N	Práctica asignada por el centro
145	2025-11-03 18:28:02.468006+00	\N	Mónica	Blanco Merino	\N	\N	\N	SANTANDER	39006	paseo de altamira ,130. 3º IZDA	moblancomerino153@gmail.com	\N	["Desarrollo software", "Desarrollo aplicaciones móviles", "Integración de sistemas multiplataforma"]	No	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	72183688M	\N	Práctica asignada por el centro
146	2025-11-03 20:31:57.243818+00	\N	Carlos	Fernandez	\N	\N	\N	Valencia	46023	calle Trafalgar, 52	carlosfer663@gmail.com	\N	["Desarrollo aplicaciones móviles", "Soporte técnico y mantenimiento de apps", "Integración de sistemas multiplataforma"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	53881536B	\N	Práctica asignada por el centro
147	2025-11-04 07:30:43.507368+00	\N	Emilio	Cócera Beltrán	\N	\N	\N	Valencia	46009	C/ Pobla del duc 11, 4	cocerae@gmail.com	\N	["Desarrollo fronted", "Bases de datos", "Desarrollo backend"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	33565150P	\N	Práctica asignada por el centro
148	2025-11-04 08:48:33.309139+00	\N	Nicolás	Beneito Colomina	\N	\N	\N	Valencia	46021	Calle Leandro de Saralegui, 11	nicolas.beneito.work@gmail.com	\N	["Departamento de Marketing (estrategia/campañas)"]	No	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	21808446F	\N	Práctica autogestionada
149	2025-11-04 10:00:11.231237+00	\N	Mariana	Cebrián Meyuy	\N	\N	\N	VALENCIA	46003	C/ NA JORDANA,32, 6	maruum04@gmail.com	\N	["Gestión de tráfico y transporte terrestre; marítimo o aéreo", "Gestión de almacén y stock", "Operaciones logísticas y distribución"]	Sí	"TRANSPORTE Y LOGÍSTICA"	Sin Empresa	\N	44530355D	\N	Práctica asignada por el centro
150	2025-11-04 11:34:39.126115+00	\N	Maite	Castro Giménez	\N	\N	\N	Alfafar	46910	Plaza Poeta Miguel Hernández, 10	mcastro@campuscamarafp.com	\N	["Desarrollo aplicaciones móviles", "Soporte técnico y mantenimiento de apps", "Integración de sistemas multiplataforma"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	44887995E	\N	Práctica autogestionada
151	2025-11-06 14:22:45.239449+00	\N	Andrea	González Arenas	\N	\N	\N	Valencia	46019	Calle Arquitecto Tolsá, 21	andreagonzalezarenas06@gmail.com	\N	["Publicidad y Comunicación (redes sociales)", "Marketing digital (SEO/SEM)", "Gestión de eventos"]	No	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	44923690K	\N	Práctica asignada por el centro
153	2025-11-06 18:06:30.809871+00	\N	Fidel	Lauroba Heinz-Senss	\N	\N	\N	Pobla de vallbona	46185	Calle Nº 28	fidellauheinz@gmail.com	\N	["Desarrollo software", "Desarrollo aplicaciones móviles", "Bases de datos y gestión de información"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	45904659V	\N	Práctica asignada por el centro
154	2025-11-07 11:05:21.893375+00	\N	Emma	Gómez Bayarri	\N	\N	\N	Almàssera	46132	Calle San Vicente Ferrer, 22	emmagb267@gmail.com	\N	["Gestión de eventos", "Publicidad y Comunicación (redes sociales)", "Marketing digital (SEO/SEM)"]	No	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	24449884X	\N	Práctica asignada por el centro
155	2025-11-11 09:32:54.882287+00	\N	Angel	Sospedra Martinez	\N	\N	\N	Torrent	46901	Almirante Churruca 20	asospedra@campuscamarafp.com	\N	["Desarrollo fronted"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	5388103T	\N	Práctica asignada por el centro
156	2025-11-11 09:40:26.735794+00	\N	Alejandro	Gámez Sánchez	\N	\N	\N	Valencia	46182	Carrer 529,9	agamez@campuscamarafp.com	\N	["Desarrollo backend", "Desarrollo fronted"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	76641673S	\N	Práctica asignada por el centro
\.


--
-- Data for Name: alumno_estados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."alumno_estados" ("id", "created_at", "email_enviado", "match_fp", "fp_enprogreso", "fp_finalizada", "alumno", "form_completo", "documentacion_completa", "evaluacion_enviada", "evaluacion_completa", "fp_asignada") FROM stdin;
116	2025-11-03 12:52:58.777112+00	2025-11-03	\N	\N	\N	23873689B	2025-11-03	\N	\N	\N	\N
117	2025-11-03 12:55:31.245636+00	2025-11-03	\N	\N	\N	73666906E	2025-11-03	\N	\N	\N	\N
118	2025-11-03 12:55:47.976183+00	2025-11-03	\N	\N	\N	53885085H	2025-11-03	\N	\N	\N	\N
119	2025-11-03 12:58:19.441912+00	2025-11-03	\N	\N	\N	23937154L	2025-11-03	\N	\N	\N	\N
120	2025-11-03 12:59:56.89658+00	2025-11-03	\N	\N	\N	03162491Z	2025-11-03	\N	\N	\N	\N
126	2025-11-03 17:28:00.796911+00	\N	\N	\N	\N	49180951M	2025-11-03	\N	\N	\N	\N
127	2025-11-03 18:28:02.878194+00	\N	\N	\N	\N	72183688M	2025-11-03	\N	\N	\N	\N
128	2025-11-03 20:31:57.607814+00	\N	\N	\N	\N	53881536B	2025-11-03	\N	\N	\N	\N
129	2025-11-04 07:30:43.925475+00	\N	\N	\N	\N	33565150P	2025-11-04	\N	\N	\N	\N
130	2025-11-04 08:48:33.756596+00	\N	\N	\N	\N	21808446F	2025-11-04	\N	\N	\N	\N
131	2025-11-04 10:00:11.609951+00	\N	\N	\N	\N	44530355D	2025-11-04	\N	\N	\N	\N
132	2025-11-04 11:34:39.506846+00	\N	\N	\N	\N	44887995E	2025-11-04	\N	\N	\N	\N
133	2025-11-06 14:22:45.712851+00	\N	\N	\N	\N	44923690K	2025-11-06	\N	\N	\N	\N
135	2025-11-06 18:06:31.197585+00	\N	\N	\N	\N	45904659V	2025-11-06	\N	\N	\N	\N
136	2025-11-07 11:05:22.334276+00	\N	\N	\N	\N	24449884X	2025-11-07	\N	\N	\N	\N
137	2025-11-11 09:32:55.301008+00	\N	\N	\N	\N	5388103T	2025-11-11	\N	\N	\N	\N
138	2025-11-11 09:40:27.102178+00	\N	\N	\N	\N	76641673S	2025-11-11	\N	\N	\N	\N
\.


--
-- Data for Name: contacto_alumnos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."contacto_alumnos" ("id", "created_at", "email_alumno", "email_enviado") FROM stdin;
\.


--
-- Data for Name: contacto_empresas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."contacto_empresas" ("id", "created_at", "email_empresa", "email_enviado") FROM stdin;
\.


--
-- Data for Name: empresas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."empresas" ("id", "created_at", "CIF", "nombre", "direccion", "provincia", "localidad", "codigo_postal", "telefono", "fax", "tipo_empresa", "email_empresa", "responsable_legal", "nif_responsable_legal", "horario", "pagina_web", "nombre_rellena") FROM stdin;
66	2025-10-30 12:36:49.244809+00	B13983010	ANPHIS SL	Ronda Narciso Monturiol 6	\N	Paterna	46980	638089545	\N	\N	jorge.garcia@anphis.es	Jose Miguel Platero Aznar	73661414G	09:00:00 - 14:00:00	www.anphis.es	\N
67	2025-10-30 17:20:00.364006+00	B96603881	FM Grupo Tecnológico SL	Calle Algepser, 16	\N	Paterna	46980	630114066	\N	\N	alvaro.garcia@fmgrupotec.com	Francisco J. Martínez Herrero	73654348E	08:00:00 - 17:30:00	www.fmgrupotec.com	\N
68	2025-11-03 06:26:20.53208+00	B46401675	EMAC COMPLEMENTOS SL	AV DE MADRID, 6	\N	QUART DE POBLET	46930	670313938	\N	\N	rrhh@emac.es	NURIA BOIX	48382235X	07:30:00 - 17:30:00	www.emac.es	\N
69	2025-11-03 15:41:24.170707+00	B75633016	Espectro Prometeo, S.L.	Calle dels Teixidors, 2, Piso 0,	\N	Valencia	46001	685975118	\N	\N	david@lagobonoia.com	David García Arcos	50868300M	09:00:00 - 14:00:00	https://www.lagobonoia.com/	\N
48	2025-10-27 12:33:30.362771+00	B46001632	AUTOBUSES VIALCO, S.L.	POL.IND PICASSENT CALLE 10 NAVE 8B	\N	PICASSENT	46220	961230673	\N	\N	rrhh@vialcobus.com	RAFAEL LLUESMA GIL	20004251R	09:00:00 - 19:00:00	http://www.vialcobus.com	\N
70	2025-11-04 09:28:29.469173+00	B98154552	VIAN DISA SL	C/ Guillem de Castro, 43	\N	Valencia	46007	680476576	\N	\N	victorgarcia@anasalmeron.es	Ana Díaz Salmerón	53058358A	09:30:00 - 19:30:00	https://anasalmeronformacion.es/	\N
71	2025-11-10 11:10:14.462914+00	B98763360	CONNEXT COMUNICACIÓN DIGITAL SL	Andarella 1, bloque 2, planta 1, puerta 3	\N	Valencia	46950	+34 657241927	\N	\N	admon@connext.es	JOAQUÍN CORTÉS AHULLÓ	20810848B	08:30:00 - 17:30:00	https://www.connext.es	\N
49	2025-10-27 12:41:54.477902+00	B56966534	Grupo Moves Innova	C/Colón 10 13a valencia	\N	Valencia	46004	627024604	\N	\N	info@plan-moves.com	Óscar Colomina	23324155Q	08:30:00 - 15:00:00	Plan-moves.com	\N
50	2025-10-27 12:49:24.515463+00	B98638596	CW Comunicacion S.L.	Calle Nicolas Copernico n8 Despacho 10	\N	Paterna	46980	616026470	\N	\N	direccion@cwcomunicacion.com	Carlos Martínez	24370557X	08:30:00 - 14:30:00	cwcomunicacion.com	\N
52	2025-10-28 09:51:33.98565+00	B40545014	BLACKCROW CONFECCION Y COSTURA SL	C/Padre Jofre,7	\N	VALENCIA	46007	+34687452966	\N	\N	miquel@miquelsuay.com	Maria Jose Fuentes Pardo	B40545014	09:21:00 - 09:21:00	www.miquelsuay.com	\N
55	2025-10-28 10:40:07.302005+00	21003161K	BRILLA INFLUENCERS Y COMUNICACIÓN	AVENIDA CORALINA 22	\N	BÉTERA	46117	644256002	\N	\N	facturacionbrillainfluencers@gmail.com	THAIS GARCÍA MAS	21003161K	09:00:00 - 14:00:00	https://brillainfluencersycomunicacion.com/	\N
56	2025-10-28 12:31:03.724385+00	B44013613	ISTOBAL ESENS	CALLE VILLA DE MADRID Nº 15	\N	L'ALCUDIA	46988	666809485	\N	\N	rmateu@istobal.com	FRANCISCO NAVARRO JARQUE	4660543R	08:00:00 - 18:00:00	ISTOBAL.COM	\N
57	2025-10-28 12:39:54.682971+00	B46445615	SANZ HERMANOS	CTRA BENISSANÓ - OLOCAU	\N	BENISSANÓ	46181	962791441	\N	\N	rrhh@gruposanz.es	JOSE JUAN SANZ PEREZ	24338637-Z	08:30:00 - 18:00:00	https://gruposanz.es	\N
58	2025-10-28 13:16:57.145394+00	B96939798	1Tapiza SL / OGO Furniture	C/ Argenters 31. Pol. Ind. El Alter	\N	Alcàsser	46290	672452797	\N	\N	pedidos@ogofurniture.com	Juan de Dios Pérez Ramos	52842660E	08:00:00 - 17:00:00	www.ogofurniture.com	\N
59	2025-10-28 15:35:22.927483+00	B42749481	TAMARIT ESTUDIO, S.L.	Calle U de Maig 12	\N	Museros	46136	962831220	\N	\N	info@tamaritestudio.com	Miquel	29209987X	08:00:00 - 14:00:00	www.tamaritestudio.com	\N
61	2025-10-29 11:00:21.116881+00	B97881569	COMUNICA2 SL	C/ PUERTO RICO, 48 BAJO DCHA	\N	Valenciaç	46006	666915903	\N	\N	miguel@comunica-2.es	Miguel Rives	44500241W	08:30:00 - 16:30:00	www.comunica-2.es	\N
62	2025-10-29 11:57:25.260914+00	B96709134	Beta Formación	c/ Tirant Lo Blanc, 26	\N	TORRENT	46900	687724161	\N	\N	victoriav@betaformacion.com	Victoria Vazquez Miguel	53606749M	09:00:00 - 20:30:00	www.betaformacion.com	\N
64	2025-10-29 14:27:43.374496+00	G96308184	Instituto Tecnológico de Embalaje, Transporte y Logística	C/ALBERT EINSTEIN 1, PARQUE TECNOLOGICO, 46980, Paterna	\N	Paterna	46980	672387733	\N	\N	amparo.company@itene.com	Demetrio Gil	73572279V	08:00:00 - 17:00:00	https://itene.com	\N
65	2025-10-29 17:30:51.083128+00	B10649580	Gloval Gestión De Ocio 2022 SL	AV.CATALUNYA 16 ENTRESUELO IZQ B	\N	Valencia	46020	650026921	\N	\N	alejandro.rosalen@gmail.com	Alejandro Rosalen Folgado	53251545J	10:00:00 - 19:00:00	https://cosmicgroup.es/	\N
\.


--
-- Data for Name: empresa_estados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."empresa_estados" ("id", "created_at", "email_enviado", "form_completo", "contrato_firmado", "fp_asignada", "fp_enprogreso", "fp_finalizada", "empresa", "documentacion_completa", "match_fp", "evaluacion_enviada", "evaluacion_completa") FROM stdin;
72	2025-10-27 12:33:30.806776+00	2025-10-27	2025-10-27	\N	\N	\N	\N	B46001632	\N	\N	\N	\N
73	2025-10-27 12:41:54.72528+00	2025-10-27	2025-10-27	\N	\N	\N	\N	B56966534	\N	\N	\N	\N
74	2025-10-27 12:49:24.798515+00	2025-10-27	2025-10-27	\N	\N	\N	\N	B98638596	\N	\N	\N	\N
79	2025-10-28 09:51:34.953869+00	2025-10-28	2025-10-28	\N	\N	\N	\N	B40545014	\N	\N	\N	\N
82	2025-10-28 10:40:07.629018+00	2025-10-28	2025-10-28	\N	\N	\N	\N	21003161K	\N	\N	\N	\N
83	2025-10-28 12:31:04.101709+00	2025-10-28	2025-10-28	\N	\N	\N	\N	B44013613	\N	\N	\N	\N
84	2025-10-28 12:39:55.310551+00	2025-10-28	2025-10-28	\N	\N	\N	\N	B46445615	\N	\N	\N	\N
85	2025-10-28 13:16:57.506284+00	2025-10-28	2025-10-28	\N	\N	\N	\N	B96939798	\N	\N	\N	\N
86	2025-10-28 15:35:23.285686+00	2025-10-28	2025-10-28	\N	\N	\N	\N	B42749481	\N	\N	\N	\N
94	2025-10-29 11:00:21.358272+00	2025-10-29	2025-10-29	\N	\N	\N	\N	B97881569	\N	\N	\N	\N
98	2025-10-29 14:27:43.807853+00	2025-10-29	2025-10-29	\N	\N	\N	\N	G96308184	\N	\N	\N	\N
96	2025-10-29 11:57:25.628497+00	2025-10-29	2025-10-29	\N	\N	\N	\N	B96709134	\N	\N	\N	\N
102	2025-10-30 12:36:49.672909+00	2025-10-30	2025-10-30	\N	\N	\N	\N	B13983010	\N	\N	\N	\N
101	2025-10-29 17:30:51.423926+00	2025-10-30	2025-10-29	\N	\N	\N	\N	B10649580	\N	\N	\N	\N
105	2025-10-30 17:20:00.811385+00	\N	2025-10-30	\N	\N	\N	\N	B96603881	\N	\N	\N	\N
106	2025-11-03 06:26:21.412056+00	\N	2025-11-03	\N	\N	\N	\N	B46401675	\N	\N	\N	\N
107	2025-11-03 15:41:24.55809+00	\N	2025-11-03	\N	\N	\N	\N	B75633016	\N	\N	\N	\N
108	2025-11-04 09:28:29.861351+00	\N	2025-11-04	\N	\N	\N	\N	B98154552	\N	\N	\N	\N
109	2025-11-10 11:10:14.916443+00	\N	2025-11-10	\N	\N	\N	\N	B98763360	\N	\N	\N	\N
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

COPY "public"."oferta_fp" ("id", "created_at", "empresa", "ciclos_formativos", "puestos", "requisitos", "contrato", "vehiculo", "estado", "motivo", "direccion_empresa", "localidad_empresa", "cp_empresa", "nombre_rellena_form", "cupo_alumnos", "tutor") FROM stdin;
39	2025-10-28 09:51:35.545254+00	B40545014	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 2, "disponibles": 2}}	{"COMERCIO INTERNACIONAL": [{"area": "Compras internacionales/ aprovisionamiento", "proyecto": "www.clec.fashion"}, {"area": "Atención a clientes internacionales", "proyecto": "www.miquelsuay.com; www.clec.fashion"}, {"area": "Gestión documental/ almacén", "proyecto": "www.miquelsuay.com"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "www.miquelsuay.com; www.clec.fashion "}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Gestión de eventos", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Atención al cliente y fidelización", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "www.miquelsuay.com"}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": "www.miquelsuay.com; www.clec.fashion"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Desarrollo backend", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Soporte técnico en entornos web", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Administración de sistemas web/hosting", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}]}	B1 de ingles	Sí	No	Nuevo	\N	PADRE JOFRE,7	VALENCIA	46007	Miquel Angel Garcia Gimeno	8	9
40	2025-10-28 09:51:35.555347+00	B40545014	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 2, "disponibles": 2}}	{"COMERCIO INTERNACIONAL": [{"area": "Compras internacionales/ aprovisionamiento", "proyecto": "www.clec.fashion"}, {"area": "Atención a clientes internacionales", "proyecto": "www.miquelsuay.com; www.clec.fashion"}, {"area": "Gestión documental/ almacén", "proyecto": "www.miquelsuay.com"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "www.miquelsuay.com; www.clec.fashion "}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Gestión de eventos", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Atención al cliente y fidelización", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "www.miquelsuay.com"}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": "www.miquelsuay.com; www.clec.fashion"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Desarrollo backend", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Soporte técnico en entornos web", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Administración de sistemas web/hosting", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}]}	B1 de ingles	Sí	No	Nuevo	\N	PADRE JOFRE,7	VALENCIA	46007	Miquel Angel Garcia Gimeno	8	9
41	2025-10-28 09:51:40.601497+00	B40545014	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 2, "disponibles": 2}}	{"COMERCIO INTERNACIONAL": [{"area": "Compras internacionales/ aprovisionamiento", "proyecto": "www.clec.fashion"}, {"area": "Atención a clientes internacionales", "proyecto": "www.miquelsuay.com; www.clec.fashion"}, {"area": "Gestión documental/ almacén", "proyecto": "www.miquelsuay.com"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "www.miquelsuay.com; www.clec.fashion "}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Gestión de eventos", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Atención al cliente y fidelización", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "www.miquelsuay.com"}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": "www.miquelsuay.com; www.clec.fashion"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Desarrollo backend", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Soporte técnico en entornos web", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Administración de sistemas web/hosting", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}]}	B1 de ingles	Sí	No	Nuevo	\N	PADRE JOFRE,7	VALENCIA	46007	Miquel Angel Garcia Gimeno	8	9
35	2025-10-27 12:33:31.372326+00	B46001632	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de tráfico y transporte terrestre; marítimo o aéreo", "proyecto": ""}, {"area": "Administración y documentación de transporte", "proyecto": ""}]}		Sí	Sí	Nuevo	\N	POL.IND PICASSENT CALLE 10 NAVE 8B	PICASSENT	46220	Salomé Rodríguez Estrems	1	5
36	2025-10-27 12:41:55.187461+00	B56966534	{"MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}}	{}		Sí	Sí	Nuevo	\N	C/ Miquel marqués 15 pobla de farnals	La Pobla de Farnals	46139	Óscar Colomina	2	6
37	2025-10-27 12:49:25.302451+00	B98638596	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{}	Sería ideal que tuviese conocimientos avanzados de RRSS y entorno Wordpress/elementor	Sí	No	Nuevo	\N	Calle Nicolas Copernico n8 Despacho 10	Paterna	46980	Carlos Martínez	1	7
42	2025-10-28 10:40:08.098811+00	21003161K	{"MARKETING Y PUBLICIDAD": {"alumnos": 5, "disponibles": 5}, "DESARROLLO APLICACIONES WEB": {"alumnos": 3, "disponibles": 3}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Campañas clientes"}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "Publicaciones RRSS"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "SEO On-page y Off-page"}, {"area": "Atención al cliente y fidelización", "proyecto": "Comunicación con clientes"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "Wordpress CSS"}, {"area": "Desarrollo backend", "proyecto": "Html javascript CSS"}, {"area": "Bases de datos", "proyecto": "Bases de datos internas"}, {"area": "Soporte técnico en entornos web", "proyecto": "Mantenimiento para clientes"}, {"area": "Administración de sistemas web/hosting", "proyecto": "Páginas web clientes"}]}	No es necesario.	Sí	No	Nuevo	\N	AVENIDA CORALINA 22	BETERA	46117	THAIS GARCÍA MAS	8	12
43	2025-10-28 12:31:04.618211+00	B44013613	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de tráfico y transporte terrestre; marítimo o aéreo", "proyecto": "Tareas del puesto"}, {"area": "Gestión de almacén y stock", "proyecto": "Tareas del puesto"}, {"area": "Operaciones logísticas y distribución", "proyecto": "Tareas del puesto"}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": "Tareas del puesto"}, {"area": "Administración y documentación de transporte", "proyecto": "Tareas del puesto"}]}	Recomendable Inglés	Sí	Sí	Nuevo	\N	CALLE VILLA DE MADRID Nº 15	PATERNA	46988	RAMON MATEU ORTIZ	1	13
44	2025-10-28 12:39:56.46468+00	B46445615	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": "-actualización de bases de datos , coordinación con transitarios , gestión pedidos internacionales , preparación y revisión documentación "}, {"area": "Gestión documental/ almacén", "proyecto": "organización y archivo digital expedientes, soporte tareas administrativas, informes"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "- apoyo en la planificación y ejecución de campañas, redacción contenidos redes sociales"}, {"area": "Gestión de eventos", "proyecto": "coordinación logística eventos corporativos, preparación materiales y soporte durante ejecución eventos"}, {"area": "Estudios de mercado e investigación comercial", "proyecto": "posibilidad de colaborar en un estudio de mercado, recogida datos y análisis de datos, apoyo en encuestas, elaboración de presentaciones"}]}	Comercio Internacional ingles nivel avanzado.	Sí	Sí	Nuevo	\N	CARRETERA BENISSANÓ OLOCAU	BENISSANÓ	46181	ISABEL PLUMED	2	14
45	2025-10-28 13:16:58.075144+00	B96939798	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": "Asistencia departamento exportación"}, {"area": "Atención a clientes internacionales", "proyecto": "Asistencia departamento exportación"}, {"area": "Gestión documental/ almacén", "proyecto": "Asistencia departamento exportación"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Asistencia departamento marketing"}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "Asistencia departamento marketing"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "Asistencia departamento marketing"}, {"area": "Gestión de eventos", "proyecto": "Asistencia departamento marketing"}, {"area": "Estudios de mercado e investigación comercial", "proyecto": "Asistencia departamento marketing"}]}	Buenas habilidades de comunicación oral y escrita. \nManejo básico paquete Office.\nAcostumbrado a trabajar en equipo y coordinarse con toda el área de ventas, administración, marketing y producción.\nEspañol nativo o nivel C2. Valorable buen nivel de inglés (B2) o de otros idiomas (alemán, italiano, árabe).	Sí	Sí	Nuevo	\N	C/ Argenters 31, Pol. Ind. El Alter	Alcàsser	46290	Paula Centeno Ortí	2	15
46	2025-10-28 15:35:23.781567+00	B42749481	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "1"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "1"}]}		Sí	Sí	Nuevo	\N	Calle U de Maig 12	Museros	46136	Miquel Tamarit	1	16
47	2025-10-28 16:47:26.880426+00	B42749481	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "1"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "1"}]}		Sí	Sí	Nuevo	\N	Calle U de Maig 12	Museros	46136	Miquel Tamarit	1	16
48	2025-10-29 11:00:21.822015+00	B97881569	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "www.gastroagencia.es"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "www.comunica-2.es"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "www.gastroagencia.es"}]}	Respnsabilidad, actutud y trabajo en equipo.	Sí	No	Nuevo	\N	C/ PUERTO RICO, 48 BAJO DCHA	Valencia	46006	Miguel Rives	2	18
49	2025-10-29 11:57:26.197299+00	B96709134	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "REdes Sociales"}], "DESARROLLO APLICACIONES WEB": [{"area": "Soporte técnico en entornos web", "proyecto": "mantenimiento  y soporte pagina web"}]}	Seria conveniente que el alumnado fuera de poblaciones cercanas o del mismo  Torrent, aunque el centro tiene a 5 minutos la estación Avda. Pais Valenciano  de Torrent. Hoy como sabeis las personas ademas de tener la competencia profesional que corresponden deben saber trabajar en equipo  asi como las soft skills	Sí	No	Nuevo	\N	c/ Tirant Lo Blanc, 26	TORRENT	46900	Victoria  Vazquez Miguel	2	19
51	2025-10-29 14:27:44.372496+00	G96308184	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "Proyecto en Laboratorio de Embalaje"}, {"area": "Operaciones logísticas y distribución", "proyecto": "Proyecto en Laboratorio de Embalaje"}]}	Nota media de expediente mínimo un 7\nProactividad\nTrabajo en equipo\nResolución de problemas\nResistencia a la adversidad	Sí	No	Nuevo	\N	C/ALBERT EINSTEIN 1, PARQUE TECNOLOGICO, 46980, Paterna	Paterna	46980	Amparo Company	1	21
52	2025-10-29 17:30:51.946358+00	B10649580	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Gestión de eventos", "proyecto": ""}]}	Trabajo en equipo, proactividad, creatividad, responsabilidad, tendencias actuales, conocimiento de herramientas como canva, metricool...	Sí	No	Nuevo	\N	Gran Vía Marqués del Turia 54, 8	Valencia	46005	Jorge Turmo Ferro	1	22
53	2025-10-30 12:36:50.243355+00	B13983010	{"DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": ""}, {"area": "Desarrollo backend", "proyecto": ""}, {"area": "Bases de datos", "proyecto": ""}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": ""}, {"area": "Desarrollo software", "proyecto": ""}]}	Buenas tardes, en principio podemos crear una plaza, de uno de los dos ciclos seleccionados. Si pensamos que podemos acoger a dos alumnos os lo comunicaremos pero de momento solo podemos atender a un alumno. Gracias.	Sí	Sí	Nuevo	\N	Ronda Narciso Monturiol 6	Paterna	46980	Jorge Garcia	2	23
54	2025-10-30 17:20:01.372793+00	B96603881	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Atención a clientes internacionales", "proyecto": ""}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Gestión de eventos", "proyecto": ""}, {"area": "Atención al cliente y fidelización", "proyecto": ""}, {"area": "Estudios de mercado e investigación comercial", "proyecto": ""}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de tráfico y transporte terrestre; marítimo o aéreo", "proyecto": ""}, {"area": "Gestión de almacén y stock", "proyecto": ""}, {"area": "Operaciones logísticas y distribución", "proyecto": ""}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": ""}, {"area": "Administración y documentación de transporte", "proyecto": ""}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": ""}, {"area": "Desarrollo software", "proyecto": ""}, {"area": "Soporte técnico y mantenimiento de apps", "proyecto": ""}, {"area": "Integración de sistemas multiplataforma", "proyecto": ""}]}	Trabajo en equipo y proactividad.	Sí	No	Nuevo	\N	Calle Algepser, 16	Paterna	46980	Álvaro García	4	24
55	2025-11-03 06:26:22.393935+00	B46401675	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": "EXPANSION "}]}		Sí	No	Nuevo	\N	AV DE MADRID 6	QUART DE POBLET	46930	SUSANA FRESNEDA	1	25
56	2025-11-03 15:41:25.183142+00	B75633016	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "lagobonoia.com"}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "lagobonoia.com"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "lagobonoia.com"}, {"area": "Atención al cliente y fidelización", "proyecto": "lagobonoia.com"}]}	Se valorará una actitud proactiva, ganas de aprender y capacidad para adaptarse a entornos dinámicos. Buscamos una persona con iniciativa, resolutiva y con interés por aplicar herramientas de inteligencia artificial (IA) en el ámbito del marketing y la automatización de procesos —tanto para generación de imágenes como de contenidos (copywriting)—.\nEl trabajo es semipresencial: algunas jornadas se realizarán de forma presencial en Valencia, con formación directa, y otras desde casa en modalidad remota.	Sí	No	Nuevo	\N	P.º de la Pechina, 15	Valencia	46008	David García Arcos	1	26
57	2025-11-04 09:28:30.401657+00	B98154552	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Estrategia y creación de campañas de matriculación en formación de imagen personal."}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "Community management y creación de contenido orgánico en nuestra redes sociales (Facebook, Instagram y Tik Tok)"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "Creación de cursos online y optimización SEO de nuestras tiendas online"}]}	Se valorará:\nSoft skills: proactividad, trabajo en equipo, soluciones creativas.\nNo es indispensable pero ayuda: Wordpress, Meta suite, Canva, Edición de vídeo, Adobe Creative Suite.	Sí	No	Nuevo	\N	C/ Guillem de Castro, 43	Valencia	46007	Víctor García Sanjuan	1	27
58	2025-11-10 11:10:15.632358+00	B98763360	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Planificación estratégica, asesoramiento, coordinación y seguimiento de acciones para alcanzar los objetivos de negocio."}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "Gestión de la estrategia de comunicación en Redes Sociales"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "Proyecto  de implementación de acciones técnicas y de contenido para optimizar el posicionamiento orgánico y aumentar la visibilidad web. "}]}	Capacidad de trabajo en equipo y valorable inglés B1 (no obligatorio).	Sí	No	Nuevo	\N	Andarella 1, bloque 2, planta 1, puerta 3	Valencia	46950	CLAUDIA COSSU	1	28
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
-- Data for Name: tutores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."tutores" ("id", "created_at", "nombre", "nif", "email", "telefono", "cif_empresa", "oferta") FROM stdin;
5	2025-10-27 12:33:31.069207+00	RAFAEL LLUESMA GIL	20004251R	rafa@vialcobus.com	961230673	B46001632	\N
6	2025-10-27 12:41:54.957255+00	Óscar Colomina Fernández	23324155Q	info@plan-moves.com	627024604	B56966534	\N
7	2025-10-27 12:49:25.055724+00	Eva García Zahino	48305516L	eva.garcia@cwcomunicacion.com	652899878	B98638596	\N
9	2025-10-28 09:51:35.272408+00	Miquel A. Garcia Gimeno	20.427.169H	miquel@miquelsuay.com	+34687452966	B40545014	\N
12	2025-10-28 10:40:07.873684+00	THAIS GARCIA MAS	21003161K	thaysgarciamas@gmail.com	644256002	21003161K	\N
13	2025-10-28 12:31:04.358797+00	DANIEL MASIA FENOLLAR	20814310T	dmasia@istobal.com	627644858	B44013613	\N
14	2025-10-28 12:39:55.855738+00	Alfonso Sanz Cambra	24397015H	rrhh@gruposanz.es	962791441	B46445615	\N
15	2025-10-28 13:16:57.810976+00	Ana María Llácer Ortí	20861701B	design@ogofurniture.com	655196378	B96939798	\N
16	2025-10-28 15:35:23.539047+00	Miquel Tamarit	29209987X	info@tamaritestudio.com	634869965	B42749481	\N
18	2025-10-29 11:00:21.589725+00	Andrea Torres	44500241W	andrea@gastroagencia.es	606771193	B97881569	\N
19	2025-10-29 11:57:25.899075+00	Victoria Vazquez Miguel	53606749M	victoriav@betaformacion.com	687724161	B96709134	\N
21	2025-10-29 14:27:44.101556+00	Amparo Company Sanchez	53205658B	amparo.company@itene.com	672387733	G96308184	\N
22	2025-10-29 17:30:51.698229+00	Jorge Turmo Ferro	18064892W	jturmocosmic@gmail.com	682457661	B10649580	\N
23	2025-10-30 12:36:49.966591+00	Jose Miguel Platero Aznar	73661414G	jose.platero@anphis.es	660002146	B13983010	\N
24	2025-10-30 17:20:01.10733+00	Álvaro García Pardo	29207927C	alvaro.garcia@fmgrupotec.com	630114066	B96603881	\N
25	2025-11-03 06:26:22.105386+00	MARIA ANGELES LEON COCERA	33405902N	mleon@emac.es	961532200	B46401675	\N
26	2025-11-03 15:41:24.87944+00	David García Arcos	50868300M	david@lagobonoia.com	685975118	B75633016	\N
27	2025-11-04 09:28:30.132533+00	Víctor García Sanjuan	448697171Y	victorgarcia@anasalmeron.es	680476576	B98154552	\N
28	2025-11-10 11:10:15.364027+00	CHRISTIAN ESPERÓN ROSALES	44887082Y	chistian.esperon@connext.es	+34 605334487	B98763360	\N
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."usuarios" ("id", "created_at", "email", "password") FROM stdin;
1	2025-09-24 13:08:28.062791+00	admin	admin
2	2025-10-20 10:02:26.5861+00	avicente@campuscamarafp.com	avicente123!
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

SELECT pg_catalog.setval('"public"."alumno_estados_id_seq"', 138, true);


--
-- Name: alumnos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."alumnos_id_seq"', 156, true);


--
-- Name: contacto_alumnos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."contacto_alumnos_id_seq"', 5, true);


--
-- Name: contacto_empresas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."contacto_empresas_id_seq"', 13, true);


--
-- Name: empresa_estados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."empresa_estados_id_seq"', 109, true);


--
-- Name: empresa_practica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."empresa_practica_id_seq"', 58, true);


--
-- Name: empresas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."empresas_id_seq"', 71, true);


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

SELECT pg_catalog.setval('"public"."practica_estados_id_seq"', 8, true);


--
-- Name: practicas_fp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."practicas_fp_id_seq"', 58, true);


--
-- Name: tutores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."tutores_id_seq"', 28, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."usuarios_id_seq"', 2, true);


--
-- PostgreSQL database dump complete
--

-- \unrestrict FR9Yo5jrcOaHzzTI7NoojvQ9QfGVbK5dkNaFtmfpO4DgYoI05m4pcCJSk3SkunI

RESET ALL;
