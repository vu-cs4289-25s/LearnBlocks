--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

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
-- Name: course_permission; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.course_permission AS ENUM (
    'public',
    'private'
);


--
-- Name: course_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.course_status AS ENUM (
    'active',
    'archived'
);


--
-- Name: module_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.module_status AS ENUM (
    'locked',
    'in_progress',
    'completed'
);


--
-- Name: roster_role; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.roster_role AS ENUM (
    'owner',
    'participant'
);


--
-- Name: task_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.task_status AS ENUM (
    'assigned',
    'in_progress',
    'completed',
    'late'
);


--
-- Name: user_role; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.user_role AS ENUM (
    'admin',
    'student',
    'teacher'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: badge; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.badge (
    badge_id integer NOT NULL,
    badge_name character varying(50) NOT NULL,
    badge_description text NOT NULL,
    s3_url text NOT NULL
);


--
-- Name: badge_badge_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.badge_badge_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: badge_badge_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.badge_badge_id_seq OWNED BY public.badge.badge_id;


--
-- Name: class; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.class (
    class_id integer NOT NULL,
    class_name character varying(255) NOT NULL,
    class_code character varying(20) NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: class_class_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.class_class_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: class_class_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.class_class_id_seq OWNED BY public.class.class_id;


--
-- Name: class_module_assignment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.class_module_assignment (
    assignment_id integer NOT NULL,
    class_id integer,
    module_id integer,
    assigned_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    due_date date NOT NULL
);


--
-- Name: class_module_assignment_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.class_module_assignment_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: class_module_assignment_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.class_module_assignment_assignment_id_seq OWNED BY public.class_module_assignment.assignment_id;


--
-- Name: course; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.course (
    course_id integer NOT NULL,
    course_name character varying(255) NOT NULL,
    status public.course_status DEFAULT 'active'::public.course_status,
    badge_id integer,
    owner_id integer,
    permission public.course_permission DEFAULT 'public'::public.course_permission
);


--
-- Name: course_class_mapping; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.course_class_mapping (
    course_id integer NOT NULL,
    class_id integer NOT NULL,
    assigned_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: course_course_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.course_course_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: course_course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.course_course_id_seq OWNED BY public.course.course_id;


--
-- Name: module; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.module (
    module_id integer NOT NULL,
    module_name character varying(255) NOT NULL,
    status public.module_status DEFAULT 'locked'::public.module_status,
    owner_id integer
);


--
-- Name: module_course_mapping; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.module_course_mapping (
    course_id integer NOT NULL,
    module_id integer NOT NULL,
    module_order integer NOT NULL
);


--
-- Name: module_module_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.module_module_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: module_module_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.module_module_id_seq OWNED BY public.module.module_id;


--
-- Name: project; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.project (
    project_id integer NOT NULL,
    user_id integer,
    project_name character varying(100) NOT NULL,
    module_id integer,
    s3_url text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    last_modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: project_project_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.project_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: project_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.project_project_id_seq OWNED BY public.project.project_id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    user_id integer NOT NULL,
    role public.user_role DEFAULT 'student'::public.user_role NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    week_activity bit(7) DEFAULT '0000000'::"bit"
);


--
-- Name: user_badge_achievement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_badge_achievement (
    achievement_id integer NOT NULL,
    badge_id integer,
    user_id integer,
    earned_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: user_badge_achievement_achievement_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_badge_achievement_achievement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_badge_achievement_achievement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_badge_achievement_achievement_id_seq OWNED BY public.user_badge_achievement.achievement_id;


--
-- Name: user_class_roster; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_class_roster (
    user_id integer NOT NULL,
    class_id integer NOT NULL,
    role public.roster_role NOT NULL,
    enrollment_date date DEFAULT CURRENT_DATE
);


--
-- Name: user_course_enrollment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_course_enrollment (
    course_id integer NOT NULL,
    user_id integer NOT NULL,
    role public.roster_role NOT NULL
);


--
-- Name: user_module_progress; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_module_progress (
    progress_id integer NOT NULL,
    user_id integer,
    module_id integer,
    status public.module_status DEFAULT 'locked'::public.module_status,
    completion_date timestamp without time zone
);


--
-- Name: user_module_progress_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_module_progress_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_module_progress_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_module_progress_progress_id_seq OWNED BY public.user_module_progress.progress_id;


--
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_user_id_seq OWNED BY public."user".user_id;


--
-- Name: badge badge_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badge ALTER COLUMN badge_id SET DEFAULT nextval('public.badge_badge_id_seq'::regclass);


--
-- Name: class class_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.class ALTER COLUMN class_id SET DEFAULT nextval('public.class_class_id_seq'::regclass);


--
-- Name: class_module_assignment assignment_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.class_module_assignment ALTER COLUMN assignment_id SET DEFAULT nextval('public.class_module_assignment_assignment_id_seq'::regclass);


--
-- Name: course course_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course ALTER COLUMN course_id SET DEFAULT nextval('public.course_course_id_seq'::regclass);


--
-- Name: module module_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module ALTER COLUMN module_id SET DEFAULT nextval('public.module_module_id_seq'::regclass);


--
-- Name: project project_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project ALTER COLUMN project_id SET DEFAULT nextval('public.project_project_id_seq'::regclass);


--
-- Name: user user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user" ALTER COLUMN user_id SET DEFAULT nextval('public.user_user_id_seq'::regclass);


--
-- Name: user_badge_achievement achievement_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_badge_achievement ALTER COLUMN achievement_id SET DEFAULT nextval('public.user_badge_achievement_achievement_id_seq'::regclass);


--
-- Name: user_module_progress progress_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_module_progress ALTER COLUMN progress_id SET DEFAULT nextval('public.user_module_progress_progress_id_seq'::regclass);


--
-- Name: badge badge_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badge
    ADD CONSTRAINT badge_pkey PRIMARY KEY (badge_id);


--
-- Name: class class_class_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.class
    ADD CONSTRAINT class_class_code_key UNIQUE (class_code);


--
-- Name: class_module_assignment class_module_assignment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.class_module_assignment
    ADD CONSTRAINT class_module_assignment_pkey PRIMARY KEY (assignment_id);


--
-- Name: class class_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.class
    ADD CONSTRAINT class_pkey PRIMARY KEY (class_id);


--
-- Name: course_class_mapping course_class_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_class_mapping
    ADD CONSTRAINT course_class_mapping_pkey PRIMARY KEY (course_id, class_id);


--
-- Name: course course_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_pkey PRIMARY KEY (course_id);


--
-- Name: module_course_mapping module_course_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_course_mapping
    ADD CONSTRAINT module_course_mapping_pkey PRIMARY KEY (course_id, module_id);


--
-- Name: module module_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module
    ADD CONSTRAINT module_pkey PRIMARY KEY (module_id);


--
-- Name: project project_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (project_id);


--
-- Name: user_badge_achievement user_badge_achievement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_badge_achievement
    ADD CONSTRAINT user_badge_achievement_pkey PRIMARY KEY (achievement_id);


--
-- Name: user_class_roster user_class_roster_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_class_roster
    ADD CONSTRAINT user_class_roster_pkey PRIMARY KEY (user_id, class_id);


--
-- Name: user_course_enrollment user_course_enrollment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_course_enrollment
    ADD CONSTRAINT user_course_enrollment_pkey PRIMARY KEY (user_id, course_id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user_module_progress user_module_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_module_progress
    ADD CONSTRAINT user_module_progress_pkey PRIMARY KEY (progress_id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: class_module_assignment fk_assignment_class; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.class_module_assignment
    ADD CONSTRAINT fk_assignment_class FOREIGN KEY (class_id) REFERENCES public.class(class_id);


--
-- Name: class_module_assignment fk_assignment_module; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.class_module_assignment
    ADD CONSTRAINT fk_assignment_module FOREIGN KEY (module_id) REFERENCES public.module(module_id);


--
-- Name: user_badge_achievement fk_badge_achievement_badge; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_badge_achievement
    ADD CONSTRAINT fk_badge_achievement_badge FOREIGN KEY (badge_id) REFERENCES public.badge(badge_id);


--
-- Name: user_badge_achievement fk_badge_achievement_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_badge_achievement
    ADD CONSTRAINT fk_badge_achievement_user FOREIGN KEY (user_id) REFERENCES public."user"(user_id);


--
-- Name: course fk_course_badge; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT fk_course_badge FOREIGN KEY (badge_id) REFERENCES public.badge(badge_id);


--
-- Name: course_class_mapping fk_course_class_class; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_class_mapping
    ADD CONSTRAINT fk_course_class_class FOREIGN KEY (class_id) REFERENCES public.class(class_id);


--
-- Name: course_class_mapping fk_course_class_course; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_class_mapping
    ADD CONSTRAINT fk_course_class_course FOREIGN KEY (course_id) REFERENCES public.course(course_id);


--
-- Name: course fk_course_owner; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT fk_course_owner FOREIGN KEY (owner_id) REFERENCES public."user"(user_id);


--
-- Name: user_course_enrollment fk_enrollment_course; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_course_enrollment
    ADD CONSTRAINT fk_enrollment_course FOREIGN KEY (course_id) REFERENCES public.course(course_id);


--
-- Name: user_course_enrollment fk_enrollment_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_course_enrollment
    ADD CONSTRAINT fk_enrollment_user FOREIGN KEY (user_id) REFERENCES public."user"(user_id);


--
-- Name: module_course_mapping fk_module_course_course; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_course_mapping
    ADD CONSTRAINT fk_module_course_course FOREIGN KEY (course_id) REFERENCES public.course(course_id);


--
-- Name: module_course_mapping fk_module_course_module; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_course_mapping
    ADD CONSTRAINT fk_module_course_module FOREIGN KEY (module_id) REFERENCES public.module(module_id);


--
-- Name: module fk_module_owner; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module
    ADD CONSTRAINT fk_module_owner FOREIGN KEY (owner_id) REFERENCES public."user"(user_id);


--
-- Name: user_module_progress fk_progress_module; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_module_progress
    ADD CONSTRAINT fk_progress_module FOREIGN KEY (module_id) REFERENCES public.module(module_id);


--
-- Name: user_module_progress fk_progress_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_module_progress
    ADD CONSTRAINT fk_progress_user FOREIGN KEY (user_id) REFERENCES public."user"(user_id);


--
-- Name: project fk_project_module; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT fk_project_module FOREIGN KEY (module_id) REFERENCES public.module(module_id);


--
-- Name: project fk_project_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT fk_project_user FOREIGN KEY (user_id) REFERENCES public."user"(user_id);


--
-- Name: user_class_roster fk_roster_class; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_class_roster
    ADD CONSTRAINT fk_roster_class FOREIGN KEY (class_id) REFERENCES public.class(class_id);


--
-- Name: user_class_roster fk_roster_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_class_roster
    ADD CONSTRAINT fk_roster_user FOREIGN KEY (user_id) REFERENCES public."user"(user_id);


--
-- PostgreSQL database dump complete
--

