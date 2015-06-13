import sae
from views import app
import dbinit

application = sae.create_wsgi_app(app)