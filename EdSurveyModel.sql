-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.8.1
-- PostgreSQL version: 9.4
-- Project Site: pgmodeler.com.br
-- Model Author: ---


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: anketing | type: DATABASE --
-- -- DROP DATABASE IF EXISTS anketing;
-- CREATE DATABASE anketing
-- ;
-- -- ddl-end --
-- 

-- object: public."user" | type: TABLE --
-- DROP TABLE IF EXISTS public."user" CASCADE;
CREATE TABLE public."user"(
	id serial NOT NULL,
	name varchar(64) NOT NULL,
	email varchar(64) NOT NULL,
	status smallint,
	CONSTRAINT pk_users PRIMARY KEY (id)

);
-- ddl-end --
COMMENT ON TABLE public."user" IS 'предполагается, что это таблица Django';
-- ddl-end --
ALTER TABLE public."user" OWNER TO postgres;
-- ddl-end --

-- object: public.roles | type: TABLE --
-- DROP TABLE IF EXISTS public.roles CASCADE;
CREATE TABLE public.roles(
	id smallint NOT NULL,
	name varchar(16) NOT NULL
);
-- ddl-end --
COMMENT ON TABLE public.roles IS 'Под какими ролями может входить на сайт пользователь. Влияет на доступную функциональность.';
-- ddl-end --
ALTER TABLE public.roles OWNER TO postgres;
-- ddl-end --

-- object: public.organisation | type: TABLE --
-- DROP TABLE IF EXISTS public.organisation CASCADE;
CREATE TABLE public.organisation(
	id serial NOT NULL,
	name varchar(64) NOT NULL,
	status smallint,
	supervisors smallint,
	CONSTRAINT pk_organisations PRIMARY KEY (id)

);
-- ddl-end --
COMMENT ON COLUMN public.organisation.supervisors IS 'группа супер-пользователей данной организации -> groups.id';
-- ddl-end --
ALTER TABLE public.organisation OWNER TO postgres;
-- ddl-end --

-- object: public."group" | type: TABLE --
-- DROP TABLE IF EXISTS public."group" CASCADE;
CREATE TABLE public."group"(
	id serial NOT NULL,
	name varchar(64) NOT NULL,
	status smallint
);
-- ddl-end --
ALTER TABLE public."group" OWNER TO postgres;
-- ddl-end --

-- object: public.usergroups | type: TABLE --
-- DROP TABLE IF EXISTS public.usergroups CASCADE;
CREATE TABLE public.usergroups(
	"user" smallint NOT NULL,
	"group" smallint NOT NULL,
	status smallint,
	organisation smallint NOT NULL,
	CONSTRAINT pk_usergroups PRIMARY KEY ("user","group")

);
-- ddl-end --
ALTER TABLE public.usergroups OWNER TO postgres;
-- ddl-end --

-- object: public.test | type: TABLE --
-- DROP TABLE IF EXISTS public.test CASCADE;
CREATE TABLE public.test(
	id serial NOT NULL,
	name varchar(64) NOT NULL,
	description text,
	status smallint,
	authors smallint NOT NULL,
	params xml,
	anketa smallint NOT NULL,
	CONSTRAINT pk_tests PRIMARY KEY (id)

);
-- ddl-end --
COMMENT ON TABLE public.test IS 'упорядоченость вопросов; возомжность редактировать свои ответы; количество попыток и т.п.';
-- ddl-end --
ALTER TABLE public.test OWNER TO postgres;
-- ddl-end --

-- object: public.userorgs | type: TABLE --
-- DROP TABLE IF EXISTS public.userorgs CASCADE;
CREATE TABLE public.userorgs(
	"user" smallint NOT NULL,
	organisation smallint NOT NULL,
	status smallint,
	CONSTRAINT pk_userorgs PRIMARY KEY ("user",organisation)

);
-- ddl-end --
COMMENT ON TABLE public.userorgs IS 'В какие организации входит пользователь.';
-- ddl-end --
ALTER TABLE public.userorgs OWNER TO postgres;
-- ddl-end --

-- object: public.task | type: TABLE --
-- DROP TABLE IF EXISTS public.task CASCADE;
CREATE TABLE public.task(
	id serial NOT NULL,
	teachers smallint NOT NULL,
	students smallint NOT NULL,
	organisation smallint NOT NULL,
	test smallint NOT NULL,
	status smallint,
	CONSTRAINT pk_tasks PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.task OWNER TO postgres;
-- ddl-end --

-- object: public.schedule | type: TABLE --
-- DROP TABLE IF EXISTS public.schedule CASCADE;
CREATE TABLE public.schedule(
	id serial NOT NULL,
	task smallint NOT NULL,
	duration daterange NOT NULL,
	CONSTRAINT pk_schedules PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.schedule OWNER TO postgres;
-- ddl-end --

-- object: public.question | type: TABLE --
-- DROP TABLE IF EXISTS public.question CASCADE;
CREATE TABLE public.question(
	id serial NOT NULL,
	qtype smallint NOT NULL,
	status smallint,
	content xml NOT NULL,
	organisation smallint NOT NULL,
	authors smallint NOT NULL,
	inverse smallint,
	CONSTRAINT pk_questions PRIMARY KEY (id)

);
-- ddl-end --
COMMENT ON COLUMN public.question.organisation IS 'Кому принадлежит. Возможно public или организация самого сайта';
-- ddl-end --
COMMENT ON COLUMN public.question.inverse IS 'обратный вопрос для кросс-проверок';
-- ddl-end --
ALTER TABLE public.question OWNER TO postgres;
-- ddl-end --

-- object: public.qtype | type: TABLE --
-- DROP TABLE IF EXISTS public.qtype CASCADE;
CREATE TABLE public.qtype(
	id smallint NOT NULL,
	name varchar(16) NOT NULL,
	CONSTRAINT pk_qtypes PRIMARY KEY (id)

);
-- ddl-end --
COMMENT ON TABLE public.qtype IS 'тип вопроса: radio, check, relations';
-- ddl-end --
ALTER TABLE public.qtype OWNER TO postgres;
-- ddl-end --

-- object: public.anketas | type: TABLE --
-- DROP TABLE IF EXISTS public.anketas CASCADE;
CREATE TABLE public.anketas(
	test smallint NOT NULL,
	question smallint NOT NULL,
	"order" smallint,
	status smallint,
	CONSTRAINT pk_anketas PRIMARY KEY (test,question)

);
-- ddl-end --
COMMENT ON TABLE public.anketas IS 'Контейнер из вопросов для конкретного теста.';
-- ddl-end --
COMMENT ON COLUMN public.anketas."order" IS 'порядок, если он важен';
-- ddl-end --
ALTER TABLE public.anketas OWNER TO postgres;
-- ddl-end --

-- object: public.activities | type: TABLE --
-- DROP TABLE IF EXISTS public.activities CASCADE;
CREATE TABLE public.activities(
	"when" date NOT NULL DEFAULT now(),
	what text,
	role smallint NOT NULL,
	who smallint NOT NULL
);
-- ddl-end --
COMMENT ON TABLE public.activities IS 'журнал активности пользователей';
-- ddl-end --
COMMENT ON COLUMN public.activities.what IS 'какое действие выполнялось';
-- ddl-end --
COMMENT ON COLUMN public.activities.role IS 'под какой ролью';
-- ddl-end --
ALTER TABLE public.activities OWNER TO postgres;
-- ddl-end --

-- object: public.answer | type: TABLE --
-- DROP TABLE IF EXISTS public.answer CASCADE;
CREATE TABLE public.answer(
	id serial NOT NULL,
	question smallint NOT NULL,
	content text NOT NULL,
	"order" smallint,
	score smallint,
	status smallint,
	CONSTRAINT pk_answers PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.answer OWNER TO postgres;
-- ddl-end --

-- object: public.surveys | type: TABLE --
-- DROP TABLE IF EXISTS public.surveys CASCADE;
CREATE TABLE public.surveys(
	"user" smallint NOT NULL,
	task smallint NOT NULL,
	question smallint NOT NULL,
	attempt smallint NOT NULL,
	answer smallint NOT NULL,
	score smallint,
	status smallint,
	CONSTRAINT pk_surveys PRIMARY KEY ("user",task,question,attempt)

);
-- ddl-end --
COMMENT ON TABLE public.surveys IS 'Ответы пользователей на анкеты';
-- ddl-end --
COMMENT ON COLUMN public.surveys.attempt IS 'номер попытки. datetime поптыки искать в журнале.';
-- ddl-end --
ALTER TABLE public.surveys OWNER TO postgres;
-- ddl-end --

-- object: fk_organisations_supervisors | type: CONSTRAINT --
-- ALTER TABLE public.organisation DROP CONSTRAINT IF EXISTS fk_organisations_supervisors CASCADE;
ALTER TABLE public.organisation ADD CONSTRAINT fk_organisations_supervisors FOREIGN KEY (supervisors)
REFERENCES public."group" (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_usergroups_users | type: CONSTRAINT --
-- ALTER TABLE public.usergroups DROP CONSTRAINT IF EXISTS fk_usergroups_users CASCADE;
ALTER TABLE public.usergroups ADD CONSTRAINT fk_usergroups_users FOREIGN KEY ("user")
REFERENCES public."user" (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_usergroups_groups | type: CONSTRAINT --
-- ALTER TABLE public.usergroups DROP CONSTRAINT IF EXISTS fk_usergroups_groups CASCADE;
ALTER TABLE public.usergroups ADD CONSTRAINT fk_usergroups_groups FOREIGN KEY ("group")
REFERENCES public."group" (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_usergroups_organisation | type: CONSTRAINT --
-- ALTER TABLE public.usergroups DROP CONSTRAINT IF EXISTS fk_usergroups_organisation CASCADE;
ALTER TABLE public.usergroups ADD CONSTRAINT fk_usergroups_organisation FOREIGN KEY (organisation)
REFERENCES public.organisation (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_tests_authors | type: CONSTRAINT --
-- ALTER TABLE public.test DROP CONSTRAINT IF EXISTS fk_tests_authors CASCADE;
ALTER TABLE public.test ADD CONSTRAINT fk_tests_authors FOREIGN KEY (authors)
REFERENCES public."group" (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_userorgs_user | type: CONSTRAINT --
-- ALTER TABLE public.userorgs DROP CONSTRAINT IF EXISTS fk_userorgs_user CASCADE;
ALTER TABLE public.userorgs ADD CONSTRAINT fk_userorgs_user FOREIGN KEY ("user")
REFERENCES public."user" (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_userorgs_organisation | type: CONSTRAINT --
-- ALTER TABLE public.userorgs DROP CONSTRAINT IF EXISTS fk_userorgs_organisation CASCADE;
ALTER TABLE public.userorgs ADD CONSTRAINT fk_userorgs_organisation FOREIGN KEY (organisation)
REFERENCES public.organisation (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_tasks_organisation | type: CONSTRAINT --
-- ALTER TABLE public.task DROP CONSTRAINT IF EXISTS fk_tasks_organisation CASCADE;
ALTER TABLE public.task ADD CONSTRAINT fk_tasks_organisation FOREIGN KEY (organisation)
REFERENCES public.organisation (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_tasks_teachers | type: CONSTRAINT --
-- ALTER TABLE public.task DROP CONSTRAINT IF EXISTS fk_tasks_teachers CASCADE;
ALTER TABLE public.task ADD CONSTRAINT fk_tasks_teachers FOREIGN KEY (teachers)
REFERENCES public."group" (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_tasks_students | type: CONSTRAINT --
-- ALTER TABLE public.task DROP CONSTRAINT IF EXISTS fk_tasks_students CASCADE;
ALTER TABLE public.task ADD CONSTRAINT fk_tasks_students FOREIGN KEY (students)
REFERENCES public."group" (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_tasks_test | type: CONSTRAINT --
-- ALTER TABLE public.task DROP CONSTRAINT IF EXISTS fk_tasks_test CASCADE;
ALTER TABLE public.task ADD CONSTRAINT fk_tasks_test FOREIGN KEY (test)
REFERENCES public.test (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_schedules_task | type: CONSTRAINT --
-- ALTER TABLE public.schedule DROP CONSTRAINT IF EXISTS fk_schedules_task CASCADE;
ALTER TABLE public.schedule ADD CONSTRAINT fk_schedules_task FOREIGN KEY (task)
REFERENCES public.task (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_questions_qtype | type: CONSTRAINT --
-- ALTER TABLE public.question DROP CONSTRAINT IF EXISTS fk_questions_qtype CASCADE;
ALTER TABLE public.question ADD CONSTRAINT fk_questions_qtype FOREIGN KEY (qtype)
REFERENCES public.qtype (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_questions_organisation | type: CONSTRAINT --
-- ALTER TABLE public.question DROP CONSTRAINT IF EXISTS fk_questions_organisation CASCADE;
ALTER TABLE public.question ADD CONSTRAINT fk_questions_organisation FOREIGN KEY (organisation)
REFERENCES public.organisation (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_questions_authors | type: CONSTRAINT --
-- ALTER TABLE public.question DROP CONSTRAINT IF EXISTS fk_questions_authors CASCADE;
ALTER TABLE public.question ADD CONSTRAINT fk_questions_authors FOREIGN KEY (authors)
REFERENCES public."group" (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_questions_inverse | type: CONSTRAINT --
-- ALTER TABLE public.question DROP CONSTRAINT IF EXISTS fk_questions_inverse CASCADE;
ALTER TABLE public.question ADD CONSTRAINT fk_questions_inverse FOREIGN KEY (inverse)
REFERENCES public.question (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_anketa_question | type: CONSTRAINT --
-- ALTER TABLE public.anketas DROP CONSTRAINT IF EXISTS fk_anketa_question CASCADE;
ALTER TABLE public.anketas ADD CONSTRAINT fk_anketa_question FOREIGN KEY (question)
REFERENCES public.question (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_anketas_test | type: CONSTRAINT --
-- ALTER TABLE public.anketas DROP CONSTRAINT IF EXISTS fk_anketas_test CASCADE;
ALTER TABLE public.anketas ADD CONSTRAINT fk_anketas_test FOREIGN KEY (test)
REFERENCES public.test (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_answers_question | type: CONSTRAINT --
-- ALTER TABLE public.answer DROP CONSTRAINT IF EXISTS fk_answers_question CASCADE;
ALTER TABLE public.answer ADD CONSTRAINT fk_answers_question FOREIGN KEY (question)
REFERENCES public.question (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_surveys_user | type: CONSTRAINT --
-- ALTER TABLE public.surveys DROP CONSTRAINT IF EXISTS fk_surveys_user CASCADE;
ALTER TABLE public.surveys ADD CONSTRAINT fk_surveys_user FOREIGN KEY ("user")
REFERENCES public."user" (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_surveys_task | type: CONSTRAINT --
-- ALTER TABLE public.surveys DROP CONSTRAINT IF EXISTS fk_surveys_task CASCADE;
ALTER TABLE public.surveys ADD CONSTRAINT fk_surveys_task FOREIGN KEY (task)
REFERENCES public.task (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_surveys_question | type: CONSTRAINT --
-- ALTER TABLE public.surveys DROP CONSTRAINT IF EXISTS fk_surveys_question CASCADE;
ALTER TABLE public.surveys ADD CONSTRAINT fk_surveys_question FOREIGN KEY (question)
REFERENCES public.question (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: fk_surveys_answer | type: CONSTRAINT --
-- ALTER TABLE public.surveys DROP CONSTRAINT IF EXISTS fk_surveys_answer CASCADE;
ALTER TABLE public.surveys ADD CONSTRAINT fk_surveys_answer FOREIGN KEY (answer)
REFERENCES public.answer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


