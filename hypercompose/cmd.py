from compose import service

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

    def ensure_image_exists(self, do_build=None):
        """Hyper does not support image push pull. Its done automatically at container creation"""
        return

    def _get_container_create_options(
            self,
            override_options,
            number,
            one_off=False,
            previous_container=None):
        options = DockerService._get_container_create_options(self, override_options,
                                                              one_off, previous_container)
        del options['volumes']
        return options

    def config_dict(self):
        return {
            'options': self.options,
            'links': self.get_link_names(),
            'net': self.network_mode.id,
            'networks': self.networks,
            'volumes_from': [
                (v.source.name, v.mode)
                for v in self.volumes_from if isinstance(v.source, Service)
            ],
        }

service.Service = HyperService


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
