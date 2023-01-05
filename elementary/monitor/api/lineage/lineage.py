import json
from typing import Dict, List, Optional

import networkx as nx

from elementary.clients.api.api import APIClient
from elementary.monitor.api.lineage.schema import (
    LineageNodeSchema,
    LineageSchema,
    NodeDependsOnNodesSchema,
)
from elementary.monitor.api.models.schema import (
    NormalizedArtifactSchema,
    NormalizedExposureSchema,
)


class LineageAPI(APIClient):
    def get_lineage(
        self,
        exclude_elementary_models: bool = False,
        nodes: Optional[Dict[str, NormalizedArtifactSchema]] = None,
    ) -> LineageSchema:
        lineage_graph = nx.DiGraph()
        nodes_depends_on_nodes = self._get_nodes_depends_on_nodes(
            exclude_elementary_models
        )
        for node_depends_on_nodes in nodes_depends_on_nodes:
            lineage_graph.add_edges_from(
                [
                    (node_depends_on_nodes.unique_id, depends_on_node)
                    for depends_on_node in node_depends_on_nodes.depends_on_nodes
                ]
            )
        return LineageSchema(
            nodes=[
                LineageNodeSchema(
                    type=node.type, id=node.unique_id, data=nodes.get(node.unique_id)
                )
                for node in nodes_depends_on_nodes
            ],
            edges=list(lineage_graph.edges),
            graph=lineage_graph,
        )

    def _get_nodes_depends_on_nodes(
        self, exclude_elementary_models: bool = False
    ) -> List[NodeDependsOnNodesSchema]:
        nodes_depends_on_nodes = []
        nodes_depends_on_nodes_results = self.dbt_runner.run_operation(
            macro_name="get_nodes_depends_on_nodes",
            macro_args={"exclude_elementary": exclude_elementary_models},
        )
        if nodes_depends_on_nodes_results:
            for node_depends_on_nodes_result in json.loads(
                nodes_depends_on_nodes_results[0]
            ):
                depends_on_nodes = node_depends_on_nodes_result.get("depends_on_nodes")
                nodes_depends_on_nodes.append(
                    NodeDependsOnNodesSchema(
                        unique_id=node_depends_on_nodes_result.get("unique_id"),
                        depends_on_nodes=json.loads(depends_on_nodes)
                        if depends_on_nodes
                        else None,
                        type=node_depends_on_nodes_result.get("type"),
                    )
                )
        return nodes_depends_on_nodes

    @staticmethod
    def get_downstream_exposures(
        node_unique_id: str, lineage: LineageSchema
    ) -> List[NormalizedExposureSchema]:
        try:
            downstream_nodes = lineage.graph.predecessors(node_unique_id)
        except nx.NetworkXError:
            return []

        exposures = [node for node in lineage.nodes if node.type == "exposure"]
        exposure_ids = [node.id for node in exposures]
        affected_exposure_ids = list(set(exposure_ids) & set(downstream_nodes))
        return [
            exposure.data
            for exposure in exposures
            if exposure.id in affected_exposure_ids
        ]
