# coding=utf-8

from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, get_language_info
from django.core.urlresolvers import reverse


class TrumbowygWidget(Textarea):
    class Media:
        css = {
            'all': (
                'fs_trumbowyg/trumbowyg/design/css/trumbowyg.css',
                'fs_trumbowyg/css/trumbowyg.css',
            )
        }
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
            'fs_trumbowyg/trumbowyg/trumbowyg.min.js',
            'fs_trumbowyg/trumbowyg/langs/ru.js',
            'fs_trumbowyg/js/trumbowyg.upload.js',
            'fs_trumbowyg/js/trumbowyg.video.js',
        )

    def render(self, name, value, attrs=None):
        output = super(TrumbowygWidget, self).render(name, value, attrs)
        script = u'''
            <script>
                $("#id_%s").trumbowyg({
                    lang: "%s",
                    semantic: true,
                    resetCss: true,
                    autogrow: true,
                    btns: [
                        "formatting",
                        "|", $.trumbowyg.btnsGrps.design,
                        "|", "link",
                        "|", "upload", "video",
                        "|", $.trumbowyg.btnsGrps.justify,
                        "|", $.trumbowyg.btnsGrps.lists,
                        "|", "horizontalRule",
                        "|", "viewHTML"
                    ],
                    uploadUrl: "%s"
                });
            </script>
        ''' % (name, get_language_info(get_language())['code'], reverse('trumbowyg_upload_image'))
        output += mark_safe(script)
        return output
