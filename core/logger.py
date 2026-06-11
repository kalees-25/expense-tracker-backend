import logging
import os


# ---------------- CREATE LOGS DIRECTORY ----------------

os.makedirs("logs", exist_ok=True)


# ---------------- LOGGER CONFIGURATION ----------------

logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        
        "%(levelname)s | "
        
        "%(name)s | "
        
        "%(message)s"
    ),
   
   
#    HANDLERS ->WHERE LOGS SHOULD GO
    handlers=[

        # FILE HANDLER -> STORE LOGS INSIDE FILE
        logging.FileHandler(
            "logs/app.log",
            encoding="utf-8"
        ),

        # STREAM HANDLER -> SHOE LOGS IN CONSOLE 
        logging.StreamHandler()
    ]
)


# ---------------- LOGGER OBJECT ----------------

logger = logging.getLogger(__name__)     #(__name__) -> CURRENT MODULE NAME