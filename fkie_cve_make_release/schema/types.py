# SPDX-FileCopyrightText: 2024 Fraunhofer FKIE
# SPDX-FileContributor: Marten Ringwelski <git@maringuu.de>
#
# SPDX-License-Identifier: GPL-3.0-only WITH GPL-3.0-linking-exception

from msgspec import Meta
from typing_extensions import Annotated

ScoreType = Annotated[float, Meta(ge=0.0, le=10.0)]
CveId = Annotated[str, Meta(pattern='^CVE-[0-9]{4}-[0-9]{4,}$')]
