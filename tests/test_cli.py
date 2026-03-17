"""Tests for the CLI."""

from click.testing import CliRunner

from budgetmap.cli import cli


class TestCLI:
    def setup_method(self):
        self.runner = CliRunner()

    def test_help(self):
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "BudgetMap" in result.output

    def test_summary_default(self):
        result = self.runner.invoke(cli, ["summary"])
        assert result.exit_code == 0

    def test_summary_specific_year(self):
        result = self.runner.invoke(cli, ["summary", "--year", "2020"])
        assert result.exit_code == 0

    def test_summary_invalid_year(self):
        result = self.runner.invoke(cli, ["summary", "--year", "1900"])
        assert result.exit_code == 1

    def test_compare(self):
        result = self.runner.invoke(cli, ["compare", "--year1", "2020", "--year2", "2024"])
        assert result.exit_code == 0

    def test_trends(self):
        result = self.runner.invoke(cli, ["trends"])
        assert result.exit_code == 0

    def test_trends_with_range(self):
        result = self.runner.invoke(cli, ["trends", "--start", "2021", "--end", "2023"])
        assert result.exit_code == 0

    def test_waste(self):
        result = self.runner.invoke(cli, ["waste"])
        assert result.exit_code == 0

    def test_waste_specific_year(self):
        result = self.runner.invoke(cli, ["waste", "--year", "2024"])
        assert result.exit_code == 0
