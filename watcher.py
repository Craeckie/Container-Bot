import docker

class Watcher:
    def __init__(self, socket_path='/var/run/docker.sock'):
        self.client = docker.DockerClient(base_url='unix://' + socket_path)

    def container_list(self):
        return self.containers.list()

    def listen_events(self, event_callback, *args, **kwargs):
        for event in self.client.events(decode=True):
            try:
                if 'status' in event and not event['status'].startswith('exec_') and event['status'] != 'pull':
                    msg = event['Actor']['Attributes']['name'] + ": " + event['status']
                    event_callback(event, msg, *args, **kwargs)
            except Exception as e:
                pass