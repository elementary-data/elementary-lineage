from typing import List

from elementary.monitor.fetchers.tests.schema import TestResultDBRowSchema
from elementary.monitor.fetchers.tests.tests import TestsFetcher
from tests.mocks.dbt_runner_mock import MockDbtRunner


class MockTestsFetcher(TestsFetcher):
    def __init__(self):
        mock_dbt_runner = MockDbtRunner()
        super().__init__(mock_dbt_runner)

    def get_all_test_results_db_rows(
        self, *args, **kwargs
    ) -> List[TestResultDBRowSchema]:
        elementary_test_result_db_row = TestResultDBRowSchema(
            id="mock_id_1",
            model_unique_id="model_id_1",
            test_unique_id="test_id_1",
            elementary_unique_id="test_id_1.row_count",
            detected_at="2023-01-01 10:00:00",
            database_name="test_db",
            schema_name="test_schema",
            table_name="table",
            column_name=None,
            test_type="anomaly_detection",
            test_sub_type="row_count",
            test_results_description="This is a fine result",
            owners='["Jeff", "Joe"]',
            tags='["awesome", "awesome-o"]',
            meta='{ "subscribers": ["@jeff", "joe"], "alert_fields": ["table", "column", "description"] }',
            test_results_query="select * from table",
            other=None,
            test_name="The test 1",
            test_params='{"table_anomalies": ["row_count"], "time_bucket": {"period": "hour", "count": 1}, "model": "{{ get_where_subquery(ref(\'customers\')) }}", "sensitivity": 3, "timestamp_column": "signup_date", "backfill_days": 2}',
            severity="ERROR",
            status="fail",
            test_created_at="2023-01-01 09:00:00",
            days_diff=1,
            invocations_rank_index=1,
        )

        dbt_test_result_db_row = TestResultDBRowSchema(
            id="mock_id_2",
            model_unique_id="model_id_1",
            test_unique_id="test_id_2",
            elementary_unique_id="test_id_2.generic",
            detected_at="2023-01-01 10:00:00",
            database_name="test_db",
            schema_name="test_schema",
            table_name="table",
            column_name="column",
            test_type="dbt_test",
            test_sub_type="generic",
            test_results_description="This is a fine result",
            owners='["Jeff", "Joe"]',
            tags='["awesome", "awesome-o"]',
            meta="{}",
            test_results_query="select * from table",
            other=None,
            test_name="The test 2",
            test_params='{"column_name": "missing_column", "model": "{{ get_where_subquery(ref(\'error_model\')) }}"}',
            severity="ERROR",
            status="fail",
            test_created_at="2023-01-01 09:00:00",
            days_diff=1,
            invocations_rank_index=1,
        )
        return [elementary_test_result_db_row, dbt_test_result_db_row]
