from django.utils.decorators import method_decorator
from django.contrib import messages


class DeleteMessageMixin(object):
    """supplements django SuccessMessageMixin with message on successful object deletion."""
    delete_message = ''

    def get_delete_message(self):
        return self.delete_message % {'object': self.get_object()}

    def delete(self, request, *args, **kwargs):
        delete_message = self.get_delete_message()
        if delete_message:
            messages.success(request, delete_message)
        return super(DeleteMessageMixin, self).delete(request, *args, **kwargs)


def class_decorator(decorator):  # applies a method decorator to a class
    def inner(cls):
        orig_dispatch = cls.dispatch

        @method_decorator(decorator)
        def new_dispatch(self, request, *args, **kwargs):
            return orig_dispatch(self, request, *args, **kwargs)

        cls.dispatch = new_dispatch
        return cls

    return inner
