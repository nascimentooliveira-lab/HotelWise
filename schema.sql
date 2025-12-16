PRAGMA foreign_keys = ON;

-- ===============================
-- TABELA: hospedes
-- ===============================
CREATE TABLE IF NOT EXISTS hospedes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL CHECK (LENGTH(TRIM(nome)) > 0),
    documento TEXT UNIQUE NOT NULL,
    email TEXT,
    telefone TEXT
);

-- ===============================
-- TABELA: quartos
-- ===============================
CREATE TABLE IF NOT EXISTS quartos (
    numero INTEGER PRIMARY KEY,
    tipo TEXT NOT NULL,                   -- SIMPLES, DUPLO, LUXO
    capacidade INTEGER NOT NULL,
    tarifa_base REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'DISPONIVEL',  -- DISPONIVEL, OCUPADO, MANUTENCAO, BLOQUEADO

    motivo_bloqueio TEXT,
    bloqueio_inicio TEXT,      -- YYYY-MM-DD
    bloqueio_fim TEXT          -- YYYY-MM-DD
);

-- ===============================
-- TABELA: reservas
-- ===============================
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    hospede_id INTEGER NOT NULL,
    quarto_numero INTEGER NOT NULL,

    data_entrada TEXT NOT NULL,   -- YYYY-MM-DD
    data_saida TEXT NOT NULL,     -- YYYY-MM-DD
    num_hospedes INTEGER NOT NULL,
    origem TEXT NOT NULL,
    estado TEXT NOT NULL,         -- PENDENTE, CONFIRMADA, CHECKIN, CHECKOUT, CANCELADA, NO_SHOW
    check_in_real TEXT,
    check_out_real TEXT,
    data_cancelamento TEXT,
    data_no_show TEXT,

    FOREIGN KEY (hospede_id) REFERENCES hospedes(id) ON DELETE CASCADE,
    FOREIGN KEY (quarto_numero) REFERENCES quartos(numero) ON DELETE CASCADE
);

-- INDEXES IMPORTANTES
CREATE INDEX IF NOT EXISTS idx_reservas_hospede ON reservas (hospede_id);
CREATE INDEX IF NOT EXISTS idx_reservas_quarto ON reservas (quarto_numero);
CREATE INDEX IF NOT EXISTS idx_reservas_entrada ON reservas (data_entrada);
CREATE INDEX IF NOT EXISTS idx_reservas_saida ON reservas (data_saida);

-- ===============================
-- TABELA: pagamentos
-- ===============================
CREATE TABLE IF NOT EXISTS pagamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    reserva_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    forma TEXT NOT NULL,                -- PIX, CRÉDITO, DÉBITO, DINHEIRO
    data_pagamento TEXT NOT NULL,       -- YYYY-MM-DD

    FOREIGN KEY (reserva_id) REFERENCES reservas(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_pag_reserva ON pagamentos (reserva_id);

-- ===============================
-- TABELA: adicionais (ex: frigobar, estacionamento)
-- ===============================
CREATE TABLE IF NOT EXISTS adicionais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    reserva_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,

    FOREIGN KEY (reserva_id) REFERENCES reservas(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_adc_reserva ON adicionais (reserva_id);

-- ===============================
-- (OPCIONAL) Histórico de ações
-- ===============================
CREATE TABLE IF NOT EXISTS historico_reserva (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reserva_id INTEGER NOT NULL,
    evento TEXT NOT NULL,
    data_registro TEXT NOT NULL,

    FOREIGN KEY (reserva_id) REFERENCES reservas(id) ON DELETE CASCADE
);



-- ===============================
-- VIEW: reserva_completa
-- ===============================
CREATE VIEW IF NOT EXISTS vw_reservas_completas AS
SELECT
    r.id AS reserva_id,

    -- hóspede
    h.id AS hospede_id,
    h.nome AS hospede_nome,
    h.documento AS hospede_documento,
    h.email AS hospede_email,
    h.telefone AS hospede_telefone,

    -- quarto
    q.numero AS quarto_numero,
    q.tipo AS quarto_tipo,
    q.capacidade AS quarto_capacidade,
    q.tarifa_base AS quarto_tarifa_base,

    -- reserva
    r.data_entrada,
    r.data_saida,
    r.num_hospedes,
    r.origem,
    r.estado,
    r.check_in_real,
    r.check_out_real,
    r.data_cancelamento,
    r.data_no_show,

    -- totais (subqueries)
    COALESCE((
        SELECT SUM(valor)
        FROM pagamentos p
        WHERE p.reserva_id = r.id
    ), 0) AS total_pago,

    COALESCE((
        SELECT SUM(valor)
        FROM adicionais a
        WHERE a.reserva_id = r.id
    ), 0) AS total_adicionais

FROM reservas r
JOIN hospedes h ON h.id = r.hospede_id
JOIN quartos q ON q.numero = r.quarto_numero;
