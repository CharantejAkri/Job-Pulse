import pytest
from unittest.mock import patch, MagicMock
from scraper.enrichment import extract_hr_info, calculate_match_score, find_hr_email


class TestExtractHRInfo:
    @patch("scraper.enrichment.openai.chat.completions.create")
    def test_hr_name_found(self, mock_openai):
        mock_openai.return_value.choices[0].message.content = "Priya Sharma"
        result = extract_hr_info("Contact Priya Sharma at priya@company.com")
        assert result == "Priya Sharma"

    @patch("scraper.enrichment.openai.chat.completions.create")
    def test_hr_name_not_found(self, mock_openai):
        mock_openai.return_value.choices[0].message.content = "Not Found"
        result = extract_hr_info("No HR mentioned in this description")
        assert result is None

    def test_empty_description(self):
        result = extract_hr_info("")
        assert result is None

    def test_none_description(self):
        result = extract_hr_info(None)
        assert result is None


class TestCalculateMatchScore:
    @patch("scraper.enrichment.openai.chat.completions.create")
    def test_match_score(self, mock_openai):
        mock_openai.return_value.choices[0].message.content = "85"
        result = calculate_match_score(
            "user-123", "Looking for React developer with 3 years experience"
        )
        assert result == 85.0

    def test_no_description(self):
        result = calculate_match_score("user-123", "")
        assert result is None


class TestFindHREmail:
    @patch("scraper.enrichment.httpx.get")
    def test_email_found(self, mock_httpx):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "email": "priya@techcorp.com",
                "status": "valid",
            }
        }
        mock_httpx.return_value = mock_response

        with patch("scraper.enrichment.settings") as mock_settings:
            mock_settings.HUNTER_IO_API_KEY = "test-key"
            result = find_hr_email("TechCorp Inc", "Priya Sharma")

        assert result["email"] == "priya@techcorp.com"
        assert result["verified"] is True

    def test_no_api_key(self):
        with patch("scraper.enrichment.settings") as mock_settings:
            mock_settings.HUNTER_IO_API_KEY = ""
            result = find_hr_email("TechCorp", "Priya Sharma")

        assert result["email"] is None
        assert result["verified"] is False
