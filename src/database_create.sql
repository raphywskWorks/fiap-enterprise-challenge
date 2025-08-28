CREATE TABLE PECAS (
    id_peca INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(100) NOT NULL,
    fabricante VARCHAR(100),
    tempo_uso_total INT
);

CREATE TABLE SENSORES (
    id_sensor INT PRIMARY KEY AUTO_INCREMENT,
    tipo_sensor VARCHAR(50) NOT NULL,
    id_peca INT,
    FOREIGN KEY (id_peca) REFERENCES PECAS(id_peca)
);

CREATE TABLE CICLOS_OPERACAO (
    id_ciclo INT PRIMARY KEY AUTO_INCREMENT,
    id_peca INT,
    data_inicio DATETIME,
    data_fim DATETIME,
    duracao INT,
    FOREIGN KEY (id_peca) REFERENCES PECAS(id_peca)
);

CREATE TABLE LEITURAS_SENSOR (
    id_leitura INT PRIMARY KEY AUTO_INCREMENT,
    id_sensor INT,
    leitura_valor FLOAT,
    leitura_data_hora DATETIME,
    FOREIGN KEY (id_sensor) REFERENCES SENSORES(id_sensor)
);

CREATE TABLE FALHAS (
    id_falha INT PRIMARY KEY AUTO_INCREMENT,
    id_peca INT,
    descricao VARCHAR(255),
    data DATETIME,
    FOREIGN KEY (id_peca) REFERENCES PECAS(id_peca)
);

CREATE TABLE ALERTAS (
    id_alerta INT PRIMARY KEY AUTO_INCREMENT,
    id_falha INT,
    nivel_risco VARCHAR(20),
    FOREIGN KEY (id_falha) REFERENCES FALHAS(id_falha)
);
