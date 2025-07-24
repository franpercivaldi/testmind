from app.agents.case_builder_agent import CaseBuilderAgent
from app.schemas.jira import JiraIssue
from app.schemas.test_case import TestCaseSchema

if __name__ == "__main__":
    ticket = JiraIssue(
        key="APISIUCC-100",
        summary="No se valida el email en el formulario",
        description="Al ingresar un email sin @, el sistema lo acepta igual.",
        issue_type="Bug",
        status="QA TESTING",
        labels=["login"],
        assignee="Juan Tester",
        reporter="Dev User",
        created="2024-07-01T12:00:00Z",
        updated="2024-07-05T10:00:00Z"
    )

    agent = CaseBuilderAgent()
    cases = agent.build_cases([ticket])

    print("✅ Caso generado:")
    print(cases[0].model_dump_json(indent=2))
