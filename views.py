from django.views.generic import TemplateView
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model


class UserView(TemplateView):
    template_name = 'user_xmlapi.xml'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        
        User = get_user_model()
        cookie_value = kwargs['cookie_value']
        try:
            session = Session.objects.get(session_key=cookie_value)
            user = User.objects.get(id=session.get_decoded()['_auth_user_id'])
        except Session.DoesNotExist:
            user = None

        if user:
            context['requested_user'] = user

        return context

