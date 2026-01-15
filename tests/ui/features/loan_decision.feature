Feature: Loan Decision
    As a loan applicant
    I want to see my application decision
    So that I know the outcome of my application


    Scenario: User sees approved decision for small loan
        Given I am a new applicant
        When I complete the application with loan amount "40000"
        Then I should see the application decision page
        And the status should be "approved"
        And I should see a congratulations message


    Scenario: User sees pending decision for high value loan
        Given I am a new applicant
        When I complete the application with loan amount "1500000"
        Then I should see the application decision page
        And the status should be "pending"


    Scenario: User sees pending decision as senior applicant
        Given I am a new applicant
        When I complete the application with date of birth "1960-01-01"
        Then I should see the application decision page
        And the status should be "pending"


    Scenario: Application summary displays correct information
        Given I am a new applicant
        When I complete the application with loan amount "40000"
        Then I should see the application decision page
        And I should see applicant name "John Doe"
        And I should see loan amount "40,000 UGX"
        And I should see loan term "30 days"


    Scenario: User can logout from decision page
        Given I have submitted a loan application
        When I click logout
        Then I should see the login page