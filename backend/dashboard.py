from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard



class CustomIndexDashboard(Dashboard):
    columns = 3
    exclude_list=['Category']

    def init_with_context(self, context):
        print(modules.AppList)
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('auth.*','Category'),
            column=0,
            order=0
        ))

        pass
        # self.children.append(modules.AppList(
        #     _('Applications'),
        #     exclude=('auth.*','category'),
        #     column=0,
        #     order=0
        # ))
    


    