import json
import sublime
import sublime_plugin

import urllib.request as request

class ChatGptCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.set_settings()
        self.show_input()

    def set_settings(self):
        settings = sublime.load_settings('ChatGPT.sublime-settings')

        self.settings = {
            'api_key': str(settings.get('api_key')),
            'timeout': int(settings.get('timeout', 10)),
            'model': str(settings.get('model', 'text-davinci-003')),
            'temperature': float(settings.get('temperature', 0.5)),
            'max_tokens': int(settings.get('max_tokens', 1024)),
            'debug': bool(settings.get('debug', False))
        }

        self.debug('settings', self.settings)

    def show_input(self):
        self.window = sublime.active_window()
        self.view = self.window.active_view()

        self.window.show_input_panel(
            self.show_input_title(),
            self.show_input_value(),
            self.show_input_done,
            None,
            None
        )

    def show_input_title(self):
        return 'ChatGPT Question (model: %s | timeout: %s)' % (self.settings['model'], self.settings['timeout'])

    def show_input_value(self):
        if len(self.settings['api_key']) == 0:
            return 'You must set the API Key (Preferences > Package Settings > ChatGPT > Settings)'

        for region in self.view.sel():
            if not region.empty():
                return self.view.substr(region)

        return self.view.settings().get('show_input_last', '')

    def show_input_done(self, input_string):
        if len(self.settings['api_key']) == 0:
            return

        self.debug('show_input_done[input_string]', input_string)

        if len(input_string) == 0:
            return

        self.view.settings().set('show_input_last', input_string)

        contents = self.request(input_string).replace('\\', '\\\\').replace('$', '\\$')

        self.debug('show_input_done[contents]', contents)

        self.view.run_command('insert_snippet', {'contents': contents})

    def request(self, input_string):
        response = self.request_response()
        data = self.request_data(input_string)
        timeout = self.settings['timeout']

        self.debug('request[data]', data)

        try:
            text = request.urlopen(response, data=data, timeout=timeout).read().decode('utf-8')

            self.debug('request[response]', text)

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
            'Authorization': 'Bearer %s' % self.settings['api_key'],
            'Content-Type': 'application/json'
        }

    def request_data(self, input_string):
        return json.dumps({
            'prompt': input_string,
            'model': self.settings['model'],
            'temperature': self.settings['temperature'],
            'max_tokens': self.settings['max_tokens']
        }).encode()

    def debug(self, key, value):
        if (self.settings['debug']):
            print(key, value)
