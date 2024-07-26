from django.views.generic import TemplateView

class ReleasesView(TemplateView):
    template_name = 'drink/releases.html'
    
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubmitDrinkView(TemplateView):
    template_name = 'drink/submitdrink.html'
    
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ReviewDrinkView(TemplateView):
    template_name = 'drink/reviewdrink.html'
    
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
