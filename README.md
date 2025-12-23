# AlchemyManager

**AlchemyManager** is a lightweight Python ORM built on SQLAlchemy, inspired by Django’s ORM.
It provides Django-like model API with `objects` manager, `QuerySet`, `Q` objects, and supports **sync and async CRUD operations** with automatic session management.

---

## Features

* Django-style `Model.objects.create()`, `.get()`, `.filter()`, `.update()`, `.delete()`
* `Q` objects for complex queries with `AND`, `OR`, `NOT`, and multiple lookups (`eq`, `lt`, `gt`, `contains`, `in`)
* Supports **sync and async operations**
* Automatic session management
* Optional explicit transaction scopes (`sync_session_scope`, `async_session_scope`)
* Typed `objects` manager for IDE autocompletion and static checking
* Bulk operations (`bulk_create`)
* Works with SQLite, PostgreSQL, MySQL (via SQLAlchemy)

---

## Installation

```bash
pip install alchemy-manager
```
---

## Usage

## Full Example
```python 
from alchemy_manager import Model, init_sync_db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


if __name__ == "__main__":
    db_path = "sqlite:///test.db"
    init_sync_db(db_path)

    instance1 = User.objects.create(name="Alice", age=20)
    instance2 = User(name="Anthony", age=17).save()
    peoples = User.objects.filter(age_gte=18).all() #[User(name="Alice")]


```


### Sync operations

```python
# Create
user = User.objects.create(name="Alice", age=20)

# Get
user = User.objects.get(id=1)

# Filter
users = User.objects.filter(age__gte=18).all()

# Update
User.objects.filter(id=1).update(name="Bob")

# Delete
user.delete()

# Bulk create
User.objects.bulk_create([
    User(name="A"),
    User(name="B"),
])
```

---

### Async operations

```python
import asyncio

async def main():
    # Create
    user = await User.objects.acreate(name="Bob", age=30)

    # Get
    user = await User.objects.aget(id=1)

    # Filter
    users = await User.objects.filter(age__gte=18).aall()

    # Update
    await User.objects.filter(id=1).aupdate(name="Charlie")

    # Delete
    await user.adelete()

asyncio.run(main())
```

---

### Explicit transaction scopes

```python
from alchemy_manager import sync_session_scope, async_session_scope

# Sync
with sync_session_scope():
    user = User.objects.create(name="Scoped")
    user.save()

# Async
async with async_session_scope():
    user = await User.objects.acreate(name="AsyncScoped")
```

---

### Q object usage

```python
from alchemy_manager.queryset import Q

# Complex query
users = User.objects.filter(
    Q(age__gte=18) & ~Q(name__startswith="A")
).all()
```


## Testing

```bash
pip install pytest pytest-asyncio
pytest -v
```


## License

MIT License
