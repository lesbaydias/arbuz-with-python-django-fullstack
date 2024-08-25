from django.contrib import admin

from landing.models import ItemTable, UsersTable, BasketItem, PurchaseItem, Purchase

admin.site.register(ItemTable)
admin.site.register(BasketItem)
admin.site.register(UsersTable)
admin.site.register(PurchaseItem)
admin.site.register(Purchase)
