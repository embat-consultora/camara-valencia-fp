SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict IJuSkiCM8gvi6byRYbbknXJx0mZ5TtHIQlXaiDEdy97kBdJsyqQmGnzrSFe9lva

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
-- Data for Name: custom_oauth_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."custom_oauth_providers" ("id", "provider_type", "identifier", "name", "client_id", "client_secret", "acceptable_client_ids", "scopes", "pkce_enabled", "attribute_mapping", "authorization_params", "enabled", "email_optional", "issuer", "discovery_url", "skip_nonce_check", "cached_discovery", "discovery_cached_at", "authorization_url", "token_url", "userinfo_url", "jwks_uri", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."flow_state" ("id", "user_id", "auth_code", "code_challenge_method", "code_challenge", "provider_type", "provider_access_token", "provider_refresh_token", "created_at", "updated_at", "authentication_method", "auth_code_issued_at", "invite_token", "referrer", "oauth_client_state_id", "linking_target_id", "email_optional") FROM stdin;
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

COPY "auth"."oauth_clients" ("id", "client_secret_hash", "registration_type", "redirect_uris", "grant_types", "client_name", "client_uri", "logo_uri", "created_at", "updated_at", "deleted_at", "client_type", "token_endpoint_auth_method") FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sessions" ("id", "user_id", "created_at", "updated_at", "factor_id", "aal", "not_after", "refreshed_at", "user_agent", "ip", "tag", "oauth_client_id", "refresh_token_hmac_key", "refresh_token_counter", "scopes") FROM stdin;
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

COPY "auth"."oauth_authorizations" ("id", "authorization_id", "client_id", "user_id", "redirect_uri", "scope", "state", "resource", "code_challenge", "code_challenge_method", "response_type", "status", "authorization_code", "created_at", "expires_at", "approved_at", "nonce") FROM stdin;
\.


--
-- Data for Name: oauth_client_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."oauth_client_states" ("id", "provider_type", "code_verifier", "created_at") FROM stdin;
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
-- Data for Name: webauthn_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."webauthn_challenges" ("id", "user_id", "challenge_type", "session_data", "created_at", "expires_at") FROM stdin;
\.


--
-- Data for Name: webauthn_credentials; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."webauthn_credentials" ("id", "user_id", "credential_id", "public_key", "attestation_type", "aaguid", "sign_count", "transports", "backup_eligible", "backed_up", "friendly_name", "created_at", "updated_at", "last_used_at") FROM stdin;
\.


--
-- Data for Name: alumnos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."alumnos" ("id", "created_at", "NIA", "nombre", "apellido", "telefono", "provincia", "localidad", "codigo_postal", "direccion", "email_alumno", "sexo", "preferencias_fp", "vehiculo", "ciclo_formativo", "estado", "motivo", "dni", "requisitos", "tipoPractica", "gestor", "tutor_centro", "horas_totales", "comentarios_centro", "observaciones_seguimiento", "anio", "nuss", "curso") FROM stdin;
150	2025-11-04 11:34:39.126115+00	\N	Maite	Castro Giménez	\N	\N	ALFAFAR	46910	Plaza Poeta Miguel Hernández, 10	mcastro@campuscamarafp.com	F	["Desarrollo aplicaciones móviles", "Soporte técnico y mantenimiento de apps", "Integración de sistemas multiplataforma"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	44887995E	\N	Autogestionada	\N	\N	\N	\N	\N	\N	\N	\N
139	2025-11-03 12:52:58.45846+00	\N	Marina	Baldovi Santiago	\N	\N	GODELLA	46110	Calle Montgó 2D	marinabalw@gmail.com	\N	["Publicidad y Comunicación (redes sociales)"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	23873689B	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
217	2026-04-27 08:05:13.337584+00	\N	Antonela	Pisciolari	634035779	\N	ALFARA DEL PATRIARCA	03130	Av. Escandinavia 72	antopiscio@gmail.com	Femenino	["Desarrollo fronted", "Soporte técnico en entornos web", "Administración de sistemas web/hosting"]	Sí	"DESARROLLO APLICACIONES WEB"	Asignado	\N	Z1066124X	\N	Asignada por el centro	Ester Piscore	\N	25	comentas	observaciones anto	2026-2027	10441234	1ro
148	2025-11-04 08:48:33.309139+00	\N	Nicolás	Beneito Colomina	\N	\N	VALENCIA	46021	Calle Leandro de Saralegui, 11	nicolas.beneito.work@gmail.com	\N	["Departamento de Marketing (estrategia/campañas)"]	No	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	21808446F	\N	Autogestionada	\N	\N	\N	\N	\N	\N	\N	\N
147	2025-11-04 07:30:43.507368+00	\N	Emilio	Cócera Beltrán	\N	\N	VALENCIA	46009	C/ Pobla del duc 11, 4	cocerae@gmail.com	\N	["Desarrollo fronted", "Bases de datos", "Desarrollo backend"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	33565150P	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
153	2025-11-06 18:06:30.809871+00	\N	Fidel	Lauroba Heinz-Senss	\N	\N	POBLA DE VALLBONA	46185	Calle Nº 28	fidellauheinz@gmail.com	\N	["Desarrollo software", "Desarrollo aplicaciones móviles", "Bases de datos y gestión de información"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	45904659V	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
154	2025-11-07 11:05:21.893375+00	\N	Emma	Gómez Bayarri	\N	\N	ALMÀSSERA	46132	Calle San Vicente Ferrer, 22	emmagb267@gmail.com	\N	["Gestión de eventos", "Publicidad y Comunicación (redes sociales)", "Marketing digital (SEO/SEM)"]	No	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	24449884X	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
155	2025-11-11 09:32:54.882287+00	\N	Angel	Sospedra Martinez	\N	\N	TORRENT	46901	Almirante Churruca 20	asospedra@campuscamarafp.com	\N	["Desarrollo fronted"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	5388103T	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
160	2025-11-13 11:10:19.278032+00	\N	Javier	Aljaro Martinez	\N	\N	PATERNA	46980	Santisimo Cristo de la Fe	jaljaro@campuscamarafp.com	\N	["Desarrollo fronted", "Soporte técnico en entornos web", "Administración de sistemas web/hosting"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	4502514B	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
163	2025-11-15 19:42:50.64776+00	\N	Salvador	Bosch Aguilar	\N	\N	GODELLA	46110	Ctra Rocafort 32	sbosch@campuscamarafp.com	\N	["Desarrollo fronted"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	50329039W	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
165	2025-11-16 12:26:40.322164+00	\N	Mauricio	Redolfi Flores	\N	\N	ALGIMIA DE ALFARA	46148	Poligon 4, Parcela 405	mauricioredolfi@gmail.com	\N	["Atención al cliente y fidelización", "Publicidad y Comunicación (redes sociales)", "Marketing digital (SEO/SEM)"]	No	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	Z2292092D	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
149	2025-11-04 10:00:11.231237+00	\N	Mariana	Cebrián Meyuy	\N	\N	VALENCIA	46003	C/ NA JORDANA,32, 6	maruum04@gmail.com	\N	["Gestión de tráfico y transporte terrestre; marítimo o aéreo", "Gestión de almacén y stock", "Operaciones logísticas y distribución"]	Sí	"TRANSPORTE Y LOGÍSTICA"	Sin Empresa	\N	44530355D	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
143	2025-11-03 12:59:56.60404+00	\N	Carlos	Carbonell Álvarez	\N	\N	LLIRIA	46160	C/Molí del Bailón 2, 7	carloscarbonellalvarez@gmail.com	\N	["Desarrollo aplicaciones móviles", "Soporte técnico y mantenimiento de apps", "Desarrollo software"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	03162491Z	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
142	2025-11-03 12:58:19.150382+00	\N	Rafa	Artesero Bueno	\N	\N	L'ELIANA	46183	AV ALCALDE ENRIQUE DARIES 12	rafters2004@gmail.com	\N	["Gestión documental/ almacén", "Departamento Comercio Ext/aduanas", "Departamento Export/import"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	23937154L	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
151	2025-11-06 14:22:45.239449+00	\N	Andrea	González Arenas	\N	\N	VALENCIA	46019	Calle Arquitecto Tolsá, 21	andreagonzalezarenas06@gmail.com	\N	["Publicidad y Comunicación (redes sociales)", "Marketing digital (SEO/SEM)", "Gestión de eventos"]	No	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	44923690K	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
158	2025-11-13 11:10:07.438391+00	\N	Enol	Puente Izquierdo	\N	\N	VALENCIA	46019	Avenida Alfahuir 41	epuente@campuscamarafp.com	\N	["Desarrollo fronted", "Soporte técnico en entornos web", "Administración de sistemas web/hosting"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	21792996J	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
146	2025-11-03 20:31:57.243818+00	\N	Carlos	Fernandez	\N	\N	VALENCIA	46023	calle Trafalgar, 52	carlosfer663@gmail.com	\N	["Desarrollo aplicaciones móviles", "Soporte técnico y mantenimiento de apps", "Integración de sistemas multiplataforma"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	53881536B	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
156	2025-11-11 09:40:26.735794+00	\N	Alejandro	Gámez Sánchez	\N	\N	VALENCIA	46182	Carrer 529,9	agamez@campuscamarafp.com	\N	["Desarrollo backend", "Desarrollo fronted"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	76641673S	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
166	2025-11-16 15:55:59.397465+00	\N	Iker	Cuadra Miranda	\N	\N	FOIOS	26134	Calle Ausias March 15, 1-2	ikercuadramiranda@gmail.com	\N	["Desarrollo fronted", "Administración de sistemas web/hosting", "Soporte técnico en entornos web"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	25741634B	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
169	2025-11-17 17:16:30.854658+00	\N	Adrian	Lamberto Del Canto	\N	\N	DOMEÑO	46174	Avenida Polideportivo, 8	alamberto@campuscamarafp.com	\N	["Desarrollo software", "Integración de sistemas multiplataforma", "Bases de datos y gestión de información"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	48713962P	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
170	2025-11-17 18:00:54.712996+00	\N	Alejandro	Pallas Celda	\N	\N	VALENCIA	46007	c/Carcagente, 6, escalera A, piso 7, puerta 24	alexpallizz6@gmail.com	\N	["Desarrollo software", "Desarrollo aplicaciones móviles", "Integración de sistemas multiplataforma"]	No	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	23321333T	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
161	2025-11-14 14:54:16.138611+00	\N	Iván	Sorolla	\N	\N	VALENCIA	46025	Calle Río Nervión, 23	icontador161005@gmail.com	\N	["Desarrollo software", "Desarrollo aplicaciones móviles", "Integración de sistemas multiplataforma"]	No	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	24442592D	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
194	2025-11-22 08:00:35.913002+00	\N	Elena	Bou Ibañez	\N	\N	BURJASSOT	46100	C/Ademuz, 2	ebouibanez@gmail.com	\N	["Departamento de Marketing (estrategia/campañas)", "Publicidad y Comunicación (redes sociales)", "Gestión de eventos"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	50508514P	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
176	2025-11-20 11:50:44.719641+00	\N	Cristina	Estrela Gombau	\N	\N	BURJASSOT	46100	C/Colón 65	estrela.cristina11@gmail.com	\N	["Administración y documentación de transporte", "Operaciones logísticas y distribución", "Gestión de almacén y stock"]	Sí	"TRANSPORTE Y LOGÍSTICA"	Sin Empresa	\N	44943188S	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
157	2025-11-13 07:03:35.978926+00	\N	Sofía	Ballester Torrego	\N	\N	VALENCIA	46017	Av Gaspar Aguilar 84	sballester@campuscamarafp.com	\N	["Desarrollo fronted"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	44895178Y	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
140	2025-11-03 12:55:30.908007+00	\N	Paula	Veses Navarro	\N	\N	LLIRIA	46160	c/Marc Cornelli Nigri	paulavesesnavarro@gmail.com	\N	["Gestión de eventos", "Publicidad y Comunicación (redes sociales)"]	Sí	"MARKETING Y PUBLICIDAD"	Asignado	\N	73666906E	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
198	2025-11-22 10:25:26.581683+00	\N	Candela	Torrejón Almenar	\N	\N	L'ELIANA	46183	C/ Pilar Mateo Herrero 1-46	candelatoal1@gmail.com	\N	["Integración de sistemas multiplataforma", "Bases de datos y gestión de información", "Desarrollo software"]	No	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	23317387X	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
141	2025-11-03 12:55:47.704964+00	\N	Alvaro	Martínez Perez	\N	\N	TORRENT	46900	Calle Lope de Rueda, 9	alvaromartinezperez2006@gmail.com	\N	["Publicidad y Comunicación (redes sociales)", "Gestión de eventos", "Departamento de Marketing (estrategia/campañas)"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	53885085H	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
144	2025-11-03 17:27:59.94601+00	\N	Luis	López Martinez	\N	\N	GODELLA	46110	Ermita nova 26	llopez@campuscamarafp.com	\N	["Bases de datos y gestión de información"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	49180951M	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
145	2025-11-03 18:28:02.468006+00	\N	Mónica	Blanco Merino	\N	\N	SANTANDER	39006	paseo de altamira ,130. 3º IZDA	moblancomerino153@gmail.com	\N	["Desarrollo software", "Desarrollo aplicaciones móviles", "Integración de sistemas multiplataforma"]	No	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	72183688M	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
201	2025-12-04 17:35:47.522652+00	\N	Germán	Marín Martorell	\N	\N	POLINYÀ DEL XÚQUER	46688	Av. Alzira 32	germanmarin2724@gmail.com	\N	["Departamento Comercio Ext/aduanas", "Compras internacionales/ aprovisionamiento", "Departamento Export/import"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	73604932X	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
202	2025-12-04 17:57:19.819777+00	\N	Vera	Matilla González	\N	\N	BUÑOL	46360	C/ Jesús Sáez Ramírez n7 p9	veramatillag@gmail.com	\N	["Departamento Export/import", "Compras internacionales/ aprovisionamiento", "Departamento Comercio Ext/aduanas"]	No	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	21804870L	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
204	2025-12-04 19:12:40.944186+00	\N	Germán	Rodrigo Cortés	\N	\N	CHESTE	46380	C/ Puerta Zafa, 2	gerrodcort@gmail.com	\N	["Departamento Export/import", "Departamento Comercio Ext/aduanas", "Compras internacionales/ aprovisionamiento"]	No	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	21803069N	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
179	2025-11-21 08:57:49.828216+00	\N	Lucia	Brotons Martín	\N	\N	QUESA	46824	Altico de la rocha	lbrotons@campuscamarafp.com	\N	["Departamento de Marketing (estrategia/campañas)", "Publicidad y Comunicación (redes sociales)", "Gestión de eventos"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	54424379P	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
181	2025-11-21 10:39:55.652668+00	\N	Héctor	GIl Borreguero	\N	\N	BÉTERA	46117	Calle isabel de Villena 1	hectorgilalfabegues@gmail.com	\N	["Gestión de tráfico y transporte terrestre; marítimo o aéreo", "Operaciones logísticas y distribución", "Administración y documentación de transporte"]	Sí	"TRANSPORTE Y LOGÍSTICA"	Sin Empresa	\N	73670597X	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
185	2025-11-21 11:44:11.96598+00	\N	Yeli	Rusakova	\N	\N	PATERNA	46980	Avd.Primer de Maig 65	lizakets1@gmail.com	\N	["Publicidad y Comunicación (redes sociales)", "Gestión de eventos", "Departamento de Marketing (estrategia/campañas)"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	Y4173555N	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
172	2025-11-18 09:21:40.378707+00	\N	ELENA	FERRANDO NAVARRO	\N	\N	VALENCIA	46119	CALLE REVERENDO CELESTINO NAVARRO BLESA,25	eferrandonavarro@gmail.com	\N	["Departamento de Marketing (estrategia/campañas)"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	49846350Z	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
193	2025-11-21 21:57:52.343368+00	\N	ROCIO	MEDRANO	\N	\N	VALENCIA	46025	Calle jose Grolllo 33	rociomedrano046@gmail.com	\N	["Publicidad y Comunicación (redes sociales)", "Gestión de eventos", "Departamento de Marketing (estrategia/campañas)"]	No	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	44929956P	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
192	2025-11-21 14:10:20.482975+00	\N	Jordán	Saiz Honteciñlas	\N	\N	SAN ANTONIO DE BENAGÉBER	46184	Carrer Pinsà 18 San Antonio	jsaiz@campuscamarafp.com	\N	["Departamento de Marketing (estrategia/campañas)", "Gestión de eventos"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	48408875Q	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
182	2025-11-21 10:40:19.653629+00	\N	Antonio	Gil Sales	\N	\N	VINAROZ	12500	AV. Francisco Jose Balada calle Nº45 nº11	tonetgil123@gmail.com	\N	["Gestión de tráfico y transporte terrestre; marítimo o aéreo", "Operaciones logísticas y distribución", "Administración y documentación de transporte"]	Sí	"TRANSPORTE Y LOGÍSTICA"	Sin Empresa	\N	20613233N	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
175	2025-11-20 08:21:44.497984+00	\N	Juan Jose	Barba Saiz	\N	\N	VALENCIA	46015	Calle Gongora	juanjoobarba@gmail.com	\N	["Desarrollo aplicaciones móviles", "Desarrollo software", "Soporte técnico y mantenimiento de apps"]	No	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	44946317Q	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
190	2025-11-21 12:46:58.887009+00	\N	Lucia	Gonzalez Iglesias	\N	\N	VALENCIA	46018	Av del Cid 58	luciagonzalezigle.22@gmail.com	\N	["Gestión de almacén y stock", "Administración y documentación de transporte", "Gestión de tráfico y transporte terrestre; marítimo o aéreo"]	No	"TRANSPORTE Y LOGÍSTICA"	Sin Empresa	\N	21803170K	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
174	2025-11-20 08:05:07.62074+00	\N	Rodrigo	Alapont Seara	\N	\N	TORRENT	46901	Carrer del Pintor Ramon Cabrelles Nº18	rodrigoalap@gmail.com	\N	["Desarrollo fronted", "Desarrollo backend", "Bases de datos"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	54293447S	\N	Autogestionada	\N	\N	\N	\N	\N	\N	\N	\N
159	2025-11-13 11:10:07.761792+00	\N	Paula	Solaz Pérez	\N	\N	VALENCIA	46011	Calle San Rafael, 4	psolaz@campuscamarafp.com	\N	["Desarrollo fronted", "Soporte técnico en entornos web", "Administración de sistemas web/hosting"]	Sí	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	26885866Q	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
183	2025-11-21 10:43:29.721276+00	\N	Marc	Capsir	\N	\N	BENIPARRELL	46469	calle albufera	marccapsir@gmail.com	\N	["Operaciones logísticas y distribución", "Gestión de almacén y stock", "Gestión de tráfico y transporte terrestre; marítimo o aéreo"]	Sí	"TRANSPORTE Y LOGÍSTICA"	Sin Empresa	\N	21790355V	\N	Autogestionada	\N	\N	\N	\N	\N	\N	\N	\N
213	2025-12-05 08:46:51.069586+00	\N	Alba	Roig Saiz	\N	\N	VALENCIA	46182	calle 231 número 2 puerta 10	albaa.roigg@gmail.com	\N	["Atención a clientes internacionales"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	54292237R	\N	Autogestionada	\N	\N	\N	\N	\N	\N	\N	\N
178	2025-11-20 18:06:55.63278+00	\N	Marcos	Tomás Campos	\N	\N	SAN ANTONIO DE BENAGÉBER	46184	Calle Serpis 156	marcostomascampos@gmail.com	\N	["Soporte técnico en entornos web", "Desarrollo fronted", "Administración de sistemas web/hosting"]	No	"DESARROLLO APLICACIONES WEB"	Sin Empresa	\N	45904965R	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
168	2025-11-17 17:02:00.258434+00	\N	Eduardo	Ruiz Ferrer	\N	\N	VALENCIA	46185	Calle Villasol 1	edurf227@gmail.com	\N	["Departamento de Marketing (estrategia/campañas)", "Publicidad y Comunicación (redes sociales)", "Gestión de eventos"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	24507596S	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
167	2025-11-17 16:37:24.698383+00	\N	Irene	Rodríguez Hernández	\N	\N	VALENCIA	46023	Calle Trafalgar 38, p20	irenerh25@gmail.com	\N	["Departamento de Marketing (estrategia/campañas)", "Gestión de eventos", "Estudios de mercado e investigación comercial"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	29221668F	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
206	2025-12-04 22:57:16.78946+00	\N	Alfredo	Ferrando Alcover	\N	\N	LA POBLA DE VALLBONA	46185	Valdelinares 9	alfredoferrandoalcover@gmail.com	\N	["Compras internacionales/ aprovisionamiento", "Departamento Comercio Ext/aduanas", "Departamento Export/import"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	23855902A	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
214	2025-12-05 11:50:23.5441+00	\N	Andrés	Contreras Camacho	\N	\N	BURJASSOT	46100	Calle Miquel Bordanau, 1	eduardo412ca@icloud.com	\N	["Desarrollo software", "Desarrollo aplicaciones móviles", "Bases de datos y gestión de información"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	Z0632158P	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
215	2025-12-05 14:51:14.694548+00	\N	Gabriela Alejandra	Merlini Rivera	\N	\N	BURJASSOT	46100	calle Santiago García 23	gabrielamerlini.17@gmail.com	\N	["Departamento Comercio Ext/aduanas", "Departamento Export/import", "Atención a clientes internacionales"]	No	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	Z2020699Q	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
209	2025-12-05 08:16:05.130598+00	\N	ESTHER	MUÑOZ ASENSIO	\N	\N	PATERNA	46980	C/MIGUEL HERNÁNDEZ 30. PTA 5	eestheer17@gmail.com	\N	["Departamento Export/import", "Departamento Comercio Ext/aduanas"]	No	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	45904376X	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
205	2025-12-04 20:12:29.296025+00	\N	Diana	Collado Segura	\N	\N	LA POBLA DE VALLBONA	46185	C/ Rio Júcar N6	dianacolladosegura@gmail.com	\N	["Departamento Export/import"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	50596419F	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
207	2025-12-05 06:50:50.852989+00	\N	Estrella del Alba	Garcia Guerola	\N	\N	PATERNA	46980	Calle Benasal 2, Puerta 29	estrelladelalba@icloud.com	\N	["Atención a clientes internacionales", "Compras internacionales/ aprovisionamiento", "Departamento Export/import"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	73226957V	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
197	2025-11-22 08:09:01.935621+00	\N	Chenoa	Chen	\N	\N	BÉTERA	46117	Mas camarena sector E n 12	chenoachen2002@gmail.com	\N	["Publicidad y Comunicación (redes sociales)", "Departamento de Marketing (estrategia/campañas)", "Gestión de eventos"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	X6719502Y	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
186	2025-11-21 11:47:15.060142+00	\N	Pablo Luis	Ruiz Alcón	\N	\N	L'ELIANA	46183	CALLE MOGENTE, 11	pablorual@hotmail.com	\N	["Departamento de Marketing (estrategia/campañas)", "Gestión de eventos", "Marketing digital (SEO/SEM)"]	Sí	"MARKETING Y PUBLICIDAD"	Sin Empresa	\N	49846806X	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
216	2025-12-05 14:57:19.526241+00	\N	Carmen	Gascó García	\N	\N	VALENCIA	46019	Carrer de Cambrils, 10	carmengascogar@gmail.com	\N	["Departamento Export/import", "Compras internacionales/ aprovisionamiento", "Departamento Comercio Ext/aduanas"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	03159051R	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
200	2025-12-04 07:57:08.160614+00	\N	Jaime	Gómez-Trénor	\N	\N	VALENCIA	46010	C/ de Cavanilles, 30, El Pla del Real, 46010 València, Valencia	jgomeztrenor632@gmail.com	\N	["Soporte técnico y mantenimiento de apps", "Desarrollo aplicaciones móviles", "Bases de datos y gestión de información"]	Sí	"DESARROLLO APLICACIONES MULTIPLATAFORMA"	Sin Empresa	\N	54290783L	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
203	2025-12-04 18:35:48.333176+00	\N	Alejandro	Rodrigues Avendaño	\N	\N	VALENCIA	46015	Calle Amador Martínez Rochína 2	jrodrigues@campuscamarafp.com	\N	["Atención a clientes internacionales", "Compras internacionales/ aprovisionamiento", "Departamento Comercio Ext/aduanas"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	Y3974502R	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
208	2025-12-05 07:26:02.180845+00	\N	Alexander	Tvile-Larsen	\N	\N	L'ELIANA	46183	Calle Conquista 6a	alexandertvile@gmail.com	\N	["Compras internacionales/ aprovisionamiento", "Departamento Export/import"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	X9816437Z	\N	Asignada por el Centro	\N	\N	\N	\N	\N	\N	\N	\N
231	2026-05-04 13:37:43.333507+00	\N	SOFIA	AGUIRRE	nan	\N	ADEMUZ	46950	molino	info@data-so.com	Femenino	["Departamento Comercio Ext/aduanas", "Atención a clientes internacionales", "Gestión documental/ almacén"]	Sí	"COMERCIO INTERNACIONAL"	Sin Empresa	\N	32594542	Ingles y portugues	Asignada por el centro	\N	\N	\N	\N	\N	2026-2027	hgjhgjhg	1ro
\.


--
-- Data for Name: alumno_estados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."alumno_estados" ("id", "created_at", "email_enviado", "match_fp", "fp_enprogreso", "fp_finalizada", "alumno", "form_completo", "documentacion_completa", "evaluacion_enviada", "evaluacion_completa", "fp_asignada", "fp_cancelada") FROM stdin;
116	2025-11-03 12:52:58.777112+00	2025-11-03	\N	\N	\N	23873689B	2025-11-03	\N	\N	\N	\N	\N
118	2025-11-03 12:55:47.976183+00	2025-11-03	\N	\N	\N	53885085H	2025-11-03	\N	\N	\N	\N	\N
120	2025-11-03 12:59:56.89658+00	2025-11-03	\N	\N	\N	03162491Z	2025-11-03	\N	\N	\N	\N	\N
127	2025-11-03 18:28:02.878194+00	\N	\N	\N	\N	72183688M	2025-11-03	\N	\N	\N	\N	\N
128	2025-11-03 20:31:57.607814+00	\N	\N	\N	\N	53881536B	2025-11-03	\N	\N	\N	\N	\N
129	2025-11-04 07:30:43.925475+00	\N	\N	\N	\N	33565150P	2025-11-04	\N	\N	\N	\N	\N
130	2025-11-04 08:48:33.756596+00	\N	\N	\N	\N	21808446F	2025-11-04	\N	\N	\N	\N	\N
131	2025-11-04 10:00:11.609951+00	\N	\N	\N	\N	44530355D	2025-11-04	\N	\N	\N	\N	\N
132	2025-11-04 11:34:39.506846+00	\N	\N	\N	\N	44887995E	2025-11-04	\N	\N	\N	\N	\N
139	2025-11-13 07:03:36.310523+00	\N	2025-11-28	\N	\N	44895178Y	2025-11-13	\N	\N	\N	2025-11-28	\N
417	2025-12-04 07:57:08.414312+00	\N	\N	\N	\N	54290783L	2025-12-04	\N	\N	\N	\N	\N
418	2025-12-04 17:35:47.921384+00	\N	\N	\N	\N	73604932X	2025-12-04	\N	\N	\N	\N	\N
133	2025-11-06 14:22:45.712851+00	\N	\N	\N	\N	44923690K	2025-11-06	\N	\N	\N	\N	\N
135	2025-11-06 18:06:31.197585+00	\N	\N	\N	\N	45904659V	2025-11-06	\N	\N	\N	\N	\N
136	2025-11-07 11:05:22.334276+00	\N	\N	\N	\N	24449884X	2025-11-07	\N	\N	\N	\N	\N
137	2025-11-11 09:32:55.301008+00	\N	\N	\N	\N	5388103T	2025-11-11	\N	\N	\N	\N	\N
419	2025-12-04 17:57:20.197983+00	\N	\N	\N	\N	21804870L	2025-12-04	\N	\N	\N	\N	\N
138	2025-11-11 09:40:27.102178+00	\N	\N	\N	\N	76641673S	2025-11-11	\N	\N	\N	\N	\N
420	2025-12-04 18:35:48.674251+00	\N	\N	\N	\N	Y3974502R	2025-12-04	\N	\N	\N	\N	\N
126	2025-11-03 17:28:00.796911+00	2025-11-13	\N	\N	\N	49180951M	2025-11-03	\N	\N	\N	\N	\N
141	2025-11-13 11:10:07.976648+00	\N	\N	\N	\N	26885866Q	2025-11-13	\N	\N	\N	\N	\N
421	2025-12-04 19:12:41.289672+00	\N	\N	\N	\N	21803069N	2025-12-04	\N	\N	\N	\N	\N
142	2025-11-13 11:10:08.084644+00	\N	\N	\N	\N	21792996J	2025-11-13	\N	\N	\N	\N	\N
143	2025-11-13 11:10:19.552966+00	\N	\N	\N	\N	4502514B	2025-11-13	\N	\N	\N	\N	\N
422	2025-12-04 20:12:29.661157+00	\N	\N	\N	\N	50596419F	2025-12-04	\N	\N	\N	\N	\N
146	2025-11-15 19:42:51.122084+00	\N	\N	\N	\N	50329039W	2025-11-15	\N	\N	\N	\N	\N
148	2025-11-16 12:26:40.796751+00	\N	\N	\N	\N	Z2292092D	2025-11-16	\N	\N	\N	\N	\N
149	2025-11-16 15:55:59.818496+00	\N	\N	\N	\N	25741634B	2025-11-16	\N	\N	\N	\N	\N
150	2025-11-17 16:37:25.181775+00	\N	\N	\N	\N	29221668F	2025-11-17	\N	\N	\N	\N	\N
151	2025-11-17 17:02:00.668485+00	\N	\N	\N	\N	24507596S	2025-11-17	\N	\N	\N	\N	\N
152	2025-11-17 17:16:31.226755+00	\N	\N	\N	\N	48713962P	2025-11-17	\N	\N	\N	\N	\N
153	2025-11-17 18:00:55.088605+00	\N	\N	\N	\N	23321333T	2025-11-17	\N	\N	\N	\N	\N
144	2025-11-14 14:54:16.52195+00	\N	\N	\N	\N	24442592D	2025-11-17	\N	\N	\N	\N	\N
155	2025-11-18 09:21:40.740354+00	\N	\N	\N	\N	49846350Z	2025-11-18	\N	\N	\N	\N	\N
157	2025-11-20 08:05:08.083185+00	\N	\N	\N	\N	54293447S	2025-11-20	\N	\N	\N	\N	\N
158	2025-11-20 08:21:44.801529+00	\N	\N	\N	\N	44946317Q	2025-11-20	\N	\N	\N	\N	\N
159	2025-11-20 11:50:45.116336+00	\N	\N	\N	\N	44943188S	2025-11-20	\N	\N	\N	\N	\N
161	2025-11-20 18:06:56.040068+00	\N	\N	\N	\N	45904965R	2025-11-20	\N	\N	\N	\N	\N
162	2025-11-21 08:57:50.197477+00	\N	\N	\N	\N	54424379P	2025-11-21	\N	\N	\N	\N	\N
165	2025-11-21 10:40:19.907829+00	\N	\N	\N	\N	20613233N	2025-11-21	\N	\N	\N	\N	\N
166	2025-11-21 10:43:30.032467+00	\N	\N	\N	\N	21790355V	2025-11-21	\N	\N	\N	\N	\N
164	2025-11-21 10:39:56.057614+00	\N	\N	\N	\N	73670597X	2025-11-21	\N	\N	\N	\N	\N
168	2025-11-21 11:44:12.508428+00	\N	\N	\N	\N	Y4173555N	2025-11-21	\N	\N	\N	\N	\N
169	2025-11-21 11:47:15.295763+00	\N	\N	\N	\N	49846806X	2025-11-21	\N	\N	\N	\N	\N
423	2025-12-04 22:57:17.181583+00	\N	\N	\N	\N	23855902A	2025-12-04	\N	\N	\N	\N	\N
173	2025-11-21 12:46:59.255332+00	\N	\N	\N	\N	21803170K	2025-11-21	\N	\N	\N	\N	\N
175	2025-11-21 14:10:20.864802+00	\N	\N	\N	\N	48408875Q	2025-11-21	\N	\N	\N	\N	\N
176	2025-11-21 21:57:52.772242+00	\N	\N	\N	\N	44929956P	2025-11-21	\N	\N	\N	\N	\N
424	2025-12-05 06:50:51.304469+00	\N	\N	\N	\N	73226957V	2025-12-05	\N	\N	\N	\N	\N
177	2025-11-22 08:00:36.386925+00	\N	\N	\N	\N	50508514P	2025-11-22	\N	\N	\N	\N	\N
180	2025-11-22 08:09:02.247176+00	\N	\N	\N	\N	X6719502Y	2025-11-22	\N	\N	\N	\N	\N
181	2025-11-22 10:25:27.012133+00	\N	\N	\N	\N	23317387X	2025-11-22	\N	\N	\N	\N	\N
425	2025-12-05 07:26:02.442312+00	\N	\N	\N	\N	X9816437Z	2025-12-05	\N	\N	\N	\N	\N
426	2025-12-05 08:16:05.518872+00	\N	\N	\N	\N	45904376X	2025-12-05	\N	\N	\N	\N	\N
119	2025-11-03 12:58:19.441912+00	2025-11-03	\N	\N	\N	23937154L	2025-12-05	\N	\N	\N	\N	\N
430	2025-12-05 08:46:51.396165+00	\N	\N	\N	\N	54292237R	2025-12-05	\N	\N	\N	\N	\N
431	2025-12-05 11:50:23.922009+00	\N	\N	\N	\N	Z0632158P	2025-12-05	\N	\N	\N	\N	\N
432	2025-12-05 14:51:15.086005+00	\N	\N	\N	\N	Z2020699Q	2025-12-05	\N	\N	\N	\N	\N
433	2025-12-05 14:57:19.767391+00	\N	\N	\N	\N	03159051R	2025-12-05	\N	\N	\N	\N	\N
434	2026-04-27 08:05:13.611363+00	2026-04-27	\N	\N	\N	Z1066124X	2026-04-27	\N	\N	\N	\N	\N
117	2025-11-03 12:55:31.245636+00	2025-11-03	2026-05-04	\N	\N	73666906E	2025-11-21	\N	\N	\N	2026-05-04	\N
436	2026-05-04 13:37:43.779546+00	\N	\N	\N	\N	32594542	2026-05-04	\N	\N	\N	\N	\N
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

COPY "public"."empresas" ("id", "created_at", "CIF", "nombre", "direccion", "provincia", "localidad", "codigo_postal", "telefono", "fax", "sectorEmpresa", "email_empresa", "responsable_legal", "nif_responsable_legal", "horario", "pagina_web", "nombre_rellena") FROM stdin;
90	2025-11-28 13:01:19.170176+00	00000000	Testing	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
66	2025-10-30 12:36:49.244809+00	B13983010	ANPHIS SL	Ronda Narciso Monturiol 6	\N	PATERNA	46980	638089545	\N	\N	jorge.garcia@anphis.es	Jose Miguel Platero Aznar	73661414G	09:00:00 - 14:00:00	www.anphis.es	\N
67	2025-10-30 17:20:00.364006+00	B96603881	FM Grupo Tecnológico SL	Calle Algepser, 16	\N	PATERNA	46980	630114066	\N	\N	alvaro.garcia@fmgrupotec.com	Francisco J. Martínez Herrero	73654348E	08:00:00 - 17:30:00	www.fmgrupotec.com	\N
68	2025-11-03 06:26:20.53208+00	B46401675	EMAC COMPLEMENTOS SL	AV DE MADRID, 6	\N	QUART DE POBLET	46930	670313938	\N	\N	rrhh@emac.es	NURIA BOIX	48382235X	07:30:00 - 17:30:00	www.emac.es	\N
69	2025-11-03 15:41:24.170707+00	B75633016	Espectro Prometeo, S.L.	Calle dels Teixidors, 2, Piso 0,	\N	VALENCIA	46001	685975118	\N	\N	david@lagobonoia.com	David García Arcos	50868300M	09:00:00 - 14:00:00	https://www.lagobonoia.com/	\N
48	2025-10-27 12:33:30.362771+00	B46001632	AUTOBUSES VIALCO, S.L.	POL.IND PICASSENT CALLE 10 NAVE 8B	\N	PICASSENT	46220	961230673	\N	\N	rrhh@vialcobus.com	RAFAEL LLUESMA GIL	20004251R	09:00:00 - 19:00:00	http://www.vialcobus.com	\N
70	2025-11-04 09:28:29.469173+00	B98154552	VIAN DISA SL	C/ Guillem de Castro, 43	\N	VALENCIA	46007	680476576	\N	\N	victorgarcia@anasalmeron.es	Ana Díaz Salmerón	53058358A	09:30:00 - 19:30:00	https://anasalmeronformacion.es/	\N
71	2025-11-10 11:10:14.462914+00	B98763360	CONNEXT COMUNICACIÓN DIGITAL SL	Andarella 1, bloque 2, planta 1, puerta 3	\N	VALENCIA	46950	+34 657241927	\N	\N	admon@connext.es	JOAQUÍN CORTÉS AHULLÓ	20810848B	08:30:00 - 17:30:00	https://www.connext.es	\N
49	2025-10-27 12:41:54.477902+00	B56966534	Grupo Moves Innova	C/Colón 10 13a valencia	\N	VALENCIA	46004	627024604	\N	\N	info@plan-moves.com	Óscar Colomina	23324155Q	08:30:00 - 15:00:00	Plan-moves.com	\N
50	2025-10-27 12:49:24.515463+00	B98638596	CW Comunicacion S.L.	Calle Nicolas Copernico n8 Despacho 10	\N	PATERNA	46980	616026470	\N	\N	direccion@cwcomunicacion.com	Carlos Martínez	24370557X	08:30:00 - 14:30:00	cwcomunicacion.com	\N
74	2025-11-18 12:11:38.777372+00	B98079916	Sonilight S.L.	CALLE FORNER 22	\N	PATERNA	46980	961105782	\N	\N	gestion@audioprobe.es	CLARA MONDRAGÓN	45803159Q	09:00:00 - 18:00:00	https://www.audioprobe.es/	\N
76	2025-11-19 12:41:38.516916+00	B98692361	SERVICIOS IMPLANTACION DYNAMIZATIC SL	PLAZA ALQUERIA DE LA CULLA 4 DESPACHO 703	\N	ALFAFAR	46910	960624308	\N	\N	adesco@dynamizatic.com	FERNANDO DE ZARATE	53050796P	08:00:00 - 18:30:00	WWW.DYNAMIZATIC.ES	\N
77	2025-11-24 14:53:55.725691+00	B03418548	Sociedad Protección Anti Granizo S.L	Poligono 11-20,	\N	GODELLETA	46388	623491588	\N	\N	silvia.segura@grupospag.com	David Ollivier Baquero	26745293L	08:00:00 - 17:00:00	https://grupospag.com/	\N
52	2025-10-28 09:51:33.98565+00	B40545014	BLACKCROW CONFECCION Y COSTURA SL	C/Padre Jofre,7	\N	VALENCIA	46007	+34687452966	\N	\N	miquel@miquelsuay.com	Maria Jose Fuentes Pardo	B40545014	09:21:00 - 09:21:00	www.miquelsuay.com	\N
55	2025-10-28 10:40:07.302005+00	21003161K	BRILLA INFLUENCERS Y COMUNICACIÓN	AVENIDA CORALINA 22	\N	BÉTERA	46117	644256002	\N	\N	facturacionbrillainfluencers@gmail.com	THAIS GARCÍA MAS	21003161K	09:00:00 - 14:00:00	https://brillainfluencersycomunicacion.com/	\N
78	2025-11-25 09:15:25.149958+00	B09958802	GRUPO LUKINOS SL	C/Caderna 1 Local 49	\N	SAN ANTONIO DE BENAGEBER	46184	656677010	\N	\N	grupolukinos@clinicaapunto.com	Noemi Oñiga Hernández	44870162z	09:00:00 - 21:00:00	www.clinicaapunto.com	\N
56	2025-10-28 12:31:03.724385+00	B44013613	ISTOBAL ESENS	CALLE VILLA DE MADRID Nº 15	\N	L'ALCUDIA	46988	666809485	\N	\N	rmateu@istobal.com	FRANCISCO NAVARRO JARQUE	4660543R	08:00:00 - 18:00:00	ISTOBAL.COM	\N
57	2025-10-28 12:39:54.682971+00	B46445615	SANZ HERMANOS	CTRA BENISSANÓ - OLOCAU	\N	BENISSANÓ	46181	962791441	\N	\N	rrhh@gruposanz.es	JOSE JUAN SANZ PEREZ	24338637-Z	08:30:00 - 18:00:00	https://gruposanz.es	\N
79	2025-11-25 10:19:59.302986+00	B85205623	VALENCIA TRADING OFFICE S.L.	AVDA MEDITERRANEO, 8	\N	ALBUIXECH	46550	673 22 48 92	\N	\N	celia.sempere@metro-ito.com	LAURENT RENARD	X1687774B	08:00:00 - 17:00:00	https://www.metro-vto.es	\N
58	2025-10-28 13:16:57.145394+00	B96939798	1Tapiza SL / OGO Furniture	C/ Argenters 31. Pol. Ind. El Alter	\N	ALCÀSSER	46290	672452797	\N	\N	pedidos@ogofurniture.com	Juan de Dios Pérez Ramos	52842660E	08:00:00 - 17:00:00	www.ogofurniture.com	\N
59	2025-10-28 15:35:22.927483+00	B42749481	TAMARIT ESTUDIO, S.L.	Calle U de Maig 12	\N	MUSEROS	46136	962831220	\N	\N	info@tamaritestudio.com	Miquel	29209987X	08:00:00 - 14:00:00	www.tamaritestudio.com	\N
62	2025-10-29 11:57:25.260914+00	B96709134	Beta Formación	c/ Tirant Lo Blanc, 26	\N	TORRENT	46900	687724161	\N	\N	victoriav@betaformacion.com	Victoria Vazquez Miguel	53606749M	09:00:00 - 20:30:00	www.betaformacion.com	\N
61	2025-10-29 11:00:21.116881+00	B97881569	COMUNICA2 SL	C/ PUERTO RICO, 48 BAJO DCHA	\N	VALENCIA	46006	666915903	\N	\N	miguel@comunica-2.es	Miguel Rives	44500241W	08:30:00 - 16:30:00	www.comunica-2.es	\N
64	2025-10-29 14:27:43.374496+00	G96308184	Instituto Tecnológico de Embalaje, Transporte y Logística	C/ALBERT EINSTEIN 1, PARQUE TECNOLOGICO, 46980, Paterna	\N	PATERNA	46980	672387733	\N	\N	amparo.company@itene.com	Demetrio Gil	73572279V	08:00:00 - 17:00:00	https://itene.com	\N
65	2025-10-29 17:30:51.083128+00	B10649580	Gloval Gestión De Ocio 2022 SL	AV.CATALUNYA 16 ENTRESUELO IZQ B	\N	VALENCIA	46020	650026921	\N	\N	alejandro.rosalen@gmail.com	Alejandro Rosalen Folgado	53251545J	10:00:00 - 19:00:00	https://cosmicgroup.es/	\N
80	2025-11-25 12:42:51.877061+00	B03129236	POINT,S.L.	PARTIDA PLANET,SN	\N	JALON	03727	690065874	\N	\N	agarmendia@point1920.com	FRANCISCO JAVIER PONS GARCIA	21437365P	08:00:00 - 17:00:00	www.point1920.com	\N
81	2025-11-25 14:10:26.727341+00	B98203581	ÉRUGA COMUNICACIO, S.L.	CALLE BOIX 7-BAJO- DCHA	\N	VALENCIA	46003	960217474	\N	\N	administracion@eruga.es	FRANCISCO MILLA IBOR	52648438N	09:00:00 - 14:00:00	www.eruga.es	\N
82	2025-11-26 11:15:11.923633+00	B06817936	NIPPY CREATIVE HUB SL	plaza del ayuntamiento	\N	VALENCIA	46002	682384762	\N	\N	tatiana@nippycreative.com	CARLOS PONCE	24334214F	11:06:00 - 11:06:00	www.nippycreative.com	\N
86	2025-11-28 07:36:14.013359+00	B98598329	CHEPEVIM, S.L. (Grupo Different Roads)	C/ Daniel Balaciart, 4, despachos 1 y 2	\N	VALENCIA	46020	696692914 	\N	\N	rrhh@desarrollomastalento.com	Víctor Navarro Monzón	29172623K	9:00 a 20:00	https://www.differentroads.es/	Patricia Calabuig
88	2025-11-28 10:41:08.229776+00	A08536583	TIBA SPAIN SAU	Calle José Aguirre, 40	\N	VALENCIA	46011	963179461	\N	\N	nmartinez@romeu.com	Óscar Blasco	20012885X	08:30:00 - 17:15:00	https://romeu.com/	\N
89	2025-11-28 12:10:24.349636+00	B98776875	Laboratorios Eyco SL	Ronda Narciso Monturiol 4, 105A	\N	PATERNA	46980	(+34) 963 898 058	\N	\N	tecnico@laboratorioseyco.com	Susana Polo Mestre	44854709V	09:00:00 - 14:30:00	https://laboratorioseyco.com/	\N
91	2025-12-01 07:38:14.547522+00	G46102539	FEMEVAL (Federación Empresarial Metalúrgica Valenciana)	Av/ Blasco Ibañez, 127	\N	VALENCIA	46022	963719761	\N	\N	rcarracedo@femeval.es	Empar Martínez	24342933D	08:00:00 - 18:00:00	www.femeval.es	\N
92	2025-12-01 08:21:35.599499+00	B98495443	CABOLISAN, S.L.	CALLE PARIS, 16	\N	LA POBLA DE VALLBONA	46185	662108158	\N	\N	ventas@cabolisan.com	RUBEN OLIVER GASENT	26752984M	08:00:00 - 14:00:00	www.cabolisan.com	\N
93	2025-12-01 12:45:06.250388+00	B97639421	Sound Depot	C/ Convento, 56	\N	BENIPARRELL	46469	605286207	\N	\N	info@sounddepot.net	Manuel Voldman Benarroch	26763099T	09:00:00 - 14:00:00	www.sounddepot.net	\N
94	2025-12-02 10:58:05.1524+00	B97900864	DELGO OPERADOR DE TRANSPORTE, SL	C/ CID, 1 BIS PI MEDITERRANI	\N	MASSALFASSAR	46560	602226765	\N	\N	ana.martinez@delgo.es	FELIX GONZALEZ DELGADO	20194110A	08:30:00 - 17:00:00	WWW.DELGO.ES	\N
95	2025-12-02 15:20:04.957545+00	B86101995	ROI UP AGENCY SLU	Rbla. de Méndez Núñez, 40, 2ª planta, 03002, Alicante	\N	ALICANTE	03002	+34 611 93 43 16	\N	\N	malopez@roi-up.es	Diego Jiménez Rodriguez	48342630B	09:00:00 - 17:00:00	https://roiupgroup.com/es-es?utm_source=google&utm_medium=cpc&utm_campaign=campaign&utm_content=&utm_term=roi%20up%20agency&gad_source=1&gad_campaignid=22195302913&gbraid=0AAAAApu2Wbb5LTqEnpudg3INBZmK4QVqP&gclid=Cj0KCQiAubrJBhCbARIsAHIdxD8zP62-Mcmtxx-nkwRl-eC1L-D_4AP6lYb0cMy9eNHntrmYFOwXgnEaAunuEALw_wcB	\N
96	2025-12-04 10:46:03.220556+00	B42753012	Agroturn Research SL	RONDA NARCISOMONTURIOL 4 - EDIFICIO A, OFICINA 1	\N	PATERNA	46980	910611589	\N	\N	luna@agroturn.nl	Luna Celeste Ferrer Escandell	47430111V	09:00:00 - 18:00:00	https://www.agroturn.es/	\N
97	2025-12-04 11:21:36.814846+00	B02723625	Erasmus Valencia International Center	Avenida Benjamín Franklin 8	\N	PATERNA	46980	687921366	\N	\N	internationalmanager@mediterranoculinary.com	Jorge Linares	B02723625	08:00:00 - 17:00:00		\N
98	2025-12-05 09:19:10.55573+00	B98715402	ROCKET EUROPE Sl	C/ CORRETGER 127 NAVE 7 Y 5	\N	PATERNA	46111	682844463	\N	\N	rrhh@ludilo.es	CARMEN ALEJANDRA GOMEZ VERDÚ	29184977R	09:00:00 - 14:00:00		\N
99	2025-12-10 10:03:18.721063+00	B22456701	LaiaGroup SL	Pérez Bayer, 11	\N	VALENCIA	46002	646694442	\N	\N	juan@nexosmart.es	Juan Carlos Rodriguez	Y8725661G	10:00:00 - 20:00:00	https://laiadesk.com/	\N
72	2025-11-17 11:55:56.471726+00	B96882022	EA GUADALAVIAR, S.L.	C/SAN SEBASTIAN 7	\N	ALFAFAR	46910	963182112	\N	\N	administracion@eaguadalaviar.es	Antonio Salinas Martí	24350759S	08:00:00 - 14:00:00		\N
101	2026-01-19 15:36:28.673355+00	B40593055	ORBITAL EOS	Carrer de la Savina, 8	\N	PATERNA	46980	654698416	\N	\N	lydia@orbitaleos.com	Juan Peña Ibáñez	34820033B	09:30:00 - 15:30:00	www.orbitaleos.com	\N
102	2026-01-21 08:46:01.448981+00	B98707565	Saymar 2015 SL	Avda Burjasot 116 Bajo	\N	VALENCIA	46009	647447567	\N	\N	david.bartual@saymarsl.es	Agustin Fernandez Valle	32880504A	09:00:00 - 18:00:00	https://www.saymarsl.es	\N
73	2025-11-17 12:23:57.505857+00	A41810920	VIVA AQUA SERVICE SPAIN	P. I. El Molí. Partida El Testar, 8, 46980 Paterna, Valencia	\N	PATERNA	46980	683580028	\N	\N	marta.urbano@aquaservice.com	Eugenio De Miguel Vázquez	07561551W	08:20:00 - 18:00:00	https://www.aquaservice.com/	\N
85	2025-11-26 11:27:38.039907+00	A46199873	SUVIMA SA	P.I. MAS DE BALÓ C/MENORCA 12	\N	RIBA-ROJA DE TURIA	46930	607506193	\N	\N	gemma.porta@suvima.com	SUVIMA SA	A46199873	08:30:00 - 17:45:00		\N
104	2026-04-27 08:16:23.336057+00	B2244933	Sanoma	Sueca 89	\N	VALENCIA	46006	634585455	\N	Servicios profesionales y empresariales	antopiscio@gmail.com	Jordi Pujol	z1054854	08:00:00 - 18:00:00		\N
105	2026-05-04 13:41:11.36281+00	45566434567	DATA SO	molino	\N	ADEMUZ	46950	5555555555	\N	Turismo y hostelería	info@data-so.com	sofia	455555	15:00:00 - 08:00:00	data-so.com	\N
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
112	2025-11-18 12:11:39.157612+00	\N	2025-11-18	\N	\N	\N	\N	B98079916	\N	\N	\N	\N
114	2025-11-19 12:41:38.94504+00	\N	2025-11-19	\N	\N	\N	\N	B98692361	\N	\N	\N	\N
115	2025-11-24 14:53:56.074518+00	\N	2025-11-24	\N	\N	\N	\N	B03418548	\N	\N	\N	\N
116	2025-11-25 09:15:25.478001+00	\N	2025-11-25	\N	\N	\N	\N	B09958802	\N	\N	\N	\N
117	2025-11-25 10:19:59.72309+00	\N	2025-11-25	\N	\N	\N	\N	B85205623	\N	\N	\N	\N
118	2025-11-25 12:42:52.215994+00	\N	2025-11-25	\N	\N	\N	\N	B03129236	\N	\N	\N	\N
119	2025-11-25 14:10:27.136478+00	\N	2025-11-25	\N	\N	\N	\N	B98203581	\N	\N	\N	\N
120	2025-11-26 11:15:12.306028+00	\N	2025-11-26	\N	\N	\N	\N	B06817936	\N	\N	\N	\N
123	2025-11-26 11:27:38.323645+00	\N	2025-11-26	\N	\N	\N	\N	A46199873	\N	\N	\N	\N
124	2025-11-28 10:41:08.491434+00	\N	2025-11-28	\N	\N	\N	\N	A08536583	\N	\N	\N	\N
125	2025-11-28 12:10:24.598+00	\N	2025-11-28	\N	\N	\N	\N	B98776875	\N	\N	\N	\N
126	2025-12-01 07:38:14.807988+00	\N	2025-12-01	\N	\N	\N	\N	G46102539	\N	\N	\N	\N
127	2025-12-01 08:21:35.960109+00	\N	2025-12-01	\N	\N	\N	\N	B98495443	\N	\N	\N	\N
128	2025-12-01 12:45:06.696584+00	\N	2025-12-01	\N	\N	\N	\N	B97639421	\N	\N	\N	\N
129	2025-12-02 10:58:05.605719+00	\N	2025-12-02	\N	\N	\N	\N	B97900864	\N	\N	\N	\N
130	2025-12-02 15:20:05.421627+00	\N	2025-12-02	\N	\N	\N	\N	B86101995	\N	\N	\N	\N
131	2025-12-04 10:46:03.582787+00	\N	2025-12-04	\N	\N	\N	\N	B42753012	\N	\N	\N	\N
132	2025-12-04 11:21:37.127798+00	\N	2025-12-04	\N	\N	\N	\N	B02723625	\N	\N	\N	\N
133	2025-12-05 09:19:10.894512+00	\N	2025-12-05	\N	\N	\N	\N	B98715402	\N	\N	\N	\N
134	2025-12-10 10:03:19.120428+00	\N	2025-12-10	\N	\N	\N	\N	B22456701	\N	\N	\N	\N
110	2025-11-17 11:55:56.81847+00	\N	2026-01-08	\N	\N	\N	\N	B96882022	\N	\N	\N	\N
136	2026-01-19 15:36:29.109552+00	\N	2026-01-19	\N	\N	\N	\N	B40593055	\N	\N	\N	\N
137	2026-01-21 08:46:01.897312+00	\N	2026-01-21	\N	\N	\N	\N	B98707565	\N	\N	\N	\N
111	2025-11-17 12:23:57.786632+00	\N	2026-01-22	\N	\N	\N	\N	A41810920	\N	\N	\N	\N
139	2026-04-27 08:16:23.794154+00	\N	2026-04-27	\N	\N	\N	\N	B2244933	\N	\N	\N	\N
140	2026-05-04 13:41:11.590225+00	\N	2026-05-04	\N	\N	\N	\N	45566434567	\N	\N	\N	\N
\.


--
-- Data for Name: error_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."error_logs" ("id", "created_at", "log", "pagina") FROM stdin;
\.


--
-- Data for Name: oferta_fp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."oferta_fp" ("id", "created_at", "empresa", "ciclos_formativos", "puestos", "requisitos", "contrato", "vehiculo", "estado", "motivo", "direccion_empresa", "localidad_empresa", "cp_empresa", "nombre_rellena_form", "cupo_alumnos", "tutor", "tipo", "seguimiento_gestores", "tutores_por_puesto") FROM stdin;
85	2026-01-08 11:13:05.380047+00	B96882022	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "gestión de almacén, stock y pedidos"}, {"area": "Operaciones logísticas y distribución", "proyecto": "gestión de envío de pedidos y recogida materiales proveedores"}]}		Sí	Sí	Nuevo	\N	C/ BOMBERS 7	PATERNA	46980	YOLANDA GUZMÁN ORTIZ	1	29	\N	\N	\N
86	2026-01-19 15:36:29.67497+00	B40593055	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Desarrollo de un plan de marketing adaptado a los objetivos estratégicos de Orbital"}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "Gestión y planificación de contenidos para redes sociales (principalmente LinkedIn y otras plataformas relevantes)."}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "Apoyo en la definición del posicionamiento de marca y mensajes clave."}]}	B2 de inglés	Sí	No	Nuevo	\N	Carrer de la Savina, 8	Paterna	46980	Lydia Vicente Lord	1	56	\N	\N	\N
87	2026-01-21 08:46:02.486365+00	B98707565	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "RRSS"}], "DESARROLLO APLICACIONES WEB": [{"area": "Soporte técnico en entornos web", "proyecto": ""}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Integración de sistemas multiplataforma", "proyecto": "MDM"}]}		Sí	No	Nuevo	\N	Avda Burjasot 116 Bajo	Valencia	46009	David Bartual	3	57	\N	\N	\N
63	2025-11-19 12:41:39.544054+00	B98692361	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 0}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "campañas en CRM, documentación, Presentaciones de empresa, hojas de productos, etc"}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "publicaciones en linkedIn"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "posicionamiento web, entradas en elblog "}, {"area": "Atención al cliente y fidelización", "proyecto": "encuestas satisfacción CRM"}]}	Carnet de conducir y Vehículo propio para desplazarse a Alfafar.\nInteresado en el sector TIC.	Sí	Sí	Nuevo	\N	PLAZA ALQUERIA DE LA CULLA 4 DESPACHO 703,	ALFAFAR	46910	AMPARO	1	33	\N	\N	\N
88	2026-01-22 08:29:27.001314+00	A41810920	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Operaciones logísticas y distribución", "proyecto": ""}]}	No se establecen requisitos adicionales. Se valorarán competencias básicas como trabajo en equipo, responsabilidad y ganas de aprender.	Sí	Sí	Nuevo	\N	P. I. El Molí. Partida El Testar, 8, 46980 Paterna, Valencia	Paterna	46980	Marta Urbano	1	30	\N	\N	\N
89	2026-04-27 08:16:24.404625+00	B2244933	{"DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 0}}	{"DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo backend", "proyecto": "Project o1"}, {"area": "Bases de datos", "proyecto": "Projecyo 2"}, {"area": "Administración de sistemas web/hosting", "proyecto": "projecto 3"}]}	ingles es un plus	Sí	No	Nuevo	\N	Sueca 89	VALENCIA	46006	Carlos Viña	1	59	\N	\N	\N
90	2026-05-04 13:41:12.209322+00	45566434567	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "REDES SOCIALES"}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "GESTION DE ALMACEN"}, {"area": "Operaciones logísticas y distribución", "proyecto": "LOGISTICA EN VALENCIA"}], "DESARROLLO APLICACIONES WEB": [{"area": "Bases de datos", "proyecto": "GGG"}]}	B1 DE INGLES	Sí	Sí	Nuevo	\N	MOLINOO	7657657	765765	SOFIA	3	60	\N	\N	\N
39	2025-10-28 09:51:35.545254+00	B40545014	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 2, "disponibles": 2}}	{"COMERCIO INTERNACIONAL": [{"area": "Compras internacionales/ aprovisionamiento", "proyecto": "www.clec.fashion"}, {"area": "Atención a clientes internacionales", "proyecto": "www.miquelsuay.com; www.clec.fashion"}, {"area": "Gestión documental/ almacén", "proyecto": "www.miquelsuay.com"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "www.miquelsuay.com; www.clec.fashion "}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Gestión de eventos", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Atención al cliente y fidelización", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "www.miquelsuay.com"}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": "www.miquelsuay.com; www.clec.fashion"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Desarrollo backend", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Soporte técnico en entornos web", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Administración de sistemas web/hosting", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}]}	B1 de ingles	Sí	No	Nuevo	\N	PADRE JOFRE,7	VALENCIA	46007	Miquel Angel Garcia Gimeno	8	9	\N	\N	\N
40	2025-10-28 09:51:35.555347+00	B40545014	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 2, "disponibles": 2}}	{"COMERCIO INTERNACIONAL": [{"area": "Compras internacionales/ aprovisionamiento", "proyecto": "www.clec.fashion"}, {"area": "Atención a clientes internacionales", "proyecto": "www.miquelsuay.com; www.clec.fashion"}, {"area": "Gestión documental/ almacén", "proyecto": "www.miquelsuay.com"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "www.miquelsuay.com; www.clec.fashion "}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Gestión de eventos", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Atención al cliente y fidelización", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "www.miquelsuay.com"}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": "www.miquelsuay.com; www.clec.fashion"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Desarrollo backend", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Soporte técnico en entornos web", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Administración de sistemas web/hosting", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}]}	B1 de ingles	Sí	No	Nuevo	\N	PADRE JOFRE,7	VALENCIA	46007	Miquel Angel Garcia Gimeno	8	9	\N	\N	\N
41	2025-10-28 09:51:40.601497+00	B40545014	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 2, "disponibles": 2}}	{"COMERCIO INTERNACIONAL": [{"area": "Compras internacionales/ aprovisionamiento", "proyecto": "www.clec.fashion"}, {"area": "Atención a clientes internacionales", "proyecto": "www.miquelsuay.com; www.clec.fashion"}, {"area": "Gestión documental/ almacén", "proyecto": "www.miquelsuay.com"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "www.miquelsuay.com; www.clec.fashion "}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Gestión de eventos", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Atención al cliente y fidelización", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "www.miquelsuay.com"}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": "www.miquelsuay.com; www.clec.fashion"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Desarrollo backend", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Soporte técnico en entornos web", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}, {"area": "Administración de sistemas web/hosting", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": "www. miquelsuay.com; www.clec.fashion, www.valenciafashioninstitute.com"}]}	B1 de ingles	Sí	No	Nuevo	\N	PADRE JOFRE,7	VALENCIA	46007	Miquel Angel Garcia Gimeno	8	9	\N	\N	\N
35	2025-10-27 12:33:31.372326+00	B46001632	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de tráfico y transporte terrestre; marítimo o aéreo", "proyecto": ""}, {"area": "Administración y documentación de transporte", "proyecto": ""}]}		Sí	Sí	Nuevo	\N	POL.IND PICASSENT CALLE 10 NAVE 8B	PICASSENT	46220	Salomé Rodríguez Estrems	1	5	\N	\N	\N
36	2025-10-27 12:41:55.187461+00	B56966534	{"MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}}	{}		Sí	Sí	Nuevo	\N	C/ Miquel marqués 15 pobla de farnals	La Pobla de Farnals	46139	Óscar Colomina	2	6	\N	\N	\N
37	2025-10-27 12:49:25.302451+00	B98638596	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{}	Sería ideal que tuviese conocimientos avanzados de RRSS y entorno Wordpress/elementor	Sí	No	Nuevo	\N	Calle Nicolas Copernico n8 Despacho 10	Paterna	46980	Carlos Martínez	1	7	\N	\N	\N
42	2025-10-28 10:40:08.098811+00	21003161K	{"MARKETING Y PUBLICIDAD": {"alumnos": 5, "disponibles": 5}, "DESARROLLO APLICACIONES WEB": {"alumnos": 3, "disponibles": 3}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Campañas clientes"}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "Publicaciones RRSS"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "SEO On-page y Off-page"}, {"area": "Atención al cliente y fidelización", "proyecto": "Comunicación con clientes"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "Wordpress CSS"}, {"area": "Desarrollo backend", "proyecto": "Html javascript CSS"}, {"area": "Bases de datos", "proyecto": "Bases de datos internas"}, {"area": "Soporte técnico en entornos web", "proyecto": "Mantenimiento para clientes"}, {"area": "Administración de sistemas web/hosting", "proyecto": "Páginas web clientes"}]}	No es necesario.	Sí	No	Nuevo	\N	AVENIDA CORALINA 22	BETERA	46117	THAIS GARCÍA MAS	8	12	\N	\N	\N
43	2025-10-28 12:31:04.618211+00	B44013613	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de tráfico y transporte terrestre; marítimo o aéreo", "proyecto": "Tareas del puesto"}, {"area": "Gestión de almacén y stock", "proyecto": "Tareas del puesto"}, {"area": "Operaciones logísticas y distribución", "proyecto": "Tareas del puesto"}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": "Tareas del puesto"}, {"area": "Administración y documentación de transporte", "proyecto": "Tareas del puesto"}]}	Recomendable Inglés	Sí	Sí	Nuevo	\N	CALLE VILLA DE MADRID Nº 15	PATERNA	46988	RAMON MATEU ORTIZ	1	13	\N	\N	\N
44	2025-10-28 12:39:56.46468+00	B46445615	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": "-actualización de bases de datos , coordinación con transitarios , gestión pedidos internacionales , preparación y revisión documentación "}, {"area": "Gestión documental/ almacén", "proyecto": "organización y archivo digital expedientes, soporte tareas administrativas, informes"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "- apoyo en la planificación y ejecución de campañas, redacción contenidos redes sociales"}, {"area": "Gestión de eventos", "proyecto": "coordinación logística eventos corporativos, preparación materiales y soporte durante ejecución eventos"}, {"area": "Estudios de mercado e investigación comercial", "proyecto": "posibilidad de colaborar en un estudio de mercado, recogida datos y análisis de datos, apoyo en encuestas, elaboración de presentaciones"}]}	Comercio Internacional ingles nivel avanzado.	Sí	Sí	Nuevo	\N	CARRETERA BENISSANÓ OLOCAU	BENISSANÓ	46181	ISABEL PLUMED	2	14	\N	\N	\N
45	2025-10-28 13:16:58.075144+00	B96939798	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": "Asistencia departamento exportación"}, {"area": "Atención a clientes internacionales", "proyecto": "Asistencia departamento exportación"}, {"area": "Gestión documental/ almacén", "proyecto": "Asistencia departamento exportación"}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Asistencia departamento marketing"}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "Asistencia departamento marketing"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "Asistencia departamento marketing"}, {"area": "Gestión de eventos", "proyecto": "Asistencia departamento marketing"}, {"area": "Estudios de mercado e investigación comercial", "proyecto": "Asistencia departamento marketing"}]}	Buenas habilidades de comunicación oral y escrita. \nManejo básico paquete Office.\nAcostumbrado a trabajar en equipo y coordinarse con toda el área de ventas, administración, marketing y producción.\nEspañol nativo o nivel C2. Valorable buen nivel de inglés (B2) o de otros idiomas (alemán, italiano, árabe).	Sí	Sí	Nuevo	\N	C/ Argenters 31, Pol. Ind. El Alter	Alcàsser	46290	Paula Centeno Ortí	2	15	\N	\N	\N
46	2025-10-28 15:35:23.781567+00	B42749481	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "1"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "1"}]}		Sí	Sí	Nuevo	\N	Calle U de Maig 12	Museros	46136	Miquel Tamarit	1	16	\N	\N	\N
47	2025-10-28 16:47:26.880426+00	B42749481	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "1"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "1"}]}		Sí	Sí	Nuevo	\N	Calle U de Maig 12	Museros	46136	Miquel Tamarit	1	16	\N	\N	\N
48	2025-10-29 11:00:21.822015+00	B97881569	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "www.gastroagencia.es"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "www.comunica-2.es"}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": "www.gastroagencia.es"}]}	Respnsabilidad, actutud y trabajo en equipo.	Sí	No	Nuevo	\N	C/ PUERTO RICO, 48 BAJO DCHA	Valencia	46006	Miguel Rives	2	18	\N	\N	\N
49	2025-10-29 11:57:26.197299+00	B96709134	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "REdes Sociales"}], "DESARROLLO APLICACIONES WEB": [{"area": "Soporte técnico en entornos web", "proyecto": "mantenimiento  y soporte pagina web"}]}	Seria conveniente que el alumnado fuera de poblaciones cercanas o del mismo  Torrent, aunque el centro tiene a 5 minutos la estación Avda. Pais Valenciano  de Torrent. Hoy como sabeis las personas ademas de tener la competencia profesional que corresponden deben saber trabajar en equipo  asi como las soft skills	Sí	No	Nuevo	\N	c/ Tirant Lo Blanc, 26	TORRENT	46900	Victoria  Vazquez Miguel	2	19	\N	\N	\N
51	2025-10-29 14:27:44.372496+00	G96308184	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": "Proyecto en Laboratorio de Embalaje"}, {"area": "Operaciones logísticas y distribución", "proyecto": "Proyecto en Laboratorio de Embalaje"}]}	Nota media de expediente mínimo un 7\nProactividad\nTrabajo en equipo\nResolución de problemas\nResistencia a la adversidad	Sí	No	Nuevo	\N	C/ALBERT EINSTEIN 1, PARQUE TECNOLOGICO, 46980, Paterna	Paterna	46980	Amparo Company	1	21	\N	\N	\N
52	2025-10-29 17:30:51.946358+00	B10649580	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Gestión de eventos", "proyecto": ""}]}	Trabajo en equipo, proactividad, creatividad, responsabilidad, tendencias actuales, conocimiento de herramientas como canva, metricool...	Sí	No	Nuevo	\N	Gran Vía Marqués del Turia 54, 8	Valencia	46005	Jorge Turmo Ferro	1	22	\N	\N	\N
53	2025-10-30 12:36:50.243355+00	B13983010	{"DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": ""}, {"area": "Desarrollo backend", "proyecto": ""}, {"area": "Bases de datos", "proyecto": ""}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": ""}, {"area": "Desarrollo software", "proyecto": ""}]}	Buenas tardes, en principio podemos crear una plaza, de uno de los dos ciclos seleccionados. Si pensamos que podemos acoger a dos alumnos os lo comunicaremos pero de momento solo podemos atender a un alumno. Gracias.	Sí	Sí	Nuevo	\N	Ronda Narciso Monturiol 6	Paterna	46980	Jorge Garcia	2	23	\N	\N	\N
54	2025-10-30 17:20:01.372793+00	B96603881	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Atención a clientes internacionales", "proyecto": ""}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Gestión de eventos", "proyecto": ""}, {"area": "Atención al cliente y fidelización", "proyecto": ""}, {"area": "Estudios de mercado e investigación comercial", "proyecto": ""}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de tráfico y transporte terrestre; marítimo o aéreo", "proyecto": ""}, {"area": "Gestión de almacén y stock", "proyecto": ""}, {"area": "Operaciones logísticas y distribución", "proyecto": ""}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": ""}, {"area": "Administración y documentación de transporte", "proyecto": ""}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": ""}, {"area": "Desarrollo software", "proyecto": ""}, {"area": "Soporte técnico y mantenimiento de apps", "proyecto": ""}, {"area": "Integración de sistemas multiplataforma", "proyecto": ""}]}	Trabajo en equipo y proactividad.	Sí	No	Nuevo	\N	Calle Algepser, 16	Paterna	46980	Álvaro García	4	24	\N	\N	\N
55	2025-11-03 06:26:22.393935+00	B46401675	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": "EXPANSION "}]}		Sí	No	Nuevo	\N	AV DE MADRID 6	QUART DE POBLET	46930	SUSANA FRESNEDA	1	25	\N	\N	\N
56	2025-11-03 15:41:25.183142+00	B75633016	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "lagobonoia.com"}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "lagobonoia.com"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "lagobonoia.com"}, {"area": "Atención al cliente y fidelización", "proyecto": "lagobonoia.com"}]}	Se valorará una actitud proactiva, ganas de aprender y capacidad para adaptarse a entornos dinámicos. Buscamos una persona con iniciativa, resolutiva y con interés por aplicar herramientas de inteligencia artificial (IA) en el ámbito del marketing y la automatización de procesos —tanto para generación de imágenes como de contenidos (copywriting)—.\nEl trabajo es semipresencial: algunas jornadas se realizarán de forma presencial en Valencia, con formación directa, y otras desde casa en modalidad remota.	Sí	No	Nuevo	\N	P.º de la Pechina, 15	Valencia	46008	David García Arcos	1	26	\N	\N	\N
57	2025-11-04 09:28:30.401657+00	B98154552	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Estrategia y creación de campañas de matriculación en formación de imagen personal."}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "Community management y creación de contenido orgánico en nuestra redes sociales (Facebook, Instagram y Tik Tok)"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "Creación de cursos online y optimización SEO de nuestras tiendas online"}]}	Se valorará:\nSoft skills: proactividad, trabajo en equipo, soluciones creativas.\nNo es indispensable pero ayuda: Wordpress, Meta suite, Canva, Edición de vídeo, Adobe Creative Suite.	Sí	No	Nuevo	\N	C/ Guillem de Castro, 43	Valencia	46007	Víctor García Sanjuan	1	27	\N	\N	\N
58	2025-11-10 11:10:15.632358+00	B98763360	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Planificación estratégica, asesoramiento, coordinación y seguimiento de acciones para alcanzar los objetivos de negocio."}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": "Gestión de la estrategia de comunicación en Redes Sociales"}, {"area": "Marketing digital (SEO/SEM)", "proyecto": "Proyecto  de implementación de acciones técnicas y de contenido para optimizar el posicionamiento orgánico y aumentar la visibilidad web. "}]}	Capacidad de trabajo en equipo y valorable inglés B1 (no obligatorio).	Sí	No	Nuevo	\N	Andarella 1, bloque 2, planta 1, puerta 3	Valencia	46950	CLAUDIA COSSU	1	28	\N	\N	\N
59	2025-11-17 11:55:57.311992+00	B96882022	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de tráfico y transporte terrestre; marítimo o aéreo", "proyecto": "COORDINACIÓN TRANSPORTE"}, {"area": "Gestión de almacén y stock", "proyecto": "GESTION DE ALMACÉN Y STOCK"}, {"area": "Operaciones logísticas y distribución", "proyecto": "SEGUIMIENTO PEDIDOS"}]}		Sí	Sí	Nuevo	\N	C/ BOMBERS 7	PATERNA	46980	YOLANDA GUZMÁN ORTIZ	1	29	\N	\N	\N
60	2025-11-17 12:23:58.281278+00	A41810920	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de almacén y stock", "proyecto": ""}]}	Propuesta de incorporación – Prácticas en Logística y Transporte\n\nNuestra idea es incorporar a una persona con formación en Grado Superior de Logística y Transporte, interesada en desarrollarse profesionalmente en el ámbito del almacén y la logística interna. Buscamos alguien con disposición para aprender desde cero, con la posibilidad de comenzar realizando prácticas y, posteriormente, integrarse de manera estable en la empresa.\n\nFunciones principales:\n\nCarga y descarga de vehículos de reparto y trailers.\n\nGestión de inventarios y control de stock.\n\nManejo del sistema SAP.\n\nAsistencia a reuniones relacionadas con la logística.\n\nMantenimiento del orden y la limpieza en el almacén.\n\nOfrecemos la oportunidad de formación práctica y crecimiento profesional en un entorno dinámico y cercano, aprendiendo todos los aspectos de la logística interna de la empresa.	Sí	Sí	Nuevo	\N	P. I. El Molí. Partida El Testar, 8,  Paterna, Valencia	Paterna	46980	Marta	1	30	\N	\N	\N
61	2025-11-18 12:11:39.758109+00	B98079916	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}]}	Nos gustaría poder hacerle una entrevista para que aprendan el lado de la vida laboral real.	Sí	Sí	Nuevo	\N	CALLE FORNER 22	Paterna	46980	CLARA MONDRAGÓN	1	31	\N	\N	\N
62	2025-11-18 12:11:57.875831+00	B98079916	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "ESTRATEGIA Y CAMPAÑAS"}]}	Nos gustaría poder hacerle una entrevista para que aprendan el lado de la vida laboral real.	Sí	Sí	Nuevo	\N	CALLE FORNER 22	Paterna	46980	CLARA MONDRAGÓN	1	31	\N	\N	\N
64	2025-11-24 14:53:56.606358+00	B03418548	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": ""}, {"area": "Compras internacionales/ aprovisionamiento", "proyecto": ""}, {"area": "Atención a clientes internacionales", "proyecto": ""}, {"area": "Gestión documental/ almacén", "proyecto": ""}], "MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Marketing digital (SEO/SEM)", "proyecto": ""}, {"area": "Gestión de eventos", "proyecto": ""}, {"area": "Estudios de mercado e investigación comercial", "proyecto": ""}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Operaciones logísticas y distribución", "proyecto": ""}, {"area": "Atención al cliente/logística inversa (devoluciones)", "proyecto": ""}, {"area": "Administración y documentación de transporte", "proyecto": ""}]}	El alumno debe disponer de carnet de conducir y vehiculo para poder llegar diariamente a nuestras instalaciones. \nSe valorarán los idiomas de Ingles y Francés en las candidaturas.	Sí	Sí	Nuevo	\N	Poligono 11-20	Godelleta	46388	Silvia Segura	3	34	\N	\N	\N
65	2025-11-25 09:15:25.95223+00	B09958802	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}]}	Se valorará conocimiento y habilidades en fotografía, grabación y edición de vídeo y diseño gráfico	Sí	Sí	Nuevo	\N	C/Caderna 1 Local 49	San Antonio de Benageber	46184	Noemi Oñiga Hernández	1	35	\N	\N	\N
66	2025-11-25 10:20:00.329327+00	B85205623	{"COMERCIO INTERNACIONAL": {"alumnos": 2, "disponibles": 2}}	{"COMERCIO INTERNACIONAL": [{"area": "Compras internacionales/ aprovisionamiento", "proyecto": ""}, {"area": "Gestión documental/ almacén", "proyecto": ""}]}	INGLES, MINIMO B2	No	Sí	Nuevo	\N	AVDA MEDITERRANEO, 8 (POLIGONO INDUSTRIAL)	ALBUIXECH	46550	CELIA SEMPERE	2	36	\N	\N	\N
67	2025-11-25 12:42:52.771956+00	B03129236	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Marketing digital (SEO/SEM)", "proyecto": ""}]}	B1 de inglés	Sí	Sí	Nuevo	\N	PARTIDA PLANET,SN	JALON	03727	ARANTXA GARMENDIA	1	37	\N	\N	\N
68	2025-11-25 14:10:27.627656+00	B98203581	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Marketing digital (SEO/SEM)", "proyecto": ""}]}		Sí	No	Nuevo	\N	CALLE BOIX 7-BAJO-DCHA.	VALENCIA	46003	MARTA GÓMEZ ESPINOSA	1	38	\N	\N	\N
69	2025-11-26 11:15:12.879654+00	B06817936	{"MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}], "DESARROLLO APLICACIONES WEB": [{"area": "Administración de sistemas web/hosting", "proyecto": "WORDPRESS/ DISEÑO WEB "}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": ""}]}	TRABAJO EN EQUIPO \nEMPATIA\nPROACTIVIDAD	Sí	No	Nuevo	\N	plaza del ayuntamiento	valenciA	46002	TATIANA GOMEZ CASARES	4	39	\N	\N	\N
70	2025-11-26 11:16:13.390095+00	B06817936	{"MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}], "DESARROLLO APLICACIONES WEB": [{"area": "Administración de sistemas web/hosting", "proyecto": "WORDPRESS/ DISEÑO WEB "}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": ""}]}	TRABAJO EN EQUIPO \nEMPATIA\nPROACTIVIDAD	Sí	No	Nuevo	\N	plaza del ayuntamiento	valenciA	46002	TATIANA GOMEZ CASARES	4	39	\N	\N	\N
71	2025-11-26 11:18:38.139527+00	B06817936	{"MARKETING Y PUBLICIDAD": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "SI"}], "DESARROLLO APLICACIONES WEB": [{"area": "Administración de sistemas web/hosting", "proyecto": "WORDPRESS/ DISEÑO WEB "}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": "SI"}]}	TRABAJO EN EQUIPO \nEMPATIA\nPROACTIVIDAD	Sí	No	Nuevo	\N	plaza del ayuntamiento	valenciA	46002	TATIANA GOMEZ CASARES	4	39	\N	\N	\N
72	2025-11-26 11:27:38.816327+00	A46199873	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "Campañas de marketing"}]}	Alumno proactivo, con ganas de hacer cosas y aprender, que no se agobie si en algún momento hay trabajo de más y que no se sienta sobrepasado. Que sea responsable ya que se tocan algunos temas más serios y delicados relacionados directamente con clientes. Capaz de apoyar en la gestión de otras cosas como eventos que la empresa lleva a cabo.	Sí	Sí	Nuevo	\N	P.I. MAS DE BALÓ C/MENORCA 12	RIBARROJA DEL TURIA, VALENCIA	46930	GEMMA PORTA	1	42	\N	\N	\N
84	2025-12-10 10:03:19.67434+00	B22456701	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": "LaiaDesk"}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo aplicaciones móviles", "proyecto": "app LaiaDesk"}]}	Aunque muchas de las existencias podrían ser online de preferencia residente, Valencia	Sí	No	Nuevo	\N	Pérez Bayer, 11	Valencia	460002	Juan Carlos Rodriguez	2	54	\N	\N	\N
73	2025-11-28 10:41:08.906813+00	A08536583	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}, "TRANSPORTE Y LOGÍSTICA": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES WEB": {"alumnos": 1, "disponibles": 1}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": ""}, {"area": "Departamento Comercio Ext/aduanas", "proyecto": ""}, {"area": "Compras internacionales/ aprovisionamiento", "proyecto": ""}, {"area": "Atención a clientes internacionales", "proyecto": ""}], "TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de tráfico y transporte terrestre; marítimo o aéreo", "proyecto": ""}, {"area": "Administración y documentación de transporte", "proyecto": ""}], "DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": ""}, {"area": "Desarrollo backend", "proyecto": ""}, {"area": "Soporte técnico en entornos web", "proyecto": ""}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo software", "proyecto": ""}, {"area": "Soporte técnico y mantenimiento de apps", "proyecto": ""}, {"area": "Integración de sistemas multiplataforma", "proyecto": ""}]}	Nivel medio - avanzado de inglés para los alumnos de los grados en Comercio Internacional y Transporte y Logística. Para los alumnos de la rama de IT no sería un requisito.	Sí	No	Nuevo	\N	Calle José Aguirre, 40	Valencia	46011	Noelia Martínez	4	43	\N	\N	\N
74	2025-11-28 12:10:25.059249+00	B98776875	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Marketing digital (SEO/SEM)", "proyecto": ""}, {"area": "Atención al cliente y fidelización", "proyecto": ""}]}		Sí	Sí	Nuevo	\N	Ronda Narciso Monturiol 4, 105A	Paterna	46980	Celia Arnau García	1	44	\N	\N	\N
79	2025-12-02 10:58:06.180374+00	B97900864	{"TRANSPORTE Y LOGÍSTICA": {"alumnos": 2, "disponibles": 2}}	{"TRANSPORTE Y LOGÍSTICA": [{"area": "Gestión de tráfico y transporte terrestre; marítimo o aéreo", "proyecto": "GESTIÓN DE TRAFICO TRANSPORTE TERRESTRE"}, {"area": "Administración y documentación de transporte", "proyecto": "DOCUMENTACIÓN TRANSPORTE Y SOFTWARE"}]}	VEHICULO PROPIO Y PERMISO DE CONDUCIR	Sí	Sí	Nuevo	\N	C/ CID, 1 PI MEDITERRANI	Massalfassar	46560	ANA MARTINEZ MARTINEZ	2	49	\N	\N	\N
80	2025-12-02 15:20:06.069185+00	B86101995	{"DESARROLLO APLICACIONES WEB": {"alumnos": 2, "disponibles": 2}, "DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 2, "disponibles": 2}}	{"DESARROLLO APLICACIONES WEB": [{"area": "Desarrollo fronted", "proyecto": ""}, {"area": "Soporte técnico en entornos web", "proyecto": ""}], "DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Bases de datos y gestión de información", "proyecto": ""}, {"area": "Integración de sistemas multiplataforma", "proyecto": ""}]}	Inglés B2, disponibilidad para modalidad hibrida	Sí	No	Nuevo	\N	Rbla. de Méndez Núñez, 40, 2ª planta, 03002, Alicante	Alicante	03002	Mariana López	4	50	\N	\N	\N
81	2025-12-04 10:46:04.067937+00	B42753012	{"DESARROLLO APLICACIONES MULTIPLATAFORMA": {"alumnos": 1, "disponibles": 1}}	{"DESARROLLO APLICACIONES MULTIPLATAFORMA": [{"area": "Desarrollo software", "proyecto": ""}]}	El trabajo es 100% remoto y el horario es flexible aunque se valorará disponibilidad de 10 a 14h. Incorporación inmediata.\nSe requieren conocimientos en Python, C# y usar GitHub.\nSe valorará positivamente estar familiarizado con Revit, conocimiento de Typescript o Javascript y trabajo previo en bases de datos.\nEl trabajo es remoto.	Sí	Sí	Nuevo	\N	RONDA NARCISOMONTURIOL 4 - EDIFICIO A, OFICINA 1	Paterna	46980	Sabina Parlatore	1	51	\N	\N	\N
82	2025-12-04 11:21:37.651745+00	B02723625	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Gestión de eventos", "proyecto": ""}, {"area": "Atención al cliente y fidelización", "proyecto": ""}, {"area": "Estudios de mercado e investigación comercial", "proyecto": ""}]}	Responsabilidad, creatividad e Inglés B2, a ser posible. Se valora cualquier otro idioma.	No	Sí	Nuevo	\N	Avenida Benjamín Franklin 8	Paterna	46980	Ramona Bucur	1	52	\N	\N	\N
83	2025-12-05 09:19:11.559224+00	B98715402	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Marketing digital (SEO/SEM)", "proyecto": "VENTA DIGITAL"}]}	Idiomas:\n•\tPreferiblemente Inglés nivel medio\nConocimientos técnicos:\n•\tManejo del paquete Office, especialmente Excel (fórmulas, buscar V, etc.).\n•\tManejo de la herramienta de diseño Canva.\nOtros:\n•\tCarné de conducir y vehículo propio (imprescindible).	No	Sí	Nuevo	\N	C/CORRETGER 127 NAVE 5 Y 7 P.E. TÁCTICA	PATERNA	46980	IRENE LLORENS	1	53	\N	\N	\N
75	2025-11-28 12:37:36.107107+00	B98598329	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 0}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}]}	\N	Sí	No	Completa	\N	C/ Daniel Balaciart, 4, despachos 1 y 2	Valencia	46002	Andrea	1	45	\N	\N	\N
76	2025-12-01 07:38:15.245811+00	G46102539	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Departamento de Marketing (estrategia/campañas)", "proyecto": ""}, {"area": "Publicidad y Comunicación (redes sociales)", "proyecto": ""}, {"area": "Marketing digital (SEO/SEM)", "proyecto": ""}]}		Sí	No	Nuevo	\N	Av/ Blasco Ibañez, 127	Valencia	46022	Raquel Carracedo	1	46	\N	\N	\N
77	2025-12-01 08:21:36.504007+00	B98495443	{"COMERCIO INTERNACIONAL": {"alumnos": 1, "disponibles": 1}}	{"COMERCIO INTERNACIONAL": [{"area": "Departamento Export/import", "proyecto": ""}, {"area": "Departamento Comercio Ext/aduanas", "proyecto": ""}, {"area": "Compras internacionales/ aprovisionamiento", "proyecto": ""}, {"area": "Atención a clientes internacionales", "proyecto": ""}, {"area": "Gestión documental/ almacén", "proyecto": ""}]}	APTITUDES. Con esto, lo demás se aprende fácil.\nAdemás de la rama de comercio la persona realizará trabajos de otras ramas: contabilidad, marketing, etc. Todo lo que aparezca en el día a día de una pyme.	Sí	Sí	Nuevo	\N	CALLE PARIS, 16	LA POBLA DE VALLBONA	46185	RUBEN OLIVER GASENT	1	47	\N	\N	\N
78	2025-12-01 12:45:07.334209+00	B97639421	{"MARKETING Y PUBLICIDAD": {"alumnos": 1, "disponibles": 1}}	{"MARKETING Y PUBLICIDAD": [{"area": "Marketing digital (SEO/SEM)", "proyecto": ""}]}	Que sea una persona con iniciativa	Sí	Sí	Nuevo	\N	C/ Convento, 56	Beniparrell	46469	Manuel Voldman Benarroch	1	48	\N	\N	\N
\.


--
-- Data for Name: practicas_fp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."practicas_fp" ("id", "created_at", "empresa", "oferta", "alumno", "ciclo_formativo", "area", "proyecto", "fecha_inicio", "tutor", "feedback_tutor", "anexos_creados", "anexos_enviados", "anexos_firmados", "doc_sao_entregada", "status", "tutor_centro", "gestor", "motivo", "feedback_tutor_centro", "direccion", "localidad", "anio", "curso") FROM stdin;
62	2026-04-27 08:29:00.697505+00	B2244933	\N	Z1066124X	DESARROLLO APLICACIONES WEB	Projecyo 2	No asignado aun	2026-05-04	Efren Marci	\N	t	f	f	f	Activo	carlos v	Ester Piscore	\N	{"fecha": "27/04/2026 09:18", "FPPYME": false, "estudios": null, "contratado": true, "programaFP": true, "tutorCentro": "carlos v", "lugarEstudios": null, "nombreEmpresa": null, "primerContacto": "Lo vamos a contratar, trabaja muy bien", "sigueEstudiando": false, "contratadoOtraEmpresa": false}	Sueca 89	VALENCIA	2026-2027	1ro
63	2026-05-04 13:58:48.139556+00	B98692361	63	73666906E	MARKETING Y PUBLICIDAD	No completado	campañas en CRM, documentación, Presentaciones de empresa, hojas de productos, etc	\N	\N	\N	\N	\N	\N	\N	Nuevo	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: feedback_forms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."feedback_forms" ("id", "created_at", "practica_id", "tipo_form", "token", "estado", "fecha_envio", "fecha_respuesta", "email_destino", "fecha_real_envio") FROM stdin;
1	2026-04-27 09:19:28.996712+00	62	feedback_inicial	c36609e33e7849458fd12bfa74706197	pendiente	2026-05-11	2026-04-28	antopiscio@gmail.com	2026-04-27T09:21:48.097Z
2	2026-04-27 09:19:29.182567+00	62	feedback_adaptacion	232f6e8465d24463baf495642a7eaf39	pendiente	2026-06-03	\N	antopiscio@gmail.com	\N
3	2026-04-27 09:19:29.366418+00	62	feedback_cierre	6b131c9b23dc46ce80f90a5505c998da	pendiente	2026-05-11	\N	antopiscio@gmail.com	\N
\.


--
-- Data for Name: feedback_respuestas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."feedback_respuestas" ("id", "created_at", "feedback_form_id", "practica_id", "respuestas_json") FROM stdin;
1	2026-04-28 12:33:43.031561+00	1	62	{"tipo": "feedback_inicial", "expectativas": {"alineado": "Sí", "aprender": ""}, "inicio_acogida": {"dudas": 3, "mejor": "asdads", "acogida": 3, "comodidad": 3, "funciones": 3}, "primeras_alertas": {"alertas": "No", "detalle_alerta": ""}}
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
-- Data for Name: gestores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."gestores" ("id", "created_at", "nombre", "activo", "email", "ciclo", "password") FROM stdin;
1	2026-04-27 08:17:53.844782+00	Ester Piscore	t	ester@yopmail.com	Desarrollo Aplicaciones Web	\N
\.


--
-- Data for Name: localidades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."localidades" ("id", "nombre", "provincia") FROM stdin;
1	ADEMUZ	VALENCIA
2	ADOR	VALENCIA
3	AGULLENT	VALENCIA
4	AIELO DE MALFERIT	VALENCIA
5	AIELO DE RUGAT	VALENCIA
6	ALAQUAS	VALENCIA
7	ALBAIDA	VALENCIA
8	ALBAL	VALENCIA
9	ALBALAT DE LA RIBERA	VALENCIA
10	ALBALAT DELS SORELLS	VALENCIA
11	ALBALAT DELS TARONGERS	VALENCIA
12	ALBERIC	VALENCIA
13	ALBORACHE	VALENCIA
14	ALBORAYA	VALENCIA
15	ALBUIXECH	VALENCIA
16	ALCANTERA DE XUQUER	VALENCIA
17	ALCASSER	VALENCIA
18	ALCUBLAS	VALENCIA
19	ALDAIA	VALENCIA
20	ALFAFAR	VALENCIA
21	ALFARA DE LA BARONIA	VALENCIA
22	ALFARA DEL PATRIARCA	VALENCIA
23	ALFAUIR	VALENCIA
24	ALGAR DE PALANCIA	VALENCIA
25	ALGEMESI	VALENCIA
26	ALGIMIA DE ALFARA	VALENCIA
27	ALGINET	VALENCIA
28	ALMASSERA	VALENCIA
29	ALMISERAT	VALENCIA
30	ALMOINES	VALENCIA
31	ALMUSSAFES	VALENCIA
32	ALPUENTE	VALENCIA
33	ALQUERIA DE LA COMTESSA	VALENCIA
34	ALZIRA	VALENCIA
35	ANDILLA	VALENCIA
36	ANNA	VALENCIA
37	ANTRELLA	VALENCIA
38	ARAS DE LOS OLMOS	VALENCIA
39	ATZENETA D'ALBAIDA	VALENCIA
40	AYORA	VALENCIA
41	BARX	VALENCIA
42	BARXETA	VALENCIA
43	BELGIDA	VALENCIA
44	BELLREGUARD	VALENCIA
45	BELLUS	VALENCIA
46	BENAGEBER	VALENCIA
47	BENAGUASIL	VALENCIA
48	BENAVITES	VALENCIA
49	BENEIXIDA	VALENCIA
50	BENETUSSER	VALENCIA
51	BENIARJO	VALENCIA
52	BENIATJAR	VALENCIA
53	BENICOLET	VALENCIA
54	BENICULL DE XUQUER	VALENCIA
55	BENEIFAIO	VALENCIA
56	BENEIFLA	VALENCIA
57	BENIGÁNIM	VALENCIA
58	BENIMODO	VALENCIA
59	BENIMUSLEM	VALENCIA
60	BENIPARRELL	VALENCIA
61	BENIRREDRA	VALENCIA
62	BENISANO	VALENCIA
63	BENISSERO	VALENCIA
64	BENISSUERA	VALENCIA
65	BETERA	VALENCIA
66	BICORP	VALENCIA
67	BOCAIRENT	VALENCIA
68	BOLBAITE	VALENCIA
69	BONREPOS I MIRAMBELL	VALENCIA
70	BUFALI	VALENCIA
71	BUGARRA	VALENCIA
72	BUNYOL	VALENCIA
73	BURJASSOT	VALENCIA
74	CALLES	VALENCIA
75	CAMPORROBLES	VALENCIA
76	CANALS	VALENCIA
77	CANET D'EN BERENGUER	VALENCIA
78	CARCAIXENT	VALENCIA
79	CARCER	VALENCIA
80	CARLET	VALENCIA
81	CARRICOLA	VALENCIA
82	CASAS BAJAS	VALENCIA
83	CASAS ALTAS	VALENCIA
84	CASINOS	VALENCIA
85	CASTELLO DE RUGAT	VALENCIA
86	CASTELLO	VALENCIA
87	CASTELLONET DE LA CONQUESTA	VALENCIA
88	CASTIELFABIB	VALENCIA
89	CATADAU	VALENCIA
90	CATARROJA	VALENCIA
91	CAUDETE DE LAS FUENTES	VALENCIA
92	CERDA	VALENCIA
93	CHELLA	VALENCIA
94	CHELVA	VALENCIA
95	CHERA	VALENCIA
96	CHESTE	VALENCIA
97	CHIVA	VALENCIA
98	CHULILLA	VALENCIA
99	COFRENTES	VALENCIA
100	CORBERA	VALENCIA
101	CORTES DE PALLAS	VALENCIA
102	COTES	VALENCIA
103	CULLERA	VALENCIA
104	DAIMUS	VALENCIA
105	DOMEÑO	VALENCIA
106	DOS AGUAS	VALENCIA
107	ELIANA, L'	VALENCIA
108	EMPERADOR	VALENCIA
109	ENGUERA	VALENCIA
110	ENOVA, L'	VALENCIA
111	ESTIVELLA	VALENCIA
112	ESTUBENY	VALENCIA
113	FAURA	VALENCIA
114	FAVARA	VALENCIA
115	FONT DE LA FIGUERA, LA	VALENCIA
116	FONT D'EN CARROS, LA	VALENCIA
117	FONTANARS DELS ALFORINS	VALENCIA
118	FORTALENY	VALENCIA
119	FOIOS	VALENCIA
120	GANDIA	VALENCIA
121	GATOVA	VALENCIA
122	GAVARDA	VALENCIA
123	GENOVES	VALENCIA
124	GESTALGAR	VALENCIA
125	GILET	VALENCIA
126	GODELLA	VALENCIA
127	GODELLETA	VALENCIA
128	GUADASSUAR	VALENCIA
129	GUADASEQUIES	VALENCIA
130	HIGUERUELAS	VALENCIA
131	JALANCE	VALENCIA
132	XERACO	VALENCIA
133	XERESA	VALENCIA
134	XATIVA	VALENCIA
135	JARAFUEL	VALENCIA
136	LLANERA DE RANES	VALENCIA
137	LLAURI	VALENCIA
138	LLIRIA	VALENCIA
139	LLORCA	VALENCIA
140	LLOMBAI	VALENCIA
141	LLOSA DE RANES, LA	VALENCIA
142	LLUTXENT	VALENCIA
143	LORIGUILLA	VALENCIA
144	LOSA DEL OBISPO	VALENCIA
145	MACASTRE	VALENCIA
146	MANISES	VALENCIA
147	MANUEL	VALENCIA
148	MARINES	VALENCIA
149	MASSALAVÉS	VALENCIA
150	MASSALFASSAR	VALENCIA
151	MASSAMAGRELL	VALENCIA
152	MASSANASSA	VALENCIA
153	MELIANA	VALENCIA
154	MILLARES	VALENCIA
155	MIRAMAR	VALENCIA
156	MISLATA	VALENCIA
157	MOGENTE	VALENCIA
158	MONCADA	VALENCIA
159	MONTSERRAT	VALENCIA
160	MONTAVERNER	VALENCIA
161	MONTESA	VALENCIA
162	MONTITXELVO	VALENCIA
163	MONTROY	VALENCIA
164	MUSEROS	VALENCIA
165	NAQUERA	VALENCIA
166	NAVARRES	VALENCIA
167	NOVELE	VALENCIA
168	OLIVA	VALENCIA
169	OLLERIA, L'	VALENCIA
170	OLOCAU	VALENCIA
171	ONTINYENT	VALENCIA
172	OTOS	VALENCIA
173	PAIPORTA	VALENCIA
174	PALMA DE GANDIA	VALENCIA
175	PALMERA	VALENCIA
176	PALOMAR, EL	VALENCIA
177	PATERNA	VALENCIA
178	PEDRALBA	VALENCIA
179	PETRES	VALENCIA
180	PICANIA	VALENCIA
181	PICASSENT	VALENCIA
182	PILES	VALENCIA
183	PINET	VALENCIA
184	POLINYA DE XUQUER	VALENCIA
185	POTRIES	VALENCIA
186	POBLA DE FARNALS, LA	VALENCIA
187	POBLA DE VALLBONA, LA	VALENCIA
188	POBLA DEL DUC, LA	VALENCIA
189	POBLA LLARGA, LA	VALENCIA
190	QUART DE POBLET	VALENCIA
191	QUART DE LES VALLS	VALENCIA
192	QUARTELL	VALENCIA
193	QUATRETONDA	VALENCIA
194	QUESA	VALENCIA
195	RAFELBUÑOL	VALENCIA
196	RAFELCOFER	VALENCIA
197	RAFELGUARAF	VALENCIA
198	RAFOL DE SALEM	VALENCIA
199	REAL	VALENCIA
200	REAL DE GANDIA	VALENCIA
201	REQUENA	VALENCIA
202	RIBA-ROJA DE TÚRIA	VALENCIA
203	RIOLA	VALENCIA
204	ROCAFORT	VALENCIA
205	ROTGLA I CORBERA	VALENCIA
206	ROTOVA	VALENCIA
207	SAGUNT	VALENCIA
208	SALEM	VALENCIA
209	SAN ANTONIO DE BENAGEBER	VALENCIA
210	SANT JOANET	VALENCIA
211	SEDAVI	VALENCIA
212	SEGART	VALENCIA
213	SELLERI	VALENCIA
214	SEMPERE	VALENCIA
215	SENYERA	VALENCIA
216	SERRA	VALENCIA
217	SIETE AGUAS	VALENCIA
218	SILLA	VALENCIA
219	SIMAT DE LA VALLLDIGNA	VALENCIA
220	SOT DE CHERA	VALENCIA
221	SUECA	VALENCIA
222	SUMACARCER	VALENCIA
223	TAVERNES DE LA VALLDIGNA	VALENCIA
224	TAVERNES BLANQUES	VALENCIA
225	TERESA DE COFRENTES	VALENCIA
226	TERRATEIG	VALENCIA
227	TITAGUAS	VALENCIA
228	TORREBAJA	VALENCIA
229	TORRELLA	VALENCIA
230	TORRENT	VALENCIA
231	TORRES TORRES	VALENCIA
232	TOUS	VALENCIA
233	TUEJAR	VALENCIA
234	TURIS	VALENCIA
235	UTIEL	VALENCIA
236	VALENCIA	VALENCIA
237	VALLADA	VALENCIA
238	VALLES	VALENCIA
239	VENTA DEL MORO	VALENCIA
240	VILAMARXANT	VALENCIA
241	VILLALONGA	VALENCIA
242	VILLAR DEL ARZOBISPO	VALENCIA
243	VILLARGORDO DEL CABRIEL	VALENCIA
244	VINALESA	VALENCIA
245	YATOVA	VALENCIA
246	LA YESA	VALENCIA
247	ZARRA	VALENCIA
248	ALCANTERA DE XUQUER	VALENCIA
249	BENICULL DE XUQUER	VALENCIA
250	EL PALMAR	VALENCIA
251	EL PERELLONET	VALENCIA
252	EL SALER	VALENCIA
253	MARENY DE BARRAQUETES	VALENCIA
254	PINEDO	VALENCIA
255	EL PERELLO	VALENCIA
256	EL BALCON DE MONTROY	VALENCIA
257	CALICANTO	VALENCIA
258	LA REVA	VALENCIA
259	ENTREPINOS	VALENCIA
260	MONTEALCEDO	VALENCIA
261	SAN RAFAEL	VALENCIA
262	MARINES NUEVO	VALENCIA
263	CUMBRES DE CALICANTO	VALENCIA
264	MASIA DE TRAVER	VALENCIA
265	SOTOLIVAR	VALENCIA
\.


--
-- Data for Name: practica_estados; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."practica_estados" ("id", "created_at", "practicaId", "documentacion_pedida", "documentacion_firmada", "en_progreso", "cancelada", "finalizada") FROM stdin;
10	2026-04-27 09:11:34.915168+00	62	2026-04-27	2026-05-04	2026-05-04	\N	\N
16	2026-05-04 13:58:48.354691+00	63	\N	\N	\N	\N	\N
\.


--
-- Data for Name: practicas_canceladas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."practicas_canceladas" ("id", "created_at", "alumno", "empresa", "ciclo", "motivo", "anio", "curso", "tutor_centro", "tutor", "area", "gestor", "feedback", "fecha_inicio", "feedbackEmpresa") FROM stdin;
\.


--
-- Data for Name: tutor_centro; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."tutor_centro" ("id", "created_at", "nombre", "email", "telefono") FROM stdin;
1	2026-04-27 08:25:44.627096+00	carlos v	carlos@yopmail.com	2332323
\.


--
-- Data for Name: tutores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."tutores" ("id", "created_at", "nombre", "nif", "email", "telefono", "cif_empresa", "oferta") FROM stdin;
30	2025-11-17 12:23:58.00831+00	Onofre Jesús Espinós Andrés	48580700P	onofre.espinos@aquaservice.com	+34619972616	A41810920	\N
5	2025-10-27 12:33:31.069207+00	RAFAEL LLUESMA GIL	20004251R	rafa@vialcobus.com	961230673	B46001632	\N
6	2025-10-27 12:41:54.957255+00	Óscar Colomina Fernández	23324155Q	info@plan-moves.com	627024604	B56966534	\N
7	2025-10-27 12:49:25.055724+00	Eva García Zahino	48305516L	eva.garcia@cwcomunicacion.com	652899878	B98638596	\N
59	2026-04-27 08:16:24.194268+00	Efren Marci	32442332	efren@yopmail.com	23232323	B2244933	\N
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
31	2025-11-18 12:11:39.475009+00	CLARA MONDRAGÓN ARNAL	45803159Q	gestion@audioprobe.es	961105782	B98079916	\N
33	2025-11-19 12:41:39.257745+00	FERNANDO DE ZARATE	53050796P	adesco@dynamizatic.com	960624308	B98692361	\N
34	2025-11-24 14:53:56.344166+00	Johnatan Pirez Beguiristain	60521649R	johnatan.pirez@grupospag.com	605405626	B03418548	\N
35	2025-11-25 09:15:25.721308+00	Noemi Oñiga Hernández	44870162Z	grupolukinos@clinicaapunto.com	656677010	B09958802	\N
36	2025-11-25 10:20:00.046746+00	GIANMARCO ROSATI	Y7642051Q	gianmarco.rosati@metro-ito.com	673 22 48 92	B85205623	\N
37	2025-11-25 12:42:52.48148+00	ARANTXA GARMENDIA BARBA	53237262J	agarmendia@point1920.com	690065874	B03129236	\N
38	2025-11-25 14:10:27.38743+00	FRANCISCO MILLA IBOR	52648438N	info@eruga.es	960217474	B98203581	\N
60	2026-05-04 13:41:12.003869+00	ANTONELA	7657657657	formacion@data-so.com	765765765	45566434567	\N
39	2025-11-26 11:15:12.593767+00	TATIANA GÓMEZ CASARES	27374374G	tatiana@nippycreative.com	682384762	B06817936	\N
42	2025-11-26 11:27:38.573952+00	GEMMA PORTA MORENO	23824123X	gemma.porta@suvima.com	607506193	A46199873	\N
43	2025-11-28 10:41:08.713043+00	Noelia Martínez Jurado	53256396B	nmartinez@romeu.com	963179461	A08536583	\N
44	2025-11-28 12:10:24.82848+00	Celia Arnau García	48382387R	tecnico@laboratorioseyco.com	689128651	B98776875	\N
45	2025-11-28 13:01:59.94912+00	no designado	000000	\N	\N	B98598329	\N
46	2025-12-01 07:38:15.034999+00	Carmen Benavent	52715805N	cbenavent@femeval.es	963719761	G46102539	\N
47	2025-12-01 08:21:36.239755+00	ALEJANDRA SANTOS ORTIZ	48588148G	contabilidad@cabolisan.com	689343265	B98495443	\N
48	2025-12-01 12:45:07.013466+00	Manuel Voldman Benarroch	26763099T	mvoldman@sounddepot.net	605286207	B97639421	\N
49	2025-12-02 10:58:05.898375+00	ANA MARTINEZ MARTINEZ	48389682M	ana.martinez@delgo.es	602226765	B97900864	\N
50	2025-12-02 15:20:05.749927+00	Mariana López	48342630B	malopez@roi-up.es	+34 611 93 43 16	B86101995	\N
51	2025-12-04 10:46:03.829142+00	Luna Celeste Ferrer Escandell	47430111V	s.parlatore@agroturn.nl	644610481	B42753012	\N
52	2025-12-04 11:21:37.409967+00	Ramona Bucur	X8923330C	internationalmanager@mediterranoculinary.com	687921366	B02723625	\N
53	2025-12-05 09:19:11.262397+00	DAVID MARCO SALVADOR	44500177F	administracion@worldbrands.es	961826179	B98715402	\N
54	2025-12-10 10:03:19.395905+00	Juan Carlos Rodríguez	B22456701	juan@nexosmart.es	646694442	B22456701	\N
29	2025-11-17 11:55:57.072722+00	EA	52725545T	administracion@eaguadalaviar.es	963182112	B96882022	\N
56	2026-01-19 15:36:29.403978+00	Juan Peña Ibáñez	34820033B	juan@orbitaleos.com	619448352	B40593055	\N
57	2026-01-21 08:46:02.206352+00	David Bartual Marco	29184592F	david.bartual@saymarsl.es	647447567	B98707565	\N
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."usuarios" ("id", "created_at", "email", "password", "rol") FROM stdin;
1	2025-09-24 13:08:28.062791+00	admin	admin	admin
2	2025-10-20 10:02:26.5861+00	avicente@campuscamarafp.com	avicente123!	admin
3	2026-04-27 08:16:24.812963+00	B2244933	B2244933	empresa
4	2026-04-27 08:17:54.074158+00	ester@yopmail.com	EsterPiscore2026	gestor
5	2026-04-27 08:25:44.725478+00	carlos@yopmail.com	carlosv2026	tutorCentro
6	2026-05-04 13:41:12.615417+00	45566434567	45566434567	empresa
\.


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."buckets" ("id", "name", "owner", "created_at", "updated_at", "public", "avif_autodetection", "file_size_limit", "allowed_mime_types", "owner_id", "type") FROM stdin;
\.


--
-- Data for Name: buckets_analytics; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."buckets_analytics" ("name", "type", "format", "created_at", "updated_at", "id", "deleted_at") FROM stdin;
\.


--
-- Data for Name: buckets_vectors; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."buckets_vectors" ("id", "type", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."objects" ("id", "bucket_id", "name", "owner", "created_at", "updated_at", "last_accessed_at", "metadata", "version", "owner_id", "user_metadata") FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."s3_multipart_uploads" ("id", "in_progress_size", "upload_signature", "bucket_id", "key", "version", "owner_id", "created_at", "user_metadata", "metadata") FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."s3_multipart_uploads_parts" ("id", "upload_id", "size", "part_number", "bucket_id", "key", "etag", "owner_id", "version", "created_at") FROM stdin;
\.


--
-- Data for Name: vector_indexes; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."vector_indexes" ("id", "name", "bucket_id", "data_type", "dimension", "distance_metric", "metadata_configuration", "created_at", "updated_at") FROM stdin;
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 1, false);


--
-- Name: alumno_estados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."alumno_estados_id_seq"', 437, true);


--
-- Name: alumnos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."alumnos_id_seq"', 233, true);


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

SELECT pg_catalog.setval('"public"."empresa_estados_id_seq"', 140, true);


--
-- Name: empresa_practica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."empresa_practica_id_seq"', 90, true);


--
-- Name: empresas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."empresas_id_seq"', 105, true);


--
-- Name: error_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."error_logs_id_seq"', 1, false);


--
-- Name: feedback_forms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."feedback_forms_id_seq"', 3, true);


--
-- Name: feedback_respuestas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."feedback_respuestas_id_seq"', 1, true);


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
-- Name: gestores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."gestores_id_seq"', 1, true);


--
-- Name: practica_estados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."practica_estados_id_seq"', 16, true);


--
-- Name: practicas_canceladas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."practicas_canceladas_id_seq"', 1, false);


--
-- Name: practicas_fp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."practicas_fp_id_seq"', 63, true);


--
-- Name: tutor_centro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."tutor_centro_id_seq"', 1, true);


--
-- Name: tutores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."tutores_id_seq"', 60, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."usuarios_id_seq"', 6, true);


--
-- PostgreSQL database dump complete
--

-- \unrestrict IJuSkiCM8gvi6byRYbbknXJx0mZ5TtHIQlXaiDEdy97kBdJsyqQmGnzrSFe9lva

RESET ALL;
