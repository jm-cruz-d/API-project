CREATE TABLE IF NOT EXISTS users (
  idUser INT NOT NULL, 
  userName VARCHAR(45) NOT NULL,
  PRIMARY KEY (idUser));
CREATE TABLE IF NOT EXISTS chats (
  idChat INT NOT NULL,
  PRIMARY KEY (idChat));
CREATE TABLE IF NOT EXISTS messages (
  idMessage INT NOT NULL,
  text VARCHAR(120) NULL,
  datetime VARCHAR(45) NULL,
  users_idUser INT NOT NULL,
  chats_idChat INT NOT NULL,
  PRIMARY KEY (idMessage),
    FOREIGN KEY (users_idUser)
    REFERENCES users (idUser)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Message_chats1
    FOREIGN KEY (chats_idChat)
    REFERENCES chats (idChat)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)