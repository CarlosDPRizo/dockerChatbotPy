CREATE TABLE IF NOT EXISTS usuario(
	pk_usu_cpf varchar(14) not null primary key,
	nome varchar(100) not null
);

CREATE TABLE IF NOT EXISTS occurrence(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	protocol VARCHAR(10) NOT NULL,
    data varchar(10) NOT NULL,
    fk_usu_cpf varchar(14) NOT NULL,
	veiculo VARCHAR(50) NOT NULL,
	placa VARCHAR(10) NOT NULL,
    constraint fk_usuario_occ foreign key(fk_usu_cpf) references usuario(pk_usu_cpf)
);

CREATE TABLE IF NOT EXISTS info(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(100) NOT NULL,
	descricao VARCHAR(200) NOT NULL,
	status VARCHAR(100) NOT NULL,
	urlImagem VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS info_occurrence(
	fk_occ_id int not null,
	fk_info_id int not null,
	constraint fk_occurence foreign key(fk_occ_id) references occurrence(id),
	constraint fk_info foreign key(fk_info_id) references info(id)
);

CREATE TABLE IF NOT EXISTS log_info(
	fk_info_id int not null,
    fk_usu_cpf varchar(14) NOT NULL,
    data varchar(10) NOT NULL,
	constraint fk_info_log foreign key(fk_info_id) references info(id),
    constraint fk_usuario_log foreign key(fk_usu_cpf) references usuario(pk_usu_cpf)
);

INSERT INTO chatbot.usuario (pk_usu_cpf, nome)
	VALUES ('111.111.111-11', 'Carlos');

INSERT INTO chatbot.occurrence (id, protocol, `data`, fk_usu_cpf, veiculo, placa)
	VALUES (1, '2025-04-26', '26/04/2025', '111.111.111-11', 'VW - VOLKSWAGEM - FOX 1.6 - 2005', 'FOX1I97');

INSERT INTO chatbot.info (id, nome, descricao, status, urlImagem)
	VALUES (1, 'Pagamento', 'Data agendada para pagamento', '30/04/2025', 'https://img.icons8.com/?size=100&id=215&format=png&color=000000'),
		(2, 'Agendamento', 'Data de agendamento para entrada do veículo', '27/04/2025', 'https://img.icons8.com/?size=100&id=eJ0GpkPbhocR&format=png&color=000000'),
		(3, 'Saída', 'Data de saída agendada do veículo', '30/04/2025', 'https://img.icons8.com/?size=100&id=24337&format=png&color=000000'),
		(4, 'Andamento', 'Andamento do processo', 'Aguardando reparos', 'https://img.icons8.com/?size=100&id=39323&format=png&color=000000'),
		(5, 'Responsável', 'Responsável pela ocorrência', 'Unidade Estacionamento 01', 'https://img.icons8.com/?size=100&id=JEOwyGQw7evS&format=png&color=000000'),
		(6, 'Agendamento', 'Data de agendamento para entrada do veículo', '', 'https://img.icons8.com/?size=100&id=eJ0GpkPbhocR&format=png&color=000000');

INSERT INTO chatbot.info_occurrence (fk_occ_id, fk_info_id)
	VALUES (1, 1),
		(1, 2),
		(1, 3),
		(1, 4),
		(1, 5);