"""
Defines the rubric criteria for essay grading.
"""

RUBRIC_CRITERIA = {
    "theme_identification": {
        "name": "Theme Identification",
        "max_score": 5,
        "keywords": {
            "surveillance": ["big brother", "thought police", "telescreen"],
            "totalitarianism": ["party", "oceania", "ministry of truth", "doublethink"],
            "manipulation_of_truth": ["newspeak", "memory hole", "2+2=5"],
        },
        "feedback_rules": {
            "high": "Excellent identification of key themes like {themes_identified}.",
            "medium": "You identified some themes, but could elaborate more on {themes_missing}.",
            "low": "Key themes were largely missed. Consider discussing {themes_missing}.",
        }
    },
    "analysis_support": {
        "name": "Analysis & Support",
        "max_score": 5,
    },
    "structure_clarity": {
        "name": "Structure & Clarity",
        "max_score": 5,
    },
}