Django Mangle
=============

Put your static assets through the wringer.


How it works
------------

Mangle works by adding a post-processing pipeline to your chosen file storage, allowing you to configure Manglers to reshape your assets.

Quickstart
----------

1. Create your custom storage backend, using the mixin

    ```
    from django.contrib.staticfiles.storage import StaticFilesStorage
    import mangle

    class CustomStorage(mangle.ManglerMixin, StaticFilesStorage):
        pass
```

1. Add storage setting

    ```
    STATICFILES_STORAGE='mysite.storage.CustomStorage'
    ```

1. Configure manglers

    ```
    MANGLERS=[
        ('mangle.css.CssMangler', {}),
        ('mangle.js.JsMangler', {}),
        ('mangle.gzip.GzipMangler', {'extensions': ['.css', '.js', '.txt']}),
    ]
    ```

1. Run `manage.py collectstatic`
