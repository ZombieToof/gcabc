from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from abcapp.models import Campaign


def index(request):
    campaigns = Campaign.objects.all()
    template = loader.get_template('campaigns/index.html')
    context = RequestContext(request, {
        'campaigns': campaigns
    })
    return HttpResponse(template.render(context))

