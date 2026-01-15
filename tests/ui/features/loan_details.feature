Feature: Loan Details
    As a loan applicant
    I want to enter my loan requirements
    So that I can receive a loan decision


    Background:
        Given I am logged in and on the loan details page

    
    Scenario: User can submit valid loan details
        When I enter loan amount "50000"
        And I select loan term "30"
        And I enter purpose "Business expansion"
        And I click submit
        Then I should see the decision page

    
    Scenario: User cannot proceed without loan amount
        When I select loan term "30"
        And I enter purpose "Business expansion"
        And I click submit
        Then I should remain on the loan details page

    
    @skip
    Scenario: User cannot proceed with zero loan amount
        When I enter loan amount "0"
        And I select loan term "30"
        And I enter purpose "Business expansion"
        And I click submit
        Then I should see the error message "Loan amount must be greater than zero"

    
    Scenario: User cannot proceed without purpose
        When I enter loan amount "50000"
        And I select loan term "30"
        And I click submit
        Then I should remain on the loan details page


    Scenario Outline: User can select valid loan terms
        When I enter loan amount "50000"
        And I select loan term "<term>"
        And I enter purpose "Business need"
        And I click submit
        Then I should see the decision page

        Examples:
            | term |
            | 15   |
            | 30   |
            | 45   |
            | 60   |
