from django.contrib import admin
from django.db import router
from users.models import User
from simple_history.admin import SimpleHistoryAdmin


admin.site.register(User, SimpleHistoryAdmin)
