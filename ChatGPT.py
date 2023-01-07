import json
import sublime
import sublime_plugin

import urllib.request as request

settings = sublime.load_settings('ChatGPT.sublime-settings')

def chatgpt_request():
    sublime.active_window().show_input_panel('ChatGPT Request', '', on_done, on_change, on_cancel)

def on_done(input_string):
    data = json.dumps({
        'prompt': input_string,
        'model': settings.get('model'),
        'temperature': settings.get('temperature', 0.5),
        'max_tokens': settings.get('max_tokens', 1024)
    }).encode()

    headers = {
        'Authorization': 'Bearer %s' % settings.get('api_key'),
        'Content-Type': 'application/json'
    }

    response = request.Request(
        url='https://api.openai.com/v1/completions',
        method='POST',
        headers=headers
    )

    timeout = settings.get('timeout', 10)

    try:
        text = request.urlopen(response, data, timeout=5).read().decode('utf-8')
        text = json.loads(text)['choices'][0]['text']
    except Exception as e:
        text = '# Error: %s #' % str(e)

    sublime.active_window().active_view().run_command('insert_text', {'string': text})

def on_change(input_string):
    pass

def on_cancel():
    pass

class ChatGptCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        chatgpt_request()
