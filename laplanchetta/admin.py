from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path


@staff_member_required
def admin_statistics_view(request):
    return render(request, 'utils/statistics.html', {
        'title': 'Estadisticas'
    })

@staff_member_required
def admin_etiquetas_view(request):
    return render(request, 'utils/etiquetas.html', {
        'title': 'Etiquetas'
    })


class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        try:
            group = request.user.groups.all()[0].name
        except:
            group = None

        app_list = super().get_app_list(request)
        print(app_list)
        for app in app_list:
            if app['name'] == 'Envio':
                print('APP:', app)
                app['models'].append(
                    {
                        'name': 'Etiquetas por cantidad',
                        'object_name': 'EtiquetasPorCantidad',
                        'admin_url': '/etiquetas',
                        #'view_only': False,
                        'view_on_site': True,
                        #'perms': {'view': True},
                        
                    }
                )
               
        # We can exclude a group here.
        if group == None:
            
            app_list += [
                {
                    'name': 'Analytics',
                    'app_label': 'Analytics',
                    'models': [
                        {
                            'name': 'Estadisticas',
                            'object_name': 'statistics',
                            'admin_url': '/statistics',
                            'view_only': True,
                        },
                        {
                            'name': 'Google Analytics',
                            'object_name': 'analytics',
                            'admin_url': 'https://analytics.google.com/analytics/web/#/p285317399/reports/reportinghub',
                            'view_only': True,
                           
                        } 
                    ]
                },
            ]
        
        return app_list

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('statistics/', admin_statistics_view, name='admin-statistics'),
            path('etiquetas/', admin_etiquetas_view, name='admin-etiquetas'),
        ]
        return urls
