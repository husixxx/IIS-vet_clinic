--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Debian 17.0-1.pgdg120+1)
-- Dumped by pg_dump version 17.0 (Ubuntu 17.0-1.pgdg22.04+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: animals; Type: TABLE; Schema: public; Owner: husic
--

CREATE TABLE public.animals (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    species character varying(50) NOT NULL,
    age integer,
    photos text,
    history text,
    status character varying(50),
    caretaker_id integer
);


ALTER TABLE public.animals OWNER TO husic;

--
-- Name: animals_id_seq; Type: SEQUENCE; Schema: public; Owner: husic
--

CREATE SEQUENCE public.animals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animals_id_seq OWNER TO husic;

--
-- Name: animals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: husic
--

ALTER SEQUENCE public.animals_id_seq OWNED BY public.animals.id;


--
-- Name: caretakers; Type: TABLE; Schema: public; Owner: husic
--

CREATE TABLE public.caretakers (
    id integer NOT NULL
);


ALTER TABLE public.caretakers OWNER TO husic;

--
-- Name: medical_records; Type: TABLE; Schema: public; Owner: husic
--

CREATE TABLE public.medical_records (
    id integer NOT NULL,
    animal_id integer NOT NULL,
    examination_date date,
    veterinarian_id integer NOT NULL,
    examination_type character varying(50),
    description text
);


ALTER TABLE public.medical_records OWNER TO husic;

--
-- Name: medical_records_id_seq; Type: SEQUENCE; Schema: public; Owner: husic
--

CREATE SEQUENCE public.medical_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.medical_records_id_seq OWNER TO husic;

--
-- Name: medical_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: husic
--

ALTER SEQUENCE public.medical_records_id_seq OWNED BY public.medical_records.id;


--
-- Name: persons; Type: TABLE; Schema: public; Owner: husic
--

CREATE TABLE public.persons (
    id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    email character varying(120) NOT NULL,
    phone character varying(20)
);


ALTER TABLE public.persons OWNER TO husic;

--
-- Name: persons_id_seq; Type: SEQUENCE; Schema: public; Owner: husic
--

CREATE SEQUENCE public.persons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.persons_id_seq OWNER TO husic;

--
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: husic
--

ALTER SEQUENCE public.persons_id_seq OWNED BY public.persons.id;


--
-- Name: veterinarians; Type: TABLE; Schema: public; Owner: husic
--

CREATE TABLE public.veterinarians (
    id integer NOT NULL
);


ALTER TABLE public.veterinarians OWNER TO husic;

--
-- Name: volunteers; Type: TABLE; Schema: public; Owner: husic
--

CREATE TABLE public.volunteers (
    id integer NOT NULL,
    is_verified boolean
);


ALTER TABLE public.volunteers OWNER TO husic;

--
-- Name: walking_schedules; Type: TABLE; Schema: public; Owner: husic
--

CREATE TABLE public.walking_schedules (
    id integer NOT NULL,
    animal_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    volunteer_id integer NOT NULL,
    status character varying(20)
);


ALTER TABLE public.walking_schedules OWNER TO husic;

--
-- Name: walking_schedules_id_seq; Type: SEQUENCE; Schema: public; Owner: husic
--

CREATE SEQUENCE public.walking_schedules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.walking_schedules_id_seq OWNER TO husic;

--
-- Name: walking_schedules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: husic
--

ALTER SEQUENCE public.walking_schedules_id_seq OWNED BY public.walking_schedules.id;


--
-- Name: animals id; Type: DEFAULT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.animals ALTER COLUMN id SET DEFAULT nextval('public.animals_id_seq'::regclass);


--
-- Name: medical_records id; Type: DEFAULT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.medical_records ALTER COLUMN id SET DEFAULT nextval('public.medical_records_id_seq'::regclass);


--
-- Name: persons id; Type: DEFAULT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.persons ALTER COLUMN id SET DEFAULT nextval('public.persons_id_seq'::regclass);


--
-- Name: walking_schedules id; Type: DEFAULT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.walking_schedules ALTER COLUMN id SET DEFAULT nextval('public.walking_schedules_id_seq'::regclass);


--
-- Data for Name: animals; Type: TABLE DATA; Schema: public; Owner: husic
--

COPY public.animals (id, name, species, age, photos, history, status, caretaker_id) FROM stdin;
\.


--
-- Data for Name: caretakers; Type: TABLE DATA; Schema: public; Owner: husic
--

COPY public.caretakers (id) FROM stdin;
\.


--
-- Data for Name: medical_records; Type: TABLE DATA; Schema: public; Owner: husic
--

COPY public.medical_records (id, animal_id, examination_date, veterinarian_id, examination_type, description) FROM stdin;
\.


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: husic
--

COPY public.persons (id, first_name, last_name, email, phone) FROM stdin;
\.


--
-- Data for Name: veterinarians; Type: TABLE DATA; Schema: public; Owner: husic
--

COPY public.veterinarians (id) FROM stdin;
\.


--
-- Data for Name: volunteers; Type: TABLE DATA; Schema: public; Owner: husic
--

COPY public.volunteers (id, is_verified) FROM stdin;
\.


--
-- Data for Name: walking_schedules; Type: TABLE DATA; Schema: public; Owner: husic
--

COPY public.walking_schedules (id, animal_id, start_time, end_time, volunteer_id, status) FROM stdin;
\.


--
-- Name: animals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: husic
--

SELECT pg_catalog.setval('public.animals_id_seq', 1, false);


--
-- Name: medical_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: husic
--

SELECT pg_catalog.setval('public.medical_records_id_seq', 1, false);


--
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: husic
--

SELECT pg_catalog.setval('public.persons_id_seq', 1, false);


--
-- Name: walking_schedules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: husic
--

SELECT pg_catalog.setval('public.walking_schedules_id_seq', 1, false);


--
-- Name: animals animals_pkey; Type: CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.animals
    ADD CONSTRAINT animals_pkey PRIMARY KEY (id);


--
-- Name: caretakers caretakers_pkey; Type: CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.caretakers
    ADD CONSTRAINT caretakers_pkey PRIMARY KEY (id);


--
-- Name: medical_records medical_records_pkey; Type: CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.medical_records
    ADD CONSTRAINT medical_records_pkey PRIMARY KEY (id);


--
-- Name: persons persons_email_key; Type: CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_email_key UNIQUE (email);


--
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- Name: veterinarians veterinarians_pkey; Type: CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.veterinarians
    ADD CONSTRAINT veterinarians_pkey PRIMARY KEY (id);


--
-- Name: volunteers volunteers_pkey; Type: CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.volunteers
    ADD CONSTRAINT volunteers_pkey PRIMARY KEY (id);


--
-- Name: walking_schedules walking_schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.walking_schedules
    ADD CONSTRAINT walking_schedules_pkey PRIMARY KEY (id);


--
-- Name: animals animals_caretaker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.animals
    ADD CONSTRAINT animals_caretaker_id_fkey FOREIGN KEY (caretaker_id) REFERENCES public.caretakers(id);


--
-- Name: caretakers caretakers_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.caretakers
    ADD CONSTRAINT caretakers_id_fkey FOREIGN KEY (id) REFERENCES public.persons(id);


--
-- Name: medical_records medical_records_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.medical_records
    ADD CONSTRAINT medical_records_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animals(id);


--
-- Name: medical_records medical_records_veterinarian_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.medical_records
    ADD CONSTRAINT medical_records_veterinarian_id_fkey FOREIGN KEY (veterinarian_id) REFERENCES public.veterinarians(id);


--
-- Name: veterinarians veterinarians_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.veterinarians
    ADD CONSTRAINT veterinarians_id_fkey FOREIGN KEY (id) REFERENCES public.persons(id);


--
-- Name: volunteers volunteers_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.volunteers
    ADD CONSTRAINT volunteers_id_fkey FOREIGN KEY (id) REFERENCES public.persons(id);


--
-- Name: walking_schedules walking_schedules_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.walking_schedules
    ADD CONSTRAINT walking_schedules_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animals(id);


--
-- Name: walking_schedules walking_schedules_volunteer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: husic
--

ALTER TABLE ONLY public.walking_schedules
    ADD CONSTRAINT walking_schedules_volunteer_id_fkey FOREIGN KEY (volunteer_id) REFERENCES public.volunteers(id);


--
-- PostgreSQL database dump complete
--

