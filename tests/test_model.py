from .models import User


def test_save_and_delete():
    user = User(name="Saver", age=40)
    user.save()

    fetched = User.objects.get(id=user.id)
    assert fetched.name == "Saver"

    user.delete()

    try:
        User.objects.get(id=user.id)
        assert False
    except LookupError:
        assert True
