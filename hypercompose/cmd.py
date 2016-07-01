from compose import service, volume

from api import Hyper

hyperconfig = "~/.hyper/config.json"
orig_project_from_options = None


def project_from_options(project_dir, options):
    global hyperconfig, orig_project_from_options
    if "hyperconfig" in options:
        hyperconfig = options.get("--hyperconfig")
        print "using hyper config", hyperconfig
    return orig_project_from_options(project_dir, options)

# monkey-patch docker-compose to adapt it to hyper
# we must do it before importing compose.cli

DockerService = service.Service


class HyperService(DockerService):

    def _get_container_create_options(
            self,
            override_options,
            number,
            one_off=False,
            previous_container=None):
        options = DockerService._get_container_create_options(self, override_options, number,
                                                              one_off, previous_container)
        del options['networking_config']
        options['host_config']['Binds'] = map(lambda x: x.replace(":rw", ""), options['host_config']['Binds'])
        if number > 1:
            options['hostname'] = self.name + str(self.number)
        else:
            options['hostname'] = self.name
        return options

    def image(self):
        try:
            images = self.client.images(self.image_name)
            if len(images) != 1:
                raise service.NoSuchImageError("Image '{}' not found".format(self.image_name))
            return images[0]
        except service.APIError as e:
            if e.response.status_code == 404 and e.explanation and 'No such image' in str(e.explanation):
                raise service.NoSuchImageError("Image '{}' not found".format(self.image_name))
            else:
                raise

    def connect_container_to_networks(self, container):
        pass

service.Service = HyperService


def build_container_name(project, service, number, one_off=False):
    bits = [project, service]
    if one_off:
        bits.append('run')
    return ''.join(bits + [str(number)])

service.build_container_name = build_container_name

volume.Volume.full_name = property(lambda self: self.name)


def get_client(environment, verbose=False, version=None, tls_config=None, host=None):
    return Hyper(config=hyperconfig)


additional_options = """\
      --hyperconfig FILE          Specify an alternate hyper config file (default: ~/.hyper/config.json)
"""


def main():
    from compose.cli import main as composemain
    from compose.cli import command
    global orig_project_from_options

    class TopLevelCommand(composemain.TopLevelCommand):
        __doc__ = composemain.TopLevelCommand.__doc__.replace(
            'docker-compose', "hyper-compose").replace(
            "Options:\n", "Options:\n" + additional_options)

    command.get_client = get_client

    orig_project_from_options = command.project_from_options
    command.project_from_options = project_from_options
    composemain.TopLevelCommand = TopLevelCommand
    composemain.main()
