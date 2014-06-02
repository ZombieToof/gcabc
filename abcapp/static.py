from django.contrib.staticfiles.finders import AppDirectoriesFinder


class NpmFreeAppDirectoriesFinder(AppDirectoriesFinder):

    def list(self, ignore_pattern):
        if ignore_pattern is None:
            ignore_pattern = []
        ignore_pattern.append('node_modules')
        return super(NpmFreeAppDirectoriesFinder, self).list(ignore_pattern)
