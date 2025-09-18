

class QueryParamsMixin :
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        querydict = self.request.GET.copy()
        if 'page' in querydict :
            querydict.pop('page')
        context['querystring'] = querydict.urlencode()
        return context







