import time

class Button:
    DELAY = 0.8
    
    def __init__(self, callback):
        self._last_time = 0
        self._callback = callback

    def click(self):
        new_time = time.time()
        if new_time < self._last_time + self.DELAY:
            return
        self._last_time = new_time
        self._callback()


class Switch:
    def __init__(self, on_switch_on, on_switch_off):
        self._is_switch_on = False
        self._on_switch_on = on_switch_on
        self._on_switch_off = on_switch_off
        self._button = Button(self._callback)

    def click(self):
        self._button.click()

    def _callback(self):
        self._is_switch_on ^= True
        if self._is_switch_on:
            self._on_switch_on()
        else:
            self._on_switch_off()