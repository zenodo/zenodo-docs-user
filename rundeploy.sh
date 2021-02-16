#!/usr/bin/env bash
#
# Copyright (C) 2017-2021 CERN.
#
# Zenodo is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Zenodo is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zenodo; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.

cd databags
mv navigation.json navigation_local.json
ln -s navigation_deploy.json navigation.json
cd ..

# Start ssh-agent
eval $(ssh-agent -s)

# Make sure to kill the ssh-agent process on EXIT
trap "kill -9 $SSH_AGENT_PID" EXIT

mv content/ content_root/
ln -s content_root/help content

# Setup and build help pages
ssh-add -D
ssh-add - <<< "${HELP_SSH_PRIVATE_KEY}"
lektor clean --yes
lektor build
ls -l
lektor deploy ghpageshelp
rm content

# Setup and build about pages
ssh-add -D
ssh-add - <<< "${ABOUT_SSH_PRIVATE_KEY}"
ln -s content_root/about content
lektor clean --yes
lektor build
lektor deploy ghpagesabout
rm content

# Setup and build blog pages
ssh-add -D
ssh-add - <<< "${BLOG_SSH_PRIVATE_KEY}"
ln -s content_root/blog content
lektor clean --yes
lektor build
lektor deploy ghpagesblog
rm content

mv content_root/ content/
rm databags/navigation.json
mv databags/navigation_local.json databags/navigation.json
