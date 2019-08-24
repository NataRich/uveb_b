# /uveb/resources/__init__.py
from .. import app, mail
from ..controllers.db.fetchers import UserFetcher, VideoFetcher, TagFetcher
from ..controllers.db.adders import UserAdder, VideoAdder, TagAdder
from ..controllers.db.updaters import UserUpdater, VideoUpdater
from ..controllers.db.deleters import UserDeleter, VideoDeleter