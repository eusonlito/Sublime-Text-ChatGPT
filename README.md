## Launch ChatGPT request from Sublime Text

This plugin connect the Sublime Text editor with the OpenAI ChatGPT using the command input panel.

Instead to write the request inside the editor, it will be written in the command palette.

The selected code will be automatically filled in the command palette so that you can complete the request.

> Remember: You can add a line break inside the command palette using the Shift + Enter key combination.

> Important: Using this plugin implies that you may be sending parts of your code to the company that manages the ChatGPT API (in this case OpenAI). It is important to keep this in mind if your code is secret or private.

> Related Packages: https://github.com/yaroslavyaroslav/OpenAI-sublime-text

### Automated Installation

Waiting for Package Control approval: https://github.com/wbond/package_control_channel/pull/8675

1. `Preferences` > `Package Control` > `Install Package`
2. Search `ChatGPT`

### Manual Installation

1. Click the `Preferences` > `Browse Packages…` menu.
2. Clone this repository inside `Packages` folder with name `ChatGPT`.
3. Restart Sublime Text.

### Settings

`Preferences` > `Package Settings` > `ChatGPT` > `Settings` to set de API KEY and default settings.

### Key Bindings

`Preferences` > `Package Settings` > `ChatGPT` > `Key Bindings` to set the command input Key Binding.

You can add this as default:

```
[
    {
        "keys": ["alt+shift+c"],
        "command": "chat_gpt"
    }
]
```
