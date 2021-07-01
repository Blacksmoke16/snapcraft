# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2019 Manas.Tech
# License granted by Canonical Limited
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The Crystal plugin can be used for Crystal projects using `shards`.

This plugin uses the common plugin keywords as well as those for "sources".
For more information check the 'plugins' topic for the former and the
'sources' topic for the latter.

Additionally, this plugin uses the following plugin-specific keywords:

    - crystal-channel:
      (string, default: latest/stable)
      The Snap Store channel to install Crystal from.

    - crystal-build-options
      (list of strings, default: '[]')
      These options are passed to `shards build`.
"""

from typing import Any, Dict, List, Set

from snapcraft.plugins.v2 import PluginV2

_CRYSTAL_CHANNEL = "latest/stable"


class CrystalPlugin(PluginV2):
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        return {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "crystal-channel": {"type": "string", "default": _CRYSTAL_CHANNEL},
                "crystal-build-options": {
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"type": "string"},
                    "default": [],
                },
            },
            "required": ["source"],
        }

    def get_build_snaps(self) -> Set[str]:
        return {f"crystal/{self.options.crystal_channel}"}

    def get_build_packages(self) -> Set[str]:
        # See https://github.com/crystal-lang/distribution-scripts/blob/8bc01e26291dc518390129e15df8f757d687871c/docker/ubuntu.Dockerfile#L9
        return {
            "git",
            "make",
            "gcc",
            "pkg-config",
            "libssl-dev",
            "libxml2-dev",
            "libyaml-dev",
            "libgmp-dev",
            "libpcre3-dev",
            "libevent-dev",
            "libz-dev",
        }

    def get_build_environment(self) -> Dict[str, str]:
        return dict()

    def get_build_commands(self) -> List[str]:
        if self.options.crystal_build_options:
            build_options = " ".join(self.options.crystal_build_options)
        else:
            build_options = ""

        return [
            f"shards build --without-development {build_options}",
            'cp -r ./bin "${SNAPCRAFT_PART_INSTALL}"/bin',
        ]
