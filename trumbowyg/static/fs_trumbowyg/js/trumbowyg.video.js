(function($) {
    $.extend(true, $.trumbowyg, {
        langs: {
            en: {
                video: "Insert Video",
                embedCode: "Embed Code"
            },
            ru: {
                video: "Вставить видео",
                embedCode: "Код для вставки"
            }
        },

        opts: {
            btnsDef: {
                video: {
                    func: function(params, tbw) {
                        tbw.saveSelection();
                        tbw.openModalInsert(
                            // Title
                            tbw.lang['video'],

                            // Fields
                            {
                                code: {
                                    label: tbw.lang['embedCode'],
                                    required: true
                                }
                            },

                            // Callback
                            function(values, fields) {
                                tbw.execCommand('insertHTML', values["code"]);
                                return true;
                            }
                        );
                    }
                }
            }
        }
    });
})(jQuery);
