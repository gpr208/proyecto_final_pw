--
-- PostgreSQL database dump
--

\restrict gOC8QJzCYvNPebKFSRwulKksKQReFq6pz9ZqadZemmej9GbTa49ylMfP9tZn8h9

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-11-17 11:54:50

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
-- TOC entry 220 (class 1259 OID 17532)
-- Name: categorias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categorias (
    categoria_id integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion text
);


ALTER TABLE public.categorias OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17531)
-- Name: categorias_categoria_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categorias_categoria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categorias_categoria_id_seq OWNER TO postgres;

--
-- TOC entry 5060 (class 0 OID 0)
-- Dependencies: 219
-- Name: categorias_categoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categorias_categoria_id_seq OWNED BY public.categorias.categoria_id;


--
-- TOC entry 228 (class 1259 OID 17585)
-- Name: detalles_orden; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.detalles_orden (
    detalle_id integer NOT NULL,
    orden_id integer,
    producto_id integer,
    cantidad integer NOT NULL,
    precio_unitario numeric(10,2) NOT NULL
);


ALTER TABLE public.detalles_orden OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17584)
-- Name: detalles_orden_detalle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.detalles_orden_detalle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.detalles_orden_detalle_id_seq OWNER TO postgres;

--
-- TOC entry 5061 (class 0 OID 0)
-- Dependencies: 227
-- Name: detalles_orden_detalle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.detalles_orden_detalle_id_seq OWNED BY public.detalles_orden.detalle_id;


--
-- TOC entry 224 (class 1259 OID 17559)
-- Name: meseros; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.meseros (
    mesero_id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    telefono character varying(20),
    fecha_contratacion date DEFAULT CURRENT_DATE
);


ALTER TABLE public.meseros OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17558)
-- Name: meseros_mesero_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.meseros_mesero_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.meseros_mesero_id_seq OWNER TO postgres;

--
-- TOC entry 5062 (class 0 OID 0)
-- Dependencies: 223
-- Name: meseros_mesero_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.meseros_mesero_id_seq OWNED BY public.meseros.mesero_id;


--
-- TOC entry 226 (class 1259 OID 17569)
-- Name: ordenes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ordenes (
    orden_id integer NOT NULL,
    numero_mesa integer NOT NULL,
    fecha_hora timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado character varying(20) DEFAULT 'Abierta'::character varying,
    mesero_id integer
);


ALTER TABLE public.ordenes OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17568)
-- Name: ordenes_orden_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ordenes_orden_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ordenes_orden_id_seq OWNER TO postgres;

--
-- TOC entry 5063 (class 0 OID 0)
-- Dependencies: 225
-- Name: ordenes_orden_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ordenes_orden_id_seq OWNED BY public.ordenes.orden_id;


--
-- TOC entry 222 (class 1259 OID 17543)
-- Name: productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.productos (
    producto_id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    precio numeric(10,2) NOT NULL,
    stock integer NOT NULL,
    categoria_id integer
);


ALTER TABLE public.productos OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17542)
-- Name: productos_producto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.productos_producto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.productos_producto_id_seq OWNER TO postgres;

--
-- TOC entry 5064 (class 0 OID 0)
-- Dependencies: 221
-- Name: productos_producto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.productos_producto_id_seq OWNED BY public.productos.producto_id;


--
-- TOC entry 4876 (class 2604 OID 17535)
-- Name: categorias categoria_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias ALTER COLUMN categoria_id SET DEFAULT nextval('public.categorias_categoria_id_seq'::regclass);


--
-- TOC entry 4883 (class 2604 OID 17588)
-- Name: detalles_orden detalle_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalles_orden ALTER COLUMN detalle_id SET DEFAULT nextval('public.detalles_orden_detalle_id_seq'::regclass);


--
-- TOC entry 4878 (class 2604 OID 17562)
-- Name: meseros mesero_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meseros ALTER COLUMN mesero_id SET DEFAULT nextval('public.meseros_mesero_id_seq'::regclass);


--
-- TOC entry 4880 (class 2604 OID 17572)
-- Name: ordenes orden_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordenes ALTER COLUMN orden_id SET DEFAULT nextval('public.ordenes_orden_id_seq'::regclass);


--
-- TOC entry 4877 (class 2604 OID 17546)
-- Name: productos producto_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos ALTER COLUMN producto_id SET DEFAULT nextval('public.productos_producto_id_seq'::regclass);


--
-- TOC entry 5046 (class 0 OID 17532)
-- Dependencies: 220
-- Data for Name: categorias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categorias (categoria_id, nombre, descripcion) FROM stdin;
1	Cervezas	Bebidas de cerveza
2	Aguardientes	Bebidas de aguardiente
3	Whisky	Bebidas de whisky
4	Ron	Bebidas de ron
5	Vodka	Bebidas de vodka
6	Tequila	Bebidas de tequila
7	Cocteles	Preparaciones de cocteles
8	Bebidas sin alcohol	Bebidas no alcoholicas
9	Snacks	Alimentos y pasabocas
10	Energizantes	Bebidas energizantes
\.


--
-- TOC entry 5054 (class 0 OID 17585)
-- Dependencies: 228
-- Data for Name: detalles_orden; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.detalles_orden (detalle_id, orden_id, producto_id, cantidad, precio_unitario) FROM stdin;
1	1	1	2	5000.00
2	2	2	1	35000.00
3	3	3	1	180000.00
4	4	4	2	32000.00
5	5	5	1	85000.00
6	6	6	1	120000.00
7	7	7	2	22000.00
8	8	8	3	5000.00
9	9	9	2	15000.00
10	10	10	2	7000.00
\.


--
-- TOC entry 5050 (class 0 OID 17559)
-- Dependencies: 224
-- Data for Name: meseros; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.meseros (mesero_id, nombre, telefono, fecha_contratacion) FROM stdin;
1	Carlos Mendoza	3001112233	2024-01-15
2	Laura Gomez	3002223344	2024-02-10
3	Andres Ramirez	3003334455	2024-03-05
4	Maria Lopez	3004445566	2024-04-12
5	Juan Torres	3005556677	2024-05-20
6	Daniela Castro	3006667788	2024-06-18
7	Sebastian Martinez	3007778899	2024-07-22
8	Valentina Rojas	3008889900	2024-08-14
9	Camilo Herrera	3009990011	2024-09-09
10	Sofia Ramirez	3010001122	2024-10-01
\.


--
-- TOC entry 5052 (class 0 OID 17569)
-- Dependencies: 226
-- Data for Name: ordenes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ordenes (orden_id, numero_mesa, fecha_hora, estado, mesero_id) FROM stdin;
1	1	2026-11-17 11:36:09.47903	Cerrada	1
2	2	2026-11-17 11:36:09.47903	Cerrada	2
3	3	2026-11-17 11:36:09.47903	Servida	3
4	4	2026-11-17 11:36:09.47903	Abierta	4
5	5	2026-11-17 11:36:09.47903	Cerrada	5
6	6	2026-11-17 11:36:09.47903	En preparación	6
7	7	2026-11-17 11:36:09.47903	Servida	7
8	8	2026-11-17 11:36:09.47903	Cerrada	8
9	9	2026-11-17 11:36:09.47903	Abierta	9
10	10	2026-11-17 11:36:09.47903	Cerrada	10
\.


--
-- TOC entry 5048 (class 0 OID 17543)
-- Dependencies: 222
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.productos (producto_id, nombre, precio, stock, categoria_id) FROM stdin;
1	Cerveza Aguila 330ml	5000.00	100	1
2	Aguardiente Antioqueno 375ml	35000.00	30	2
3	Whisky Old Parr 750ml	180000.00	15	3
4	Ron Medellin 375ml	32000.00	25	4
5	Vodka Smirnoff 750ml	85000.00	20	5
6	Tequila Jose Cuervo 750ml	120000.00	12	6
7	Mojito Tradicional	22000.00	40	7
8	Gaseosa Coca Cola 400ml	5000.00	80	8
9	Papas a la Francesa	15000.00	30	9
10	Bebida Energizante 250ml	7000.00	45	10
\.


--
-- TOC entry 5065 (class 0 OID 0)
-- Dependencies: 219
-- Name: categorias_categoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categorias_categoria_id_seq', 10, true);


--
-- TOC entry 5066 (class 0 OID 0)
-- Dependencies: 227
-- Name: detalles_orden_detalle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.detalles_orden_detalle_id_seq', 10, true);


--
-- TOC entry 5067 (class 0 OID 0)
-- Dependencies: 223
-- Name: meseros_mesero_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.meseros_mesero_id_seq', 10, true);


--
-- TOC entry 5068 (class 0 OID 0)
-- Dependencies: 225
-- Name: ordenes_orden_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ordenes_orden_id_seq', 10, true);


--
-- TOC entry 5069 (class 0 OID 0)
-- Dependencies: 221
-- Name: productos_producto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.productos_producto_id_seq', 10, true);


--
-- TOC entry 4885 (class 2606 OID 17541)
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (categoria_id);


--
-- TOC entry 4893 (class 2606 OID 17593)
-- Name: detalles_orden detalles_orden_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalles_orden
    ADD CONSTRAINT detalles_orden_pkey PRIMARY KEY (detalle_id);


--
-- TOC entry 4889 (class 2606 OID 17567)
-- Name: meseros meseros_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.meseros
    ADD CONSTRAINT meseros_pkey PRIMARY KEY (mesero_id);


--
-- TOC entry 4891 (class 2606 OID 17578)
-- Name: ordenes ordenes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_pkey PRIMARY KEY (orden_id);


--
-- TOC entry 4887 (class 2606 OID 17552)
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (producto_id);


--
-- TOC entry 4896 (class 2606 OID 17594)
-- Name: detalles_orden detalles_orden_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalles_orden
    ADD CONSTRAINT detalles_orden_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.ordenes(orden_id);


--
-- TOC entry 4897 (class 2606 OID 17599)
-- Name: detalles_orden detalles_orden_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalles_orden
    ADD CONSTRAINT detalles_orden_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(producto_id);


--
-- TOC entry 4895 (class 2606 OID 17579)
-- Name: ordenes ordenes_mesero_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_mesero_id_fkey FOREIGN KEY (mesero_id) REFERENCES public.meseros(mesero_id);


--
-- TOC entry 4894 (class 2606 OID 17553)
-- Name: productos productos_categoria_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_categoria_id_fkey FOREIGN KEY (categoria_id) REFERENCES public.categorias(categoria_id);


-- Completed on 2026-11-17 11:54:50

--
-- PostgreSQL database dump complete
--

\unrestrict gOC8QJzCYvNPebKFSRwulKksKQReFq6pz9ZqadZemmej9GbTa49ylMfP9tZn8h9

