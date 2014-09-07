drop table if exists runners;
create table runners(
  id INTEGER primary key autoincrement,
  venue TEXT not NULL,
  course INTEGER,
  last_known INTEGER not NULL,
  start_time TEXT,
  end_time TEXT
);
