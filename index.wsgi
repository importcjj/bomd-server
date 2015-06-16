import sae
from views import app
import Tools.dbinit

application = sae.create_wsgi_app(app)