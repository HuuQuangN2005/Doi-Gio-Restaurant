from restaurant import app
from restaurant.models import db
from flask_admin.theme import Bootstrap4Theme
from flask_admin.contrib.sqla import ModelView
from restaurant.models.sql import Food, Category
from flask import url_for

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView


from flask_admin import Admin, AdminIndexView


class MyAdminIndex(AdminIndexView):
    @expose("/")
    def index(self):
        # tạo list menu items
        menu = []


        for v in self.admin._views:
            if v.is_visible():
        # build URL đúng
                try:
                    url = url_for(f"{v.endpoint}.index")
                except:
                    url = "#"

            menu.append({"name": v.name, "url": url})
        
        return self.render('admin/master.html', admin_menu=menu)

admin = Admin(app, name="MyAdmin", index_view=MyAdminIndex())

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Food, db.session))