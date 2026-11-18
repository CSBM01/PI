CREATE TABLE tecnico (
    id_tecnico INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    setor TEXT
);

CREATE TABLE equipamento (
    id_equipamento INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_tag TEXT UNIQUE NOT NULL,
    descricao TEXT,
    fabricante TEXT
);

CREATE TABLE medicao (
    id_medicao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tecnico INTEGER,
    id_equipamento INTEGER,
    data_calibracao TEXT,
    status_final TEXT,
    FOREIGN KEY (id_tecnico) REFERENCES tecnico(id_tecnico),
    FOREIGN KEY (id_equipamento) REFERENCES equipamento(id_equipamento)
);
