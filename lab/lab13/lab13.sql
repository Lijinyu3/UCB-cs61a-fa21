.read data.sql


CREATE TABLE bluedog AS
  SELECT color, pet
    FROM students
    WHERE color = "blue" AND pet = "dog";

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song
    FROM students
    WHERE color = "blue" AND pet = "dog";


CREATE TABLE smallest_int_having AS
  SELECT time, smallest
    FROM students
    GROUP BY smallest
    HAVING COUNT(*) = 1;


CREATE TABLE matchmaker AS
  SELECT a_stu.pet, a_stu.song, a_stu.color, b_stu.color
    FROM students as a_stu, students as b_stu
    WHERE a_stu.pet = b_stu.pet AND a_stu.song = b_stu.song AND a_stu.time < b_stu.time;


CREATE TABLE sevens AS
  SELECT seven
    FROM students, numbers
    WHERE students.time = numbers.time AND number = 7 AND numbers.'7' = "True";


CREATE TABLE avg_difference AS
  SELECT ROUND(AVG(ABS(number - smallest)))
    FROM students;

