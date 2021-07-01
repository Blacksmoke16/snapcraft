# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2020 Canonical Ltd
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

from textwrap import dedent

from testtools import TestCase
from testtools.matchers import Equals

from snapcraft.plugins.v2.crystal import CrystalPlugin

class CrystalPluginTest(TestCase):
    def test_schema(self):
        self.assertThat(
            CrystalPlugin.get_schema(),
            Equals(
                {
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "additionalProperties": False,
                    "type": "object",
                    "properties": {
                        "crystal-channel": {"type": "string", "default": "latest/stable"},
                        "crystal-build-options": {
                            "type": "array",
                            "uniqueItems": True,
                            "items": {"type": "string"},
                            "default": [],
                        },
                    },
                    "required": ["source"],
                }
            ),
        )

    def test_get_build_snaps(self):
        class Options:
            crystal_channel = "latest/edge"

        self.assertThat(
            CrystalPlugin(part_name="my-part", options=Options()).get_build_snaps(), 
            Equals({"crystal/latest/edge"})
        )

    def test_get_build_packages(self):
        self.assertThat(
            CrystalPlugin(part_name="my-part", options=lambda: None).get_build_packages(), 
            Equals({"git", "make", "gcc", "pkg-config", "libssl-dev", "libxml2-dev", "libyaml-dev", "libgmp-dev", "libpcre3-dev", "libevent-dev", "libz-dev"})
        )

    def test_get_build_environment(self):
        self.assertThat(
            CrystalPlugin(part_name="my-part", options=lambda: None).get_build_environment(), 
            Equals(dict())
        )

    def test_get_build_commands(self):
        class Options:
            crystal_channel = "latest/stable"
            crystal_build_options = []

        self.assertThat(
            CrystalPlugin(part_name="my-part", options=Options()).get_build_commands(),
            Equals(
                [
                    f'shards build --without-development ',
                    'cp -r ./bin "${SNAPCRAFT_PART_INSTALL}"/bin',
                ]
            ),
        )

    def test_get_build_commands_with_build_options(self):
        class Options:
            crystal_channel = "latest/stable"
            crystal_build_options = ['--release', '--static']

        self.assertThat(
            CrystalPlugin(part_name="my-part", options=Options()).get_build_commands(),
            Equals(
                [
                    f'shards build --without-development --release --static',
                    'cp -r ./bin "${SNAPCRAFT_PART_INSTALL}"/bin',
                ]
            ),
        )