from django.contrib.staticfiles.finders import AppDirectoriesFinder


class NpmFreeAppDirectoriesFinder(AppDirectoriesFinder):
    '''
    A finder for app directories that automatically adds
    node_modules to the list of files not to list.

    node_modules can be huge (>11000 files), will never be served and
    slows down finder.list() to a crawl. Usually this is not bad, but
    django-debug-toolbar calls list() for every page view, so it can
    easily add 10 Seconds to each page reload.
    '''

    def list(self, ignore_pattern):
        if ignore_pattern is None:
            ignore_pattern = []
        ignore_pattern.append('node_modules')
        return super(NpmFreeAppDirectoriesFinder, self).list(ignore_pattern)
