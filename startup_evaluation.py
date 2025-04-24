from dataclasses import dataclass


@dataclass
class StartupQuestion:
    question: str
    answer: str


@dataclass
class CategoryScore:
    category: str
    score: float


@dataclass
class StartupEvaluation:
    company_name: str
    company_summary: str
    questions: [StartupQuestion]
    category_scores: [CategoryScore]
    evaluation_text: str
    final_score: float
