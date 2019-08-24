# /uveb/resources/__init__.py
from .. import app, mail
from ..models.user import UserModel
from ..models.video import VideoModel
from ..models.tag import TagModel
from ..controllers.auth.mails import SendMail
from ..controllers.auth.validate import Validate
from ..controllers.db.fetchers import UserFetcher, VideoFetcher, TagFetcher
from ..controllers.db.adders import UserAdder, VideoAdder, TagAdder
from ..controllers.db.updaters import UserUpdater, VideoUpdater
from ..controllers.db.deleters import UserDeleter, VideoDeleter
from ..utility.utils import gen_code