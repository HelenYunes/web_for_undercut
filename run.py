
from web_for_undercut import app
import os

if __name__ == '__main__':

    app.run(debug=bool(os.getenv("DEBUG_MODE", default=False)))