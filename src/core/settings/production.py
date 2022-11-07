import os
from .base import *

# For security and performance reasons, DEBUG is turned off
DEBUG = env.bool("DEBUG", default=False)

# Webpack
WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "dist/",
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}
