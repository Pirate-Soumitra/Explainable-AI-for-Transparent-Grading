"""
Simulates the grading model. In a real scenario, this would be a trained ML model.
For demonstration, it uses simple keyword matching and length checks.
"""
from typing import Dict, Any
from xai_grader.rubric import RUBRIC_CRITERIA

class GradingModel:
    def __init__(self):
        pass

    def grade_essay(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates grading an essay based on extracted features and rubric.
        Returns predicted scores for each rubric criterion.
        """
        processed_text = features["processed_text"]
        word_count = features["word_count"]
        scores = {}
        detected_elements = {} # To pass to XAI for explanation

        # --- Simulate Theme Identification Grading ---
        theme_score = 0
        identified_themes = []
        missing_themes = []
        for theme_key, keywords in RUBRIC_CRITERIA["theme_identification"]["keywords"].items():
            found_any_keyword = False
            for keyword in keywords:
                if keyword in processed_text:
                    found_any_keyword = True
                    break
            if found_any_keyword:
                theme_score += 1.5 # Arbitrary score for finding a theme
                identified_themes.append(theme_key.replace('_', ' ').title())
            else:
                missing_themes.append(theme_key.replace('_', ' ').title())

        scores["theme_identification"] = min(theme_score, RUBRIC_CRITERIA["theme_identification"]["max_score"])
        detected_elements["theme_identification"] = {
            "identified": identified_themes,
            "missing": missing_themes
        }

        # --- Simulate Analysis & Support Grading ---
        # Very basic: assume longer essays have more analysis, or check for specific phrases
        analysis_score = min(word_count / 100, RUBRIC_CRITERIA["analysis_support"]["max_score"])
        scores["analysis_support"] = analysis_score
        detected_elements["analysis_support"] = {"word_count": word_count}

        # --- Simulate Structure & Clarity Grading ---
        # Very basic: assume fewer "bad" words means better clarity
        bad_words = ["badly written", "confusing"] # Placeholder for actual grammar/structure checks
        clarity_score = RUBRIC_CRITERIA["structure_clarity"]["max_score"]
        for bw in bad_words:
            if bw in processed_text:
                clarity_score -= 2 # Deduct points
        scores["structure_clarity"] = max(0, clarity_score)
        detected_elements["structure_clarity"] = {"bad_phrases_found": [bw for bw in bad_words if bw in processed_text]}

        return {"scores": scores, "detected_elements": detected_elements}