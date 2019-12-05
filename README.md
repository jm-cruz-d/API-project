# API-project

**Description:** You want to analyze the `public` chat messages (like slack public channels) of your team and create sentiment metrics of the different people on your team. The goal of this project is to analyze the conversations of your team to ensure they are happy 😃.

**Main goal**: Analyze the conversations coming from a chat like `slack`

- This project is an API in bottle just to store chat messages in a mysql database.
- Extract sentiment from chat messages included in database.
- Recommend friends to a user based on the contents from chat `documents` using a recommender system with `NLP` analysis. (Almost done in visual, but complitly in Jupyter Notebook)

## API functions

- (GET) `/Users/` 
  - **Purpose:** Get all users
  - **Returns:** `user_id` and `username`

- (GET) `/Users/<idUser>` 
  - **Purpose:** Get messages from idUser
  - **Params:** `idUser` the idUser number
  - **Returns:** `user_id`

- (POST) `/user/create` 
  - **Purpose:** Create a user and save into DB
  - **Params:** `username` the user name
  - **Returns:** `user_id`

- (POST) `/chat/create` 
  - **Purpose:** Create a conversation to load messages
  - **Params:** An array of users ids `[user_id]`
  - **Returns:** `chat_id`

- (POST) `/chat/<chat_id>/addmessage` 
  - **Purpose:** Add a message to the conversation. Help: Before adding the chat message to the database, check that the incoming user is part of this chat id. If not, raise an exception.
  - **Params:**
    - `chat_id`: Chat to store message
    - `user_id`: the user that writes the message
    - `text`: Message text
  - **Returns:** `message_id`  

- (GET) `/chat/<chat_id>/list` 
  - **Purpose:** Get all messages from `chat_id`
  - **Returns:** json array with all messages from this `chat_id`

- (GET) `/chat/<chat_id>/sentiment` 
  - **Purpose:** Analyze messages from `chat_id`. Use `NLTK` sentiment analysis package for this task
  - **Returns:** json with all sentiments from messages in the chat

- (GET) `/message/<idUser>` 
  - **Purpose:** Get messages from idUser and userName
  - **Params:** `idUser` the idUser number
  - **Returns:** dictionary with userName and all messages from each.


(IN PROCESS)
- (GET) `/recommend/<name>`  
  - **Purpose:** Recommend friend to this user based on chat contents
  - **Returns:** json array with top 3 similar users




