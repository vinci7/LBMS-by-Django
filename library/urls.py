from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'library.views.home'),
    url(r'^login', 'library.views.login'),
    url(r'^index', 'library.views.index'),
    url(r'^exit', 'library.views.exit'),

    url(r'^addbooks', 'library.views.addbooks'),
    url(r'^doaddbooks', 'library.views.doaddbooks'),
    url(r'^addbook', 'library.views.addbook'),
    url(r'^doaddbook', 'library.views.doaddbook'),

    url(r'^outbook', 'library.views.outbook'),
    url(r'^dooutbook', 'library.views.dooutbook'),
    url(r'^inbook', 'library.views.inbook'),
    url(r'^doinbook', 'library.views.doinbook'),

    url(r'^findbook', 'library.views.findbook'),
    url(r'^dofindbook', 'library.views.dofindbook'),
    
    url(r'^addcard', 'library.views.addcard'),
    url(r'^doaddcard', 'library.views.doaddcard'),

    url(r'^showcard', 'library.views.showcard'),
    url(r'^deletecard', 'library.views.deletecard'),
    
)
