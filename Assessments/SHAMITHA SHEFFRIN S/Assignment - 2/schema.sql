--SQL_SCHEMA_PREPARED_BY_DB2


--Table_Creation

create table if not exists user(username varchar(32) null,rollno int null,email varchar(32) null,password varchar(16) null);


--Inserting_into_table

insert into user values
('shagish',312323,'962219104095@gmail.com','helloworld'),
('benoj',342334,'962219205017@gmail.com','hellobruh'),
('shami',626327,'962219104097@gmail.com','hellodood')
('Shahina',897343,'962219104098@gmail.com','haihai')
('sreeja',897234,'962219104109@gmail.com','hihihi');


--Updating_Table_Values

update user set password='hellohi' where username='shagish';


--Deleting_table_rows

delete from user where username='benoj';
