import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, nmodel, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        if nmodel == "field_master":
            slug = slugify(instance.field_master_name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).first()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, nmodel, new_slug=new_slug)
    return slug


def unique_slug_generator_meta_tag(instance, nmodel, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        if nmodel == "meta_tag":
            slug = slugify(instance.page)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(page_url=slug).first()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator_meta_tag(instance, nmodel, new_slug=new_slug)
    return slug
