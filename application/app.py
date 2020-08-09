from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes

# TODO: lisää groups.db rajoitukset ja aihe?
# TODO: omat chätit: osa viimeisintä viestiä ja sen kellon aika (tai pvämäärä)
# TODO: uudet chätit: nimi ja kuvaus ja osallistujien määrä n/x
# TODO: mahdollisuus piilottaa chatit?
# TODO: search toimii ilman napin painallusta

#todo: scroll chattiin

#TODO: eriväriset viestit riippuen lägettäjästä