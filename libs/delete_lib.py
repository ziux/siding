

def delete_queryset(queryset,using=False):
    for query in queryset:
        res = query.df_delete(using)
        if res:
            return res
    return False

def delete_instance(instance):
    instance.df = 1
    instance.save()
