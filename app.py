import os
from flask import Flask

from models.corpus import Excerpt, STORAGE


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(ROOT_DIR, "assets"),
    template_folder=os.path.join(ROOT_DIR, "templates")
)
index = STORAGE.open_index(schema=Excerpt)
import routes.main
