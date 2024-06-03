#!/bin/sh

# SPDX-FileCopyrightText: 2024 Fraunhofer FKIE
# SPDX-FileContributor: Marten Ringwelski <git@maringuu.de>
#
# SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception

set -e

schema=$(mktemp)
schema_url="https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema"
schema_json=nvd.json

curl $schema_url > $schema
jq < $schema > $schema_json

datamodel-codegen \
    --input $schema_json \
    --input-file-type jsonschema \
    --output-model-type 'msgspec.Struct' \
    --snake-case-field \
    --keep-model-order \
    --output "."
