"""This is a hacked version  of snapcraft's go plugin.

It was modifyied to use etcd's build script.

This plugin uses the common plugin keywords as well as those for "sources".
For more information check the 'plugins' topic for the former and the
'sources' topic for the latter.

Additionally, this plugin uses the following plugin-specific keywords:

    - go-importpath:
      (string)
      This entry tells the checked out `source` to live within a certain path
      within `GOPATH`.
"""

import logging
import os
import shutil

import snapcraft
from snapcraft import common


logger = logging.getLogger(__name__)


class EtcdPlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()
        schema['properties']['go-importpath'] = {
            'type': 'string',
            'default': ''
        }
        # The import path must be specified.
        schema['required'].append('go-importpath')

        # Inform Snapcraft of the properties associated with pulling. If these
        # change in the YAML Snapcraft will consider the pull step dirty.
        schema['pull-properties'].append('go-importpath')

        # Inform Snapcraft of the properties associated with building. If these
        # change in the YAML Snapcraft will consider the build step dirty.
        schema['build-properties'].extend(['source', 'go-importpath'])
        return schema

    def __init__(self, name, options, project):
        super().__init__(name, options, project)
        self.build_packages.append('golang-go')
        self._gopath = os.path.join(self.partdir, 'go')
        self._gopath_src = os.path.join(self._gopath, 'src')
        self._gopath_bin = os.path.join(self._gopath, 'bin')

    def pull(self):
        # use -d to only download (build will happen later)
        # use -t to also get the test-deps
        # since we are not using -u the sources will stick to the
        # original checkout.
        super().pull()
        os.makedirs(self._gopath_src, exist_ok=True)

        go_package = self.options.go_importpath
        go_package_path = os.path.join(self._gopath_src, go_package)
        if os.path.islink(go_package_path):
            os.unlink(go_package_path)
        os.makedirs(os.path.dirname(go_package_path), exist_ok=True)
        os.symlink(self.sourcedir, go_package_path)
        self._run(['go', 'get', '-t', '-d', './{}/...'.format(go_package)])

    def clean_pull(self):
        super().clean_pull()

        # Remove the gopath (if present)
        if os.path.exists(self._gopath):
            shutil.rmtree(self._gopath)

    def build(self):
        super().build()
        build_command = os.path.join(
            self.options.go_importpath, 'build')
        self._run([build_command])

        install_bin_path = os.path.join(self.installdir, 'bin')
        os.makedirs(install_bin_path, exist_ok=True)
        build_bin_path = os.path.join(self._gopath_src, 'bin')
        for binary in os.listdir(build_bin_path):
            binary_path = os.path.join(build_bin_path, binary)
            shutil.copy2(binary_path, install_bin_path)

    def clean_build(self):
        super().clean_build()

        if os.path.isdir(self._gopath_bin):
            shutil.rmtree(self._gopath_bin)

    def _run(self, cmd, **kwargs):
        env = self._build_environment()
        return self.run(cmd, cwd=self._gopath_src, env=env, **kwargs)

    def _build_environment(self):
        env = os.environ.copy()
        env['GOPATH'] = self._gopath

        include_paths = []
        for root in [self.installdir, self.project.stage_dir]:
            include_paths.extend(
                common.get_library_paths(root, self.project.arch_triplet))

        flags = common.combine_paths(include_paths, '-L', ' ')
        env['CGO_LDFLAGS'] = '{} {} {}'.format(
            env.get('CGO_LDFLAGS', ''), flags, env.get('LDFLAGS', ''))

        return env
