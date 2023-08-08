import requests
from datetime import datetime

current_date = datetime.now().strftime("%d/%m/%Y")


def create_linear_issue(title, description, team_id, label_ids, assignee_id):
    url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": "Bearer lin_api_SXjav6DzW08KLl3kEguWBFZW1XCNEBeOOhnLhcEp",
        "Content-Type": "application/json",
    }
    mutation = """
    mutation IssueCreate($title: String!, $description: String!, $teamId: String!, $labelIds: [String!], $assigneeId: String) {
      issueCreate(input: {
        title: $title
        description: $description
        teamId: $teamId
        labelIds: $labelIds
        assigneeId: $assigneeId
      }) {
        success
        issue {
          id
          title
        }
      }
    }
    """
    variables = {
        "title": title,
        "description": description,
        "teamId": team_id,
        "labelIds": label_ids,
        "assigneeId": assignee_id,
    }
    response = requests.post(url, json={"query": mutation, "variables": variables}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("data") and data["data"]["issueCreate"]["success"]:
            issue_id = data["data"]["issueCreate"]["issue"]["id"]
            print("Issue created with ID:", issue_id)
            return issue_id
        else:
            print("Issue creation failed.")
    else:
        print("Request failed. Status code:", response.status_code)


def create_sub_issue(title, description, parent_issue_id, label_ids, assignee_id):
    url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": "Bearer lin_api_SXjav6DzW08KLl3kEguWBFZW1XCNEBeOOhnLhcEp", 
        "Content-Type": "application/json",
    }
    mutation = """
    mutation CreateSubIssue($title: String!, $description: String!, $parentIssueId: String, $labelIds: [String!], $assigneeId: String) {
      issueCreate(input: {
        title: $title,
        description: $description,
        parentId: $parentIssueId,
        teamId: "0d322b0a-a9e5-43e5-8e84-103f8ed40c4f",
        labelIds: $labelIds,
        assigneeId: $assigneeId
      }) {
        issue {
          id
          title
          description
          createdAt
          updatedAt
        }
      }
    }
    """
    variables = {
        "title": title,
        "description": description,
        "parentIssueId": parent_issue_id,
        "labelIds": label_ids,
        "assigneeId": assignee_id,
    }
    response = requests.post(url, json={"query": mutation, "variables": variables}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("data") and data["data"]["issueCreate"]["issue"]:
            sub_issue = data["data"]["issueCreate"]["issue"]
            return sub_issue
        else:
            print("Sub-issue creation failed.")
    else:
        print("Request failed. Status code:", response.status_code)


def run_script():
    assignee_id = "1fe8ac67-4a1b-4c66-b987-15fef97f4960"
    parent_id = create_linear_issue(f"End to End Testing - {current_date}", "Run E2E tests on YFO, YYW, and YYM", "0d322b0a-a9e5-43e5-8e84-103f8ed40c4f", ["b6879697-ad7b-4fbe-9506-f4ca1e87d8a3"], assignee_id)
    if parent_id:
        print("Parent ID:", parent_id)
        sub_issue_data = [
            {"title": "Web App", "description": "Test Web App On Production", "label_ids": ["b6879697-ad7b-4fbe-9506-f4ca1e87d8a3"]},
            {"title": "Mobile App", "description": "Test Mobile App Description On Production", "label_ids": ["b6879697-ad7b-4fbe-9506-f4ca1e87d8a3"]},
            {"title": "Yebo Yes Web", "description": "Test Yebo Yes Web Description On Production", "label_ids": ["b6879697-ad7b-4fbe-9506-f4ca1e87d8a3"]},
        ]
        for data in sub_issue_data:
            title = data["title"]
            description = data["description"]
            label_ids = data["label_ids"]
            created_sub_issue = create_sub_issue(title, description, parent_id, label_ids, assignee_id)
            if created_sub_issue:
                print(f"Created Sub-issue with title '{title}':")
                print(created_sub_issue)


if __name__ == "__main__":
    run_script()
