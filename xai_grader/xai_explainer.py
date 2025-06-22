"""
The Explainable AI (XAI) component.
Generates human-readable explanations based on rubric scores and detected elements.
"""
from typing import Dict, Any
from xai_grader.rubric import RUBRIC_CRITERIA

class XAIExplainer:
    def __init__(self):
        pass

    def generate_explanations(
        self,
        original_text: str,
        predicted_scores: Dict[str, float],
        detected_elements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates detailed explanations for each rubric criterion.
        """
        explanations = {}
        overall_feedback = []
        total_score = 0
        max_total_score = 0

        for criterion_key, score in predicted_scores.items():
            criterion_info = RUBRIC_CRITERIA.get(criterion_key)
            if not criterion_info:
                continue

            criterion_name = criterion_info["name"]
            max_criterion_score = criterion_info["max_score"]
            total_score += score
            max_total_score += max_criterion_score

            feedback_text = ""
            # Determine score level (high, medium, low)
            score_percentage = (score / max_criterion_score) * 100

            if criterion_key == "theme_identification":
                identified = detected_elements.get(criterion_key, {}).get("identified", [])
                missing = detected_elements.get(criterion_key, {}).get("missing", [])
                
                if score_percentage >= 80:
                    feedback_text = criterion_info["feedback_rules"]["high"].format(
                        themes_identified=", ".join(identified) if identified else "various themes"
                    )
                elif score_percentage >= 40:
                    feedback_text = criterion_info["feedback_rules"]["medium"].format(
                        themes_missing=", ".join(missing) if missing else "some specific themes"
                    )
                else:
                    feedback_text = criterion_info["feedback_rules"]["low"].format(
                        themes_missing=", ".join(missing) if missing else "key themes"
                    )

            elif criterion_key == "analysis_support":
                word_count = detected_elements.get(criterion_key, {}).get("word_count", 0)
                if score_percentage >= 80:
                    feedback_text = f"Your analysis is strong and well-supported. The essay is comprehensive ({word_count} words)."
                elif score_percentage >= 40:
                    feedback_text = f"Your analysis shows potential, but could benefit from more in-depth textual evidence. Consider expanding on your points. (Word count: {word_count})."
                else:
                    feedback_text = f"The essay lacks sufficient analysis and textual support. Ensure you are directly referencing the text to back up your claims. (Word count: {word_count})."

            elif criterion_key == "structure_clarity":
                bad_phrases = detected_elements.get(criterion_key, {}).get("bad_phrases_found", [])
                if score_percentage >= 80:
                    feedback_text = "Your essay is well-structured, clear, and easy to read. Grammar and spelling are excellent."
                elif score_percentage >= 40:
                    feedback_text = f"The structure is generally clear, but there are some areas for improvement in clarity or grammar. (Detected issues: {', '.join(bad_phrases) if bad_phrases else 'none specific'})."
                else:
                    feedback_text = f"The essay's structure and clarity need significant improvement. Focus on paragraph organization, sentence structure, and proofreading. (Detected issues: {', '.join(bad_phrases) if bad_phrases else 'none specific'})."

            explanations[criterion_key] = {
                "name": criterion_name,
                "score": score,
                "max_score": max_criterion_score,
                "feedback": feedback_text
            }
            overall_feedback.append(f"- {criterion_name}: {feedback_text}")

        overall_grade = f"{total_score:.1f} / {max_total_score}"
        overall_summary = "Overall, your essay demonstrates "
        if total_score / max_total_score >= 0.8:
            overall_summary += "an excellent understanding and strong writing skills."
        elif total_score / max_total_score >= 0.5:
            overall_summary += "a good understanding, but there are areas for improvement."
        else:
            overall_summary += "areas needing significant improvement in understanding and writing."

        return {
            "overall_grade": overall_grade,
            "overall_summary": overall_summary,
            "criterion_explanations": explanations
        }