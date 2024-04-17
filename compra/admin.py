from django.contrib import admin
from .models import Compra, OrderItem


class CompraAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'fecha_compra', 'status', 'transaction_id', 'medio_de_pago', 'total', 'completada']
    ordering = ['fecha_compra']
    #change_form_template = "compra/compra_changeform.html"
    list_filter = ('cliente', 'fecha_compra', 'completada', 'status')
    search_fields = ("cliente__email__startswith", )
    #readonly_fields =('cliente', 'fecha_compra', 'status', 'medio_de_pago', 'transaction_id', 'total')
    #exclude = ('completada',)

    def get_list_display(self, request):

        list_display = super().get_list_display(request)

        try:
            group = request.user.groups.all()[0].name
        except:
            group = None

        if group == 'CABA' or group == 'BARILOCHE':
            return ['cliente', 'fecha_compra', 'status', 'completada']
        else:
            return list_display


    def get_queryset(self, request):

        qs = super().get_queryset(request)

        try:
            group = request.user.groups.all()[0].name
        except:
            group = None

        if group == 'CABA':
            for x in qs.filter(correo='CABA', completada=False):
                print('QUERY:', x)
            return qs.filter(correo='CABA', completada=False)
        elif group == 'BARILOCHE':
            return qs.filter(correo='BARILOCHE', completada=False)
        else:
            return qs.exclude(status=None)
    

    def get_form(self, request, obj=None, **kwargs):
        """Override the get_form and extend the 'exclude' keyword arg"""
        try:
            group = request.user.groups.all()[0].name
        except:
            group = None
        
        if group == 'CABA' or group == 'BARILOCHE':
            if obj:
                kwargs.update({
                    'exclude': getattr(kwargs, 'exclude', tuple()) + (
                        'medio_de_pago',
                        'transaction_id',
                        'fecha_compra',
                        'total',
                        'descuento',
                        'correo'
                    ),
                })
        return super(CompraAdmin, self).get_form(request, obj, **kwargs)


    '''
    def change_view(self, request, object_id=None, form_url='',extra_context=None):
        qs = Compra.objects.filter(id=object_id).first()
        print('obj_id:',qs.numero_de_retiro)
        is_super =  request.user.is_superuser

        if qs.numero_de_retiro != '0':
           template_response = super().change_view(request, object_id, form_url,
                                                extra_context)
        else:
            # get the default template response
            template_response = super().change_view(request, object_id, form_url,
                                                extra_context)
            # here we simply hide the div that contains the save and delete buttons
            template_response.content = template_response.rendered_content.replace(
            '<div class="row-extra">',
            '<div class="row-extra" style="display: none">')
        return template_response

    '''

admin.site.register(Compra, CompraAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['producto', 'compra', 'quantity', 'fecha_added']
    ordering = ['fecha_added']

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        
        try:
            group = request.user.groups.all()[0].name
        except:
            group = None

        if group == 'CABA':
            return qs.filter(compra__correo='CABA', compra__completada=False)
        elif group == 'BARILOCHE':
            return qs.filter(compra__correo='BARILOCHE', compra__completada=False)
        else:
            return qs


admin.site.register(OrderItem, OrderItemAdmin)


