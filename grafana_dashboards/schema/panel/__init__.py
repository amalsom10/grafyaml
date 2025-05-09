# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import voluptuous as v

from grafana_dashboards.schema.panel.base import Base
from grafana_dashboards.schema.panel.dashlist import Dashlist
from grafana_dashboards.schema.panel.graph import Graph
from grafana_dashboards.schema.panel.logs import Logs
from grafana_dashboards.schema.panel.singlestat import Singlestat
from grafana_dashboards.schema.panel.stat import Stat
from grafana_dashboards.schema.panel.text import Text
from grafana_dashboards.schema.panel.table import Table
from grafana_dashboards.schema.panel.gauge import Gauge
from grafana_dashboards.schema.panel.bargauge import Bargauge
from grafana_dashboards.schema.panel.timeseries import Timeseries
from grafana_dashboards.schema.panel.piechart import PieChart
from grafana_dashboards.schema.panel.statetimeline import StateTimeline


class Panel(object):
    def __init__(self, usingNewSchema=False):
        self.usingNewSchema = usingNewSchema

    def validate_individually(self, panel: dict):
        validate = Base().get_schema()
        validate(panel)

        if panel["type"] == "dashlist":
            schema = Dashlist(usingNewSchema=self.usingNewSchema).get_schema()
        elif panel["type"] == "graph":
            schema = Graph(usingNewSchema=self.usingNewSchema).get_schema()
        elif panel["type"] == "logs":
            schema = Logs(usingNewSchema=self.usingNewSchema).get_schema()
        elif panel["type"] == "singlestat":
            schema = Singlestat(usingNewSchema=self.usingNewSchema).get_schema()
        elif panel["type"] == "stat":
            schema = Stat(usingNewSchema=self.usingNewSchema).get_schema()
        elif panel["type"] == "text":
            schema = Text().get_schema()
        elif panel["type"] == "table":
            schema = Table(usingNewSchema=self.usingNewSchema).get_schema()
        elif panel["type"] == "gauge":
            schema = Gauge(usingNewSchema=self.usingNewSchema).get_schema()
        elif panel["type"] == "bargauge":
            schema = Bargauge(usingNewSchema=self.usingNewSchema).get_schema()
        elif panel["type"] == "timeseries":
            schema = Timeseries().get_schema()
        elif panel["type"] == "piechart":
            schema = PieChart().get_schema()
        elif panel["type"] == "state-timeline":
            schema = StateTimeline().get_schema()

        return schema(panel)

    def _validate(self):
        def f(data):
            if not isinstance(data, list):
                raise v.Invalid("Should be a list")

            return [self.validate_individually(panel) for panel in data]

        return f

    def get_schema(self):
        schema = v.Schema(
            {
                v.Required("panels", default=[]): v.All(self._validate()),
            }
        )

        return schema
