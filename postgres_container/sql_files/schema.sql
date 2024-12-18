PGDMP  5                 
    |            cbmoron_database    17.2 (Debian 17.2-1.pgdg120+1)    17.0 =    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    25425    cbmoron_database    DATABASE     {   CREATE DATABASE cbmoron_database WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
     DROP DATABASE cbmoron_database;
                     root    false            �            1255    25589    check_and_insert_away_team_id()    FUNCTION       CREATE FUNCTION public.check_and_insert_away_team_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM teams WHERE team_id = NEW.away_team_id) THEN
        INSERT INTO teams (team_id) VALUES (NEW.away_team_id);
    END IF;
    RETURN NEW;
END;
$$;
 6   DROP FUNCTION public.check_and_insert_away_team_id();
       public               root    false            �            1255    25591    check_and_insert_home_team_id()    FUNCTION       CREATE FUNCTION public.check_and_insert_home_team_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM teams WHERE team_id = NEW.home_team_id) THEN
        INSERT INTO teams (team_id) VALUES (NEW.home_team_id);
    END IF;
    RETURN NEW;
END;
$$;
 6   DROP FUNCTION public.check_and_insert_home_team_id();
       public               root    false            �            1255    25593    check_and_insert_player_id()    FUNCTION     C  CREATE FUNCTION public.check_and_insert_player_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM players_info WHERE player_id = NEW.player_id) THEN
        INSERT INTO players_info (player_id,player_link) VALUES (NEW.player_id,NEW.player_link);
    END IF;
    RETURN NEW;
END;
$$;
 3   DROP FUNCTION public.check_and_insert_player_id();
       public               root    false            �            1255    25587    check_and_insert_stage_id()    FUNCTION       CREATE FUNCTION public.check_and_insert_stage_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM results WHERE stage_id = NEW.stage_id) THEN
        INSERT INTO stages (stage_id) VALUES (NEW.stage_id);
    END IF;
    RETURN NEW;
END;
$$;
 2   DROP FUNCTION public.check_and_insert_stage_id();
       public               root    false            �            1259    25426    match_partials    TABLE     �   CREATE TABLE public.match_partials (
    match_id integer NOT NULL,
    q1_home integer,
    q2_home integer,
    q3_home integer,
    q4_home integer,
    q1_away integer,
    q2_away integer,
    q3_away integer,
    q4_away integer
);
 "   DROP TABLE public.match_partials;
       public         heap r       ayllon    false            �            1259    25429    players_career_path    TABLE     5  CREATE TABLE public.players_career_path (
    identifier integer NOT NULL,
    player_id bigint NOT NULL,
    season character varying(255),
    league character varying(255),
    team_id bigint,
    team_name character varying(255),
    license character varying(255),
    date_in date,
    date_out date
);
 '   DROP TABLE public.players_career_path;
       public         heap r       ayllon    false            �            1259    25434 "   players_career_path_identifier_seq    SEQUENCE     �   CREATE SEQUENCE public.players_career_path_identifier_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE public.players_career_path_identifier_seq;
       public               ayllon    false    218            �           0    0 "   players_career_path_identifier_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE public.players_career_path_identifier_seq OWNED BY public.players_career_path.identifier;
          public               ayllon    false    219            �            1259    25435    players_info    TABLE     %  CREATE TABLE public.players_info (
    player_id bigint NOT NULL,
    player_name character varying(255),
    "position" character varying(255),
    height bigint,
    weight bigint,
    birthday date,
    nationality character varying(255),
    player_link character varying(255) NOT NULL
);
     DROP TABLE public.players_info;
       public         heap r       ayllon    false            �            1259    25820 $   players_matches_stats_identifier_seq    SEQUENCE     �   CREATE SEQUENCE public.players_matches_stats_identifier_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.players_matches_stats_identifier_seq;
       public               root    false            �            1259    25440    players_matches_stats    TABLE     S  CREATE TABLE public.players_matches_stats (
    identifier integer DEFAULT nextval('public.players_matches_stats_identifier_seq'::regclass) NOT NULL,
    match_id integer,
    team_id integer,
    vs_team_id integer,
    player_id integer,
    player_link character varying(255),
    starting boolean,
    number integer,
    player_name character varying(255),
    minutes time without time zone,
    points integer,
    two_points_in integer,
    two_points_tried integer,
    two_points_perc double precision,
    three_points_in integer,
    three_points_tried integer,
    three_points_perc double precision,
    field_goals_in integer,
    field_goals_tried integer,
    field_goals_perc double precision,
    free_throws_in integer,
    free_throws_tried integer,
    free_throws_perc double precision,
    offensive_rebounds integer,
    deffensive_rebounds integer,
    total_rebounds integer,
    assists integer,
    steals integer,
    turnovers integer,
    blocks_favor integer,
    blocks_against integer,
    dunks integer,
    personal_fouls integer,
    fouls_received integer,
    efficiency integer,
    balance integer,
    middle_shootings_in integer,
    middle_shootings_tried integer,
    middle_shootings_perc double precision,
    zone_shootings_in integer,
    zone_shootings_tried integer,
    zone_shootings_perc double precision
);
 )   DROP TABLE public.players_matches_stats;
       public         heap r       ayllon    false    231            �            1259    25445    players_stats_career    TABLE     �  CREATE TABLE public.players_stats_career (
    player_id integer NOT NULL,
    season character varying(255),
    team_name_extended character varying(255),
    stage_abbrev character varying(255),
    stage_name_extended character varying(255),
    n_matches bigint,
    min_total character varying(255),
    min_avg time(0) without time zone,
    points_total bigint,
    points_avg double precision,
    twos_in_total bigint,
    twos_tried_total bigint,
    twos_perc double precision,
    twos_in_avg double precision,
    twos_tried_avg double precision,
    threes_in_total bigint,
    threes_tried_total bigint,
    threes_perc double precision,
    threes_in_avg double precision,
    threes_tried_avg double precision,
    field_goals_in_total bigint,
    field_goals_tried_total bigint,
    field_goals_perc double precision,
    field_goals_in_avg double precision,
    field_goals_tried_avg double precision,
    free_throws_in_total bigint,
    free_throws_tried_total bigint,
    free_throws_perc double precision,
    free_throws_in_avg double precision,
    free_throws_tried_avg double precision,
    offensive_rebounds_total bigint,
    offensive_rebounds_avg double precision,
    deffensive_rebounds_total bigint,
    deffensive_rebounds_avg double precision,
    total_rebounds_total bigint,
    total_rebounds_avg double precision,
    assists_total bigint,
    assists_avg double precision,
    turnovers_total bigint,
    turnovers_avg double precision,
    blocks_favor_total bigint,
    blocks_favor_avg double precision,
    blocks_against_total bigint,
    blocks_against_avg double precision,
    dunks_total bigint,
    dunks_avg double precision,
    personal_fouls_total bigint,
    personal_fouls_avg double precision,
    fouls_received_total bigint,
    fouls_received_avg double precision,
    efficiency_total bigint,
    efficiency_avg double precision,
    identifier integer NOT NULL
);
 (   DROP TABLE public.players_stats_career;
       public         heap r       ayllon    false            �            1259    25450 #   players_stats_career_identifier_seq    SEQUENCE     �   CREATE SEQUENCE public.players_stats_career_identifier_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 :   DROP SEQUENCE public.players_stats_career_identifier_seq;
       public               ayllon    false    222            �           0    0 #   players_stats_career_identifier_seq    SEQUENCE OWNED BY     k   ALTER SEQUENCE public.players_stats_career_identifier_seq OWNED BY public.players_stats_career.identifier;
          public               ayllon    false    223            �            1259    25451    players_stats_career_view    VIEW     �  CREATE VIEW public.players_stats_career_view AS
 SELECT DISTINCT player_id,
    season,
    team_name_extended,
    stage_abbrev,
    stage_name_extended,
    n_matches,
    min_total,
    (regexp_replace((min_total)::text, ':.*'::text, ''::text))::integer AS min_total_mins,
    min_avg,
    points_total,
    points_avg,
    twos_in_total,
    twos_tried_total,
    twos_perc,
    twos_in_avg,
    twos_tried_avg,
    threes_in_total,
    threes_perc,
    threes_in_avg,
    threes_tried_avg,
    field_goals_tried_total,
    field_goals_perc,
    field_goals_in_avg,
    field_goals_tried_avg,
    free_throws_tried_total,
    free_throws_perc,
    free_throws_in_avg,
    free_throws_tried_avg,
    offensive_rebounds_total,
    offensive_rebounds_avg,
    deffensive_rebounds_total,
    deffensive_rebounds_avg,
    total_rebounds_total,
    total_rebounds_avg,
    assists_total,
    assists_avg,
    turnovers_total,
    turnovers_avg,
    blocks_favor_total,
    blocks_favor_avg,
    blocks_against_total,
    blocks_against_avg,
    dunks_total,
    dunks_avg,
    personal_fouls_total,
    personal_fouls_avg,
    fouls_received_total,
    fouls_received_avg,
    efficiency_total,
    efficiency_avg
   FROM public.players_stats_career;
 ,   DROP VIEW public.players_stats_career_view;
       public       v       ayllon    false    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222    222            �            1259    25456    results    TABLE     M  CREATE TABLE public.results (
    match_id integer NOT NULL,
    home_team_id integer,
    away_team_id integer,
    stage_id integer,
    matchday integer,
    home_score integer,
    away_score integer,
    date date,
    match_link character varying(255),
    "time" time without time zone,
    category character varying(255)
);
    DROP TABLE public.results;
       public         heap r       ayllon    false            �            1259    25461    shooting_chart_availability    TABLE     m   CREATE TABLE public.shooting_chart_availability (
    match_id integer NOT NULL,
    availability boolean
);
 /   DROP TABLE public.shooting_chart_availability;
       public         heap r       ayllon    false            �            1259    25822    shootings_identifier_seq    SEQUENCE     �   CREATE SEQUENCE public.shootings_identifier_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.shootings_identifier_seq;
       public               root    false            �            1259    25464 	   shootings    TABLE       CREATE TABLE public.shootings (
    identifier integer DEFAULT nextval('public.shootings_identifier_seq'::regclass) NOT NULL,
    player_id integer NOT NULL,
    match_id integer NOT NULL,
    team_id integer,
    home_away character varying(255),
    vs_team_id integer,
    number integer,
    player_name character varying(255),
    success boolean,
    quarter integer,
    shoot_time time without time zone,
    top_top double precision,
    left_left double precision,
    shooting_type character varying(255)
);
    DROP TABLE public.shootings;
       public         heap r       ayllon    false    233            �            1259    25469    stages    TABLE     w   CREATE TABLE public.stages (
    stage_id integer NOT NULL,
    stage_name character varying(255),
    year integer
);
    DROP TABLE public.stages;
       public         heap r       ayllon    false            �            1259    25472    teams    TABLE     b   CREATE TABLE public.teams (
    team_id integer NOT NULL,
    team_name character varying(255)
);
    DROP TABLE public.teams;
       public         heap r       ayllon    false            �            1259    25821 "   teams_matches_stats_identifier_seq    SEQUENCE     �   CREATE SEQUENCE public.teams_matches_stats_identifier_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE public.teams_matches_stats_identifier_seq;
       public               root    false            �            1259    25475    teams_matches_stats    TABLE     �  CREATE TABLE public.teams_matches_stats (
    identifier integer DEFAULT nextval('public.teams_matches_stats_identifier_seq'::regclass) NOT NULL,
    match_id integer NOT NULL,
    team_id integer,
    vs_team_id integer,
    points integer,
    two_points_in integer,
    two_points_tried integer,
    two_points_perc double precision,
    three_points_in integer,
    three_points_tried integer,
    three_points_perc double precision,
    field_goals_in integer,
    field_goals_tried integer,
    field_goals_perc double precision,
    free_throws_in integer,
    free_throws_tried integer,
    free_throws_perc double precision,
    offensive_rebounds integer,
    deffensive_rebounds integer,
    total_rebounds integer,
    assists integer,
    steals integer,
    turnovers integer,
    blocks_favor integer,
    blocks_against integer,
    dunks integer,
    personal_fouls integer,
    fouls_received integer,
    efficiency integer,
    middle_shootings_in integer,
    middle_shootings_tried integer,
    middle_shootings_perc double precision,
    zone_shootings_in integer,
    zone_shootings_tried integer,
    zone_shootings_perc double precision,
    minutes character varying(255)
);
 '   DROP TABLE public.teams_matches_stats;
       public         heap r       ayllon    false    232            �           2604    25478    players_career_path identifier    DEFAULT     �   ALTER TABLE ONLY public.players_career_path ALTER COLUMN identifier SET DEFAULT nextval('public.players_career_path_identifier_seq'::regclass);
 M   ALTER TABLE public.players_career_path ALTER COLUMN identifier DROP DEFAULT;
       public               ayllon    false    219    218            �           2604    25479    players_stats_career identifier    DEFAULT     �   ALTER TABLE ONLY public.players_stats_career ALTER COLUMN identifier SET DEFAULT nextval('public.players_stats_career_identifier_seq'::regclass);
 N   ALTER TABLE public.players_stats_career ALTER COLUMN identifier DROP DEFAULT;
       public               ayllon    false    223    222            �           2606    25481 "   match_partials match_partials_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.match_partials
    ADD CONSTRAINT match_partials_pkey PRIMARY KEY (match_id);
 L   ALTER TABLE ONLY public.match_partials DROP CONSTRAINT match_partials_pkey;
       public                 ayllon    false    217            �           2606    25483 ,   players_career_path players_career_path_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.players_career_path
    ADD CONSTRAINT players_career_path_pkey PRIMARY KEY (identifier);
 V   ALTER TABLE ONLY public.players_career_path DROP CONSTRAINT players_career_path_pkey;
       public                 ayllon    false    218            �           2606    25485    players_info players_info_PKEY 
   CONSTRAINT     e   ALTER TABLE ONLY public.players_info
    ADD CONSTRAINT "players_info_PKEY" PRIMARY KEY (player_id);
 J   ALTER TABLE ONLY public.players_info DROP CONSTRAINT "players_info_PKEY";
       public                 ayllon    false    220            �           2606    25487 2   players_matches_stats players_matches_stats_2_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.players_matches_stats
    ADD CONSTRAINT players_matches_stats_2_pkey PRIMARY KEY (identifier);
 \   ALTER TABLE ONLY public.players_matches_stats DROP CONSTRAINT players_matches_stats_2_pkey;
       public                 ayllon    false    221            �           2606    25489 .   players_stats_career players_stats_career_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public.players_stats_career
    ADD CONSTRAINT players_stats_career_pkey PRIMARY KEY (identifier);
 X   ALTER TABLE ONLY public.players_stats_career DROP CONSTRAINT players_stats_career_pkey;
       public                 ayllon    false    222            �           2606    25491    results results_leb_oro_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_leb_oro_pkey PRIMARY KEY (match_id);
 F   ALTER TABLE ONLY public.results DROP CONSTRAINT results_leb_oro_pkey;
       public                 ayllon    false    225            �           2606    25493 <   shooting_chart_availability shooting_chart_availability_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.shooting_chart_availability
    ADD CONSTRAINT shooting_chart_availability_pkey PRIMARY KEY (match_id);
 f   ALTER TABLE ONLY public.shooting_chart_availability DROP CONSTRAINT shooting_chart_availability_pkey;
       public                 ayllon    false    226            �           2606    25495    shootings shootings_pkey_2 
   CONSTRAINT     `   ALTER TABLE ONLY public.shootings
    ADD CONSTRAINT shootings_pkey_2 PRIMARY KEY (identifier);
 D   ALTER TABLE ONLY public.shootings DROP CONSTRAINT shootings_pkey_2;
       public                 ayllon    false    227            �           2606    25497    stages stages_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.stages
    ADD CONSTRAINT stages_pkey PRIMARY KEY (stage_id);
 <   ALTER TABLE ONLY public.stages DROP CONSTRAINT stages_pkey;
       public                 ayllon    false    228            �           2606    25499 .   teams_matches_stats teams_matches_stats_2_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public.teams_matches_stats
    ADD CONSTRAINT teams_matches_stats_2_pkey PRIMARY KEY (identifier);
 X   ALTER TABLE ONLY public.teams_matches_stats DROP CONSTRAINT teams_matches_stats_2_pkey;
       public                 ayllon    false    230            �           2606    25501    teams teams_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (team_id);
 :   ALTER TABLE ONLY public.teams DROP CONSTRAINT teams_pkey;
       public                 ayllon    false    229            �           2620    25590 -   results check_and_insert_away_team_id_trigger    TRIGGER     �   CREATE TRIGGER check_and_insert_away_team_id_trigger BEFORE INSERT ON public.results FOR EACH ROW EXECUTE FUNCTION public.check_and_insert_away_team_id();
 F   DROP TRIGGER check_and_insert_away_team_id_trigger ON public.results;
       public               ayllon    false    235    225            �           2620    25592 -   results check_and_insert_home_team_id_trigger    TRIGGER     �   CREATE TRIGGER check_and_insert_home_team_id_trigger BEFORE INSERT ON public.results FOR EACH ROW EXECUTE FUNCTION public.check_and_insert_home_team_id();
 F   DROP TRIGGER check_and_insert_home_team_id_trigger ON public.results;
       public               ayllon    false    236    225            �           2620    25594 *   results check_and_insert_player_id_trigger    TRIGGER     �   CREATE TRIGGER check_and_insert_player_id_trigger BEFORE INSERT ON public.results FOR EACH ROW EXECUTE FUNCTION public.check_and_insert_player_id();
 C   DROP TRIGGER check_and_insert_player_id_trigger ON public.results;
       public               ayllon    false    225    237            �           2620    25588 )   results check_and_insert_stage_id_trigger    TRIGGER     �   CREATE TRIGGER check_and_insert_stage_id_trigger BEFORE INSERT ON public.results FOR EACH ROW EXECUTE FUNCTION public.check_and_insert_stage_id();
 B   DROP TRIGGER check_and_insert_stage_id_trigger ON public.results;
       public               ayllon    false    225    234            �           2606    25502    results away_team_id    FK CONSTRAINT     }   ALTER TABLE ONLY public.results
    ADD CONSTRAINT away_team_id FOREIGN KEY (away_team_id) REFERENCES public.teams(team_id);
 >   ALTER TABLE ONLY public.results DROP CONSTRAINT away_team_id;
       public               ayllon    false    229    3286    225            �           2606    25507    results home_team_id    FK CONSTRAINT     }   ALTER TABLE ONLY public.results
    ADD CONSTRAINT home_team_id FOREIGN KEY (home_team_id) REFERENCES public.teams(team_id);
 >   ALTER TABLE ONLY public.results DROP CONSTRAINT home_team_id;
       public               ayllon    false    229    3286    225            �           2606    25512 $   shooting_chart_availability match_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.shooting_chart_availability
    ADD CONSTRAINT match_id FOREIGN KEY (match_id) REFERENCES public.results(match_id) NOT VALID;
 N   ALTER TABLE ONLY public.shooting_chart_availability DROP CONSTRAINT match_id;
       public               ayllon    false    225    3278    226            �           2606    25517    match_partials match_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.match_partials
    ADD CONSTRAINT match_id FOREIGN KEY (match_id) REFERENCES public.results(match_id) NOT VALID;
 A   ALTER TABLE ONLY public.match_partials DROP CONSTRAINT match_id;
       public               ayllon    false    225    3278    217            �           2606    25522    players_matches_stats match_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.players_matches_stats
    ADD CONSTRAINT match_id FOREIGN KEY (match_id) REFERENCES public.results(match_id) NOT VALID;
 H   ALTER TABLE ONLY public.players_matches_stats DROP CONSTRAINT match_id;
       public               ayllon    false    221    225    3278            �           2606    25527    teams_matches_stats match_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams_matches_stats
    ADD CONSTRAINT match_id FOREIGN KEY (match_id) REFERENCES public.results(match_id) NOT VALID;
 F   ALTER TABLE ONLY public.teams_matches_stats DROP CONSTRAINT match_id;
       public               ayllon    false    230    3278    225            �           2606    25532    shootings match_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.shootings
    ADD CONSTRAINT match_id FOREIGN KEY (match_id) REFERENCES public.results(match_id) NOT VALID;
 <   ALTER TABLE ONLY public.shootings DROP CONSTRAINT match_id;
       public               ayllon    false    225    227    3278            �           2606    25537    players_career_path player_idFK    FK CONSTRAINT     �   ALTER TABLE ONLY public.players_career_path
    ADD CONSTRAINT "player_idFK" FOREIGN KEY (player_id) REFERENCES public.players_info(player_id) NOT VALID;
 K   ALTER TABLE ONLY public.players_career_path DROP CONSTRAINT "player_idFK";
       public               ayllon    false    3272    218    220            �           2606    25542     players_stats_career player_idFK    FK CONSTRAINT     �   ALTER TABLE ONLY public.players_stats_career
    ADD CONSTRAINT "player_idFK" FOREIGN KEY (player_id) REFERENCES public.players_info(player_id) NOT VALID;
 L   ALTER TABLE ONLY public.players_stats_career DROP CONSTRAINT "player_idFK";
       public               ayllon    false    3272    222    220            �           2606    25547    results stage_id    FK CONSTRAINT     w   ALTER TABLE ONLY public.results
    ADD CONSTRAINT stage_id FOREIGN KEY (stage_id) REFERENCES public.stages(stage_id);
 :   ALTER TABLE ONLY public.results DROP CONSTRAINT stage_id;
       public               ayllon    false    3284    225    228            �           2606    25552    players_matches_stats team_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.players_matches_stats
    ADD CONSTRAINT team_id FOREIGN KEY (team_id) REFERENCES public.teams(team_id) NOT VALID;
 G   ALTER TABLE ONLY public.players_matches_stats DROP CONSTRAINT team_id;
       public               ayllon    false    3286    221    229            �           2606    25557    teams_matches_stats team_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams_matches_stats
    ADD CONSTRAINT team_id FOREIGN KEY (team_id) REFERENCES public.teams(team_id) NOT VALID;
 E   ALTER TABLE ONLY public.teams_matches_stats DROP CONSTRAINT team_id;
       public               ayllon    false    3286    230    229            �           2606    25562    shootings team_id    FK CONSTRAINT        ALTER TABLE ONLY public.shootings
    ADD CONSTRAINT team_id FOREIGN KEY (team_id) REFERENCES public.teams(team_id) NOT VALID;
 ;   ALTER TABLE ONLY public.shootings DROP CONSTRAINT team_id;
       public               ayllon    false    229    3286    227            �           2606    25567    players_career_path team_idFK    FK CONSTRAINT     �   ALTER TABLE ONLY public.players_career_path
    ADD CONSTRAINT "team_idFK" FOREIGN KEY (team_id) REFERENCES public.teams(team_id) NOT VALID;
 I   ALTER TABLE ONLY public.players_career_path DROP CONSTRAINT "team_idFK";
       public               ayllon    false    218    229    3286            �           2606    25572     players_matches_stats vs_team_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.players_matches_stats
    ADD CONSTRAINT vs_team_id FOREIGN KEY (vs_team_id) REFERENCES public.teams(team_id) NOT VALID;
 J   ALTER TABLE ONLY public.players_matches_stats DROP CONSTRAINT vs_team_id;
       public               ayllon    false    229    221    3286            �           2606    25577    teams_matches_stats vs_team_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.teams_matches_stats
    ADD CONSTRAINT vs_team_id FOREIGN KEY (vs_team_id) REFERENCES public.teams(team_id) NOT VALID;
 H   ALTER TABLE ONLY public.teams_matches_stats DROP CONSTRAINT vs_team_id;
       public               ayllon    false    230    229    3286            �           2606    25582    shootings vs_team_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.shootings
    ADD CONSTRAINT vs_team_id FOREIGN KEY (vs_team_id) REFERENCES public.teams(team_id) NOT VALID;
 >   ALTER TABLE ONLY public.shootings DROP CONSTRAINT vs_team_id;
       public               ayllon    false    227    229    3286           