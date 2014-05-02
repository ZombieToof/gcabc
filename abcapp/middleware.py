from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django_phpBB3.models import Config as PhpbbConfig
from django_phpBB3.models import Session as PhpbbSession

from abcapp.models import Player


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = _get_user_via_phpbb_session(request)
    return request._cached_user


def _get_user_via_phpbb_session(request):
    cookie_name = PhpbbConfig.objects.filter(
        id='cookie_name')[0].config_value
    session_id = request.COOKIES.get('%s_sid' % cookie_name)
    if not session_id:
        return
    sessions = PhpbbSession.objects.filter(id=session_id)
    if not sessions:
        return
    session = sessions[0]
    # FIXME: do the magic validation stuff to make sure the
    # session is still valid

    phpbb_user = session.session_user

    # make sure we have a Player and django User object
    player = None
    try:
        player = phpbb_user.player
    except ObjectDoesNotExist:
        with transaction.atomic():
            django_username = 'phpbb_%s' % phpbb_user.id
            print 'create django user'
            django_user = User.objects.get_or_create(
                username=django_username)[0]
            print 'create player'
            player = Player.objects.get_or_create(
                phpbb_user=phpbb_user,
                django_user=django_user)[0]
            print player
    if player is None:
        return

    # brute force: sync important data to the django user
    django_user = player.django_user
    first_name = phpbb_user.username[:30]  # size limit of auth.User
    if django_user.first_name != first_name:
        django_user.first_name = first_name
    email = phpbb_user.email
    if django_user.email != email:
        django_user.email = email
    return django_user


class PhpbbAuthenticationMiddleware(object):
    def process_request(self, request):
        request.user = get_user(request)
