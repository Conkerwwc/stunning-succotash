
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);



-- Insert some data having issues with Alice Value
INSERT INTO employees (name) 
 VALUES 
 ('Alice'),
 ('Bob'), 
 ('Jose Perez'),
 ('Nimish Arvind'),
 ('Mark Hamill (The Joker & Luke Skywalker)'),
 ('Tech Chmpion'), 
 ('Jennfer Hale');              
SELECT * FROM employees;


-- 2. Add the new, empty column
ALTER TABLE employees
ADD COLUMN country VARCHAR(100);

-- 3. Update existing rows to populate the new column
# Ok if Dominican Republic id is 3 then Professor Nimish is from that Country 
# I must change it to United States
# Postgres Documentation (2025). UPDATE	SQL Commands. https://www.postgresql.org/docs/current/sql-update.html
UPDATE employees
SET country = v.country
FROM (
    VALUES
        (7, 'Dominican Republic'),
        (2, 'Afghanistan'),
        (1, 'Puerto Rico'),
        (4, 'United States'),
        (5, 'United States'),
        (6, 'Italy'),
        (3, 'United States')
) AS v(id, country)
WHERE employees.id = v.id;

-- 4. View the final result
SELECT * FROM employees;


-- 5. Add the new, empty column
ALTER TABLE employees
ADD COLUMN department_name VARCHAR(100);

-- 6. Update existing rows to populate the new column
UPDATE employees
SET department_name = v.department_name
FROM (
    VALUES
        (1, 'Data Analysts'),
        (2, 'Actors'),
        (3, 'HR'),
        (4, 'Actors'),
        (5, 'Sales'),
        (6, 'Sales')

) AS v(id, department_name)
WHERE employees.id = v.id;

-- 6. View the final result
SELECT * FROM employees;

ALTER TABLE employees
DROP COLUMN sales;


-- 7. Add the new, empty column
ALTER TABLE employees
ADD Column sales VARCHAR(100);

-- 8. Update existing rows to populate the new column: Gemini AI FLash Mistake here, however number 7 
-- was very useful because I forgot ALTER TABLE for some reason. 





ALTER TABLE employees
ADD COLUMN is_active BOOLEAN DEFAULT true;

UPDATE employees
SET is_active = false
WHERE name IN ('Alice', 'Bob ');

SELECT * FROM employees WHERE is_active = true;

SELECT * FROM employees;



DELETE FROM employees
WHERE name = 'Alice' OR name = 'Bob ';
# Flash AI reminding me about WHERE name IN, for some reason I forget IN again
DELETE FROM employees
WHERE name IN ('Alice', 'Bob ');
# |||||||||||Fixing extra rows from other Python Code added to the Table
# ||||||||||| Or Same Code that adds the same names or values.
DELETE FROM employees
WHERE id BETWEEN 37 AND 64; 


 SELECT * FROM  employees;
# Syntax error here * it should before FROM and this is still bad no id

#Fixing ALice 
UPDATE employees
SET department_id = 4
WHERE id = 39 AND name = 'Alice';

DELETE FROM employees
WHERE id = 39;

ALTER TABLE employees
ADD COLUMN sales_name VARCHAR(100);

UPDATE employees
SET sales_name = v.sales_name
FROM (
    VALUES
        ( 11, 'AKM Semiconductor Inc.'), -- error 140 to 179
        ( 12, '3M Co.'),
        ( 13, 'Asahi Glass Co Ltd.'),
        ( 14, 'Daikan Industries Ltd. '),
        ( 15, 'Dynacast International Inc.'),
        ( 16, 'Foster Electric Co. Ltd. '),
        ( 17, 'Murata Manufacturing Co. Ltd.')
) AS v(id, sales_name)
WHERE employees.id = v.id;



SELECT * FROM employees;


INSERT INTO employees (id, name, country)
VALUES
    ( 11, 'Joshua Iliya', 'Nigeria'),
    ( 12, 'Miguel Chaves Zamora', 'Cayman Islands'),
    ( 13, 'Willyn Eloro', 'Philippines'),
    ( 14, 'Yuosef Basher', 'United Arab Emirates'),
    ( 15, 'Zilas Ezhim', 'Nigeria'),
    ( 16, 'Muhammad Dayan Qayumi', 'Afghanistan'),
    ( 17, 'Elaha Osmani', 'Afghanistan'),
    (18, 'Diep Nguyem','Viet Nam'),
    (19, 'Jisham Ahmed', 'Germany'),
    (20, 'Hennadii Lysenko','Poland'),
    (21, 'Chidinnma Okeke', 'Switzerland'),
    (22, 'Ruan Kruger', 'South Africa'),
    (23, 'Austin Givens', 'United States'),
    (24, 'Larae Demorest', 'United States'),
    (25, 'Emmanuel Osazuwa', 'United Kingdom'),
    (26, 'Ismael Yahaya', 'Nigeria'),
    (27, 'Manukwem Manukwem', 'Nigeria'),
    (28, 'Arlene Deveaux', 'Turks and Caicos Islands'),
    (29, 'Anne Wachana', 'Kenya')
ON CONFLICT (id) DO NOTHING; -- W3 resource (December 31, 2024). Mastering PostgreSQL ON CONFLICT DO NOTHING
-- https://www.w3resource.com/PostgreSQL/snippets/postgres-on-conflict-do-nothing.php
--||||                          ||||

-- Prisma (N.D.). PostgreSQL / Inserting and modifying data
-- How to use `INSERT ON CONFLICT` to upsert data in PostgreSQL
--https://www.prisma.io/dataguide/postgresql/inserting-and-modifying-data/insert-on-conflict
-- ||||                                     ||||||||
UPDATE employees
SET sales_name = v.sales_name
FROM (
    VALUES
        ( 31, 'AKM Semiconductor Inc.'),  -- Updates same name
        ( 30, '3M Co.'),                   -- Updates same name
        ( 32, 'Asahi Glass Co Ltd.'),
        ( 33, 'Daikan Industries Ltd. '),
        ( 34, 'Dynacast International Inc.'),
        ( 35, 'Foster Electric Co. Ltd. '),
        ( 36, 'Murata Manufacturing Co. Ltd.')
) AS v(id, sales_name)
WHERE employees.id = v.id;

ALTER SEQUENCE employees_id_seq RESTART WITH 30;
-- Fixin error 209
--Postgres Documentation (2025).s https://www.postgresql.org/docs/current/sql-altersequence.html

ALTER TABLE employees
ADD COLUMN salary VARCHAR(100);
INSERT INTO employees (id, name, country, salary)
VALUES  ()