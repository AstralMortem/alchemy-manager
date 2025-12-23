from .models import User
from alchemy_manager.queryset import Q


def test_filter_and_update():
    u = User.objects.create(name="Charlie", age=17)

    User.objects.filter(age__lt=18).update(is_active=False)

    updated = User.objects.get(id=u.id)
    assert updated.is_active is False


def test_delete_queryset():
    u = User.objects.create(name="Temp")
    User.objects.filter(id=u.id).delete()

    try:
        User.objects.get(id=u.id)
        assert False
    except LookupError:
        assert True


def test_q_and_or_not():
    User.objects.create(name="John", age=25)
    User.objects.create(name="Jane", age=15)

    adults = User.objects.filter(Q(age__ge=18) & Q(name__contains="Joh")).all()

    assert len(adults) == 1
    assert adults[0].name == "John"


def test_q_not():
    inactive = User.objects.filter(~Q(is_active=True)).all()
    assert isinstance(inactive, list)
