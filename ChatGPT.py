import json
import sublime
import sublime_plugin

import urllib.request as request

settings = sublime.load_settings('ChatGPT.sublime-settings')

class ChatGptCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.show_input()

    def show_input(self):
        self.window = sublime.active_window()
        self.view = self.window.active_view()

        self.window.show_input_panel(
            'ChatGPT Request',
            self.show_input_last(),
            self.show_input_done,
            None,
            None
        )

    def show_input_last(self):
        if len(settings.get('api_key', '')) == 0:
            return 'Set the API Key first on package Settings: Menu > Preferences > Package Settingst > ChatGPT > Settings - User'

        return self.view.settings().get('show_input_last', '')

    def show_input_done(self, input_string):
        if len(settings.get('api_key', '')) == 0:
            return

        self.debug('show_input_done[input_string]', input_string)

        if len(input_string) == 0:
            return

        self.view.settings().set('show_input_last', input_string)
        self.view.run_command('insert_snippet', {'contents': self.request(input_string)})

    def request(self, input_string):
        response = self.request_response()
        data = self.request_data(input_string)
        timeout = settings.get('timeout', 10)

        self.debug('request[data]', data)

        try:
            text = request.urlopen(response, data=data, timeout=timeout).read().decode('utf-8')
            text = str(json.loads(text)['choices'][0]['text'])

            if len(text) == 0:
                text = '# No Response #'
        except Exception as e:
            text = '# Error: %s #' % str(e)

        self.debug('request[text]', text)

        return text

    def request_response(self):
        return request.Request(
            url='https://api.openai.com/v1/completions',
            method='POST',
            headers=self.request_headers()
        )

    def request_headers(self):
        return {
            'Authorization': 'Bearer %s' % settings.get('api_key'),
            'Content-Type': 'application/json'
        }

    def request_data(self, input_string):
        return json.dumps({
            'prompt': input_string,
            'model': settings.get('model', 'text-davinci-003'),
            'temperature': settings.get('temperature', 0.5),
            'max_tokens': settings.get('max_tokens', 1024)
        }).encode()

    def debug(self, key, value):
        if (settings.get('debug', False)):
            print(key, value)
