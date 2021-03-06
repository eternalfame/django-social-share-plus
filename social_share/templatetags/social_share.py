# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.contrib.sites.models import Site
from django.db.models import Model
from django.template.defaultfilters import urlencode

try:
    from django_bitly.templatetags.bitly import bitlify
    DJANGO_BITLY = True
except ImportError:
    DJANGO_BITLY = False


register = template.Library()


TWITTER_ENDPOINT = 'http://twitter.com/intent/tweet?text=%s'
FACEBOOK_ENDPOINT = 'http://www.facebook.com/sharer/sharer.php?u=%s'
GPLUS_ENDPOINT = 'http://plus.google.com/share?url=%s'
VK_ENDPOINT = 'http://vk.com/share.php?url=%s'
OK_ENDPOINT = "http://www.odnoklassniki.ru/dk?st.cmd=addShare&st.s=1&st._surl=%s"
MAILRU_ENDPOINT = "http://connect.mail.ru/share?url=%s"


def compile_text(context, text):
    ctx = template.context.Context(context)
    return template.Template(text).render(ctx)


class MockRequest(object):
    @staticmethod
    def build_absolute_uri(relative_url):
        if relative_url.startswith('http'):
            return relative_url
        current_site = Site.objects.get_current()
        return '%s%s' % (current_site.domain, relative_url)


def __build_url(request, obj_or_url):
    if obj_or_url is not None:
        if isinstance(obj_or_url, Model):
            if DJANGO_BITLY:
                return bitlify(obj_or_url)
            else:
                return request.build_absolute_uri(obj_or_url.get_absolute_url())
        else:
            return request.build_absolute_uri(obj_or_url)
    return ''


def _build_url(request, obj_or_url):
    return __build_url(request, obj_or_url).replace("127.0.0.1:8111", "msb.khabkrai.ru")


def _compose_tweet(text, url=None):
    if url is None:
        url = ''
    total_lenght = len(text) + len(' ') + len(url)
    if total_lenght > 140:
        truncated_text = text[:(140 - len(url))] + "…"
    else:
        truncated_text = text
    return "%s %s" % (truncated_text, url)


@register.simple_tag(takes_context=True)
def post_to_twitter_url(context, text, obj_or_url=None):
    text = compile_text(context, text)
    request = context.get('request', MockRequest())

    url = _build_url(request, obj_or_url)

    tweet = _compose_tweet(text, url)
    context['tweet_url'] = TWITTER_ENDPOINT % urlencode(tweet)
    return context


@register.inclusion_tag('social_share/templatetags/post_to_twitter.html', takes_context=True)
def post_to_twitter(context, text, obj_or_url=None, link_text='Post to Twitter'):
    context = post_to_twitter_url(context, text, obj_or_url)

    request = context.get('request', MockRequest())
    url = _build_url(request, obj_or_url)
    tweet = _compose_tweet(text, url)

    context['link_text'] = link_text
    context['full_text'] = tweet
    return context


@register.simple_tag(takes_context=True)
def post_to_facebook_url(context, obj_or_url=None):
    request = context.get('request', MockRequest())
    url = _build_url(request, obj_or_url)
    context['facebook_url'] = FACEBOOK_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('social_share/templatetags/post_to_facebook.html', takes_context=True)
def post_to_facebook(context, obj_or_url=None, link_text='Post to Facebook'):
    context = post_to_facebook_url(context, obj_or_url)
    context['link_text'] = link_text
    return context


@register.simple_tag(takes_context=True)
def post_to_gplus_url(context, obj_or_url=None):
    request = context.get('request', MockRequest())
    url = _build_url(request, obj_or_url)
    context['gplus_url'] = GPLUS_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('social_share/templatetags/post_to_gplus.html', takes_context=True)
def post_to_gplus(context, obj_or_url=None, link_text='Post to Google+'):
    context = post_to_gplus_url(context, obj_or_url)
    context['link_text'] = link_text
    return context


@register.simple_tag(takes_context=True)
def post_to_vk_url(context, obj_or_url=None):
    request = context.get('request', MockRequest())
    url = _build_url(request, obj_or_url)
    context['vk_url'] = VK_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('social_share/templatetags/post_to_vk.html', takes_context=True)
def post_to_vk(context, obj_or_url=None, link_text='Post to VK'):
    context = post_to_vk_url(context, obj_or_url)
    context['link_text'] = link_text
    return context


@register.simple_tag(takes_context=True)
def post_to_ok_url(context, obj_or_url=None):
    request = context.get('request', MockRequest())
    url = _build_url(request, obj_or_url)
    context['ok_url'] = OK_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('social_share/templatetags/post_to_ok.html', takes_context=True)
def post_to_ok(context, obj_or_url=None, link_text='Post to OK'):
    context = post_to_ok_url(context, obj_or_url)
    context['link_text'] = link_text
    return context


@register.simple_tag(takes_context=True)
def post_to_mailru_url(context, obj_or_url=None):
    request = context.get('request', MockRequest())
    url = _build_url(request, obj_or_url)
    context['mailru_url'] = MAILRU_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('social_share/templatetags/post_to_mailru.html', takes_context=True)
def post_to_mailru(context, obj_or_url=None, link_text='Post to Mail.ru'):
    context = post_to_mailru_url(context, obj_or_url)
    context['link_text'] = link_text
    return context
