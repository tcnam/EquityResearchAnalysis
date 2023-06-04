import time


class ProgressBarPrinter:
    def __init__(self, width, step, stream, fname):
        self.width = width
        self.block_progress = 0
        self.current_progress = 0
        self.start_time = time.time()
        self.step = step
        self.stream = stream

        # Prints the progress bar's layout
        print(f"{fname}: [{'-' * self.width}] 0%% <0.00 seconds>",
              flush=True, end='', file=self.stream)
        print("\b" * (self.width + len("] 0%% <0.00 seconds>")),
              end='', file=self.stream)

    def update(self, progress):
        # Parsing input
        if progress is None:
            progress = self.current_progress + self.step
        if not isinstance(progress, float):
            raise TypeError("ProgressBar: input must be float or None")

        # Keep the progress bar under 99% until end() has been called
        self.current_progress = min(progress, 0.99)
        self.print_bar(self.current_progress)

    def print_bar(self, progress):
        block = int(round(self.width * progress)) - self.block_progress
        self.block_progress += block
        bar = ('#' * block) + ('-' * (self.width - self.block_progress))
        progress = int(progress * 100)
        elapsed_time = round(time.time() - self.start_time, 2)
        text = f"{bar}] {progress}% <{elapsed_time} seconds>"
        print(text + ("\b" * (len(text) - block)),
              flush=True, end='', file=self.stream)

    def end(self):
        self.print_bar(1.0)
        print(flush=True, file=self.stream)


