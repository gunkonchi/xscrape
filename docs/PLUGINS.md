# Plugins

Plugins let you hook into the request lifecycle without modifying core code.

## Lifecycle hooks

| Hook | Called |
|---|---|
| `on_start` | When the client starts |
| `on_request` | Before each HTTP request |
| `on_response` | After a successful HTTP response |
| `on_parse` | After parsing a `Tweet` or `User` |
| `on_save` | Before saving to storage |
| `on_stop` | When the client stops |

## Writing a plugin

```python
from xscrape.plugins.base import Plugin

class LoggingPlugin(Plugin):
    async def on_request(self, ctx):
        print(f"-> {ctx.endpoint}")

    async def on_response(self, ctx):
        print(f"<- {ctx.status} in {ctx.duration_ms}ms")
```

## Registering

```python
from xscrape.plugins.registry import registry

registry.register(LoggingPlugin())
```

## Loading from a module

```python
registry.load("my_package.my_plugin:MyPlugin")
```
