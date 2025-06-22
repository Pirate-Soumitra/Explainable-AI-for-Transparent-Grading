"""
Main script to run the XAI Transparent Grading system.
"""
from xai_grader.input_processor import InputProcessor
from xai_grader.grading_model import GradingModel
from xai_grader.xai_explainer import XAIExplainer

def run_grading_pipeline(submission_text: str):
    """
    Runs the full grading pipeline and returns the results.
    """

    # 1. Process Input
    processor = InputProcessor()
    features = processor.extract_features(submission_text)

    # 2. Grade Submission
    grader = GradingModel()
    grading_results = grader.grade_essay(features)

    # 3. Generate Explanations
    explainer = XAIExplainer()
    explanations = explainer.generate_explanations(
        original_text=features["original_text"],
        predicted_scores=grading_results["scores"],
        detected_elements=grading_results["detected_elements"]
    )
    return explanations

def display_report_cli(explanations):
    """Displays the grading report in the command line."""
    # 4. Output Report
    print("\n--- Transparent Grade Report ---")
    print(f"Overall Grade: {explanations['overall_grade']}")
    print(f"Summary: {explanations['overall_summary']}")
    print("\nDetailed Feedback:")
    for exp_data in explanations["criterion_explanations"].values():
        print(f"\nCriterion: {exp_data['name']} ({exp_data['score']:.1f}/{exp_data['max_score']})")
        print(f"  Feedback: {exp_data['feedback']}")

    print("\n--- Grading Process Complete ---")

if __name__ == "__main__":
    sample_essay = """
    George Orwell's 1984 explores the terrifying concept of totalitarianism through the Party's absolute control. Big Brother is always watching, and the Thought Police enforce conformity. The novel also delves into the manipulation of truth, exemplified by Newspeak and the constant rewriting of history in the Ministry of Truth. Winston Smith's struggle against this oppressive regime highlights the importance of individual thought and freedom.
    """

    sample_essay_poor = """
    This book is about a guy named Winston who lives in a really bad place. There's a big brother who watches everyone. It's confusing sometimes and the writing is a bit bad.
    """

    print("Grading Sample Essay 1 (Good):")
    report1 = run_grading_pipeline(sample_essay)
    display_report_cli(report1)
    
    print("\n" + "="*50 + "\n")

    print("Grading Sample Essay 2 (Poor):")
    report2 = run_grading_pipeline(sample_essay_poor)
    display_report_cli(report2)