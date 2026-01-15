Feature: Personal Details
    As a loan applicant
    I want to enter my personal information
    So that I can proceed with my loan application


    Background:
        Given I am logged in as a new applicant


    Scenario: User can submit valid personal details
        When I enter full name "John Doe"
        And I enter national ID "CM12345678"
        And I enter email "john@example.com"
        And I enter date of birth "1990-05-15"
        And I click next
        Then I should see the loan details page


    Scenario: User cannot proceed without full name
        When I enter national ID "CM12345678"
        And I enter date of birth "1990-05-15"
        And I click next
        Then I should remain on the personal details page


    @skip
    Scenario: User cannot proceed with short full name
        When I enter full name "J"
        And I enter national ID "CM12345678"
        And I enter date of birth "1990-05-15"
        And I click next
        Then I should see the error message " "


    Scenario: User cannot proceed without national ID
        When I enter full name "John Doe"
        And I enter date of birth "1990-05-15"
        And I click next
        Then I should remain on the personal details page


    Scenario: User cannot proceed without date of birth
        When I enter full name "John Doe"
        And I enter national ID "CM12345678"
        And I enter date of birth " "
        And I click next
        Then I should remain on the personal details page


    @skip
    Scenario: User must be at least 18 years old
        When I enter full name "John Doe"
        And I enter national ID "CM12345678"
        And I enter date of birth "2015-01-01"
        And I click next
        Then I should see the error message " "


    Scenario: User can proceed without email
        When I enter full name "John Doe"
        And I enter national ID "CM12345678"
        And I enter date of birth "1990-05-15"
        And I click next
        Then I should see the loan details page


    Scenario: User cannot proceed with invalid email
        When I enter full name "John Doe"
        And I enter national ID "CM12345678"
        And I enter email "invalid-email"
        And I enter date of birth "1990-05-15"
        And I click next
        Then I should remain on the personal details page