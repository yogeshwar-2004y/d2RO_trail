--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

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
-- Name: create_report_for_accepted_memo(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.create_report_for_accepted_memo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    default_project_id INTEGER := 1;
    default_lru_id INTEGER := 1;
    default_serial_id INTEGER := 1;
    memo_project_id INTEGER;
    memo_lru_id INTEGER;
    memo_serial_id INTEGER;
    approval_status TEXT;
BEGIN
    -- Only proceed if the memo status is being changed to 'assigned'
    IF NEW.memo_status = 'assigned' AND (OLD.memo_status IS NULL OR OLD.memo_status != 'assigned') THEN
        
        -- Check if there's an approval record with 'accepted' status
        SELECT status INTO approval_status
        FROM memo_approval 
        WHERE memo_id = NEW.memo_id AND status = 'accepted';
        
        -- Only create report if memo is accepted (not just assigned)
        IF approval_status IS NULL THEN
            RAISE NOTICE 'Memo % is assigned but not accepted, skipping report creation', NEW.memo_id;
            RETURN NEW;
        END IF;
        
        -- Check if report already exists for this memo
        IF EXISTS (SELECT 1 FROM reports WHERE memo_id = NEW.memo_id) THEN
            RAISE NOTICE 'Report already exists for memo %, skipping', NEW.memo_id;
            RETURN NEW;
        END IF;
        
        -- Try to determine project_id based on wing_proj_ref_no
        SELECT project_id INTO memo_project_id
        FROM projects 
        WHERE LOWER(project_name) = ANY(
            SELECT LOWER(unnest(string_to_array(NEW.wing_proj_ref_no, '/')))
        )
        LIMIT 1;
        
        IF memo_project_id IS NULL THEN
            memo_project_id := default_project_id;
        END IF;
        
        -- Try to determine lru_id based on lru_sru_desc
        SELECT lru_id INTO memo_lru_id
        FROM lrus 
        WHERE LOWER(lru_name) = LOWER(NEW.lru_sru_desc)
        LIMIT 1;
        
        IF memo_lru_id IS NULL THEN
            memo_lru_id := default_lru_id;
        END IF;
        
        -- Determine serial_id
        SELECT serial_id INTO memo_serial_id
        FROM serial_numbers 
        WHERE lru_id = memo_lru_id 
        ORDER BY serial_id 
        LIMIT 1;
        
        IF memo_serial_id IS NULL THEN
            -- Create a new serial number entry
            INSERT INTO serial_numbers (lru_id, serial_number)
            VALUES (memo_lru_id, 1)
            RETURNING serial_id INTO memo_serial_id;
        END IF;
        
        -- Create the report
        INSERT INTO reports (
            memo_id, 
            project_id, 
            lru_id, 
            serial_id,
            inspection_stage, 
            date_of_review, 
            review_venue,
            status, 
            created_at
        ) VALUES (
            NEW.memo_id,
            memo_project_id,
            memo_lru_id,
            memo_serial_id,
            NEW.lru_sru_desc,  -- inspection_stage
            NEW.memo_date,     -- date_of_review
            NEW.venue,         -- review_venue
            'ASSIGNED',        -- status
            NOW()              -- created_at
        );
        
        RAISE NOTICE 'Report created automatically for accepted memo %', NEW.memo_id;
        
    END IF;
    
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.create_report_for_accepted_memo() OWNER TO postgres;

--
-- Name: FUNCTION create_report_for_accepted_memo(); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.create_report_for_accepted_memo() IS 'Automatically creates a report when a memo status changes to assigned AND the memo has been accepted';


--
-- Name: get_next_number(integer, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_next_number(p_test_id integer DEFAULT NULL::integer, p_stage_id integer DEFAULT NULL::integer, p_substage_id integer DEFAULT NULL::integer, p_level character varying DEFAULT 'stage'::character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    next_num INTEGER;
BEGIN
    CASE p_level
        WHEN 'stage' THEN
            SELECT COALESCE(MAX(stage_number), 0) + 1 INTO next_num
            FROM stages WHERE test_id = p_test_id;
        WHEN 'substage' THEN
            SELECT COALESCE(MAX(substage_number), 0) + 1 INTO next_num
            FROM substages WHERE stage_id = p_stage_id;
        WHEN 'item' THEN
            SELECT COALESCE(MAX(item_number), 0) + 1 INTO next_num
            FROM substage_items WHERE substage_id = p_substage_id;
        ELSE
            next_num := 1;
    END CASE;
    
    RETURN next_num;
END;
$$;


ALTER FUNCTION public.get_next_number(p_test_id integer, p_stage_id integer, p_substage_id integer, p_level character varying) OWNER TO postgres;

--
-- Name: FUNCTION get_next_number(p_test_id integer, p_stage_id integer, p_substage_id integer, p_level character varying); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.get_next_number(p_test_id integer, p_stage_id integer, p_substage_id integer, p_level character varying) IS 'Gets the next available number for stages, substages, or items';


--
-- Name: renumber_items(integer, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.renumber_items(p_test_id integer DEFAULT NULL::integer, p_stage_id integer DEFAULT NULL::integer, p_substage_id integer DEFAULT NULL::integer, p_level character varying DEFAULT 'stage'::character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    item_record RECORD;
    new_number INTEGER := 1;
BEGIN
    CASE p_level
        WHEN 'stage' THEN
            FOR item_record IN 
                SELECT stage_id FROM stages 
                WHERE test_id = p_test_id AND is_active = TRUE
                ORDER BY stage_number
            LOOP
                UPDATE stages SET stage_number = new_number WHERE stage_id = item_record.stage_id;
                new_number := new_number + 1;
            END LOOP;
        WHEN 'substage' THEN
            FOR item_record IN 
                SELECT substage_id FROM substages 
                WHERE stage_id = p_stage_id AND is_active = TRUE
                ORDER BY substage_number
            LOOP
                UPDATE substages SET substage_number = new_number WHERE substage_id = item_record.substage_id;
                new_number := new_number + 1;
            END LOOP;
        WHEN 'item' THEN
            FOR item_record IN 
                SELECT item_id FROM substage_items 
                WHERE substage_id = p_substage_id AND is_active = TRUE
                ORDER BY item_number
            LOOP
                UPDATE substage_items SET item_number = new_number WHERE item_id = item_record.item_id;
                new_number := new_number + 1;
            END LOOP;
    END CASE;
END;
$$;


ALTER FUNCTION public.renumber_items(p_test_id integer, p_stage_id integer, p_substage_id integer, p_level character varying) OWNER TO postgres;

--
-- Name: FUNCTION renumber_items(p_test_id integer, p_stage_id integer, p_substage_id integer, p_level character varying); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.renumber_items(p_test_id integer, p_stage_id integer, p_substage_id integer, p_level character varying) IS 'Renumbers items after deletion to maintain sequential order';


--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activity_logs (
    activity_id integer NOT NULL,
    project_id integer,
    activity_performed character varying(100) NOT NULL,
    performed_by integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now(),
    additional_info text,
    notified_user_id integer,
    is_read boolean DEFAULT false,
    notification_type character varying(50)
);


ALTER TABLE public.activity_logs OWNER TO postgres;

--
-- Name: activity_logs_activity_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.activity_logs_activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_logs_activity_id_seq OWNER TO postgres;

--
-- Name: activity_logs_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.activity_logs_activity_id_seq OWNED BY public.activity_logs.activity_id;


--
-- Name: assembled_board_inspection_report; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assembled_board_inspection_report (
    report_id integer NOT NULL,
    project_name text,
    report_ref_no character varying(100),
    memo_ref_no character varying(100),
    lru_name text,
    sru_name text,
    dp_name text,
    part_no character varying(100),
    inspection_stage text,
    test_venue text,
    quantity integer,
    sl_nos text,
    serial_number character varying(100),
    start_date date,
    end_date date,
    dated1 date,
    dated2 date,
    obs1 text,
    rem1 character varying(20),
    upload1 text,
    obs2 text,
    rem2 character varying(20),
    upload2 text,
    obs3 text,
    rem3 character varying(20),
    upload3 text,
    obs4 text,
    rem4 character varying(20),
    upload4 text,
    obs5 text,
    rem5 character varying(20),
    upload5 text,
    obs6 text,
    rem6 character varying(20),
    upload6 text,
    obs7 text,
    rem7 character varying(20),
    upload7 text,
    obs8 text,
    rem8 character varying(20),
    upload8 text,
    obs9 text,
    rem9 character varying(20),
    upload9 text,
    obs10 text,
    rem10 character varying(20),
    upload10 text,
    obs11 text,
    rem11 character varying(20),
    upload11 text,
    obs12 text,
    rem12 character varying(20),
    upload12 text,
    obs13 text,
    rem13 character varying(20),
    upload13 text,
    obs14 text,
    rem14 character varying(20),
    upload14 text,
    obs15 text,
    rem15 character varying(20),
    upload15 text,
    obs16 text,
    rem16 character varying(20),
    upload16 text,
    obs17 text,
    rem17 character varying(20),
    upload17 text,
    obs18 text,
    rem18 character varying(20),
    upload18 text,
    obs19 text,
    rem19 character varying(20),
    upload19 text,
    obs20 text,
    rem20 character varying(20),
    upload20 text,
    prepared_by text,
    verified_by text,
    approved_by text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT assembled_board_inspection_report_rem10_check CHECK (((rem10)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem11_check CHECK (((rem11)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem12_check CHECK (((rem12)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem13_check CHECK (((rem13)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem14_check CHECK (((rem14)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem15_check CHECK (((rem15)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem16_check CHECK (((rem16)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem17_check CHECK (((rem17)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem18_check CHECK (((rem18)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem19_check CHECK (((rem19)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem1_check CHECK (((rem1)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem20_check CHECK (((rem20)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem2_check CHECK (((rem2)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem3_check CHECK (((rem3)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem4_check CHECK (((rem4)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem5_check CHECK (((rem5)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem6_check CHECK (((rem6)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem7_check CHECK (((rem7)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem8_check CHECK (((rem8)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT assembled_board_inspection_report_rem9_check CHECK (((rem9)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[])))
);


ALTER TABLE public.assembled_board_inspection_report OWNER TO postgres;

--
-- Name: assembled_board_inspection_report_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.assembled_board_inspection_report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.assembled_board_inspection_report_report_id_seq OWNER TO postgres;

--
-- Name: assembled_board_inspection_report_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.assembled_board_inspection_report_report_id_seq OWNED BY public.assembled_board_inspection_report.report_id;


--
-- Name: bare_pcb_inspection_report; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bare_pcb_inspection_report (
    report_id integer NOT NULL,
    project_name text,
    report_ref_no character varying(100),
    memo_ref_no character varying(100),
    lru_name text,
    sru_name text,
    dp_name text,
    part_no character varying(100),
    inspection_stage text,
    test_venue text,
    quantity integer,
    sl_nos text,
    serial_number character varying(100),
    inspection_count character varying(50),
    start_date date,
    end_date date,
    dated1 date,
    dated2 date,
    obs1 text,
    rem1 character varying(20),
    upload1 text,
    obs2 text,
    rem2 character varying(20),
    upload2 text,
    obs3 text,
    rem3 character varying(20),
    upload3 text,
    obs4 text,
    rem4 character varying(20),
    upload4 text,
    obs5 text,
    rem5 character varying(20),
    upload5 text,
    obs6 text,
    rem6 character varying(20),
    upload6 text,
    obs7 text,
    rem7 character varying(20),
    upload7 text,
    obs8 text,
    rem8 character varying(20),
    upload8 text,
    obs9 text,
    rem9 character varying(20),
    upload9 text,
    obs10 text,
    rem10 character varying(20),
    upload10 text,
    obs11 text,
    rem11 character varying(20),
    upload11 text,
    obs12 text,
    rem12 character varying(20),
    upload12 text,
    overall_status text,
    quality_rating integer,
    recommendations text,
    prepared_by text,
    verified_by text,
    approved_by text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.bare_pcb_inspection_report OWNER TO postgres;

--
-- Name: bare_pcb_inspection_report_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bare_pcb_inspection_report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bare_pcb_inspection_report_report_id_seq OWNER TO postgres;

--
-- Name: bare_pcb_inspection_report_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bare_pcb_inspection_report_report_id_seq OWNED BY public.bare_pcb_inspection_report.report_id;


--
-- Name: bulletins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bulletins (
    bulletin_id integer NOT NULL,
    sub_test_id integer NOT NULL,
    parent_bulletin_id integer,
    bulletin_name character varying(200) NOT NULL,
    bulletin_description text,
    created_at timestamp without time zone DEFAULT now(),
    created_by integer,
    updated_at timestamp without time zone DEFAULT now(),
    updated_by integer
);


ALTER TABLE public.bulletins OWNER TO postgres;

--
-- Name: bulletins_bulletin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bulletins_bulletin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bulletins_bulletin_id_seq OWNER TO postgres;

--
-- Name: bulletins_bulletin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bulletins_bulletin_id_seq OWNED BY public.bulletins.bulletin_id;


--
-- Name: conformal_coating_inspection_report; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.conformal_coating_inspection_report (
    report_id integer NOT NULL,
    project_name text,
    report_ref_no character varying(100),
    memo_ref_no character varying(100),
    lru_name text,
    sru_name text,
    dp_name text,
    part_no character varying(100),
    inspection_stage text,
    test_venue text,
    quantity integer,
    sl_nos text,
    serial_number character varying(100),
    start_date date,
    end_date date,
    dated1 date,
    dated2 date,
    obs1 text,
    rem1 character varying(20),
    upload1 text,
    expected1 text DEFAULT 'Should not be there'::text,
    obs2 text,
    rem2 character varying(20),
    upload2 text,
    expected2 text DEFAULT 'Should not be there'::text,
    obs3 text,
    rem3 character varying(20),
    upload3 text,
    expected3 text DEFAULT 'Should not be there'::text,
    obs4 text,
    rem4 character varying(20),
    upload4 text,
    expected4 text DEFAULT 'Should not be there'::text,
    obs5 text,
    rem5 character varying(20),
    upload5 text,
    expected5 text DEFAULT 'Not recommended'::text,
    obs6 text,
    rem6 character varying(20),
    upload6 text,
    expected6 text DEFAULT 'No Deformity'::text,
    obs7 text,
    rem7 character varying(20),
    upload7 text,
    expected7 text DEFAULT 'No Damages'::text,
    obs8 text,
    rem8 character varying(20),
    upload8 text,
    expected8 text DEFAULT 'Should have linear Coating'::text,
    obs9 text,
    rem9 character varying(20),
    upload9 text,
    expected9 text DEFAULT '30 to 130 microns'::text,
    overall_status text,
    quality_rating integer,
    recommendations text,
    prepared_by text,
    verified_by text,
    approved_by text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    original_report_id integer,
    report_card_id integer,
    CONSTRAINT conformal_coating_inspection_report_rem1_check CHECK (((rem1)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT conformal_coating_inspection_report_rem2_check CHECK (((rem2)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT conformal_coating_inspection_report_rem3_check CHECK (((rem3)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT conformal_coating_inspection_report_rem4_check CHECK (((rem4)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT conformal_coating_inspection_report_rem5_check CHECK (((rem5)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT conformal_coating_inspection_report_rem6_check CHECK (((rem6)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT conformal_coating_inspection_report_rem7_check CHECK (((rem7)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT conformal_coating_inspection_report_rem8_check CHECK (((rem8)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT conformal_coating_inspection_report_rem9_check CHECK (((rem9)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[])))
);


ALTER TABLE public.conformal_coating_inspection_report OWNER TO postgres;

--
-- Name: conformal_coating_inspection_report_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.conformal_coating_inspection_report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.conformal_coating_inspection_report_report_id_seq OWNER TO postgres;

--
-- Name: conformal_coating_inspection_report_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.conformal_coating_inspection_report_report_id_seq OWNED BY public.conformal_coating_inspection_report.report_id;


--
-- Name: cot_screening_inspection_report; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cot_screening_inspection_report (
    report_id integer NOT NULL,
    project_name text,
    report_ref_no character varying(100),
    memo_ref_no character varying(100),
    lru_name text,
    sru_name text,
    dp_name text,
    part_no character varying(100),
    inspection_stage text,
    test_venue text,
    quantity integer,
    sl_nos text,
    serial_number character varying(100),
    start_date date,
    end_date date,
    dated1 date,
    dated2 date,
    test_nature1 text,
    test_nature2 text,
    test_nature3 text,
    rem1 character varying(20),
    upload1 text,
    rem2 character varying(20),
    upload2 text,
    rem3 character varying(20),
    upload3 text,
    prepared_by text,
    verified_by text,
    approved_by text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cot_screening_inspection_report_rem1_check CHECK (((rem1)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT cot_screening_inspection_report_rem2_check CHECK (((rem2)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[]))),
    CONSTRAINT cot_screening_inspection_report_rem3_check CHECK (((rem3)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying])::text[])))
);


ALTER TABLE public.cot_screening_inspection_report OWNER TO postgres;

--
-- Name: cot_screening_inspection_report_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cot_screening_inspection_report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cot_screening_inspection_report_report_id_seq OWNER TO postgres;

--
-- Name: cot_screening_inspection_report_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cot_screening_inspection_report_report_id_seq OWNED BY public.cot_screening_inspection_report.report_id;


--
-- Name: document_annotations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_annotations (
    annotation_id integer NOT NULL,
    comment_id integer NOT NULL,
    page_no integer NOT NULL,
    x_position numeric(5,2) NOT NULL,
    y_position numeric(5,2) NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    document_id integer NOT NULL
);


ALTER TABLE public.document_annotations OWNER TO postgres;

--
-- Name: document_annotations_annotation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.document_annotations_annotation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.document_annotations_annotation_id_seq OWNER TO postgres;

--
-- Name: document_annotations_annotation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.document_annotations_annotation_id_seq OWNED BY public.document_annotations.annotation_id;


--
-- Name: document_annotations_backup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_annotations_backup (
    annotation_id integer,
    comment_id integer,
    document_id character varying(100),
    page_no integer,
    x_position numeric(5,2),
    y_position numeric(5,2),
    created_at timestamp without time zone
);


ALTER TABLE public.document_annotations_backup OWNER TO postgres;

--
-- Name: document_comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_comments (
    comment_id integer NOT NULL,
    document_name character varying(255),
    version character varying(50),
    reviewer_id integer,
    page_no integer NOT NULL,
    section character varying(100),
    description text,
    commented_by character varying(100) DEFAULT 'Anonymous'::character varying,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    is_annotation boolean DEFAULT false,
    status character varying(10),
    accepted_at timestamp without time zone,
    justification text,
    accepted_by integer,
    document_id integer NOT NULL,
    CONSTRAINT document_comments_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'accepted'::character varying, 'rejected'::character varying])::text[])))
);


ALTER TABLE public.document_comments OWNER TO postgres;

--
-- Name: document_comments_backup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_comments_backup (
    comment_id integer,
    document_id character varying(100),
    document_name character varying(255),
    version character varying(50),
    reviewer_id integer,
    page_no integer,
    section character varying(100),
    description text,
    commented_by character varying(100),
    created_at timestamp without time zone,
    is_annotation boolean,
    status character varying(10),
    accepted_at timestamp without time zone,
    justification text,
    accepted_by integer
);


ALTER TABLE public.document_comments_backup OWNER TO postgres;

--
-- Name: document_comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.document_comments_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.document_comments_comment_id_seq OWNER TO postgres;

--
-- Name: document_comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.document_comments_comment_id_seq OWNED BY public.document_comments.comment_id;


--
-- Name: document_reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_reviews (
    review_id integer NOT NULL,
    document_id integer NOT NULL,
    reviewer_id integer NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying NOT NULL,
    review_date timestamp without time zone DEFAULT now(),
    CONSTRAINT document_reviews_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'accepted'::character varying, 'rejected'::character varying])::text[])))
);


ALTER TABLE public.document_reviews OWNER TO postgres;

--
-- Name: document_reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.document_reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.document_reviews_review_id_seq OWNER TO postgres;

--
-- Name: document_reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.document_reviews_review_id_seq OWNED BY public.document_reviews.review_id;


--
-- Name: document_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_types (
    type_id integer NOT NULL,
    type_name character varying(255) NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted boolean DEFAULT false
);


ALTER TABLE public.document_types OWNER TO postgres;

--
-- Name: document_types_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.document_types_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.document_types_type_id_seq OWNER TO postgres;

--
-- Name: document_types_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.document_types_type_id_seq OWNED BY public.document_types.type_id;


--
-- Name: document_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_version (
    version_id integer NOT NULL,
    document_id integer NOT NULL,
    version character varying(20) NOT NULL,
    revision character varying(20),
    doc_version character varying(2) NOT NULL,
    uploaded_by integer NOT NULL,
    uploaded_date timestamp without time zone DEFAULT now(),
    file_path character varying(255) NOT NULL,
    CONSTRAINT document_version_doc_version_check CHECK (((doc_version)::text ~ '^[A-Z]{1,2}$'::text))
);


ALTER TABLE public.document_version OWNER TO postgres;

--
-- Name: document_version_version_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.document_version_version_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.document_version_version_id_seq OWNER TO postgres;

--
-- Name: document_version_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.document_version_version_id_seq OWNED BY public.document_version.version_id;


--
-- Name: iqa_observation_reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.iqa_observation_reports (
    report_id integer NOT NULL,
    project_id integer NOT NULL,
    lru_id integer NOT NULL,
    document_id integer,
    observation_count character varying(50),
    report_date date DEFAULT CURRENT_DATE NOT NULL,
    current_year character varying(10),
    lru_part_number character varying(100),
    serial_number character varying(100),
    inspection_stage character varying(255) DEFAULT 'Document review/report'::character varying,
    doc_review_date date,
    review_venue character varying(255),
    reference_document text,
    reviewed_by_user_id integer,
    reviewed_by_signature_path text,
    reviewed_by_verified_name character varying(255),
    approved_by_user_id integer,
    approved_by_signature_path text,
    approved_by_verified_name character varying(255),
    created_by integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.iqa_observation_reports OWNER TO postgres;

--
-- Name: iqa_observation_reports_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.iqa_observation_reports_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.iqa_observation_reports_report_id_seq OWNER TO postgres;

--
-- Name: iqa_observation_reports_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.iqa_observation_reports_report_id_seq OWNED BY public.iqa_observation_reports.report_id;


--
-- Name: kit_of_parts_inspection_report; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kit_of_parts_inspection_report (
    report_id integer NOT NULL,
    project_name text,
    dp_name text,
    report_ref_no character varying(100),
    memo_ref_no character varying(100),
    lru_name text,
    sru_name text,
    part_no character varying(100),
    quantity integer,
    sl_nos text,
    test_venue text,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    test1_sl_no integer DEFAULT 1,
    test1_case text DEFAULT 'Any observation pending from previous KOP stage'::text,
    test1_expected text DEFAULT 'NIL'::text,
    test1_observations text,
    test1_remarks character varying(10),
    test1_upload text,
    test2_sl_no integer DEFAULT 2,
    test2_case text DEFAULT 'CoC verification of components'::text,
    test2_expected text DEFAULT 'Verified'::text,
    test2_observations text,
    test2_remarks character varying(10),
    test2_upload text,
    test3_sl_no integer DEFAULT 3,
    test3_case text DEFAULT 'Quantity as BOM'::text,
    test3_expected text DEFAULT 'Matching'::text,
    test3_observations text,
    test3_remarks character varying(10),
    test3_upload text,
    test4_sl_no integer DEFAULT 4,
    test4_case text DEFAULT 'Quantity as per number of boards to be assembled'::text,
    test4_expected text DEFAULT 'Matching'::text,
    test4_observations text,
    test4_remarks character varying(10),
    test4_upload text,
    test5_sl_no integer DEFAULT 5,
    test5_case text DEFAULT 'Components storage in ESD cover'::text,
    test5_expected text DEFAULT 'Stored in ESD'::text,
    test5_observations text,
    test5_remarks character varying(10),
    test5_upload text,
    test6_sl_no integer DEFAULT 6,
    test6_case text DEFAULT 'All connectors to be fitted with screws before assembly'::text,
    test6_expected text DEFAULT 'Fitted properly'::text,
    test6_observations text,
    test6_remarks character varying(10),
    test6_upload text,
    test7_sl_no integer DEFAULT 7,
    test7_case text DEFAULT 'Any other observations'::text,
    test7_expected text DEFAULT 'NIL'::text,
    test7_observations text,
    test7_remarks character varying(10),
    test7_upload text,
    prepared_by_qa_g1 text,
    verified_by_g1h_qa_g text,
    approved_by text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    inspection_stage text,
    dated1 date,
    dated2 date,
    original_report_id integer,
    report_card_id integer,
    CONSTRAINT kit_of_parts_inspection_report_test1_remarks_check CHECK (((test1_remarks)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, ''::character varying])::text[]))),
    CONSTRAINT kit_of_parts_inspection_report_test2_remarks_check CHECK (((test2_remarks)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, ''::character varying])::text[]))),
    CONSTRAINT kit_of_parts_inspection_report_test3_remarks_check CHECK (((test3_remarks)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, ''::character varying])::text[]))),
    CONSTRAINT kit_of_parts_inspection_report_test4_remarks_check CHECK (((test4_remarks)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, ''::character varying])::text[]))),
    CONSTRAINT kit_of_parts_inspection_report_test5_remarks_check CHECK (((test5_remarks)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, ''::character varying])::text[]))),
    CONSTRAINT kit_of_parts_inspection_report_test6_remarks_check CHECK (((test6_remarks)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, ''::character varying])::text[]))),
    CONSTRAINT kit_of_parts_inspection_report_test7_remarks_check CHECK (((test7_remarks)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, ''::character varying])::text[])))
);


ALTER TABLE public.kit_of_parts_inspection_report OWNER TO postgres;

--
-- Name: kit_of_parts_inspection_report_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kit_of_parts_inspection_report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kit_of_parts_inspection_report_report_id_seq OWNER TO postgres;

--
-- Name: kit_of_parts_inspection_report_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kit_of_parts_inspection_report_report_id_seq OWNED BY public.kit_of_parts_inspection_report.report_id;


--
-- Name: login_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.login_logs (
    serial_num integer NOT NULL,
    user_id integer NOT NULL,
    activity_performed character varying(100) NOT NULL,
    performed_by integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.login_logs OWNER TO postgres;

--
-- Name: login_logs_serial_num_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.login_logs_serial_num_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.login_logs_serial_num_seq OWNER TO postgres;

--
-- Name: login_logs_serial_num_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.login_logs_serial_num_seq OWNED BY public.login_logs.serial_num;


--
-- Name: lrus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lrus (
    lru_id integer NOT NULL,
    project_id integer NOT NULL,
    lru_name character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    lru_part_number character varying(100)
);


ALTER TABLE public.lrus OWNER TO postgres;

--
-- Name: COLUMN lrus.lru_part_number; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.lrus.lru_part_number IS 'LRU Part Number - supports mix of numbers, text, and symbols (e.g., ABC-123-XYZ, 456/789, etc.)';


--
-- Name: lrus_lru_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.lrus_lru_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.lrus_lru_id_seq OWNER TO postgres;

--
-- Name: lrus_lru_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.lrus_lru_id_seq OWNED BY public.lrus.lru_id;


--
-- Name: mechanical_inspection_report; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mechanical_inspection_report (
    report_id integer NOT NULL,
    project_name text,
    report_ref_no character varying(100),
    memo_ref_no character varying(100),
    lru_name text,
    sru_name text,
    dp_name text,
    part_no character varying(100),
    inspection_stage text,
    test_venue text,
    quantity integer,
    sl_nos text,
    start_date date,
    end_date date,
    dated1 date,
    dated2 date,
    dim1_dimension text,
    dim1_tolerance text,
    dim1_observed_value text,
    dim1_instrument_used text,
    dim1_remarks text,
    dim1_upload text,
    dim2_dimension text,
    dim2_tolerance text,
    dim2_observed_value text,
    dim2_instrument_used text,
    dim2_remarks text,
    dim2_upload text,
    dim3_dimension text,
    dim3_tolerance text,
    dim3_observed_value text,
    dim3_instrument_used text,
    dim3_remarks text,
    dim3_upload text,
    param1_name text DEFAULT 'Burrs'::text,
    param1_compliance_observation text,
    param1_expected text DEFAULT 'Not Expected'::text,
    param1_remarks text,
    param1_upload text,
    param2_name text DEFAULT 'Damages'::text,
    param2_compliance_observation text,
    param2_expected text DEFAULT 'Not Expected'::text,
    param2_remarks text,
    param2_upload text,
    param3_name text DEFAULT 'Name Plate'::text,
    param3_compliance_observation text,
    param3_expected text DEFAULT 'As per Drawing'::text,
    param3_remarks text,
    param3_upload text,
    param4_name text DEFAULT 'Engraving'::text,
    param4_compliance_observation text,
    param4_expected text DEFAULT 'As per Drawing'::text,
    param4_remarks text,
    param4_upload text,
    param5_name text DEFAULT 'Passivation'::text,
    param5_compliance_observation text,
    param5_expected text DEFAULT 'As per Drawing'::text,
    param5_remarks text,
    param5_upload text,
    param6_name text DEFAULT 'Chromate'::text,
    param6_compliance_observation text,
    param6_expected text DEFAULT 'As per Drawing'::text,
    param6_remarks text,
    param6_upload text,
    param7_name text DEFAULT 'Electro-less Nickel plating'::text,
    param7_compliance_observation text,
    param7_expected text DEFAULT 'As per Drawing'::text,
    param7_remarks text,
    param7_upload text,
    param8_name text DEFAULT 'Fasteners'::text,
    param8_compliance_observation text,
    param8_expected text DEFAULT 'As per Drawing'::text,
    param8_remarks text,
    param8_upload text,
    overall_status text,
    quality_rating integer,
    recommendations text,
    prepared_by text,
    verified_by text,
    approved_by text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.mechanical_inspection_report OWNER TO postgres;

--
-- Name: TABLE mechanical_inspection_report; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.mechanical_inspection_report IS 'Mechanical inspection reports based on MechanicalInspection.vue template';


--
-- Name: COLUMN mechanical_inspection_report.project_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.project_name IS 'Project name from general information';


--
-- Name: COLUMN mechanical_inspection_report.lru_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.lru_name IS 'LRU (Line Replaceable Unit) name being inspected';


--
-- Name: COLUMN mechanical_inspection_report.dp_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.dp_name IS 'DP (Design Point) name';


--
-- Name: COLUMN mechanical_inspection_report.start_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.start_date IS 'Inspection start date';


--
-- Name: COLUMN mechanical_inspection_report.end_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.end_date IS 'Inspection end date';


--
-- Name: COLUMN mechanical_inspection_report.dim1_dimension; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.dim1_dimension IS 'First dimensional measurement - dimension';


--
-- Name: COLUMN mechanical_inspection_report.dim1_tolerance; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.dim1_tolerance IS 'First dimensional measurement - tolerance';


--
-- Name: COLUMN mechanical_inspection_report.dim1_observed_value; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.dim1_observed_value IS 'First dimensional measurement - observed value';


--
-- Name: COLUMN mechanical_inspection_report.dim1_instrument_used; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.dim1_instrument_used IS 'First dimensional measurement - instrument used';


--
-- Name: COLUMN mechanical_inspection_report.dim1_remarks; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.dim1_remarks IS 'First dimensional measurement - remarks';


--
-- Name: COLUMN mechanical_inspection_report.dim1_upload; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.dim1_upload IS 'First dimensional measurement - uploaded file path';


--
-- Name: COLUMN mechanical_inspection_report.param1_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.param1_name IS 'First parameter name (default: Burrs)';


--
-- Name: COLUMN mechanical_inspection_report.param1_compliance_observation; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.param1_compliance_observation IS 'First parameter - allowed/not allowed';


--
-- Name: COLUMN mechanical_inspection_report.param1_expected; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.param1_expected IS 'First parameter - expected value';


--
-- Name: COLUMN mechanical_inspection_report.param1_remarks; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.param1_remarks IS 'First parameter - remarks/observations';


--
-- Name: COLUMN mechanical_inspection_report.param1_upload; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanical_inspection_report.param1_upload IS 'First parameter - uploaded file path';


--
-- Name: mechanical_inspection_report_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mechanical_inspection_report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mechanical_inspection_report_report_id_seq OWNER TO postgres;

--
-- Name: mechanical_inspection_report_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mechanical_inspection_report_report_id_seq OWNED BY public.mechanical_inspection_report.report_id;


--
-- Name: memo_approval; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.memo_approval (
    approval_id integer NOT NULL,
    memo_id integer NOT NULL,
    user_id integer,
    comments text,
    authentication text,
    attachment_path text,
    status character varying(10) NOT NULL,
    approval_date timestamp without time zone,
    approved_by integer,
    test_date timestamp without time zone,
    CONSTRAINT memo_approval_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'accepted'::character varying, 'rejected'::character varying])::text[])))
);


ALTER TABLE public.memo_approval OWNER TO postgres;

--
-- Name: memo_approval_approval_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.memo_approval_approval_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.memo_approval_approval_id_seq OWNER TO postgres;

--
-- Name: memo_approval_approval_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.memo_approval_approval_id_seq OWNED BY public.memo_approval.approval_id;


--
-- Name: memo_references; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.memo_references (
    ref_id integer NOT NULL,
    memo_id integer,
    ref_doc character varying(255),
    ref_no character varying(255),
    ver double precision,
    rev double precision
);


ALTER TABLE public.memo_references OWNER TO postgres;

--
-- Name: memo_references_ref_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.memo_references_ref_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.memo_references_ref_id_seq OWNER TO postgres;

--
-- Name: memo_references_ref_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.memo_references_ref_id_seq OWNED BY public.memo_references.ref_id;


--
-- Name: memos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.memos (
    memo_id integer NOT NULL,
    from_person text NOT NULL,
    to_person text NOT NULL,
    thru_person text,
    casdic_ref_no character varying,
    dated date,
    wing_proj_ref_no character varying,
    lru_sru_desc text,
    part_number character varying,
    slno_units text[],
    qty_offered integer,
    manufacturer character varying(255),
    drawing_no_rev text,
    source text,
    unit_identification text,
    mechanical_inspn text,
    inspn_test_stage_offered text,
    stte_status text,
    test_stage_cleared text,
    venue text,
    memo_date date,
    name_designation text,
    test_facility character varying(255),
    test_cycle_duration text,
    test_start_on timestamp without time zone,
    test_complete_on timestamp without time zone,
    calibration_status text,
    func_check_initial timestamp without time zone,
    perf_check_during timestamp without time zone,
    func_check_end timestamp without time zone,
    certified text[],
    remarks text,
    submitted_at timestamp without time zone,
    submitted_by integer,
    accepted_at timestamp without time zone,
    accepted_by integer,
    coordinator text,
    memo_status character varying(40) DEFAULT 'not_assigned'::character varying,
    template_id integer,
    qa_remarks text,
    qa_signature text,
    CONSTRAINT memos_memo_status_check CHECK (((memo_status)::text = ANY ((ARRAY['assigned'::character varying, 'not_assigned'::character varying, 'rejected'::character varying, 'successfully_completed'::character varying, 'completed_with_observations'::character varying, 'test_not_conducted'::character varying, 'test_failed'::character varying, 'completed with obs'::character varying])::text[])))
);


ALTER TABLE public.memos OWNER TO postgres;

--
-- Name: COLUMN memos.template_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.memos.template_id IS 'Foreign key reference to report_templates table for assigned template';


--
-- Name: memos_memo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.memos_memo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.memos_memo_id_seq OWNER TO postgres;

--
-- Name: memos_memo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.memos_memo_id_seq OWNED BY public.memos.memo_id;


--
-- Name: news_updates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news_updates (
    id integer NOT NULL,
    news_text text NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    hidden boolean DEFAULT false
);


ALTER TABLE public.news_updates OWNER TO postgres;

--
-- Name: news_updates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.news_updates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.news_updates_id_seq OWNER TO postgres;

--
-- Name: news_updates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.news_updates_id_seq OWNED BY public.news_updates.id;


--
-- Name: plan_doc_assignment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan_doc_assignment (
    assignment_id integer NOT NULL,
    document_id integer NOT NULL,
    user_id integer NOT NULL,
    assigned_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.plan_doc_assignment OWNER TO postgres;

--
-- Name: plan_doc_assignment_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.plan_doc_assignment_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.plan_doc_assignment_assignment_id_seq OWNER TO postgres;

--
-- Name: plan_doc_assignment_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.plan_doc_assignment_assignment_id_seq OWNED BY public.plan_doc_assignment.assignment_id;


--
-- Name: plan_documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan_documents (
    document_id integer NOT NULL,
    lru_id integer NOT NULL,
    document_number character varying(50) NOT NULL,
    version character varying(10),
    revision character varying(3),
    doc_ver character varying(2),
    uploaded_by integer NOT NULL,
    upload_date timestamp without time zone DEFAULT now(),
    file_path character varying(255) NOT NULL,
    status character varying(50) DEFAULT 'not assigned'::character varying,
    is_active boolean DEFAULT true,
    original_filename character varying(255),
    file_size bigint,
    file_type character varying(50),
    is_approved boolean DEFAULT false,
    approved_by integer,
    approved_at timestamp without time zone,
    document_type integer,
    CONSTRAINT plan_documents_doc_ver_check CHECK ((((doc_ver)::text ~ '^v[0-9]+$'::text) OR ((doc_ver)::text ~ '^[0-9]+$'::text) OR ((doc_ver)::text ~ '^[A-Z]{1,2}$'::text))),
    CONSTRAINT plan_documents_status_check CHECK ((TRIM(BOTH FROM status) = ANY (ARRAY['not accepted'::text, 'accepted with observations'::text, 'accepted'::text, 'not assigned'::text, 'assigned'::text])))
);


ALTER TABLE public.plan_documents OWNER TO postgres;

--
-- Name: COLUMN plan_documents.document_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.plan_documents.document_type IS 'Foreign key to document_types table - categorizes the document type';


--
-- Name: plan_documents_document_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.plan_documents_document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.plan_documents_document_id_seq OWNER TO postgres;

--
-- Name: plan_documents_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.plan_documents_document_id_seq OWNED BY public.plan_documents.document_id;


--
-- Name: project_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_users (
    project_user_id integer NOT NULL,
    project_id integer NOT NULL,
    user_id integer NOT NULL,
    assigned_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.project_users OWNER TO postgres;

--
-- Name: project_users_project_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_users_project_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_users_project_user_id_seq OWNER TO postgres;

--
-- Name: project_users_project_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_users_project_user_id_seq OWNED BY public.project_users.project_user_id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    project_id integer NOT NULL,
    project_name character varying(50) NOT NULL,
    created_by integer NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    project_date date,
    project_director character varying(100),
    deputy_project_director character varying(100),
    qa_manager character varying(100),
    project_director_id integer,
    deputy_project_director_id integer,
    qa_manager_id integer
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- Name: COLUMN projects.project_director; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.projects.project_director IS 'Project Director name - supports text with spaces';


--
-- Name: COLUMN projects.deputy_project_director; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.projects.deputy_project_director IS 'Deputy Project Director name - supports text with spaces';


--
-- Name: COLUMN projects.qa_manager; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.projects.qa_manager IS 'QA Manager name - supports text with spaces';


--
-- Name: projects_project_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.projects_project_id_seq OWNER TO postgres;

--
-- Name: projects_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_project_id_seq OWNED BY public.projects.project_id;


--
-- Name: raw_material_inspection_report; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.raw_material_inspection_report (
    report_id integer NOT NULL,
    project_name text,
    report_ref_no character varying(100),
    memo_ref_no character varying(100),
    lru_name text,
    sru_name text,
    dp_name text,
    part_no character varying(100),
    inspection_stage text,
    test_venue text,
    quantity integer,
    sl_nos text,
    serial_number character varying(100),
    start_date date,
    end_date date,
    dated1 date,
    dated2 date,
    applicability1 character varying(10) DEFAULT 'A'::character varying,
    compliance1 character varying(10),
    rem1 character varying(20),
    upload1 text,
    applicability2 character varying(10) DEFAULT 'A'::character varying,
    compliance2 character varying(10),
    rem2 character varying(20),
    upload2 text,
    applicability3 character varying(10) DEFAULT 'NA'::character varying,
    compliance3 character varying(10),
    rem3 character varying(20),
    upload3 text,
    applicability4 character varying(10) DEFAULT 'A'::character varying,
    compliance4 character varying(10),
    rem4 character varying(20),
    upload4 text,
    applicability5 character varying(10) DEFAULT 'NA'::character varying,
    compliance5 character varying(10),
    rem5 character varying(20),
    upload5 text,
    applicability6 character varying(10) DEFAULT 'A'::character varying,
    compliance6 character varying(10),
    rem6 character varying(20),
    upload6 text,
    applicability7 character varying(10) DEFAULT 'NA'::character varying,
    compliance7 character varying(10),
    rem7 character varying(20),
    upload7 text,
    overall_status text,
    quality_rating integer,
    recommendations text,
    prepared_by text,
    verified_by text,
    approved_by text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT raw_material_inspection_report_applicability1_check CHECK (((applicability1)::text = ANY ((ARRAY['A'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_applicability2_check CHECK (((applicability2)::text = ANY ((ARRAY['A'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_applicability3_check CHECK (((applicability3)::text = ANY ((ARRAY['A'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_applicability4_check CHECK (((applicability4)::text = ANY ((ARRAY['A'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_applicability5_check CHECK (((applicability5)::text = ANY ((ARRAY['A'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_applicability6_check CHECK (((applicability6)::text = ANY ((ARRAY['A'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_applicability7_check CHECK (((applicability7)::text = ANY ((ARRAY['A'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_compliance1_check CHECK (((compliance1)::text = ANY ((ARRAY['YES'::character varying, 'NO'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_compliance2_check CHECK (((compliance2)::text = ANY ((ARRAY['YES'::character varying, 'NO'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_compliance3_check CHECK (((compliance3)::text = ANY ((ARRAY['YES'::character varying, 'NO'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_compliance4_check CHECK (((compliance4)::text = ANY ((ARRAY['YES'::character varying, 'NO'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_compliance5_check CHECK (((compliance5)::text = ANY ((ARRAY['YES'::character varying, 'NO'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_compliance6_check CHECK (((compliance6)::text = ANY ((ARRAY['YES'::character varying, 'NO'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_compliance7_check CHECK (((compliance7)::text = ANY ((ARRAY['YES'::character varying, 'NO'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_rem1_check CHECK (((rem1)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_rem2_check CHECK (((rem2)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_rem3_check CHECK (((rem3)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_rem4_check CHECK (((rem4)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_rem5_check CHECK (((rem5)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_rem6_check CHECK (((rem6)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[]))),
    CONSTRAINT raw_material_inspection_report_rem7_check CHECK (((rem7)::text = ANY ((ARRAY['OK'::character varying, 'NOT OK'::character varying, 'NA'::character varying])::text[])))
);


ALTER TABLE public.raw_material_inspection_report OWNER TO postgres;

--
-- Name: raw_material_inspection_report_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.raw_material_inspection_report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.raw_material_inspection_report_report_id_seq OWNER TO postgres;

--
-- Name: raw_material_inspection_report_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.raw_material_inspection_report_report_id_seq OWNED BY public.raw_material_inspection_report.report_id;


--
-- Name: report_observations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_observations (
    obs_id integer NOT NULL,
    report_id integer NOT NULL,
    s_no integer NOT NULL,
    category character varying(10),
    observation text NOT NULL,
    CONSTRAINT report_observations_category_check CHECK (((category)::text = ANY ((ARRAY['major'::character varying, 'minor'::character varying])::text[])))
);


ALTER TABLE public.report_observations OWNER TO postgres;

--
-- Name: report_observations_obs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_observations_obs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.report_observations_obs_id_seq OWNER TO postgres;

--
-- Name: report_observations_obs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_observations_obs_id_seq OWNED BY public.report_observations.obs_id;


--
-- Name: report_templates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_templates (
    template_id integer NOT NULL,
    template_name character varying(50) NOT NULL
);


ALTER TABLE public.report_templates OWNER TO postgres;

--
-- Name: report_templates_template_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_templates_template_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.report_templates_template_id_seq OWNER TO postgres;

--
-- Name: report_templates_template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_templates_template_id_seq OWNED BY public.report_templates.template_id;


--
-- Name: reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reports (
    report_id integer NOT NULL,
    project_id integer NOT NULL,
    lru_id integer NOT NULL,
    serial_id integer NOT NULL,
    inspection_stage text,
    date_of_review date,
    review_venue text,
    reference_document integer,
    memo_id integer,
    status character varying(50) DEFAULT 'ASSIGNED'::character varying,
    created_at timestamp without time zone DEFAULT now(),
    content text DEFAULT 'Report not yet completed'::text,
    template_id integer,
    is_completed boolean DEFAULT false,
    completed_at timestamp without time zone,
    filled_data jsonb,
    CONSTRAINT reports_status_check CHECK (((status)::text = ANY ((ARRAY['ASSIGNED'::character varying, 'SUCCESSFULLY COMPLETED'::character varying, 'TEST NOT CONDUCTED'::character varying, 'TEST FAILED'::character varying])::text[])))
);


ALTER TABLE public.reports OWNER TO postgres;

--
-- Name: TABLE reports; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.reports IS 'Main table for storing inspection reports';


--
-- Name: COLUMN reports.project_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.project_id IS 'Reference to the project this report belongs to';


--
-- Name: COLUMN reports.lru_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.lru_id IS 'Reference to the LRU being inspected';


--
-- Name: COLUMN reports.inspection_stage; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.inspection_stage IS 'Stage of inspection (e.g., Stage 1, Stage 2, etc.)';


--
-- Name: COLUMN reports.memo_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.memo_id IS 'Reference to the memo that triggered this report';


--
-- Name: COLUMN reports.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.status IS 'Current status of the report (pending, completed, etc.)';


--
-- Name: COLUMN reports.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.created_at IS 'Timestamp when the report was created';


--
-- Name: COLUMN reports.content; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.content IS 'Report content - initially shows "Report not yet completed"';


--
-- Name: COLUMN reports.template_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.template_id IS 'Reference to the report template used';


--
-- Name: COLUMN reports.is_completed; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.is_completed IS 'Whether the report has been completed';


--
-- Name: COLUMN reports.completed_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.reports.completed_at IS 'Timestamp when the report was completed';


--
-- Name: reports_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reports_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reports_report_id_seq OWNER TO postgres;

--
-- Name: reports_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reports_report_id_seq OWNED BY public.reports.report_id;


--
-- Name: review_comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.review_comments (
    comment_id integer NOT NULL,
    review_id integer NOT NULL,
    commented_by integer NOT NULL,
    comment_text text NOT NULL,
    classification character varying(10) NOT NULL,
    justification text,
    status character varying(10) DEFAULT 'open'::character varying,
    "timestamp" timestamp without time zone DEFAULT now(),
    CONSTRAINT review_comments_classification_check CHECK (((classification)::text = ANY ((ARRAY['major'::character varying, 'minor'::character varying])::text[]))),
    CONSTRAINT review_comments_status_check CHECK (((status)::text = ANY ((ARRAY['open'::character varying, 'resolved'::character varying])::text[])))
);


ALTER TABLE public.review_comments OWNER TO postgres;

--
-- Name: review_comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.review_comments_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.review_comments_comment_id_seq OWNER TO postgres;

--
-- Name: review_comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.review_comments_comment_id_seq OWNED BY public.review_comments.comment_id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_role_id_seq OWNER TO postgres;

--
-- Name: roles_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;


--
-- Name: serial_numbers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.serial_numbers (
    serial_id integer NOT NULL,
    lru_id integer NOT NULL,
    serial_number character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.serial_numbers OWNER TO postgres;

--
-- Name: serial_numbers_serial_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.serial_numbers_serial_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.serial_numbers_serial_id_seq OWNER TO postgres;

--
-- Name: serial_numbers_serial_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.serial_numbers_serial_id_seq OWNED BY public.serial_numbers.serial_id;


--
-- Name: shared_memos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shared_memos (
    share_id integer NOT NULL,
    memo_id integer NOT NULL,
    shared_by integer NOT NULL,
    shared_with integer NOT NULL,
    shared_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.shared_memos OWNER TO postgres;

--
-- Name: shared_memos_share_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shared_memos_share_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shared_memos_share_id_seq OWNER TO postgres;

--
-- Name: shared_memos_share_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shared_memos_share_id_seq OWNED BY public.shared_memos.share_id;


--
-- Name: sub_tests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sub_tests (
    sub_test_id integer NOT NULL,
    group_id integer NOT NULL,
    sub_test_name character varying(200) NOT NULL,
    sub_test_description text,
    created_at timestamp without time zone DEFAULT now(),
    created_by integer,
    updated_at timestamp without time zone DEFAULT now(),
    updated_by integer
);


ALTER TABLE public.sub_tests OWNER TO postgres;

--
-- Name: sub_tests_sub_test_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sub_tests_sub_test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sub_tests_sub_test_id_seq OWNER TO postgres;

--
-- Name: sub_tests_sub_test_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sub_tests_sub_test_id_seq OWNED BY public.sub_tests.sub_test_id;


--
-- Name: tech_support_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tech_support_requests (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    issue_date date NOT NULL,
    issue_description text NOT NULL,
    status character varying(50) DEFAULT 'pending'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status_updated_by integer,
    status_updated_at timestamp without time zone
);


ALTER TABLE public.tech_support_requests OWNER TO postgres;

--
-- Name: tech_support_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tech_support_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tech_support_requests_id_seq OWNER TO postgres;

--
-- Name: tech_support_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tech_support_requests_id_seq OWNED BY public.tech_support_requests.id;


--
-- Name: test_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_groups (
    group_id integer NOT NULL,
    group_name character varying(100) NOT NULL,
    group_description text
);


ALTER TABLE public.test_groups OWNER TO postgres;

--
-- Name: test_groups_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.test_groups_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.test_groups_group_id_seq OWNER TO postgres;

--
-- Name: test_groups_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.test_groups_group_id_seq OWNED BY public.test_groups.group_id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_roles (
    user_role_id integer NOT NULL,
    user_id integer NOT NULL,
    role_id integer NOT NULL,
    assigned_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.user_roles OWNER TO postgres;

--
-- Name: user_roles_user_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_roles_user_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_roles_user_role_id_seq OWNER TO postgres;

--
-- Name: user_roles_user_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_roles_user_role_id_seq OWNED BY public.user_roles.user_role_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    name character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    password_hash character varying(75) NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    signature_path character varying(255),
    signature_password character varying(64) NOT NULL,
    deleted boolean DEFAULT false,
    enabled boolean DEFAULT true
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: COLUMN users.signature_password; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.users.signature_password IS 'SHA-256 hashed signature password';


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: activity_logs activity_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs ALTER COLUMN activity_id SET DEFAULT nextval('public.activity_logs_activity_id_seq'::regclass);


--
-- Name: assembled_board_inspection_report report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assembled_board_inspection_report ALTER COLUMN report_id SET DEFAULT nextval('public.assembled_board_inspection_report_report_id_seq'::regclass);


--
-- Name: bare_pcb_inspection_report report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bare_pcb_inspection_report ALTER COLUMN report_id SET DEFAULT nextval('public.bare_pcb_inspection_report_report_id_seq'::regclass);


--
-- Name: bulletins bulletin_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bulletins ALTER COLUMN bulletin_id SET DEFAULT nextval('public.bulletins_bulletin_id_seq'::regclass);


--
-- Name: conformal_coating_inspection_report report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conformal_coating_inspection_report ALTER COLUMN report_id SET DEFAULT nextval('public.conformal_coating_inspection_report_report_id_seq'::regclass);


--
-- Name: cot_screening_inspection_report report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_screening_inspection_report ALTER COLUMN report_id SET DEFAULT nextval('public.cot_screening_inspection_report_report_id_seq'::regclass);


--
-- Name: document_annotations annotation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_annotations ALTER COLUMN annotation_id SET DEFAULT nextval('public.document_annotations_annotation_id_seq'::regclass);


--
-- Name: document_comments comment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_comments ALTER COLUMN comment_id SET DEFAULT nextval('public.document_comments_comment_id_seq'::regclass);


--
-- Name: document_reviews review_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_reviews ALTER COLUMN review_id SET DEFAULT nextval('public.document_reviews_review_id_seq'::regclass);


--
-- Name: document_types type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_types ALTER COLUMN type_id SET DEFAULT nextval('public.document_types_type_id_seq'::regclass);


--
-- Name: document_version version_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_version ALTER COLUMN version_id SET DEFAULT nextval('public.document_version_version_id_seq'::regclass);


--
-- Name: iqa_observation_reports report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iqa_observation_reports ALTER COLUMN report_id SET DEFAULT nextval('public.iqa_observation_reports_report_id_seq'::regclass);


--
-- Name: kit_of_parts_inspection_report report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kit_of_parts_inspection_report ALTER COLUMN report_id SET DEFAULT nextval('public.kit_of_parts_inspection_report_report_id_seq'::regclass);


--
-- Name: login_logs serial_num; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login_logs ALTER COLUMN serial_num SET DEFAULT nextval('public.login_logs_serial_num_seq'::regclass);


--
-- Name: lrus lru_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lrus ALTER COLUMN lru_id SET DEFAULT nextval('public.lrus_lru_id_seq'::regclass);


--
-- Name: mechanical_inspection_report report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mechanical_inspection_report ALTER COLUMN report_id SET DEFAULT nextval('public.mechanical_inspection_report_report_id_seq'::regclass);


--
-- Name: memo_approval approval_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memo_approval ALTER COLUMN approval_id SET DEFAULT nextval('public.memo_approval_approval_id_seq'::regclass);


--
-- Name: memo_references ref_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memo_references ALTER COLUMN ref_id SET DEFAULT nextval('public.memo_references_ref_id_seq'::regclass);


--
-- Name: memos memo_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memos ALTER COLUMN memo_id SET DEFAULT nextval('public.memos_memo_id_seq'::regclass);


--
-- Name: news_updates id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_updates ALTER COLUMN id SET DEFAULT nextval('public.news_updates_id_seq'::regclass);


--
-- Name: plan_doc_assignment assignment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_doc_assignment ALTER COLUMN assignment_id SET DEFAULT nextval('public.plan_doc_assignment_assignment_id_seq'::regclass);


--
-- Name: plan_documents document_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_documents ALTER COLUMN document_id SET DEFAULT nextval('public.plan_documents_document_id_seq'::regclass);


--
-- Name: project_users project_user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_users ALTER COLUMN project_user_id SET DEFAULT nextval('public.project_users_project_user_id_seq'::regclass);


--
-- Name: projects project_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN project_id SET DEFAULT nextval('public.projects_project_id_seq'::regclass);


--
-- Name: raw_material_inspection_report report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_material_inspection_report ALTER COLUMN report_id SET DEFAULT nextval('public.raw_material_inspection_report_report_id_seq'::regclass);


--
-- Name: report_observations obs_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_observations ALTER COLUMN obs_id SET DEFAULT nextval('public.report_observations_obs_id_seq'::regclass);


--
-- Name: report_templates template_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_templates ALTER COLUMN template_id SET DEFAULT nextval('public.report_templates_template_id_seq'::regclass);


--
-- Name: reports report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports ALTER COLUMN report_id SET DEFAULT nextval('public.reports_report_id_seq'::regclass);


--
-- Name: review_comments comment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_comments ALTER COLUMN comment_id SET DEFAULT nextval('public.review_comments_comment_id_seq'::regclass);


--
-- Name: roles role_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);


--
-- Name: serial_numbers serial_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.serial_numbers ALTER COLUMN serial_id SET DEFAULT nextval('public.serial_numbers_serial_id_seq'::regclass);


--
-- Name: shared_memos share_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_memos ALTER COLUMN share_id SET DEFAULT nextval('public.shared_memos_share_id_seq'::regclass);


--
-- Name: sub_tests sub_test_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_tests ALTER COLUMN sub_test_id SET DEFAULT nextval('public.sub_tests_sub_test_id_seq'::regclass);


--
-- Name: tech_support_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tech_support_requests ALTER COLUMN id SET DEFAULT nextval('public.tech_support_requests_id_seq'::regclass);


--
-- Name: test_groups group_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_groups ALTER COLUMN group_id SET DEFAULT nextval('public.test_groups_group_id_seq'::regclass);


--
-- Name: user_roles user_role_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN user_role_id SET DEFAULT nextval('public.user_roles_user_role_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: activity_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.activity_logs (activity_id, project_id, activity_performed, performed_by, "timestamp", additional_info, notified_user_id, is_read, notification_type) FROM stdin;
1	\N	User Updated	1002	2025-10-15 15:45:20.267791	ID:1112|Name:Mohana|User 'Mohana' (ID: 1112) was updated: name to 'mohana', role to ID 5	\N	f	\N
2	\N	Memo Assigned	1004	2025-10-15 15:54:28.302993	ID:4|Name:lru|Memo 'lru' (ID: 4) was accepted	\N	f	\N
3	\N	User Updated	1002	2025-10-15 16:10:20.573432	ID:1004|Name:Mohan|User 'Mohan' (ID: 1004) was updated: password, role to ID 2, signature	\N	f	\N
4	\N	Memo Assigned	1004	2025-10-15 16:11:13.233867	ID:4|Name:lru|Memo 'lru' (ID: 4) was accepted	\N	f	\N
5	1	Project Updated	1002	2025-10-17 12:52:42.233336	ID:1|Name:Flight Control System|Project 'Flight Control System' was updated	\N	f	\N
6	\N	Memo Submitted	1005	2025-10-24 14:47:11.908227	ID:14|Name:testing orm -2|Memo 'testing orm -2' (ID: 14) was submitted	\N	f	\N
7	\N	Memo Assigned	1004	2025-10-24 14:48:41.28246	ID:14|Name:testing orm -2|Memo 'testing orm -2' (ID: 14) was accepted	\N	f	\N
8	\N	Memo Rejected	1004	2025-10-24 15:24:44.46653	ID:14|Name:testing orm -2|Memo 'testing orm -2' (ID: 14) was rejected	\N	f	\N
9	5500	Project Added	1011	2025-10-27 10:47:56.88197	ID:5500|Name:dharshini|Project 'dharshini' created with 2 LRUs	\N	f	\N
10	\N	User Added	1002	2025-10-27 10:49:49.36685	ID:1212|Name:dharshini|User 'dharshini' (ID: 1212) with role ID 3 was created	\N	f	\N
11	\N	Memo Submitted	1005	2025-10-27 11:08:33.648403	ID:15|Name:dharsh 1|Memo 'dharsh 1' (ID: 15) was submitted	\N	f	\N
12	\N	Memo Assigned	1004	2025-10-27 11:09:51.022408	ID:15|Name:dharsh 1|Memo 'dharsh 1' (ID: 15) was accepted	\N	f	\N
13	121212	Project Added	1011	2025-10-27 16:32:53.34539	ID:121212|Name:demo|Project 'demo' created with 1 LRUs	\N	f	\N
14	111111	Project Added	1011	2025-10-28 11:36:42.367232	ID:111111|Name:thanish|Project 'thanish' created with 1 LRUs	\N	f	\N
16	111111	New Project Created	1011	2025-10-28 11:36:42.383167	New project 'thanish' (ID: 111111) has been created and requires your attention.	9999	f	project_created
15	111111	New Project Created	1011	2025-10-28 11:36:42.379893	New project 'thanish' (ID: 111111) has been created and requires your attention.	1003	t	project_created
18	12344321	Project Added	1011	2025-10-28 12:02:18.95708	ID:12344321|Name:pg1|Project 'pg1' created with 1 LRUs	\N	f	\N
20	12344321	New Project Created	1011	2025-10-28 12:02:18.970788	New project 'pg1' (ID: 12344321) has been created and requires your attention.	9999	f	project_created
19	12344321	New Project Created	1011	2025-10-28 12:02:18.964104	New project 'pg1' (ID: 12344321) has been created and requires your attention.	1003	t	project_created
21	12344321	New Project Created	1011	2025-10-28 12:02:18.976265	New project 'pg1' (ID: 12344321) has been created and requires your attention.	1004	t	project_created
17	111111	New Project Created	1011	2025-10-28 11:36:42.386278	New project 'thanish' (ID: 111111) has been created and requires your attention.	1004	t	project_created
24	\N	New Tech Support Request	1004	2025-10-28 12:06:55.703091	New tech support request #14 from Mohan (User ID: 1004). Issue: notification	1007	f	tech_support_request
22	\N	New Tech Support Request	1004	2025-10-28 12:06:55.694865	New tech support request #14 from Mohan (User ID: 1004). Issue: notification	1011	t	tech_support_request
23	\N	New Tech Support Request	1004	2025-10-28 12:06:55.702317	New tech support request #14 from Mohan (User ID: 1004). Issue: notification	1002	t	tech_support_request
27	5500	Project Assigned	1003	2025-10-28 12:32:44.447763	You have been assigned to project 'dharshini' (ID: 5500) by Mahadev M.	1112	f	project_assigned
28	12344321	Document Uploaded (Version A)	1005	2025-10-28 12:51:13.645555	New document 'doc54' version v1.0 (doc_ver: A) uploaded for LRU 'pglru' in project 'pg1' by user ID 1005.	\N	f	\N
29	12344321	New Document Uploaded (Version A)	1005	2025-10-28 12:51:13.655704	New document 'doc54' version v1.0 uploaded for LRU 'pglru' in project 'pg1'. Review required.	9999	f	document_upload_version_a
30	12344321	New Document Uploaded (Version A)	1005	2025-10-28 12:51:13.661043	New document 'doc54' version v1.0 uploaded for LRU 'pglru' in project 'pg1'. Review required.	1004	t	document_upload_version_a
31	12344321	Reviewer Assigned to Plan Document	1002	2025-10-28 14:13:26.357219	QA Head assigned dharshini to review plan documents for LRU 'pglru' in project 'pg1'.	\N	f	\N
34	111111	Reviewer Assigned to Plan Document	1002	2025-10-28 14:19:38.624536	QA Head assigned saravana to review plan documents for LRU 'thanish1' in project 'thanish'.	\N	f	\N
35	111111	Plan Document Assignment	1002	2025-10-28 14:19:38.634453	You have been assigned to review plan documents for LRU 'thanish1' in project 'thanish' by Sudhiksha M K.	1008	f	plan_document_assigned
36	12344321	Comment Added to Plan Document	1212	2025-10-28 14:24:35.901777	Reviewer dharshini added a comment to document 'b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf' in LRU 'pglru' for project 'pg1'.	\N	f	\N
38	12344321	Comment Accepted	1005	2025-10-28 14:30:04.454728	Mahaashri C V accepted a comment on document 'b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf' (46) in LRU 'pglru' for project 'pg1'.	\N	f	\N
40	12344321	Comment Added to Plan Document	1212	2025-10-28 14:30:54.871863	Reviewer dharshini added a comment to document 'b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf' in LRU 'pglru' for project 'pg1'.	\N	f	\N
41	12344321	New Comment on Plan Document	1212	2025-10-28 14:30:54.883486	Reviewer dharshini added a comment to document 'b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf' in LRU 'pglru' of project 'pg1'. Please review and address the feedback.	1005	t	plan_document_comment
42	12344321	Comment Rejected	1005	2025-10-28 14:32:10.474553	Mahaashri C V rejected a comment on document 'b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf' (46) in LRU 'pglru' for project 'pg1'.	\N	f	\N
44	12344321	Document Version v1.0 Uploaded	1005	2025-10-28 14:36:44.384637	New version 'v1.0' (doc_ver: B) of document 'doc332' uploaded for LRU 'pglru' in project 'pg1' by user ID 1005. Assigned reviewer: dharshini.	\N	f	\N
39	12344321	Your Comment Was Accepted	1005	2025-10-28 14:30:04.470103	Designer Mahaashri C V accepted your comment on document 'b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf' (46) in LRU 'pglru' of project 'pg1'. Justification: good	1212	t	comment_accepted
43	12344321	Your Comment Was Rejected	1005	2025-10-28 14:32:10.481045	Designer Mahaashri C V rejected your comment on document 'b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf' (46) in LRU 'pglru' of project 'pg1'. Justification: so wat	1212	t	comment_rejected
32	12344321	Plan Document Assignment	1002	2025-10-28 14:13:26.367803	You have been assigned to review plan documents for LRU 'pglru' in project 'pg1' by Sudhiksha M K.	1212	t	plan_document_assigned
33	111111	Project Assigned	1003	2025-10-28 14:19:10.01024	You have been assigned to project 'thanish' (ID: 111111) by Mahadev M.	1112	t	project_assigned
37	12344321	New Comment on Plan Document	1212	2025-10-28 14:24:35.917056	Reviewer dharshini added a comment to document 'b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf' in LRU 'pglru' of project 'pg1'. Please review and address the feedback.	1005	t	plan_document_comment
26	111111	Project Assigned	1003	2025-10-28 12:31:22.778203	You have been assigned to project 'thanish' (ID: 111111) by Mahadev M.	1005	t	project_assigned
168	\N	TECH_SUPPORT_STATUS_UPDATE	1515	2025-11-13 16:16:18.093084	Updated tech support request #15 status to resolved	\N	f	\N
169	3	Project Assigned	1003	2025-11-13 16:17:54.195437	You have been assigned to project 'project3' (ID: 3) by Mahadev M.	1112	f	project_assigned
46	5500	Document Uploaded (Version A)	1112	2025-10-28 14:39:13.48526	New document 'doc 1111' version v1.0 (doc_ver: A) uploaded for LRU 'dharsh 2' in project 'dharshini' by user ID 1112.	\N	f	\N
47	5500	New Document Uploaded (Version A)	1112	2025-10-28 14:39:13.496557	New document 'doc 1111' version v1.0 uploaded for LRU 'dharsh 2' in project 'dharshini'. Review required.	9999	f	document_upload_version_a
48	5500	New Document Uploaded (Version A)	1112	2025-10-28 14:39:13.505802	New document 'doc 1111' version v1.0 uploaded for LRU 'dharsh 2' in project 'dharshini'. Review required.	1004	t	document_upload_version_a
45	12344321	New Document Version Uploaded	1005	2025-10-28 14:36:44.395521	New version 'v1.0' of document 'doc332' uploaded for LRU 'pglru' in project 'pg1'. Please review.	1212	t	document_upload_new_version
50	121212	Comment Added to Plan Document	1212	2025-10-28 15:00:59.449064	Reviewer dharshini added a comment to document 'cb366ba1-0256-4cda-b9c1-3664b9f13032.pdf' in LRU 'demo_lru' for project 'demo'.	\N	f	\N
51	121212	Comment Rejected	1003	2025-10-28 15:02:49.102143	Mahadev M rejected a comment on document 'cb366ba1-0256-4cda-b9c1-3664b9f13032.pdf' (44) in LRU 'demo_lru' for project 'demo'.	\N	f	\N
52	121212	Your Comment Was Rejected	1003	2025-10-28 15:02:49.126161	Designer Mahadev M rejected your comment on document 'cb366ba1-0256-4cda-b9c1-3664b9f13032.pdf' (44) in LRU 'demo_lru' of project 'demo'. Justification: check 1	1212	f	comment_rejected
56	5500	Reviewer Assigned to Plan Document	1002	2025-10-28 15:23:15.245821	QA Head assigned dharshini to review plan documents for LRU 'dharsh 2' in project 'dharshini'.	\N	f	\N
57	5500	Plan Document Assignment	1002	2025-10-28 15:23:15.25768	You have been assigned to review plan documents for LRU 'dharsh 2' in project 'dharshini' by Sudhiksha M K.	1212	f	plan_document_assigned
60	5500	Comment Added to Plan Document	1212	2025-10-28 15:28:45.104755	Reviewer dharshini added a comment to document 'c22cb015-6d3a-4911-b7c4-2ded6409dc78.pdf' in LRU 'dharsh 2' for project 'dharshini'.	\N	f	\N
62	5500	New Comment on Plan Document	1212	2025-10-28 15:28:45.121321	Reviewer dharshini added a comment to document 'c22cb015-6d3a-4911-b7c4-2ded6409dc78.pdf' in LRU 'dharsh 2' of project 'dharshini'. Please review and address the feedback.	1112	f	plan_document_comment
63	5500	Comment Accepted	1005	2025-10-28 15:29:10.186381	Mahaashri C V accepted a comment on document 'c22cb015-6d3a-4911-b7c4-2ded6409dc78.pdf' (43) in LRU 'dharsh 2' for project 'dharshini'.	\N	f	\N
64	5500	Your Comment Was Accepted	1005	2025-10-28 15:29:10.203461	Designer Mahaashri C V accepted your comment on document 'c22cb015-6d3a-4911-b7c4-2ded6409dc78.pdf' (43) in LRU 'dharsh 2' of project 'dharshini'. Justification: ok ok	1212	f	comment_accepted
61	5500	New Comment on Plan Document	1212	2025-10-28 15:28:45.119644	Reviewer dharshini added a comment to document 'c22cb015-6d3a-4911-b7c4-2ded6409dc78.pdf' in LRU 'dharsh 2' of project 'dharshini'. Please review and address the feedback.	1005	t	plan_document_comment
67	\N	Memo Submitted	1005	2025-11-01 09:44:52.45125	ID:16|Name:thanish1|Memo 'thanish1' (ID: 16) was submitted	\N	f	\N
68	\N	New Memo Submitted	1005	2025-11-01 09:45:17.097215	Memo ID 16 submitted by user ID 1005. Please review.	9999	f	memo_submitted
69	\N	New Memo Submitted	1005	2025-11-01 09:45:17.099453	Memo ID 16 submitted by user ID 1005. Please review.	1004	t	memo_submitted
70	\N	Report Created	1004	2025-11-01 09:46:27.346965	A report (Serial ID 301) has been created for Memo ID 16.	1003	f	report_created
71	\N	Your Report Created	1004	2025-11-01 09:46:27.388299	A report has been created for your memo (ID 16). Serial ID 301.	1005	f	report_created_submitted_by_designer
72	\N	Memo Assigned	1004	2025-11-01 09:46:27.389959	ID:16|Name:thanish1|Memo 'thanish1' (ID: 16) was accepted	\N	f	\N
73	\N	Memo Accepted	1004	2025-11-01 09:46:27.391082	Memo ID 16 submitted by Mahaashri C V was accepted by QA Head ID 1004.	1003	f	memo_accepted
74	\N	Your Memo Accepted	1004	2025-11-01 09:46:27.393048	Your memo (ID 16) was accepted by QA Head ID 1004.	1005	f	memo_accepted_submitted_by_designer
75	\N	Memo Assigned to You	1004	2025-11-01 09:46:27.394597	You have been assigned to review Memo ID 16 by QA Head ID 1004.	1008	t	memo_assigned
76	\N	Conformal Coating Inspection Report Approved	1004	2025-11-01 17:45:24.998478	Report ID: 14|Report Ref: bnm|Project: ghj|LRU: None|Approved by: Mohan	\N	f	\N
77	\N	Report num : bnm has been approved	1004	2025-11-01 17:45:25.012515	Report ID 14 (Ref: bnm) has been approved by Mohan for project 'ghj', LRU 'None'. Please review.	9999	f	report_approved
79	\N	Conformal Coating Inspection Report Approved	1004	2025-11-03 09:48:48.281137	Report ID: 21|Report Ref: Report 21|Project: Unknown|LRU: Unknown|Approved by: Mohan	\N	f	\N
80	\N	Report num : Report 21 has been approved	1004	2025-11-03 09:48:48.289014	Report ID 21 (Ref: Report 21) has been approved by Mohan for project 'Unknown', LRU 'Unknown'. Please review.	9999	f	report_approved
82	\N	Conformal Coating Inspection Report Approved	1004	2025-11-03 10:08:18.9478	Report ID: 16|Report Ref: nbv|Project: hgfd|LRU: None|Approved by: Mohan	\N	f	\N
83	\N	Report num : nbv has been approved	1004	2025-11-03 10:08:18.955108	Report ID 16 (Ref: nbv) has been approved by Mohan for project 'hgfd', LRU 'None'. Please review.	9999	f	report_approved
85	\N	Conformal Coating Inspection Report Approved	1004	2025-11-03 11:32:35.021091	Report ID: 17|Report Ref: cvbn|Project: dfgh|LRU: None|Approved by: Mohan	\N	f	\N
86	\N	Report num : cvbn has been approved	1004	2025-11-03 11:32:35.032985	Report ID 17 (Ref: cvbn) has been approved by Mohan for project 'dfgh', LRU 'None'. Please review.	9999	f	report_approved
88	\N	Conformal Coating Inspection Report Approved	1004	2025-11-03 11:45:24.455115	Report ID: 18|Report Ref: bvnm,|Project: gfhjkl|LRU: None|Approved by: Mohan	\N	f	\N
89	\N	Report num : bvnm, has been approved	1004	2025-11-03 11:45:24.464749	Report ID 18 (Ref: bvnm,) has been approved by Mohan for project 'gfhjkl', LRU 'None'. Please review.	9999	f	report_approved
91	\N	Kit of Parts Inspection Report Approved	1004	2025-11-03 12:07:04.885616	Report ID: 9|Report Ref: bnm|Project: bvnm|LRU: nk|Approved by: Mohan	\N	f	\N
81	\N	Report num : Report 21 has been approved	1004	2025-11-03 09:48:48.341628	Report ID 21 (Ref: Report 21) has been approved by Mohan for project 'Unknown', LRU 'Unknown'. Please review.	1004	t	report_approved
84	\N	Report num : nbv has been approved	1004	2025-11-03 10:08:19.00485	Report ID 16 (Ref: nbv) has been approved by Mohan for project 'hgfd', LRU 'None'. Please review.	1004	t	report_approved
87	\N	Report num : cvbn has been approved	1004	2025-11-03 11:32:35.103483	Report ID 17 (Ref: cvbn) has been approved by Mohan for project 'dfgh', LRU 'None'. Please review.	1004	t	report_approved
90	\N	Report num : bvnm, has been approved	1004	2025-11-03 11:45:24.535042	Report ID 18 (Ref: bvnm,) has been approved by Mohan for project 'gfhjkl', LRU 'None'. Please review.	1004	t	report_approved
92	\N	Report num : bnm has been approved	1004	2025-11-03 12:07:04.921585	Report ID 9 (Ref: bnm) has been approved by Mohan for project 'bvnm', LRU 'nk'. Please review.	9999	f	report_approved
94	\N	Kit of Parts Inspection Report Approved	1004	2025-11-03 14:15:48.436846	Report ID: 10|Report Ref: 1|Project: aaa|LRU: sss|Approved by: Mohan	\N	f	\N
95	\N	Report num : 1 has been approved	1004	2025-11-03 14:15:48.481195	Report ID 10 (Ref: 1) has been approved by Mohan for project 'aaa', LRU 'sss'. Please review.	9999	f	report_approved
97	\N	User Updated	1002	2025-11-10 11:12:37.06706	ID:1002|Name:Sudhiksha M K|User 'Sudhiksha M K' (ID: 1002) was updated: password, role to ID 1	\N	f	\N
98	100694	Project Added	1002	2025-11-10 11:17:11.640178	ID:100694|Name:manual testing|Project 'manual testing' created with 2 LRUs	\N	f	\N
99	100694	New Project Created	1002	2025-11-10 11:17:11.85747	New project 'manual testing' (ID: 100694) has been created and requires your attention.	1003	f	project_created
100	100694	New Project Created	1002	2025-11-10 11:17:12.02375	New project 'manual testing' (ID: 100694) has been created and requires your attention.	9999	f	project_created
102	100694	Project Updated	1002	2025-11-10 11:17:59.364992	ID:100694|Name:manual testing|Project 'manual testing' was updated	\N	f	\N
103	\N	User Updated	1002	2025-11-10 11:18:44.661297	ID:1011|Name:admin|User 'admin' (ID: 1011) was updated: password, role to ID 1	\N	f	\N
104	\N	User Added	1002	2025-11-10 11:20:17.630139	ID:1616|Name:pradeepa|User 'pradeepa' (ID: 1616) with role ID 5 was created	\N	f	\N
105	\N	User Updated	1002	2025-11-10 11:39:47.537782	ID:1002|Name:Sudhiksha M K|User 'Sudhiksha M K' (ID: 1002) was updated: password, role to ID 1	\N	f	\N
106	\N	TECH_SUPPORT_REQUEST	1002	2025-11-10 11:42:13.269021	Tech support request submitted by sudhiksha (User ID: 1002)	\N	f	\N
107	\N	New Tech Support Request	1002	2025-11-10 11:42:13.44618	New tech support request #15 from sudhiksha (User ID: 1002). Issue: login not working	1007	f	tech_support_request
108	\N	New Tech Support Request	1002	2025-11-10 11:42:13.560845	New tech support request #15 from sudhiksha (User ID: 1002). Issue: login not working	1011	f	tech_support_request
109	\N	New Tech Support Request	1002	2025-11-10 11:42:13.661271	New tech support request #15 from sudhiksha (User ID: 1002). Issue: login not working	1002	f	tech_support_request
110	\N	TECH_SUPPORT_STATUS_UPDATE	1002	2025-11-10 11:42:30.007517	Updated tech support request #15 status to in_progress	\N	f	\N
111	100694	Project Assigned	1003	2025-11-10 12:23:21.945969	You have been assigned to project 'manual testing' (ID: 100694) by Mahadev M.	1005	f	project_assigned
112	100694	Project Assigned	1003	2025-11-10 14:03:02.730124	You have been assigned to project 'manual testing' (ID: 100694) by Mahadev M.	1616	f	project_assigned
113	100694	Document Uploaded (Version A)	1616	2025-11-10 14:05:05.784584	New document 'manualdoc' version v1.0 (doc_ver: A) uploaded for LRU 'manual01' in project 'manual testing' by user ID 1616.	\N	f	\N
114	100694	New Document Uploaded (Version A)	1616	2025-11-10 14:05:05.852446	New document 'manualdoc' version v1.0 uploaded for LRU 'manual01' in project 'manual testing'. Review required.	9999	f	document_upload_version_a
116	100694	Reviewer Assigned to Plan Document	1002	2025-11-10 14:07:07.991219	QA Head assigned dharshini to review plan documents for LRU 'manual01' in project 'manual testing'.	\N	f	\N
117	100694	Plan Document Assignment	1002	2025-11-10 14:07:08.002297	You have been assigned to review plan documents for LRU 'manual01' in project 'manual testing' by Sudhiksha M K.	1212	f	plan_document_assigned
118	100694	Comment Added to Plan Document	1212	2025-11-10 14:08:04.600088	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' for project 'manual testing'.	\N	f	\N
119	100694	New Comment on Plan Document	1212	2025-11-10 14:08:04.606662	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1005	f	plan_document_comment
120	100694	New Comment on Plan Document	1212	2025-11-10 14:08:04.678841	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1616	f	plan_document_comment
121	100694	Comment Added to Plan Document	1212	2025-11-10 14:08:15.943882	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' for project 'manual testing'.	\N	f	\N
122	100694	New Comment on Plan Document	1212	2025-11-10 14:08:15.957128	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1005	f	plan_document_comment
123	100694	New Comment on Plan Document	1212	2025-11-10 14:08:16.060968	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1616	f	plan_document_comment
124	100694	Comment Added to Plan Document	1212	2025-11-10 14:08:29.521963	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' for project 'manual testing'.	\N	f	\N
125	100694	New Comment on Plan Document	1212	2025-11-10 14:08:29.532284	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1005	f	plan_document_comment
126	100694	New Comment on Plan Document	1212	2025-11-10 14:08:29.618348	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1616	f	plan_document_comment
127	100694	Comment Rejected	1616	2025-11-10 14:09:21.999212	pradeepa rejected a comment on document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' (47) in LRU 'manual01' for project 'manual testing'.	\N	f	\N
128	100694	Your Comment Was Rejected	1616	2025-11-10 14:09:22.004052	Designer pradeepa rejected your comment on document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' (47) in LRU 'manual01' of project 'manual testing'. Justification: rej3	1212	f	comment_rejected
129	100694	Comment Accepted	1616	2025-11-10 14:10:10.567565	pradeepa accepted a comment on document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' (47) in LRU 'manual01' for project 'manual testing'.	\N	f	\N
96	\N	Report num : 1 has been approved	1004	2025-11-03 14:15:48.55145	Report ID 10 (Ref: 1) has been approved by Mohan for project 'aaa', LRU 'sss'. Please review.	1004	t	report_approved
101	100694	New Project Created	1002	2025-11-10 11:17:12.102231	New project 'manual testing' (ID: 100694) has been created and requires your attention.	1004	t	project_created
115	100694	New Document Uploaded (Version A)	1616	2025-11-10 14:05:05.932128	New document 'manualdoc' version v1.0 uploaded for LRU 'manual01' in project 'manual testing'. Review required.	1004	t	document_upload_version_a
170	\N	Report Created	1004	2025-11-13 16:19:31.36512	A report (Serial ID 317) has been created for Memo ID 18.	1003	f	report_created
214	\N	User Updated	1002	2025-11-19 12:17:12.443569	ID:1001|Name:Avanthika|User 'Avanthika' (ID: 1001) was updated: password, role to ID 3	\N	f	\N
130	100694	Your Comment Was Accepted	1616	2025-11-10 14:10:10.575116	Designer pradeepa accepted your comment on document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' (47) in LRU 'manual01' of project 'manual testing'. Justification: acc 2	1212	f	comment_accepted
131	100694	Comment Rejected	1616	2025-11-10 14:10:34.135709	pradeepa rejected a comment on document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' (47) in LRU 'manual01' for project 'manual testing'.	\N	f	\N
132	100694	Your Comment Was Rejected	1616	2025-11-10 14:10:34.143164	Designer pradeepa rejected your comment on document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' (47) in LRU 'manual01' of project 'manual testing'. Justification: rej1	1212	f	comment_rejected
133	100694	Document Version v2.0 Uploaded	1616	2025-11-10 14:11:03.427232	New version 'v2.0' (doc_ver: B) of document 'manualdoc' uploaded for LRU 'manual01' in project 'manual testing' by user ID 1616. Assigned reviewer: dharshini.	\N	f	\N
134	100694	New Document Version Uploaded	1616	2025-11-10 14:11:03.446644	New revision 'B' of document 'manualdoc' uploaded for LRU 'manual01' in project 'manual testing'. Please review.	1212	f	document_upload_new_version
135	100694	Comment Added to Plan Document	1212	2025-11-10 14:12:24.093337	Reviewer dharshini added a comment to document 'f5d59013-7837-4b01-8b01-d8f83c0d1bd7.pdf' in LRU 'manual01' for project 'manual testing'.	\N	f	\N
136	100694	New Comment on Plan Document	1212	2025-11-10 14:12:24.107173	Reviewer dharshini added a comment to document 'f5d59013-7837-4b01-8b01-d8f83c0d1bd7.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1005	f	plan_document_comment
137	100694	New Comment on Plan Document	1212	2025-11-10 14:12:24.209995	Reviewer dharshini added a comment to document 'f5d59013-7837-4b01-8b01-d8f83c0d1bd7.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1616	f	plan_document_comment
138	100694	Comment Rejected	1616	2025-11-10 14:13:08.704253	pradeepa rejected a comment on document 'f5d59013-7837-4b01-8b01-d8f83c0d1bd7.pdf' (47) in LRU 'manual01' for project 'manual testing'.	\N	f	\N
139	100694	Your Comment Was Rejected	1616	2025-11-10 14:13:08.708176	Designer pradeepa rejected your comment on document 'f5d59013-7837-4b01-8b01-d8f83c0d1bd7.pdf' (47) in LRU 'manual01' of project 'manual testing'. Justification: rewj	1212	f	comment_rejected
140	100694	Comment Added to Plan Document	1212	2025-11-10 14:13:44.895543	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' for project 'manual testing'.	\N	f	\N
141	100694	New Comment on Plan Document	1212	2025-11-10 14:13:44.903033	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1005	f	plan_document_comment
142	100694	New Comment on Plan Document	1212	2025-11-10 14:13:44.970365	Reviewer dharshini added a comment to document 'b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf' in LRU 'manual01' of project 'manual testing'. Please review and address the feedback.	1616	f	plan_document_comment
143	\N	Memo Submitted	1616	2025-11-11 10:15:55.065543	ID:17|Name:manual02|Memo 'manual02' (ID: 17) was submitted	\N	f	\N
144	\N	New Memo Submitted	1616	2025-11-11 10:15:55.192463	Memo ID 17 submitted by user ID 1616. Please review.	9999	f	memo_submitted
145	\N	New Memo Submitted	1616	2025-11-11 10:15:55.279494	Memo ID 17 submitted by user ID 1616. Please review.	1004	f	memo_submitted
78	\N	Report num : bnm has been approved	1004	2025-11-01 17:45:25.013799	Report ID 14 (Ref: bnm) has been approved by Mohan for project 'ghj', LRU 'None'. Please review.	1004	t	report_approved
93	\N	Report num : bnm has been approved	1004	2025-11-03 12:07:05.118834	Report ID 9 (Ref: bnm) has been approved by Mohan for project 'bvnm', LRU 'nk'. Please review.	1004	t	report_approved
146	\N	Report Created	1004	2025-11-11 10:21:30.943283	A report (Serial ID 327) has been created for Memo ID 17.	1003	f	report_created
147	\N	Your Report Created	1004	2025-11-11 10:21:31.078421	A report has been created for your memo (ID 17). Serial ID 327.	1616	f	report_created_submitted_by_designer
148	\N	Memo Assigned	1004	2025-11-11 10:21:31.218085	ID:17|Name:manual02|Memo 'manual02' (ID: 17) was accepted	\N	f	\N
149	\N	Memo Accepted	1004	2025-11-11 10:21:31.350899	Memo ID 17 submitted by pradeepa was accepted by QA Head ID 1004.	1003	f	memo_accepted
150	\N	Your Memo Accepted	1004	2025-11-11 10:21:31.50704	Your memo (ID 17) was accepted by QA Head ID 1004.	1616	f	memo_accepted_submitted_by_designer
151	\N	Memo Assigned to You	1004	2025-11-11 10:21:31.673343	You have been assigned to review Memo ID 17 by QA Head ID 1004.	1212	f	memo_assigned
152	\N	Memo Submitted	1616	2025-11-11 10:25:27.620039	ID:18|Name:manual01|Memo 'manual01' (ID: 18) was submitted	\N	f	\N
153	\N	New Memo Submitted	1616	2025-11-11 10:25:27.910869	Memo ID 18 submitted by user ID 1616. Please review.	9999	f	memo_submitted
154	\N	New Memo Submitted	1616	2025-11-11 10:25:27.982706	Memo ID 18 submitted by user ID 1616. Please review.	1004	f	memo_submitted
155	\N	Memo Rejected	1004	2025-11-11 10:32:05.223544	Memo ID 18 submitted by pradeepa was rejected by QA Head ID 1004.	1003	f	memo_rejected
156	\N	Your Memo Rejected	1004	2025-11-11 10:32:05.298863	Your memo (ID 18) was rejected by QA Head ID 1004.	1616	f	memo_rejected
157	\N	Memo Rejected	1004	2025-11-11 10:32:19.409922	Memo ID 18 submitted by pradeepa was rejected by QA Head ID 1004.	1003	f	memo_rejected
158	\N	Your Memo Rejected	1004	2025-11-11 10:32:19.487284	Your memo (ID 18) was rejected by QA Head ID 1004.	1616	f	memo_rejected
159	\N	Memo Rejected	1004	2025-11-11 10:36:31.542148	Memo ID 18 submitted by pradeepa was rejected by QA Head ID 1004.	1003	f	memo_rejected
160	\N	Your Memo Rejected	1004	2025-11-11 10:36:31.61535	Your memo (ID 18) was rejected by QA Head ID 1004.	1616	f	memo_rejected
161	\N	Conformal Coating Inspection Report Approved	1004	2025-11-11 12:11:17.558069	Report ID: 19|Report Ref: ytuio|Project: ERP QA Automation Tool|LRU: ghj|Approved by: Mohan	\N	f	\N
162	\N	Report num : ytuio has been approved	1004	2025-11-11 12:11:17.575751	Report ID 19 (Ref: ytuio) has been approved by Mohan for project 'ERP QA Automation Tool', LRU 'ghj'. Please review.	9999	f	report_approved
163	\N	Report num : ytuio has been approved	1004	2025-11-11 12:11:17.669044	Report ID 19 (Ref: ytuio) has been approved by Mohan for project 'ERP QA Automation Tool', LRU 'ghj'. Please review.	1004	f	report_approved
164	\N	Kit of Parts Inspection Report Approved	1004	2025-11-11 14:20:13.776639	Report ID: 11|Report Ref: cxvbn|Project: ERP QA Automation Tool|LRU: hjk|Approved by: Mohan	\N	f	\N
165	\N	Report num : cxvbn has been approved	1004	2025-11-11 14:20:13.786296	Report ID 11 (Ref: cxvbn) has been approved by Mohan for project 'ERP QA Automation Tool', LRU 'hjk'. Please review.	9999	f	report_approved
166	\N	Report num : cxvbn has been approved	1004	2025-11-11 14:20:13.849582	Report ID 11 (Ref: cxvbn) has been approved by Mohan for project 'ERP QA Automation Tool', LRU 'hjk'. Please review.	1004	f	report_approved
167	\N	User Added	1002	2025-11-13 16:07:49.129193	ID:1515|Name:yogesh|User 'yogesh' (ID: 1515) with role ID 1 was created	\N	f	\N
171	\N	Your Report Created	1004	2025-11-13 16:19:31.583485	A report has been created for your memo (ID 18). Serial ID 317.	1616	f	report_created_submitted_by_designer
172	\N	Memo Assigned	1004	2025-11-13 16:19:31.803675	ID:18|Name:manual01|Memo 'manual01' (ID: 18) was accepted	\N	f	\N
173	\N	Memo Accepted	1004	2025-11-13 16:19:32.049021	Memo ID 18 submitted by pradeepa was accepted by QA Head ID 1004.	1003	f	memo_accepted
174	\N	Your Memo Accepted	1004	2025-11-13 16:19:32.283516	Your memo (ID 18) was accepted by QA Head ID 1004.	1616	f	memo_accepted_submitted_by_designer
175	\N	Memo Assigned to You	1004	2025-11-13 16:19:32.5259	You have been assigned to review Memo ID 18 by QA Head ID 1004.	1001	f	memo_assigned
176	\N	Memo Submitted	1003	2025-11-17 10:07:31.71762	ID:19|Name:testing orm -2|Memo 'testing orm -2' (ID: 19) was submitted	\N	f	\N
177	\N	New Memo Submitted	1003	2025-11-17 10:07:31.941354	Memo ID 19 submitted by user ID 1003. Please review.	9999	f	memo_submitted
178	\N	New Memo Submitted	1003	2025-11-17 10:07:32.012173	Memo ID 19 submitted by user ID 1003. Please review.	1004	f	memo_submitted
179	\N	Memo Rejected	1004	2025-11-17 10:18:54.951983	Memo ID 19 has been rejected by QA Head ID 1004.	1003	f	memo_rejected
180	\N	Memo Rejected	1004	2025-11-17 10:24:52.849187	Memo ID 19 has been rejected by QA Head ID 1004.	1003	f	memo_rejected
181	\N	Memo Rejected	1004	2025-11-17 10:24:56.234711	ID:19|Name:testing orm -2|Memo 'testing orm -2' (ID: 19) was rejected	\N	f	\N
182	\N	User Updated	1002	2025-11-17 10:57:37.025706	ID:1515|Name:yogesh|User 'yogesh' (ID: 1515) was updated: password, role to ID 1, signature	\N	f	\N
183	\N	Kit of Parts Inspection Report Approved	1515	2025-11-17 10:58:40.277915	Report ID: 12|Report Ref: ytuio|Project: ERP QA Automation Tool|LRU: dfghj|Approved by: yogesh	\N	f	\N
184	\N	Report num : ytuio has been approved	1515	2025-11-17 10:58:40.29351	Report ID 12 (Ref: ytuio) has been approved by yogesh for project 'ERP QA Automation Tool', LRU 'dfghj'. Please review.	9999	f	report_approved
185	\N	Report num : ytuio has been approved	1515	2025-11-17 10:58:40.300473	Report ID 12 (Ref: ytuio) has been approved by yogesh for project 'ERP QA Automation Tool', LRU 'dfghj'. Please review.	1004	f	report_approved
186	\N	Memo Submitted	1003	2025-11-18 11:32:48.572745	ID:20|Name:Admin LRU|Memo 'Admin LRU' (ID: 20) was submitted	\N	f	\N
187	\N	New Memo Submitted	1003	2025-11-18 11:32:48.753448	Memo ID 20 submitted by user ID 1003. Please review.	9999	f	memo_submitted
188	\N	New Memo Submitted	1003	2025-11-18 11:32:48.769068	Memo ID 20 submitted by user ID 1003. Please review.	1004	f	memo_submitted
189	5500	IQA Observation Report Submitted	1002	2025-11-18 11:42:21.351566	ID:1|LRU:dharsh 1|Document:doc5500 vv1.0|Observations:2	\N	f	\N
190	5500	Document Version v1.2 Uploaded	1003	2025-11-18 12:23:34.741459	New version 'v1.2' (doc_ver: B) of document 'doc1121' uploaded for LRU 'dharsh 2' in project 'dharshini' by user ID 1003. Assigned reviewer: dharshini.	\N	f	\N
191	5500	New Document Version Uploaded	1003	2025-11-18 12:23:34.768529	New revision 'B' of document 'doc1121' uploaded for LRU 'dharsh 2' in project 'dharshini'. Please review.	1212	f	document_upload_new_version
192	5500	Comment Added to Plan Document	1212	2025-11-18 12:25:37.461224	Reviewer dharshini added a comment to document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' in LRU 'dharsh 2' for project 'dharshini'.	\N	f	\N
193	5500	New Comment on Plan Document	1212	2025-11-18 12:25:37.476547	Reviewer dharshini added a comment to document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' in LRU 'dharsh 2' of project 'dharshini'. Please review and address the feedback.	1005	f	plan_document_comment
194	5500	New Comment on Plan Document	1212	2025-11-18 12:25:37.482957	Reviewer dharshini added a comment to document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' in LRU 'dharsh 2' of project 'dharshini'. Please review and address the feedback.	1112	f	plan_document_comment
195	5500	Comment Added to Plan Document	1212	2025-11-18 12:25:54.748818	Reviewer dharshini added a comment to document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' in LRU 'dharsh 2' for project 'dharshini'.	\N	f	\N
196	5500	New Comment on Plan Document	1212	2025-11-18 12:25:54.754148	Reviewer dharshini added a comment to document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' in LRU 'dharsh 2' of project 'dharshini'. Please review and address the feedback.	1005	f	plan_document_comment
197	5500	New Comment on Plan Document	1212	2025-11-18 12:25:54.757026	Reviewer dharshini added a comment to document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' in LRU 'dharsh 2' of project 'dharshini'. Please review and address the feedback.	1112	f	plan_document_comment
198	5500	Comment Rejected	1005	2025-11-18 12:26:29.352301	Mahaashri C V rejected a comment on document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' (43) in LRU 'dharsh 2' for project 'dharshini'.	\N	f	\N
199	5500	Your Comment Was Rejected	1005	2025-11-18 12:26:29.356702	Designer Mahaashri C V rejected your comment on document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' (43) in LRU 'dharsh 2' of project 'dharshini'. Justification: corrected	1212	f	comment_rejected
200	5500	Comment Rejected	1005	2025-11-18 12:26:50.311378	Mahaashri C V rejected a comment on document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' (43) in LRU 'dharsh 2' for project 'dharshini'.	\N	f	\N
201	5500	Your Comment Was Rejected	1005	2025-11-18 12:26:50.316015	Designer Mahaashri C V rejected your comment on document '649bc02e-21c2-4cdd-950b-71de3e160d38.pdf' (43) in LRU 'dharsh 2' of project 'dharshini'. Justification: accepted 1 	1212	f	comment_rejected
202	5500	IQA Observation Report Submitted	1005	2025-11-18 12:28:21.52291	ID:2|LRU:dharsh 2|Document:doc 1111 vv1.0|Observations:1	\N	f	\N
203	5500	IQA Observation Report Submitted	1005	2025-11-18 12:33:51.528121	ID:3|LRU:dharsh 2|Document:doc1121 vv1.2|Observations:2	\N	f	\N
204	4004	Project Added	1002	2025-11-19 10:33:15.527679	ID:4004|Name:PROJECT_SAMPLE|Project 'PROJECT_SAMPLE' created with 2 LRUs	\N	f	\N
206	4004	New Project Created	1002	2025-11-19 10:33:15.558529	New project 'PROJECT_SAMPLE' (ID: 4004) has been created and requires your attention.	9999	f	project_created
207	4004	New Project Created	1002	2025-11-19 10:33:15.563115	New project 'PROJECT_SAMPLE' (ID: 4004) has been created and requires your attention.	1004	f	project_created
208	4004	Project Updated	1002	2025-11-19 10:37:28.231663	ID:4004|Name:PROJECT_SAMPLE|Project 'PROJECT_SAMPLE' was updated	\N	f	\N
209	4004	Project Updated	1002	2025-11-19 11:03:30.216504	ID:4004|Name:PROJECT_SAMPLE|Project 'PROJECT_SAMPLE' was updated	\N	f	\N
210	\N	User Disabled	1002	2025-11-19 11:38:16.271085	ID:1001|Name:Avanthika|User 'Avanthika' (ID: 1001) was disabled	\N	f	\N
211	\N	User Enabled	1002	2025-11-19 11:38:19.568255	ID:1001|Name:Avanthika|User 'Avanthika' (ID: 1001) was enabled	\N	f	\N
212	\N	User Deleted	1002	2025-11-19 11:58:30.691319	ID:1007|Name:thanishk|User 'thanishk' (ID: 1007) was soft deleted - all records preserved	\N	f	\N
213	\N	User Disabled	1002	2025-11-19 12:17:06.322831	ID:1001|Name:Avanthika|User 'Avanthika' (ID: 1001) was disabled. Active sessions will be terminated.	\N	f	\N
215	\N	User Enabled	1002	2025-11-19 12:18:09.359284	ID:1001|Name:Avanthika|User 'Avanthika' (ID: 1001) was enabled. Active sessions will be terminated.	\N	f	\N
216	\N	User Updated	1002	2025-11-19 12:18:14.00049	ID:1001|Name:Avanthika|User 'Avanthika' (ID: 1001) was updated: password, role to ID 3	\N	f	\N
217	4004	Project Assigned	1003	2025-11-19 15:33:35.325104	You have been assigned to project 'PROJECT_SAMPLE' (ID: 4004) by Mahadev M.	1112	f	project_assigned
218	4004	Project Updated	1002	2025-11-19 16:01:53.318985	ID:4004|Name:PROJECT_SAMPLE|Project 'PROJECT_SAMPLE' was updated	\N	f	\N
219	4004	Document Uploaded (Version A)	1003	2025-11-20 14:59:59.084396	New document 'doc4004' version v1.0 (doc_ver: A) uploaded for LRU 'LRU4005' in project 'PROJECT_SAMPLE' by user ID 1003.	\N	f	\N
220	4004	New Document Uploaded (Version A)	1003	2025-11-20 14:59:59.092945	New document 'doc4004' version v1.0 uploaded for LRU 'LRU4005' in project 'PROJECT_SAMPLE'. Review required.	9999	f	document_upload_version_a
221	4004	New Document Uploaded (Version A)	1003	2025-11-20 14:59:59.096786	New document 'doc4004' version v1.0 uploaded for LRU 'LRU4005' in project 'PROJECT_SAMPLE'. Review required.	1004	f	document_upload_version_a
222	\N	TECH_SUPPORT_REQUEST	1002	2025-11-20 15:50:00.029346	Tech support request submitted by Sudhiksha M K (User ID: 1002)	\N	f	\N
223	\N	New Tech Support Request	1002	2025-11-20 15:50:00.036978	New tech support request #16 from Sudhiksha M K (User ID: 1002). Issue: fvnfvnmv	1007	f	tech_support_request
224	\N	New Tech Support Request	1002	2025-11-20 15:50:00.041332	New tech support request #16 from Sudhiksha M K (User ID: 1002). Issue: fvnfvnmv	1011	f	tech_support_request
225	\N	New Tech Support Request	1002	2025-11-20 15:50:00.044249	New tech support request #16 from Sudhiksha M K (User ID: 1002). Issue: fvnfvnmv	1002	f	tech_support_request
226	\N	New Tech Support Request	1002	2025-11-20 15:50:00.047069	New tech support request #16 from Sudhiksha M K (User ID: 1002). Issue: fvnfvnmv	1515	f	tech_support_request
227	4004	Document Uploaded (Version A)	1003	2025-11-21 10:44:57.551067	New document 'doc4002' version v1.0 (doc_ver: A) uploaded for LRU 'LRU4002' in project 'PROJECT_SAMPLE' by user ID 1003.	\N	f	\N
228	4004	New Document Uploaded (Version A)	1003	2025-11-21 10:44:57.564426	New document 'doc4002' version v1.0 uploaded for LRU 'LRU4002' in project 'PROJECT_SAMPLE'. Review required.	9999	f	document_upload_version_a
229	4004	New Document Uploaded (Version A)	1003	2025-11-21 10:44:57.575668	New document 'doc4002' version v1.0 uploaded for LRU 'LRU4002' in project 'PROJECT_SAMPLE'. Review required.	1004	f	document_upload_version_a
230	64301877	Document Uploaded (Version A)	1003	2025-11-21 11:00:42.769005	New document 'doc666' version v1.0 (doc_ver: A) uploaded for LRU 'Test LRU' in project 'Test Project' by user ID 1003.	\N	f	\N
231	64301877	New Document Uploaded (Version A)	1003	2025-11-21 11:00:42.777943	New document 'doc666' version v1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	9999	f	document_upload_version_a
232	64301877	New Document Uploaded (Version A)	1003	2025-11-21 11:00:42.781814	New document 'doc666' version v1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	1004	f	document_upload_version_a
233	4321	Project Added	1002	2025-11-25 14:59:26.024737	ID:4321|Name:project123|Project 'project123' created with 1 LRUs	\N	f	\N
235	4321	New Project Created	1002	2025-11-25 14:59:26.037308	New project 'project123' (ID: 4321) has been created and requires your attention.	9999	f	project_created
236	4321	New Project Created	1002	2025-11-25 14:59:26.040844	New project 'project123' (ID: 4321) has been created and requires your attention.	1004	f	project_created
237	11	Project Added	1002	2025-11-25 15:03:20.516568	ID:11|Name:q|Project 'q' created with 1 LRUs	\N	f	\N
238	11	New Project Created	1002	2025-11-25 15:03:20.518548	New project 'q' (ID: 11) has been created and requires your attention.	1003	f	project_created
239	11	New Project Created	1002	2025-11-25 15:03:20.522272	New project 'q' (ID: 11) has been created and requires your attention.	9999	f	project_created
240	11	New Project Created	1002	2025-11-25 15:03:20.525797	New project 'q' (ID: 11) has been created and requires your attention.	1004	f	project_created
241	54	Project Added	1002	2025-11-25 15:15:27.543051	ID:54|Name:a|Project 'a' created with 1 LRUs	\N	f	\N
242	54	New Project Created	1002	2025-11-25 15:15:27.547971	New project 'a' (ID: 54) has been created and requires your attention.	1003	f	project_created
243	54	New Project Created	1002	2025-11-25 15:15:27.552871	New project 'a' (ID: 54) has been created and requires your attention.	9999	f	project_created
244	54	New Project Created	1002	2025-11-25 15:15:27.555691	New project 'a' (ID: 54) has been created and requires your attention.	1004	f	project_created
245	90691014	Document Uploaded (Version A)	1003	2025-11-25 15:56:24.04748	New document 'DOC554' version V1.2 (doc_ver: A) uploaded for LRU 'Test LRU' in project 'Test Project' by user ID 1003.	\N	f	\N
246	90691014	New Document Uploaded (Version A)	1003	2025-11-25 15:56:24.057381	New document 'DOC554' version V1.2 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	9999	f	document_upload_version_a
247	90691014	New Document Uploaded (Version A)	1003	2025-11-25 15:56:24.0666	New document 'DOC554' version V1.2 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	1004	f	document_upload_version_a
248	85546124	Document Uploaded (Version A)	1003	2025-11-25 15:58:43.123573	New document 'DOC343' version V1.0 (doc_ver: A) uploaded for LRU 'Test LRU' in project 'Test Project' by user ID 1003.	\N	f	\N
249	85546124	New Document Uploaded (Version A)	1003	2025-11-25 15:58:43.127687	New document 'DOC343' version V1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	9999	f	document_upload_version_a
250	85546124	New Document Uploaded (Version A)	1003	2025-11-25 15:58:43.131078	New document 'DOC343' version V1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	1004	f	document_upload_version_a
251	12345	Reviewer Updated for Plan Document	1002	2025-11-25 16:01:00.648342	QA Head updated reviewer assignment to dharshini for plan documents in LRU 'Test LRU' in project 'Test Project'.	\N	f	\N
252	12345	Plan Document Assignment Updated	1002	2025-11-25 16:01:00.655956	You have been assigned to review plan documents for LRU 'Test LRU' in project 'Test Project' by Sudhiksha M K.	1212	f	plan_document_assigned
253	12345	Reviewer Updated for Plan Document	1002	2025-11-25 16:01:14.305512	QA Head updated reviewer assignment to dharshini for plan documents in LRU 'Test LRU' in project 'Test Project'.	\N	f	\N
254	12345	Plan Document Assignment Updated	1002	2025-11-25 16:01:14.310502	You have been assigned to review plan documents for LRU 'Test LRU' in project 'Test Project' by Sudhiksha M K.	1212	f	plan_document_assigned
255	1010	Project Added	1002	2025-11-25 16:03:22.699257	ID:1010|Name:TESTING_CASDIC|Project 'TESTING_CASDIC' created with 1 LRUs	\N	f	\N
256	1010	New Project Created	1002	2025-11-25 16:03:22.701837	New project 'TESTING_CASDIC' (ID: 1010) has been created and requires your attention.	1003	f	project_created
257	1010	New Project Created	1002	2025-11-25 16:03:22.707524	New project 'TESTING_CASDIC' (ID: 1010) has been created and requires your attention.	9999	f	project_created
258	1010	New Project Created	1002	2025-11-25 16:03:22.71623	New project 'TESTING_CASDIC' (ID: 1010) has been created and requires your attention.	1004	f	project_created
259	1010	Document Uploaded (Version A)	1003	2025-11-25 16:04:38.775375	New document 'DOC1010' version V1.0 (doc_ver: A) uploaded for LRU 'TESTING_CASDIC' in project 'TESTING_CASDIC' by user ID 1003.	\N	f	\N
260	1010	New Document Uploaded (Version A)	1003	2025-11-25 16:04:38.780354	New document 'DOC1010' version V1.0 uploaded for LRU 'TESTING_CASDIC' in project 'TESTING_CASDIC'. Review required.	9999	f	document_upload_version_a
261	1010	New Document Uploaded (Version A)	1003	2025-11-25 16:04:38.785415	New document 'DOC1010' version V1.0 uploaded for LRU 'TESTING_CASDIC' in project 'TESTING_CASDIC'. Review required.	1004	f	document_upload_version_a
262	1010	Reviewer Assigned to Plan Document	1002	2025-11-25 16:05:05.502255	QA Head assigned Avanthika to review plan documents for LRU 'TESTING_CASDIC' in project 'TESTING_CASDIC'.	\N	f	\N
263	1010	Plan Document Assignment	1002	2025-11-25 16:05:05.507741	You have been assigned to review plan documents for LRU 'TESTING_CASDIC' in project 'TESTING_CASDIC' by Sudhiksha M K.	1001	f	plan_document_assigned
264	1010	Comment Added to Plan Document	1001	2025-11-25 16:05:53.209944	Reviewer Avanthika added a comment to document 'fbf11ad6-5e81-49bf-8b9e-34a32963d28c.docx' in LRU 'TESTING_CASDIC' for project 'TESTING_CASDIC'.	\N	f	\N
265	1010	Comment Added to Plan Document	1001	2025-11-25 16:06:09.092827	Reviewer Avanthika added a comment to document 'fbf11ad6-5e81-49bf-8b9e-34a32963d28c.docx' in LRU 'TESTING_CASDIC' for project 'TESTING_CASDIC'.	\N	f	\N
266	1010	Project Updated	1002	2025-11-25 16:07:06.776073	ID:1010|Name:TESTING_CASDIC|Project 'TESTING_CASDIC' was updated	\N	f	\N
267	1010	Document Uploaded (Version A)	1003	2025-11-25 16:13:18.481643	New document 'DOC1001' version V1.0 (doc_ver: A) uploaded for LRU 'TESTING 2' in project 'TESTING_CASDIC' by user ID 1003.	\N	f	\N
268	1010	New Document Uploaded (Version A)	1003	2025-11-25 16:13:18.486912	New document 'DOC1001' version V1.0 uploaded for LRU 'TESTING 2' in project 'TESTING_CASDIC'. Review required.	9999	f	document_upload_version_a
269	1010	New Document Uploaded (Version A)	1003	2025-11-25 16:13:18.490598	New document 'DOC1001' version V1.0 uploaded for LRU 'TESTING 2' in project 'TESTING_CASDIC'. Review required.	1004	f	document_upload_version_a
270	1010	Comment Added to Plan Document	1001	2025-11-25 16:15:03.944448	Reviewer Avanthika added a comment to document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
271	1010	Comment Added to Plan Document	1001	2025-11-25 16:15:39.517898	Reviewer Avanthika added a comment to document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
272	1010	Comment Added to Plan Document	1001	2025-11-25 16:15:55.428174	Reviewer Avanthika added a comment to document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
273	1010	Comment Added to Plan Document	1001	2025-11-25 16:16:46.237462	Reviewer Avanthika added a comment to document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
274	1010	Comment Added to Plan Document	1001	2025-11-25 16:17:20.973183	Reviewer Avanthika added a comment to document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
275	1010	Comment Added to Plan Document	1001	2025-11-25 16:18:22.026255	Reviewer Avanthika added a comment to document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
234	4321	New Project Created	1002	2025-11-25 14:59:26.032679	New project 'project123' (ID: 4321) has been created and requires your attention.	1003	t	project_created
205	4004	New Project Created	1002	2025-11-19 10:33:15.544485	New project 'PROJECT_SAMPLE' (ID: 4004) has been created and requires your attention.	1003	t	project_created
276	1010	Comment Accepted	1003	2025-11-25 16:21:20.22175	Mahadev M accepted a comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
277	1010	Your Comment Was Accepted	1003	2025-11-25 16:21:20.229137	Designer Mahadev M accepted your comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' of project 'TESTING_CASDIC'. Justification: GFHJKL	1001	f	comment_accepted
278	1010	Comment Accepted	1003	2025-11-25 16:21:35.29881	Mahadev M accepted a comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
279	1010	Your Comment Was Accepted	1003	2025-11-25 16:21:35.303296	Designer Mahadev M accepted your comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' of project 'TESTING_CASDIC'. Justification: BVNM,	1001	f	comment_accepted
280	1010	Comment Accepted	1003	2025-11-25 16:21:43.291011	Mahadev M accepted a comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
281	1010	Your Comment Was Accepted	1003	2025-11-25 16:21:43.296272	Designer Mahadev M accepted your comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' of project 'TESTING_CASDIC'. Justification: BVNM,.	1001	f	comment_accepted
282	1010	Comment Rejected	1003	2025-11-25 16:21:52.739392	Mahadev M rejected a comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
283	1010	Your Comment Was Rejected	1003	2025-11-25 16:21:52.747377	Designer Mahadev M rejected your comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' of project 'TESTING_CASDIC'. Justification: NBM,	1001	f	comment_rejected
284	1010	Comment Accepted	1003	2025-11-25 16:22:05.608384	Mahadev M accepted a comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
285	1010	Your Comment Was Accepted	1003	2025-11-25 16:22:05.614106	Designer Mahadev M accepted your comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' of project 'TESTING_CASDIC'. Justification: BVNM,	1001	f	comment_accepted
286	1010	Comment Accepted	1003	2025-11-25 16:22:13.098236	Mahadev M accepted a comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' for project 'TESTING_CASDIC'.	\N	f	\N
287	1010	Your Comment Was Accepted	1003	2025-11-25 16:22:13.104204	Designer Mahadev M accepted your comment on document 'cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf' (56) in LRU 'TESTING 2' of project 'TESTING_CASDIC'. Justification: BVNM	1001	f	comment_accepted
288	76513893	Document Uploaded (Version A)	1003	2025-11-25 20:20:44.81816	New document 'gh' version hg.0 (doc_ver: A) uploaded for LRU 'Test LRU' in project 'Test Project' by user ID 1003.	\N	f	\N
289	76513893	New Document Uploaded (Version A)	1003	2025-11-25 20:20:44.830354	New document 'gh' version hg.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	9999	f	document_upload_version_a
290	76513893	New Document Uploaded (Version A)	1003	2025-11-25 20:20:44.837855	New document 'gh' version hg.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	1004	f	document_upload_version_a
291	\N	User Updated	1002	2025-11-25 20:22:23.95221	ID:9999|Name:Updated Test User|User 'Updated Test User' (ID: 9999) was updated: role to ID 2, signature	\N	f	\N
292	\N	User Updated	1002	2025-11-26 08:45:15.355022	ID:1616|Name:pradeepa|User 'pradeepa' (ID: 1616) was updated: role to ID 5, signature	\N	f	\N
293	70646485	Document Uploaded (Version A)	1003	2025-11-26 10:51:52.487735	New document 'doc-3232' version v1.0 (doc_ver: A) uploaded for LRU 'Test LRU' in project 'Test Project' by user ID 1003.	\N	f	\N
294	70646485	New Document Uploaded (Version A)	1003	2025-11-26 10:51:52.498059	New document 'doc-3232' version v1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	1004	f	document_upload_version_a
295	70646485	New Document Uploaded (Version A)	1003	2025-11-26 10:51:52.50312	New document 'doc-3232' version v1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	9999	f	document_upload_version_a
296	22199255	Document Uploaded (Version A)	1003	2025-11-26 11:52:00.263051	New document 'doc-001' version v1.0 (doc_ver: A) uploaded for LRU 'Test LRU' in project 'Test Project' by user ID 1003.	\N	f	\N
297	22199255	New Document Uploaded (Version A)	1003	2025-11-26 11:52:00.272389	New document 'doc-001' version v1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	1004	f	document_upload_version_a
298	22199255	New Document Uploaded (Version A)	1003	2025-11-26 11:52:00.278573	New document 'doc-001' version v1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	9999	f	document_upload_version_a
299	67995283	Document Uploaded (Version A)	1003	2025-11-26 12:03:49.804603	New document 'd-007' version v1.0 (doc_ver: A) uploaded for LRU 'Test LRU' in project 'Test Project' by user ID 1003.	\N	f	\N
300	67995283	New Document Uploaded (Version A)	1003	2025-11-26 12:03:49.829637	New document 'd-007' version v1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	1004	f	document_upload_version_a
301	67995283	New Document Uploaded (Version A)	1003	2025-11-26 12:03:49.833133	New document 'd-007' version v1.0 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	9999	f	document_upload_version_a
302	66820093	Document Uploaded (Version A)	1003	2025-11-26 12:33:20.007294	New document 'doc44' version v6.8 (doc_ver: A) uploaded for LRU 'Test LRU' in project 'Test Project' by user ID 1003.	\N	f	\N
303	66820093	New Document Uploaded (Version A)	1003	2025-11-26 12:33:20.017893	New document 'doc44' version v6.8 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	1004	f	document_upload_version_a
304	66820093	New Document Uploaded (Version A)	1003	2025-11-26 12:33:20.024774	New document 'doc44' version v6.8 uploaded for LRU 'Test LRU' in project 'Test Project'. Review required.	9999	f	document_upload_version_a
305	\N	TECH_SUPPORT_REQUEST	1002	2025-12-08 08:37:49.158197	Tech support request submitted by Sudhiksha M K (User ID: 1002)	\N	f	\N
306	\N	New Tech Support Request	1002	2025-12-08 08:37:49.168075	New tech support request #17 from Sudhiksha M K (User ID: 1002). Issue: trrhgfj	1007	f	tech_support_request
307	\N	New Tech Support Request	1002	2025-12-08 08:37:49.174683	New tech support request #17 from Sudhiksha M K (User ID: 1002). Issue: trrhgfj	1011	f	tech_support_request
308	\N	New Tech Support Request	1002	2025-12-08 08:37:49.177032	New tech support request #17 from Sudhiksha M K (User ID: 1002). Issue: trrhgfj	1002	f	tech_support_request
309	\N	New Tech Support Request	1002	2025-12-08 08:37:49.178571	New tech support request #17 from Sudhiksha M K (User ID: 1002). Issue: trrhgfj	1515	f	tech_support_request
\.


--
-- Data for Name: assembled_board_inspection_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assembled_board_inspection_report (report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number, start_date, end_date, dated1, dated2, obs1, rem1, upload1, obs2, rem2, upload2, obs3, rem3, upload3, obs4, rem4, upload4, obs5, rem5, upload5, obs6, rem6, upload6, obs7, rem7, upload7, obs8, rem8, upload8, obs9, rem9, upload9, obs10, rem10, upload10, obs11, rem11, upload11, obs12, rem12, upload12, obs13, rem13, upload13, obs14, rem14, upload14, obs15, rem15, upload15, obs16, rem16, upload16, obs17, rem17, upload17, obs18, rem18, upload18, obs19, rem19, upload19, obs20, rem20, upload20, prepared_by, verified_by, approved_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: bare_pcb_inspection_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bare_pcb_inspection_report (report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number, inspection_count, start_date, end_date, dated1, dated2, obs1, rem1, upload1, obs2, rem2, upload2, obs3, rem3, upload3, obs4, rem4, upload4, obs5, rem5, upload5, obs6, rem6, upload6, obs7, rem7, upload7, obs8, rem8, upload8, obs9, rem9, upload9, obs10, rem10, upload10, obs11, rem11, upload11, obs12, rem12, upload12, overall_status, quality_rating, recommendations, prepared_by, verified_by, approved_by, created_at, updated_at) FROM stdin;
1	ERP QA Automation Tool	ytuio	76y	ghgjkl	vbnkjl	fdgh	ty56	hjkl	ghjkl	6	3 4 	SL-001	INS-001	2025-10-18	2025-10-04	2025-10-04	2025-10-04	1	OK		2	OK		3	OK		4	OK		5	OK		6	OK		7	NOT OK		8	NOT OK		9	NOT OK		10	NOT OK		11	NOT OK		12	OK		COMPLETED	\N					2025-10-03 12:27:36.839127+05:30	2025-10-03 12:27:36.839127+05:30
\.


--
-- Data for Name: bulletins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bulletins (bulletin_id, sub_test_id, parent_bulletin_id, bulletin_name, bulletin_description, created_at, created_by, updated_at, updated_by) FROM stdin;
87	18	23	10 Cycles – High Temperature	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
88	18	23	10 Cycles – Low Temperature	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
89	26	41	X Axis	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
90	26	41	Y Axis	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
91	26	41	Z Axis	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
92	26	43	Visual Inspection	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
93	26	43	Dimensional Check	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
94	26	43	Functional Check	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
95	49	68	X Axis	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
96	49	68	Y Axis	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
97	49	68	Z Axis	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
98	49	70	Visual Inspection	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
99	49	70	Dimensional Check	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
100	49	70	Functional Check	\N	2025-10-24 16:42:41.589075	\N	2025-10-24 16:42:41.589075	\N
1	1	\N	Tensile Strength	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
2	1	\N	Ultrasonic Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
3	1	\N	Die Penetration Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
4	1	\N	Chemical Composition	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
5	2	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
6	2	\N	Dimensional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
7	3	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
8	3	\N	Dimensional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
9	8	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
10	8	\N	Dimensional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
11	8	\N	Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
12	9	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
13	9	\N	Dimensional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
14	9	\N	Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
15	14	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
16	14	\N	Post Power Burn-in Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
17	17	\N	Pre-Vibration Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
18	17	\N	Pre-Vibration Functional Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
19	17	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
20	17	\N	Post Vibration Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
21	18	\N	Pre Thermal Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
22	18	\N	Pre-Thermal Functional Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
23	18	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
24	18	\N	Post Thermal Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
25	18	\N	Post Thermal Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
26	19	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
27	19	\N	Pre-Vibration Functional Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
28	19	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
29	19	\N	Post Vibration Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
30	20	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
31	20	\N	Dimensional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
32	20	\N	Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
33	21	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
34	21	\N	Dimensional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
35	21	\N	Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
36	23	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
37	23	\N	Post HT Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
38	24	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
39	24	\N	Post LT Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
40	26	\N	Initial Resonance Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
41	26	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
42	26	\N	Final Resonance Research	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
43	26	\N	Post RV Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
44	27	\N	Radiated Emission Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
45	27	\N	Conducted Emission Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
46	27	\N	Radiated Susceptibility Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
47	27	\N	Conducted Susceptibility Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
48	28	\N	DC Test (LDC)	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
49	28	\N	Single Phase AC (SAC)	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
50	28	\N	Three Phase AC (TAC)	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
51	29	\N	Altitude	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
52	29	\N	Low Temperature	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
53	29	\N	High Temperature	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
54	29	\N	Humidity	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
55	30	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
56	30	\N	Post Humidity Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
57	45	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
58	45	\N	Dimensional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
59	45	\N	Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
60	46	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
61	46	\N	Dimensional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
62	46	\N	Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
63	47	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
64	47	\N	Post HT Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
65	48	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
66	48	\N	Post LT Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
67	49	\N	Initial Resonance Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
68	49	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
69	49	\N	Final Resonance Research	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
70	49	\N	Post RV Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
71	51	\N	Radiated Emission Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
72	51	\N	Conducted Emission Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
73	51	\N	Radiated Susceptibility Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
74	51	\N	Conducted Susceptibility Test	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
75	52	\N	DC Test (LDC)	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
76	52	\N	Single Phase AC (SAC)	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
77	52	\N	Three Phase AC (TAC)	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
78	53	\N	Altitude	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
79	53	\N	Low Temperature	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
80	53	\N	High Temperature	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
81	53	\N	Humidity	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
82	56	\N	INSITU Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
83	56	\N	Post Humidity Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
84	59	\N	Visual Inspection	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
85	59	\N	Dimensional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
86	59	\N	Functional Check	\N	2025-10-24 16:42:11.13347	\N	2025-10-24 16:42:11.13347	\N
\.


--
-- Data for Name: conformal_coating_inspection_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.conformal_coating_inspection_report (report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number, start_date, end_date, dated1, dated2, obs1, rem1, upload1, expected1, obs2, rem2, upload2, expected2, obs3, rem3, upload3, expected3, obs4, rem4, upload4, expected4, obs5, rem5, upload5, expected5, obs6, rem6, upload6, expected6, obs7, rem7, upload7, expected7, obs8, rem8, upload8, expected8, obs9, rem9, upload9, expected9, overall_status, quality_rating, recommendations, prepared_by, verified_by, approved_by, created_at, updated_at, original_report_id, report_card_id) FROM stdin;
18	gfhjkl	bvnm,	\N	\N	nm	ghjk	nm	hjk	vfgbhn	\N	ghjk	SL-001	2025-11-04	2025-11-04	\N	\N	no	OK	\N	no	no	OK	\N	no	no	OK	\N	no	no	OK	\N	no	no	OK	\N	no	no	OK	\N	no	no damages	OK	\N	no damages	no	NOT OK	\N	yes	yes	OK	\N	yes	\N	\N	\N	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	2025-11-03 11:44:28.959686+05:30	2025-11-03 11:45:20.094482+05:30	\N	21
19	ERP QA Automation Tool	ytuio	sdf	ghj	ghj	fdgh	bnm	defrgt	ghjkl	3	7	SL-001	2025-11-11	2025-10-30	2025-11-11	2025-11-11	yes	NOT OK	\N	no	yes	NOT OK	\N	no	yes	NOT OK	\N	no	yes	NOT OK	\N	no	yes	NOT OK	\N	no	no	OK	\N	no	no damages	OK	\N	no damages	yes	OK	\N	yes	yes	OK	\N	yes	\N	\N	\N	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	2025-11-11 12:10:39.937534+05:30	2025-11-11 12:11:09.949003+05:30	\N	22
\.


--
-- Data for Name: cot_screening_inspection_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cot_screening_inspection_report (report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number, start_date, end_date, dated1, dated2, test_nature1, test_nature2, test_nature3, rem1, upload1, rem2, upload2, rem3, upload3, prepared_by, verified_by, approved_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: document_annotations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.document_annotations (annotation_id, comment_id, page_no, x_position, y_position, created_at, document_id) FROM stdin;
1	1	1	54.14	18.04	2025-09-22 11:59:53.937963	30
2	2	1	57.70	5.34	2025-09-22 12:09:23.380717	30
3	3	1	41.70	23.36	2025-09-22 12:09:57.520532	30
4	4	1	49.84	9.18	2025-09-22 13:14:04.528162	34
5	5	1	37.85	10.58	2025-09-24 12:26:48.692223	30
6	6	1	61.36	14.85	2025-09-29 14:34:35.485591	35
7	10	1	51.26	33.38	2025-09-29 15:18:36.366238	35
8	11	1	27.65	14.95	2025-09-29 17:31:42.038152	37
9	12	1	70.75	27.55	2025-09-29 17:31:53.127681	37
10	13	1	29.33	6.94	2025-10-10 09:38:12.61775	39
11	14	1	83.81	30.97	2025-10-10 09:38:24.492352	39
12	15	1	54.25	42.60	2025-10-13 09:50:41.124346	41
13	16	1	29.39	24.92	2025-10-13 09:51:48.442172	41
16	19	1	19.29	4.77	2025-10-22 12:26:26.094306	43
17	20	1	17.93	16.96	2025-10-22 17:01:00.124382	43
18	21	1	24.91	32.00	2025-10-27 11:02:52.389056	44
19	22	2	75.89	86.03	2025-10-27 11:03:22.449973	44
20	23	1	77.53	14.23	2025-10-28 14:16:59.27392	48
21	24	1	73.70	10.03	2025-10-28 14:20:15.334383	47
22	25	1	46.90	17.41	2025-10-28 14:24:35.882579	48
23	26	2	80.62	7.53	2025-10-28 14:30:45.25227	48
24	27	1	69.73	39.31	2025-10-28 15:00:51.984644	46
25	28	1	73.17	10.11	2025-10-28 15:28:45.082475	50
26	29	1	20.83	5.61	2025-11-10 14:08:00.45829	51
27	30	1	67.55	80.95	2025-11-10 14:08:05.754533	51
28	31	2	8.64	28.57	2025-11-10 14:08:17.159572	51
29	32	1	57.96	8.06	2025-11-10 14:12:00.456738	52
30	33	1	79.35	25.23	2025-11-10 14:13:30.769064	51
31	34	1	55.63	39.87	2025-11-18 12:25:21.518716	53
32	35	1	43.09	92.96	2025-11-18 12:25:51.210541	53
33	36	1	17.49	19.23	2025-11-25 16:05:27.420836	59
34	37	1	19.48	75.61	2025-11-25 16:05:57.422038	59
35	38	1	14.54	18.59	2025-11-25 16:14:57.450886	60
36	39	2	19.36	22.34	2025-11-25 16:15:27.417926	60
37	40	2	59.62	82.20	2025-11-25 16:15:40.628879	60
38	41	3	18.22	32.84	2025-11-25 16:16:27.420615	60
39	42	4	68.86	46.55	2025-11-25 16:16:57.431057	60
40	43	5	21.38	49.80	2025-11-25 16:17:57.420727	60
\.


--
-- Data for Name: document_annotations_backup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.document_annotations_backup (annotation_id, comment_id, document_id, page_no, x_position, y_position, created_at) FROM stdin;
1	1	DOC-001	1	54.14	18.04	2025-09-22 11:59:53.937963
2	2	DOC-001	1	57.70	5.34	2025-09-22 12:09:23.380717
3	3	DOC-001	1	41.70	23.36	2025-09-22 12:09:57.520532
4	4	doc-015	1	49.84	9.18	2025-09-22 13:14:04.528162
5	5	DOC-001	1	37.85	10.58	2025-09-24 12:26:48.692223
6	6	doc055	1	61.36	14.85	2025-09-29 14:34:35.485591
7	10	doc055	1	51.26	33.38	2025-09-29 15:18:36.366238
8	11	doc057	1	27.65	14.95	2025-09-29 17:31:42.038152
9	12	doc057	1	70.75	27.55	2025-09-29 17:31:53.127681
10	13	coc55	1	29.33	6.94	2025-10-10 09:38:12.61775
11	14	coc55	1	83.81	30.97	2025-10-10 09:38:24.492352
12	15	doc55	1	54.25	42.60	2025-10-13 09:50:41.124346
13	16	doc55	1	29.39	24.92	2025-10-13 09:51:48.442172
14	17	41	1	56.84	44.01	2025-10-15 09:53:10.31626
15	18	41	1	55.49	24.92	2025-10-15 09:54:07.426148
\.


--
-- Data for Name: document_comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.document_comments (comment_id, document_name, version, reviewer_id, page_no, section, description, commented_by, created_at, is_annotation, status, accepted_at, justification, accepted_by, document_id) FROM stdin;
28	c22cb015-6d3a-4911-b7c4-2ded6409dc78.pdf	v1.0	1212	1		ok	1212	2025-10-28 15:28:45.082475	t	accepted	2025-10-28 15:29:10.176168	ok ok	1005	50
31	b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf	v1.0	1212	2		tech 3	1212	2025-11-10 14:08:17.159572	t	rejected	2025-11-10 14:09:00.456764	rej3	1616	51
30	b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf	v1.0	1212	1		tech 2	1212	2025-11-10 14:08:05.754533	t	accepted	2025-11-10 14:10:00.455781	acc 2	1616	51
29	b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf	v1.0	1212	1		tech 1	1212	2025-11-10 14:08:00.45829	t	rejected	2025-11-10 14:10:30.758719	rej1	1616	51
32	f5d59013-7837-4b01-8b01-d8f83c0d1bd7.pdf	v2.0	1212	1		manual2	1212	2025-11-10 14:12:00.456738	t	rejected	2025-11-10 14:13:00.658499	rewj	1616	52
19	dcdfd350-d358-4c10-9d46-f2ae845ab75b.pdf	v1.0	1111	1		checking doc_id updations	1111	2025-10-22 12:26:26.094306	t	rejected	2025-10-22 12:27:54.709363	rejected	1005	43
20	dcdfd350-d358-4c10-9d46-f2ae845ab75b.pdf	v1.0	1111	1		test 2	1111	2025-10-22 17:01:00.124382	t	accepted	2025-10-22 17:01:43.10416	accepted	1005	43
5	729abc37-37ab-498e-9930-c0245eb95789.pdf	v1.0	\N	1		generated	Anonymous	2025-09-24 12:26:48.692223	t	accepted	2025-10-24 14:30:06.156239	ghjk	1005	30
22	c3def326-2b74-4f6e-b9cb-803c9ea52e70.pdf	v1.0	1212	2		comment 2	1212	2025-10-27 11:03:22.449973	t	rejected	2025-10-27 11:04:40.508068	gfh	1005	44
21	c3def326-2b74-4f6e-b9cb-803c9ea52e70.pdf	v1.0	1212	1		comment 1	1212	2025-10-27 11:02:52.389056	t	accepted	2025-10-27 11:04:51.058166	hgjk	1005	44
24	9b0f1ba9-07b9-4028-9695-1c41cd30c5de.pdf	v1	1008	1		haloooooooooo	1008	2025-10-28 14:20:15.334383	t	accepted	2025-10-28 14:21:15.324256	mohana	1112	47
1	729abc37-37ab-498e-9930-c0245eb95789.pdf	v1.0	\N	1		report list	Anonymous	2025-09-22 11:59:53.937963	t	\N	\N	\N	\N	30
2	729abc37-37ab-498e-9930-c0245eb95789.pdf	v1.0	\N	1		summary	Anonymous	2025-09-22 12:09:23.380717	t	\N	\N	\N	\N	30
4	9917b33e-afdb-4c74-8e2d-77b1dd176741.pdf	v1.5	\N	1		memo	Anonymous	2025-09-22 13:14:04.528162	t	\N	\N	\N	\N	34
33	b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf	v1.0	1212	1		old	1212	2025-11-10 14:13:30.769064	t	\N	\N	\N	\N	51
6	43c000c6-c7ec-4e63-b6d1-9d573df473a3.pdf	v1.1	1008	1		unknown lru	Anonymous	2025-09-29 14:34:35.485591	t	accepted	2025-09-29 14:55:05.842209	justification done\n	1003	35
10	43c000c6-c7ec-4e63-b6d1-9d573df473a3.pdf	v1.1	1008	1		Reference	Anonymous	2025-09-29 15:18:36.366238	t	accepted	2025-09-29 15:40:49.635536	rejected	1003	35
11	67f3c018-e0d0-4aca-94be-04a6268d284e.pdf	v1.3	1008	1		mahadev	Anonymous	2025-09-29 17:31:42.038152	t	accepted	2025-09-29 17:32:45.773568	just	1003	37
12	67f3c018-e0d0-4aca-94be-04a6268d284e.pdf	v1.3	1008	1		Avanthika	Anonymous	2025-09-29 17:31:53.127681	t	rejected	2025-09-29 17:34:07.251024	pg	1003	37
14	aa11f80a-5fb7-47de-9fa9-6eed11a39ac1.pdf	v1.0	1001	1		comment 2	1001	2025-10-10 09:38:24.492352	t	rejected	2025-10-10 09:41:40.379942	rej	1003	39
13	aa11f80a-5fb7-47de-9fa9-6eed11a39ac1.pdf	v1.0	1001	1		comment 1	1001	2025-10-10 09:38:12.61775	t	accepted	2025-10-10 09:41:56.222638	acc	1003	39
15	8692c214-54fd-4c1d-94df-a6ad951d78d4.docx	v1.0	1111	1		comment 1	1111	2025-10-13 09:50:41.124346	t	rejected	2025-10-13 09:51:06.634129	r	1005	41
16	8692c214-54fd-4c1d-94df-a6ad951d78d4.docx	v1.0	1111	1		comment 2	1111	2025-10-13 09:51:48.442172	t	accepted	2025-10-13 09:52:15.977725	a	1005	41
25	b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf	v1.0	1212	1		dharshiniiiiiiiii	1212	2025-10-28 14:24:35.882579	t	accepted	2025-10-28 14:26:44.960911	dharsh	1005	48
23	b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf	v1.0	1212	1		haloooo	1212	2025-10-28 14:16:59.27392	t	accepted	2025-10-28 14:29:51.879936	good	1005	48
26	b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf	v1.0	1212	2		empty	1212	2025-10-28 14:30:45.25227	t	rejected	2025-10-28 14:32:09.969763	so wat	1005	48
27	cb366ba1-0256-4cda-b9c1-3664b9f13032.pdf	v1.1	1212	1		check 1	1212	2025-10-28 15:00:51.984644	t	rejected	2025-10-28 15:02:49.075982	check 1	1003	46
35	649bc02e-21c2-4cdd-950b-71de3e160d38.pdf	v1.2	1212	1		comment 2 for checking	1212	2025-11-18 12:25:51.210541	t	rejected	2025-11-18 12:26:21.523716	corrected	1005	53
34	649bc02e-21c2-4cdd-950b-71de3e160d38.pdf	v1.2	1212	1		comment 1 for chcking	1212	2025-11-18 12:25:21.518716	t	rejected	2025-11-18 12:26:29.606723	accepted 1 	1005	53
36	fbf11ad6-5e81-49bf-8b9e-34a32963d28c.docx	V1.0	1001	1		SCOPE OF DOC	1001	2025-11-25 16:05:27.420836	t	\N	\N	\N	\N	59
37	fbf11ad6-5e81-49bf-8b9e-34a32963d28c.docx	V1.0	1001	1		DESIGN TEAM 	1001	2025-11-25 16:05:57.422038	t	\N	\N	\N	\N	59
43	cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf	V1.0	1001	5		COMMENT7	1001	2025-11-25 16:17:57.420727	t	accepted	2025-11-25 16:21:05.32121	GFHJKL	1003	60
42	cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf	V1.0	1001	4		COMMENT5	1001	2025-11-25 16:16:57.431057	t	accepted	2025-11-25 16:21:20.466915	BVNM,	1003	60
41	cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf	V1.0	1001	3		COMMENT4	1001	2025-11-25 16:16:27.420615	t	accepted	2025-11-25 16:21:35.32519	BVNM,.	1003	60
40	cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf	V1.0	1001	2		COMMENT3	1001	2025-11-25 16:15:40.628879	t	rejected	2025-11-25 16:21:43.54886	NBM,	1003	60
39	cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf	V1.0	1001	2		COMMENT2	1001	2025-11-25 16:15:27.417926	t	accepted	2025-11-25 16:22:05.337896	BVNM,	1003	60
38	cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf	V1.0	1001	1		INTRODUCTION	1001	2025-11-25 16:14:57.450886	t	accepted	2025-11-25 16:22:05.86003	BVNM	1003	60
\.


--
-- Data for Name: document_comments_backup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.document_comments_backup (comment_id, document_id, document_name, version, reviewer_id, page_no, section, description, commented_by, created_at, is_annotation, status, accepted_at, justification, accepted_by) FROM stdin;
1	DOC-001	729abc37-37ab-498e-9930-c0245eb95789.pdf	v1.0	\N	1		report list	Anonymous	2025-09-22 11:59:53.937963	t	\N	\N	\N	\N
2	DOC-001	729abc37-37ab-498e-9930-c0245eb95789.pdf	v1.0	\N	1		summary	Anonymous	2025-09-22 12:09:23.380717	t	\N	\N	\N	\N
4	doc-015	9917b33e-afdb-4c74-8e2d-77b1dd176741.pdf	v1.5	\N	1		memo	Anonymous	2025-09-22 13:14:04.528162	t	\N	\N	\N	\N
5	DOC-001	729abc37-37ab-498e-9930-c0245eb95789.pdf	v1.0	\N	1		generated	Anonymous	2025-09-24 12:26:48.692223	t	\N	\N	\N	\N
9	TEST-DOC-001	Test Document	\N	\N	1	\N	This is a test comment for acceptance testing	Test Reviewer	2025-09-29 14:53:09.01686	f	accepted	2025-09-29 14:53:11.085291	This is a test justification for accepting the comment	1001
6	doc055	43c000c6-c7ec-4e63-b6d1-9d573df473a3.pdf	v1.1	1008	1		unknown lru	Anonymous	2025-09-29 14:34:35.485591	t	accepted	2025-09-29 14:55:05.842209	justification done\n	1003
10	doc055	43c000c6-c7ec-4e63-b6d1-9d573df473a3.pdf	v1.1	1008	1		Reference	Anonymous	2025-09-29 15:18:36.366238	t	accepted	2025-09-29 15:40:49.635536	rejected	1003
11	doc057	67f3c018-e0d0-4aca-94be-04a6268d284e.pdf	v1.3	1008	1		mahadev	Anonymous	2025-09-29 17:31:42.038152	t	accepted	2025-09-29 17:32:45.773568	just	1003
12	doc057	67f3c018-e0d0-4aca-94be-04a6268d284e.pdf	v1.3	1008	1		Avanthika	Anonymous	2025-09-29 17:31:53.127681	t	rejected	2025-09-29 17:34:07.251024	pg	1003
14	coc55	aa11f80a-5fb7-47de-9fa9-6eed11a39ac1.pdf	v1.0	1001	1		comment 2	1001	2025-10-10 09:38:24.492352	t	rejected	2025-10-10 09:41:40.379942	rej	1003
13	coc55	aa11f80a-5fb7-47de-9fa9-6eed11a39ac1.pdf	v1.0	1001	1		comment 1	1001	2025-10-10 09:38:12.61775	t	accepted	2025-10-10 09:41:56.222638	acc	1003
15	doc55	8692c214-54fd-4c1d-94df-a6ad951d78d4.docx	v1.0	1111	1		comment 1	1111	2025-10-13 09:50:41.124346	t	rejected	2025-10-13 09:51:06.634129	r	1005
16	doc55	8692c214-54fd-4c1d-94df-a6ad951d78d4.docx	v1.0	1111	1		comment 2	1111	2025-10-13 09:51:48.442172	t	accepted	2025-10-13 09:52:15.977725	a	1005
17	41	52227c1b-579b-4af3-b669-ac3a441e8b6d.docx		1001	1		testing 1	1001	2025-10-15 09:53:10.31626	t	\N	\N	\N	\N
18	41	52227c1b-579b-4af3-b669-ac3a441e8b6d.docx		1001	1		testing 1	1001	2025-10-15 09:54:07.426148	t	\N	\N	\N	\N
\.


--
-- Data for Name: document_reviews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.document_reviews (review_id, document_id, reviewer_id, status, review_date) FROM stdin;
\.


--
-- Data for Name: document_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.document_types (type_id, type_name, description, created_at, updated_at, deleted) FROM stdin;
1	srs	sw spec	2025-11-19 17:01:33.199601	2025-11-19 17:01:33.199601	f
2	tech	\N	2025-11-19 17:07:22.404362	2025-11-19 17:07:22.404362	f
\.


--
-- Data for Name: document_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.document_version (version_id, document_id, version, revision, doc_version, uploaded_by, uploaded_date, file_path) FROM stdin;
\.


--
-- Data for Name: iqa_observation_reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.iqa_observation_reports (report_id, project_id, lru_id, document_id, observation_count, report_date, current_year, lru_part_number, serial_number, inspection_stage, doc_review_date, review_venue, reference_document, reviewed_by_user_id, reviewed_by_signature_path, reviewed_by_verified_name, approved_by_user_id, approved_by_signature_path, approved_by_verified_name, created_by, created_at, updated_at) FROM stdin;
1	5500	42	44	OBS-001	2025-11-18	2025	hj	nm	Document review/report	2025-11-18	nm	bnm	1004	http://localhost:8000/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan	1004	http://localhost:8000/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan	1002	2025-11-18 11:42:21.351566+05:30	2025-11-18 11:42:21.351566+05:30
2	5500	43	50	OBS-001	2025-11-18	2025	partA	slA	Document review/report	2025-11-18	casdic	reference	1004	http://localhost:8000/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan	1004	http://localhost:8000/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan	1005	2025-11-18 12:28:21.52291+05:30	2025-11-18 12:28:21.52291+05:30
3	5500	43	53	OBS-001	2025-11-18	2025	LRUB	SLB	Document review/report	2025-11-18	CASDIC	REF	1004	http://localhost:8000/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan	1004	http://localhost:8000/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan	1005	2025-11-18 12:33:51.528121+05:30	2025-11-18 12:33:51.528121+05:30
\.


--
-- Data for Name: kit_of_parts_inspection_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kit_of_parts_inspection_report (report_id, project_name, dp_name, report_ref_no, memo_ref_no, lru_name, sru_name, part_no, quantity, sl_nos, test_venue, start_date, end_date, test1_sl_no, test1_case, test1_expected, test1_observations, test1_remarks, test1_upload, test2_sl_no, test2_case, test2_expected, test2_observations, test2_remarks, test2_upload, test3_sl_no, test3_case, test3_expected, test3_observations, test3_remarks, test3_upload, test4_sl_no, test4_case, test4_expected, test4_observations, test4_remarks, test4_upload, test5_sl_no, test5_case, test5_expected, test5_observations, test5_remarks, test5_upload, test6_sl_no, test6_case, test6_expected, test6_observations, test6_remarks, test6_upload, test7_sl_no, test7_case, test7_expected, test7_observations, test7_remarks, test7_upload, prepared_by_qa_g1, verified_by_g1h_qa_g, approved_by, created_at, updated_at, inspection_stage, dated1, dated2, original_report_id, report_card_id) FROM stdin;
11	ERP QA Automation Tool	fdgh	cxvbn	sdf	hjk	nm	ty56	3	5	cfgvbhjnk	2025-11-11 00:00:00	2025-11-12 00:00:00	1	Any observation pending from previous KOP stage	NIL	Nil	OK		2	CoC verification of components	Verified	Verified	OK		3	Quantity as BOM	Matching	Matching	OK		4	Quantity as per number of boards to be assembled	Matching	Matching	OK		5	Components storage in ESD cover	Stored in ESD	No	NOT OK		6	All connectors to be fitted with screws before assembly	Fitted properly	No	NOT OK		7	Any other observations	NIL	Yes	NOT OK		Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	2025-11-11 14:19:28.598558+05:30	2025-11-11 14:20:11.363667+05:30	hjkl	2025-11-10	2025-11-12	\N	20
12	ERP QA Automation Tool	fdgh	ytuio	sdf	dfghj	nm,	hbhjk	5	bnm 	bn	2025-11-11 00:00:00	2025-11-12 00:00:00	1	Any observation pending from previous KOP stage	NIL	Nil	OK		2	CoC verification of components	Verified	Not Verified	NOT OK		3	Quantity as BOM	Matching	Not Matching	NOT OK		4	Quantity as per number of boards to be assembled	Matching	Not Matching	NOT OK		5	Components storage in ESD cover	Stored in ESD	No	NOT OK		6	All connectors to be fitted with screws before assembly	Fitted properly	Yes	OK		7	Any other observations	NIL	Nil	OK		Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	yogesh|/api/users/signature/a2500efb-0918-427c-a736-654082cad781.png	yogesh|/api/users/signature/4910b6a9-91da-4de2-9cca-62c3ea88d79e.png	2025-11-11 14:23:28.598939+05:30	2025-11-17 10:58:17.381136+05:30	h	2025-11-12	2025-11-12	\N	2
10	aaa	xxx	1	1	sss	xxx	1	4	1,3	ggg	2025-11-03 00:00:00	2025-11-21 00:00:00	1	Any observation pending from previous KOP stage	NIL	Nil	OK		2	CoC verification of components	Verified	Not Verified	NOT OK		3	Quantity as BOM	Matching	Matching	OK		4	Quantity as per number of boards to be assembled	Matching	Matching	OK		5	Components storage in ESD cover	Stored in ESD	Yes	OK		6	All connectors to be fitted with screws before assembly	Fitted properly	Yes	OK		7	Any other observations	NIL	Yes	NOT OK		Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	Mohan|/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	2025-11-03 12:10:25.063906+05:30	2025-11-03 14:15:45.48033+05:30	fff	2025-11-07	2025-11-15	\N	9
\.


--
-- Data for Name: login_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.login_logs (serial_num, user_id, activity_performed, performed_by, "timestamp") FROM stdin;
1	1111	LOGIN	1111	2025-10-17 12:44:34.83937
2	1011	LOGIN	1011	2025-10-17 12:44:57.766601
3	1011	LOGIN	1011	2025-10-17 12:50:35.484916
4	1011	LOGOUT	1011	2025-10-17 12:51:05.971559
5	1111	LOGIN	1111	2025-10-17 12:51:20.300445
6	1111	LOGOUT	1111	2025-10-17 12:51:24.108443
7	1011	LOGIN	1011	2025-10-17 12:51:28.671177
8	1011	LOGOUT	1011	2025-10-17 12:51:34.5985
9	1005	LOGIN	1005	2025-10-17 12:51:35.648025
10	1005	LOGOUT	1005	2025-10-17 12:51:43.180605
11	1004	LOGIN	1004	2025-10-17 12:51:47.425954
12	1004	LOGOUT	1004	2025-10-17 12:51:52.860329
13	1003	LOGIN	1003	2025-10-17 12:51:57.004472
14	1003	LOGIN	1003	2025-10-17 12:52:02.323426
15	1011	LOGIN	1011	2025-10-17 12:52:05.641579
16	1011	LOGIN	1011	2025-10-21 10:11:54.047067
17	1011	LOGIN	1011	2025-10-21 10:19:19.042037
18	1011	LOGIN	1011	2025-10-21 10:21:40.780795
19	1003	LOGIN	1003	2025-10-21 10:22:41.27816
20	1003	LOGIN	1003	2025-10-21 10:40:37.646469
21	1111	LOGIN	1111	2025-10-21 10:41:07.388319
22	1111	LOGIN	1111	2025-10-21 10:59:08.869714
23	1111	LOGOUT	1111	2025-10-21 10:59:54.266483
24	1011	LOGIN	1011	2025-10-21 11:00:03.211303
25	1011	LOGOUT	1011	2025-10-21 11:00:22.044854
26	1111	LOGIN	1111	2025-10-21 11:00:23.945786
27	1111	LOGIN	1111	2025-10-21 11:07:07.698961
28	1011	LOGIN	1011	2025-10-21 11:07:12.496271
29	1011	LOGOUT	1011	2025-10-21 11:07:42.506041
30	1111	LOGIN	1111	2025-10-21 11:07:50.487384
31	1001	LOGIN	1001	2025-10-21 11:16:59.568278
32	1005	LOGIN	1005	2025-10-21 11:22:30.133545
33	1005	LOGIN	1005	2025-10-22 12:17:55.319063
34	1011	LOGIN	1011	2025-10-22 12:18:25.924402
35	1005	LOGIN	1005	2025-10-22 12:24:34.203089
36	1111	LOGIN	1111	2025-10-22 12:25:59.868122
37	1005	LOGIN	1005	2025-10-22 12:27:25.687127
38	1111	LOGIN	1111	2025-10-22 17:00:29.671971
39	1005	LOGIN	1005	2025-10-22 17:01:18.795744
40	1005	LOGIN	1005	2025-10-24 09:41:08.715944
41	1005	LOGIN	1005	2025-10-24 12:47:45.380117
42	1005	LOGIN	1005	2025-10-24 14:28:06.714818
43	1005	LOGIN	1005	2025-10-24 14:28:19.156209
44	1111	LOGIN	1111	2025-10-24 14:28:22.272385
45	1002	LOGIN	1002	2025-10-24 14:28:36.384492
46	1005	LOGIN	1005	2025-10-24 14:29:48.608018
47	1005	LOGIN	1005	2025-10-24 14:35:07.607736
48	1002	LOGIN	1002	2025-10-24 14:44:41.443172
49	1001	LOGIN	1001	2025-10-24 14:45:11.597696
50	1005	LOGIN	1005	2025-10-24 14:45:21.13703
51	1005	LOGIN	1005	2025-10-24 14:45:41.615862
52	1004	LOGIN	1004	2025-10-24 14:47:42.516275
53	1111	LOGIN	1111	2025-10-24 14:49:11.919272
54	1011	LOGIN	1011	2025-10-24 14:49:41.906464
55	1004	LOGIN	1004	2025-10-24 15:23:58.701268
56	1001	LOGIN	1001	2025-10-24 15:38:22.003323
57	1005	LOGIN	1005	2025-10-24 15:38:49.708913
58	1005	LOGIN	1005	2025-10-24 16:34:29.140566
59	1002	LOGIN	1002	2025-10-27 10:22:06.586769
60	1002	LOGIN	1002	2025-10-27 10:35:10.677809
61	1002	LOGIN	1002	2025-10-27 10:43:54.874489
62	1011	LOGIN	1011	2025-10-27 10:46:16.331282
63	1212	LOGIN	1212	2025-10-27 10:52:07.236271
64	1005	LOGIN	1005	2025-10-27 10:58:51.61002
65	1003	LOGIN	1003	2025-10-27 10:59:22.082463
66	1005	LOGIN	1005	2025-10-27 10:59:52.390342
67	1004	LOGIN	1004	2025-10-27 11:01:08.132067
68	1212	LOGIN	1212	2025-10-27 11:01:54.182531
69	1005	LOGIN	1005	2025-10-27 11:04:10.886548
70	1212	LOGIN	1212	2025-10-27 11:05:53.024083
71	1005	LOGIN	1005	2025-10-27 11:07:03.637378
72	1004	LOGIN	1004	2025-10-27 11:09:03.333878
73	1212	LOGIN	1212	2025-10-27 11:10:33.327688
74	1111	LOGIN	1111	2025-10-27 11:11:33.640347
75	1003	LOGIN	1003	2025-10-27 11:11:37.221912
76	1212	LOGIN	1212	2025-10-27 11:12:03.640504
77	1003	LOGIN	1003	2025-10-27 11:12:16.706269
78	1212	LOGIN	1212	2025-10-27 11:13:20.243061
79	1003	LOGIN	1003	2025-10-27 14:19:30.83632
80	1002	LOGIN	1002	2025-10-27 15:01:19.260667
81	1002	LOGIN	1002	2025-10-27 15:07:37.21049
82	1212	LOGIN	1212	2025-10-27 15:17:19.879091
83	1011	LOGIN	1011	2025-10-27 15:19:53.478885
84	1212	LOGIN	1212	2025-10-27 15:20:19.866804
85	1011	LOGIN	1011	2025-10-27 15:22:49.860428
86	1001	LOGIN	1001	2025-10-27 15:24:49.556822
87	1001	LOGIN	1001	2025-10-27 15:38:30.977425
88	1003	LOGIN	1003	2025-10-27 15:38:42.250582
89	1011	LOGIN	1011	2025-10-27 16:31:58.299263
90	1003	LOGIN	1003	2025-10-27 16:33:07.995122
91	1003	LOGIN	1003	2025-10-27 16:48:49.03069
92	1004	LOGIN	1004	2025-10-27 16:49:53.068144
93	1212	LOGIN	1212	2025-10-27 16:50:48.179099
94	1011	LOGIN	1011	2025-10-28 11:36:02.241339
95	1003	LOGIN	1003	2025-10-28 11:36:57.497438
96	1011	LOGIN	1011	2025-10-28 12:01:31.115071
97	1003	LOGIN	1003	2025-10-28 12:02:31.123907
98	1004	LOGIN	1004	2025-10-28 12:03:16.341512
99	1004	LOGIN	1004	2025-10-28 12:06:59.715044
100	1011	LOGIN	1011	2025-10-28 12:07:01.492956
101	1002	LOGIN	1002	2025-10-28 12:10:01.734175
102	1002	LOGIN	1002	2025-10-28 12:11:31.119843
103	1003	LOGIN	1003	2025-10-28 12:16:58.681722
104	1005	LOGIN	1005	2025-10-28 12:28:01.116721
105	1005	LOGIN	1005	2025-10-28 12:29:33.544253
106	1005	LOGOUT	1005	2025-10-28 12:30:31.553938
107	1003	LOGIN	1003	2025-10-28 12:30:56.844764
108	1003	LOGOUT	1003	2025-10-28 12:31:24.764738
109	1005	LOGIN	1005	2025-10-28 12:31:31.116805
110	1003	LOGIN	1003	2025-10-28 12:32:31.120864
111	1112	LOGIN	1112	2025-10-28 12:33:01.113696
112	1005	LOGIN	1005	2025-10-28 12:37:01.563775
113	1005	LOGOUT	1005	2025-10-28 12:38:00.917848
114	1004	LOGIN	1004	2025-10-28 12:38:10.458795
115	1005	LOGIN	1005	2025-10-28 12:38:31.122629
116	1005	LOGOUT	1005	2025-10-28 12:38:46.874575
117	1001	LOGIN	1001	2025-10-28 12:38:57.653159
118	1004	LOGIN	1004	2025-10-28 12:46:29.058828
119	1004	LOGIN	1004	2025-10-28 12:48:59.543458
120	1005	LOGIN	1005	2025-10-28 12:50:33.553068
121	1004	LOGIN	1004	2025-10-28 12:51:29.072889
122	1005	LOGIN	1005	2025-10-28 14:09:45.345822
123	1004	LOGIN	1004	2025-10-28 14:10:24.823897
124	1212	LOGIN	1212	2025-10-28 14:13:45.24855
125	1005	LOGIN	1005	2025-10-28 14:17:01.450193
126	1112	LOGIN	1112	2025-10-28 14:17:17.716332
127	1003	LOGIN	1003	2025-10-28 14:17:26.383433
128	1004	LOGIN	1004	2025-10-28 14:17:45.24872
129	1003	LOGIN	1003	2025-10-28 14:18:45.250312
130	1004	LOGIN	1004	2025-10-28 14:19:14.9406
131	1008	LOGIN	1008	2025-10-28 14:19:44.935138
132	1005	LOGIN	1005	2025-10-28 14:20:19.167838
133	1112	LOGIN	1112	2025-10-28 14:20:37.697723
134	1005	LOGIN	1005	2025-10-28 14:21:45.321577
135	1212	LOGIN	1212	2025-10-28 14:24:02.822563
136	1005	LOGIN	1005	2025-10-28 14:24:44.926119
137	1112	LOGIN	1112	2025-10-28 14:25:14.916529
138	1112	LOGIN	1112	2025-10-28 14:26:14.979126
139	1005	LOGIN	1005	2025-10-28 14:26:26.310261
140	1212	LOGIN	1212	2025-10-28 14:30:15.184051
141	1005	LOGIN	1005	2025-10-28 14:31:15.23854
142	1212	LOGIN	1212	2025-10-28 14:32:15.247065
143	1112	LOGIN	1112	2025-10-28 14:35:57.088971
144	1005	LOGIN	1005	2025-10-28 14:36:05.786932
145	1212	LOGIN	1212	2025-10-28 14:36:51.561452
146	1004	LOGIN	1004	2025-10-28 14:37:15.150702
147	1112	LOGIN	1112	2025-10-28 14:37:44.829715
148	1004	LOGIN	1004	2025-10-28 14:39:18.042973
149	1212	LOGIN	1212	2025-10-28 14:46:45.086017
150	1212	LOGIN	1212	2025-10-28 14:51:57.090415
151	1212	LOGIN	1212	2025-10-28 15:01:09.885151
152	1003	LOGIN	1003	2025-10-28 15:01:52.076073
153	1212	LOGIN	1212	2025-10-28 15:02:52.063038
154	1003	LOGIN	1003	2025-10-28 15:03:54.970208
155	1112	LOGIN	1112	2025-10-28 15:08:54.945601
156	1212	LOGIN	1212	2025-10-28 15:16:07.867839
157	1005	LOGIN	1005	2025-10-28 15:19:54.979087
158	1005	LOGIN	1005	2025-10-28 15:21:20.401813
159	1212	LOGIN	1212	2025-10-28 15:21:52.3647
160	1004	LOGIN	1004	2025-10-28 15:22:40.690505
161	1212	LOGIN	1212	2025-10-28 15:23:15.278415
162	1005	LOGIN	1005	2025-10-28 15:23:57.161041
163	1212	LOGIN	1212	2025-10-28 15:27:20.220166
164	1005	LOGIN	1005	2025-10-28 15:27:54.265854
165	1212	LOGIN	1212	2025-10-28 15:28:02.892147
166	1005	LOGIN	1005	2025-10-28 15:28:50.28763
167	1212	LOGIN	1212	2025-10-28 15:29:20.298817
168	1005	LOGIN	1005	2025-10-28 15:30:08.25428
169	1005	LOGIN	1005	2025-11-01 09:27:22.016783
170	1005	LOGIN	1005	2025-11-01 09:41:52.43367
171	1004	LOGIN	1004	2025-11-01 09:45:22.122575
172	1005	LOGIN	1005	2025-11-01 09:46:29.08022
173	1003	LOGIN	1003	2025-11-01 09:46:52.136174
174	1003	LOGIN	1003	2025-11-01 09:47:32.936608
175	1008	LOGIN	1008	2025-11-01 09:47:52.128294
176	1008	LOGIN	1008	2025-11-01 09:48:22.443126
177	1002	LOGIN	1002	2025-11-01 09:52:26.397793
178	1004	LOGIN	1004	2025-11-01 09:52:52.435812
179	1001	LOGIN	1001	2025-11-01 10:30:55.444963
180	1003	LOGIN	1003	2025-11-01 10:31:26.40453
181	1003	LOGIN	1003	2025-11-01 14:18:12.922333
182	1001	LOGIN	1001	2025-11-01 14:35:43.194462
183	1005	LOGIN	1005	2025-11-01 14:38:13.496314
184	1004	LOGIN	1004	2025-11-01 14:43:13.514221
185	1003	LOGIN	1003	2025-11-01 14:44:43.5149
186	1111	LOGIN	1111	2025-11-01 14:49:27.802779
187	1008	LOGIN	1008	2025-11-01 14:49:41.256138
188	1004	LOGIN	1004	2025-11-01 16:58:40.909187
189	1008	LOGIN	1008	2025-11-01 17:01:10.902862
190	1004	LOGIN	1004	2025-11-01 17:25:33.70262
191	1002	LOGIN	1002	2025-11-01 17:39:41.562655
192	1008	LOGIN	1008	2025-11-01 17:44:03.620803
193	1112	LOGIN	1112	2025-11-01 17:45:33.56955
194	1002	LOGIN	1002	2025-11-01 17:46:03.583345
195	1004	LOGIN	1004	2025-11-01 17:49:34.260991
196	1003	LOGIN	1003	2025-11-03 09:25:46.5287
197	1011	LOGIN	1011	2025-11-03 09:37:19.463321
198	1011	LOGIN	1011	2025-11-03 09:38:14.162844
199	1003	LOGIN	1003	2025-11-03 09:44:13.609054
200	1008	LOGIN	1008	2025-11-03 09:47:03.636061
201	1011	LOGIN	1011	2025-11-03 10:12:04.360808
202	1003	LOGIN	1003	2025-11-03 10:12:26.913895
203	1008	LOGIN	1008	2025-11-03 10:13:26.579199
204	1008	LOGOUT	1008	2025-11-03 10:19:57.400966
205	1003	LOGIN	1003	2025-11-03 10:20:20.26695
206	1008	LOGIN	1008	2025-11-03 10:22:27.422218
207	1004	LOGIN	1004	2025-11-03 11:58:54.282519
208	1008	LOGIN	1008	2025-11-03 12:01:25.073772
209	1008	LOGOUT	1008	2025-11-03 12:03:35.342787
210	1003	LOGIN	1003	2025-11-03 12:03:48.779139
211	1001	LOGIN	1001	2025-11-03 12:04:24.762802
212	1111	LOGIN	1111	2025-11-03 12:04:38.800582
213	1004	LOGIN	1004	2025-11-03 12:07:24.759274
214	1008	LOGIN	1008	2025-11-03 12:09:25.170176
215	1008	LOGIN	1008	2025-11-03 14:06:34.115611
216	1002	LOGIN	1002	2025-11-07 10:56:28.311991
217	1002	LOGIN	1002	2025-11-07 16:39:17.721625
218	1002	LOGIN	1002	2025-11-07 16:39:48.400229
219	1002	LOGIN	1002	2025-11-10 09:39:39.867511
220	1002	LOGIN	1002	2025-11-10 10:34:02.550979
221	1002	LOGIN	1002	2025-11-10 10:39:58.573327
222	1002	LOGIN	1002	2025-11-10 10:41:10.455922
223	1002	LOGIN	1002	2025-11-10 10:41:41.00449
224	1002	LOGIN	1002	2025-11-10 10:43:20.195042
225	1002	LOGIN	1002	2025-11-10 10:44:11.893385
226	1002	LOGIN	1002	2025-11-10 10:45:09.055758
227	1002	LOGIN	1002	2025-11-10 10:46:22.275153
228	1002	LOGIN	1002	2025-11-10 10:46:30.040206
229	1002	LOGIN	1002	2025-11-10 10:53:45.678888
230	1002	LOGIN	1002	2025-11-10 10:55:41.791232
231	1005	LOGIN	1005	2025-11-10 10:59:15.905994
232	1002	LOGIN	1002	2025-11-10 10:59:46.548878
233	1011	LOGIN	1011	2025-11-10 11:01:16.901663
234	1011	LOGIN	1011	2025-11-10 11:01:42.260088
235	1011	LOGIN	1011	2025-11-10 11:01:46.869339
236	1005	LOGIN	1005	2025-11-10 11:03:53.730021
237	1003	LOGIN	1003	2025-11-10 11:05:53.417876
238	1002	LOGIN	1002	2025-11-10 11:06:23.725049
239	1003	LOGOUT	1003	2025-11-10 11:12:39.852349
240	1002	LOGIN	1002	2025-11-10 11:12:52.561639
241	1002	LOGIN	1002	2025-11-10 11:37:37.611573
242	1002	LOGIN	1002	2025-11-10 11:37:47.683978
243	1002	LOGIN	1002	2025-11-10 11:38:17.564941
244	1011	LOGIN	1011	2025-11-10 11:38:19.608539
245	1003	LOGIN	1003	2025-11-10 11:38:31.404725
246	1003	LOGOUT	1003	2025-11-10 11:40:39.809513
247	1002	LOGIN	1002	2025-11-10 11:40:55.266976
248	1002	LOGIN	1002	2025-11-10 11:41:02.450019
249	1002	LOGOUT	1002	2025-11-10 11:41:04.39682
250	1002	LOGIN	1002	2025-11-10 11:41:16.674308
251	1002	LOGIN	1002	2025-11-10 11:41:46.251181
252	1002	LOGOUT	1002	2025-11-10 11:41:48.266139
253	1002	LOGIN	1002	2025-11-10 11:42:16.975359
254	1002	LOGIN	1002	2025-11-10 12:18:30.807774
255	1616	LOGIN	1616	2025-11-10 12:21:31.168792
256	1003	LOGIN	1003	2025-11-10 12:23:01.151792
257	1003	LOGIN	1003	2025-11-10 12:25:01.164479
258	1616	LOGIN	1616	2025-11-10 12:25:08.079209
259	1616	LOGIN	1616	2025-11-10 12:37:40.740289
260	1002	LOGIN	1002	2025-11-10 13:53:59.633125
261	1002	LOGIN	1002	2025-11-10 13:58:00.777901
262	1003	LOGIN	1003	2025-11-10 14:01:00.665937
263	1003	LOGIN	1003	2025-11-10 14:03:30.762877
264	1616	LOGIN	1616	2025-11-10 14:04:00.762532
265	1004	LOGIN	1004	2025-11-10 14:05:06.006536
266	1212	LOGIN	1212	2025-11-10 14:07:08.093059
267	1616	LOGIN	1616	2025-11-10 14:08:30.708815
268	1212	LOGIN	1212	2025-11-10 14:11:05.826008
269	1616	LOGIN	1616	2025-11-10 14:12:31.022581
270	1212	LOGIN	1212	2025-11-10 14:13:09.027432
271	1616	LOGIN	1616	2025-11-10 15:27:27.859979
272	1616	LOGIN	1616	2025-11-11 10:12:10.945452
273	1004	LOGIN	1004	2025-11-11 10:17:40.634233
274	1616	LOGIN	1616	2025-11-11 10:23:40.938159
275	1004	LOGIN	1004	2025-11-11 10:25:29.590479
276	1003	LOGIN	1003	2025-11-11 10:27:10.766266
277	1212	LOGIN	1212	2025-11-11 10:28:40.68096
278	1004	LOGIN	1004	2025-11-11 10:31:10.630992
279	1212	LOGIN	1212	2025-11-11 10:32:53.150046
280	1111	LOGIN	1111	2025-11-11 10:33:37.059838
281	1004	LOGIN	1004	2025-11-11 10:35:40.94377
282	1003	LOGIN	1003	2025-11-11 10:43:12.246777
283	1003	LOGOUT	1003	2025-11-11 12:11:39.932742
284	1004	LOGIN	1004	2025-11-11 12:12:39.935512
285	1003	LOGIN	1003	2025-11-11 14:17:58.606126
286	1004	LOGIN	1004	2025-11-11 14:21:28.591943
287	1003	LOGIN	1003	2025-11-11 14:21:58.289305
288	1002	LOGIN	1002	2025-11-12 09:02:27.553909
289	1002	LOGOUT	1002	2025-11-12 09:02:42.355255
290	1002	LOGIN	1002	2025-11-12 09:07:10.970781
291	1002	LOGIN	1002	2025-11-12 10:18:08.522557
292	1002	LOGIN	1002	2025-11-12 10:39:29.837377
293	1002	LOGIN	1002	2025-11-12 10:44:16.788914
294	1002	LOGOUT	1002	2025-11-12 10:44:46.781315
295	1002	LOGIN	1002	2025-11-12 10:45:16.472575
296	1002	LOGOUT	1002	2025-11-12 11:07:11.752423
297	1002	LOGIN	1002	2025-11-12 11:24:01.97732
298	1002	LOGIN	1002	2025-11-13 09:34:14.894893
299	1002	LOGOUT	1002	2025-11-13 09:35:16.125418
300	1002	LOGIN	1002	2025-11-13 09:39:31.924102
301	1002	LOGOUT	1002	2025-11-13 09:39:37.892805
302	1002	LOGIN	1002	2025-11-13 09:39:59.501857
303	1002	LOGOUT	1002	2025-11-13 09:43:25.660178
304	1002	LOGIN	1002	2025-11-13 09:50:02.204928
305	1002	LOGOUT	1002	2025-11-13 09:50:32.530796
306	1002	LOGIN	1002	2025-11-13 09:53:03.615828
307	1002	LOGOUT	1002	2025-11-13 09:55:34.118897
308	1002	LOGIN	1002	2025-11-13 10:02:10.542122
309	1002	LOGOUT	1002	2025-11-13 10:02:40.917077
310	1002	LOGIN	1002	2025-11-13 10:02:47.22147
311	1002	LOGOUT	1002	2025-11-13 10:02:48.756585
312	1002	LOGIN	1002	2025-11-13 10:31:24.327243
313	1002	LOGIN	1002	2025-11-13 10:50:50.131081
314	1002	LOGIN	1002	2025-11-13 11:36:00.272492
315	1002	LOGIN	1002	2025-11-13 11:55:16.257415
316	1002	LOGIN	1002	2025-11-13 12:06:08.493327
317	1002	LOGIN	1002	2025-11-13 12:36:52.240613
318	1002	LOGIN	1002	2025-11-13 12:39:49.356082
319	1002	LOGOUT	1002	2025-11-13 12:49:11.270159
320	1002	LOGIN	1002	2025-11-13 12:50:14.525101
321	1002	LOGIN	1002	2025-11-13 14:28:06.307655
322	1002	LOGOUT	1002	2025-11-13 14:29:06.777487
323	1002	LOGIN	1002	2025-11-13 16:04:30.283508
324	1002	LOGIN	1002	2025-11-13 16:05:00.469622
325	1002	LOGOUT	1002	2025-11-13 16:12:31.382269
326	1515	LOGIN	1515	2025-11-13 16:15:30.475334
327	1515	LOGOUT	1515	2025-11-13 16:16:30.787173
328	1002	LOGOUT	1002	2025-11-13 16:17:14.266915
329	1003	LOGIN	1003	2025-11-13 16:17:38.282282
330	1003	LOGOUT	1003	2025-11-13 16:18:07.976257
331	1004	LOGIN	1004	2025-11-13 16:18:37.977047
332	1003	LOGIN	1003	2025-11-14 10:08:54.502616
333	1003	LOGOUT	1003	2025-11-14 10:09:24.197763
334	1002	LOGIN	1002	2025-11-14 10:10:24.195906
335	1002	LOGIN	1002	2025-11-14 10:12:19.608772
336	1002	LOGIN	1002	2025-11-14 17:00:36.018577
337	1003	LOGIN	1003	2025-11-14 17:45:01.18002
338	1003	LOGIN	1003	2025-11-14 17:45:08.544857
339	1003	LOGOUT	1003	2025-11-14 17:45:31.393652
340	1003	LOGIN	1003	2025-11-14 17:46:31.033829
341	1003	LOGOUT	1003	2025-11-14 17:46:43.730249
342	1003	LOGIN	1003	2025-11-14 17:50:07.822385
343	1003	LOGIN	1003	2025-11-14 17:50:30.680604
344	1003	LOGOUT	1003	2025-11-14 17:51:30.992068
345	1003	LOGIN	1003	2025-11-14 17:51:45.370155
346	1011	LOGIN	1011	2025-11-14 17:58:16.025305
347	1002	LOGIN	1002	2025-11-14 17:58:27.885914
348	1002	LOGIN	1002	2025-11-14 17:58:45.705217
349	1003	LOGIN	1003	2025-11-14 17:59:16.024975
350	1002	LOGIN	1002	2025-11-14 18:05:46.028078
351	1002	LOGIN	1002	2025-11-17 09:49:18.491245
352	1004	LOGIN	1004	2025-11-17 10:02:18.353008
353	1003	LOGIN	1003	2025-11-17 10:02:47.704481
354	1004	LOGIN	1004	2025-11-17 10:07:47.381684
355	1004	LOGOUT	1004	2025-11-17 10:12:38.613697
356	1002	LOGIN	1002	2025-11-17 10:12:47.695611
357	1002	LOGOUT	1002	2025-11-17 10:18:23.022334
358	1004	LOGIN	1004	2025-11-17 10:18:32.597336
359	1003	LOGIN	1003	2025-11-17 10:38:47.380322
360	1011	LOGIN	1011	2025-11-17 10:40:49.35197
361	1011	LOGIN	1011	2025-11-17 10:41:15.622283
362	1011	LOGIN	1011	2025-11-17 10:41:17.692802
363	1002	LOGIN	1002	2025-11-17 10:41:37.547651
364	1002	LOGOUT	1002	2025-11-17 10:42:17.705233
365	1515	LOGIN	1515	2025-11-17 10:42:39.508922
366	1515	LOGIN	1515	2025-11-17 10:42:47.73729
367	1515	LOGIN	1515	2025-11-17 10:47:39.749374
368	1003	LOGIN	1003	2025-11-17 10:48:17.688674
369	1004	LOGIN	1004	2025-11-17 10:55:17.379894
370	1004	LOGOUT	1004	2025-11-17 10:56:17.382285
371	1515	LOGIN	1515	2025-11-17 10:56:33.693577
372	1515	LOGIN	1515	2025-11-17 11:02:35.236385
373	1515	LOGIN	1515	2025-11-17 11:34:09.709977
374	1515	LOGIN	1515	2025-11-17 11:34:20.449867
375	1515	LOGIN	1515	2025-11-17 15:35:34.856572
376	1515	LOGIN	1515	2025-11-17 15:36:03.382314
377	1515	LOGOUT	1515	2025-11-17 15:36:05.56725
378	1002	LOGIN	1002	2025-11-17 15:37:35.12858
379	1002	LOGOUT	1002	2025-11-17 16:29:05.435751
380	1002	LOGIN	1002	2025-11-17 16:29:28.775232
381	1002	LOGIN	1002	2025-11-17 16:29:35.446468
382	1001	LOGIN	1001	2025-11-18 08:47:50.813949
383	1001	LOGIN	1001	2025-11-18 09:08:35.498509
384	1002	LOGIN	1002	2025-11-18 10:02:56.157108
385	1002	LOGIN	1002	2025-11-18 10:03:21.342962
386	1002	LOGIN	1002	2025-11-18 10:03:51.350173
387	1003	LOGIN	1003	2025-11-18 10:05:21.347741
388	1005	LOGIN	1005	2025-11-18 10:06:21.505991
389	1002	LOGIN	1002	2025-11-18 10:09:21.514085
390	1005	LOGIN	1005	2025-11-18 10:20:05.377679
391	1003	LOGIN	1003	2025-11-18 11:30:21.363087
392	1002	LOGIN	1002	2025-11-18 11:41:21.356813
393	1002	LOGIN	1002	2025-11-18 11:53:22.050821
394	1003	LOGIN	1003	2025-11-18 12:22:21.52348
395	1001	LOGIN	1001	2025-11-18 12:23:51.523017
396	1111	LOGIN	1111	2025-11-18 12:23:58.05446
397	1616	LOGIN	1616	2025-11-18 12:24:08.114299
398	1008	LOGIN	1008	2025-11-18 12:24:23.569985
399	1002	LOGIN	1002	2025-11-18 12:24:29.825566
400	1004	LOGIN	1004	2025-11-18 12:24:39.40681
401	1212	LOGIN	1212	2025-11-18 12:24:51.523915
402	1005	LOGIN	1005	2025-11-18 12:25:55.993321
403	1002	LOGIN	1002	2025-11-18 12:37:51.52134
404	1004	LOGIN	1004	2025-11-18 12:56:21.525367
405	1002	LOGIN	1002	2025-11-19 10:02:17.156765
406	1002	LOGIN	1002	2025-11-19 10:02:45.179619
407	1002	LOGIN	1002	2025-11-19 10:02:47.825798
408	1002	LOGOUT	1002	2025-11-19 10:45:08.132561
409	1002	LOGIN	1002	2025-11-19 10:46:15.87213
410	1002	LOGOUT	1002	2025-11-19 12:17:33.888454
411	1002	LOGIN	1002	2025-11-19 12:17:41.070767
412	1002	LOGOUT	1002	2025-11-19 12:18:15.80493
413	1001	LOGIN	1001	2025-11-19 12:18:33.621169
414	1001	LOGOUT	1001	2025-11-19 12:18:38.739019
415	1002	LOGIN	1002	2025-11-19 12:18:48.589318
416	1002	LOGOUT	1002	2025-11-19 12:22:03.639068
417	1002	LOGIN	1002	2025-11-19 12:22:12.630635
418	1002	LOGOUT	1002	2025-11-19 12:22:14.646119
419	1005	LOGIN	1005	2025-11-19 12:22:29.361015
420	1005	LOGOUT	1005	2025-11-19 12:24:03.61874
421	1001	LOGIN	1001	2025-11-19 12:24:33.617199
422	1001	LOGOUT	1001	2025-11-19 12:24:44.328344
423	1003	LOGIN	1003	2025-11-19 12:25:03.926209
424	1003	LOGOUT	1003	2025-11-19 12:29:03.617899
425	1001	LOGIN	1001	2025-11-19 12:29:28.253519
426	1001	LOGOUT	1001	2025-11-19 12:41:49.125029
427	1005	LOGIN	1005	2025-11-19 12:42:06.071231
428	1005	LOGOUT	1005	2025-11-19 12:45:03.612271
429	1002	LOGIN	1002	2025-11-19 12:45:13.394361
430	1002	LOGOUT	1002	2025-11-19 12:45:18.350802
431	1112	LOGIN	1112	2025-11-19 12:45:43.388857
432	1112	LOGOUT	1112	2025-11-19 12:45:48.341686
433	1616	LOGIN	1616	2025-11-19 12:46:13.387611
434	1616	LOGOUT	1616	2025-11-19 12:46:18.036658
435	1003	LOGIN	1003	2025-11-19 12:46:31.739415
436	1003	LOGOUT	1003	2025-11-19 12:50:30.843443
437	1005	LOGIN	1005	2025-11-19 12:50:43.385377
438	1005	LOGOUT	1005	2025-11-19 12:50:48.339637
439	1616	LOGIN	1616	2025-11-19 12:51:05.641898
440	1616	LOGOUT	1616	2025-11-19 12:51:18.353207
441	1112	LOGIN	1112	2025-11-19 12:51:32.051588
442	1112	LOGOUT	1112	2025-11-19 13:00:48.343124
475	1005	LOGIN	1005	2025-11-19 15:32:32.814133
476	1005	LOGOUT	1005	2025-11-19 15:33:02.067004
477	1003	LOGIN	1003	2025-11-19 15:33:21.205093
478	1003	LOGOUT	1003	2025-11-19 15:51:27.825342
479	1112	LOGIN	1112	2025-11-19 15:51:41.429979
480	1112	LOGOUT	1112	2025-11-19 15:52:11.44225
481	1002	LOGIN	1002	2025-11-19 15:52:38.532282
482	1002	LOGOUT	1002	2025-11-19 16:02:00.696345
483	1112	LOGIN	1112	2025-11-19 16:02:57.124245
484	1112	LOGOUT	1112	2025-11-19 16:06:03.362298
485	1002	LOGIN	1002	2025-11-19 16:06:27.137349
486	1003	LOGIN	1003	2025-11-19 16:59:38.850196
487	1003	LOGOUT	1003	2025-11-19 17:06:45.825987
488	1002	LOGIN	1002	2025-11-19 17:07:15.476293
489	1002	LOGIN	1002	2025-11-20 14:54:20.806764
490	1002	LOGOUT	1002	2025-11-20 14:54:28.236533
491	1002	LOGIN	1002	2025-11-20 14:57:21.790327
492	1002	LOGOUT	1002	2025-11-20 14:57:51.86191
493	1003	LOGIN	1003	2025-11-20 14:58:32.96367
494	1003	LOGOUT	1003	2025-11-20 15:00:47.216053
496	1003	LOGOUT	1003	2025-11-20 15:22:35.382832
497	1003	LOGIN	1003	2025-11-20 15:29:03.861376
498	1002	LOGOUT	1002	2025-11-20 15:47:51.032948
499	1002	LOGIN	1002	2025-11-20 15:48:47.229895
500	1002	LOGOUT	1002	2025-11-20 16:22:31.322324
501	1002	LOGIN	1002	2025-11-20 16:22:59.916533
502	1002	LOGOUT	1002	2025-11-20 16:23:01.893209
503	1003	LOGOUT	1003	2025-11-20 16:59:58.508137
504	1003	LOGIN	1003	2025-11-20 17:00:04.040697
505	1003	LOGOUT	1003	2025-11-20 17:00:28.528339
506	1003	LOGIN	1003	2025-11-21 10:39:29.530673
507	1003	LOGOUT	1003	2025-11-21 10:57:25.64642
508	1003	LOGIN	1003	2025-11-21 10:57:41.907862
509	1003	LOGOUT	1003	2025-11-21 11:01:29.612618
510	1002	LOGIN	1002	2025-11-21 11:01:56.481487
511	1002	LOGOUT	1002	2025-11-21 11:02:00.229767
512	1004	LOGIN	1004	2025-11-21 11:02:29.622197
513	1004	LOGOUT	1004	2025-11-21 11:02:31.797507
514	1002	LOGIN	1002	2025-11-21 11:23:49.42466
515	1002	LOGOUT	1002	2025-11-24 12:21:07.811588
516	1002	LOGIN	1002	2025-11-24 12:21:37.99188
517	1002	LOGOUT	1002	2025-11-24 12:22:37.992248
518	1002	LOGIN	1002	2025-11-24 12:22:43.264968
519	1002	LOGOUT	1002	2025-11-25 12:23:18.948089
520	1003	LOGIN	1003	2025-11-25 12:23:27.768093
521	1003	LOGOUT	1003	2025-11-25 12:29:34.821532
522	1003	LOGIN	1003	2025-11-25 12:29:48.313378
523	1002	LOGOUT	1002	2025-11-25 13:08:24.050219
524	1002	LOGIN	1002	2025-11-25 13:08:35.250026
525	1002	LOGOUT	1002	2025-11-25 13:08:36.886077
526	1002	LOGIN	1002	2025-11-25 13:24:54.141591
527	1002	LOGOUT	1002	2025-11-25 13:25:00.424254
528	1003	LOGIN	1003	2025-11-25 13:25:24.145409
529	1003	LOGOUT	1003	2025-11-25 13:37:07.901759
530	1003	LOGIN	1003	2025-11-25 13:37:31.500263
531	1003	LOGOUT	1003	2025-11-25 14:09:13.983558
532	1002	LOGIN	1002	2025-11-25 14:09:22.655362
533	1002	LOGOUT	1002	2025-11-25 14:09:24.71004
534	1003	LOGIN	1003	2025-11-25 14:09:33.676513
535	1003	LOGOUT	1003	2025-11-25 14:58:14.532357
536	1002	LOGIN	1002	2025-11-25 14:58:21.423541
537	1003	LOGOUT	1003	2025-11-25 15:11:38.410279
538	1003	LOGIN	1003	2025-11-25 15:11:46.381333
539	1003	LOGOUT	1003	2025-11-25 15:11:47.872847
540	1002	LOGIN	1002	2025-11-25 15:11:55.013183
541	1002	LOGOUT	1002	2025-11-25 15:32:59.638466
542	1003	LOGIN	1003	2025-11-25 15:33:08.111046
543	1003	LOGOUT	1003	2025-11-25 15:40:08.490655
544	1003	LOGIN	1003	2025-11-25 15:45:36.615095
545	1002	LOGOUT	1002	2025-11-25 15:55:16.697504
546	1003	LOGIN	1003	2025-11-25 15:55:21.534003
547	1003	LOGOUT	1003	2025-11-25 15:58:59.117746
548	1004	LOGIN	1004	2025-11-25 15:59:06.313671
549	1004	LOGOUT	1004	2025-11-25 15:59:59.105013
550	1001	LOGIN	1001	2025-11-25 16:00:18.60579
551	1001	LOGOUT	1001	2025-11-25 16:00:29.123301
552	1004	LOGIN	1004	2025-11-25 16:00:41.170046
553	1004	LOGOUT	1004	2025-11-25 16:01:14.555128
554	1212	LOGIN	1212	2025-11-25 16:01:23.175276
555	1212	LOGOUT	1212	2025-11-25 16:01:57.377028
556	1002	LOGIN	1002	2025-11-25 16:02:27.007915
557	1002	LOGOUT	1002	2025-11-25 16:03:27.422685
558	1003	LOGIN	1003	2025-11-25 16:03:51.325868
559	1003	LOGOUT	1003	2025-11-25 16:04:38.797059
560	1004	LOGIN	1004	2025-11-25 16:04:46.513072
561	1004	LOGOUT	1004	2025-11-25 16:05:05.554614
562	1001	LOGIN	1001	2025-11-25 16:05:17.737979
563	1001	LOGOUT	1001	2025-11-25 16:06:27.423905
564	1002	LOGIN	1002	2025-11-25 16:06:36.174481
565	1002	LOGOUT	1002	2025-11-25 16:07:08.252228
566	1001	LOGIN	1001	2025-11-25 16:07:16.830345
567	1001	LOGOUT	1001	2025-11-25 16:09:57.797548
568	1003	LOGIN	1003	2025-11-25 16:10:27.424402
569	1003	LOGOUT	1003	2025-11-25 16:13:27.411088
570	1001	LOGIN	1001	2025-11-25 16:13:35.763082
571	1001	LOGOUT	1001	2025-11-25 16:18:27.417888
572	1003	LOGIN	1003	2025-11-25 16:18:55.277744
573	1003	LOGOUT	1003	2025-11-25 16:33:57.648973
574	1001	LOGIN	1001	2025-11-25 16:34:18.459608
575	1003	LOGOUT	1003	2025-11-25 16:58:15.549952
576	1003	LOGIN	1003	2025-11-25 16:58:31.367685
577	1001	LOGOUT	1001	2025-11-25 19:49:33.136058
578	1001	LOGIN	1001	2025-11-25 19:50:03.296516
579	1003	LOGOUT	1003	2025-11-25 20:10:42.860872
580	1003	LOGIN	1003	2025-11-25 20:10:51.303371
581	1001	LOGOUT	1001	2025-11-25 20:19:51.570821
582	1001	LOGIN	1001	2025-11-25 20:19:58.247404
583	1001	LOGOUT	1001	2025-11-25 20:19:59.984617
584	1003	LOGIN	1003	2025-11-25 20:20:08.461556
585	1003	LOGOUT	1003	2025-11-25 20:21:01.947297
586	1002	LOGIN	1002	2025-11-25 20:21:31.969024
587	1003	LOGOUT	1003	2025-11-25 20:24:13.087683
588	1003	LOGIN	1003	2025-11-25 20:42:02.509926
589	1003	LOGOUT	1003	2025-11-25 20:44:48.461196
590	1002	LOGIN	1002	2025-11-25 20:49:35.621405
591	1002	LOGOUT	1002	2025-11-25 20:50:35.9392
592	1002	LOGIN	1002	2025-11-25 20:57:14.742267
593	1002	LOGOUT	1002	2025-11-25 20:57:45.210333
594	1003	LOGIN	1003	2025-11-25 20:57:50.867139
595	1003	LOGOUT	1003	2025-11-25 21:00:09.783899
596	1003	LOGIN	1003	2025-11-25 21:00:15.70385
597	1002	LOGOUT	1002	2025-11-25 23:32:25.850472
598	1003	LOGOUT	1003	2025-11-26 08:43:56.976587
599	1003	LOGIN	1003	2025-11-26 08:44:03.075621
600	1003	LOGOUT	1003	2025-11-26 08:44:27.058824
601	1002	LOGIN	1002	2025-11-26 08:44:47.842527
602	1003	LOGIN	1003	2025-11-26 10:50:56.858887
603	1003	LOGIN	1003	2025-11-26 10:59:16.391501
604	1002	LOGOUT	1002	2025-11-26 11:46:06.104302
605	1003	LOGIN	1003	2025-11-26 11:46:18.98732
606	1003	LOGOUT	1003	2025-11-26 12:03:01.306557
607	1003	LOGIN	1003	2025-11-26 12:03:14.434067
608	1003	LOGOUT	1003	2025-11-26 12:06:57.852708
609	1003	LOGIN	1003	2025-11-26 12:07:03.990854
610	1003	LOGOUT	1003	2025-11-26 12:32:14.81278
611	1003	LOGIN	1003	2025-11-26 12:32:19.791246
612	1003	LOGOUT	1003	2025-11-26 13:01:58.38938
613	1003	LOGIN	1003	2025-11-26 16:05:49.431946
614	1003	LOGOUT	1003	2025-12-08 08:25:34.048343
615	1003	LOGIN	1003	2025-12-08 08:36:39.018565
616	1003	LOGOUT	1003	2025-12-08 08:36:59.834484
617	1002	LOGIN	1002	2025-12-08 08:37:09.014524
618	1002	LOGOUT	1002	2025-12-08 09:20:39.018335
619	1002	LOGIN	1002	2025-12-08 09:26:39.017371
620	1002	LOGOUT	1002	2025-12-08 09:26:44.901313
621	1002	LOGIN	1002	2025-12-08 09:33:09.020576
622	1002	LOGOUT	1002	2025-12-08 09:43:09.01612
623	1002	LOGIN	1002	2025-12-08 09:43:30.975117
624	1002	LOGOUT	1002	2025-12-08 09:51:39.016917
625	1001	LOGIN	1001	2025-12-09 11:22:06.79052
626	1001	LOGOUT	1001	2025-12-09 11:22:38.131433
627	1003	LOGIN	1003	2025-12-09 11:22:53.065457
628	1002	LOGIN	1002	2025-12-18 11:16:43.829642
\.


--
-- Data for Name: lrus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lrus (lru_id, project_id, lru_name, created_at, lru_part_number) FROM stdin;
3	2	GPS Receiver	2025-08-20 16:12:03.257438	\N
4	2	Navigation Display	2025-08-20 16:12:03.257438	\N
5	3	lru	2025-09-05 11:30:29.191263	\N
6	5	sample lru	2025-09-24 11:59:06.48209	\N
7	12345	Test LRU	2025-09-26 15:34:46.869026	\N
8	99999	Test LRU	2025-09-26 15:43:00.558097	\N
9	100001	Admin LRU	2025-09-26 15:43:00.629369	\N
10	200001	Admin LRU	2025-09-26 15:44:11.857954	\N
11	999999	Test LRU	2025-09-26 15:44:59.42699	\N
12	300001	Admin LRU	2025-09-26 15:45:24.327494	\N
13	9999999	Test LRU	2025-09-26 16:00:01.999662	\N
14	3000001	Admin LRU	2025-09-26 16:00:02.166858	\N
15	76513893	Test LRU	2025-09-26 16:11:16.614758	\N
16	21406228	Admin LRU	2025-09-26 16:11:16.763137	\N
17	21377527	Test LRU	2025-09-26 16:11:56.467559	\N
18	26244255	Admin LRU	2025-09-26 16:12:02.400893	\N
19	21973383	Admin LRU	2025-09-26 16:12:12.863081	\N
20	28170588	Admin LRU	2025-09-26 16:12:22.894692	\N
21	70646485	Test LRU	2025-09-26 16:12:30.57494	\N
22	25268707	Admin LRU	2025-09-26 16:12:30.731442	\N
23	67995283	Test LRU	2025-09-26 16:12:40.435997	\N
24	23290007	Admin LRU	2025-09-26 16:12:40.562028	\N
25	90691014	Test LRU	2025-09-26 17:47:21.702261	\N
26	23906058	Admin LRU	2025-09-26 17:47:21.898116	\N
27	85546124	Test LRU	2025-09-26 17:52:19.335336	\N
28	66820093	Test LRU	2025-09-26 19:28:47.649889	\N
29	25789744	Admin LRU	2025-09-26 19:28:47.770224	\N
30	71332586	Test LRU	2025-09-26 19:31:47.343095	\N
31	25048373	Test LRU	2025-09-26 19:32:03.952164	\N
32	28030449	Admin LRU	2025-09-26 19:32:04.01286	\N
33	29600208	Admin LRU	2025-09-26 19:32:35.159488	\N
34	67312557	Test LRU	2025-09-26 19:52:10.952905	\N
35	28141924	Admin LRU	2025-09-26 19:52:11.023473	\N
36	22199255	Test LRU	2025-09-27 11:00:51.166378	\N
37	28713804	Admin LRU	2025-09-27 11:00:51.230514	\N
38	64301877	Test LRU	2025-09-27 11:16:34.216149	\N
39	22434888	Admin LRU	2025-09-27 11:16:34.276589	\N
40	55	testing orm -1 	2025-10-13 04:14:49.478547	\N
41	55	testing orm -2	2025-10-13 04:14:49.484752	\N
1	1	Flight Computer	2025-08-20 16:12:03.257438	\N
2	1	Autopilot Systems	2025-08-20 16:12:03.257438	\N
42	5500	dharsh 1	2025-10-27 10:47:56.855262	\N
43	5500	dharsh 2	2025-10-27 10:47:56.855262	\N
44	121212	demo_lru	2025-10-27 16:32:48.171878	\N
45	111111	thanish1	2025-10-28 11:36:32.151842	\N
46	12344321	pglru	2025-10-28 12:02:00.810309	\N
47	100694	manual01	2025-11-10 11:17:10.151508	\N
48	100694	manual02	2025-11-10 11:17:10.151508	\N
49	4004	LRU4001	2025-11-19 10:32:54.812549	4001
50	4004	LRU4002	2025-11-19 10:32:54.812549	4003
51	4004	LRU4005	2025-11-19 16:01:30.694491	4005
52	4321	project123_4321 -1 	2025-11-25 14:59:14.538937	4321-1
53	11	q	2025-11-25 15:02:53.268728	1
54	54	a	2025-11-25 15:15:26.160504	a1
55	1010	TESTING_CASDIC	2025-11-25 16:02:57.418185	23456
56	1010	TESTING 2	2025-11-25 16:06:57.419042	65432
\.


--
-- Data for Name: mechanical_inspection_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mechanical_inspection_report (report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, part_no, inspection_stage, test_venue, quantity, sl_nos, start_date, end_date, dated1, dated2, dim1_dimension, dim1_tolerance, dim1_observed_value, dim1_instrument_used, dim1_remarks, dim1_upload, dim2_dimension, dim2_tolerance, dim2_observed_value, dim2_instrument_used, dim2_remarks, dim2_upload, dim3_dimension, dim3_tolerance, dim3_observed_value, dim3_instrument_used, dim3_remarks, dim3_upload, param1_name, param1_compliance_observation, param1_expected, param1_remarks, param1_upload, param2_name, param2_compliance_observation, param2_expected, param2_remarks, param2_upload, param3_name, param3_compliance_observation, param3_expected, param3_remarks, param3_upload, param4_name, param4_compliance_observation, param4_expected, param4_remarks, param4_upload, param5_name, param5_compliance_observation, param5_expected, param5_remarks, param5_upload, param6_name, param6_compliance_observation, param6_expected, param6_remarks, param6_upload, param7_name, param7_compliance_observation, param7_expected, param7_remarks, param7_upload, param8_name, param8_compliance_observation, param8_expected, param8_remarks, param8_upload, overall_status, quality_rating, recommendations, prepared_by, verified_by, approved_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: memo_approval; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.memo_approval (approval_id, memo_id, user_id, comments, authentication, attachment_path, status, approval_date, approved_by, test_date) FROM stdin;
10	7	\N	chk status	authenticated	\N	rejected	2025-09-26 10:42:13.626082	1004	\N
21	9	1008	dsfghj	/api/users/signature/f1d6c65b-cb5b-4d56-bc0d-cc70b2ee1ad1.png	\N	accepted	2025-10-09 14:58:45.046277	1004	2025-10-18 19:59:00
22	6	1001	accept 1	/api/users/signature/f1d6c65b-cb5b-4d56-bc0d-cc70b2ee1ad1.png	\N	accepted	2025-10-10 09:13:25.153408	1004	2025-10-11 09:12:00
23	3	1008	accept 2	/api/users/signature/5cd02dac-7eb6-4624-8bfb-9efe11c14380.png	\N	accepted	2025-10-10 09:14:10.314834	1004	2025-10-10 09:16:00
24	5	1008	accept 3	/api/users/signature/f1d6c65b-cb5b-4d56-bc0d-cc70b2ee1ad1.png	\N	accepted	2025-10-10 09:14:57.473316	1004	2025-10-10 00:14:00
26	13	1003	cgvhbjk	/api/users/signature/f1d6c65b-cb5b-4d56-bc0d-cc70b2ee1ad1.png	\N	accepted	2025-10-10 16:54:41.684181	1004	2025-10-10 16:50:00
28	4	1111	bnm,	/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	\N	accepted	2025-10-15 16:11:13.203177	1004	2025-10-15 16:10:00
30	14	\N	reject test 	/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	\N	rejected	2025-10-24 15:24:44.456649	1004	\N
31	15	1212	bnm,	/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	\N	accepted	2025-10-27 11:09:50.981964	1004	2025-10-27 01:09:00
32	16	1008	comment accep	/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	\N	accepted	2025-11-01 09:46:27.342036	1004	\N
33	17	1212	accepted	/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	memo_approval_uploads/ec85167c-1126-43b6-a3f1-5e95694c5abd.pdf	accepted	2025-11-11 10:21:30.732734	1004	2025-11-12 10:20:00
34	18	1001	comments	/api/users/signature/a2500efb-0918-427c-a736-654082cad781.png	\N	accepted	2025-11-13 16:19:31.142344	1004	2025-11-13 16:18:00
35	19	\N	ghjk	/api/users/signature/4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	\N	rejected	2025-11-17 10:24:56.035363	1004	\N
\.


--
-- Data for Name: memo_references; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.memo_references (ref_id, memo_id, ref_doc, ref_no, ver, rev) FROM stdin;
1	3	doc-11	docref	1	1
2	5	doc001	document	1	1
3	7	doc008	document 8	1	2
4	17	fg	fghjk	78	76
5	20	jj	k	\N	\N
\.


--
-- Data for Name: memos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.memos (memo_id, from_person, to_person, thru_person, casdic_ref_no, dated, wing_proj_ref_no, lru_sru_desc, part_number, slno_units, qty_offered, manufacturer, drawing_no_rev, source, unit_identification, mechanical_inspn, inspn_test_stage_offered, stte_status, test_stage_cleared, venue, memo_date, name_designation, test_facility, test_cycle_duration, test_start_on, test_complete_on, calibration_status, func_check_initial, perf_check_during, func_check_end, certified, remarks, submitted_at, submitted_by, accepted_at, accepted_by, coordinator, memo_status, template_id, qa_remarks, qa_signature) FROM stdin;
19	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-11-17	demoo	testing orm -2	nm	{1}	1	kjn	 nm	NA	{SoFT,"Endurance Vibration Test","Post RV Functional Check","Functional Check"}	ASSY	m,m,	mn 	nm 		2025-11-17				\N	\N		\N	\N	\N	{}		2025-11-17 10:07:31.4732	1003	\N	\N	mn,	rejected	\N	\N	\N
4	Mahaashri C V	QA Head			\N	\N	lru	22www	{}	0	mmmm	\N	\N	{"Initial Integration Test - Functional"}	ASSY	\N	na	then	\N	\N	\N	nmfnmdf	\N	\N	\N		\N	\N	\N	{}	\N	2025-09-23 15:13:09.840356	1005	2025-10-15 16:11:13.15688	1004	\N	assigned	\N	Rejected by QA Head - needs revision	\N
18	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-11-11	manual02/test	manual01	fghj	{1,10,2,3,4,5,6,7,8,9}	10	hj	ty	NA	{"CoTS Screening","High Temperature Storage","",""}	PARTS	nb	bnm	bnm		2025-11-11				\N	\N		\N	\N	\N	{}		2025-11-11 10:25:27.529371	1616	2025-11-13 16:19:31.110956	1004	dfghj	completed_with_observations	\N	remarks	\N
20	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-11-18	testtt	Admin LRU	J	{3}	1	h	uu	NA	{Manufacturing,"","",""}	STAGE	l		p		2025-11-18				\N	\N		\N	\N	\N	{}		2025-11-18 11:32:48.430872	1003	\N	\N		not_assigned	\N	\N	\N
14	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-10-24	vbnj	testing orm -2	78	{2}	1	bnm	bn	NA	{QT,"EMI / EMC","Radiated Emission Test",""}	PARTS	bnm,	kjl	nm,		2025-10-24				\N	\N		\N	\N	\N	{}		2025-10-24 14:47:40.518204	1005	2025-10-24 14:48:41.171664	1004	ghjkl	rejected	\N	\N	\N
3	Mahadev M	QA Head			\N	memo3/casdic	lru	asqw12-	{}	0	sdsd	\N	\N	{"System Performance Test - Acceptance"}	PARTS	\N	na	last	\N	\N	\N	facility	\N	2025-09-24 00:55:00	2025-09-24 00:40:00	ok	2025-09-25 01:00:00	2025-09-24 12:55:00	2025-09-24 00:55:00	{}	\N	2025-09-23 14:53:58.692073	1003	2025-10-10 09:14:10.311439	1004	\N	assigned	\N	\N	\N
5	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-09-25	casdic/	lru	tyyu67	{3,4}	2	someone	na	\N	{"Initial Integration Test - Functional"}	PARTS	current	na	past	techno	2025-09-25	name	something	0.30	2025-09-25 00:55:00	2025-09-26 00:55:00	ok	2025-09-12 11:50:00	2025-09-26 11:50:00	2025-09-26 11:45:00	{a,b}	text	2025-09-25 15:51:23.309144	1005	2025-10-10 09:14:57.470336	1004	indrajeet	assigned	\N	completed with obs	\N
15	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-10-27	dharsh001	dharsh 1	hjkl	{1,10,2,3}	4	bhjkl	gfhj	NA	{Manufacturing,"Raw Material Inspection","Tensile Strength",""}	PARTS	ghj	bnm,	jnk		2025-10-27				\N	\N		\N	\N	\N	{}		2025-10-27 11:08:49.94629	1005	2025-10-27 11:09:50.932804	1004	gfhj	assigned	\N	\N	\N
16	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-11-01	thanish	thanish1	part112	{2,3}	2	tt	98	NA	{"CoTS Screening","Machined Part Inspection","Dimensional Check",""}	FINAL	current	mm	past		2025-11-01				\N	\N		\N	\N	\N	{}		2025-11-01 09:45:17.077145	1005	2025-11-01 09:46:27.285436	1004	thanishka	assigned	\N	\N	\N
7	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	sumedha/ttaa	2025-09-26	casdic/sumedha/memo8	Flight Computer	part55	{FC-10001,FC-10002}	2	avanthika	na	NA	{"Navigation Accuracy Test - Acceptance"}	INSTALL	current1	na	current2	vista	2025-09-26	vista	facility	0.55	2025-09-26 00:50:00	2025-09-27 00:55:00	ok	2025-09-29 00:50:00	2025-09-27 11:40:00	2025-09-25 08:55:00	{d,e}	sample to check memo status	2025-09-26 10:38:59.119079	1005	2025-09-26 10:40:27.094477	1004	thanishka	rejected	\N	\N	\N
9	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-10-06		Autopilot System	1	{AP-20001}	1	hg	2	NA	{"System Performance Test - Acceptance"}	PARTS	kj	tfrgh	kkj 		2025-10-06				\N	\N		\N	\N	\N	{b,c}	kjl	2025-10-06 15:41:54.549678	1005	2025-10-09 14:58:44.98108	1004		assigned	\N	\N	\N
17	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-11-11	manual/testing/05	manual02	56	{3,2,4}	3	gfhj	ty	NA	{QT,"Endurance Vibration Test","INSITU Functional Check","Y Axis"}	ASSY	dfghj	gfhj	gfhj		2025-11-11				\N	\N		\N	\N	\N	{}		2025-11-11 10:15:54.956956	1616	2025-11-11 10:21:30.70305	1004	dfghjkl;	assigned	\N	\N	\N
13	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-10-10	hjk	Admin LRU	hjk	{2,10,4,8}	4	j	m,	NA	{"Initial Integration Test - Functional"}	ASSY	hj	hgj	nm		2025-10-10				\N	\N		\N	\N	\N	{b}		2025-10-10 16:47:19.486692	1003	2025-10-10 16:54:41.666101	1004	jk	completed_with_observations	\N	cgvhbjk	\N
6	MED, CASDIC (DARE), Bangalore	DGAQA cell,	ORDAQA(ADE), Bangalore	CASDIC/QA/2025	2025-09-25	casdic/sumedha/memo123	sample lru	try56	{5,4,3,2,1,6}	6	mahaa	NA	nothing	{"System Performance Test - Acceptance"}	ASSY	current	na	past	bglr	2025-09-25	somebody	db c	0.45	2025-09-26 00:55:00	2025-10-04 00:50:00	jf	2025-09-18 03:05:00	2025-09-26 10:50:00	2025-09-24 10:45:00	{a,b,c,d,e,f}	sample text	2025-09-25 16:03:00.479639	1003	2025-10-10 09:13:25.083372	1004	mohana	successfully_completed	\N	completed	/api/users/signature/f9cb4e70-60b3-4c32-ba13-830233a0a648.png
\.


--
-- Data for Name: news_updates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news_updates (id, news_text, created_at, updated_at, hidden) FROM stdin;
2	news 2	2025-09-10 15:40:38.576691	2025-09-11 15:40:38.576691	t
6	its friday	2025-09-19 11:55:35.57705	2025-09-24 12:38:10.52134	t
9	Simple test news	2025-10-10 04:50:52.391032	2025-10-10 04:56:25.359184	t
8	Test news item from API	2025-10-10 04:49:51.402901	2025-10-10 04:56:30.239147	t
7	Test news item from API	2025-10-10 04:49:49.526176	2025-10-10 04:56:35.070739	t
14	haloooo	2025-10-15 15:31:05.505158	2025-10-15 15:31:05.505158	t
13	news	2025-10-13 04:15:20.250076	2025-10-13 04:15:20.250087	t
11	Test timestamp fix	2025-10-10 10:28:20.854306	2025-10-10 10:28:20.854311	t
12	Test corrected timestamp	2025-10-10 04:59:07.509639	2025-10-10 04:59:07.509653	t
10	news	2025-10-10 04:56:41.306466	2025-10-10 04:56:41.306476	t
5	holiday	2025-09-11 17:34:34.825605	2025-09-15 10:47:32.105703	t
4	its raining	2025-09-11 17:34:34.825605	2025-09-11 18:20:32.29114	t
17	thanishka	2025-11-10 11:29:09.117422	2025-11-10 11:29:09.117422	f
19	news	2025-11-13 16:05:21.112068	2025-11-13 16:05:21.112068	f
20	news from desktop	2025-11-13 16:06:00.470375	2025-11-13 16:06:00.470375	f
\.


--
-- Data for Name: plan_doc_assignment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plan_doc_assignment (assignment_id, document_id, user_id, assigned_at) FROM stdin;
6	29	1001	2025-09-11 11:09:18.104861
5	26	1008	2025-09-24 11:53:06.623976
7	30	1008	2025-09-24 11:53:06.623976
9	35	1008	2025-09-29 14:33:47.842884
10	36	1008	2025-09-29 15:42:40.479508
11	37	1008	2025-09-29 16:50:54.102068
14	40	1111	2025-10-13 09:49:50.822192
15	41	1111	2025-10-13 09:53:10.25098
16	42	1001	2025-10-13 10:26:03.309185
17	43	1111	2025-10-22 12:25:39.666718
18	44	1212	2025-10-27 11:01:52.397742
19	45	1212	2025-10-27 11:05:41.35652
20	46	1212	2025-10-27 16:50:37.486908
21	48	1212	2025-10-28 14:13:14.940005
22	47	1008	2025-10-28 14:19:28.240115
23	49	1212	2025-10-28 14:36:44.397492
24	50	1212	2025-10-28 15:23:10.579664
25	51	1212	2025-11-10 14:07:00.777238
26	52	1212	2025-11-10 14:11:03.52994
27	53	1212	2025-11-18 12:23:34.773997
12	38	1212	2025-11-25 16:01:00.687995
13	39	1212	2025-11-25 16:01:00.687995
28	59	1001	2025-11-25 16:04:57.415765
\.


--
-- Data for Name: plan_documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plan_documents (document_id, lru_id, document_number, version, revision, doc_ver, uploaded_by, upload_date, file_path, status, is_active, original_filename, file_size, file_type, is_approved, approved_by, approved_at, document_type) FROM stdin;
27	1	DOC-001	v1.0	A	v1	1001	2025-09-09 11:42:50.114909	plan_doc_uploads\\e925679a-bc2f-49ee-b99d-624ec44090bb.pdf	assigned	f	Phase document - AVIATRAX.pdf	132503	\N	f	\N	\N	\N
28	1	DOC-005	v1.0	A	1	1005	2025-09-10 10:51:15.031091	plan_doc_uploads\\97e38f6d-5f06-4f93-95ab-cd890d967cae.pdf	assigned	f	Trello-like_Sprint_Management_Platform[1].pdf	146623	\N	f	\N	\N	\N
26	1	DOC-001	v1.0	A	v1	1001	2025-09-09 11:37:39.69853	plan_doc_uploads\\26cbb09a-f190-4127-bea2-d69a69124d4b.pdf	assigned	t	IQA_Observation_Report_Unknown LRU_2025-01-15 (5).pdf	8164	\N	f	\N	\N	\N
30	1	DOC-001	v1.0	B	1	1005	2025-09-11 12:32:01.117719	plan_doc_uploads\\729abc37-37ab-498e-9930-c0245eb95789.pdf	assigned	t	QA_Head_Reports_Summary_26-08-2025 (3).pdf	10272	\N	f	\N	\N	\N
33	1	DOC-11	v1.2	C	1	1005	2025-09-18 10:47:33.237713	plan_doc_uploads\\753994fd-ecab-42e0-89d8-d03c11345d86.pdf	assigned	t	MODULE 1 - QA AUTOMATION v1.pdf	212990	\N	f	\N	\N	\N
35	6	doc055	v1.1		A	1003	2025-09-29 14:32:44.119635	plan_doc_uploads\\43c000c6-c7ec-4e63-b6d1-9d573df473a3.pdf	assigned	t	IQA_Observation_Report_Unknown LRU_2025-01-15 (6).pdf	8164	\N	f	\N	\N	\N
36	6	doc56	v1.2		B	1003	2025-09-29 15:42:40.447903	plan_doc_uploads\\706f79f9-21cc-45b0-b83e-0927de8a1e32.pdf	assigned	t	Coverage report.pdf	334567	\N	f	\N	\N	\N
37	6	doc057	v1.3		C	1003	2025-09-29 16:50:54.066353	plan_doc_uploads\\67f3c018-e0d0-4aca-94be-04a6268d284e.pdf	assigned	t	IQA_Observation_Report_Unknown LRU_2025-01-15 (6).pdf	8164	\N	f	\N	\N	\N
29	3	DOC-002	v1.0	A	1	1003	2025-09-10 16:41:57.293195	plan_doc_uploads\\2193f94f-30e3-48e4-9022-11ea87a97dd8.pdf	assigned	t	MODULE 1 - QA AUTOMATION.pdf	495952	\N	f	\N	\N	\N
31	2	DOC-11	v1.1	B	1	1003	2025-09-12 14:57:51.580954	plan_doc_uploads\\9ee1c808-280d-46f3-8fe7-0dcab153c3d7.pdf	not assigned	t	Sudhiksha_M_K.pdf	119320	\N	f	\N	\N	\N
32	4	doc12	v1.6	F	1	1003	2025-09-12 15:08:12.308097	plan_doc_uploads\\ae9d6d07-59cc-472f-ac6d-1ffe8745cb76.pdf	not assigned	t	3df5a32a-893a-4e56-bc20-9536f32d7863.pdf	27880	\N	f	\N	\N	\N
34	5	doc-015	v1.5	C	A	1003	2025-09-22 13:13:27.092411	plan_doc_uploads\\9917b33e-afdb-4c74-8e2d-77b1dd176741.pdf	not assigned	t	Castic memo.pdf	407241	\N	f	\N	\N	\N
59	55	DOC1010	V1.0		A	1003	2025-11-25 16:04:38.766941	plan_doc_uploads\\fbf11ad6-5e81-49bf-8b9e-34a32963d28c.docx	assigned	t	MODULE 1 - QA AUTOMATION (2).docx	4802500	\N	f	\N	\N	1
57	25	DOC554	V1.2		A	1003	2025-11-25 15:56:24.003572	plan_doc_uploads\\b10c749d-2bfc-431b-ae0d-c574f3b8d89c.pdf	not assigned	t	IQA_Observation_Report_dharsh 2_2025-11-18 (1).pdf	4406693	\N	f	\N	\N	1
48	46	doc54	v1.0		A	1005	2025-10-28 12:51:13.625256	plan_doc_uploads\\b11ded3c-4c97-4ae0-82b5-3766f09a7bac.pdf	assigned	t	contents.pdf	85999	\N	f	\N	\N	\N
40	40	doc55	v1.0		A	1005	2025-10-13 09:48:05.241305	plan_doc_uploads\\8692c214-54fd-4c1d-94df-a6ad951d78d4.docx	assigned	t	Presentation II feedback sem 7 internship template.docx	15341	\N	f	\N	\N	\N
41	40	doc55	v1.1		B	1005	2025-10-13 09:53:10.242634	plan_doc_uploads\\52227c1b-579b-4af3-b669-ac3a441e8b6d.docx	assigned	t	Presentation II feedback sem 7 internship template.docx	15341	\N	f	\N	\N	\N
42	41	doc56	v1.0		A	1005	2025-10-13 10:25:28.074539	plan_doc_uploads\\0300f8b5-5b29-446e-9b75-3deb11d369ea.pdf	assigned	t	IQA_Observation_Report_Unknown LRU_2025-01-15 (6).pdf	8164	\N	f	\N	\N	\N
43	40	doc556	v1.0		C	1005	2025-10-22 12:25:39.597262	plan_doc_uploads\\dcdfd350-d358-4c10-9d46-f2ae845ab75b.pdf	assigned	t	Tech Support Requests Report.pdf	108134	\N	f	\N	\N	\N
44	42	doc5500	v1.0		A	1005	2025-10-27 11:00:53.469305	plan_doc_uploads\\c3def326-2b74-4f6e-b9cb-803c9ea52e70.pdf	assigned	t	front pg.pdf	148310	\N	f	\N	\N	\N
47	45	doc-1	v1		A	1005	2025-10-28 12:37:55.573832	plan_doc_uploads\\9b0f1ba9-07b9-4028-9695-1c41cd30c5de.pdf	assigned	t	vitest_report.pdf	1184754	\N	f	\N	\N	\N
45	42	doc5500	v1.1		B	1005	2025-10-27 11:05:41.323957	plan_doc_uploads\\01f92a74-610a-4b01-a8b3-f9782c6e2fa8.pdf	accepted	t	pg number 1.pdf	2136017	\N	f	\N	\N	\N
49	46	doc332	v1.0		B	1005	2025-10-28 14:36:44.371483	plan_doc_uploads\\5682f101-c438-4859-9543-a2d8cf0c026b.pdf	accepted	t	Tech Support Requests Report.pdf	108134	\N	f	\N	\N	\N
51	47	manualdoc	v1.0		A	1616	2025-11-10 14:05:05.769005	plan_doc_uploads\\b649f17c-d30e-442f-aba2-6a36b62d6c23.pdf	assigned	t	Tech Support Requests Report.pdf	134660	\N	f	\N	\N	\N
46	44	doc 11	v1.1		A	1003	2025-10-27 16:49:39.085065	plan_doc_uploads\\cb366ba1-0256-4cda-b9c1-3664b9f13032.pdf	accepted	t	contents.pdf	85999	\N	f	\N	\N	\N
58	27	DOC343	V1.0		A	1003	2025-11-25 15:58:43.121216	plan_doc_uploads\\b173253a-4e20-49a4-9a73-786bf77ff11f.docx	not assigned	t	MODULE 1 - QA AUTOMATION (2).docx	4802500	\N	f	\N	\N	2
52	47	manualdoc	v2.0		B	1616	2025-11-10 14:11:03.416036	plan_doc_uploads\\f5d59013-7837-4b01-8b01-d8f83c0d1bd7.pdf	accepted	t	Tech Support Requests Report.pdf	134660	\N	f	\N	\N	\N
50	43	doc 1111	v1.0		A	1112	2025-10-28 14:39:13.476988	plan_doc_uploads\\c22cb015-6d3a-4911-b7c4-2ded6409dc78.pdf	assigned	t	front pg.pdf	148310	\N	f	\N	\N	\N
53	43	doc1121	v1.2		B	1003	2025-11-18 12:23:34.713544	plan_doc_uploads\\649bc02e-21c2-4cdd-950b-71de3e160d38.pdf	assigned	t	IQA_Observation_Report_dharsh 1_2025-11-18 (3).pdf	4406777	\N	f	\N	\N	\N
54	51	doc4004	v1.0		A	1003	2025-11-20 14:59:59.071101	plan_doc_uploads\\b7ad40b8-3331-41df-a541-b01663476f70.pdf	not assigned	t	IQA_Observation_Report_dharsh 2_2025-11-18 (2).pdf	4406693	\N	f	\N	\N	1
55	50	doc4002	v1.0		A	1003	2025-11-21 10:44:57.500431	plan_doc_uploads\\1fbb037e-2757-46de-aa0b-4bae3b23de57.pdf	not assigned	t	IQA_Observation_Report_dharsh 2_2025-11-18 (2).pdf	4406693	\N	f	\N	\N	1
56	38	doc666	v1.0		A	1003	2025-11-21 11:00:42.737662	C:\\Users\\HP\\OneDrive\\Desktop\\AVIATRAX - desktop\\backend\\dist\\plan_doc_uploads\\2e4027ea-b2df-49a2-a4f3-3ba99ef40bc1.pdf	not assigned	t	IQA_Observation_Report_dharsh 1_2025-01-15 (6).pdf	1307182	\N	f	\N	\N	2
60	56	DOC1001	V1.0		A	1003	2025-11-25 16:13:18.477562	plan_doc_uploads\\cb81959a-0ab4-45a2-a34e-52c7854ff735.pdf	accepted	t	MODULE 1 - QA AUTOMATION (2).pdf	1554648	\N	f	\N	\N	1
38	7	coc55	v1.0		A	1003	2025-10-10 09:37:06.533453	plan_doc_uploads\\aa11f80a-5fb7-47de-9fa9-6eed11a39ac1.pdf	assigned	t	IQA_Observation_Report_Unknown LRU_2025-01-15 (6).pdf	8164	\N	f	\N	\N	\N
39	7	coc55	v1.2		B	1003	2025-10-10 09:42:20.531456	plan_doc_uploads\\75552e94-1b2b-4153-b2b3-502a869f49cd.pdf	assigned	t	QA_Head_Reports_Summary_10-10-2025.pdf	6097	\N	f	\N	\N	\N
61	15	gh	hg.0		A	1003	2025-11-25 20:20:44.795316	6a7cfddb-b10e-4751-82fa-02d49b52819a.pdf	not assigned	t	IQA_Observation_Report_dharsh 2_2025-11-18 (2).pdf	4406693	\N	f	\N	\N	1
62	21	doc-3232	v1.0		A	1003	2025-11-26 10:51:52.467183	84d24c6f-48a8-4660-a1e8-a33f9a06ab69.pdf	not assigned	t	IQA_Observation_Report_dharsh 1_2025-11-18 (2).pdf	4406639	\N	f	\N	\N	2
63	36	doc-001	v1.0		A	1003	2025-11-26 11:52:00.23907	plan_doc_uploads\\7394dad4-b7b9-42dd-ae29-1091242ce6c4.pdf	not assigned	t	Accenture Registration.pdf	142993	\N	f	\N	\N	2
64	23	d-007	v1.0		A	1003	2025-11-26 12:03:49.777895	C:\\Users\\HP\\OneDrive\\Documents\\aviatrax - doc fetch\\AVIATRAX - final\\backend\\dist\\plan_doc_uploads\\9a371997-da6a-4d96-b59e-c5b0f1d29ec2.pdf	not assigned	t	Accenture Registration.pdf	142993	\N	f	\N	\N	1
65	28	doc44	v6.8		A	1003	2025-11-26 12:33:19.978546	bd9e95c2-46b6-4ad3-a7d1-cb7b57e10a8d.pdf	not assigned	t	AVIATRAX_CD_Deployment_Guide.pdf	94062	\N	f	\N	\N	2
\.


--
-- Data for Name: project_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_users (project_user_id, project_id, user_id, assigned_at) FROM stdin;
1	1	1005	2025-09-12 15:49:35.607739
2	55	1005	2025-10-13 09:47:17.105491
3	5500	1005	2025-10-27 10:59:31.5767
4	12344321	1005	2025-10-28 12:17:30.807594
5	111111	1005	2025-10-28 12:31:00.806119
6	5500	1112	2025-10-28 12:32:32.764253
7	111111	1112	2025-10-28 14:18:52.171109
8	100694	1005	2025-11-10 12:23:04.590168
9	100694	1616	2025-11-10 14:03:00.457761
10	3	1112	2025-11-13 16:17:52.126325
11	4004	1112	2025-11-19 15:33:22.610409
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (project_id, project_name, created_by, created_at, project_date, project_director, deputy_project_director, qa_manager, project_director_id, deputy_project_director_id, qa_manager_id) FROM stdin;
2	Navigation Module	1003	2025-08-20 16:09:38.149564	\N	\N	\N	\N	\N	\N	\N
3	project3	1002	2025-09-05 11:30:29.191263	2025-09-06	\N	\N	\N	\N	\N	\N
5	project 5	1002	2025-09-24 11:59:06.48209	2025-09-24	\N	\N	\N	\N	\N	\N
12345	Test Project	1001	2025-09-26 15:34:46.869026	2024-01-01	\N	\N	\N	\N	\N	\N
99999	Test Project	1001	2025-09-26 15:43:00.558097	2024-01-01	\N	\N	\N	\N	\N	\N
100001	Admin Test Project	1003	2025-09-26 15:43:00.629369	2024-01-01	\N	\N	\N	\N	\N	\N
200001	Admin Test Project	1003	2025-09-26 15:44:11.857954	2024-01-01	\N	\N	\N	\N	\N	\N
999999	Test Project	1001	2025-09-26 15:44:59.42699	2024-01-01	\N	\N	\N	\N	\N	\N
300001	Admin Test Project	1003	2025-09-26 15:45:24.327494	2024-01-01	\N	\N	\N	\N	\N	\N
9999999	Test Project	1001	2025-09-26 16:00:01.999662	2024-01-01	\N	\N	\N	\N	\N	\N
3000001	Admin Test Project	1003	2025-09-26 16:00:02.166858	2024-01-01	\N	\N	\N	\N	\N	\N
76513893	Test Project	1001	2025-09-26 16:11:16.614758	2024-01-01	\N	\N	\N	\N	\N	\N
21406228	Admin Test Project	1003	2025-09-26 16:11:16.763137	2024-01-01	\N	\N	\N	\N	\N	\N
21377527	Test Project	1001	2025-09-26 16:11:56.467559	2024-01-01	\N	\N	\N	\N	\N	\N
26244255	Admin Test Project	1003	2025-09-26 16:12:02.400893	2024-01-01	\N	\N	\N	\N	\N	\N
21973383	Admin Test Project	1003	2025-09-26 16:12:12.863081	2024-01-01	\N	\N	\N	\N	\N	\N
28170588	Admin Test Project	1003	2025-09-26 16:12:22.894692	2024-01-01	\N	\N	\N	\N	\N	\N
70646485	Test Project	1001	2025-09-26 16:12:30.57494	2024-01-01	\N	\N	\N	\N	\N	\N
25268707	Admin Test Project	1003	2025-09-26 16:12:30.731442	2024-01-01	\N	\N	\N	\N	\N	\N
67995283	Test Project	1001	2025-09-26 16:12:40.435997	2024-01-01	\N	\N	\N	\N	\N	\N
23290007	Admin Test Project	1003	2025-09-26 16:12:40.562028	2024-01-01	\N	\N	\N	\N	\N	\N
90691014	Test Project	1001	2025-09-26 17:47:21.702261	2024-01-01	\N	\N	\N	\N	\N	\N
23906058	Admin Test Project	1003	2025-09-26 17:47:21.898116	2024-01-01	\N	\N	\N	\N	\N	\N
85546124	Test Project	1001	2025-09-26 17:52:19.335336	2024-01-01	\N	\N	\N	\N	\N	\N
66820093	Test Project	1001	2025-09-26 19:28:47.649889	2024-01-01	\N	\N	\N	\N	\N	\N
25789744	Admin Test Project	1003	2025-09-26 19:28:47.770224	2024-01-01	\N	\N	\N	\N	\N	\N
71332586	Test Project	1001	2025-09-26 19:31:47.343095	2024-01-01	\N	\N	\N	\N	\N	\N
25048373	Test Project	1001	2025-09-26 19:32:03.952164	2024-01-01	\N	\N	\N	\N	\N	\N
28030449	Admin Test Project	1003	2025-09-26 19:32:04.01286	2024-01-01	\N	\N	\N	\N	\N	\N
29600208	Admin Test Project	1003	2025-09-26 19:32:35.159488	2024-01-01	\N	\N	\N	\N	\N	\N
67312557	Test Project	1001	2025-09-26 19:52:10.952905	2024-01-01	\N	\N	\N	\N	\N	\N
28141924	Admin Test Project	1003	2025-09-26 19:52:11.023473	2024-01-01	\N	\N	\N	\N	\N	\N
22199255	Test Project	1001	2025-09-27 11:00:51.166378	2024-01-01	\N	\N	\N	\N	\N	\N
28713804	Admin Test Project	1003	2025-09-27 11:00:51.230514	2024-01-01	\N	\N	\N	\N	\N	\N
64301877	Test Project	1001	2025-09-27 11:16:34.216149	2024-01-01	\N	\N	\N	\N	\N	\N
22434888	Admin Test Project	1003	2025-09-27 11:16:34.276589	2024-01-01	\N	\N	\N	\N	\N	\N
55	testing orm	1011	2025-10-13 04:14:49.46766	2025-10-13	\N	\N	\N	\N	\N	\N
1	Flight Control System	1002	2025-08-20 16:09:38.149564	\N	\N	\N	\N	\N	\N	\N
5500	dharshini	1011	2025-10-27 10:47:56.855262	2025-10-27	\N	\N	\N	\N	\N	\N
121212	demo	1011	2025-10-27 16:32:48.171878	2025-10-10	\N	\N	\N	\N	\N	\N
111111	thanish	1011	2025-10-28 11:36:32.151842	2025-10-28	\N	\N	\N	\N	\N	\N
12344321	pg1	1011	2025-10-28 12:02:00.810309	2025-10-28	\N	\N	\N	\N	\N	\N
100694	manual testing	1002	2025-11-10 11:17:10.151508	2025-11-09	\N	\N	\N	\N	\N	\N
4004	PROJECT_SAMPLE	1002	2025-11-19 10:32:54.812549	2025-11-19	Sudhiksha M K	hamanth	dharshini	\N	\N	\N
4321	project123	1002	2025-11-25 14:59:14.538937	2025-11-19	\N	\N	\N	1001	1001	1011
11	q	1002	2025-11-25 15:02:53.268728	2025-11-25	\N	\N	\N	1011	1011	1011
54	a	1002	2025-11-25 15:15:26.160504	2025-11-12	\N	\N	\N	1011	1011	1011
1010	TESTING_CASDIC	1002	2025-11-25 16:02:57.418185	2025-11-05	admin	admin	admin	\N	\N	\N
\.


--
-- Data for Name: raw_material_inspection_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.raw_material_inspection_report (report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number, start_date, end_date, dated1, dated2, applicability1, compliance1, rem1, upload1, applicability2, compliance2, rem2, upload2, applicability3, compliance3, rem3, upload3, applicability4, compliance4, rem4, upload4, applicability5, compliance5, rem5, upload5, applicability6, compliance6, rem6, upload6, applicability7, compliance7, rem7, upload7, overall_status, quality_rating, recommendations, prepared_by, verified_by, approved_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: report_observations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report_observations (obs_id, report_id, s_no, category, observation) FROM stdin;
\.


--
-- Data for Name: report_templates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.report_templates (template_id, template_name) FROM stdin;
1	conformal coating inspection report
2	cots screening inspection report
3	bare pcb inspection report
4	mechanical inspection report
5	assembled board inspection report
6	raw material inspection report
7	kit of part inspection report
\.


--
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports (report_id, project_id, lru_id, serial_id, inspection_stage, date_of_review, review_venue, reference_document, memo_id, status, created_at, content, template_id, is_completed, completed_at, filled_data) FROM stdin;
3	1	5	6	lru	2025-09-25	techno	\N	5	ASSIGNED	2025-09-29 10:14:31.296869	Report not yet completed	\N	f	\N	\N
18	1	9	1	hj	2025-10-10	QA Lab	\N	13	ASSIGNED	2025-10-10 11:24:41.710821	\N	1	f	\N	\N
20	1	42	282	dharsh 1	\N		\N	15	ASSIGNED	2025-10-27 11:09:50.987725	Report not yet completed	7	f	\N	\N
21	111111	45	301	thanish1	\N		\N	16	ASSIGNED	2025-11-01 09:46:27.346965	Report not yet completed	1	f	\N	\N
9	1	1	1	Autopilot System	\N		\N	9	ASSIGNED	2025-10-09 14:58:45.070144	Report not yet completed	7	f	\N	\N
22	1	48	327	manual02	\N		\N	17	ASSIGNED	2025-11-11 10:21:30.737789	Report not yet completed	1	f	\N	\N
2	1	5	1	lru	\N	\N	\N	4	ASSIGNED	2025-09-29 10:14:31.295174	Report not yet completed	7	f	\N	\N
23	1	47	317	manual01	\N		\N	18	ASSIGNED	2025-11-13 16:19:31.145567	Report not yet completed	3	f	\N	\N
4	1	5	6	sample lru	2025-09-25	bglr	\N	6	SUCCESSFULLY COMPLETED	2025-09-29 10:14:31.298298	Report not yet completed	1	f	\N	\N
\.


--
-- Data for Name: review_comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.review_comments (comment_id, review_id, commented_by, comment_text, classification, justification, status, "timestamp") FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (role_id, role_name) FROM stdin;
1	Admin
2	QA Head
3	QA Reviewer
4	Design Head
5	Designer
\.


--
-- Data for Name: serial_numbers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.serial_numbers (serial_id, lru_id, serial_number, created_at) FROM stdin;
1	1	FC-10001	2025-08-20 16:13:13.512937
2	1	FC-10002	2025-08-20 16:13:13.512937
3	2	AP-20001	2025-08-20 16:13:13.512937
4	3	GPS-30001	2025-08-20 16:13:13.512937
5	4	ND-40001	2025-08-20 16:13:13.512937
6	5	1	2025-09-05 11:30:29.191263
7	5	2	2025-09-05 11:30:29.191263
8	5	3	2025-09-05 11:30:29.191263
9	5	4	2025-09-05 11:30:29.191263
10	5	5	2025-09-05 11:30:29.191263
11	6	1	2025-09-24 11:59:06.48209
12	6	2	2025-09-24 11:59:06.48209
13	6	3	2025-09-24 11:59:06.48209
14	6	4	2025-09-24 11:59:06.48209
15	6	5	2025-09-24 11:59:06.48209
16	6	6	2025-09-24 11:59:06.48209
17	7	1	2025-09-26 15:34:46.869026
18	7	2	2025-09-26 15:34:46.869026
19	7	3	2025-09-26 15:34:46.869026
20	7	4	2025-09-26 15:34:46.869026
21	7	5	2025-09-26 15:34:46.869026
22	8	1	2025-09-26 15:43:00.558097
23	8	2	2025-09-26 15:43:00.558097
24	8	3	2025-09-26 15:43:00.558097
25	8	4	2025-09-26 15:43:00.558097
26	8	5	2025-09-26 15:43:00.558097
27	9	1	2025-09-26 15:43:00.629369
28	9	2	2025-09-26 15:43:00.629369
29	9	3	2025-09-26 15:43:00.629369
30	9	4	2025-09-26 15:43:00.629369
31	9	5	2025-09-26 15:43:00.629369
32	9	6	2025-09-26 15:43:00.629369
33	9	7	2025-09-26 15:43:00.629369
34	9	8	2025-09-26 15:43:00.629369
35	9	9	2025-09-26 15:43:00.629369
36	9	10	2025-09-26 15:43:00.629369
37	10	1	2025-09-26 15:44:11.857954
38	10	2	2025-09-26 15:44:11.857954
39	10	3	2025-09-26 15:44:11.857954
40	10	4	2025-09-26 15:44:11.857954
41	10	5	2025-09-26 15:44:11.857954
42	10	6	2025-09-26 15:44:11.857954
43	10	7	2025-09-26 15:44:11.857954
44	10	8	2025-09-26 15:44:11.857954
45	10	9	2025-09-26 15:44:11.857954
46	10	10	2025-09-26 15:44:11.857954
47	11	1	2025-09-26 15:44:59.42699
48	11	2	2025-09-26 15:44:59.42699
49	11	3	2025-09-26 15:44:59.42699
50	11	4	2025-09-26 15:44:59.42699
51	11	5	2025-09-26 15:44:59.42699
52	12	1	2025-09-26 15:45:24.327494
53	12	2	2025-09-26 15:45:24.327494
54	12	3	2025-09-26 15:45:24.327494
55	12	4	2025-09-26 15:45:24.327494
56	12	5	2025-09-26 15:45:24.327494
57	12	6	2025-09-26 15:45:24.327494
58	12	7	2025-09-26 15:45:24.327494
59	12	8	2025-09-26 15:45:24.327494
60	12	9	2025-09-26 15:45:24.327494
61	12	10	2025-09-26 15:45:24.327494
62	13	1	2025-09-26 16:00:01.999662
63	13	2	2025-09-26 16:00:01.999662
64	13	3	2025-09-26 16:00:01.999662
65	13	4	2025-09-26 16:00:01.999662
66	13	5	2025-09-26 16:00:01.999662
67	14	1	2025-09-26 16:00:02.166858
68	14	2	2025-09-26 16:00:02.166858
69	14	3	2025-09-26 16:00:02.166858
70	14	4	2025-09-26 16:00:02.166858
71	14	5	2025-09-26 16:00:02.166858
72	14	6	2025-09-26 16:00:02.166858
73	14	7	2025-09-26 16:00:02.166858
74	14	8	2025-09-26 16:00:02.166858
75	14	9	2025-09-26 16:00:02.166858
76	14	10	2025-09-26 16:00:02.166858
77	15	1	2025-09-26 16:11:16.614758
78	15	2	2025-09-26 16:11:16.614758
79	15	3	2025-09-26 16:11:16.614758
80	15	4	2025-09-26 16:11:16.614758
81	15	5	2025-09-26 16:11:16.614758
82	16	1	2025-09-26 16:11:16.763137
83	16	2	2025-09-26 16:11:16.763137
84	16	3	2025-09-26 16:11:16.763137
85	16	4	2025-09-26 16:11:16.763137
86	16	5	2025-09-26 16:11:16.763137
87	16	6	2025-09-26 16:11:16.763137
88	16	7	2025-09-26 16:11:16.763137
89	16	8	2025-09-26 16:11:16.763137
90	16	9	2025-09-26 16:11:16.763137
91	16	10	2025-09-26 16:11:16.763137
92	17	1	2025-09-26 16:11:56.467559
93	17	2	2025-09-26 16:11:56.467559
94	17	3	2025-09-26 16:11:56.467559
95	17	4	2025-09-26 16:11:56.467559
96	17	5	2025-09-26 16:11:56.467559
97	18	1	2025-09-26 16:12:02.400893
98	18	2	2025-09-26 16:12:02.400893
99	18	3	2025-09-26 16:12:02.400893
100	18	4	2025-09-26 16:12:02.400893
101	18	5	2025-09-26 16:12:02.400893
102	18	6	2025-09-26 16:12:02.400893
103	18	7	2025-09-26 16:12:02.400893
104	18	8	2025-09-26 16:12:02.400893
105	18	9	2025-09-26 16:12:02.400893
106	18	10	2025-09-26 16:12:02.400893
107	19	1	2025-09-26 16:12:12.863081
108	19	2	2025-09-26 16:12:12.863081
109	19	3	2025-09-26 16:12:12.863081
110	19	4	2025-09-26 16:12:12.863081
111	19	5	2025-09-26 16:12:12.863081
112	19	6	2025-09-26 16:12:12.863081
113	19	7	2025-09-26 16:12:12.863081
114	19	8	2025-09-26 16:12:12.863081
115	19	9	2025-09-26 16:12:12.863081
116	19	10	2025-09-26 16:12:12.863081
117	20	1	2025-09-26 16:12:22.894692
118	20	2	2025-09-26 16:12:22.894692
119	20	3	2025-09-26 16:12:22.894692
120	20	4	2025-09-26 16:12:22.894692
121	20	5	2025-09-26 16:12:22.894692
122	20	6	2025-09-26 16:12:22.894692
123	20	7	2025-09-26 16:12:22.894692
124	20	8	2025-09-26 16:12:22.894692
125	20	9	2025-09-26 16:12:22.894692
126	20	10	2025-09-26 16:12:22.894692
127	21	1	2025-09-26 16:12:30.57494
128	21	2	2025-09-26 16:12:30.57494
129	21	3	2025-09-26 16:12:30.57494
130	21	4	2025-09-26 16:12:30.57494
131	21	5	2025-09-26 16:12:30.57494
132	22	1	2025-09-26 16:12:30.731442
133	22	2	2025-09-26 16:12:30.731442
134	22	3	2025-09-26 16:12:30.731442
135	22	4	2025-09-26 16:12:30.731442
136	22	5	2025-09-26 16:12:30.731442
137	22	6	2025-09-26 16:12:30.731442
138	22	7	2025-09-26 16:12:30.731442
139	22	8	2025-09-26 16:12:30.731442
140	22	9	2025-09-26 16:12:30.731442
141	22	10	2025-09-26 16:12:30.731442
142	23	1	2025-09-26 16:12:40.435997
143	23	2	2025-09-26 16:12:40.435997
144	23	3	2025-09-26 16:12:40.435997
145	23	4	2025-09-26 16:12:40.435997
146	23	5	2025-09-26 16:12:40.435997
147	24	1	2025-09-26 16:12:40.562028
148	24	2	2025-09-26 16:12:40.562028
149	24	3	2025-09-26 16:12:40.562028
150	24	4	2025-09-26 16:12:40.562028
151	24	5	2025-09-26 16:12:40.562028
152	24	6	2025-09-26 16:12:40.562028
153	24	7	2025-09-26 16:12:40.562028
154	24	8	2025-09-26 16:12:40.562028
155	24	9	2025-09-26 16:12:40.562028
156	24	10	2025-09-26 16:12:40.562028
157	25	1	2025-09-26 17:47:21.702261
158	25	2	2025-09-26 17:47:21.702261
159	25	3	2025-09-26 17:47:21.702261
160	25	4	2025-09-26 17:47:21.702261
161	25	5	2025-09-26 17:47:21.702261
162	26	1	2025-09-26 17:47:21.898116
163	26	2	2025-09-26 17:47:21.898116
164	26	3	2025-09-26 17:47:21.898116
165	26	4	2025-09-26 17:47:21.898116
166	26	5	2025-09-26 17:47:21.898116
167	26	6	2025-09-26 17:47:21.898116
168	26	7	2025-09-26 17:47:21.898116
169	26	8	2025-09-26 17:47:21.898116
170	26	9	2025-09-26 17:47:21.898116
171	26	10	2025-09-26 17:47:21.898116
172	27	1	2025-09-26 17:52:19.335336
173	27	2	2025-09-26 17:52:19.335336
174	27	3	2025-09-26 17:52:19.335336
175	27	4	2025-09-26 17:52:19.335336
176	27	5	2025-09-26 17:52:19.335336
177	28	1	2025-09-26 19:28:47.649889
178	28	2	2025-09-26 19:28:47.649889
179	28	3	2025-09-26 19:28:47.649889
180	28	4	2025-09-26 19:28:47.649889
181	28	5	2025-09-26 19:28:47.649889
182	29	1	2025-09-26 19:28:47.770224
183	29	2	2025-09-26 19:28:47.770224
184	29	3	2025-09-26 19:28:47.770224
185	29	4	2025-09-26 19:28:47.770224
186	29	5	2025-09-26 19:28:47.770224
187	29	6	2025-09-26 19:28:47.770224
188	29	7	2025-09-26 19:28:47.770224
189	29	8	2025-09-26 19:28:47.770224
190	29	9	2025-09-26 19:28:47.770224
191	29	10	2025-09-26 19:28:47.770224
192	30	1	2025-09-26 19:31:47.343095
193	30	2	2025-09-26 19:31:47.343095
194	30	3	2025-09-26 19:31:47.343095
195	30	4	2025-09-26 19:31:47.343095
196	30	5	2025-09-26 19:31:47.343095
197	31	1	2025-09-26 19:32:03.952164
198	31	2	2025-09-26 19:32:03.952164
199	31	3	2025-09-26 19:32:03.952164
200	31	4	2025-09-26 19:32:03.952164
201	31	5	2025-09-26 19:32:03.952164
202	32	1	2025-09-26 19:32:04.01286
203	32	2	2025-09-26 19:32:04.01286
204	32	3	2025-09-26 19:32:04.01286
205	32	4	2025-09-26 19:32:04.01286
206	32	5	2025-09-26 19:32:04.01286
207	32	6	2025-09-26 19:32:04.01286
208	32	7	2025-09-26 19:32:04.01286
209	32	8	2025-09-26 19:32:04.01286
210	32	9	2025-09-26 19:32:04.01286
211	32	10	2025-09-26 19:32:04.01286
212	33	1	2025-09-26 19:32:35.159488
213	33	2	2025-09-26 19:32:35.159488
214	33	3	2025-09-26 19:32:35.159488
215	33	4	2025-09-26 19:32:35.159488
216	33	5	2025-09-26 19:32:35.159488
217	33	6	2025-09-26 19:32:35.159488
218	33	7	2025-09-26 19:32:35.159488
219	33	8	2025-09-26 19:32:35.159488
220	33	9	2025-09-26 19:32:35.159488
221	33	10	2025-09-26 19:32:35.159488
222	34	1	2025-09-26 19:52:10.952905
223	34	2	2025-09-26 19:52:10.952905
224	34	3	2025-09-26 19:52:10.952905
225	34	4	2025-09-26 19:52:10.952905
226	34	5	2025-09-26 19:52:10.952905
227	35	1	2025-09-26 19:52:11.023473
228	35	2	2025-09-26 19:52:11.023473
229	35	3	2025-09-26 19:52:11.023473
230	35	4	2025-09-26 19:52:11.023473
231	35	5	2025-09-26 19:52:11.023473
232	35	6	2025-09-26 19:52:11.023473
233	35	7	2025-09-26 19:52:11.023473
234	35	8	2025-09-26 19:52:11.023473
235	35	9	2025-09-26 19:52:11.023473
236	35	10	2025-09-26 19:52:11.023473
237	36	1	2025-09-27 11:00:51.166378
238	36	2	2025-09-27 11:00:51.166378
239	36	3	2025-09-27 11:00:51.166378
240	36	4	2025-09-27 11:00:51.166378
241	36	5	2025-09-27 11:00:51.166378
242	37	1	2025-09-27 11:00:51.230514
243	37	2	2025-09-27 11:00:51.230514
244	37	3	2025-09-27 11:00:51.230514
245	37	4	2025-09-27 11:00:51.230514
246	37	5	2025-09-27 11:00:51.230514
247	37	6	2025-09-27 11:00:51.230514
248	37	7	2025-09-27 11:00:51.230514
249	37	8	2025-09-27 11:00:51.230514
250	37	9	2025-09-27 11:00:51.230514
251	37	10	2025-09-27 11:00:51.230514
252	38	1	2025-09-27 11:16:34.216149
253	38	2	2025-09-27 11:16:34.216149
254	38	3	2025-09-27 11:16:34.216149
255	38	4	2025-09-27 11:16:34.216149
256	38	5	2025-09-27 11:16:34.216149
257	39	1	2025-09-27 11:16:34.276589
258	39	2	2025-09-27 11:16:34.276589
259	39	3	2025-09-27 11:16:34.276589
260	39	4	2025-09-27 11:16:34.276589
261	39	5	2025-09-27 11:16:34.276589
262	39	6	2025-09-27 11:16:34.276589
263	39	7	2025-09-27 11:16:34.276589
264	39	8	2025-09-27 11:16:34.276589
265	39	9	2025-09-27 11:16:34.276589
266	39	10	2025-09-27 11:16:34.276589
267	40	1	2025-10-13 04:14:49.486996
268	40	2	2025-10-13 04:14:49.487003
269	40	3	2025-10-13 04:14:49.487006
270	40	4	2025-10-13 04:14:49.487009
271	40	5	2025-10-13 04:14:49.487011
272	40	6	2025-10-13 04:14:49.487013
273	40	7	2025-10-13 04:14:49.487016
274	40	8	2025-10-13 04:14:49.487018
275	40	9	2025-10-13 04:14:49.48702
276	41	1	2025-10-13 04:14:49.501131
277	41	2	2025-10-13 04:14:49.501138
278	41	3	2025-10-13 04:14:49.501141
279	41	4	2025-10-13 04:14:49.501143
280	41	5	2025-10-13 04:14:49.501145
281	41	6	2025-10-13 04:14:49.501147
282	42	1	2025-10-27 10:47:56.855262
283	42	2	2025-10-27 10:47:56.855262
284	42	3	2025-10-27 10:47:56.855262
285	42	4	2025-10-27 10:47:56.855262
286	42	5	2025-10-27 10:47:56.855262
287	42	6	2025-10-27 10:47:56.855262
288	42	7	2025-10-27 10:47:56.855262
289	42	8	2025-10-27 10:47:56.855262
290	42	9	2025-10-27 10:47:56.855262
291	42	10	2025-10-27 10:47:56.855262
292	43	1	2025-10-27 10:47:56.855262
293	43	2	2025-10-27 10:47:56.855262
294	43	3	2025-10-27 10:47:56.855262
295	43	4	2025-10-27 10:47:56.855262
296	43	5	2025-10-27 10:47:56.855262
297	44	1	2025-10-27 16:32:48.171878
298	44	2	2025-10-27 16:32:48.171878
299	44	3	2025-10-27 16:32:48.171878
300	44	4	2025-10-27 16:32:48.171878
301	45	1	2025-10-28 11:36:32.151842
302	45	2	2025-10-28 11:36:32.151842
303	45	3	2025-10-28 11:36:32.151842
304	45	4	2025-10-28 11:36:32.151842
305	45	5	2025-10-28 11:36:32.151842
306	45	6	2025-10-28 11:36:32.151842
307	45	7	2025-10-28 11:36:32.151842
308	45	8	2025-10-28 11:36:32.151842
309	46	1	2025-10-28 12:02:00.810309
310	46	2	2025-10-28 12:02:00.810309
311	46	3	2025-10-28 12:02:00.810309
312	46	4	2025-10-28 12:02:00.810309
313	46	5	2025-10-28 12:02:00.810309
314	46	6	2025-10-28 12:02:00.810309
315	46	7	2025-10-28 12:02:00.810309
316	46	8	2025-10-28 12:02:00.810309
317	47	1	2025-11-10 11:17:10.151508
318	47	2	2025-11-10 11:17:10.151508
319	47	3	2025-11-10 11:17:10.151508
320	47	4	2025-11-10 11:17:10.151508
321	47	5	2025-11-10 11:17:10.151508
322	47	6	2025-11-10 11:17:10.151508
323	47	7	2025-11-10 11:17:10.151508
324	47	8	2025-11-10 11:17:10.151508
325	47	9	2025-11-10 11:17:10.151508
326	47	10	2025-11-10 11:17:10.151508
327	48	1	2025-11-10 11:17:10.151508
328	48	2	2025-11-10 11:17:10.151508
329	48	3	2025-11-10 11:17:10.151508
330	48	4	2025-11-10 11:17:10.151508
331	48	5	2025-11-10 11:17:10.151508
332	49	1	2025-11-19 10:32:54.812549
333	49	2	2025-11-19 10:32:54.812549
334	49	3	2025-11-19 10:32:54.812549
335	49	4	2025-11-19 10:32:54.812549
336	49	5	2025-11-19 10:32:54.812549
337	49	6	2025-11-19 10:32:54.812549
338	49	7	2025-11-19 10:32:54.812549
339	49	8	2025-11-19 10:32:54.812549
340	49	9	2025-11-19 10:32:54.812549
341	50	1	2025-11-19 10:32:54.812549
342	50	2	2025-11-19 10:32:54.812549
343	50	3	2025-11-19 10:32:54.812549
344	50	4	2025-11-19 10:32:54.812549
345	50	5	2025-11-19 10:32:54.812549
346	51	1	2025-11-19 16:01:30.694491
347	51	2	2025-11-19 16:01:30.694491
348	51	3	2025-11-19 16:01:30.694491
349	51	4	2025-11-19 16:01:30.694491
350	51	5	2025-11-19 16:01:30.694491
351	51	6	2025-11-19 16:01:30.694491
352	51	7	2025-11-19 16:01:30.694491
353	51	8	2025-11-19 16:01:30.694491
354	51	9	2025-11-19 16:01:30.694491
355	51	10	2025-11-19 16:01:30.694491
356	51	11	2025-11-19 16:01:30.694491
357	51	12	2025-11-19 16:01:30.694491
358	51	13	2025-11-19 16:01:30.694491
359	51	14	2025-11-19 16:01:30.694491
360	51	15	2025-11-19 16:01:30.694491
361	51	16	2025-11-19 16:01:30.694491
362	51	17	2025-11-19 16:01:30.694491
363	51	18	2025-11-19 16:01:30.694491
364	51	19	2025-11-19 16:01:30.694491
365	51	20	2025-11-19 16:01:30.694491
366	51	21	2025-11-19 16:01:30.694491
367	51	22	2025-11-19 16:01:30.694491
368	51	23	2025-11-19 16:01:30.694491
369	51	24	2025-11-19 16:01:30.694491
370	51	25	2025-11-19 16:01:30.694491
371	51	26	2025-11-19 16:01:30.694491
372	51	27	2025-11-19 16:01:30.694491
373	51	28	2025-11-19 16:01:30.694491
374	51	29	2025-11-19 16:01:30.694491
375	51	30	2025-11-19 16:01:30.694491
376	51	31	2025-11-19 16:01:30.694491
377	51	32	2025-11-19 16:01:30.694491
378	51	33	2025-11-19 16:01:30.694491
379	51	34	2025-11-19 16:01:30.694491
380	51	35	2025-11-19 16:01:30.694491
381	51	36	2025-11-19 16:01:30.694491
382	51	37	2025-11-19 16:01:30.694491
383	52	1	2025-11-25 14:59:14.538937
384	52	2	2025-11-25 14:59:14.538937
385	52	3	2025-11-25 14:59:14.538937
386	52	4	2025-11-25 14:59:14.538937
387	52	5	2025-11-25 14:59:14.538937
388	52	6	2025-11-25 14:59:14.538937
389	52	7	2025-11-25 14:59:14.538937
390	52	8	2025-11-25 14:59:14.538937
391	52	9	2025-11-25 14:59:14.538937
392	52	10	2025-11-25 14:59:14.538937
393	52	11	2025-11-25 14:59:14.538937
394	52	12	2025-11-25 14:59:14.538937
395	52	13	2025-11-25 14:59:14.538937
396	52	14	2025-11-25 14:59:14.538937
397	52	15	2025-11-25 14:59:14.538937
398	52	16	2025-11-25 14:59:14.538937
399	52	17	2025-11-25 14:59:14.538937
400	52	18	2025-11-25 14:59:14.538937
401	52	19	2025-11-25 14:59:14.538937
402	52	20	2025-11-25 14:59:14.538937
403	53	1	2025-11-25 15:02:53.268728
404	54	1	2025-11-25 15:15:26.160504
405	54	2	2025-11-25 15:15:26.160504
406	54	3	2025-11-25 15:15:26.160504
407	54	4	2025-11-25 15:15:26.160504
408	54	5	2025-11-25 15:15:26.160504
409	54	6	2025-11-25 15:15:26.160504
410	55	1	2025-11-25 16:02:57.418185
411	55	2	2025-11-25 16:02:57.418185
412	55	3	2025-11-25 16:02:57.418185
413	55	4	2025-11-25 16:02:57.418185
414	56	1	2025-11-25 16:06:57.419042
415	56	2	2025-11-25 16:06:57.419042
416	56	3	2025-11-25 16:06:57.419042
\.


--
-- Data for Name: shared_memos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shared_memos (share_id, memo_id, shared_by, shared_with, shared_at) FROM stdin;
2	6	1001	1008	2025-09-26 11:48:35.687752
3	4	1008	1001	2025-09-26 11:50:35.713878
4	9	1008	1001	2025-10-13 09:09:59.592029
5	15	1212	1111	2025-10-27 11:11:03.647895
6	17	1212	1111	2025-11-11 10:33:28.925045
\.


--
-- Data for Name: sub_tests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sub_tests (sub_test_id, group_id, sub_test_name, sub_test_description, created_at, created_by, updated_at, updated_by) FROM stdin;
1	1	Raw Material Inspection	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
2	1	Machined Part Inspection	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
3	1	Assembly Inspection	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
4	1	Kit of Part Inspection	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
5	1	Bare PCB Inspection	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
6	1	Assembled PCB Inspection	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
7	1	SRU Level Testing	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
8	1	SRU with Mechanical Assembly	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
9	1	LRU Level Assembly Inspection	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
10	2	Visual Inspection	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
11	2	Functional Check	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
12	2	High Temperature Storage	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
13	2	Thermal Shock	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
14	2	Power Burn-In Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
15	3	Pre-ESS Functional Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
16	3	Power Burn-in / Burn-in Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
17	3	Pre Thermal Vibration Test (RV1)	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
18	3	Thermal Cycling	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
19	3	Post Thermal Vibration Test (RV2)	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
20	3	Final Functional Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
21	4	Pre-QT Functional Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
22	4	Low Pressure (Altitude Test)	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
23	4	High Temperature Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
24	4	Low Temperature Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
25	4	Thermal Shock Test (Temperature Shock)	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
26	4	Endurance Vibration Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
27	4	EMI / EMC	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
28	4	POWER SUPPLY TEST	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
29	4	CATH (Combined Altitude Temperature Humidity Test)	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
30	4	Humidity Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
31	4	Acceleration Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
32	4	Mechanical Shock Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
33	4	Shock Crash Hazard	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
34	4	Transit Drop	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
35	4	Bench Handling	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
36	4	Fluid Contamination Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
37	4	Mould Growth (Fungus Test)	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
38	4	Salt Fog Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
39	4	Rain Drip Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
40	4	Gunfire Vibration	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
41	4	Lightning Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
42	4	Icing / Freezing Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
43	4	Explosive Atmosphere Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
44	4	Acoustic Noise Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
45	4	Post-QT Functional Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
46	5	Pre-SoFT Functional Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
47	5	High Temperature Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
48	5	Low Temperature Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
49	5	Endurance Vibration Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
50	5	Low Pressure (Altitude Test)	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
51	5	EMI / EMC	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
52	5	POWER SUPPLY TEST	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
53	5	CATH (Combined Altitude Temperature Humidity Test)	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
54	5	Acceleration Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
55	5	Shock Crash Hazard	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
56	5	Humidity Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
57	5	Rapid Decomposition Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
58	5	Explosive Atmosphere Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
59	5	Post-SoFT Functional Test	\N	2025-10-24 09:56:01.324888	\N	2025-10-24 09:56:01.324888	\N
\.


--
-- Data for Name: tech_support_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tech_support_requests (id, username, user_id, issue_date, issue_description, status, created_at, updated_at, status_updated_by, status_updated_at) FROM stdin;
1	sudhiksha	1111	2025-10-15	error	pending	2025-10-15 20:40:44.767377	2025-10-15 20:40:44.767377	\N	\N
4	sudhiksha	1002	2025-10-15	cannot login	resolved	2025-10-15 21:12:23.480905	2025-10-15 23:18:39.608778	1011	2025-10-15 23:18:39.608778
2	sudhiksha	1002	2025-10-15	cannot login	resolved	2025-10-15 21:09:45.582573	2025-10-15 23:18:45.868686	1011	2025-10-15 23:18:45.868686
3	test_user	123	2024-01-15	Test issue description	in_progress	2025-10-15 21:12:04.801142	2025-10-16 11:01:37.543282	1011	2025-10-16 11:01:37.543282
5	sudhiksha	1111	2025-10-16	backend	pending	2025-10-16 11:36:38.449108	2025-10-16 11:36:38.449108	\N	\N
6	sudhiksha	1111	2025-10-16	backend	pending	2025-10-16 11:36:39.363567	2025-10-16 11:36:39.363567	\N	\N
7	sudhiksha	1111	2025-10-17	gfhjk	pending	2025-10-16 13:13:53.058261	2025-10-16 13:13:53.058261	\N	\N
8	jose	1111	2025-10-16	testing 	pending	2025-10-16 16:38:33.652638	2025-10-16 16:38:33.652638	\N	\N
9	jose	1111	2025-10-16	testing 	in_progress	2025-10-16 16:39:03.294558	2025-10-16 17:02:32.121352	1011	2025-10-16 17:02:32.121352
10	JOSE	1111	2025-10-21	testing dashboard	in_progress	2025-10-21 10:58:54.261702	2025-10-21 11:04:56.934594	1011	2025-10-21 11:04:56.934594
12	test_user	9999	2025-10-21	Testing duplicate prevention	pending	2025-10-21 11:05:49.043076	2025-10-21 11:05:49.043076	\N	\N
13	jose	1111	2025-10-21	duplicate	resolved	2025-10-21 11:06:41.392165	2025-10-21 11:07:33.648819	1011	2025-10-21 11:07:33.648819
11	JOSE	1111	2025-10-21	testing dashboard	resolved	2025-10-21 10:59:13.142317	2025-10-27 10:51:14.168564	1011	2025-10-27 10:51:14.168564
14	Mohan	1004	2025-10-28	notification	in_progress	2025-10-28 12:06:31.550798	2025-10-28 12:11:01.114724	1002	2025-10-28 12:11:01.114724
15	sudhiksha	1002	2025-11-10	login not working	resolved	2025-11-10 11:42:13.180559	2025-11-13 16:16:00.784868	1515	2025-11-13 16:16:00.784868
16	Sudhiksha M K	1002	2025-11-20	fvnfvnmv	pending	2025-11-20 15:49:47.294624	2025-11-20 15:49:47.294624	\N	\N
17	Sudhiksha M K	1002	2025-12-08	trrhgfj	pending	2025-12-08 08:37:39.014788	2025-12-08 08:37:39.014788	\N	\N
\.


--
-- Data for Name: test_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.test_groups (group_id, group_name, group_description) FROM stdin;
1	Manufacturing	Raw Material, Machined Parts, Assembly & PCB Inspection
2	CoTS Screening	Visual Inspection, Functional Check & Power Burn-In
3	ESS	Environmental Stress Screening & Thermal Cycling
4	SoFT	Safety of Flight Test – Critical Safety Validation
5	QT	Qualification Test – Comprehensive Testing Suite
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_roles (user_role_id, user_id, role_id, assigned_at) FROM stdin;
5	1005	5	2025-08-12 15:28:08.132612
12	1003	4	2025-10-06 15:56:12.921994
14	1007	1	2025-10-06 16:01:39.88887
15	1008	3	2025-10-06 16:02:39.869173
18	1111	3	2025-10-13 04:13:21.959665
21	1112	5	2025-10-15 15:45:16.304002
22	1004	2	2025-10-15 16:09:50.834054
23	1212	3	2025-10-27 10:49:37.533255
25	1011	1	2025-11-10 11:18:39.851971
27	1002	1	2025-11-10 11:39:39.95815
29	1515	1	2025-11-17 10:57:17.690512
31	1001	3	2025-11-19 12:18:13.994924
32	9999	2	2025-11-25 20:22:01.973717
33	1616	5	2025-11-26 08:44:57.078879
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, name, email, password_hash, created_at, updated_at, signature_path, signature_password, deleted, enabled) FROM stdin;
1003	Mahadev M	mahadevmanohar07@gmail.com	a56a3abcf08af55024f6127488c0722b7eb4f4617352971f72bf1bdbbced0c70	2025-08-12 15:21:45.679485	2025-10-06 15:56:12.921994	signature_uploads\\cd2573ff-9b40-4a17-bce8-2bc5764152d4.png	ab7217359bc5b91cbdc004dd378440324d7931cae5df31f536a3238ebecfa4c5	f	t
1515	yogesh	yogesh@gmail.com	aac06207cb3796a3129cf81696a7c85e9298df25d0779d0e9af28d4b7be6b64b	2025-11-13 16:07:30.781479	2025-11-17 11:47:59.460148	signature_uploads\\4910b6a9-91da-4de2-9cca-62c3ea88d79e.png	5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8	f	t
1008	saravana	sarva@gmail.com	2d70999ae1805e4bcef9b4ab3a4b827f578c61740f30076fcdc35c7ae7f586b3	2025-09-10 16:39:00.610846	2025-10-06 16:02:39.869173	signature_uploads\\5cd02dac-7eb6-4624-8bfb-9efe11c14380.png	b29f623a3383c2212fce185b5dbe1906c7bf6475e73fb21c188c5e0d2d855e00	f	t
1005	Mahaashri C V	mahaashri@gmail.com	1e4f52a959f00546bff6e2f2adf6bbea729b86ae97c1032aa7330c1148761bc4	2025-08-12 15:21:45.679485	2025-08-12 15:21:45.679485	\N	543dee933267773eb5d12b6a975d998d6b4fe77e1fa04709efe010dceb3dbbc5	f	t
1007	thanishk	thanishk@gmail.com	c1c224b03cd9bc7b6a86d77f5dace40191766c485cd55dc48caf9ac873335d6f	2025-09-05 11:12:00.551723	2025-11-19 11:58:12.957535	signature_uploads\\d68a57d1-fa39-4a2c-9681-c14f7c6acf92.png	0d14b63329ad1fecca741cede81f4774f7ca72753291175d3da9af7f4ae6208c	t	t
1001	Avanthika	avanthikapg22@gmail.com	2d70999ae1805e4bcef9b4ab3a4b827f578c61740f30076fcdc35c7ae7f586b3	2025-08-12 15:21:45.679485	2025-11-19 12:18:13.994924	signature_uploads\\f9cb4e70-60b3-4c32-ba13-830233a0a648.png	6af0e6a6edec1bf378b0f1f9aacc544a8294c929fb4f76d68a4bd88ef186931e	f	t
1111	jose	jose@gmail.com	2d70999ae1805e4bcef9b4ab3a4b827f578c61740f30076fcdc35c7ae7f586b3	2025-10-13 04:13:21.958092	2025-10-13 04:13:21.958097	\N	1ec4ed037766aa181d8840ad04b9fc6e195fd37dedc04c98a5767a67d3758ece	f	t
1112	mohana	mohana@gmail.com	1e4f52a959f00546bff6e2f2adf6bbea729b86ae97c1032aa7330c1148761bc4	2025-10-15 04:10:54.851145	2025-10-15 15:45:16.304002	\N	981914190280dbe8fed260d4bc8ade11e56ccf323737fae9a3998e17489bbea6	f	t
1004	Mohan	mohan@gmail.com	0842f829addd94cce828d6e285134094fe228e6869939044be0fa5521a447cec	2025-08-12 15:21:45.679485	2025-10-15 16:09:50.834054	signature_uploads\\4dc11e9c-9566-4dec-b697-23ceed73fcbc.png	6d040ef7ff7b00b320d5b106470a5bce510f92a4550a43a668c5e20a1fda029a	f	t
1212	dharshini	dharsh@gmail.com	3e85eb75b161e2ff36c72f241e4c112b1846b2b9b4571327cc3a9734b6def803	2025-10-27 10:49:37.533255	2025-10-27 10:49:37.533255	signature_uploads\\102eb453-fbcd-4aea-8e27-bba52bb75bf0.png	f9a76f13274a7c19f92109f03edfd187e1b102011725cc8485a95a30e5f792e2	f	t
9999	Updated Test User	updated@example.com	13d249f2cb4127b40cfa757866850278793f814ded3c587fe5889e889a7a9f6c	2025-10-13 04:12:43.435737	2025-11-25 20:22:01.973717	bcd7f24d-2fdf-432e-9742-96fef7b8cfa4.png	d6406be0fb6ef02f53204e943bb727bc12a42675884054047f722822e0ca05f6	f	t
1011	admin	admin@gmail.com	c1c224b03cd9bc7b6a86d77f5dace40191766c485cd55dc48caf9ac873335d6f	2025-10-06 12:29:22.247312	2025-11-10 11:18:39.851971	signature_uploads\\f0610a41-bd2f-41fa-8fb9-0991b20d6a3c.png	1a2fc26dc7ea5a2a4748b7cb2b1ef193d96ab2c99f93092f69e63075b28d1278	f	t
1002	Sudhiksha M K	sudhikshamk06@gmail.com	5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8	2025-08-12 15:21:45.679485	2025-11-10 11:39:39.95815	signature_uploads\\d9ed38c8-17ad-4fed-85a2-71ecc9b7a494.png	de85035bd33a49d9e54a5544536536e2115cc341be17865d0321910a9ca79b22	f	t
1616	pradeepa	pradeepa@gmail.com	1e4f52a959f00546bff6e2f2adf6bbea729b86ae97c1032aa7330c1148761bc4	2025-11-10 11:20:10.158177	2025-11-26 08:44:57.078879	dd345566-b8cb-4baf-a117-f019e8fbfb45.png	26ff16c184c904cbcfbd3c277e37624c6f2d93851ce2ae6dca4229957ca57a2b	f	t
\.


--
-- Name: activity_logs_activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.activity_logs_activity_id_seq', 309, true);


--
-- Name: assembled_board_inspection_report_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assembled_board_inspection_report_report_id_seq', 1, false);


--
-- Name: bare_pcb_inspection_report_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bare_pcb_inspection_report_report_id_seq', 5, true);


--
-- Name: bulletins_bulletin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bulletins_bulletin_id_seq', 1, false);


--
-- Name: conformal_coating_inspection_report_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.conformal_coating_inspection_report_report_id_seq', 19, true);


--
-- Name: cot_screening_inspection_report_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cot_screening_inspection_report_report_id_seq', 1, false);


--
-- Name: document_annotations_annotation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.document_annotations_annotation_id_seq', 40, true);


--
-- Name: document_comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.document_comments_comment_id_seq', 43, true);


--
-- Name: document_reviews_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.document_reviews_review_id_seq', 8, true);


--
-- Name: document_types_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.document_types_type_id_seq', 2, true);


--
-- Name: document_version_version_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.document_version_version_id_seq', 11, true);


--
-- Name: iqa_observation_reports_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.iqa_observation_reports_report_id_seq', 3, true);


--
-- Name: kit_of_parts_inspection_report_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kit_of_parts_inspection_report_report_id_seq', 12, true);


--
-- Name: login_logs_serial_num_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.login_logs_serial_num_seq', 628, true);


--
-- Name: lrus_lru_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.lrus_lru_id_seq', 56, true);


--
-- Name: mechanical_inspection_report_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mechanical_inspection_report_report_id_seq', 1, false);


--
-- Name: memo_approval_approval_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.memo_approval_approval_id_seq', 35, true);


--
-- Name: memo_references_ref_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.memo_references_ref_id_seq', 5, true);


--
-- Name: memos_memo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.memos_memo_id_seq', 20, true);


--
-- Name: news_updates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.news_updates_id_seq', 20, true);


--
-- Name: plan_doc_assignment_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plan_doc_assignment_assignment_id_seq', 28, true);


--
-- Name: plan_documents_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plan_documents_document_id_seq', 65, true);


--
-- Name: project_users_project_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_users_project_user_id_seq', 11, true);


--
-- Name: projects_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_project_id_seq', 5, true);


--
-- Name: raw_material_inspection_report_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.raw_material_inspection_report_report_id_seq', 1, false);


--
-- Name: report_observations_obs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_observations_obs_id_seq', 1, false);


--
-- Name: report_templates_template_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_templates_template_id_seq', 7, true);


--
-- Name: reports_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_report_id_seq', 23, true);


--
-- Name: review_comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.review_comments_comment_id_seq', 8, true);


--
-- Name: roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_role_id_seq', 5, true);


--
-- Name: serial_numbers_serial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.serial_numbers_serial_id_seq', 416, true);


--
-- Name: shared_memos_share_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shared_memos_share_id_seq', 6, true);


--
-- Name: sub_tests_sub_test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sub_tests_sub_test_id_seq', 1, false);


--
-- Name: tech_support_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tech_support_requests_id_seq', 17, true);


--
-- Name: test_groups_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.test_groups_group_id_seq', 1, false);


--
-- Name: user_roles_user_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_roles_user_role_id_seq', 33, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: activity_logs activity_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_pkey PRIMARY KEY (activity_id);


--
-- Name: assembled_board_inspection_report assembled_board_inspection_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assembled_board_inspection_report
    ADD CONSTRAINT assembled_board_inspection_report_pkey PRIMARY KEY (report_id);


--
-- Name: bare_pcb_inspection_report bare_pcb_inspection_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bare_pcb_inspection_report
    ADD CONSTRAINT bare_pcb_inspection_report_pkey PRIMARY KEY (report_id);


--
-- Name: bulletins bulletins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bulletins
    ADD CONSTRAINT bulletins_pkey PRIMARY KEY (bulletin_id);


--
-- Name: bulletins bulletins_sub_test_id_bulletin_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bulletins
    ADD CONSTRAINT bulletins_sub_test_id_bulletin_name_key UNIQUE (sub_test_id, bulletin_name);


--
-- Name: conformal_coating_inspection_report conformal_coating_inspection_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conformal_coating_inspection_report
    ADD CONSTRAINT conformal_coating_inspection_report_pkey PRIMARY KEY (report_id);


--
-- Name: cot_screening_inspection_report cot_screening_inspection_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cot_screening_inspection_report
    ADD CONSTRAINT cot_screening_inspection_report_pkey PRIMARY KEY (report_id);


--
-- Name: document_annotations document_annotations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_annotations
    ADD CONSTRAINT document_annotations_pkey PRIMARY KEY (annotation_id);


--
-- Name: document_comments document_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_comments
    ADD CONSTRAINT document_comments_pkey PRIMARY KEY (comment_id);


--
-- Name: document_reviews document_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_reviews
    ADD CONSTRAINT document_reviews_pkey PRIMARY KEY (review_id);


--
-- Name: document_types document_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_types
    ADD CONSTRAINT document_types_pkey PRIMARY KEY (type_id);


--
-- Name: document_version document_version_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_version
    ADD CONSTRAINT document_version_pkey PRIMARY KEY (version_id);


--
-- Name: iqa_observation_reports iqa_observation_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iqa_observation_reports
    ADD CONSTRAINT iqa_observation_reports_pkey PRIMARY KEY (report_id);


--
-- Name: kit_of_parts_inspection_report kit_of_parts_inspection_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kit_of_parts_inspection_report
    ADD CONSTRAINT kit_of_parts_inspection_report_pkey PRIMARY KEY (report_id);


--
-- Name: login_logs login_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login_logs
    ADD CONSTRAINT login_logs_pkey PRIMARY KEY (serial_num);


--
-- Name: lrus lrus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lrus
    ADD CONSTRAINT lrus_pkey PRIMARY KEY (lru_id);


--
-- Name: mechanical_inspection_report mechanical_inspection_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mechanical_inspection_report
    ADD CONSTRAINT mechanical_inspection_report_pkey PRIMARY KEY (report_id);


--
-- Name: memo_approval memo_approval_memo_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memo_approval
    ADD CONSTRAINT memo_approval_memo_id_key UNIQUE (memo_id);


--
-- Name: memo_approval memo_approval_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memo_approval
    ADD CONSTRAINT memo_approval_pkey PRIMARY KEY (approval_id);


--
-- Name: memo_references memo_references_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memo_references
    ADD CONSTRAINT memo_references_pkey PRIMARY KEY (ref_id);


--
-- Name: memos memos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memos
    ADD CONSTRAINT memos_pkey PRIMARY KEY (memo_id);


--
-- Name: news_updates news_updates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_updates
    ADD CONSTRAINT news_updates_pkey PRIMARY KEY (id);


--
-- Name: plan_doc_assignment plan_doc_assignment_document_id_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_doc_assignment
    ADD CONSTRAINT plan_doc_assignment_document_id_user_id_key UNIQUE (document_id, user_id);


--
-- Name: plan_doc_assignment plan_doc_assignment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_doc_assignment
    ADD CONSTRAINT plan_doc_assignment_pkey PRIMARY KEY (assignment_id);


--
-- Name: plan_documents plan_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_documents
    ADD CONSTRAINT plan_documents_pkey PRIMARY KEY (document_id);


--
-- Name: project_users project_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_users
    ADD CONSTRAINT project_users_pkey PRIMARY KEY (project_user_id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (project_id);


--
-- Name: raw_material_inspection_report raw_material_inspection_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_material_inspection_report
    ADD CONSTRAINT raw_material_inspection_report_pkey PRIMARY KEY (report_id);


--
-- Name: report_observations report_observations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_observations
    ADD CONSTRAINT report_observations_pkey PRIMARY KEY (obs_id);


--
-- Name: report_templates report_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_templates
    ADD CONSTRAINT report_templates_pkey PRIMARY KEY (template_id);


--
-- Name: reports reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (report_id);


--
-- Name: review_comments review_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_comments
    ADD CONSTRAINT review_comments_pkey PRIMARY KEY (comment_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- Name: roles roles_role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_role_name_key UNIQUE (role_name);


--
-- Name: serial_numbers serial_numbers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.serial_numbers
    ADD CONSTRAINT serial_numbers_pkey PRIMARY KEY (serial_id);


--
-- Name: shared_memos shared_memos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_memos
    ADD CONSTRAINT shared_memos_pkey PRIMARY KEY (share_id);


--
-- Name: sub_tests sub_tests_group_id_sub_test_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_tests
    ADD CONSTRAINT sub_tests_group_id_sub_test_name_key UNIQUE (group_id, sub_test_name);


--
-- Name: sub_tests sub_tests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_tests
    ADD CONSTRAINT sub_tests_pkey PRIMARY KEY (sub_test_id);


--
-- Name: tech_support_requests tech_support_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tech_support_requests
    ADD CONSTRAINT tech_support_requests_pkey PRIMARY KEY (id);


--
-- Name: test_groups test_groups_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_groups
    ADD CONSTRAINT test_groups_group_name_key UNIQUE (group_name);


--
-- Name: test_groups test_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_groups
    ADD CONSTRAINT test_groups_pkey PRIMARY KEY (group_id);


--
-- Name: shared_memos unique_memo_sharing; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_memos
    ADD CONSTRAINT unique_memo_sharing UNIQUE (memo_id, shared_by, shared_with);


--
-- Name: project_users unique_project_user; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_users
    ADD CONSTRAINT unique_project_user UNIQUE (project_id, user_id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_role_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: idx_activity_logs_is_read; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_activity_logs_is_read ON public.activity_logs USING btree (is_read);


--
-- Name: idx_activity_logs_notification_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_activity_logs_notification_type ON public.activity_logs USING btree (notification_type);


--
-- Name: idx_activity_logs_notified_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_activity_logs_notified_user ON public.activity_logs USING btree (notified_user_id);


--
-- Name: idx_activity_logs_performed_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_activity_logs_performed_by ON public.activity_logs USING btree (performed_by);


--
-- Name: idx_activity_logs_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_activity_logs_project_id ON public.activity_logs USING btree (project_id);


--
-- Name: idx_activity_logs_timestamp; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_activity_logs_timestamp ON public.activity_logs USING btree ("timestamp");


--
-- Name: idx_document_annotations_comment_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_document_annotations_comment_id ON public.document_annotations USING btree (comment_id);


--
-- Name: idx_document_annotations_document_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_document_annotations_document_id ON public.document_annotations USING btree (document_id);


--
-- Name: idx_document_comments_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_document_comments_created_at ON public.document_comments USING btree (created_at);


--
-- Name: idx_document_comments_document_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_document_comments_document_id ON public.document_comments USING btree (document_id);


--
-- Name: idx_document_comments_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_document_comments_status ON public.document_comments USING btree (status);


--
-- Name: idx_document_types_deleted; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_document_types_deleted ON public.document_types USING btree (deleted);


--
-- Name: idx_iqa_report_approved_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_iqa_report_approved_by ON public.iqa_observation_reports USING btree (approved_by_user_id);


--
-- Name: idx_iqa_report_created_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_iqa_report_created_by ON public.iqa_observation_reports USING btree (created_by);


--
-- Name: idx_iqa_report_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_iqa_report_date ON public.iqa_observation_reports USING btree (report_date);


--
-- Name: idx_iqa_report_document_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_iqa_report_document_id ON public.iqa_observation_reports USING btree (document_id);


--
-- Name: idx_iqa_report_lru_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_iqa_report_lru_id ON public.iqa_observation_reports USING btree (lru_id);


--
-- Name: idx_iqa_report_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_iqa_report_project_id ON public.iqa_observation_reports USING btree (project_id);


--
-- Name: idx_iqa_report_reviewed_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_iqa_report_reviewed_by ON public.iqa_observation_reports USING btree (reviewed_by_user_id);


--
-- Name: idx_login_logs_activity; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_login_logs_activity ON public.login_logs USING btree (activity_performed);


--
-- Name: idx_login_logs_timestamp; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_login_logs_timestamp ON public.login_logs USING btree ("timestamp");


--
-- Name: idx_login_logs_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_login_logs_user_id ON public.login_logs USING btree (user_id);


--
-- Name: idx_plan_documents_approved_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_plan_documents_approved_at ON public.plan_documents USING btree (approved_at);


--
-- Name: idx_plan_documents_approved_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_plan_documents_approved_by ON public.plan_documents USING btree (approved_by);


--
-- Name: idx_plan_documents_document_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_plan_documents_document_type ON public.plan_documents USING btree (document_type);


--
-- Name: idx_plan_documents_is_approved; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_plan_documents_is_approved ON public.plan_documents USING btree (is_approved);


--
-- Name: idx_reports_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reports_created_at ON public.reports USING btree (created_at);


--
-- Name: idx_reports_filled_data; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reports_filled_data ON public.reports USING gin (filled_data);


--
-- Name: idx_reports_lru_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reports_lru_id ON public.reports USING btree (lru_id);


--
-- Name: idx_reports_memo_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reports_memo_id ON public.reports USING btree (memo_id);


--
-- Name: idx_reports_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reports_project_id ON public.reports USING btree (project_id);


--
-- Name: idx_reports_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reports_status ON public.reports USING btree (status);


--
-- Name: idx_shared_memos_memo_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shared_memos_memo_id ON public.shared_memos USING btree (memo_id);


--
-- Name: idx_shared_memos_shared_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shared_memos_shared_by ON public.shared_memos USING btree (shared_by);


--
-- Name: idx_shared_memos_shared_with; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shared_memos_shared_with ON public.shared_memos USING btree (shared_with);


--
-- Name: idx_tech_support_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tech_support_created_at ON public.tech_support_requests USING btree (created_at);


--
-- Name: idx_tech_support_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tech_support_status ON public.tech_support_requests USING btree (status);


--
-- Name: idx_tech_support_status_updated_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tech_support_status_updated_at ON public.tech_support_requests USING btree (status_updated_at);


--
-- Name: idx_tech_support_status_updated_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tech_support_status_updated_by ON public.tech_support_requests USING btree (status_updated_by);


--
-- Name: idx_tech_support_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tech_support_user_id ON public.tech_support_requests USING btree (user_id);


--
-- Name: idx_users_deleted; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_deleted ON public.users USING btree (deleted);


--
-- Name: idx_users_enabled; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_enabled ON public.users USING btree (enabled);


--
-- Name: assembled_board_inspection_report trg_update_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_updated_at BEFORE UPDATE ON public.assembled_board_inspection_report FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: bare_pcb_inspection_report trg_update_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_updated_at BEFORE UPDATE ON public.bare_pcb_inspection_report FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: cot_screening_inspection_report trg_update_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_updated_at BEFORE UPDATE ON public.cot_screening_inspection_report FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: conformal_coating_inspection_report trg_update_updated_at_conformal_coating; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_updated_at_conformal_coating BEFORE UPDATE ON public.conformal_coating_inspection_report FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: iqa_observation_reports trg_update_updated_at_iqa_report; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_updated_at_iqa_report BEFORE UPDATE ON public.iqa_observation_reports FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: kit_of_parts_inspection_report trg_update_updated_at_kit_of_parts; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_updated_at_kit_of_parts BEFORE UPDATE ON public.kit_of_parts_inspection_report FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: mechanical_inspection_report trg_update_updated_at_mechanical; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_updated_at_mechanical BEFORE UPDATE ON public.mechanical_inspection_report FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: raw_material_inspection_report trg_update_updated_at_raw_material; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_updated_at_raw_material BEFORE UPDATE ON public.raw_material_inspection_report FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: memos trigger_create_report_on_memo_accepted; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_create_report_on_memo_accepted AFTER UPDATE ON public.memos FOR EACH ROW EXECUTE FUNCTION public.create_report_for_accepted_memo();


--
-- Name: TRIGGER trigger_create_report_on_memo_accepted ON memos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TRIGGER trigger_create_report_on_memo_accepted ON public.memos IS 'Triggers report creation when memo is assigned and accepted';


--
-- Name: activity_logs activity_logs_notified_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_notified_user_id_fkey FOREIGN KEY (notified_user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: activity_logs activity_logs_performed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_performed_by_fkey FOREIGN KEY (performed_by) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: activity_logs activity_logs_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id) ON DELETE CASCADE;


--
-- Name: bulletins bulletins_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bulletins
    ADD CONSTRAINT bulletins_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: bulletins bulletins_parent_bulletin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bulletins
    ADD CONSTRAINT bulletins_parent_bulletin_id_fkey FOREIGN KEY (parent_bulletin_id) REFERENCES public.bulletins(bulletin_id) ON DELETE CASCADE;


--
-- Name: bulletins bulletins_sub_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bulletins
    ADD CONSTRAINT bulletins_sub_test_id_fkey FOREIGN KEY (sub_test_id) REFERENCES public.sub_tests(sub_test_id) ON DELETE CASCADE;


--
-- Name: bulletins bulletins_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bulletins
    ADD CONSTRAINT bulletins_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: conformal_coating_inspection_report conformal_coating_inspection_report_original_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conformal_coating_inspection_report
    ADD CONSTRAINT conformal_coating_inspection_report_original_report_id_fkey FOREIGN KEY (original_report_id) REFERENCES public.reports(report_id) ON DELETE CASCADE;


--
-- Name: conformal_coating_inspection_report conformal_coating_inspection_report_report_card_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conformal_coating_inspection_report
    ADD CONSTRAINT conformal_coating_inspection_report_report_card_id_fkey FOREIGN KEY (report_card_id) REFERENCES public.reports(report_id) ON DELETE CASCADE;


--
-- Name: document_reviews document_reviews_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_reviews
    ADD CONSTRAINT document_reviews_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.plan_documents(document_id);


--
-- Name: document_reviews document_reviews_reviewer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_reviews
    ADD CONSTRAINT document_reviews_reviewer_id_fkey FOREIGN KEY (reviewer_id) REFERENCES public.users(user_id);


--
-- Name: document_version document_version_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_version
    ADD CONSTRAINT document_version_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.plan_documents(document_id);


--
-- Name: document_version document_version_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_version
    ADD CONSTRAINT document_version_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.users(user_id);


--
-- Name: document_annotations fk_document_annotations_document_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_annotations
    ADD CONSTRAINT fk_document_annotations_document_id FOREIGN KEY (document_id) REFERENCES public.plan_documents(document_id) ON DELETE CASCADE;


--
-- Name: document_comments fk_document_comments_document_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_comments
    ADD CONSTRAINT fk_document_comments_document_id FOREIGN KEY (document_id) REFERENCES public.plan_documents(document_id) ON DELETE CASCADE;


--
-- Name: plan_documents fk_plan_documents_approved_by; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_documents
    ADD CONSTRAINT fk_plan_documents_approved_by FOREIGN KEY (approved_by) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: tech_support_requests fk_tech_support_status_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tech_support_requests
    ADD CONSTRAINT fk_tech_support_status_updated_by FOREIGN KEY (status_updated_by) REFERENCES public.users(user_id);


--
-- Name: iqa_observation_reports iqa_observation_reports_approved_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iqa_observation_reports
    ADD CONSTRAINT iqa_observation_reports_approved_by_user_id_fkey FOREIGN KEY (approved_by_user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: iqa_observation_reports iqa_observation_reports_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iqa_observation_reports
    ADD CONSTRAINT iqa_observation_reports_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: iqa_observation_reports iqa_observation_reports_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iqa_observation_reports
    ADD CONSTRAINT iqa_observation_reports_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.plan_documents(document_id) ON DELETE SET NULL;


--
-- Name: iqa_observation_reports iqa_observation_reports_lru_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iqa_observation_reports
    ADD CONSTRAINT iqa_observation_reports_lru_id_fkey FOREIGN KEY (lru_id) REFERENCES public.lrus(lru_id) ON DELETE CASCADE;


--
-- Name: iqa_observation_reports iqa_observation_reports_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iqa_observation_reports
    ADD CONSTRAINT iqa_observation_reports_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id) ON DELETE CASCADE;


--
-- Name: iqa_observation_reports iqa_observation_reports_reviewed_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iqa_observation_reports
    ADD CONSTRAINT iqa_observation_reports_reviewed_by_user_id_fkey FOREIGN KEY (reviewed_by_user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: kit_of_parts_inspection_report kit_of_parts_inspection_report_original_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kit_of_parts_inspection_report
    ADD CONSTRAINT kit_of_parts_inspection_report_original_report_id_fkey FOREIGN KEY (original_report_id) REFERENCES public.reports(report_id) ON DELETE CASCADE;


--
-- Name: kit_of_parts_inspection_report kit_of_parts_inspection_report_report_card_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kit_of_parts_inspection_report
    ADD CONSTRAINT kit_of_parts_inspection_report_report_card_id_fkey FOREIGN KEY (report_card_id) REFERENCES public.reports(report_id) ON DELETE CASCADE;


--
-- Name: login_logs login_logs_performed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login_logs
    ADD CONSTRAINT login_logs_performed_by_fkey FOREIGN KEY (performed_by) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: login_logs login_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login_logs
    ADD CONSTRAINT login_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: lrus lrus_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lrus
    ADD CONSTRAINT lrus_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id);


--
-- Name: memo_approval memo_approval_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memo_approval
    ADD CONSTRAINT memo_approval_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(user_id);


--
-- Name: memo_approval memo_approval_memo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memo_approval
    ADD CONSTRAINT memo_approval_memo_id_fkey FOREIGN KEY (memo_id) REFERENCES public.memos(memo_id) ON DELETE CASCADE;


--
-- Name: memo_approval memo_approval_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memo_approval
    ADD CONSTRAINT memo_approval_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: memo_references memo_references_memo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memo_references
    ADD CONSTRAINT memo_references_memo_id_fkey FOREIGN KEY (memo_id) REFERENCES public.memos(memo_id) ON DELETE CASCADE;


--
-- Name: memos memos_accepted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memos
    ADD CONSTRAINT memos_accepted_by_fkey FOREIGN KEY (accepted_by) REFERENCES public.users(user_id);


--
-- Name: memos memos_submitted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memos
    ADD CONSTRAINT memos_submitted_by_fkey FOREIGN KEY (submitted_by) REFERENCES public.users(user_id);


--
-- Name: memos memos_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.memos
    ADD CONSTRAINT memos_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.report_templates(template_id);


--
-- Name: plan_doc_assignment plan_doc_assignment_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_doc_assignment
    ADD CONSTRAINT plan_doc_assignment_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.plan_documents(document_id) ON DELETE CASCADE;


--
-- Name: plan_doc_assignment plan_doc_assignment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_doc_assignment
    ADD CONSTRAINT plan_doc_assignment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: plan_documents plan_documents_document_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_documents
    ADD CONSTRAINT plan_documents_document_type_fkey FOREIGN KEY (document_type) REFERENCES public.document_types(type_id) ON DELETE SET NULL;


--
-- Name: plan_documents plan_documents_lru_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_documents
    ADD CONSTRAINT plan_documents_lru_id_fkey FOREIGN KEY (lru_id) REFERENCES public.lrus(lru_id);


--
-- Name: plan_documents plan_documents_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan_documents
    ADD CONSTRAINT plan_documents_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.users(user_id);


--
-- Name: project_users project_users_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_users
    ADD CONSTRAINT project_users_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id) ON DELETE CASCADE;


--
-- Name: project_users project_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_users
    ADD CONSTRAINT project_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: projects projects_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(user_id);


--
-- Name: projects projects_deputy_project_director_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_deputy_project_director_id_fkey FOREIGN KEY (deputy_project_director_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: projects projects_project_director_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_project_director_id_fkey FOREIGN KEY (project_director_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: projects projects_qa_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_qa_manager_id_fkey FOREIGN KEY (qa_manager_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: report_observations report_observations_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_observations
    ADD CONSTRAINT report_observations_report_id_fkey FOREIGN KEY (report_id) REFERENCES public.reports(report_id) ON DELETE CASCADE;


--
-- Name: reports reports_lru_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_lru_id_fkey FOREIGN KEY (lru_id) REFERENCES public.lrus(lru_id) ON DELETE CASCADE;


--
-- Name: reports reports_memo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_memo_id_fkey FOREIGN KEY (memo_id) REFERENCES public.memos(memo_id) ON DELETE CASCADE;


--
-- Name: reports reports_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id) ON DELETE CASCADE;


--
-- Name: reports reports_reference_document_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_reference_document_fkey FOREIGN KEY (reference_document) REFERENCES public.plan_documents(document_id) ON DELETE SET NULL;


--
-- Name: reports reports_serial_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_serial_id_fkey FOREIGN KEY (serial_id) REFERENCES public.serial_numbers(serial_id) ON DELETE CASCADE;


--
-- Name: review_comments review_comments_commented_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_comments
    ADD CONSTRAINT review_comments_commented_by_fkey FOREIGN KEY (commented_by) REFERENCES public.users(user_id);


--
-- Name: review_comments review_comments_review_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_comments
    ADD CONSTRAINT review_comments_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.document_reviews(review_id);


--
-- Name: serial_numbers serial_numbers_lru_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.serial_numbers
    ADD CONSTRAINT serial_numbers_lru_id_fkey FOREIGN KEY (lru_id) REFERENCES public.lrus(lru_id);


--
-- Name: shared_memos shared_memos_memo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_memos
    ADD CONSTRAINT shared_memos_memo_id_fkey FOREIGN KEY (memo_id) REFERENCES public.memos(memo_id) ON DELETE CASCADE;


--
-- Name: shared_memos shared_memos_shared_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_memos
    ADD CONSTRAINT shared_memos_shared_by_fkey FOREIGN KEY (shared_by) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: shared_memos shared_memos_shared_with_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_memos
    ADD CONSTRAINT shared_memos_shared_with_fkey FOREIGN KEY (shared_with) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: sub_tests sub_tests_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_tests
    ADD CONSTRAINT sub_tests_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: sub_tests sub_tests_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_tests
    ADD CONSTRAINT sub_tests_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.test_groups(group_id) ON DELETE CASCADE;


--
-- Name: sub_tests sub_tests_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_tests
    ADD CONSTRAINT sub_tests_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

