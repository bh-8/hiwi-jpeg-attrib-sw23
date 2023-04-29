from progress.bar import ShadyBar

class ProgressBar(ShadyBar):
    suffix = "%(index)03d/%(max)03d %(percent).1f%% [%(elapsed_hours)d:%(elapsed_minutes)02d:%(elapsed_seconds)02d / %(remaining_hours)d:%(remaining_minutes)02d:%(remaining_seconds)02d]"
    @property
    def remaining_hours(self):
        return self.eta // 3600
    @property
    def remaining_minutes(self):
        return (self.eta // 60) % 60
    @property
    def remaining_seconds(self):
        return self.eta % 60
    @property
    def elapsed_hours(self):
        return self.elapsed // 3600
    @property
    def elapsed_minutes(self):
        return (self.elapsed // 60) % 60
    @property
    def elapsed_seconds(self):
        return self.elapsed % 60
