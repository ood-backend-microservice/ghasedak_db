from django.db import models, transaction

from _db.utility import ActiveManager


class CreateHistoryModelMixin(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    class Meta:
        abstract = True


class UpdateHistoryModelMixin(models.Model):
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )

    class Meta:
        abstract = True


class SoftDeleteModelMixin(models.Model):
    all_objects = models.Manager()
    objects = ActiveManager()

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='آیا حذف شده است؟',
        db_index=True,
    )

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)

    class Meta:
        abstract = True


class CreationSensitiveModelMixin(models.Model):
    @property
    def being_created(self):
        return not bool(self.pk)

    def after_create(self):
        """
            on_create is a simple callback function called after creating
            a new record on database. (for first time)
            this function is in a same transaction with save function
        """
        pass

    def before_create(self):
        """
            before_create is a simple callback function called before creating
            a new record on database. (for first time)
            this function is in a same transaction with save function
        """
        pass

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        with transaction.atomic():
            is_create = bool(self.being_created)
            if is_create:
                self.before_create()
            super().save(force_insert, force_update, using, update_fields)
            if is_create:
                self.after_create()

    class Meta:
        abstract = True


class BaseModel(models.Model):
    objects = models.Manager()

    @property
    def meta(self):
        return self._meta

    @property
    def instance_from_db(self):
        return self.__class__.objects.filter(pk=self.pk).first()

    @classmethod
    def get_field(cls, field):
        return cls._meta.get_field(field)

    class Meta:
        abstract = True
