-- crear la base de datos
create database if not exists todo_app;

-- usar la base de datos
use todo_app;

-- tabla de usuarios
create table users (
  id int auto_increment primary key,
  username varchar(50) not null unique,
  password varchar(255) not null,
  email varchar(100) not null unique,
  created_at timestamp default current_timestamp
);

-- tabla de tareas
create table tasks (
  id int auto_increment primary key,
  user_id int not null,
  title varchar(100) not null,
  description text,
  completed boolean default false,
  created_at timestamp default current_timestamp,
  updated_at timestamp default current_timestamp on update current_timestamp,
  foreign key (user_id) references users(id)
    on delete cascade
    on update cascade
);
