"""
Unit tests for the 4-Stage Matching Engine:
- Stage 1 Hard Gate
- Stage 2 Weighted Scoring
- Stage 3 Ranking
- Stage 4 Explainability Breakdown
"""

import pytest
from backend.app.matching.hard_filter import evaluate_hard_gate
from backend.app.matching.weighted_scorer import calculate_weighted_score
from backend.app.matching.engine import evaluate_single_scheme, rank_and_match_schemes


class TestHardFilterGate:
    def test_stand_up_india_mandate_pass_female(self):
        rule = {
            "scheme_code": "STANDUP-INDIA",
            "eligible_genders": "Female",
            "eligible_categories": "SC,ST",
            "min_age": 18,
            "max_age": 70,
            "applicable_states": "All India"
        }
        profile = {"gender": "Female", "social_category": "General", "state": "Delhi", "business_stage": "ideation"}
        passed, failures, matched, missing = evaluate_hard_gate(profile, rule)
        assert passed is True
        assert len(failures) == 0

    def test_stand_up_india_mandate_fail_male_general(self):
        rule = {
            "scheme_code": "STANDUP-INDIA",
            "eligible_genders": "Female",
            "eligible_categories": "SC,ST",
            "min_age": 18,
            "max_age": 70,
            "applicable_states": "All India"
        }
        profile = {"gender": "Male", "social_category": "General", "state": "Delhi", "business_stage": "ideation"}
        passed, failures, matched, missing = evaluate_hard_gate(profile, rule)
        assert passed is False
        assert any("strictly requires" in f for f in failures)

    def test_state_specific_gate_fail(self):
        rule = {
            "scheme_code": "UP-MMYSY",
            "applicable_states": "Uttar Pradesh",
            "eligible_genders": "All",
            "eligible_categories": "All"
        }
        profile = {"state": "Maharashtra"}
        passed, failures, matched, missing = evaluate_hard_gate(profile, rule)
        assert passed is False


class TestWeightedScorer:
    def test_score_calculation(self):
        rule = {
            "weight_category": 25.0,
            "weight_gender": 20.0,
            "weight_sector": 25.0,
            "weight_location": 10.0,
            "weight_stage": 10.0,
            "weight_funding": 10.0,
            "eligible_categories": "OBC,SC,ST",
            "eligible_genders": "Female",
            "eligible_sectors": "Textiles,Manufacturing",
            "eligible_states": "All India",
            "eligible_stages": "Ideation,Startup"
        }
        profile = {
            "funding_requirement": 200000,
            "business_sector": "Textiles",
            "gender": "Female",
            "social_category": "OBC",
            "business_stage": "Ideation"
        }
        score, matched, failed = calculate_weighted_score(profile, rule)
        assert 0 <= score <= 100
        assert score >= 70  # Strong fit


class TestSchemeMatchingEngine:
    def test_evaluate_single_scheme_eligible(self):
        scheme_rule = {
            "id": 1,
            "scheme_code": "PMEGP",
            "scheme_name": "Prime Minister Employment Generation Programme",
            "scheme_description": "Credit-linked capital subsidy",
            "applicable_states": "All India",
            "eligible_genders": "All",
            "eligible_categories": "All",
            "eligible_sectors": "Manufacturing,Services,Textiles",
            "max_benefit_amount": 5000000,
            "weight_category": 20.0,
            "weight_gender": 15.0,
            "weight_sector": 25.0,
            "weight_location": 15.0,
            "weight_stage": 10.0,
            "weight_funding": 15.0
        }
        profile = {
            "gender": "Female",
            "social_category": "OBC",
            "state": "Uttar Pradesh",
            "business_sector": "Textiles",
            "funding_requirement": 500000
        }
        result = evaluate_single_scheme(profile, scheme_rule)
        assert result["eligibility_status"] == "Eligible"
        assert result["match_score"] > 50
        assert len(result["matched_criteria"]) > 0

    def test_rank_and_match_schemes_multi(self):
        schemes = [
            {
                "id": 1,
                "scheme_code": "PMEGP",
                "scheme_name": "PMEGP",
                "applicable_states": "All India",
                "eligible_genders": "All",
                "eligible_categories": "All",
                "eligible_sectors": "All",
                "max_benefit_amount": 5000000
            },
            {
                "id": 2,
                "scheme_code": "STANDUP-INDIA",
                "scheme_name": "Stand-Up India",
                "applicable_states": "All India",
                "eligible_genders": "Female",
                "eligible_categories": "SC,ST",
                "eligible_sectors": "All",
                "max_benefit_amount": 10000000
            }
        ]
        profile = {
            "gender": "Male",
            "social_category": "General",
            "state": "Delhi"
        }
        results = rank_and_match_schemes(profile, schemes)
        # Stand-Up India must be Not Eligible for Male General
        su = next(r for r in results if r["scheme_code"] == "STANDUP-INDIA")
        assert su["eligibility_status"] == "Not Eligible"
