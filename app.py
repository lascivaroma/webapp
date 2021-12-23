import os
import logging
from flask import Flask


logger = logging.getLogger()

from .models.corpus import Excerpt, STORAGE, INDEX_DIR, INDEX_NAME


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(ROOT_DIR, "assets"),
    template_folder=os.path.join(ROOT_DIR, "templates")
)

if not os.path.exists(INDEX_DIR):
    logging.warn(f"Creating directory for Index as it was not found ({INDEX_DIR})")
    ix = STORAGE.create()
    logging.warn(f"Creating the Index")
    ix = STORAGE.create_index(Excerpt)


index = STORAGE.open_index(schema=Excerpt)


from . import filters
from .routes import main
from .cli import *
