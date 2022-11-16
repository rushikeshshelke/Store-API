class GlobalVariables:

    APP_CONFIG_PATH = "./configs"
    APP_LOGS_PATH = "./logs"

    APP_DOCS_PATH = "/static"

    LOGGER = None

    CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
    INSERT_INTO_USERS = "INSERT INTO users values(NULL,?,?)"
    SELECT_USERS_BY_UNAME = "SELECT * FROM users WHERE username=?"
    SELECT_USERS_BY_UID = "SELECT * FROM users WHERE id=?"

    CREATE_ITEMS_TABLE = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
    INSERT_INTO_ITEMS = "INSERT INTO items values(?,?)"
    SELECT_ITEM_BY_NAME = "SELECT * FROM items WHERE name=?"
    SELECT_ITEMS = "SELECT * FROM items"
    DELETE_ITEM = "DELETE FROM items WHERE name=?"
    UPDATE_IETM = "UPDATE items SET price=? WHERE name=?"

    ADMIN_USER = 1

    BLACK_LIST = set()