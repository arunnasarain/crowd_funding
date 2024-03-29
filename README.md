## Crowd Funding Platform

### Introduction
This project aims to develop a crowd funding platform where users can create projects, invest in them, and provide feedback. The platform provides various functionalities for managing projects, investors, investments, and feedback.

Access the sql file in `/migrations/CrowdFunding.sql`.

### Troubleshooting MySQL Connector
If facing issues with the MySQL connector related to auth plugin `Authentication plugin 'caching_sha2_password' is not supported`, follow these steps:

1. Uninstall the MySQL connector:
   ```
   pip uninstall mysql-connector
   ```
2. Uninstall MySQL Connector Python:
   ```
   pip uninstall mysql-connector-python
   ```
3. Reinstall MySQL Connector Python:
   ```
   pip install mysql-connector-python
   ```

---

### Module 1 - Task 1: Creating a New Project
Implement a POST `/project` endpoint to add a new project to the system. Users will submit project details in JSON format.

#### Input JSON
```json
{
  "title": "My Healthcare Project",
  "description": "A great healthcare initiative",
  "category": "Healthcare",
  "fundingGoal": 50000.00,
  "currentFunding": 0.00
}
```

#### Output JSON (Upon Successful Addition)
```json
{
  "id": 1,
  "title": "My Healthcare Project",
  "description": "A great healthcare initiative",
  "category": "Healthcare",
  "fundingGoal": 50000.00,
  "currentFunding": 0.00,
  "createdAt": "2023-07-22",
  "updatedAt": "2023-07-22"
}
```

---

### Module 1 - Task 2: Discovering All Projects
Implement a GET `/project` endpoint to retrieve all projects from the system.

#### Output JSON
```json
[
  {
    "id": 1,
    "title": "My Healthcare Project",
    "description": "A great healthcare initiative",
    "category": "Healthcare",
    "fundingGoal": 50000.00,
    "currentFunding": 0.00,
    "createdAt": "2023-07-22",
    "updatedAt": "2023-07-22"
  }
]
```

---

### Module 1 - Task 3: Unveiling Projects by Category
Implement a GET `/project?category={category}` endpoint to retrieve projects with a specific category.

#### Output JSON
```json
[
  {
    "id": 1,
    "title": "My Healthcare Project",
    "description": "A great healthcare initiative",
    "category": "Healthcare",
    "fundingGoal": 50000.00,
    "currentFunding": 0.00,
    "createdAt": "2023-07-22",
    "updatedAt": "2023-07-22"
  }
]
```

---

### Module 1 - Task 4: Project Details and Feedback
Implement a GET `/project/{project_id}` endpoint to retrieve project details along with feedback (if available) based on the project ID.

#### Output JSON
```json
{
  "id": 1,
  "title": "My Healthcare Project",
  "description": "A great healthcare initiative",
  "category": "Healthcare",
  "fundingGoal": 50000.00,
  "currentFunding": 0.00,
  "createdAt": "2023-07-22",
  "updatedAt": "2023-07-22",
  "feedbacks": []
}
```

---

### Module 1 - Task 5: Retrieving All Investors
Implement a GET `/investor` endpoint to retrieve information about all investors.

#### Output JSON
```json
[
  {
    "investorId": 1,
    "investorName": "John Doe",
    "email": "john.doe@example.com",
    "totalInvestedAmount": 5000.00
  },
  {
    "investorId": 2,
    "investorName": "Jane Smith",
    "email": "jane.smith@example.com",
    "totalInvestedAmount": 0.00
  },
  ...
]
```

---

### Module 1 - Task 6: Facilitating Investor Investments
Implement a POST `/investor/investment` endpoint to enable investors to make investments in projects.

#### Input JSON
```json
{
  "project_id": 1,
  "investor_id": 1,
  "amount": 5000.00
}
```

#### Output JSON (Upon Successful Investment)
```json
{
  "investmentId": 1,
  "projectId": 1,
  "investorId": 1,
  "investorName": "John Doe",
  "invetorEmail": "john.doe@example.com",
  "amountInvested": 5000.0,
  "timestamp": "2023-07-22T14:49:53.8355342"
}
```

---

### Module 1 - Task 7: Revealing Investor Contributions in Project
Implement a GET `/project/{project_id}/investments` endpoint to display a list of investors and their respective investment amounts for a specific project.

#### Output JSON
```json
{
  "projectId": 1,
  "currentFunding": 5000.00,
  "fundingGoal": 50000.00,
  "investors": [
    {
      "investorId": 1,
      "investorName": "John Doe",
      "email": "john.doe@example.com",
      "amount": 5000.00
    }
  ],
  "timestamp": "2023-07-22T14:36:37.1496922"
}
```

---

### Module 1 - Task 8: Personalized Investment Dashboard
Implement a GET `/investor/dashboard/{investor_id}` endpoint to allow investors to access their personalized dashboard.

#### Output JSON
```json
{
  "investorId": 1,
  "investorName": "John Doe",
  "email": "john.doe@example.com",
  "totalInvestedAmount": 5000,
  "projectInvestments": [
    {
      "projectId": 1,
      "title": "My Healthcare Project",
      "category": "Healthcare",
      "fundingGoal": 50000.00,
      "investedAmount": 5000.00
    }
  ]
}
```

---

### Module 1 - Task 9: Crafting Feedback and Ratings for Project
Implement a POST `/investor/{project_id}/feedback` endpoint to allow investors to provide feedback and rate projects.

#### Input JSON
```json
{
  "investorId": 1,
  "rating": 4,
  "comment": "This project looks promising!"
}
```

#### Output JSON (Upon Successful Submission)
```json
{
  "feedbackId": 1,
  "projectId": 1,
  "investorId": 1,
}
```