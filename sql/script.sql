-- crear la base de datos
create database todo_app;
go

-- usar la base de datos
use todo_app;
go

-- tabla de usuarios
create table users (
  id int identity(1,1) primary key,
  username varchar(50) not null unique,
  password varchar(255) not null,
  email varchar(100) not null unique,
  created_at datetime default getdate()
);
go

-- tabla de tareas
create table tasks (
  id int identity(1,1) primary key,
  user_id int not null,
  title varchar(100) not null,
  description text,
  completed bit default 0,
  created_at datetime default getdate(),
  updated_at datetime default getdate(),
  foreign key (user_id) references users(id)
    on delete cascade
    on update cascade
);
go
