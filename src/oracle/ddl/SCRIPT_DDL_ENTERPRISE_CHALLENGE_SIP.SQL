-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   em:        2025-09-08 20:20:17 BRT
--   site:      Oracle Database 11g
--   tipo:      Oracle Database 11g



DROP TABLE T_SIP_ALERTAS CASCADE CONSTRAINTS 
;

DROP TABLE T_SIP_CICLO_OPERACAO CASCADE CONSTRAINTS 
;

DROP TABLE T_SIP_FALHAS CASCADE CONSTRAINTS 
;

DROP TABLE T_SIP_LEITURA_SENSOR CASCADE CONSTRAINTS 
;

DROP TABLE T_SIP_PECA CASCADE CONSTRAINTS 
;

DROP TABLE T_SIP_SENSOR CASCADE CONSTRAINTS 
;

-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE T_SIP_ALERTAS 
    ( 
     id_alertas NUMBER (3)  NOT NULL , 
     id_falhas  NUMBER (3)  NOT NULL , 
     nv_leitura NUMBER (3)  NOT NULL , 
     tp_alerta  CHAR (10 CHAR)  NOT NULL , 
     ds_alerta  CHAR (50)  NOT NULL 
    ) 
;

ALTER TABLE T_SIP_ALERTAS 
    ADD CONSTRAINT CK_SIP_ALERTAS_NIVEL 
    CHECK (NV_LEITURA != 0)
;
ALTER TABLE T_SIP_ALERTAS 
    ADD CONSTRAINT PK_T_SIP_ALERTAS PRIMARY KEY ( id_alertas ) ;

CREATE TABLE T_SIP_CICLO_OPERACAO 
    ( 
     id_ciclo   NUMBER (3)  NOT NULL , 
     id_peca    NUMBER (3)  NOT NULL , 
     dt_inicio  DATE  NOT NULL , 
     dt_termino DATE  NOT NULL , 
     dr_ciclo   NUMBER (8)  NOT NULL 
    ) 
;

ALTER TABLE T_SIP_CICLO_OPERACAO 
    ADD CONSTRAINT PK_T_SIP_CICLO_OPERACAO PRIMARY KEY ( id_ciclo ) ;

CREATE TABLE T_SIP_FALHAS 
    ( 
     id_falhas NUMBER (3)  NOT NULL , 
     id_peca   NUMBER (3)  NOT NULL , 
     ds_falha  CHAR (50)  NOT NULL , 
     sg_falha  CHAR (5 BYTE)  NOT NULL , 
     dt_falha  DATE  NOT NULL 
    ) 
;

ALTER TABLE T_SIP_FALHAS 
    ADD CONSTRAINT PK_T_SIP_FALHAS PRIMARY KEY ( id_falhas ) ;

CREATE TABLE T_SIP_LEITURA_SENSOR 
    ( 
     id_leitura    NUMBER (3)  NOT NULL , 
     id_ciclo      NUMBER (3)  NOT NULL , 
     vl_leitura    NUMBER  NOT NULL , 
     dt_hr_leitura DATE  NOT NULL 
    ) 
;

ALTER TABLE T_SIP_LEITURA_SENSOR 
    ADD CONSTRAINT CK_SIP_LEITURA_SENSOR_VALOR 
    CHECK (VL_LEITURA != 0)
;
ALTER TABLE T_SIP_LEITURA_SENSOR 
    ADD CONSTRAINT PK_T_SIP_LEITURA_SENSOR PRIMARY KEY ( id_leitura ) ;

CREATE TABLE T_SIP_PECA 
    ( 
     id_peca       NUMBER (3)  NOT NULL , 
     tp_peca       CHAR (20 CHAR)  NOT NULL , 
     nm_facricante CHAR (50 CHAR)  NOT NULL , 
     tmp_uso       NUMBER (8)  NOT NULL , 
     ds_peca       CHAR (150 CHAR)  NOT NULL , 
     dt_instalacao DATE  NOT NULL 
    ) 
;

ALTER TABLE T_SIP_PECA 
    ADD CONSTRAINT PK_T_SIP_PECA PRIMARY KEY ( id_peca ) ;

ALTER TABLE T_SIP_PECA 
    ADD CONSTRAINT UN_SIP_PECA_TIPO UNIQUE ( tp_peca ) ;

ALTER TABLE T_SIP_PECA 
    ADD CONSTRAINT UN_SIP_PECA_NOME UNIQUE ( nm_facricante ) ;

ALTER TABLE T_SIP_PECA 
    ADD CONSTRAINT UN_SIP_PECA_TEMPO UNIQUE ( tmp_uso ) ;

ALTER TABLE T_SIP_PECA 
    ADD CONSTRAINT UN_SIP_PECA_DESCRICAO UNIQUE ( ds_peca ) ;

ALTER TABLE T_SIP_PECA 
    ADD CONSTRAINT UN_SIP_PECA_DATA UNIQUE ( dt_instalacao ) ;

CREATE TABLE T_SIP_SENSOR 
    ( 
     id_sensor     NUMBER (3)  NOT NULL , 
     id_peca       NUMBER (3)  NOT NULL , 
     tp_sensor     CHAR (20 CHAR)  NOT NULL , 
     nm_fabricante CHAR (50)  NOT NULL , 
     dt_instalacao DATE  NOT NULL , 
     md_sensor     CHAR (30)  NOT NULL 
    ) 
;

ALTER TABLE T_SIP_SENSOR 
    ADD CONSTRAINT PK_T_SIP_SENSOR PRIMARY KEY ( id_sensor ) ;

ALTER TABLE T_SIP_ALERTAS 
    ADD CONSTRAINT FK_SIP_ALERTAS_FALHAS FOREIGN KEY 
    ( 
     id_falhas
    ) 
    REFERENCES T_SIP_FALHAS 
    ( 
     id_falhas
    ) 
;

ALTER TABLE T_SIP_CICLO_OPERACAO 
    ADD CONSTRAINT FK_SIP_CICLO_OP_PECA FOREIGN KEY 
    ( 
     id_peca
    ) 
    REFERENCES T_SIP_PECA 
    ( 
     id_peca
    ) 
;

ALTER TABLE T_SIP_FALHAS 
    ADD CONSTRAINT FK_SIP_FALHAS_PECA FOREIGN KEY 
    ( 
     id_peca
    ) 
    REFERENCES T_SIP_PECA 
    ( 
     id_peca
    ) 
;

ALTER TABLE T_SIP_LEITURA_SENSOR 
    ADD CONSTRAINT FK_SIP_LEITURA_SENSOR_CICLO_OP FOREIGN KEY 
    ( 
     id_ciclo
    ) 
    REFERENCES T_SIP_CICLO_OPERACAO 
    ( 
     id_ciclo
    ) 
;

ALTER TABLE T_SIP_SENSOR 
    ADD CONSTRAINT FK_SIP_SENSOR_PECA FOREIGN KEY 
    ( 
     id_peca
    ) 
    REFERENCES T_SIP_PECA 
    ( 
     id_peca
    ) 
;



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             6
-- CREATE INDEX                             0
-- ALTER TABLE                             18
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
