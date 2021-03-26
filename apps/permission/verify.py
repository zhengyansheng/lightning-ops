import os

import casbin
from django.conf import settings

from .adapter import DjangoAdapter
from .models import PermRule, RoleBind


def verify_permission(*args):
    # username, path, method
    adapter = DjangoAdapter(PermRule, RoleBind)
    model_conf_file = os.path.join(settings.ROOT_DIR, "config", "keymatch_model.conf")
    e = casbin.Enforcer(model_conf_file, adapter=adapter)
    return e.enforce(*args)