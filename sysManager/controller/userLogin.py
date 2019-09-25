# -*- coding: utf-8 -*-
from config.app import login_manager
from sysManager.models.models import Users


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))