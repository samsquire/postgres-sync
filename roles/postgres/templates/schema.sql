drop database if exists app;
create database app;
\connect app;
create table table1 (
	id SERIAL,
	data varchar(128)
);

create table table2 (
	id SERIAL,
	data varchar(128)
);

create table table3 (
	id SERIAL,
	data varchar(128)
);

create table versions (
	id SERIAL,
	row_number int,
	column_number int,
	item_number int,
	hash text,
	timestamp int,
	version int,
	table_name text,
	column_name text
);

insert into table1 (data) values ('One');
insert into table2 (data) values ('One');
insert into table3 (data) values ('One');
