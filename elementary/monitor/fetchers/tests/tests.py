import json
from typing import List, Optional

from elementary.clients.dbt.base_dbt_runner import BaseDbtRunner
from elementary.clients.fetcher.fetcher import FetcherClient
from elementary.monitor.fetchers.tests.schema import (
    SourceFreshnessResultDBRowSchema,
    TestResultDBRowSchema,
)
from elementary.utils.log import get_logger

logger = get_logger(__name__)


class TestsFetcher(FetcherClient):
    def __init__(self, dbt_runner: BaseDbtRunner):
        super().__init__(dbt_runner)

    def get_all_test_results_db_rows(
        self,
        days_back: Optional[int] = 7,
        invocations_per_test: int = 720,
        disable_passed_test_metrics: bool = False,
    ) -> List[TestResultDBRowSchema]:
        run_operation_response = self.dbt_runner.run_operation(
            macro_name="elementary_cli.get_test_results",
            macro_args=dict(
                days_back=days_back,
                invocations_per_test=invocations_per_test,
                disable_passed_test_metrics=disable_passed_test_metrics,
            ),
        )
        test_results = (
            json.loads(run_operation_response[0]) if run_operation_response else []
        )
        test_results = [
            TestResultDBRowSchema(**test_result) for test_result in test_results
        ]
        return test_results

    def get_source_freshness_results_db_rows(
        self,
        days_back: Optional[int] = 7,
        invocations_per_test: int = 720,
    ) -> List[SourceFreshnessResultDBRowSchema]:
        run_operation_response = self.dbt_runner.run_operation(
            macro_name="elementary_cli.get_source_freshness_results",
            macro_args=dict(
                days_back=days_back,
                invocations_per_test=invocations_per_test,
            ),
        )
        source_freshness_results = (
            json.loads(run_operation_response[0]) if run_operation_response else []
        )
        source_freshness_results = [
            SourceFreshnessResultDBRowSchema(**source_freshness_result)
            for source_freshness_result in source_freshness_results
        ]
        return source_freshness_results
