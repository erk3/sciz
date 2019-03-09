CREATE TABLE sciz (
  room INTEGER references room(id),
  url VARCHAR(255),
  jwt VARCHAR(255),
  PRIMARY KEY(room)
);
